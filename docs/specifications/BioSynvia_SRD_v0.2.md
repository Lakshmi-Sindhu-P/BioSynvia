# BioSynvia System Requirements Document

## Version 0.2

November 5, 2026. Working title. Owner: Lakshmi Sindhu Pulugundla.

### System objective

Implement the offline CHO soft-sensor workbench in PRD v1.2 and a separately gated package of reusable bioprocess modeling components. The component package combines typed process data, model execution, numerical verification, registry and versioned research outputs. Physical-system synchronization, closed-loop control and operational Digital Twin validation remain outside scope.

### Edition control and requirement status

Part A is the controlling v0.2 expansion. Part B reproduces SRD v0.1 in full, retaining every SR-DAT, SR-FEA, SR-MOD, SR-UI, SR-MH and SR-NFR ID and acceptance test T-001 through T-018. Original version/page labels identify baseline content. PRD v1.2 controls product scope. This SRD defines proposed system behavior and tests; none of the new SR-DT requirements is declared implemented.

| Baseline location | Effective v0.2 change |
| --- | --- |
| Sections 1 through 3 | Add Track B component architecture and release distinction |
| Sections 4.1, 4.2 and 6 | Add raw-assay missingness invariants, unit-operation and modality metadata, explicit availability semantics |
| Sections 4.5, 7 and 8 | Add callable simulation, evidence tiers, registry/consumer, characterization and bounded optimization |
| Sections 9 and 10 | Retain T-001 through T-018; add T-019 through T-034 and new DT traceability |
| Sections 11 through 13 | Add CG1 through CG5 and component-release acceptance; retain Track A gates |

### Current implementation evidence

Archive verification, source filename reconciliation, the provisional audit CLI and project-owned EDA script exist. EDA found 214 original assay blanks represented as aligned zeros and incomplete temporal sensor coverage. The 18 current regression tests are software evidence only, not completion of T-001 through T-018. Target approval, canonical/model-ready release, model fitting, component simulation and dashboard acceptance remain open. [E1]

Track B B0 requirements are required for the component release; B1 requirements need acceptance or an approved deferral. Gated requirements must emit an eligibility decision. Synthetic component verification cannot be counted as real-data model validation.

<!-- page -->
## 1 Component architecture and canonical extensions

The offline flow is source verification, raw-aware data audit, canonical records, approved target/features, group-safe evaluation, component registration, bounded execution, validated outputs and independent consumer/read-only review. No module may bypass source, target, split or evidence-tier checks by calling the numerical solver directly through the supported interface.

### Logical entities and invariants

| Entity | Required information | Invariant |
| --- | --- | --- |
| UnitOperation | ID, type, material context, scale/context metadata and provenance | Unknown material/scale attributes explicit; no invented CGT identity |
| Measurement | Experiment/reactor/unit-operation IDs, field/variable IDs, inline/at_line/offline modality, event and availability time, values/units/quality/source refs | Availability unknown remains null with reviewed assumption; never autoequal to event time |
| ParameterSet | ID/version, component version, named values and units, fit groups, bounds, covariance/uncertainty where available, approval | Only compatible immutable versions; synthetic and fitted values distinguishable |
| Component | ID/version/family, state/input/output schemas, equations artifact hash, applicability domain and evidence tier | No dashboard dependency; no untrusted executable loading |
| Scenario | ID/version, component/parameter refs, initial state, input schedule, times, objective/constraints, seed and budget | Immutable request plus source/assumption provenance |
| ResearchArtifact | Schema/type/version, payload hashes, parents, status, units, timestamps and claim limits | No measured/simulated label ambiguity; missing outputs never fabricated |

### Added data controls

SR-DT-001 (B0; DT-01). The system shall validate these entities and referential links, including unit-operation/material context and the acquisition-versus-availability distinction. Missing required references or incompatible units shall block execution. Unknown metadata may be explicit only where the schema permits it. Evidence: T-019 and T-020.

SR-DT-002 (B0; DT-01 and DT-06). Canonical assay validity shall derive from original sheets. A blank original assay shall retain unknown_missing_cause, null canonical value and source pointer even if an aligned cell is zero. A zero present in the original record shall remain a distinct observed value, subject to quality review. Record original and aligned values separately. Evidence: T-021.

SR-DT-003 (B0; DT-01 and DT-03). Feature eligibility shall combine acquisition/availability policy, original sensor quality status, accepted alignment policy, required-channel support and reviewed maximum age. Stale/missing/ineligible features shall produce unsupported status or a preregistered missing-feature policy. Do not treat any prior sensor row as proof of feature validity. Evidence: T-020 and existing T-005/T-010.

