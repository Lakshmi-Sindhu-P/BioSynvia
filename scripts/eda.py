"""Reproduce the first descriptive EDA; source records are never modified."""

import argparse
from collections import Counter
import hashlib
import io
import json
import math
from pathlib import Path
import re
import sys
import zipfile

import numpy as np
import openpyxl
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from biosynvia.source import inventory_archive


def numeric(frame):
    values = frame.apply(pd.to_numeric, errors="coerce")
    return values.where(np.isfinite(values))


def longest_constant_hours(times, values):
    start = None
    previous = None
    longest = 0.0
    for time, value in zip(times, values):
        if pd.isna(time) or pd.isna(value):
            start = None
            previous = None
            continue
        if start is None or value != previous:
            start = time
        longest = max(longest, time - start)
        previous = value
    return longest


def analyze(archive_path, out):
    if out.exists():
        raise ValueError("Choose a new report directory; prior EDA outputs are preserved.")
    manifest = inventory_archive(archive_path)
    if not manifest["experiment_structure"]["valid"]:
        raise ValueError("Source structure is invalid.")
    out.mkdir(parents=True)
    tables, fields, inventory, offline, frames = [], [], [], [], {}
    raw_sheets, comparisons, raw_targets = [], [], []
    with zipfile.ZipFile(archive_path) as z:
        for entry in manifest["files"]:
            if not entry["path"].endswith(".csv"):
                continue
            raw = z.read(entry["path"])
            text = pd.read_csv(io.BytesIO(raw), dtype=str, keep_default_na=False)
            df = numeric(text)
            exp, mode, reactor, kind = (entry[key] for key in
                                       ["experiment_id", "process_mode", "reactor_id", "measurement_kind"])
            run = f"{exp}_{reactor}"
            frames[(run, kind)] = df
            t = df["Time (h)"]
            dt = t.diff().dropna()
            positive = dt[dt > 1e-10]
            summary = {"experiment": exp, "mode": mode, "reactor": reactor, "run": run,
                       "kind": kind, "rows": len(df), "variable_columns": len(df.columns) - 1,
                       "first_hour": t.min(), "last_hour": t.max(),
                       "missing_time": int(t.isna().sum()), "negative_time": int((t < 0).sum()),
                       "duplicate_times": int(t.duplicated().sum()), "backwards_steps": int((dt < 0).sum()),
                       "median_interval_hours": positive.median(), "max_interval_hours": positive.max(),
                       "gaps_over_twice_median": int((positive > positive.median() * 2 + 1e-8).sum()),
                       "sha256": hashlib.sha256(raw).hexdigest(), "source_file": entry["path"]}
            tables.append(summary)
            inventory.append({**entry, "sha256": summary["sha256"]})
            for col in df:
                values = df[col].dropna()
                blanks = text[col].str.strip().eq("")
                unit = re.search(r"\(([^()]*)\)$", col)
                fields.append({"run": run, "experiment": exp, "mode": mode, "kind": kind,
                               "source_file": entry["path"], "field": col,
                               "unit_text_in_header": unit.group(1) if unit else "not_explicit",
                               "unit_status": "header_text_only_not_semantically_verified",
                               "rows": len(df), "finite": len(values), "blank": int(blanks.sum()),
                               "invalid_or_nonfinite": int((df[col].isna() & ~blanks).sum()),
                               "missing_total": int(df[col].isna().sum()),
                               "zero": int((values == 0).sum()), "negative": int((values < 0).sum()),
                               "unique_finite": values.nunique(), "min": values.min(),
                               "p01": values.quantile(.01), "median": values.median(),
                               "p99": values.quantile(.99), "max": values.max(),
                               "longest_exact_constant_hours": longest_constant_hours(t, df[col])})
            if kind == "offline":
                offline.append(df.assign(run=run, experiment=exp, mode=mode, reactor=reactor))
            print(f"Profiled {run} {kind}: {len(df):,} rows", flush=True)

        # Original assay tables establish which aligned entries were actually measured.
        for entry in manifest["files"]:
            if not entry["path"].endswith(".xlsx"):
                continue
            raw = z.read(entry["path"])
            digest = hashlib.sha256(raw).hexdigest()
            inventory.append({**entry, "sha256": digest})
            workbook = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
            for sheet in workbook:
                head = list(sheet.iter_rows(min_row=1, max_row=3, values_only=True))
                raw_sheets.append({"experiment": entry["experiment_id"], "sheet": sheet.title,
                                   "reported_rows_including_header": sheet.max_row,
                                   "reported_columns": sheet.max_column,
                                   "headers": json.dumps(head[0], ensure_ascii=False),
                                   "status_first_two_rows": json.dumps([r[-1] for r in head[1:]]
                                                                       if head and head[0][-1] == "Status" else [])})
                if "_offline_" not in sheet.title:
                    continue
                rows = sheet.iter_rows(values_only=True)
                columns = next(rows)
                raw_df = numeric(pd.DataFrame(rows, columns=columns)).dropna(how="all")
                run = f"{entry['experiment_id']}_{sheet.title[:3]}"
                aligned = frames[(run, "offline")]
                for _, row in raw_df.iterrows():
                    time = row["Time (h)"]
                    matched = aligned.loc[np.isclose(aligned["Time (h)"], time, atol=1e-8, rtol=0)]
                    for col in raw_df.columns[1:]:
                        raw_value = row[col]
                        value = matched.iloc[0][col] if len(matched) == 1 and col in matched else np.nan
                        if len(matched) != 1:
                            status = "missing_or_ambiguous_aligned_time"
                        elif pd.isna(raw_value):
                            status = ("both_missing" if pd.isna(value) else
                                      "raw_missing_aligned_zero" if value == 0 else "raw_missing_aligned_nonzero")
                        elif pd.isna(value):
                            status = "raw_present_aligned_missing"
                        elif np.isclose(raw_value, value, rtol=1e-8, atol=1e-8):
                            status = "numeric_match"
                        else:
                            status = "numeric_mismatch"
                        comparisons.append({"experiment": entry["experiment_id"], "run": run,
                                            "sheet": sheet.title, "time_hours": time,
                                            "field": col, "status": status})
                # Count original nonmissing primary assay values by run (SEM is not another target).
                for col in raw_df.columns[1:]:
                    values = raw_df[col].dropna()
                    raw_targets.append({"experiment": entry["experiment_id"], "mode": entry["process_mode"],
                                        "run": run, "field": col, "raw_rows": len(raw_df),
                                        "raw_finite": len(values), "raw_missing": int(raw_df[col].isna().sum()),
                                        "raw_min": values.min(), "raw_max": values.max()})
            workbook.close()
            print(f"Inspected original assay sheets: {entry['experiment_id']}", flush=True)

    table = pd.DataFrame(tables)
    field = pd.DataFrame(fields)
    original = pd.DataFrame(raw_targets)
    compare = pd.DataFrame(comparisons)
    assays = pd.concat(offline, ignore_index=True)
    def save(frame, name):
        frame.to_csv(out / name, index=False)
    save(table, "table_profiles.csv")
    save(field, "field_dictionary.csv")
    save(pd.DataFrame(inventory), "dataset_inventory.csv")
    save(pd.DataFrame(raw_sheets), "workbook_sheet_inventory.csv")
    save(original, "raw_assay_coverage.csv")
    save(compare, "raw_aligned_assay_comparison.csv")
    save(compare.groupby(["field", "status"]).size().reset_index(name="cells"), "assay_comparison_summary.csv")
    target_summary = original.groupby("field").agg(raw_values=("raw_finite", "sum"),
                          raw_missing=("raw_missing", "sum"), runs=("run", "nunique"),
                          experiments=("experiment", "nunique"), minimum=("raw_min", "min"),
                          maximum=("raw_max", "max")).reset_index()
    save(target_summary, "target_coverage.csv")
    field_summary = field.groupby(["kind", "field"]).agg(rows=("rows", "sum"),
                      finite=("finite", "sum"), missing=("missing_total", "sum"),
                      invalid=("invalid_or_nonfinite", "sum"), zero=("zero", "sum"),
                      negative=("negative", "sum"), minimum=("min", "min"), maximum=("max", "max"),
                      constant_runs=("unique_finite", lambda s: int((s <= 1).sum()))).reset_index()
    save(field_summary, "field_summary.csv")
    vcd = "VCD Mean (cells/mL)"
    peaks = assays.groupby(["experiment", "mode", "run"])[vcd].agg(["count", "min", "max"]).reset_index()
    save(peaks, "vcd_by_run.csv")
    support = []
    for (run, kind), df in sorted(frames.items()):
        if kind != "offline":
            continue
        sensor_time = frames[(run, "inline")]["Time (h)"].to_numpy()
        for time in df["Time (h)"]:
            position = np.searchsorted(sensor_time, time, side="right") - 1
            age = time - sensor_time[position] if position >= 0 else math.inf
            support.append({"run": run, "time_hours": time, "sensor_age_hours": age,
                            "after_sensor_end": bool(time > sensor_time[-1] + 1e-8)})
    support = pd.DataFrame(support)
    save(support, "assay_sensor_availability.csv")
    metrics = {"archive_md5": manifest["md5"], "archive_sha256": manifest["sha256"],
               "aligned_rows_by_kind": table.groupby("kind")["rows"].sum().to_dict(),
               "variable_count_by_kind": {kind: int(part["variable_columns"].max())
                                          for kind, part in table.groupby("kind")},
               "time_quality_totals": table[["missing_time", "negative_time", "duplicate_times", "backwards_steps"]].sum().to_dict(),
               "assay_comparison_counts": compare["status"].value_counts().to_dict(),
               "aligned_missing_cells_excluding_time": int(field.loc[field.field != "Time (h)", "missing_total"].sum()),
               "aligned_invalid_cells_excluding_time": int(field.loc[field.field != "Time (h)", "invalid_or_nonfinite"].sum()),
               "original_assay_missing_cells": int(original.raw_missing.sum()),
               "workbook_sheets": len(raw_sheets),
               "assays_after_sensor_end": int(support.after_sensor_end.sum()),
               "assays_sensor_age_over_one_hour": int((support.sensor_age_hours > 1 + 1e-8).sum()),
               "maximum_sensor_age_hours": float(support.sensor_age_hours.max()),
               "python_version": sys.version.split()[0], "pandas_version": pd.__version__,
               "numpy_version": np.__version__, "openpyxl_version": openpyxl.__version__,
               "scope": "All aligned CSV cells; original workbook headers/dimensions and all offline assay cells. "
                        "Original inline sensor values/statuses not fully profiled.",
               "plot_units": "VCD displayed in millions of cells/mL; source values remain cells/mL."}
    (out / "summary.json").write_text(json.dumps(metrics, indent=2, allow_nan=False) + "\n")
    (out / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    make_plots(out, frames, table, original, peaks)
    write_report(out, metrics, table, target_summary, compare, field, support)
    print(json.dumps(metrics, indent=2), flush=True)


def md_table(frame):
    header = "| " + " | ".join(str(col) for col in frame.columns) + " |"
    divider = "| " + " | ".join("---" for _ in frame.columns) + " |"
    rows = ["| " + " | ".join(str(value).replace("|", "/") for value in row) + " |"
            for row in frame.itertuples(index=False, name=None)]
    return "\n".join([header, divider, *rows])


def write_report(out, metrics, table, targets, comparisons, field, support):
    primary = targets[~targets.field.str.contains(" SEM")].copy()
    primary["coverage_percent"] = (100 * primary.raw_values / (primary.raw_values + primary.raw_missing)).round(1)
    primary = primary.rename(columns={"field": "Assay", "raw_values": "Measured values",
                                      "raw_missing": "Missing values", "coverage_percent": "Coverage (%)"})
    primary = primary[["Assay", "Measured values", "Missing values", "Coverage (%)"]]
    zeros = field[(field.field == "C (300kHz)") & (field.unique_finite <= 1)]
    inline = table[table.kind == "inline"]
    offline = table[table.kind == "offline"]
    per_run = offline[["run", "mode", "rows", "last_hour"]].merge(
        inline[["run", "rows", "last_hour", "max_interval_hours"]], on="run", suffixes=("_assay", "_sensor"))
    per_run = per_run.round(3)
    freshness = pd.DataFrame([{"Maximum prior-sensor age": label,
                               "Assay timestamps with a sensor this recent": int((support.sensor_age_hours <= hours + 1e-8).sum())}
                              for label, hours in [("1 minute", 1/60), ("5 minutes", 5/60),
                                                   ("30 minutes", .5), ("1 hour", 1)]])
    report = f"""# BioSynvia dataset EDA report

November 5, 2026. Descriptive analysis of the real publisher archive. No model fitted.

## Executive findings

- The verified archive contains 12 experiments and 24 reactor runs: 9 batch and
  3 fed-batch experiments, each with two reactors. The scientific grouping unit
  is the experiment; the two reactors must remain together during evaluation.
- There are {metrics['aligned_rows_by_kind']['inline']:,} aligned sensor timestamps
  and {metrics['aligned_rows_by_kind']['offline']:,} aligned assay timestamps.
  Sensor rows are not independent biological experiments or additional assay labels.
- VCD has 378 nonmissing original measurements across all 24 reactors and 12
  experiments. It is a well-covered candidate, pending quality and feature review.
- The aligned CSVs appear complete, but {metrics['original_assay_missing_cells']}
  blank original assay cells appear as zeros. Treating these as measured zeros
  would change the scientific data. Preserve the original missingness mask.
- Sensor sampling is nominally one minute but includes long gaps and early
  endings. {metrics['assays_after_sensor_end']} assay timestamps occur after their
  reactor's final aligned sensor timestamp. A causal join needs freshness limits.

## 1. What the dataset contains

This is a laboratory CHO-K1 cell-culture dataset from Uhlendorff, Fulek, Eimler,
Pein-Hackelbusch and Frahm. CHO means Chinese hamster ovary. The research task is
to investigate whether frequently recorded reactor signals can estimate a
sparsely measured biological attribute. Batch and fed-batch are process-mode
labels supplied by the source; this EDA does not estimate a causal mode effect.

Source: https://zenodo.org/records/20829178
DOI: `10.5281/zenodo.20829178`.

The ZIP is 227,627,771 bytes. Its MD5 matches the published digest
`{metrics['archive_md5']}`. SHA-256:
`{metrics['archive_sha256']}`.
Reuse status remains unverified; this work does not redistribute the raw archive.

| Layer | Observed contents |
| --- | --- |
| Original files | 12 Excel workbooks, 16 sheets each, 192 sheets in total |
| Aligned sensor files | 24 CSVs; 40 numeric variables plus elapsed time |
| Aligned assay files | 24 CSVs; 16 numeric fields plus elapsed time |
| Sensor variables | 38 other sensor/process fields plus cumulative NaOH and feed weights |
| Assay fields | 10 primary assay fields plus 6 SEM fields |

SEM columns accompany replicate measurement summaries; they are not six extra
independent targets. No measurement method or unit conversion is inferred solely
from these labels. The field dictionary preserves the complete original headers.
For `C (300kHz)` and similar fields, the parenthesis denotes frequency, not a
verified unit for the measured C value. Header extraction must not become unit approval.

Sensor families include dissolved CO2/O2, turbidity transmission/reflection,
conductivity/permittivity and frequency-dependent C channels, process settings,
liquid volume and cumulative additions. Assays cover viable/total cell density,
viability, cell diameter/compactness/aggregation, glucose, lactate, ammonium and
osmolality.

## 2. Coverage and growth behavior

Each reactor has {int(offline.rows.min())}–{int(offline.rows.max())} assay timestamps.
Final assay times range from {offline.last_hour.min():.1f} to
{offline.last_hour.max():.1f} hours. Per-run median assay intervals range from
{offline.median_interval_hours.min():.1f} to {offline.median_interval_hours.max():.1f}
hours, with a maximum observed gap of {offline.max_interval_hours.max():.1f} hours.

VCD spans 0–16,166,666.7 cells/mL. Zero VCD entries are present in the original
workbooks and are not automatically recoded as missing. Assay validity and limits
of detection still require review. Growth trajectories differ substantially among
experiments. These are descriptive differences, not estimates of process-mode
effects or model performance.

![Coverage and peak growth](coverage_and_growth.png)

![Assay trajectories and illustrative sensor traces](trajectories.png)

Lines joining assay points are visual guides only. They do not create interpolated
ground-truth labels. The two illustrative sensor/assay panels use separate axes;
their visual similarity is not a fitted calibration or proof of predictability.

## 3. Original assay missingness versus aligned zeros

{metrics['assay_comparison_counts'].get('numeric_match', 0):,} original nonmissing
assay cells match the aligned CSV value at the same reactor, field and timestamp
within relative/absolute tolerance `1e-8`. Another 214 original blanks align to
zero: 135 glucose, 51 lactate and 28 ammonium cells. No other comparison status
was observed. All 378 original VCD means match aligned values at original assay times.

The aligned CSVs contain zero missing/nonfinite numeric cells, which alone is a
misleading quality signal. Missingness must be measured against the original sheets.
The cause of each blank is unknown; this EDA does not label blanks as depletion,
below detection limit, or equipment failure.

{md_table(primary)}

![Missing assay cells in original sheets](raw_assay_missingness.png)

## 4. Timestamp quality and sensor availability

All 48 aligned tables have finite, nonnegative, increasing timestamps with no
duplicates. This does not establish that upstream alignment was causal.
Median adjacent sensor time intervals are one minute in every reactor; the largest
observed gap is {inline.max_interval_hours.max():.2f} hours in EXP005_R02.

EXP011_R02 aligned sensor data end at 67.13 hours while its assay table continues
to 195 hours. Other early endings also occur. Across all reactors,
{metrics['assays_sensor_age_over_one_hour']} assay timestamps have a latest prior
aligned sensor row more than one hour old; the maximum age is
{metrics['maximum_sensor_age_hours']:.2f} hours.

The following is a sensitivity count using *any aligned sensor row*, not a
recommended scientific cutoff and not a count of approved model features:

{md_table(freshness)}

Use acquisition/availability timestamps and a reviewed maximum lag before fitting.
Do not carry the last sensor value indefinitely or use a future row to fill a gap.

## 5. Sensor quality signals to investigate

The C (300kHz) channel is entirely zero in {', '.join(zeros.run)}. The field summary
also shows three constant-zero runs for other C channels and Cole-fit outputs.
This suggests unavailable or inactive fitted channels in those runs, but the cause
is not established. Do not assume a numeric zero is a usable sensor observation.

Examples of ranges requiring source/instrument review include total aeration
down to -0.259 sL/h, agitation up to 3,000 rpm, and negative cumulative NaOH weights.
Negative reflection or corrected dielectric signals are not automatically invalid;
instrument meaning and preprocessing must be checked first.

Original sensor sheets include status fields absent from aligned CSVs. Header and
first-row inspection found a `Warning Active` status in EXP001_R01 permittivity.
This EDA does not count every original sensor status, classify the warning, or
reconstruct upstream interpolation. Full raw sensor/status auditing remains open.
Long identical-value spans are recorded in `field_dictionary.csv`; these may be
setpoints, resampling effects or faults and are not automatically removed.

## 6. Target and implementation decision

VCD is the strongest initial candidate on coverage grounds: 378 original means,
24 reactors, 12 experiment groups, with an explicit cells/mL header. This is a
provisional recommendation, not scientific approval or evidence of predictive
accuracy. TCD, viability, diameter, compactness, aggregation and osmolality also
have complete original coverage. Glucose, lactate and ammonium require their raw
missingness masks and have fewer observed targets.

Before modeling:

1. Preserve original assay values and missingness; never train against filled zeros.
2. Restore sensor status provenance and review upstream time alignment.
3. Define sensor-only feature eligibility, freshness limits and abstention behavior.
4. Review VCD meaning, assay quality and target decision; preserve real zeros.
5. Freeze whole-experiment partitions before model tuning. Only three fed-batch
   experiment groups are available; subgroup estimates will be uncertain.

No train/test split or performance comparison was produced by this EDA. All data
were inspected descriptively; document this exploratory access when freezing a
later evaluation protocol. Model results must not be used to revise the final holdout.

## 7. Scope, method and reproducibility

Analyzed all cells of all 48 aligned CSVs, original workbook sheet headers and
dimensions, and all original offline assay cells. Original inline status/value
streams were not exhaustively scanned. The archive and its members remain unchanged.
Numeric conversion flags aligned blank/unparseable/nonfinite values separately;
statistics use finite values. Original assay matching uses reactor, field and
elapsed time with `1e-8` hour matching tolerance. No imputation, smoothing,
normalization, unit conversion, fitted models, correlation screening, hypothesis
tests or synthetic labels were used. Charts scale VCD by one million for display.

Reproduce with `scripts/eda.py`; follow `scripts/README.md` for environment setup
and commands. Use a new output directory on rerun to preserve prior results.
Environment versions and source fingerprints are in `summary.json` and
`source_manifest.json`.

Supporting tables: `dataset_inventory.csv`, `workbook_sheet_inventory.csv`,
`table_profiles.csv`, `field_dictionary.csv`, `field_summary.csv`,
`raw_assay_coverage.csv`, `target_coverage.csv`, `assay_comparison_summary.csv`,
`raw_aligned_assay_comparison.csv`, `assay_sensor_availability.csv`, and
`vcd_by_run.csv`.

## Appendix: per-reactor sampling summary

`last_hour_assay` and `last_hour_sensor` are final timestamps, not proof of a
complete acquisition period. `max_interval_hours` is the largest adjacent sensor gap.

{md_table(per_run)}
"""
    (out / "report.md").write_text(report, encoding="utf-8")


def make_plots(out, frames, table, original, peaks):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "figure.facecolor": "#ffffff", "axes.titleweight": "bold"})
    colors = {"batch": "#166b85", "fed-batch": "#c46d27"}
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), layout="constrained")
    off = table[table.kind == "offline"]
    axes[0].bar(range(len(off)), off.rows, color=[colors[m] for m in off["mode"]])
    axes[0].set(xticks=range(len(off)), xticklabels=off.run, ylabel="Aligned assay timestamps", title="Sparse assay coverage by reactor")
    axes[0].tick_params(axis="x", rotation=90, labelsize=7)
    for mode, part in peaks.groupby("mode"):
        axes[1].scatter(part.experiment, part["max"] / 1e6, label=mode, color=colors[mode], s=45, alpha=.8)
    axes[1].tick_params(axis="x", rotation=90)
    axes[1].set(ylabel="Peak observed VCD (million cells/mL)", title="Growth range differs across experiments")
    axes[1].legend(frameon=False)
    fig.savefig(out / "coverage_and_growth.png", dpi=180)
    plt.close(fig)

    vcd = "VCD Mean (cells/mL)"
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), layout="constrained")
    for mode, ax in zip(("batch", "fed-batch"), axes[0]):
        for (run, kind), df in sorted(frames.items()):
            exp = int(run[3:6])
            if kind == "offline" and ((exp <= 9) == (mode == "batch")):
                ax.plot(df["Time (h)"], df[vcd] / 1e6, marker=".", linewidth=.9, alpha=.7)
        ax.set(title=f"{mode}: VCD assay trajectories", xlabel="Elapsed time (hours)", ylabel="VCD (million cells/mL)")
    for run, ax in zip(("EXP001_R01", "EXP010_R01"), axes[1]):
        inline, offline = frames[(run, "inline")], frames[(run, "offline")]
        ax.plot(inline["Time (h)"], inline["Permittivity (pF/cm)"], color="#166b85", linewidth=.8, label="Aligned permittivity")
        ax.set(xlabel="Elapsed time (hours)", ylabel="Permittivity (pF/cm)", title=f"{run}: dense sensors, sparse assays")
        right = ax.twinx()
        right.scatter(offline["Time (h)"], offline[vcd] / 1e6, color="#c46d27", s=20, label="VCD assays")
        right.set_ylabel("VCD (million cells/mL)", color="#a65719")
        ax.legend(loc="upper left", frameon=False, fontsize=8)
        right.legend(loc="upper right", frameon=False, fontsize=8)
    fig.suptitle("Descriptive observations; lines between assays are visual guides, not inferred labels", fontsize=12)
    fig.savefig(out / "trajectories.png", dpi=180)
    plt.close(fig)

    missing = original.groupby("field")[["raw_missing", "raw_rows"]].sum()
    missing = missing[missing.raw_missing > 0].sort_values("raw_missing")
    fig, ax = plt.subplots(figsize=(10, 4.5), layout="constrained")
    ax.barh(missing.index, missing.raw_missing, color="#bb5438")
    for i, (_, row) in enumerate(missing.iterrows()):
        ax.text(row.raw_missing + .3, i, f"{int(row.raw_missing)}/{int(row.raw_rows)}", va="center", fontsize=9)
    ax.set(xlabel="Missing cells in original offline worksheets", title="Original assay blanks must not become ground-truth zeros")
    ax.set_xlim(0, max(missing.raw_missing.max() * 1.3, 1))
    fig.savefig(out / "raw_assay_missingness.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=Path("data/raw/Dataset.zip"))
    parser.add_argument("--output", type=Path, default=Path("reports/eda"))
    args = parser.parse_args()
    analyze(args.archive, args.output)
