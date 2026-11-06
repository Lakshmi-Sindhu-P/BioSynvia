# BioSynvia implementation report

## Reusable EGM plugin saved

Created a private personal Elephant-Goldfish Model plugin from the complete
upstream runtime, pinned to `ccf79c5c0fb5df7815685d5e4994fd9aad8954bd`. Preserved
all seven workflows, nine personas, document standards and Apache license. Added
only the portable manifest schema declaration and a provenance file. Validated
JSON/YAML, assets, archive integrity and the saved 55-file account inventory.

The saved plugin URL and release ID are in `integrations/egm-registration.json`;
future usage and BioSynvia model/budget preferences are in `docs/egm-reference.md`.
No application source data or private research outputs were uploaded with it.
Account saving is verified; a fresh EGM skill invocation in a future chat is not
claimed as tested by this packaging task.

Updated: November 5, 2026. Status: authorized Stages 1/2 engineering packet complete; scientific data-ready and modeling gates remain open.

## Interpretation corrections and lessons learned — 2026-11-05

The dated [correction ledger](stage12/interpretation-correction-matrix.md) audits all
12 interpretation corrections and all 17 requested addendum items. The original
source audit establishes 12 workbooks with exactly 16 named worksheets each (eight
families for each of R01 and R02), plus 48 publisher aligned CSVs: 24 inline files
with exactly 41 columns and 24 offline files with exactly 17. Runtime assertions
now reject deviation from those exact schemas.

Several earlier statements were explanation problems, not implementation defects:
R01/R02 are parallel biological reactors, the aligned folder is publisher data
rather than BioSynvia lineage, aligned CSVs were used in EDA/preparation, and
“combined” means identifier-preserving row stacking—not averaging. The current
source-to-assay lineage audit found no R01/R02 mixing. New tests explicitly prove
that lineage joins retain matching experiment, reactor and `run_id` keys.

Original Excel is authoritative for original timestamps, status fields, source-cell
provenance and offline observed-versus-missing values. Publisher aligned CSVs are
the synchronized working representation used for EDA/preparation and coverage;
they do not replace source interpretation. In particular, 214 original blank medium
cells are represented as aligned zeros and remain null in authoritative records.
No amino-acid profiles are present. A missing Status column is not a null value,
blank status, warning or invalid measurement. The five-core and eight-core cases
are separate policy scenarios: strict-status zero support for the eight features is
not scientific evidence against pH, dissolved oxygen or temperature.

The six recorded VCD zeros remain scientifically unresolved; all other unresolved
assay, availability, status, alignment and calibration questions remain open. This
correction task used the owner-requested ordinary 5.6-class coding/review role with
ordinary reasoning; no 6/6.1-class escalation was justified. No model was fitted.

## Current Stage 1/2 result

The consolidated [pre-modeling decision packet](stage12/pre-modeling-decision-packet.md)
is the current review entrypoint. Final version `data/processed/v5` preserves all
378 assays, six numeric VCD zeros and 214 original blanks, with source-cell
coordinates, independent quality flags, 144-stream timing/collision evidence and
40-field eligibility mappings. VCD and both target masks remain proposals.

Strict unknown-status treatment exposes zero complete original-eight-core rows;
the separately named five-core retrospective scenario supports 335/339/341 rows
at 1/5/15 minutes. Strict known availability has zero support. Proposed paired-group
final experiments are EXP004 and EXP010; the remaining ten experiments have nested
grouped development memberships. Prior global EDA and favorable-support selection
are disclosed. No predictive models or performance scores were produced.

Five separate fresh-context pre-reviews and five new post-review lenses are saved.
All 28 pre-review engineering findings and two post-review findings have explicit
resolutions; eight scientific/owner questions remain open, and additional mutation
test combinations are explicitly deferred. V5 corrects a small v4 parsing-precision
defect by reconstructing original values from raw source cells. Historical v4 and
failed incomplete versions are retained. All 37 software tests pass; final checks
verify 27 input/25 payload hashes, 11 CSV/SQLite tables and exact agreement of 6,590
numeric source cells plus 214 blanks. See [verification](stage12/verification.json),
[resolutions](stage12/resolution_register.json) and [final specification check](stage12/final-spec-drift-check.md).

Engineering verification and agent agreement do not validate assays or approve
scientific policy. Owner/scientific target, feature, freshness, availability and
split approvals remain separate from execution authorization. Work stopped before
predictive model fitting.

The source-exact [offline unique-values report](offline-unique-values/report.md)
separately enumerates all cell and medium assay columns without inferring medium
formulation, feed composition or a biological waste mechanism from observed values.