<!-- page -->
## 2 Reusable execution and numerical requirements

### Model interface

SR-DT-004 (B0 and G7; DT-02). A public local interface shall expose describe, validate and simulate operations independent of the dashboard. A request binds the component version, initial state, process-input schedule, parameter version, output-time grid and solver settings. A consumer shall invoke it without duplicating equations. Invalid requests fail before numerical execution. Evidence: T-022.

SR-DT-005 (B0 and G7; DT-02). Each mechanistic component shall define equations, state meaning/units, parameter units and signs, feed/volume/dilution conventions and applicability bounds. Numerical verification shall include a known analytic limiting case, tolerance refinement, state/flow consistency and declared conservation/positivity rules. If a conservation law is intentionally approximate, document the omitted terms and accepted diagnostic. Scientific error budgets shall be justified before acceptance, not invented after fitting. Evidence: T-023 and T-024.

SR-DT-006 (B0; DT-02 and DT-03). Eligibility shall resolve to synthetic_verified, data_calibrated, group_evaluated or unsupported, with source and review evidence. G7 failure shall block data-backed calibration claims while permitting an isolated synthetic demonstration. Hybrid outputs inherit limitations of their mechanistic and correction components. Evidence: T-025.

### Comparative evaluation

SR-DT-007 (B0 and G7; DT-03). Statistical, mechanistic and hybrid comparisons shall share a frozen group manifest, observed-target mask, target unit and declared information scenario. Model-family differences in initialization or assay inputs shall create separate comparison strata. Preprocessing, calibration, correction and parameter selection use training groups only. Unsupported families are not assigned fabricated errors. Evidence: T-026 and T-007/T-008/T-009.

SR-DT-008 (B0; DT-03 and DT-06). Evaluation shall retain per-experiment errors, coverage/abstention counts, macro group summaries, fit failures, eligibility outcomes and negative baseline deltas. Uncertainty distinguishes numerical, parameter, predictive and scenario uncertainty. An absent interval shall be null with a reason, never an implied zero-width interval. Evidence: T-026 and existing T-011/T-012.

### Failure behavior

Solver failure, physically inadmissible states, unsupported bounds, unknown units or insufficient data shall return explicit status and reason codes. Partial solver output may be retained as unapproved diagnostics, but no approved prediction/trajectory shall be emitted for the failed request. All failures retain request IDs, parameter/model refs and reproducible diagnostics.

<!-- page -->
## 3 Registry outputs and downstream consumer

SR-DT-009 (B0; DT-04). Registry metadata shall bind model/component, equations/code hashes, parameter set, feature/target contracts, training groups, environment, schema versions, evidence tier, domain and approval records. Any changed dependency invalidates approval/cached results. No entry marked approved_for_research implies manufacturing validation. Evidence: T-027.

SR-DT-010 (B0; DT-04). Metadata shall be JSON validated against published versioned schemas; tabular trajectory/prediction payloads shall be typed Parquet with declared units/time semantics and finite-or-null values. Serialize measured, predicted and simulated origins separately. Unsupported point outputs must be null, not zero or NaN. Evidence: T-019, T-027 and T-028.

SR-DT-011 (B0; DT-04). A separate local consumer shall validate schemas and payload digests and read outputs without importing private scientific implementation modules. Accept supported schema versions only; reject unknown major versions, digest mismatches, missing required units and unresolved parameter refs. Safe loading rules in SR-NFR-011 remain in force. Evidence: T-028.

### Proposed simulation request contract

Required top-level keys: schema_version, request_id, unit_operation_id, component_ref, parameter_set_ref, evidence_mode, initial_state, input_schedule, output_times_hours, solver and provenance_refs. Named state/input/parameter values are paired with units; reference objects carry ID, version and SHA-256. No example below is an observed dataset value.

Output times shall be finite and increasing within the permitted horizon. Input schedules shall define interpolation/hold semantics and event order, cover the requested horizon and reject overlapping ambiguous segments. Units must resolve through the approved conversion registry. Evidence: T-019, T-022 and T-023.

### Proposed result envelope

