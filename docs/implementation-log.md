# Implementation log

## 2026-11-05 — Handoff interpretation correction audit

Read the owner-reviewed builder handoff and audited all 12 interpretation
corrections plus 17 required packet changes. Added exact runtime assertions for
the 12-workbook/16-named-sheet structure and the 48 aligned CSV schemas (24 inline
× 41 columns; 24 offline × 17 columns). New output `data/processed/v6` preserves
v5 and adds a 60-row source schema inventory. Tests prove source-to-assay lineage
retains experiment, reactor and run identity; the audit found no confirmed R01/R02
mixing defect.

Published a dated correction matrix and revised the pre-modeling packet with the
dual-source authority policy, layer/key rules, status-state distinction, explicit
five/eight policy scenarios, source preservation evidence, unchanged unresolved
questions and model-fitting pause. Original workbook offline cells remain authority
for null versus numeric-zero meaning; no model or scientific interpretation was
added. This bounded task used the requested ordinary 5.6-class coding/review role
with ordinary reasoning; no 6/6.1 escalation was warranted.

## 2026-11-05 — First implementation increment

### Step 1: Recover the available project context

The local workspace was empty. Read the existing BioSynvia planning chats
“Branch · Rewards Network Application Advice” and “Research Orchestration Plugins
Prompt”. These describe an offline CHO modeling workbench and place the dataset
audit before target selection, model training, and dashboard development.

The full PRD v1.1 and SRD v0.1 are referenced as generated attachments in those
chats but are not available as local project files. Their complete requirement IDs
and acceptance tests have not been recovered. Chat summaries are context, not a
substitute for the specifications. This increment therefore makes no claim of
PRD/SRD compliance.

### Step 2: Build a runnable local audit

Added a dependency-free Python package and command. A provisional CSV contract
makes experiment groups, cultivations, time, variables, values, and units explicit.
The validator detects structural problems and conflicting group assignments.
Missing values are counted, not filled. Raw source files are read only.

### Step 3: Make results traceable

Reports include file fingerprints calculated from exactly the bytes parsed and
deterministic summaries. Failed validation suppresses target candidates. All
candidates otherwise remain subject to scientific review. Reports protect existing
files and do not claim model performance.

### Step 4: Verify with synthetic data

Added invented examples with two paired experiment groups and an intentionally
missing laboratory value. Added regression tests for validation, provenance,
repeatability, future-only sensor availability, and file protection. Run the test
command in the README for current results.

Verification on this increment: all 13 tests passed on Python 3.14.5. The CLI
example produced `outputs/synthetic-audit.json` with 8 sensor rows, 8 measurement
rows, 4 cultivations, and 2 experiment groups. It reported zero structural errors
and one expected missing-value warning. Seven nonmissing synthetic target
observations had at least one sensor observation at or before their measurement
time. These counts validate the demo workflow only.

### Outstanding inputs and limits

- Need authoritative PRD and SRD files and the source dataset/data dictionary.
- The actual source schema, reuse terms, units, time origins, and pairing need review.
- No source-specific adapter, feature alignment, split manifest, models, uncertainty,
  dashboard, or DSH integration is implemented yet.
- No DSH plugins or external services have been installed. Earlier research chat
  recommendations have not been treated as verified plugin compatibility evidence.
- Range summaries do not check biological plausibility; extremely large finite
  values can pass this structural contract. Empty values are the only accepted
  missing-value convention.

## 2026-11-05 — Recover PRD and acquire source archive

The owner clarified that the specifications were expected in project files and
the dataset had not been saved. A focused local filename search found PRD v1.1
in Downloads; it was copied unchanged into `docs/specifications` with a text
extraction. No local SRD was found. The earlier missing-PRD status above describes
the state before this recovery.

Read the PRD's data contract, first sprint, functional requirements and M1 gate.
Added `requirements-status.md` to distinguish partial implementations from unmet
acceptance criteria. The staging CSV schema is not the full PRD canonical model.

Verified the dataset publisher page and downloaded its source archive into ignored
`data/raw/Dataset.zip`. Publisher: https://zenodo.org/records/20829178 . Download
completed during this increment. Size: 227,627,771 bytes. Verified published MD5:
`71b2a35b7df2ed11644ec9f177453772`. The repeatable `inventory` command creates
`outputs/source_manifest.json`, recording SHA-256 and member metadata. It found
12 XLSX and 48 CSV files with no count/path warnings; it did not extract files or
parse measurements. License/reuse status remains unresolved.

All 16 tests passed, including checksum mismatch rejection and no-extraction
inventory checks. Next: recover SRD, reconcile experiment/reactor/type combinations,
and inspect columns, units and original/aligned timestamps. No target decision,
real-data audit acceptance, or model validation has been completed.

## 2026-11-05 — SRD recovery and reproducible EDA

Copied the owner-provided SRD v0.1 into `docs/specifications` unchanged and read
its data intake, canonical schema and acceptance requirements. Added source
combination reconciliation and two tests; all 18 software tests pass.

At the owner's request, created `reports/implementation-report.md` as the ongoing
work report and implemented `scripts/eda.py` inside the project. The script was
executed successfully twice: initial tables/charts under `reports/eda`, then the
current report, charts, availability diagnostics and tables under `reports/eda-v2`.
It reads the ZIP directly and does not change source files. Analysis dependencies
are optional and documented separately from the dependency-free audit package.

