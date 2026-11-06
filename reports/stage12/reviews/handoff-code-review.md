# Correction-handoff engineering review

Date: 2026-11-05  
Role: Fresh-context Goldfish — engineering review (not scientific proof)  
Model: Codex / GPT-5 as exposed to this reviewer; exact model sub-version and reasoning setting were not exposed in the runtime.  
Scope: current `biosynvia/stage12.py`, `tests/test_stage12.py`, frozen `data/processed/v6`, `scripts/profile_offline_unique_values.py`, and `reports/offline-unique-values` against `docs/builder-handoff-dataset-interpretation-and-corrections.md`, especially sections 14–16. Source archive was read but not changed. No application, data, bundle, or model-fitting action was changed or run.

## Outcome

No confirmed reactor/experiment cross-join, raw/offline-target substitution, blank-to-zero conversion, Status conflation, or fit-gate bypass was found in the reviewed Stage 12 implementation or frozen v6 artifacts. This is an engineering conclusion only. It does not resolve the outstanding assay, availability, alignment, instrument, or biological questions in handoff section 16.

## Verified evidence

* The current producer and frozen v6 producer have the same SHA-256 (`a4b35c…3a53b`). `verify_bundle(data/processed/v6)` succeeded; SQLite integrity, all manifest output hashes, and CSV/SQLite logical comparisons passed.
* The raw archive inventory produced no warnings. `assert_source_schema` accepted the real archive and returned 60 inventory records: 12 workbooks plus 48 aligned CSVs. Runtime code requires exactly the expected 16 named sheets per workbook (`stage12.py:190–215`) and exact ordered headers for each aligned CSV type.
* v6 contains 378 `assay_decisions`, 6,804 source-cell records, and 15,120 lineage records. Every assay has exactly 40 lineage features; `(assay_id, feature)` is unique. A direct `many_to_one` check from lineage to decisions found all `experiment_id`, `reactor_id`, and `run_id` values equal.
* Snapshot construction first selects parent assays by `run_id` and then traverses a sheet whose reactor prefix forms that same run (`stage12.py:263–310`). The integration test independently checks all three keys after a build (`tests/test_stage12.py:160–164`). The split proposal also requires exactly both reactors per experiment and does not consume target values (`stage12.py:127–159`).
* Offline source cells have `predictor_allowed=False`; the canonical feature lineage is created only from non-offline sheets. Original assay values overwrite parent values from physical workbook cells and are checked exactly (`stage12.py:279–320`). In v6, 214 source blanks remain blank (glucose 135, lactate 51, ammonium 28), while numeric zero remains a distinct value; the profile script decodes `raw_value_json`, checks the blank flag, and never imputes or joins (`scripts/profile_offline_unique_values.py:19–73`).
* Numeric pH/DO/temperature rows are explicitly represented as `status_column_absent=True` rather than null measurements: 4,158 such v6 lineage rows are numeric and none are recorded as blank Status. Their strict-availability eligibility is false; no status is assumed `Ok` (`stage12.py:79–125`).
* The model gate remains closed: v6 manifest `model_fit_permitted=false`, all contracts reject a true fit/scientific/owner approval flag before build, and the module states it deliberately contains no fitting (`stage12.py:1`, `239–244`, `362–367`). The strict-availability five-feature count is zero, accurately preserving unresolved result availability.

## Confirmed defects

None in the audited scope.

## Missing or weak tests / engineering follow-ups

### P2 — workbook-sheet rejection is implemented but not negatively tested

`assert_source_schema` rejects missing or unexpected workbook sheet names (`stage12.py:196–205`), but the test named `test_exact_publisher_schema_rejects_wrong_sheet_and_csv_headers` creates only correct sheet sets and mutates only an aligned CSV header (`tests/test_stage12.py:84–103`). Add a negative assertion that removes or renames one expected workbook sheet, and another that adds an unexpected sheet. This directly closes correction 1’s executable-assertion test evidence.

### P2 — the end-to-end fixture bypasses the schema guard

The only full-build integration test patches `assert_source_schema` to return an empty inventory (`tests/test_stage12.py:152–154`). That is reasonable for a reduced synthetic workbook fixture with nonpublisher sheet names, but it means the build-path test does not exercise the actual archive-schema gate. Keep the compact fixture if useful, but add a focused non-mocked build or a dedicated schema-build test using exact sheet names/CSV members.

### P3 — bundle verification emits a pandas future warning

The direct v6 verification and test run pass, but `verify_bundle` emits pandas `FutureWarning` messages because CSV nulls arrive as `NaN` while SQLite returns `None` (`stage12.py:172–176`). Current verification is successful, yet a future pandas release may make the logical comparison fail. Normalize null representations before comparison or make the expected null-equivalence explicit, then add a regression assertion without warnings.

### P3 — original-workbook header contracts remain inferred, not fixed schemas

The runtime guard fixes all workbook sheet names, and it records the headers encountered, but it does not compare each raw workbook worksheet’s ordered headers to a declared per-family contract. This is not a defect for the checksum-pinned current source archive, which passed direct inspection. If the builder’s phrase “exact workbook schema” is intended to cover columns as well as the required 16 sheet names, add versioned per-family header contracts and targeted failure tests. Do not invent semantics for the headers while doing so.

## Scientific unknowns retained

No code evidence resolves assay SOP/SEM construction, the six VCD-zero interpretations, status meanings, measurement-result availability, clock synchronization, publisher alignment causality, EXP011 R02 coverage, duplicate-timestamp disposition, calibration, or reuse/retrieval questions. Engineering agreement does not validate those matters.

## Commands run

* `/Users/sindhu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests.test_stage12 -v` — 12 tests passed.
* Direct v6 manifest/SQLite/hash verification plus source-schema, run-key, blank/zero, Status, and fit-gate checks — passed, with only the noted pandas future warnings.
