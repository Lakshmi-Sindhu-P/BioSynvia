"""Reproduce targeted source/quality investigations before modeling."""

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

import numpy as np
import openpyxl
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from biosynvia.source import inventory_archive


def investigate(archive, output):
    if output.exists():
        raise ValueError("Choose a new output directory to preserve earlier evidence.")
    manifest = inventory_archive(archive)
    output.mkdir(parents=True)
    profiles, statuses, zeros, support, cells, transitions = [], [], [], [], [], []
    for exp, mode in [("EXP011", "fed-batch"), ("EXP002", "batch")]:
        with zipfile.ZipFile(archive) as z:
            source_name = f"Individual raw data tables/{exp}_{mode}.xlsx"
            raw = z.read(source_name)
            digest = hashlib.sha256(raw).hexdigest()
            wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=False)
            raw_streams = {}
            for sheet in wb:
                rows = sheet.iter_rows(values_only=True)
                headers = next(rows)
                df = pd.DataFrame(rows, columns=headers).dropna(how="all")
                t = pd.to_numeric(df["Time (h)"], errors="coerce")
                dt = t.diff()
                reactor = sheet.title[:3]
                if "offline" not in sheet.title:
                    raw_streams[sheet.title] = df
                count = Counter(str(value) if pd.notna(value) else "<blank>" for value in df["Status"]) if "Status" in df else {}
                profile = {"experiment": exp, "reactor": reactor, "sheet": sheet.title,
                           "source_file": source_name, "source_sha256": digest,
                           "rows": len(df), "first_hour": t.min(), "last_hour": t.max(),
                           "invalid_times": int((~np.isfinite(t)).sum()),
                           "duplicates": int(t.duplicated().sum()), "backwards_steps": int((dt < 0).sum()),
                           "largest_gap_hours": dt.max(), "rows_after_67_1333h": int((t > 67.1333333334).sum()),
                           "has_status_field": "Status" in df,
                           "last_status": str(df["Status"].iloc[-1]) if "Status" in df else None}
                profiles.append(profile)
                for value, n in count.items():
                    statuses.append({"experiment": exp, "sheet": sheet.title, "status": value, "rows": n})
                if "Status" in df:
                    changed = df["Status"].ne(df["Status"].shift())
                    for idx in df.index[changed]:
                        transitions.append({"experiment": exp, "sheet": sheet.title,
                                            "time_hours": float(t.loc[idx]), "new_status": str(df.loc[idx, "Status"])})
                if sheet.title == "R02_offline_CellAnalysis":
                    label = pd.to_numeric(df["VCD Mean (cells/mL)"], errors="coerce")
                    for idx in df.index[label.eq(0)]:
                        record = df.loc[idx]
                        zero = {"experiment": exp, "reactor": "R02", "time_hours": float(record["Time (h)"]),
                                "VCD": float(record["VCD Mean (cells/mL)"]),
                                "VCD_SEM": float(record["VCD SEM (cells/mL)"]),
                                "TCD": float(record["TCD Mean (cells/mL)"]),
                                "viability_percent": float(record["Viability Mean (%)"]),
                                "viability_SEM": float(record["Viability SEM (%)"]),
                                "source_file": source_name, "source_sheet": sheet.title,
                                "source_excel_row": int(idx) + 2, "source_digest": digest,
                                "source_has_assay_status_column": "Status" in df,
                                "quality_status": "recorded_zero_pending_assay_review",
                                "label_approved": False}
                        zeros.append(zero)
                        for col in ["VCD Mean (cells/mL)", "VCD SEM (cells/mL)", "Viability Mean (%)"]:
                            col_num = list(headers).index(col) + 1
                            cell = sheet.cell(row=int(idx) + 2, column=col_num)
                            cells.append({"experiment": exp, "sheet": sheet.title, "cell": cell.coordinate,
                                          "field": col, "value": cell.value, "excel_type": cell.data_type})
            wb.close()
            inline_name = f"Time-axis aligned raw data tables/{exp}_{mode}_R02_inline.csv"
            aligned = pd.read_csv(io.BytesIO(z.read(inline_name)))
            offline_name = f"Time-axis aligned raw data tables/{exp}_{mode}_R02_offline.csv"
            assays = pd.read_csv(io.BytesIO(z.read(offline_name)))
            aligned_times = aligned["Time (h)"].to_numpy()
            for _, assay in assays.iterrows():
                cutoff = float(assay["Time (h)"])
                for name, df in raw_streams.items():
                    if not name.startswith("R02_"):
                        continue
                    times = pd.to_numeric(df["Time (h)"], errors="coerce").to_numpy()
                    valid = np.isfinite(times) & (times <= cutoff)
                    # Select the latest time, independent of worksheet row ordering.
                    prior = np.flatnonzero(valid)
                    pos = prior[np.argmax(times[prior])] if len(prior) else None
                    support.append({"experiment": exp, "reactor": "R02", "assay_time_hours": cutoff,
                                    "VCD": float(assay["VCD Mean (cells/mL)"]), "stream": name,
                                    "last_prior_hour": float(times[pos]) if pos is not None else None,
                                    "age_hours": float(cutoff - times[pos]) if pos is not None else None,
                                    "after_stream_end": bool(cutoff > np.nanmax(times) + 1e-8),
                                    "prior_status": str(df.iloc[pos]["Status"]) if pos is not None and "Status" in df else None,
                                    "status_scope": "sensor_stream_only_not_assay_quality"})
                prior = aligned_times[aligned_times <= cutoff]
                support.append({"experiment": exp, "reactor": "R02", "assay_time_hours": cutoff,
                                "VCD": float(assay["VCD Mean (cells/mL)"]), "stream": "aligned_inline_all_fields",
                                "last_prior_hour": float(prior[-1]) if len(prior) else None,
                                "age_hours": float(cutoff - prior[-1]) if len(prior) else None,
                                "after_stream_end": bool(cutoff > aligned_times[-1] + 1e-8),
                                "prior_status": None, "status_scope": "not_exported"})
            print(f"Inspected every row of {exp}'s 16 original sheets", flush=True)
    for name, records in [("stream_profiles", profiles), ("sensor_status_counts", statuses),
                          ("sensor_status_transitions", transitions), ("recorded_zero_vcd", zeros),
                          ("zero_source_cells", cells), ("assay_stream_support", support)]:
        pd.DataFrame(records).to_csv(output / (name + ".csv"), index=False)
    issue_register = {
        "source_archive_sha256": manifest["sha256"],
        "scope": "Every row of every sheet in EXP002 and EXP011 only; all six VCD zeros in those workbooks.",
        "issues": [
            {"id": "DQ-001", "status": "open", "question": "Why is EXP011 R02 aligned inline coverage truncated?",
             "policy": "No extension of all-channel aligned coverage by forward-fill; review per-stream raw availability."},
            {"id": "DQ-002", "status": "open", "question": "What assay/detection/QC interpretation applies to six recorded zero VCDs?",
             "policy": "Preserve original numeric zeros; quality pending; no approved training-label designation."},
            {"id": "DQ-003", "status": "open", "question": "What do raw sensor status categories permit for modeling?",
             "policy": "Preserve stream statuses; sensor Ok is not evidence that an offline assay is valid."}],
        "limits": ["No source values were altered.", "No labels scientifically approved.",
                   "No source resampling algorithm or assay detection limit inferred.",
                   "Only these two workbooks were exhaustively status-profiled."]}
    (output / "issue_register.json").write_text(json.dumps(issue_register, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=Path("data/raw/Dataset.zip"))
    parser.add_argument("--output", type=Path, default=Path("reports/quality-review"))
    args = parser.parse_args()
    investigate(args.archive, args.output)
