# Proposed autonomous work plan

Status: owner authorized autonomous execution of Stages 1 and 2 on November 5, 2026.
Those engineering stages are complete; the consolidated review packet is
`reports/stage12/pre-modeling-decision-packet.md`. Stages 3–6 remain separately gated.
Authority: PRD v1.2 and SRD v0.2. Engineering method: karpathy-guidelines.
This proposal does not itself approve a target, scientific quality policy or model run.

## Objective and immediate next step

Build a reproducible offline CHO modeling workbench, followed by the separately
gated research component track. The immediate next milestone is a documented
data and evaluation protocol that makes subsequent model experiments reproducible.

The saved v3 data are inspection candidates: 378 assay rows, 40 raw-derived input
candidates and a provisional 333-row/eight-input subset. The five-minute sensor-age
setting, feature subset, assay interpretation and units are not final scientific
decisions. No trained model or approved group split exists.

## Stage 1 Close the data and target decision packet

Actions:

- Reconcile current reports and requirement status with the implemented pipeline.
- Complete a source-to-field dictionary with units, sensor/status meaning,
  acquisition/availability semantics and unresolved evidence gaps.
- Investigate duplicate EXP004 timestamps, inactive/zero channels, the six recorded
  VCD zeros and EXP011's feed/aligned cutoff. Preserve all source evidence.
- Use actual sampling/cadence/coverage to justify proposed freshness and quality
  rules. Do not tune quality rules to obtain attractive target correlations.
- Propose VCD as the research target, the sensor-only inference task, allowed
  inputs, inclusion/exclusion reasons and the intended interpretation of errors.
- If source documentation cannot settle an issue, record the uncertainty and
  formulate precise author/scientific-review questions. Do not contact others
  without the owner's explicit instruction.

Deliverables: target_decision draft, inference_contract, data_quality_policy draft,
feature_eligibility table, issue register and concise decision report.

Pass evidence: every proposed rule has a reason and source or an explicitly stated
assumption; original nulls and numeric zeros remain distinct; counts reconcile;
unresolved issues cannot silently become accepted labels or inputs.

## Stage 2 Prepare reproducible data and the evaluation design

Actions:

- Preserve original and backup hashes. Work on copies and save new versioned
  inspection outputs rather than overwrite previous artifacts.
- Apply proposed deterministic type/unit/quality rules with original values,
  transformation logs and per-row inclusion/exclusion reasons retained.
- Test past-only snapshot construction, availability/freshness, duplicate handling
  and input/source lineage. Treat the current acquisition-time assumption explicitly.
- Draft experiment-group partitions and development folds. Both reactors from an
  experiment stay together. Prefer the PRD's two-group final holdout if coverage
  and mode composition support it; otherwise document the grouped alternative.
- Choose group IDs using design/coverage criteria before any model performance
  comparison. Disclose prior descriptive access to all experiments.
- Define candidate feature families and a small bounded comparison protocol.
  Correlation/plots inform questions; model-driven feature selection, lag/window
  selection, imputation, scaling and PCA/PLS belong inside training folds.

Deliverables: versioned prepared CSV/SQLite tables, manifests, test evidence,
proposed split manifest, feature protocol and benchmark protocol.

Pass evidence: original data unchanged, no paired-group overlap, no future inputs,
no invented assay targets, source and artifact hashes resolve, and no incomplete
run is promoted to an accepted dataset.

### Decision checkpoint before model fitting

Return one consolidated review packet covering the target, uncertain labels,
quality/availability rules, feature information contract, split IDs and evaluation
protocol. Owner approval authorizes the research protocol; it does not establish
assay validity or manufacture scientific-review evidence. If a question requires
an independent scientific reviewer or author clarification, state that explicitly.

Unknown assay-zero semantics must not be silently settled by deletion or by
accepting zeros as ordinary labels. A proposed include-versus-withhold sensitivity
analysis may be part of the reviewed protocol. It is not automatically the primary
scientific analysis. Until the target/protocol approval gate is satisfied, continue
unaffected engineering and documentation but do not claim an approved training set.

## Stage 3 Establish the statistical model bench

After the protocol checkpoint passes:

- Implement the training-only median baseline, a transparent sensor baseline,
  Ridge/PLS where appropriate and one limited nonlinear comparator.
- Use approved grouped development folds and pipelines. Keep searches bounded
  and document the parameter grid, seeds, inputs and preprocessing.
- Compare input families, plausible past-only windows and missing-sensor behavior
  within development folds. Do not add complex models merely for breadth.
