# Requirements reconciliation

Current controlling editions are PRD v1.2 and SRD v0.2. Their PDFs include the
complete original baselines; the baseline FR/SR requirements below remain in force.
The added DT scope and tests are specified but unimplemented. Track A software
progress is not acceptance of Track B modeling components.

The authoritative PRD was recovered from Downloads and copied unchanged to
`docs/specifications/BioSynvia_PRD_v1.1_Problem_First.pdf` on 2026-11-05.
The accompanying `.txt` is a text extraction for implementation reference, not
a revised specification. The owner supplied SRD v0.1; it is now preserved unchanged
beside the PRD, with a text extraction. Its schemas are proposed designs, not
proof that the existing staging CSV contract meets them.

| PRD requirement | Current evidence | Remaining work |
| --- | --- | --- |
| FR-01 Archive provenance and integrity | `inventory` command verifies the published MD5 before listing ZIP members; records DOI, URL, hashes, sizes and manifest creation time | Preserve exact retrieval event separately; confirm reuse terms |
| FR-02 Hierarchical file inventory | Source filenames reconciled to 12 experiments, two reactors and both modalities; duplicate/missing/mode checks; all 60 files inventoried | Continue cross-checking source content against filename metadata |
| FR-03 Typed unit-aware canonical data | Provisional CSV validator and synthetic tests | Source adapter; field provenance, quality flags, plausibility policies, process mode and unit dictionary |
| FR-04 Time-alignment audit | Future-only sensor availability excluded from the audit count | Original/aligned timestamp analysis, lag tolerances, causal joins and tests |
| FR-05 Target selection | Candidate inventory only | Real coverage, biological interpretation, no-leakage policy and reviewed target decision |
| FR-06–FR-11 | Not implemented | Group splits, feature generation, baselines, evaluations and dashboard |
| FR-12 Qualified claims | README, CLI and reports identify the current research-only status | Carry labels into future model cards and UI |
| FR-13–FR-18 | Not implemented | Uncertainty, ablations, registry and gated mechanistic/hybrid extensions |

No milestone is accepted as complete. In particular, M1 requires a real-data
target decision and data dictionary, not just a successful checksum or synthetic
audit. Do not change the expected publisher checksum to accept a failed download.

The existing CSV contract remains an internal staging format. It does not yet
implement the PRD's full sensor-sample/offline-assay provenance or timestamp model.
Source-specific ingestion must preserve those fields before any model-ready claim.

## SRD reconciliation and first real-data EDA

- SR-DAT-001: source observation parsing is preceded by publisher checksum verification in the EDA script.
- SR-DAT-002: source manifest now includes citation, tool version, rights status,
  hashes and local file time. Exact retrieval event remains unrecorded and explicit.
- SR-DAT-003: all expected filename combinations reconciled; 18 software tests
  include missing/duplicate combination and mode mismatch cases.
- SR-DAT-004/005/006: first real-data field profiles, missingness and original/aligned
  offline comparisons generated. Full original sensor statuses and causal alignment
  reconstruction remain open.
- SR-DAT-007: no target approval and no model fitting. VCD recommendation remains provisional.
- SR-DAT-008: EDA writes to a new directory and protects old runs, but is not yet an
  atomic approved-artifact pipeline. Interrupted partial EDA outputs are unapproved.
- SR-FEA-001 and later modeling requirements remain unimplemented; do not treat
  the EDA sensor-availability count as a complete feature snapshot builder.

## Added component scope

PRD DT-01 through DT-10 map to SRD SR-DT-001 through SR-DT-021 and acceptance
specifications T-019 through T-034. All remain proposed. The new raw-missingness
and stale-input requirements are motivated by real EDA findings but are not yet a
completed canonical/feature implementation. The source data do not establish
Raman, downstream chromatography, cross-scale validation, formal product
comparability or an operational Digital Twin.

## Authorized Stages 1 and 2 protocol increment (2026-11-05)

The owner authorized execution of these stages, superseding the plan's historical
awaiting-approval label. See `docs/stage12-executable-spec.md` and the consolidated
packet under `reports/stage12`. This engineering increment does not pass G1/G2/G3,
M1/M2 or CG1; scientific approval and later model/release acceptance remain open.

| Requirement/gate | Current bounded disposition | Evidence / remaining condition |
| --- | --- | --- |
| FR-01/02, SR-DAT-001/002/003 | Source structure/integrity implemented and tested; provenance partial | Verified archive/backup, member and producer hashes; exact retrieval and reuse rights unknown |
| FR-03, SR-DAT-004/006, SR-FEA-001 | Selected-observation dictionary, source coordinates and independent quality flags implemented | Canonical snapshots and original assay cells; units/status meaning remain unverified; archive retains full raw history |
| FR-04, SR-DAT-005, SR-FEA-002/003, SR-DT-003, T-020/021 | Raw past-only snapshots and explicit unknown-availability scenario implemented/tested | Raw-to-aligned resampling/offset, clock/order precision and real result availability unresolved; strict scenario has no supported predictions |
| FR-05, SR-DAT-007, G1 | Target recommendation/record implemented; approval blocked | VCD source/units/cadence/counts and two label sensitivities recorded; no primary mask or scientific assay approval |
| SR-DAT-008 | Versioned atomic artifact promotion implemented/tested | Payload/input hashes, CSV/SQLite agreement and incomplete-run protection; scientific acceptance separate |
| FR-06, SR-FEA-006/007 | Target-blind paired-group split proposal implemented/tested; approval pending | Exact coverage fractions, paired reactors and explicit inner/outer groups; prior EDA exposure disclosed |
| SR-FEA-005/008 | Feature eligibility and missing-input population evidence implemented | All input approvals false; unsupported/abstention protocol specified, prediction execution deferred |
| SR-FEA-004, FR-07–11, SR-MOD, G2/G3, M2 | Deferred to gated modeling stages | Rolling windows, fitted preprocessing, model selection/evaluation and workbench not executed |
| DT-06/SR-DT-012, CG1 and component release | Full characterization/scientific release deferred | Sampling/quality packet is a subset; no growth-window, mechanistic, comparability or component acceptance claim |

Agent reviews check engineering and reasoning. Their agreement supplies no assay
validation or independent scientific sign-off. Unknown authority is retained in
the issue register while unaffected engineering continues.