```json
{
  "schema_version": "1.0.0",
  "artifact_kind": "simulation",
  "request_id": "synthetic-contract-example",
  "execution_status": "unsupported",
  "evidence_tier": "unsupported",
  "trajectory_ref": null,
  "predicted_value": null,
  "uncertainty": null,
  "reason_codes": ["PARAMETER_SET_NOT_APPROVED"],
  "research_only": true
}
```

Successful envelopes additionally require component/parameter/schema refs, units, time origin, applicability, numerical diagnostics, source/parent hashes, creation time, environment and uncertainty-status metadata. Null fields must satisfy the status-specific schema; unsupported examples do not exempt successful outputs from those fields.

<!-- page -->
## 4 Characterization comparability and troubleshooting

SR-DT-012 (B0; DT-06). A characterization protocol shall define analysis windows, growth/trajectory summaries, units, valid data masks and experiment-level uncertainty. Summarize paired reactors within experiments; record process mode, design settings, quality events and confounders. Invalid growth-rate windows shall return unavailable with a reason. Evidence: T-029.

SR-DT-013 (B1 and G; DT-07). Comparability requests shall contain a defined change, attributes/units, group assignments, estimand, margins with scientific rationale, uncertainty/multiplicity plan, assay support and reviewer. Missing prerequisites force descriptive_only or insufficient_evidence status. A nonsignificant difference must never automatically yield equivalent. VCD differences shall not be labeled product-quality comparability without the required quality attributes. Evidence: T-030.

SR-DT-014 (B0; DT-06). Troubleshooting outputs shall separate observations, candidate hypotheses and required follow-up. Status flags, long gaps and all-zero channels shall retain source evidence and not become an automated causal diagnosis. Evidence: T-029.

### Characterization artifacts

Produce characterization_protocol.json, per_experiment_characterization.parquet, sensor_quality_summary.parquet and process_characterization_report.md. Each summary carries group IDs, time windows, valid counts, units, quality/exclusion rules and source/config hashes. Compare mode-associated patterns descriptively unless adjusted estimates have adequate independent-group support.

The current 12-group design does not justify treating 274,781 sensor rows as independent replication. Growth-phase selection, transformations and exclusion decisions must be logged. Restrict any bootstrap to a justified experiment/paired structure and state the limitations of inference with three fed-batch groups.

### Comparability artifacts

Store comparison_protocol.json and comparability_report.md with a status enum: descriptive_only, insufficient_evidence, inconclusive or protocol_criterion_met. The last means only that a prespecified research criterion was met. It must not be rendered as regulatory approval or product comparability without separate appropriate evidence and review. Reviewer-defined margins are required; no default biological threshold is supplied.

### Current EDA issue disposition

The 214 raw blanks/aligned zeros require SR-DT-002 regression fixtures. Fourteen post-recording assays and 27 assays with prior sensor age over one hour motivate SR-DT-003; one hour is a diagnostic sensitivity level, not an approved universal maximum age. Entirely zero fitted C channels require quality review, not silent deletion. These findings are descriptive evidence from E1, not accepted scientific thresholds.

<!-- page -->
## 5 Sensitivity scenarios and constrained optimization

SR-DT-015 (B1 and G; DT-05). Sensitivity, sweep and optimization requests shall specify model/parameter versions, evidence tier, initial states, decision variables/units, objective/units/direction, constraints, bounds/domain provenance, seed, solver and evaluation/time budget. Freeze the protocol before the run. Missing objective, undefined units or unapproved operating bounds block optimization. Evidence: T-031.

SR-DT-016 (B1 and G; DT-05). Validate schedules, domain, numerical state limits and constraints both before and after simulation. Return feasible, infeasible, unsupported, numerical_failure or budget_exhausted. A failed candidate may not be labeled optimal. Confirm returned feasible candidates with tighter solver tolerances and sensitivity to model/parameter uncertainty, and report boundary hits. Evidence: T-031 and T-032.

SR-DT-017 (B1; DT-05). Store every evaluated scenario, objective, feasibility result, failure and stopping reason in an immutable local ledger with complete lineage. Do not suppress nonconvergence or use held-out experimental outcomes to optimize settings. Report model-conditional optima as hypothetical and unconfirmed by experiment. Evidence: T-032.

### Bounded execution policy

The scientific protocol must supply finite bounds and a finite evaluation/time budget. No automatic cloud compute, external service, scheduling or live process actuation is introduced. Existing no-cloud-cost rules remain. A local timeout or exhausted budget yields a terminal status and retained diagnostics, not a silently restarted unlimited search.