- Save predictions, configurations, feature/target/split references, per-experiment
  MAE/RMSE/bias, prediction coverage, failure records and uncertainty limitations.

Pass evidence: leakage tests pass, every score resolves to actual observed targets
and frozen group assignments, and worse-than-baseline or unsupported outcomes are
retained. No accuracy threshold is invented after seeing the results.

## Stage 4 Freeze and evaluate

Freeze the chosen model/protocol using development evidence. Evaluate the reserved
experiments according to the approved protocol; preserve the first evaluation and
any later rerun/change records. Do not retune using final-test results.

Deliverables: frozen run, per-experiment and mode-specific report, failure analysis,
approved sensitivity analyses, missing-sensor checks, model card and reproduction
evidence. Negative results are acceptable research conclusions.

Pass evidence: independent code/data references reproduce the result within
declared numerical tolerances. Report small-group and prior-EDA-access limitations.
Improved scores are not necessary to pass honest research reporting.

## Stage 5 Build the read-only review workbench

Build the local dashboard around saved accepted artifacts. Show measured versus
predicted values, missing/unsupported periods, experiment comparisons, input/model
versions, data provenance and limitations. No training or source mutation occurs
on dashboard startup. Verify read-only behavior and reviewer usability.

Deliverables: local app, concise technical narrative and complete Track A evidence
package. No publishing or live process connection is implied.

## Stage 6 Develop the separate modeling component track

Implement versioned unit-operation/model contracts, parameter/registry metadata,
simulation outputs and an independent local consumer. Carry characterization and
comparability evidence forward from Track A.

Perform G7 mechanistic eligibility review before data-backed ODE calibration or
hybrid claims. If it fails, keep a clearly labeled synthetic numerical component
demonstration separate from real-data model evaluation. Bounded scenarios and
optimization require a reviewed objective, units, domain and constraints.

Cross-scale, Raman and chromatography extensions require separate suitable data
and scope decisions. A gap report is an honest feasibility result, not validation.
Pass evidence: applicable DT requirements, numerical tests, lineage/schema tests,
consumer compatibility and approved research-use boundaries.

## Project structure

Use existing folders; add modules only when a stage requires them.

```text
BioSynvia/
  biosynvia/       reusable data, validation and later modeling functions
  scripts/         reproducible commands that call those functions
  configs/         reviewed target, quality, feature and split protocols
  tests/           source integrity, temporal/group safety and model checks
  data/
    raw/           preserved publisher archive
    backups/       verified separate source copy
    processed/     versioned tables, lineage, database and manifests
  runs/            immutable model-run evidence after modeling is authorized
  reports/         EDA, scientific results and ongoing implementation report
  docs/            requirements, decisions and methodology
  app/             later read-only review interface
```

Keep pandas/SQLite and small explicit modules for current local preparation.
Do not introduce workflow frameworks, distributed services or extra infrastructure
without a demonstrated need and an explanation of the tradeoff.

## Autonomy boundaries

After this plan is approved, routine work within the authorized stage can proceed
without repeated permission: inspect local/public sources, write small code changes,
add meaningful tests, generate local figures, run local checks, create versioned
derived artifacts and keep reports current. Use the Karpathy guidelines throughout.

Bring back substantive scientific decisions at the consolidated protocol checkpoint,
contradictory requirements, data gaps that prevent the next gate, and requests to
expand data/model scope or change the meaning of a claimed result. Do not repeatedly
ask about routine implementation details that fit the agreed contract.

Existing owner-approval boundaries remain for external messaging, paid/cloud work,
publishing/sharing, new private data transmission, destructive changes to originals
and live process access. Do not infer authorization for those from local build approval.

No requirement can be marked complete just because software runs. Do not invent
assay meaning, units, reviewer approval, model performance, uncertainty or evidence.
Unresolved cases stay explicit; continue work that does not depend on them.

## Reporting and verification cadence

Before a bounded task, state the deliverable and how success will be checked.
During work, explain meaningful findings and changed assumptions. For each
completed increment, update the implementation report and decision/requirement
status with changes, commands, tests, artifacts, limits and the next step.

Run checks appropriate to the change; do not add redundant tests or rerun expensive
analyses without a reason. Preserve failed scientific and numerical outcomes.
At each stage boundary, return a compact evidence summary and unresolved decisions.

## Proposed approval scope

Approve this structure to authorize autonomous Stages 1 and 2 and their local
code/data/documentation work. The next return point is the single pre-modeling
decision packet. Stages 3 through 6 describe the agreed direction and become
executable only when their protocol and scientific eligibility gates are met.
This keeps routine work autonomous while making consequential research choices
reviewable before model fitting.
