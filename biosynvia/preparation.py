"""Saved, raw-aware inspection datasets. Requires optional pandas/openpyxl."""

from hashlib import sha256
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import re
import shutil
import sqlite3
import zipfile

import numpy as np
import openpyxl
import pandas as pd

from .source import inventory_archive


CORE_FIELDS = ["Dissolved CO2 (%-sat)", "Transmission (arb. Unit)",
               "Reflection (arb. Unit)", "Conductivity (mS/cm)", "Permittivity (pF/cm)",
               "pH", "Dissolved O2 (% air sat)", "Temperature (°C)"]
TARGET = "VCD Mean (cells/mL)"


def fingerprint(path):
    with Path(path).open("rb") as handle:
        return sha256(handle.read()).hexdigest()


def backup_archive(source, directory):
    """Create/reuse a checksum-verified separate backup; never overwrite it."""
    source = Path(source)
    digest = fingerprint(source)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"Dataset_{digest[:16]}.zip"
    if target.exists():
        if fingerprint(target) != digest:
            raise ValueError("Existing backup differs from source; refusing overwrite.")
    else:
        with source.open("rb") as original, target.open("xb") as copy:
            shutil.copyfileobj(original, copy)
        if fingerprint(target) != digest:
            raise ValueError("Backup verification failed.")
    return target, digest


def numeric_copy(original):
    """Return a deep working copy plus type/missingness audit, without imputation."""
    working = original.copy(deep=True)
    audit = []
    for field in working:
        parsed = pd.to_numeric(working[field], errors="coerce")
        finite = parsed.where(np.isfinite(parsed))
        audit.append({"field": field, "imported_dtype": str(original[field].dtype),
                      "working_dtype": "float64", "source_nulls": int(original[field].isna().sum()),
                      "new_invalid_or_nonfinite": int((finite.isna() & original[field].notna()).sum()),
                      "unique_finite": int(finite.nunique()), "working_nulls": int(finite.isna().sum())})
        working[field] = finite.astype(float)
    return working, audit


def feature_id(field):
    return "x__" + re.sub(r"[^a-z0-9]+", "_", field.lower()).strip("_")


def snapshot_stream(original, assay_times, max_age_hours):
    """Acquire latest prior row only; keep source value and rejection reason."""
    fields = [field for field in original if field not in ("Time (h)", "Status")]
    working, _ = numeric_copy(original[["Time (h)", *fields]])
    working["source_row"] = np.arange(len(original)) + 2
    working["source_status"] = original["Status"].to_numpy() if "Status" in original else "not_provided"
    working = working[np.isfinite(working["Time (h)"])].sort_values("Time (h)", kind="stable")
    duplicate_times = set(working.loc[working["Time (h)"].duplicated(keep=False), "Time (h)"])
    times = working["Time (h)"].to_numpy()
    constant_zero_history = {field: working[field].eq(0).cummin().to_numpy()
                             for field in fields
                             if field.startswith(("C (", "fc (", "Alpha", "DeltaEps", "Fitting "))}
    records = []
    for index, cutoff in enumerate(assay_times):
        pos = np.searchsorted(times, cutoff, side="right") - 1
        row = working.iloc[pos] if pos >= 0 else None
        ambiguous = row is not None and row["Time (h)"] in duplicate_times
        for field in fields:
            value = float(row[field]) if row is not None and pd.notna(row[field]) else None
            age = float(cutoff - row["Time (h)"]) if row is not None else None
            status = row["source_status"] if row is not None else None
            reason = "usable_for_inspection"
            if row is None:
                reason = "no_past_observation"
            elif ambiguous:
                reason = "duplicate_source_time_requires_review"
            elif age > max_age_hours + 1e-10:
                reason = "stale"
            elif "Status" in original and (pd.isna(status) or status != "Ok"):
                reason = "sensor_status_requires_review"
            elif value is None:
                reason = "invalid_or_missing_value"
            # Do not use inactive fitted-channel zeros as though informative.
            elif field in constant_zero_history and constant_zero_history[field][pos]:
                reason = "constant_zero_derived_channel"
            alternatives = []
            if ambiguous:
                for _, candidate in working[working["Time (h)"].eq(row["Time (h)"])].iterrows():
                    alternatives.append({"source_excel_row": int(candidate["source_row"]),
                                         "value": float(candidate[field]) if pd.notna(candidate[field]) else None,
                                         "status": str(candidate["source_status"]) if pd.notna(candidate["source_status"]) else None})
            records.append({"assay_position": index, "field": field, "feature": feature_id(field),
                            "source_value": value if not ambiguous else None,
                            "inspection_value": value if reason == "usable_for_inspection" else None,
                            "source_time_hours": float(row["Time (h)"]) if row is not None else None,
                            "source_excel_row": int(row["source_row"]) if row is not None and not ambiguous else None,
                            "source_candidates_json": json.dumps(alternatives),
                            "age_hours": age, "source_status": status if pd.notna(status) and not ambiguous else None,
                            "reason": reason})
    return records