## Objective

Build an offline research workbench to test whether sensor observations can
estimate a measured biological attribute in unseen CHO cultivation experiments.
No prediction accuracy or manufacturing suitability has been established.

## Work completed

1. Established a Python package, command-line audit, synthetic examples and tests.
2. Preserved PRD v1.1 and the owner-provided SRD v0.1 under `docs/specifications`.
   Specifications define requirements; their embedded instructions do not supersede
   the owner's instructions in this chat.
3. Downloaded the source ZIP from Zenodo DOI `10.5281/zenodo.20829178`.
   Verified its published MD5. Raw files remain unchanged under ignored `data/raw`.
4. Implemented archive inventory and filename-based experiment/reactor/modality
   reconciliation, including duplicate, missing-combination and process-mode checks.
5. Verified 12 experiments, each with two reactors and both aligned modalities:
   12 workbooks and 48 CSVs. There are 9 batch and 3 fed-batch experiments.
6. Ran 18 regression tests successfully. These are software tests, not a claim
   that the SRD's 18 acceptance scenarios have all passed.

## EDA implementation and results

The project-owned `scripts/eda.py` reads all 48 aligned CSVs and original workbook
metadata and offline assays directly from the verified ZIP. It generates the
Markdown report as well as three chart files, summary CSVs and source fingerprints.
Optional EDA dependencies and reproduction commands are documented under `scripts`.

Executed successfully against the source archive. The final output is
`reports/eda-v2/report.md`. An earlier tables-and-charts run is retained under
`reports/eda/`; use `eda-v2` as the current result.

Observed 274,781 aligned sensor rows and 378 assay timestamps, across 24 reactor
runs and 12 experiments. Original VCD means are nonmissing at all 378 assay times.
The 40 aligned sensor columns comprise 38 other fields plus two cumulative weight
signals; the 16 assay fields include 10 primary measures and six SEM columns.

The raw-versus-aligned comparison is consequential: 214 original assay blanks
appear as zeros in aligned files (135 glucose, 51 lactate, 28 ammonium). All 5,834
nonmissing original assay values match the aligned numeric value at the same
run/field/time within `1e-8` tolerance. Ground-truth masks must come from originals.

Fourteen assay timestamps occur after their reactor's sensor data end. Twenty-seven
have a latest prior sensor row more than one hour old. One gap reaches 37.45 hours;
EXP011_R02 sensor data end at 67.13 hours versus assays through 195 hours. Three
reactor runs have all-zero C (300kHz) data. These findings require explicit feature
availability and sensor-quality policy before modeling.

No imputation, final split selection, model fitting or target approval was done.
The original inline streams/statuses were not exhaustively scanned; the report
distinguishes that limitation from the complete aligned/assay profiling.

Verification: an independent standard-library CSV pass reproduced both headline
row counts. A separate original-workbook pass confirmed the 214 blank cells and
found no nonnumeric/nonfinite values among the nonblank offline assay cells.
Summary tables matched between the two EDA runs. All three figures were visually
reviewed for legibility. Clean-environment installation has not been tested.

## Scientific gates still open

- Units need semantic review beyond text in headers.
- Raw-to-aligned sensor transformations and status flags need a causal-use policy.
- Target and feature eligibility need explicit review before modeling.
- No frozen split, trained baseline, uncertainty analysis or dashboard yet.
- Data redistribution rights remain unresolved; no source files are published.

## Reports and evidence

- `docs/implementation-log.md`: chronological implementation details.
- `docs/requirements-status.md`: remaining requirement gaps.
- `outputs/source_manifest_v2.json`: source hashes and grouping inventory.
- `reports/eda-v2/report.md`: current EDA narrative, with figures and summary tables beside it.

## Specification expansion after capability review

Updated PRD to v1.2 and SRD to v0.2 in response to the owner-supplied role-capability
assessment. Current PDFs are under `docs/specifications` and linked from that
folder's README. Each contains a controlling revision and the complete retained
baseline, with an explicit precedence table and unchanged original IDs/gates.

The PRD now specifies DT-01 through DT-10: unit-operation/process contracts,
reusable simulation, fair model comparison, registry and integration outputs,
bounded scenarios/optimization, characterization, comparability exploration,
scale feasibility, PAT/chemometrics and future downstream work. The SRD derives
21 new system requirements and 16 new acceptance specifications. These are
documented plans, not passed implementation tests.

The scope retains Track A V1 and introduces Track B component acceptance. G7
still controls data-backed mechanistic/hybrid claims. Missing data may yield a
scientific no-go or synthetic-only demonstration, never a false validation result.
The EDA findings are incorporated into raw-aware assay and sensor-availability
requirements. References were checked against primary NIST/FDA source records.

