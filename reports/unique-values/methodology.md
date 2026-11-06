# How BioSynvia loads and profiles the dataset

November 5, 2026. This document describes the implemented scripts, not a planned
model-training pipeline. The current PRD v1.2/SRD v0.2 define the build direction.

> Historical-status notice (updated 2026-11-05): the “not combined yet” section
> below describes the earlier EDA stage only. Current versioned evidence includes
> a SQLite audit database and controlled source-to-assay lineage under
> `data/processed/v6`, while no approved canonical modeling dataset, accepted
> feature snapshot, train/test evaluation or model fit exists. See the current
> [pre-modeling packet](../stage12/pre-modeling-decision-packet.md).

## The dataset has several levels

- An experiment is the independent experimental group: EXP001 through EXP012.
- Each experiment has two reactor runs, R01 and R02. R01 is reused across experiments,
  so a run is identified by experiment plus reactor, not reactor alone.
- Each reactor has an aligned inline CSV and an aligned offline CSV: 48 CSVs total.
- Each experiment also has an original Excel workbook containing 16 separately
  timed source streams or assay tables: 12 workbooks and 192 sheets total.

Original sensor streams have their own timestamps and record counts. Rows at the
same position in different sheets are not automatically simultaneous. Correct
feature construction needs an explicit time-based, source-aware joining policy.

## How the first EDA loads the files

The archive remains at `data/raw/Dataset.zip`. It is read directly; there is no
requirement to extract files or open a desktop Excel application. The code verifies
the publisher checksum before parsing source observations.

1. Read one aligned CSV member from the ZIP and parse it into a pandas table.
2. Extract experiment, mode, reactor and measurement kind from its verified filename.
3. Compute per-file timestamp and field profiles. Keep the parsed table in memory
   under `(experiment_reactor, inline_or_offline)` for comparisons and figures.
4. Repeat for all 48 CSVs. This is a batch of individual file reads, not SQL queries.
5. Concatenate the 24 small offline tables in memory, adding experiment, reactor,
   run and process-mode columns. The resulting 378-row table supports descriptive
   coverage summaries and plots; it is not a pooled training dataset.
6. Load one original workbook at a time with openpyxl in read-only mode. Inventory
   all sheet headers/dimensions and read the offline tables to check original values
   and missingness. Compare by run, source field and assay time rather than row position.
7. Write report tables, figures and fingerprints. Do not merge 274,781 sensor rows
   with 378 assay rows into a model-ready table or interpolate new assay labels.

Reading with openpyxl does not edit the workbook. `data_only=True` in the EDA reads
stored formula results if present; the targeted zero investigation uses
`data_only=False` and confirms the relevant source cells are numeric zeros.

## What the additional scripts do

`scripts/investigate_data_quality.py` scans every row of all sheets in EXP002 and
EXP011, profiles per-stream endpoints/status transitions, identifies six numeric
zero VCD source cells and evaluates latest-prior raw/CSV coverage at R02 assay times.
Its evidence and unresolved issues are in `reports/quality-review`.

`scripts/profile_unique_values.py` reads all 48 aligned CSVs and collects numeric
values by measurement kind and original field name. It combines values for each
field across reactor files solely to count/enumerate distinct numeric values.
This does not join experiments or create training examples. It also scans every
Status-column row in all 12 original workbooks: 72 source streams in total.

## What unique means here

Categories: the exact identifiers/labels present in source filenames or Status
cells. `<blank>` in the report is a missing-status marker, not literal instrument
text. There are two nonblank Status labels: Ok and Warning Active.

Numeric fields: exact equality after conversion to float64. Thus text forms `0`
and `0.0` count as one numeric value. There is no tolerance rounding/binning;
nearly equal floats can count separately. Units/field names remain separate, as
do inline and offline fields. Missing/nonfinite values are excluded and counted.

The distinct-count profile covers aligned CSV values, so glucose/lactate/ammonium
lists contain zeros introduced in upstream aligned files. Those distinct values
must not be interpreted as all genuinely measured assay values. Original assay
missingness is recorded separately in the main EDA and quality report.

`numeric_unique_counts.csv` contains all 58 field profiles, including a time field
for each modality. It reports cell count, distinct count, min/max and the five
most frequent numeric values. For fields with at most 12 distinct values it also
lists every value directly. `numeric_distinct_values.json.gz` contains every
finite distinct numeric value for each field, sorted numerically. It is a local
derived-data artifact, not a proposed public redistribution.

## Verified categorical values

| Attribute | Values |
| --- | --- |
| Experiments | EXP001, EXP002, EXP003, EXP004, EXP005, EXP006, EXP007, EXP008, EXP009, EXP010, EXP011, EXP012 |
| Reactors within each experiment | R01, R02 |
| Process modes | batch, fed-batch |
| Aligned measurement kinds | inline, offline |
| Nonblank raw sensor Status labels | Ok, Warning Active |

Across 72 raw status streams, there are 1,726,803 Ok records, 4,037 Warning Active
records and 6,325 missing Status values. These are sensor-record counts and are
not independent samples, durations, assay approvals or fault counts. Different
streams sample at different rates. Missing Status does not mean Ok. Instrument
semantics and quality rules remain open questions.

## Example numeric distinct counts

| Field | Distinct values across aligned tables | Observed range |
| --- | --- | --- |
| Inline pH | 191 | 6.806 to 7.099 |
| Inline temperature | 627 | 35.810 to 37.286 degrees C |
| Inline dissolved CO2 | 271,941 | 0 to approximately 41.431 percent saturation |
| Offline VCD mean | 363 | 0 to approximately 16.167 million cells/mL |
| Offline viability mean | 371 | 0 to approximately 97.263 percent |

378 recorded VCD means having 363 distinct numeric values is expected when some
measurements repeat. It does not reduce or increase the independent experiment
count. The 378 records include the six numeric zeros pending assay review.

## What had not been combined at this EDA stage

At that time there was no approved canonical modeling dataset, SQL database, feature
snapshot table or train/test split. There was no direct interpolation of sparse assay targets
onto the sensor grid. A future pipeline must preserve source identity, original
missingness, per-stream status, units, acquisition/availability time, maximum
feature age and experiment grouping before creating accepted feature/target rows.

For EXP011 R02, the original non-feed sensor streams extend well beyond the aligned
CSV cutoff. The future importer must distinguish raw per-stream availability from
the aligned all-column export, rather than discard or forward-fill whole runs.