def combine_original_assays(cell_original, medium_original):
    cell, cell_audit = numeric_copy(cell_original)
    medium, medium_audit = numeric_copy(medium_original)
    if cell["Time (h)"].isna().any() or medium["Time (h)"].isna().any():
        raise ValueError("Original assay has invalid time.")
    # Preserve a missing modality at its own measured timestamp, never interpolate.
    merged = cell.merge(medium, on="Time (h)", how="outer", validate="one_to_one").sort_values("Time (h)")
    merged["target_review_required"] = merged[TARGET].isna() | (merged[TARGET] <= 0)
    merged["target_review_reason"] = np.select(
        [merged[TARGET].isna(), merged[TARGET].eq(0), merged[TARGET].lt(0)],
        ["missing_target", "recorded_zero_pending_assay_review", "negative_target_pending_review"], default="routine_review_pending")
    merged["scientific_label_approved"] = False
    return merged.reset_index(drop=True), cell_audit + medium_audit


def save_table(frame, name, output, connection):
    frame.to_csv(output / f"{name}.csv", index=False)
    frame.to_sql(name, connection, index=False, if_exists="fail", chunksize=500)


def prepare(archive, backup_directory, output, max_age_minutes=5):
    archive, output = Path(archive), Path(output)
    if output.exists() or output.with_name(output.name + ".incomplete").exists():
        raise ValueError("Choose a new versioned output directory.")
    if not np.isfinite(max_age_minutes) or max_age_minutes <= 0:
        raise ValueError("Maximum sensor age must be positive and finite.")
    source = inventory_archive(archive)
    if source["warnings"]:
        raise ValueError("Source inventory has unresolved structure warnings.")
    backup, original_hash = backup_archive(archive, Path(backup_directory))
    stage = output.with_name(output.name + ".incomplete")
    stage.mkdir(parents=True)
    tables = {"inline": [], "offline": []}
    audits, descriptions, sizes, assay_frames, features, source_issues = [], [], [], [], [], []
    dictionary = {}
    with zipfile.ZipFile(backup) as z:
        for item in source["files"]:
            if not item["path"].endswith(".csv"):
                continue
            original_df = pd.read_csv(io.BytesIO(z.read(item["path"])))
            working_df, audit = numeric_copy(original_df)
            run = f"{item['experiment_id']}_{item['reactor_id']}"
            for row in audit:
                audits.append({"source_file": item["path"], "kind": item["measurement_kind"], **row})
            desc = working_df.describe().T.reset_index(names="field")
            desc["source_file"] = item["path"]
            descriptions.append(desc)
            sizes.append({"source_file": item["path"], "rows": len(original_df), "columns": len(original_df.columns),
                          "original_dataframe_bytes": int(original_df.memory_usage(deep=True).sum()),
                          "working_dataframe_bytes": int(working_df.memory_usage(deep=True).sum())})
            working_df["experiment_id"] = item["experiment_id"]
            working_df["reactor_id"] = item["reactor_id"]
            working_df["run_id"] = run
            working_df["process_mode"] = item["process_mode"]
            working_df["source_file"] = item["path"]
            tables[item["measurement_kind"]].append(working_df)
        for item in source["files"]:
            if not item["path"].endswith(".xlsx"):
                continue
            raw = z.read(item["path"])
            digest = sha256(raw).hexdigest()
            wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
            for reactor in ("R01", "R02"):
                def load_sheet(name):
                    rows = wb[name].iter_rows(values_only=True)
                    return pd.DataFrame(rows, columns=next(rows)).dropna(how="all")
                cell = load_sheet(f"{reactor}_offline_CellAnalysis")
                medium = load_sheet(f"{reactor}_offline_MediumAnalysis")
                assays, audit = combine_original_assays(cell, medium)
                for row in audit:
                    audits.append({"source_file": item["path"], "kind": "original_offline", **row})
                run = f"{item['experiment_id']}_{reactor}"
                assays["experiment_id"] = item["experiment_id"]
                assays["reactor_id"] = reactor
                assays["run_id"] = run
                assays["process_mode"] = item["process_mode"]
                assays["source_file"] = item["path"]
                assays["source_sha256"] = digest
                assays["assay_id"] = [f"{run}_assay_{i:03}" for i in range(len(assays))]
                assay_frames.append(assays)
                for name in wb.sheetnames:
                    if not name.startswith(reactor + "_") or "_offline_" in name:
                        continue
                    raw_df = load_sheet(name)
                    _, raw_audit = numeric_copy(raw_df.drop(columns=["Status"], errors="ignore"))
                    for row in raw_audit:
                        audits.append({"source_file": item["path"] + "::" + name, "kind": "original_sensor", **row})
                    raw_times = pd.to_numeric(raw_df["Time (h)"], errors="coerce")
                    if raw_times.duplicated(keep=False).any():
                        source_issues.append({"source_file": item["path"], "source_sheet": name,
                                              "issue": "duplicate_source_timestamps",
                                              "involved_rows": int(raw_times.duplicated(keep=False).sum())})
                    for row in snapshot_stream(raw_df, assays["Time (h)"].to_numpy(), max_age_minutes / 60):
                        row.update(assay_id=assays.iloc[row.pop("assay_position")]["assay_id"],
                                   run_id=run, experiment_id=item["experiment_id"], source_sheet=name,
                                   source_file=item["path"], source_sha256=digest)
                        features.append(row)
                        dictionary[row["feature"]] = {"feature": row["feature"], "original_field": row["field"],
                                                       "role": "input_candidate", "unit_status": "header_only_pending_review",
                                                       "core_inspection_feature": row["field"] in CORE_FIELDS}
            wb.close()
            print(f"Copied and inspected original streams: {item['experiment_id']}", flush=True)

    combined = {kind: pd.concat(parts, ignore_index=True) for kind, parts in tables.items()}
    assays = pd.concat(assay_frames, ignore_index=True)
    long_features = pd.DataFrame(features)
    wide = long_features.pivot(index="assay_id", columns="feature", values="inspection_value")
    processed = assays[["assay_id", "experiment_id", "reactor_id", "run_id", "process_mode", "Time (h)",
                        "target_review_required", "target_review_reason", "scientific_label_approved"]].copy(deep=True)
    processed["y__vcd_cells_per_ml"] = assays[TARGET]
    processed["process_mode_code"] = processed.process_mode.map({"batch": 0, "fed-batch": 1}).astype(int)
    processed = processed.merge(wide, on="assay_id", validate="one_to_one")
    core = [feature_id(field) for field in CORE_FIELDS]
    processed["core_features_complete"] = processed[core].notna().all(axis=1)
    processed["inspection_candidate"] = ~processed.target_review_required & processed.core_features_complete
    inspection = processed.loc[processed.inspection_candidate, ["assay_id", "experiment_id", "run_id", "Time (h)",
                               "y__vcd_cells_per_ml", *core]].copy(deep=True)
    connection = sqlite3.connect(stage / "biosynvia.sqlite")
    try:
        for frame, name in [(combined["inline"], "combined_inline"), (combined["offline"], "aligned_offline"),
                            (assays, "original_offline"), (long_features, "feature_lineage"),
                            (processed, "processed_candidates"), (inspection, "inspection_subset")]:
            save_table(frame, name, stage, connection)
        connection.execute('CREATE INDEX inline_run_time ON combined_inline (run_id, "Time (h)")')
        connection.execute('CREATE INDEX assay_run_time ON original_offline (run_id, "Time (h)")')
        connection.execute('CREATE INDEX lineage_assay ON feature_lineage (assay_id, feature)')
        connection.commit()
    finally:
        connection.close()
    pd.DataFrame(audits).to_csv(stage / "datatype_null_unique_audit.csv", index=False)
    pd.concat(descriptions).to_csv(stage / "source_descriptive_statistics.csv", index=False)
    pd.DataFrame(sizes).to_csv(stage / "dataframe_sizes.csv", index=False)
    pd.DataFrame(dictionary.values()).to_csv(stage / "feature_dictionary.csv", index=False)
    (stage / "source_issues.json").write_text(json.dumps(source_issues, indent=2) + "\n")
    correlations(processed, stage)
    summary = {"status": "prepared_for_inspection_not_approved_for_training", "source_sha256": original_hash,
               "producer_code_sha256": fingerprint(Path(__file__)),
               "created_at_utc": datetime.now(timezone.utc).isoformat(),
               "backup_path": str(backup.resolve()), "backup_sha256": fingerprint(backup),
               "combined_inline_rows": len(combined["inline"]), "aligned_offline_rows": len(combined["offline"]),
               "original_offline_rows": len(assays), "processed_candidate_rows": len(processed),
               "inspection_subset_rows": len(inspection), "recorded_zero_targets": int(assays[TARGET].eq(0).sum()),
               "original_assay_missing_cells": int(assays[list(cell.columns[1:]) + list(medium.columns[1:])].isna().sum().sum()),
               "max_age_minutes": max_age_minutes, "age_policy_approval": "pending_scientific_review",
               "availability_assumption": "Acquisition time used for retrospective inspection; result availability unknown.",
               "feature_selection": "Eight domain-motivated core inspection fields; correlations do not select/drop fields.",
               "target_approved": False, "split_approved": False, "model_fit_permitted": False,
               "null_policy": "Preserve missing values; no fitted imputation, interpolation or scaling.",
               "encoding": {"batch": 0, "fed-batch": 1}, "encoded_mode_role": "context_only_not_default_model_input",
               "outputs": {file.name: {"bytes": file.stat().st_size, "sha256": fingerprint(file)}
                           for file in stage.iterdir() if file.is_file()}}
    (stage / "preparation_manifest.json").write_text(json.dumps(summary, indent=2) + "\n")
    if fingerprint(archive) != original_hash:
        raise ValueError("Source fingerprint changed during preparation.")
    stage.rename(output)
    print(json.dumps({key: value for key, value in summary.items() if key != "outputs"}, indent=2))
    return summary


