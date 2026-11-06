# Stages 1 and 2 executable specification

Revision 2, 2026-11-05. Execution authorized by the owner; supersedes the plan's
awaiting-approval status for Stages 1 and 2 only. Controlling sources are PRD v1.2
and SRD v0.2 including their retained baseline PDFs/text. No model fitting.

## Scope and evidence

Preserve source ZIP and verified backup, all original values and v3 artifacts.
Produce versioned v4 protocol artifacts from v3 and raw workbook evidence. v3 is
an inspection dataset, not an approved training set. Reconcile 378 observed VCD
means, six numeric zeros, 214 original medium blanks, 40 sensor candidates, 12
paired experiment groups and 24 reactors. SEMs are uncertainty summaries, not
independent samples. Agent reviews check reasoning/code, not assay validity.

Implement a small explicit protocol module and CLI, JSON contracts under configs,
and versioned CSV/SQLite plus manifest under data/processed/v4. Do not rerun broad
EDA or install dependencies. Preserve incomplete output on failure and promote
only after internal validation. Every artifact hash, producer/config/source hash,
environment and command must resolve. Verify original and backup before/after.

## Stage 1 deliverables

1. target_decision: recommend VCD for retrospective sensor-based research;
   all scientific approval flags false. Preserve six zeros as recorded observed
   values pending assay interpretation. Propose separately reported positive-only
   and recorded-zero-inclusive sensitivities; neither is approved primary analysis.
2. inference_contract: one prediction at actual assay acquisition cutoff using
   same-reactor past raw sensor observations only. Acquisition is not known result
   availability. Provide assumed-acquisition retrospective scenario and strict
   availability scenario (unknown availability blocked); no deployment claim.
3. quality_policy: retain raw Status; unknown/Warning excluded from proposed
   inputs; absent Status explicitly unknown, never implicitly Ok. Keep invalid,
   stale, duplicate, and past-only inactive-derived-zero flags independently.
   Five minutes is a provisional engineering scenario, not scientific approval.
   Summarize actual per-stream positive cadence and 1/5/15-minute coverage effects,
   using only metadata/values needed for quality, never target correlation.
4. feature_eligibility: all 40 field IDs, header quantity/unit separately from
   frequency qualifiers, source modality/status/provenance, unresolved semantics,
   default family and eligibility reason. No verified units invented. Mode/time/
   IDs context only; all offline assays and their SEMs forbidden inputs.
5. issue register: zeros, blank-to-zero aligned artifacts, EXP004 duplicates,
   EXP011 feed/aligned cutoff, fitted-zero channels, unknown availability, units,
   status and source rights/retrieval limitations. Preserve negative findings.

## Stage 2 deliverables

1. v4 assay_decisions retains every assay, original source coordinates and values,
   proposed positive/nonnegative masks, quality/feature completeness and separate
   scientific approval false. No invented target. Per-feature lineage references
   v3 and adds acquisition/availability fields, independent quality flags and source
   cell coordinates; preserve competing duplicate candidates. Store source and
   sheet-level dictionary evidence and offline field metadata as well.
2. deterministic split proposal uses experiment ID/mode and input coverage only,
   never VCD values or model scores. Prefer two final-test groups: one batch and
   one fed-batch. Choose highest minimum reactor five-status-bearing-core coverage within each mode,
   tie lexicographic ID; disclose this favors supported-input evaluation. All
   remaining groups form leave-one-experiment-out development folds. Guard paired
   reactors, duplicate IDs, disjointness and at least two development groups.
   Prior all-group EDA is disclosed: final test is reserved prospectively now,
   not an untouched external validation. Split/protocol approvals remain false.
3. benchmark protocol defines training-only median baseline, bounded transparent
   sensor baseline/Ridge/PLS and one limited nonlinear comparator for later stages;
   no fitting now. Imputation/scaling/PCA/components/feature/window selection and
   tuning remain inside development training groups, with inner grouped folds if
   tuned. Compare families on matched target masks, split IDs and input scenarios;
   report availability/abstention and common-support plus intended-population views.
   Primary metrics proposed MAE/RMSE/bias per reactor/experiment and equal-weight
   experiment macro summaries in cells/mL; mode summaries descriptive. Uncertainty
   resamples experiment groups, with small-N limitations. No acceptance threshold
   or biological equivalence claim invented. Freeze before final holdout evaluation.
4. verification: meaningful tests for point-in-time availability, future mutation,
   independent quality flags, duplicate/zero/null preservation, split invariants,
   target-blind split stability, tamper detection and incomplete-run protection.
   No training imports/calls or trained outputs. Record test commands/results.

## Reviews, output and gates

Before implementation use five separate fresh-context Goldfish reviews: scientific
validity (Astra high), data quality (Sol high), temporal/group leakage (Sol high),
reproducibility/provenance (Sol medium), PRD/SRD scope (Sol medium). Save each review.
After implementation new fresh-context reviewers verify code, data, lineage,
tests, reports and spec compliance. Save all findings and accepted/rejected/
deferred/unresolved/requiring-owner-input dispositions with reasons/evidence.
Implement accepted engineering corrections; scientific unknowns remain questions.
Use bounded Luna extraction and Terra packet reporting. Native agents substitute
for unavailable EGM plugin; do not create user-visible chats. Record assignments,
fallbacks and usage telemetry (user baseline weekly83% remaining; latest measured
weekly17% used at2026-11-05T21:23:19Z; measurement may lag). Preserve >=60% remaining.

Return one consolidated pre-modeling decision packet with recommendation, six
zeros, sensor quality/availability, feature eligibility, sample effects, exact
proposed split IDs, evaluation protocol, open scientific questions, review
resolutions and verification. Stop before model fitting. Owner protocol approval
and independent scientific evidence are distinct gates; neither is fabricated.

## Revision 2 pre-review correction

Data-quality and leakage reviews identified that absent Status on process
parameters makes strict eight-core coverage zero. Preserve this negative finding.
Report eight-core under the old assumed-status policy separately from strict
eight-core and a five-status-bearing-core feasibility scenario (CO2, transmission,
reflection, conductivity, permittivity). Use only the latter explicitly named
scenario for metadata-only split ranking. This is not an approved feature redesign.
Distinguish absent Status column, blank supplied Status and warning text. No
strict known-availability scenario can support predictions while availability
is unknown; its error metrics are undefined. Define signed bias as prediction
minus observed VCD; pool assays within each experiment, weight experiments equally,
and also report reactor metrics. Do not bootstrap two final groups into an
inferential final-test interval. Record review input spec revision/hash.