Validation: checked stable unique IDs, cross-document coverage, current versions,
PDF rendering and preservation of all baseline page text/content streams. The
PRD is 30 pages (8 revision plus 22 baseline); the SRD is 35 pages (10 revision
plus 25 baseline). Original PDF files remain unchanged.

## Focused quality and distinct-value follow-up

At the owner's request, added reproducible project scripts for the two data
questions and full-source distinct-value/status profiling. Current methodology
is documented in `reports/unique-values/methodology.md`; the investigation is in
`reports/quality-review/report.md`.

Every sheet row of EXP002 and EXP011 was inspected. EXP011 R02's original feed
stream ends at 67.139444 hours but other original sensor/process streams continue
to about 195 hours. The aligned cutoff is therefore not evidence that all original
sensor recording ended. A common-coverage export is a hypothesis, not a proven
algorithm. All six VCD zeros were confirmed as numeric original cells. There is
no Status column in the relevant cell-assay sheets; sensor Status cannot approve
those labels. The issue register preserves zeros with pending review status.

Scanned all 72 original Status streams across 12 workbooks: 1,726,803 Ok records,
4,037 Warning Active records and 6,325 missing statuses. Distinct numeric profiles
cover all 58 modality/field combinations in aligned CSVs, with compressed full
value lists retained locally. No pooled training dataset or models were created.

The owner explicitly requested the Karpathy guidelines for the build. Applied
them to this bounded deliverable: assumptions stated, only relevant scripts/docs
changed, source evidence checked, and unresolved interpretation kept explicit.

## Saved preparation following the owner's EDA workflow

Implemented `scripts/prepare_data.py` backed by `biosynvia/preparation.py`. It
preserves the original archive, creates a separate checksum-verified backup,
works on deep DataFrame copies and saves combined CSVs plus an indexed SQLite
database. This paragraph is historical v3 context; it is superseded by the dated
handoff-correction section above and current `data/processed/v6` packet, while v3
remains preserved as parent evidence.

The original 378 assays retain 214 null cells and six numeric VCD zeros. All forty
raw-derived input candidates have snapshot lineage. A provisional eight-feature,
five-minute-age policy produces 333 inspection rows; six recorded-zero cases and
39 incomplete-input cases remain in the parent tables with flags. Source-unit,
availability and target review remain open; no model fitting is permitted yet.

Added numeric/type/null/unique and size audits, descriptive correlation outputs,
encoding/role maps, scientific feature-context notes, a relationship plot and
nonlinear/temporal analysis guidance. No feature is automatically removed using
whole-dataset target correlations. Found duplicate raw timestamps in EXP004;
conflicts are preserved and ambiguous candidate values withheld.

Verified all 26 software tests, source/backup/code hashes, SQLite integrity,
row counts, preserved missingness/zeros and past-only/stale-value rules. No models
were trained. The initial incomplete and diagnostic v2 runs are superseded by v3.


### Final correction close-out — 2026-11-05

The corrected consolidated packet is `reports/stage12/pre-modeling-decision-packet.md`.
Two fresh 5.6-class delegated reviews and their dispositions are saved. Supplemental
released-v6 regression tests pass 5/5 and verify zero experiment/reactor/run
mismatches across 15,120 lineage rows and 378 assays. Prior full-suite 38/38 and
updated focused Stage12 12/12 are separate runs. Three engineering hardening topics
remain deferred as documented in the resolution register, including the pandas
null-comparison FutureWarning; none is hidden as a completed fix. The five-hour
usage limit was reached during finalization; no reset was consumed.

The original-offline distinct-value report enumerates every cell/medium column,
including SEMs, globally and per run. Glucose/lactate/ammonium/osmolality have
241/319/349/140 distinct numeric values and 135/51/28/0 original blanks; none
contains a recorded numeric zero. Unique values do not identify the medium recipe
or establish waste-production causation. EGM is enabled globally for this Codex
user (`egm@egm`), verified outside BioSynvia; see
`integrations/egm-global-installation.json`. Model fitting remains paused.


## Scientific-evidence closure and owner approval checkpoint — 2026-11-05

The owner accepted Stages 1–2 as engineering work only and confirmed the order:
current VCD estimation, future forecasting, then exploratory optimization toward
a digital twin. Model fitting remains paused. The current consolidated decision
document is `reports/scientific-closure/approval-packet.md`. Its defaults are not
approved or applied to the released v6 data.