Key results: 274,781 sensor rows, 378 assay timestamps, 214 original assay blanks
represented as aligned zeros, complete original VCD coverage across 12 experiments,
14 assay times after sensor recording ends, and gaps/constant-zero sensor channels
requiring further investigation. See the EDA report for exact scope, caveats and
tables. VCD is only a provisional candidate. No model or accepted feature pipeline
has been built. The remaining SRD/PRD gaps are tracked in `requirements-status.md`.

## 2026-11-05 — Expanded product and system specifications

Applied the owner's capability gap assessment to PRD v1.2 and SRD v0.2, preserving
the complete earlier PDFs as baselines within each revised edition. Added a
separate research component release, stable DT/SR-DT IDs, T-019 through T-034,
explicit schema/interface and failure behavior, scientific eligibility rules and
cross-document traceability. Primary NIST/FDA references provide architectural,
PAT and comparability context; they are not claims of compliance.

Updated current-spec links and requirements/implementation reports. Checked the
10 product IDs, 21 unique new system IDs, 16 new test IDs and unchanged baseline
page content. Rendered/reviewed new pages; original files remain preserved. No
new modeling capability was implemented by this documentation revision.

## 2026-11-05 — Quality investigation and methodology clarification

Added `scripts/investigate_data_quality.py` and `scripts/profile_unique_values.py`.
Verified original sensor endpoints, six numeric VCD source zeros and lack of assay
Status columns in the two relevant workbooks. Scanned all Status rows across all
12 workbooks and profiled distinct numeric values in all aligned fields. Recorded
results and open questions in quality-review and unique-values reports. Preserved
original values and did not approve labels, select groups or fit models.

The owner requested karpathy-guidelines; its instructions were read and applied.
Current build scope follows PRD v1.2/SRD v0.2. Raw per-stream availability must be
distinguished from the all-field aligned export in the next canonical-data work.

## 2026-11-05 — Backup and persisted preparation pipeline

Followed the owner's load/copy/inspect/manipulate/extract/encode/save sequence,
with scientific-quality and grouped-validation safeguards. Current completed
inspection data are saved under `data/processed/v3` as CSVs and SQLite tables,
with backup and producer/source/output hashes. Added 8 meaningful preparation
tests; all 26 project tests pass in the analysis environment.

The initial raw-duplicate detection stopped the first run. Preserved conflicts
and introduced ambiguous-snapshot flags rather than choosing values. A later test
also verifies derived-channel quality uses only past history. Final v3 includes
these rules; prior v2 is superseded. No source or scientific label was altered.

Added relationship-analysis guidance and plots covering the owner's questions
about nonlinear/temporal associations and alternatives to a correlation matrix.
Feature selection, imputation/scaling and model comparison remain development-fold
activities after scientific target/input and experiment-group protocol review.

## 2026-11-05 — Authorized Stages 1/2 protocol execution

Saved `docs/stage12-executable-spec.md` before implementation and completed five
separate fresh-context pre-reviews (scientific, quality, leakage, provenance and
requirements). Native agent roles substituted for unavailable EGM discovery.
The review/model/usage record and all 28 pre-review dispositions are saved under
`reports/stage12`. Luna supplied bounded header extraction; reviewers did not fit
models or supply scientific assay approvals.

Implemented explicit target/inference/quality/split/benchmark/issue contracts,
raw source-cell lineage, independent quality flags, all-stream cadence/collisions,
strict/assumed acquisition scenarios, sample effects and exact paired-group split
proposals in `biosynvia/stage12.py` and `scripts/build_stage12.py`. Earlier v3 and
source data are retained. Initial JSON-scalar serialization and CSV-text logical
comparison failures remain in named incomplete directories with failure logs.
The corrected checker preserves JSON text through CSV/SQLite comparison. A
synthetic integration fixture verifies byte-stable CSV/config/producer/split
payloads over two runs, zero/null/cell preservation and validation failure without
promotion. The full-data build and fresh postreviews supply final packet evidence.
No model fitting occurs in this increment.

### Final source-exact correction and verification

V4 completed its engineering checks but post-review found CSV-parser rounding in
701 numeric source/decision pairs, including one VCD mean (one floating-point
step, approximately 1.46e-11 cells/mL). The correction reconstructs original assay
columns directly from physical source-cell values and verifies exact null-aware
agreement before promotion. V5 is the current complete protocol bundle; v4 and
failed incomplete versions remain retained. V5 also carries per-stream descriptive
raw/aligned endpoint differences without asserting the unknown export algorithm.

The full 37-test suite passes. Final verification checks all 6,804 source-cell
records, exact original numeric/null agreement, all 27 consumed-input and 25
payload hashes, 11 CSV/SQLite tables, the unchanged archive/backup and proposed
EXP004/EXP010 final groups. The frozen v5 manifest is identified in
`reports/stage12/verification.json`. Fresh postreviews verify that final bundle;
no model fitting or scientific approval is inferred.

A provider usage cap interrupted two postreviewers before their reports were
saved. The owner explicitly reset the limit and authorized resumption; both
resumed their existing fresh-context reviews and retained their original requested
models. Prior telemetry and the separate reset baseline are recorded in
`reports/stage12/coordination.json`. The later owner instruction to use 5.6 for
implementation/code writing arrived after v5 source changes were complete. No
additional application code was written by the coordinator after that instruction.
