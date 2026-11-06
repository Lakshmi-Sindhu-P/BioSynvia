# BioSynvia Product Requirements Document

## Version 1.2

November 5, 2026. Working title. Owner: Lakshmi Sindhu Pulugundla.

### Problem and intended result

Bioreactor sensors record process conditions frequently, while laboratory assays measure biological state intermittently. BioSynvia investigates whether these signals can estimate a measured biological attribute in unseen CHO experiments. It will also develop reusable research modeling components with documented inputs, equations, validity limits and integration outputs for future Digital Twin architectures.

The expanded objective is to design, implement and evaluate bioprocess modeling components combining experimental data, statistical and mechanistic models, offline simulation, scientific validation and versioned outputs. The deliverable is a research component package. An operational Digital Twin would require physical-system connections and lifecycle integration beyond this project's scope. [S9]

### How this edition is controlled

This is an expanded edition, not a replacement of the V1 scientific foundation. Part A contains the controlling v1.2 revisions. Part B reproduces PRD v1.1 in full to retain every original requirement, gate, source and acceptance criterion. Original page numbers and version labels in Part B identify retained baseline text, not the current edition.

Where scope, status or sequencing differs, Part A controls the specified clauses. All other baseline provisions remain effective. SRD v0.2 supplies the corresponding implementation contracts. Requirements describe intended behavior and do not establish that it has been built or scientifically approved.

### Two distinct release claims

| Release | Required outcome | Permitted description |
| --- | --- | --- |
| Track A V1 | Existing audited soft-sensor pipeline, grouped evaluation, failure analysis and read-only review | Offline CHO soft-sensor research workbench, after its gates pass |
| Track B component release | Reusable unit-operation contract, callable component, registry, consumer demonstration and characterization pack | Research modeling components intended for future Digital Twin integration |
| Track B data-backed simulation | G7 eligibility plus fitted-model and numerical verification evidence | Data-calibrated research simulation within documented limits |

Neither release permits claims of a complete CGT Digital Twin, industrial deployment, validated process control, product comparability or experimentally confirmed optimization. There is no J&J affiliation or claim of satisfying a hiring decision.

<!-- page -->
## 1 Change control and verified project status

### Baseline clauses updated by this edition

| Baseline location | Effective revision |
| --- | --- |
| Sections 1.1 and 1.3 | Add reusable unit-operation modeling, component integration and process characterization to product objectives |
| Sections 1.4 and 5.3 | Retain all exclusions; distinguish research components from a complete operational Digital Twin |
| Sections 3.1 and 3.5 | Add observed EDA evidence below; keep source facts separate from measured local findings |
| Sections 5.2 and 6 | Retain FR-01 through FR-18; add DT-01 through DT-10 with Track B priorities |
| Sections 7 through 9 | Add characterization, comparability, simulation and integration workflows in Sections 3 through 5 of Part A |
| Sections 11 through 13 | Retain G0 through G9 and M1 through M5; add component gates CG1 through CG5 |
| Sections 12, 14 and 16 | Add dependencies, effort assumptions, research risks and unresolved decisions in Section 6 of Part A |

### Evidence available on November 5

The archive was downloaded and its published MD5 verified. Filename reconciliation found 12 experiments, two reactors per experiment, 12 workbooks, 192 worksheets and 48 aligned CSVs. There are 9 batch and 3 fed-batch experiment groups. [E1]

The project-owned EDA script counted 274,781 aligned sensor rows and 378 assay timestamps. Aligned files contain 40 sensor/process fields, including two cumulative weight channels, and 16 assay fields comprising ten primary measures and six SEM fields. These counts describe columns, not independent biological replicates. [E1]

All 378 original VCD means are nonmissing and match aligned values. However, 214 original assay blanks appear as zeros in aligned files: 135 glucose, 51 lactate and 28 ammonium cells. Fourteen assays occur after their reactor's aligned sensor recording ends. Twenty-seven assays have a latest prior aligned sensor row over one hour old. [E1]

### Consequences for the product

The original assay mask is authoritative for determining observed targets. Missing laboratory measurements shall not become zero labels. Zero VCD values that exist in original records remain subject to assay-quality review and shall not be silently discarded. Sensor availability, quality flags and alignment causality must be resolved before model readiness.

The dependency-free audit CLI, source inventory, EDA script and 18 software tests exist. These tests are not the SRD's 18 acceptance scenarios. No scientific target approval, model-ready data release, model comparison, frozen holdout, simulation component or dashboard has passed acceptance. VCD is a provisional candidate, not an approved target.

<!-- page -->
## 2 Added product requirements