Positive-state checks, conservation checks and solver tolerances are component-specific. Small numerical negatives may be flagged within an approved tolerance; do not clip them silently. Include validation that the proposed solution is feasible under the accepted numerical policy and that claimed benefit does not disappear under reasonable tolerance refinement.

### UI and service separation

The simulation executor is a local CLI/library. The read-only dashboard displays previously generated scenarios and comparisons with visible hypothetical labels. Dashboard launch must not fit, calibrate, optimize, mutate registry records or contact process equipment. This preserves SR-UI-007 and SR-NFR-009. A later interactive computation design requires a new explicit scope decision and read/write separation.

### Model risk disclosure

Observed calibration fit, held-out prediction, numerical verification and optimization feasibility are different evidence types. Neither a converged solver nor a feasible optimizer establishes biological usefulness. If parameter identifiability is inadequate, block data-backed scenario recommendations and retain only clearly separated synthetic demonstrations.

<!-- page -->
## 6 Conditional scale PAT and downstream extensions

SR-DT-018 (G; DT-08). Produce scale_translation_feasibility.md identifying scales, relevant geometry/engineering variables, comparable biology, units and evidence gaps. No cross-scale validation status is permitted without a suitable dataset, independently defined scale groups and a transfer-evaluation protocol. Volume differences alone shall not create kLa, mixing, shear or power-input measurements. Evidence: T-033.

SR-DT-019 (G; DT-09). A spectroscopy adapter contract shall include modality, instrument/calibration metadata, spectral axis/intensity units, sample and reference IDs, measurement availability, experiment/batch groups and source hashes. Preserve a separate dataset namespace; absent spectroscopy data yields data_unavailable rather than simulated Raman validation. Evidence: T-034.

SR-DT-020 (G; DT-09). PCA/PLS or other chemometric preprocessing, component selection and reference alignment shall be train-group-only and point-in-time valid. Do not merge unrelated CHO and spectroscopy records as if they were paired observations. Missing units/reference linkage block a scientific modeling claim. Evidence: T-034 and existing T-007.

SR-DT-021 (Future G; DT-10). A downstream extension shall require a separate chromatography source, unit-operation/material contract, operating variables, chromatogram/analytical outputs, source rights, group design and evaluation protocol. Until approved, return not_implemented or data_unavailable and produce a documented extension contract/gap record. Evidence: T-034.

### Extension evidence statuses

Each extension shall distinguish contract_defined, data_unavailable, synthetic_verified, data_calibrated, group_evaluated and unsupported. Data-gap reports are accepted feasibility deliverables; they do not count as executed scientific validation. Separate datasets retain separate provenance and evaluation scopes even when consumed by a common registry.

### Artifacts and dependency references

| Artifact | Producer | Required parents |
| --- | --- | --- |
| component_contract.json | Component authoring | Schema version, equations/code ref, intended use |
| parameter_set.json | Calibration/review | Component, fit-group manifest, units and bounds |
| simulation_request.json | Scenario authoring | Component, parameter set, input/domain protocol |
| result.json and trajectory.parquet | Execution | Request, source refs, environment and solver |
| consumer_validation.json | Independent consumer | Result/schema/payload digests |
| scale/PAT/downstream feasibility reports | Extension audit | Source inventory, required fields and gap decisions |

Paths are local and manifest-controlled. Use atomic approved-artifact promotion after complete validation; interrupted writes remain unapproved. Do not load arbitrary serialized executables to satisfy a registry reference.

<!-- page -->
## 7 Added acceptance tests and product traceability

T-001 through T-018 remain required where applicable. These new tests are proposed specifications; no execution pass is claimed here.

