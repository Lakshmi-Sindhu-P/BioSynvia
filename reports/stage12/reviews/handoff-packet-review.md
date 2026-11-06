# Fresh-context handoff-packet review

**Date:** 2026-11-05  
**Role:** Goldfish — correction/specification compliance review  
**Actual model / reasoning:** `gpt-5.6-terra` / medium  
**Boundary:** Engineering evidence only. This review does not approve scientific interpretation, assay validity, targets, features, splits, or model fitting.

## Disposition

The packet materially satisfies the Section 14 correction ledger and Section 15 addendum requirements, with two actionable evidence gaps below. It correctly distinguishes prior explanation errors from implementation defects: no current R01/R02 or experiment mixing was found in the released data, but the stronger claim that this is proved by an executable released-bundle test is not yet supported.

Direct read-only v6 inspection joined all 15,120 lineage rows to unique assay keys and found zero `experiment_id`, `reactor_id`, and `run_id` mismatches across 24 runs. This is current artifact evidence, not a preserved regression test.

## Findings

### P1 — no released-v6 regression test for cross-run isolation

**Affected requirements:** Handoff §15.6–15.7; matrix rows 15.6–15.7; packet claim that a new test proves identity preservation.

**Evidence:** `tests/test_stage12.py::Stage12IntegrationTests::test_full_build_reproduction_zero_null_coordinates_and_failure_gate` makes the identifier comparisons only after constructing a synthetic EXP001–EXP006 fixture; it does not load `data/processed/v6/feature_lineage.csv` or `assay_decisions.csv`. The v6 verification JSON reports no cross-join, but that is an artifact/table assertion. My direct inspection found zero mismatches in v6, so this is not evidence of a present mixing defect.

**Needed fix:** Add a manifest-bound test/verifier for the released v6 bundle that requires unique `assay_id`, performs a many-to-one lineage-to-assay join, and asserts equality of experiment, reactor, and run IDs. Until then, say “verified against v6 artifact,” not “proved by a test.”

### P2 — CSV/SQLite logical-agreement check carries compatibility debt

**Affected requirement:** packet verification claim for v6 CSV/SQLite logical agreement.

**Evidence:** The pinned test command passed 38/38, but repeatedly emitted pandas `FutureWarning` at `biosynvia/stage12.py:176`: future `assert_frame_equal` will treat `nan` and `None` as mismatched null-like values. There is no current logical mismatch.

**Needed fix:** Normalize null representation before comparing CSV and SQLite tables and add a regression test. Until then, state that agreement passes in the pinned environment with this warning.

## Section 14 audit

| Correction | Status | Evidence checked |
| --- | --- | --- |
| 14.1 workbook structure | Satisfied | v6 inventory; exact-sheet/header rejection test. |
| 14.2 R01/R02 runs | Partial | v6 data clean; P1 limits test claim. |
| 14.3 aligned CSV is not lineage | Satisfied | Source-authority matrix. |
| 14.4 amino-acid claim | Satisfied | Exact offline schema; packet says absent. |
| 14.5 direct inspection | Satisfied | 41/17 headers and inventory. |
| 14.6 Status states | Satisfied | absent/blank/non-Ok/null/invalid tests. |
| 14.7 five/eight scenarios | Satisfied | Policy support, not scientific invalidity. |
| 14.8 dual sources | Satisfied | Excel and CSV authority roles explicit. |
| 14.9 `combined` meaning | Partial | Correct row-stack definition; P1 applies. |
| 14.10 aligned zeros | Satisfied | 214 blanks versus six numeric VCD zeros retained. |
| 14.11 agent agreement | Satisfied | Explicitly not scientific evidence. |
| 14.12 no current mixing | Partial | Current v6 check passes; P1 applies. |

## Section 15 audit

| Requirement range | Status | Evidence / limitation |
| --- | --- | --- |
| 15.1–15.5 | Satisfied | Exact 12×16 and 48-file structures, authority matrix, layer diagram, identity keys/no time-only join. |
| 15.6–15.7 | Partial | v6 data check passes; released-bundle executable proof missing (P1). |
| 15.8–15.10 | Satisfied | Separate tables before snapshot; blanks/zeros and expected sheets protected. |
| 15.11–15.13 | Satisfied | Separate raw/aligned coverage, Status states, five/eight scenarios. |
| 15.14–15.17 | Satisfied | No amino acids; no fitted model/twin; dated ledger; unresolved findings retained. |

## Boundary verification

- All gates remain false: target, feature, split, scientific, owner protocol, and model-fit approval.
- Scientific unknowns remain retained, including zero disposition, SOP/QC, availability and clocks, Status semantics, calibration, alignment, feed cutoff, collisions, retrieval, and rights.
- Historical v3/v4 material is labeled historical/superseded; v4’s numeric-precision defect is not concealed.
- The offline unique-values artifacts are internally consistent with frozen v5 descriptive scope: 16 measurement fields, 378 records each, 214 medium blanks (135/51/28), and six VCD numeric zeros; no medium numeric zeros. This is not scientific interpretation or a v6 regression test.
- EGM installation/reference is correctly presented as workflow availability only, not certification.

## Verification run

`/Users/sindhu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest discover -v` completed **38/38 passing**, with the P2 warnings above. The system Python lacks NumPy and cannot import the Stage 12 test module, so it is not equivalent test evidence.

No fitting, bundle rebuild, or implementation edits were performed.