Track B priorities are local to the component release. B0 means required for that release, B1 means required or explicitly deferred with rationale, and G means data-gated. They do not silently expand Track A's P0 scope.

| ID and priority | Product requirement | Acceptance evidence |
| --- | --- | --- |
| DT-01 B0 | Represent experiment, reactor, unit operation, material context, measurement modality, units and provenance in versioned contracts | Schema and referential-integrity tests; acquisition and availability times distinguished; unknown metadata explicit |
| DT-02 B0 and G7 | Provide a callable upstream bioreactor component with typed initial state, process inputs, parameter set and outputs | Independent invocation without copying equations; solver, unit and failure tests; synthetic-only mode if G7 fails |
| DT-03 B0 and G7 | Compare statistical, mechanistic and hybrid approaches when each is eligible | Identical experiment groups, observed labels, information availability and evaluation units; unsupported families reported as not evaluated |
| DT-04 B0 | Register models and export versioned integration outputs | Registry resolves complete lineage; separate consumer reads validated artifacts; unknown schema and altered artifact rejected |
| DT-05 B1 and G | Support bounded sensitivity analysis, scenario sweeps and constrained optimization | Objective, bounds and solver budget fixed; invalid scenarios rejected; feasible result and uncertainty reported or explicit no-feasible-solution outcome |
| DT-06 B0 | Characterize experiments, growth trajectories, sensor behavior and mode-associated variation | Per-experiment report with pairing, valid counts, exclusions, uncertainty and design-confounding statement |
| DT-07 B1 and G | Explore process comparability using a defined change and comparison protocol | Prespecified attributes, margins and groups where defensible; descriptive-only status when prerequisites fail |
| DT-08 G | Assess scale-translation feasibility | Cross-scale engineering and measurement evidence, or explicit gap report; no scale-up claim from volume alone |
| DT-09 G | Add PAT and spectroscopy interfaces with chemometric workflow | Separate licensed dataset with spectra/reference linkage; training-only preprocessing; grouped external evaluation |
| DT-10 Future G | Define a downstream unit-operation extension | Separate chromatography dataset and process contract before implementation or validation claims |

The earlier P2 classification still applies to data-backed mechanistic/hybrid validation in Track A. Track B makes the reusable interface and honest eligibility outcome explicit deliverables. A verified synthetic demonstration can satisfy interface engineering evidence but cannot satisfy data-backed model validation.

<!-- page -->
## 3 Scientific use cases and comparison rules

### Process characterization and troubleshooting

The scientist shall be able to compare measured VCD trajectories, viable/total cell relationships, assay cadence, sensor coverage, growth summaries and failure events across all experiments. Characterization shall identify its time windows, actual sample support, missingness and quality exclusions. Specific growth-rate estimates require positive measurements, adequate time support and an explicit fitting window; no logarithm of a filled zero is permitted.

Pairing shall be preserved in summaries and uncertainty. Compare reactors within each experiment before aggregating between experiments. Record available design settings and confounders. Fit adjusted models only when the number of independent groups and design support the requested adjustment. With 12 groups and three fed-batch groups, report uncertainty and avoid treating minute-level sensor rows as independent replicates.

Troubleshooting shall expose observed events, candidate explanations and missing evidence separately. A sensor gap or all-zero channel can motivate a quality flag; it does not prove an instrument fault, cell death or a causal mechanism. Measured differences shall remain visible even when they contradict a preferred model narrative.

### Comparability exploration

Comparability requires a defined process change, relevant attributes, intended interpretation, group assignment, assay methods and prospectively justified criteria. A batch/fed-batch trajectory comparison alone is exploratory characterization. A nonsignificant difference is not evidence of equivalence. Unavailable product-quality attributes shall not be replaced with VCD and described as product comparability. FDA/ICH Q5E concerns product assessment around manufacturing changes; it is context for boundaries, not a certification standard met by this prototype. [S11]

Where equivalence testing is scientifically appropriate, specify the estimand, margins, uncertainty method, handling of paired reactors and multiplicity before examining comparative outcomes. If these prerequisites or statistical support are absent, issue a descriptive report and an insufficient-evidence decision rather than a pass/fail equivalence claim.

### Fair model comparisons

Retain the original experiment-group evaluation and sensor-only primary inference contract. Mechanistic and hybrid models shall use the same eligible groups, observed targets and available-at-cutoff information as the comparison they claim to beat. Any lab-assisted initialization or additional input must be disclosed and evaluated as a separate information scenario.

