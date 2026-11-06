# Saved data preparation workflow

This implements the owner's sequence of backup, load, copy, inspect, manipulate,
extract, label and save. It prepares inspectable data; scientific target and
feature approval remain separate from successful software execution.

## Source and working copies

`data/raw/Dataset.zip` is preserved. A separate hash-verified archive copy is saved
under `data/backups`. The preparation script reads that backup, loads each table
as `original_df`, and uses `copy(deep=True)` for a working DataFrame. Regression
tests verify changes to the working copy do not alter the original DataFrame.

The archive backup is on the same computer: it protects the source during local
processing, but does not provide an independent off-device disaster-recovery copy.
Existing backups and completed output versions are never silently overwritten.

## Tables saved in the current output version

| Table and CSV | Contents |
| --- | --- |
| combined_inline | All aligned sensor rows with experiment/reactor, mode, run and source-file identifiers |
| aligned_offline | All original aligned assay rows, including upstream-filled zeros, retained for comparison |
| original_offline | Combined original assay values; raw missingness preserved; numeric zeros flagged distinctly |
| feature_lineage | One raw-derived feature snapshot per assay/field with source row, source time/status/value, age and disposition |
| processed_candidates | All original assay timestamps plus named inputs/target, metadata and review/completeness flags |
| inspection_subset | Provisional complete-case subset for eight core fields and nonzero recorded VCD; not approved training labels |

All six tables are saved as CSV files and in `biosynvia.sqlite`, with indexes on
run/time or assay/feature for repeated local queries. The SQLite database avoids
reopening Excel files for these saved tables. It does not contain every original
raw sensor row; the complete originals remain in the backup and the feature
lineage records point to them.

## Inspection and manipulation policy

The pipeline saves dataframe dimensions/memory sizes, per-field inferred and
working dtypes, null counts, invalid/nonfinite conversion counts, unique counts
and descriptive statistics. Numeric conversion occurs only on the working copy;
unparseable/nonfinite cells remain null and are counted. Source values remain
recoverable from the original archive and row references.

Original cell and medium assay tables are combined by measured elapsed time
within each reactor, with a one-to-one join check. There is no interpolation of
assay labels. Original glucose/lactate/ammonium blanks stay null even where aligned
files contain zero. The six recorded VCD zeros remain numeric zero in saved
original/processed tables with pending-review flags. They are omitted only from
the expressly provisional nonzero inspection subset, not deleted from the data.

Candidate inputs are extracted from original sensor streams at each actual assay
time using the latest observation at or before the cutoff. The default five-minute
maximum age is a sensitivity/inspection assumption requiring review. Status
Warning Active or missing Status excludes that candidate value where a Status
column exists. Streams without a Status column retain that absence explicitly.
Acquisition time is used under an explicit retrospective assumption; actual
availability-time semantics remain unapproved.

Only past history is used to flag fitted channels that have been entirely zero
so far. Zero batch feed values are not excluded by that rule. Duplicate source
timestamps retain competing row/value/status evidence and give an ambiguous
snapshot rather than silently choosing a value. Per-stream duplicate events are
recorded in `source_issues.json`.

## Extraction encoding and relationship analysis

All 40 raw-derived candidate fields are retained in the inspection data. An initial
eight-field subset spans dissolved CO2, transmission, reflection, conductivity,
permittivity, pH, dissolved O2 and temperature. This is a domain-motivated inspection
set, not a fitted feature-selection result. Other process/frequency fields remain
available for later controlled comparisons.

Inputs are named `x__...`; VCD is `y__vcd_cells_per_ml`. The feature dictionary maps
each input ID to its original column and explicitly pending unit review. Experiment
and reactor IDs are metadata/group keys, not model inputs. Mode has a documented
0=batch, 1=fed-batch code for inspection/context; it is not included in the default
eight-input inspection matrix. Continuous sensor values stay numeric, without
unnecessary categorical encoding or discretization.

Descriptive relationship outputs include a Pearson feature matrix and target
Pearson/Spearman comparisons, nonzero-target sensitivity and within-run-centered
Pearson. Pair counts are reported. These use the inspected dataset descriptively
and never automatically remove features. They are not independent-sample significance
tests, causal results or a valid way to tune against the future final holdout.

Read `reports/relationship-analysis-guide.md` for nonlinear, time-dependent and
model-based alternatives. Model-driven feature selection, imputation, scaling,
PCA/PLS and lag/window selection belong inside experiment-group development folds.

## Reproduction and queries

Use the optional analysis environment in `scripts/README.md`:

```sh
python scripts/prepare_data.py --output data/processed/new-version
```

An output is promoted from `.incomplete` only after all tables/manifests are saved
and the source hash is rechecked. Failed runs remain explicitly incomplete. The
manifest records backup/source hashes, producer code hash, sizes/output hashes,
encoding, age assumptions, counts and unapproved scientific/modeling status.

Example Python query after preparation, using the current versioned database:

```python
import sqlite3
import pandas as pd

with sqlite3.connect("file:data/processed/v3/biosynvia.sqlite?mode=ro", uri=True) as db:
    data = pd.read_sql_query(
        'SELECT * FROM original_offline WHERE experiment_id = ? ORDER BY "Time (h)"',
        db, params=["EXP011"],
    )
```

Before model fitting, approve target interpretation/quality, raw sensor unit/status
and availability rules, the group protocol and appropriate error criteria. No fitted
imputation, final test choice or model training is performed by this preparation.