The full ten-page author manuscript was visually inspected through its official
browser PDF viewer after direct downloads were denied. Ten page images and their
hashes are retained; original PDF bytes were not archived. The evidence register
separates publication facts, inferences and remaining author questions. It confirms
Countstar BioTech/trypan-blue analysis and technical triplicates, named media and
condition mapping, calibration procedures, change-only/forward-filled process
states, nearest-neighbor alignment and below-limit concentration blanks. It also
confirms contamination and feed discontinuation in EXP011 R02, with antibiotic
exposure of both reactors. Five VCD zeros have that context; their individual QC
remains unresolved, as does the separate EXP002 R02 zero.

These facts refine previous unknowns, rather than validate every measurement.
Original 214 blank cells remain blank; no numerical censoring bounds are invented.
Assay-updated feed is withheld pending causal timing evidence. Published calibration
procedures are not per-row certificates, and process row age is not necessarily
per-variable acquisition age. Published CHO studies inform diagnostic checks but
do not validate BioSynvia predictions or a twin.

A bounded standard-library script, `scripts/summarize_scientific_decision_counts.py`,
verifies frozen inputs and counts alternative target, Status, freshness, contamination
and forecasting scenarios. The conservative joint proposal has 343 positive source
records and 308 supported current-estimation rows; alternatives retain 322 or 333.
A source-informed split alternative proposes EXP008/EXP010 (234 development/74
reserved), replacing neither the released split nor approvals. Forecast counts are
nominal ceilings only: new-origin features have not been constructed. All original
records and uncertainties remain retained. Source extraction, counting and fresh
packet review use configured gpt-5.6-terra at medium reasoning; engineering review
is not scientific approval.

Scientific closure final verification: the bounded count script reproduces all
three count artifacts byte-for-byte; ten official-viewer captures have retained
hashes; local packet links resolve; the v6 manifest and approval flags are unchanged.
Fresh review findings are resolved in
`reports/scientific-closure/decisions-and-resolutions.json`. Table2 footnotes are
now source-verified rather than unresolved. The nine owner decisions remain
pending. No model was fitted.

## Public project packaging — 2026-11-06

Prepared the public GitHub project at the owner's request. Added a project
walkthrough, a focused README and invented synthetic CSV examples. The synthetic
audit passes with zero errors and one expected missing-value warning; all 18
source-independent audit/inventory tests pass on Python 3.12. The system Python
3.9 does not meet the documented Python 3.11+ requirement.

The public package excludes original/processed datasets, large value enumerations,
source-cell observation exports, personal plugin installation records and local
credentials. The full local research files remain intact. Staged text was checked
for common credential patterns; no matches were found. Git attributes preserve
fingerprinted artifact bytes and mark PDFs/images as binary. Scientific approvals
and fitting gates are unchanged; no model was fitted for this publication.


## Formal research attribution — 2026-11-06

Verified the five authors, titles, dates, versions and distinct DOIs against the
preprint publisher and Zenodo records. Added root `CITATIONS.md` and portable
`references.bib`, full README references, and attribution/license information for
the retained manuscript captures. The preprint is identified as not peer reviewed.
Dataset rights remain unresolved separately from the article's CC BY 4.0 notice.
No original data, frozen observations, source-image bytes or model gates changed.


## Public presentation and rights update — 2026-11-06

Refreshed the README with original branding, problem/benefit overview, dataset
summary, three existing descriptive EDA figures and a staged digital-twin roadmap.
Added restricted proprietary evaluation terms for original BioSynvia work, with
third-party rights kept separate. Supplied build/reference documents, manuscript
captures, development-tool copies and the local ignore file are excluded from
the current public tree while local copies remain intact. Fitting stays paused.

## README presentation alignment — 2026-11-06

Reworked the public README to follow the owner's Campaign Prophet presentation:
centered banner/badges, emoji section navigation, layered overview, tables,
expandable findings, visual gallery, project structure and a checked roadmap.
Added an implementation-grounded technology stack, distinguishing current tools
from planned modeling. Citations, restricted licensing, paused fitting and local
reference exclusions remain intact. No application behavior or data changed.


## Research motivation and goal — 2026-11-06

Centered the public project goal on investigating lower-intervention bioprocess
research: current VCD estimation, forecasting, abnormal-culture warning research,
process-response modeling and an eventual validated hybrid digital twin. The
README distinguishes intended reductions in sampling, contamination opportunities
and unnecessary experiments from demonstrated outcomes. EXP011 remains a single
challenge case, not validated contamination-detector evidence. Reference assays,
aseptic technique, prospective validation and the paused fitting gate are retained.
No application behavior, datasets or approval flags changed.