Fit parameters, preprocessing, feature selection and uncertainty calibration on development groups only. Report macro experiment-level error, per-experiment failures, unsupported predictions and coverage. Failure to beat the baseline is an acceptable research outcome. Eligibility failure is not a numerical performance result and must not be presented as one.

<!-- page -->
## 4 Reusable components and simulation behavior

### Component assembly

A consumer supplies a unit-operation identifier, model/version, initial state, process-input schedule, parameter-set version, requested output times and solver settings. The component returns state trajectories, units, validity/applicability status, optional qualified uncertainty, numerical diagnostics and complete lineage. It shall have no dependency on the dashboard and shall not require the consumer to copy or edit scientific equations.

Registry entries shall distinguish statistical, mechanistic and hybrid families and their evidence tiers: synthetic verified, data calibrated, group evaluated, or unsupported. Approved-for-research parameter sets identify the reviewer, purpose and limits; approval never implies manufacturing validation. Changed equations, parameters, inputs or feature policies invalidate dependent cached results.

### Scenarios and optimization

Sensitivity analysis, parameter sweeps and optimization are distinct activities. Sensitivity describes response to specified perturbations; sweeps evaluate declared cases; optimization searches for a solution to a fixed objective under constraints. Each records the model, objective and unit, decision variables and units, operating domain, conservation/positivity rules, solver tolerances, compute budget, seed and uncertainty assumptions.

Only parameters or inputs with a documented scientific interpretation may be varied. Data-supported ranges require source and reviewer records. Synthetic ranges must be labeled as assumptions and cannot be mixed with data-backed results. Reject infeasible schedules, unsupported units, negative biological states beyond declared numerical tolerances and out-of-domain requests before presenting a candidate optimum.

An optimizer shall return feasible, infeasible, unsupported, numerical_failure or budget_exhausted status. An unconverged or infeasible point is not a recommendation. Confirm a candidate with tighter numerical tolerances and sensitivity checks, report boundary solutions, and retain failed runs. An optimum is model-conditional and hypothetical until supported by appropriate experiments. No process settings are applied to a reactor.

### Scientist workflow

The read-only review interface may compare precomputed scenarios with measured trajectories. It shall display model family, evidence tier, parameter version, assumptions, unsupported regions and uncertainty status. Scenario computation is an explicit local CLI action; dashboard startup shall not fit, optimize or write source/model artifacts. Integration is demonstrated by a local consumer, not a production endpoint or live control link.

<!-- page -->
## 5 Data extensions and integration boundaries

### PAT and multimodal inputs

Represent inline, at-line and offline modalities explicitly. Record acquisition/collection time, result availability time, sampling location, instrument/source, unit-operation ID and provenance. Unknown availability is not silently equal to acquisition; the inference contract must state and review any assumption. PAT is a process-measurement framework, not a synonym for Raman spectroscopy. [S10]

An optional spectroscopy package needs measured spectra, axis and intensity units, instrument/calibration metadata, sample-to-reference linkage, batch/group identity and timestamps. PCA/PLS preprocessing, component selection and reference matching must be fitted or selected inside development folds. Do not join a separate Raman dataset to the CHO experiments or imply they share samples.

The current dataset does not establish Raman or chromatography coverage. A generic spectroscopy interface is engineering evidence; scientific Raman modeling requires Raman spectra and suitable references. A chromatography extension needs its own unit operation, settings, materials, chromatograms/analytical outputs and evaluation design.

### Scale translation

The current laboratory data do not establish cross-scale validation. A feasibility report shall assess whether meaningful scale contrasts, reactor geometry, agitation/aeration, mixing, oxygen-transfer information, shear proxies and comparable biological observations exist. Do not derive kLa, power per volume or mixing time from working volume alone. Distinguish directly measured engineering quantities from inferred ones and document uncertainty.

If suitable cross-scale data are absent, deliver a gap report and proposed acquisition/design plan. A synthetic scale exercise may demonstrate a contract but shall not support a scale-up or scale-down performance claim.

### Integration outputs

Predictions and simulations shall use versioned JSON metadata and typed Parquet tables with declared units, source IDs, model/parameter versions, time semantics, status, uncertainty and applicability. Unsupported results contain null numeric predictions and reason codes. A model-derived trajectory must never be serialized as a measured assay.

Integration acceptance requires a separate consumer that validates and reads the outputs without importing private model internals. Corrupt hashes, incompatible schema versions, missing units and unknown parameter versions must fail visibly. The initial demonstration is entirely local; OPC UA, industrial middleware, live synchronization and control are outside this release.

<!-- page -->
## 6 Delivery gates effort and open decisions

