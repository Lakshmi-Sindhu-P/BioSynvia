# Reproduce the dataset EDA

`eda.py` is the project-owned EDA script. It reads the original ZIP directly,
verifies its publisher checksum, profiles all 48 aligned CSVs, inventories all
192 workbook sheets, compares original offline assays with aligned values, and
creates descriptive plots, summary CSVs, JSON provenance and a Markdown report.
It never changes the source archive and never fits a predictive model.

## Portable setup

Use Python 3.12 and the optional EDA dependencies in a local environment:

```sh
python3.12 -m venv .venv-eda
.venv-eda/bin/python -m pip install -r scripts/requirements-eda.txt
MPLCONFIGDIR=.mplconfig .venv-eda/bin/python scripts/eda.py \
  --archive data/raw/Dataset.zip \
  --output reports/eda-new-run
```

Choose a new output directory each time. An existing directory is protected from
overwrite. Failed execution may leave diagnostic partial outputs; a run is only
complete if it exits successfully and produces `report.md` plus all three figures.

## Command used in this session

The bundled Python environment supplied pandas, NumPy, openpyxl and other base
dependencies. Missing plotting libraries were installed locally in ignored
`.analysis-deps/`, without changing the bundled environment:

```sh
PYTHONPATH=.analysis-deps MPLCONFIGDIR=.mplconfig XDG_CACHE_HOME=.mplconfig \
  /Users/sindhu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/eda.py --output reports/eda-v2
```

The portable setup above uses the same core analysis versions. It is a pinned
dependency list, not a claim of clean-environment reproduction already tested.

## Interpretation limits

The script reports descriptive counts and ranges. It does not assign causes to
missingness, approve units, establish biological plausibility, reconstruct raw
inline alignment, select a holdout, or validate a prediction model. Its heuristic
gap and sensor-freshness counts are diagnostics, not accepted modeling thresholds.

## Focused quality and distinct-value scripts

Use the same optional analysis environment to run:

```sh
python scripts/investigate_data_quality.py --output reports/quality-review-new
python scripts/profile_unique_values.py --output reports/unique-values-new
python scripts/profile_offline_unique_values.py --output reports/offline-unique-values-new
```

The first scans EXP002/EXP011 source streams and recorded VCD zeros. The second
profiles all aligned numeric fields and scans every raw Status column in all 12
workbooks. Both require a new output directory and preserve source files. Read
`reports/quality-review/report.md` for unresolved scientific questions and
`reports/unique-values/methodology.md` for file-loading/combination details.
`profile_offline_unique_values.py` reads frozen source-exact offline cell evidence
after manifest verification and reports distinct values separately by field and run;
it does not infer medium formulation or biological mechanisms.

## Persist combined and prepared copies

```sh
python scripts/prepare_data.py --output data/processed/new-version
```

This creates/reuses a separate verified archive backup, works on deep DataFrame
copies, and saves combined CSV tables plus an indexed SQLite database, original
assay missingness, raw-derived snapshots/lineage, type/size/null/unique audits and
descriptive associations. It does not fit models or approve labels. The completed
session output is `data/processed/v3`; prior diagnostic runs are superseded.
See `docs/data-preparation-workflow.md` for table definitions, assumptions and a
read-only query example.

Optional relationship plots use the same local plotting environment as the EDA:

```sh
PYTHONPATH=.analysis-deps MPLCONFIGDIR=.mplconfig XDG_CACHE_HOME=.mplconfig \
  python scripts/plot_relationships.py --output reports/preparation/new-relationships.png
```

Released-bundle identity verification: `verify_released_isolation.py` checks the frozen v6 manifest and rejects cross-experiment/reactor/source identity and offline-predictor contamination; evidence is saved in `reports/stage12/released-isolation-verification.json`.

`summarize_scientific_decision_counts.py` verifies frozen v6 fingerprints and reports pre-fit target, status, freshness, contamination-mask and forecast-ceiling counts in `reports/scientific-closure`. It never fits models or edits source data.