def correlations(processed, output):
    """Descriptive associations only; no feature selection or significance claims."""
    columns = [column for column in processed if column.startswith("x__")]
    x = processed[columns]
    x.corr().to_csv(output / "pearson_feature_matrix.csv")
    observations = []
    for field in columns:
        paired = processed[[field, "y__vcd_cells_per_ml", "run_id"]].dropna()
        nonzero = paired[paired.y__vcd_cells_per_ml > 0]
        centered = paired[[field, "y__vcd_cells_per_ml"]] - paired.groupby("run_id")[[field, "y__vcd_cells_per_ml"]].transform("mean")
        observations.append({"feature": field, "pairs": len(paired),
                             "pearson_recorded_targets": paired[field].corr(paired.y__vcd_cells_per_ml),
                             "spearman_recorded_targets": paired[field].rank().corr(paired.y__vcd_cells_per_ml.rank()),
                             "pearson_nonzero_sensitivity": nonzero[field].corr(nonzero.y__vcd_cells_per_ml),
                             "within_run_centered_pearson": centered[field].corr(centered.y__vcd_cells_per_ml),
                             "scope": "pooled_descriptive_not_feature_selection_or_causal_inference"})
    pd.DataFrame(observations).to_csv(output / "feature_target_associations.csv", index=False)