Track A retains G0 through G9, M1 through M5 and the original 50-80 focused-hour planning range; none is retrospectively marked complete by the EDA. Track B is a separately reviewable outcome, not a reason to delay or weaken Track A's validation.

| Added gate | Pass evidence | Failure outcome |
| --- | --- | --- |
| CG1 Data and characterization | Raw missingness preserved, quality/time policy reviewed, DT-06 report accepted | Repair data contract; no modeling acceptance |
| CG2 Component eligibility | Unit-operation contract, equations/states/units, G7 outcome and intended-use tier | Synthetic-only component or documented no-go for data-backed simulation |
| CG3 Numerical and integration | Solver verification, registry, schemas, lineage and independent consumer tests | Component release blocked |
| CG4 Research comparison and scenarios | Fair comparisons where eligible; bounded scenarios and optimization evidence or justified deferral | Report negative/ineligible outcomes; no optimization claim |
| CG5 Component research release | DT-01/02/03/04/06 accounted for, B1 dispositions, extension gap reports and reproducible evidence | Keep under development; do not present as completed component package |

### Sequence and estimates

Complete raw-aware ingestion and target review, then Track A leakage controls and baseline evaluation. Define Track B contracts alongside this work; calibrate and compare models only after their scientific gates. Prioritize the bioreactor component, integration contract, registry/consumer and characterization before extra modalities.

Retain the original additional 18-35 hour mechanistic/hybrid estimate if eligible. Provisionally budget another 25-45 focused hours for component interfaces, integration/registry, characterization and scenario demonstration beyond that original plan. These are unvalidated planning ranges, not deadlines. Re-estimate after architecture and data review; avoid double-counting shared work. Genuine cross-scale, Raman or chromatography studies require separate data and estimates.

### Added risks and decisions

Record confounding and small-group uncertainty; failed identifiability; optimizer exploitation of model error; unsupported scale inference; incompatible downstream schemas; stale parameter sets; and synthetic/data-backed evidence mixing. Mitigate through explicit domains, immutable lineage, negative results, numerical checks and claim review.

Owner decisions still required: target approval; meaningful error tolerance; component state/parameter scope; scenario objective and bounds; comparison attributes/margins; scientific reviewer and approval records; availability-time assumptions; and whether new datasets justify an extension. The supplied role comparison motivates scope, but no independent current J&J job-description verification is claimed.

<!-- page -->
## 7 Sources change summary and retained baseline

### Change summary

This edition adds ten stable DT requirements, a second release track, five component gates, process characterization and comparability protocols, bounded optimization, multimodal/scale feasibility outcomes, integration acceptance and current EDA limitations. It preserves all baseline FR/NFR IDs and does not change research-only, no-cloud-cost, naming or redistribution boundaries.

### Added source register

S9. Satwekar et al. Operationalizing Digital Twins in Biomanufacturing through Interoperable Process Analytical Technology. NIST publication record, July 16, 2026; DOI 10.1007/s00449-026-03369-9. Used for architectural context concerning models, PAT and interoperability, not to claim this project implements that architecture or satisfies a standard.

https://www.nist.gov/publications/operationalizing-digital-twins-biomanufacturing-through-interoperable-process

S10. FDA. PAT A Framework for Innovative Pharmaceutical Development Manufacturing and Quality Assurance. October 2004. Used for measurement-framework context; no regulatory compliance or validation claim.

https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pat-framework-innovative-pharmaceutical-development-manufacturing-and-quality-assurance

S11. FDA/ICH. Q5E Comparability of Biotechnological Biological Products Subject to Changes in Their Manufacturing Process. June 2005. Used to distinguish product comparability from exploratory run comparisons.

https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q5e-comparability-biotechnologicalbiological-products-subject-changes-their-manufacturing-process

E1. BioSynvia EDA run of November 5, 2026. Project evidence: reports/eda-v2/report.md, summary.json, source_manifest.json and raw_aligned_assay_comparison.csv. Code: scripts/eda.py. These support descriptive dataset findings only; raw inline status streams were not exhaustively audited.

U1. Owner-supplied capability gap assessment beginning Partially but not to the depth. Used as the requested scope-change brief. External factual claims were separated from proposed requirements; the cited primary source records were checked November 5, 2026.

### Part B retained PRD v1.1

The following 22 pages reproduce the complete baseline unchanged. Apply Part A's precedence table when a baseline scope/status statement differs. Retained baseline source/trademark discussions describe their original review date and do not constitute a refreshed legal opinion. The new edition does not grant public branding or raw-data redistribution permission.

End of controlling revision. Retained baseline follows.