| Test | Fixture and required result | Requirements |
| --- | --- | --- |
| T-019 | Missing unit-operation ref, incompatible unit or wrong schema type/version is rejected; valid typed contract passes | SR-DT-001/010; DT-01/04 |
| T-020 | A result collected before cutoff but available after cutoff is excluded; unknown availability needs reviewed policy | SR-DT-001/003; DT-01/03 |
| T-021 | Original blank plus aligned zero stays missing; original measured zero stays observed with provenance | SR-DT-002; DT-01/06 |
| T-022 | Separate caller invokes component without copying equations; invalid input never reaches solver | SR-DT-004; DT-02 |
| T-023 | Known analytic limiting case and unit-consistent balance fixture match approved numerical tolerances | SR-DT-005; DT-02 |
| T-024 | Tolerance refinement and state/conservation violation trigger diagnostics or rejection as specified | SR-DT-005; DT-02 |
| T-025 | Failed G7 or unidentifiable parameter set cannot become data-backed evidence; synthetic output stays labeled | SR-DT-006; DT-02/03 |
| T-026 | Family comparison with different groups, target masks or input scenarios is rejected or separated; negative result retained | SR-DT-007/008; DT-03 |
| T-027 | Mutated parameter/code/payload hash invalidates lineage; missing uncertainty is explicit | SR-DT-009/010; DT-04 |
| T-028 | Independent consumer reads valid outputs and rejects corrupt payloads/unsupported major schema versions | SR-DT-010/011; DT-04 |
| T-029 | Unequal reactor/group sizes preserve paired experiment summaries; inadequate growth window returns unavailable | SR-DT-012/014; DT-06 |
| T-030 | Missing comparison margins or quality attributes forces descriptive/insufficient status; nonsignificance does not imply equivalence | SR-DT-013; DT-07 |
| T-031 | Out-of-domain, incompatible-unit, unconstrained or infeasible scenario is rejected; failed point not labeled optimum | SR-DT-015/016; DT-05 |
| T-032 | Budget exhaustion returns terminal status; all evaluations retained; feasible candidate rechecked numerically | SR-DT-016/017; DT-05 |
| T-033 | Single-scale/volume-only data produces gap report and blocks cross-scale validation claim | SR-DT-018; DT-08 |
| T-034 | Missing spectra/references/chromatography data yields gap status; train/test or cross-dataset mixing fails | SR-DT-019/020/021; DT-09/10 |

Track B release coverage is all ten DT product IDs through SR-DT-001 through SR-DT-021. B0 engineering requirements must pass; scientific conditional branches require documented eligibility/no-go. A deferral is not a passing test. The QA report shall distinguish implemented, tested, blocked, failed and deferred requirements.

<!-- page -->
## 8 Release acceptance source register and baseline

### Component release sequence

CG1 requires the raw-aware data/characterization pack and disposition of EDA issues. CG2 requires component contracts, equations/state/unit review and G7 evidence tier. CG3 requires numerical verification, versioned registry/output schemas and independent consumer tests. CG4 requires fair family comparisons where eligible plus bounded scenario/optimization evidence or approved B1 deferral. CG5 assembles the reproducible research component package, extension gap reports and claims review.

Retain the original source, target, split, holdout, naming and data-rights gates. Track A acceptance does not assert Track B acceptance. A complete component engineering package may contain a synthetic_verified simulation but shall not be labeled a validated CHO mechanistic/hybrid model. No target approval, independent scientific review or release sign-off is fabricated by this document update.

### Required reviewer evidence package

Provide the full source/quality manifest, target and feature approvals, group protocol, component/equations contract, parameter/identifiability record, solver verification, applicable model comparisons, characterization report, comparability status, scenario ledger, registry and consumer results, pinned environment and exact reproduction commands. Include negative results, unsupported states and extension data gaps. Acceptance records identify reviewer, date, purpose, scope and artifacts.

### Added sources and evidence

R9. NIST publication record for Satwekar et al., Operationalizing Digital Twins in Biomanufacturing through Interoperable Process Analytical Technology, July 16, 2026; DOI 10.1007/s00449-026-03369-9. Architectural context only; no standards-conformance claim.

https://www.nist.gov/publications/operationalizing-digital-twins-biomanufacturing-through-interoperable-process

R10. FDA PAT framework guidance, October 2004. Used to frame process measurements and modality interfaces, not as regulatory approval.

https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pat-framework-innovative-pharmaceutical-development-manufacturing-and-quality-assurance

R11. FDA/ICH Q5E guidance, June 2005. Used to distinguish exploratory trajectory comparison from product comparability around manufacturing changes.

https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q5e-comparability-biotechnologicalbiological-products-subject-changes-their-manufacturing-process

E1. BioSynvia reports/eda-v2/report.md, summary.json, source_manifest.json, raw_aligned_assay_comparison.csv and scripts/eda.py. Supports descriptive local data findings; does not validate model predictions or exhaustively audit original inline status streams.

### Part B retained SRD v0.1

The following 25 pages reproduce the complete baseline unchanged. Read baseline statements such as proposed not built and optional P2 together with this edition's current-status and two-track scope rules. The baseline's FR/SR/test IDs remain stable. References to PRD v1.1 in retained pages mean the retained foundation as controlled by PRD v1.2 Part A.

End of controlling revision. Retained baseline follows.
