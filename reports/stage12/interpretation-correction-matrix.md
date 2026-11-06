# Interpretation correction matrix — 2026-11-05

Every row maps a handoff correction to its prior source, evidence, and resolution. No model fitting occurred.

| ID | Prior wording / source | Classification | Concrete evidence | Corrected statement / resolution |
|---|---|---|---|---|
|14.1|Handoff §14.1 workbook ambiguity|Explanation|`data/processed/v6/source_schema_inventory.csv`; `tests/test_stage12.py::test_exact_publisher_schema_rejects_wrong_sheet_and_csv_headers`|12 workbooks each have exact 16 sheets.|
|14.2|Handoff §14.2 “versions”|Explanation; no defect|`tests/test_released_isolation.py`; `reports/stage12/released-isolation-verification.json`|R01/R02 are parallel runs.|
|14.3|Handoff §14.3 lineage term|Explanation|`reports/stage12/pre-modeling-decision-packet.md` source-authority matrix|Aligned CSVs are not BioSynvia lineage.|
|14.4|Handoff §14.4 amino-acid claim|Explanation|`data/processed/v6/source_schema_inventory.csv`; `tests/test_stage12.py::test_exact_publisher_schema_rejects_wrong_sheet_and_csv_headers`|No amino-acid profiles supplied.|
|14.5|Handoff §14.5 pre-inspection claim|Explanation|`data/processed/v6/source_schema_inventory.csv`; `tests/test_stage12.py::test_exact_publisher_schema_rejects_wrong_sheet_and_csv_headers`|Claims cite direct inspection.|
|14.6|Handoff §14.6 Status conflation|Explanation|`tests/test_stage12.py::test_unknown_and_blank_status_not_silently_ok`; v6 `feature_lineage.csv`|Absent/blank/warning/null/invalid stay distinct.|
|14.7|Handoff §14.7 five/eight framing|Explanation|v6 `sample_effects.csv`; `reports/stage12/pre-modeling-decision-packet.md`|Strict support is policy, not scientific invalidity.|
|14.8|Handoff §14.8 CSV-use implication|Explanation|`reports/unique-values/methodology.md`; v3 `aligned_offline.csv`; `reports/stage12/pre-modeling-decision-packet.md`|CSVs served EDA/preparation; Excel serves authority.|
|14.9|Handoff §14.9 combined ambiguity|Explanation; no defect|`tests/test_released_isolation.py`; `reports/stage12/released-isolation-verification.json`|Combined means stacking, not averaging.|
|14.10|Handoff §14.10 aligned zeros|Upstream representation/explanation; no BioSynvia corruption|`tests/test_preparation.py::test_missing_assay_and_recorded_zero_are_distinct`; v6 `assay_source_cells.csv`|Excel cells define observed/missing.|
|14.11|Handoff §14.11 agent agreement|Explanation|`reports/stage12/pre-modeling-decision-packet.md` unresolved questions; v6 `issue_register.json`|Engineering review is not science.|
|14.12|Handoff §14.12 mixing concern|No defect found|`tests/test_released_isolation.py`; `reports/stage12/released-isolation-verification.json`|No R01/R02 mixing found.|
|15.1|Handoff §15.1|Implemented|`data/processed/v6/source_schema_inventory.csv`; `tests/test_stage12.py::test_exact_publisher_schema_rejects_wrong_sheet_and_csv_headers`|12 ×16 structure.|
|15.2|Handoff §15.2|Implemented|`data/processed/v6/source_schema_inventory.csv`; `tests/test_stage12.py::test_exact_publisher_schema_rejects_wrong_sheet_and_csv_headers`|24×41 inline; 24×17 offline.|
|15.3|Handoff §15.3|Implemented|`reports/stage12/pre-modeling-decision-packet.md` source-authority matrix|Dual-source roles explicit.|
|15.4|Handoff §15.4|Implemented|`reports/stage12/pre-modeling-decision-packet.md` layer diagram|Layers separated.|
|15.5|Handoff §15.5|Implemented|`reports/stage12/pre-modeling-decision-packet.md` join-key declaration; `tests/test_released_isolation.py`; `reports/stage12/released-isolation-verification.json`|`run_id`; never time alone.|
|15.6|Handoff §15.6|Implemented|`tests/test_released_isolation.py`; `reports/stage12/released-isolation-verification.json`|No reactor cross-join.|
|15.7|Handoff §15.7|Implemented|`tests/test_released_isolation.py`; `reports/stage12/released-isolation-verification.json`|No experiment cross-join.|
|15.8|Handoff §15.8|Implemented|`tests/test_released_isolation.py::test_rejects_offline_predictors`; `tests/test_stage12.py::test_full_build_reproduction_zero_null_coordinates_and_failure_gate`|Inline/offline distinct; no snapshot payload.|
|15.9|Handoff §15.9|Implemented|`tests/test_preparation.py::test_missing_assay_and_recorded_zero_are_distinct`; v6 `assay_source_cells.csv`|Null and zero preserved.|
|15.10|Handoff §15.10|Implemented|`data/processed/v6/source_schema_inventory.csv`; `tests/test_stage12.py::test_exact_publisher_schema_rejects_wrong_sheet_and_csv_headers`|Sheet names runtime asserted.|
|15.11|Handoff §15.11|Implemented|`data/processed/v6/time_policy.csv`; `data/processed/v6/source_schema_inventory.csv`|Raw/aligned coverage separate.|
|15.12|Handoff §15.12|Implemented|`tests/test_stage12.py::test_unknown_and_blank_status_not_silently_ok`; v6 `feature_lineage.csv`|Missing Status is not null/invalid.|
|15.13|Handoff §15.13|Implemented|v6 `sample_effects.csv`; v6 `group_coverage.csv`; `reports/stage12/pre-modeling-decision-packet.md`|Five/eight retained.|
|15.14|Handoff §15.14|Implemented|`data/processed/v6/source_schema_inventory.csv`; `tests/test_stage12.py::test_exact_publisher_schema_rejects_wrong_sheet_and_csv_headers`|Amino acids absent.|
|15.15|Handoff §15.15|Implemented|v6 `stage12_manifest.json`; v6 `target_decision.json`; `reports/stage12/pre-modeling-decision-packet.md`|No model/digital twin.|
|15.16|Handoff §15.16|Implemented|`docs/builder-handoff-dataset-interpretation-and-corrections.md` §§14–15; this dated matrix|All prior locations link to evidence.|
|15.17|Handoff §15.17|Implemented|v6 `issue_register.json`; `reports/stage12/pre-modeling-decision-packet.md` unresolved-question list|Negative/unresolved findings retained.|

## Model-orchestration record

Confirmed delegated handoff-audit role: `gpt-5.6-terra`, medium reasoning. Fresh reviewer self-reported only generic GPT-5 metadata. No higher-tier delegation was requested; coordinator-host model accounting is not asserted. Scientific interpretation remains unapproved.

Final released-v6 regression evidence: `scripts/verify_released_isolation.py`, `tests/test_released_isolation.py` (5/5 passing), and `reports/stage12/released-isolation-verification.json`. Fresh-review dispositions, including three deferred engineering topics, are in `resolution_register.json`. These supplement the historical producer snapshot without changing the frozen v6 bundle.
