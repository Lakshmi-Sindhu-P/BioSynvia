"""Profile numeric distinct values and original sensor Status categories."""

import argparse
from collections import Counter, defaultdict
import gzip
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


def profile(archive, out):
    if out.exists():
        raise ValueError("Choose a new output directory.")
    source = inventory_archive(archive)
    out.mkdir(parents=True)
    arrays = defaultdict(list)
    status_rows = []
    with zipfile.ZipFile(archive) as z:
        for item in source["files"]:
            if item["path"].endswith(".csv"):
                df = pd.read_csv(io.BytesIO(z.read(item["path"])))
                for col in df:
                    arr = pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
                    arrays[(item["measurement_kind"], col)].append(arr)
            elif item["path"].endswith(".xlsx"):
                wb = openpyxl.load_workbook(io.BytesIO(z.read(item["path"])), read_only=True, data_only=True)
                for sheet in wb:
                    header = next(sheet.iter_rows(min_row=1, max_row=1, values_only=True))
                    if "Status" not in header:
                        continue
                    index = list(header).index("Status") + 1
                    counts = Counter()
                    for (value,) in sheet.iter_rows(min_row=2, min_col=index, max_col=index, values_only=True):
                        counts[str(value) if value is not None else "<blank>"] += 1
                    for status, count in counts.items():
                        status_rows.append({"experiment": item["experiment_id"], "sheet": sheet.title,
                                            "status": status, "rows": count})
                wb.close()
                print(f"Read all Status values in {item['experiment_id']}", flush=True)
    rows = []
    full_values = out / "numeric_distinct_values.json.gz"
    with gzip.open(full_values, "wt", encoding="utf-8") as handle:
        handle.write("[\n")
        for n, ((kind, field), parts) in enumerate(sorted(arrays.items())):
            values = np.concatenate(parts)
            finite = values[np.isfinite(values)]
            unique, counts = np.unique(finite, return_counts=True)
            top = np.argsort(-counts, kind="stable")[:5]
            rows.append({"kind": kind, "field": field, "cells": len(values), "finite_cells": len(finite),
                         "nonfinite_or_missing": len(values) - len(finite), "distinct_numeric_values": len(unique),
                         "minimum": float(unique[0]) if len(unique) else None,
                         "maximum": float(unique[-1]) if len(unique) else None,
                         "top_values_and_counts": json.dumps([{ "value": float(unique[i]), "count": int(counts[i])}
                                                               for i in top]),
                         "all_values_if_at_most_12": json.dumps(unique.tolist()) if len(unique) <= 12 else "see compressed value list"})
            if n:
                handle.write(",\n")
            json.dump({"kind": kind, "field": field, "values": unique.tolist()}, handle, allow_nan=False)
        handle.write("\n]\n")
    pd.DataFrame(rows).to_csv(out / "numeric_unique_counts.csv", index=False)
    pd.DataFrame(status_rows).to_csv(out / "raw_sensor_status_counts.csv", index=False)
    global_status = Counter()
    for row in status_rows:
        global_status[row["status"]] += row["rows"]
    categories = {"experiment_ids": sorted(source["experiment_structure"]["experiment_modes"]),
                  "reactor_ids_within_experiment": ["R01", "R02"],
                  "process_modes": sorted(source["experiment_structure"]["mode_counts"]),
                  "aligned_measurement_kinds": ["inline", "offline"],
                  "raw_status_values_and_row_counts": dict(sorted(global_status.items())),
                  "status_streams_scanned": len({(row["experiment"], row["sheet"]) for row in status_rows}),
                  "archive_sha256": source["sha256"],
                  "numeric_uniqueness_method": "Exact equality after numeric float64 parsing; missing/nonfinite excluded. "
                                               "No tolerance binning or raw-text distinctness.",
                  "status_scope": "All Status-column rows in all 12 original workbooks. Counts are sensor records, not independent experiments.",
                  "time_scope": "Elapsed time values counted within each modality across all runs; equal times from different runs are not joined."}
    (out / "categorical_values.json").write_text(json.dumps(categories, indent=2) + "\n")
    print(json.dumps(categories, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=Path("data/raw/Dataset.zip"))
    parser.add_argument("--output", type=Path, default=Path("reports/unique-values"))
    args = parser.parse_args()
    profile(args.archive, args.output)
