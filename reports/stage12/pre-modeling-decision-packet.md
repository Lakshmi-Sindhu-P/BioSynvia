# Stage 1/2 pre-modeling decision packet

## Subsequent scientific-evidence checkpoint — 2026-11-05

The owner accepted this release as an **engineering checkpoint only**. The current
[scientific approval packet](../scientific-closure/approval-packet.md) supersedes
this historical packet's unresolved-source statements where the full preprint now
provides evidence: assay methods, named media, calibration procedure, alignment,
forward-filled process states, below-limit concentration blanks and EXP011 context.
All new cohort/feature/split choices remain proposals. The frozen v6 data, original
split and fitting gates remain unchanged; fitting is still paused.

**Decision requested:** review the proposed target, input and split policies after the scientific questions below are answered. VCD is recommended as a candidate for retrospective research, but no primary label mask, feature family, freshness threshold or split is approved. Assay validity is unknown. Owner and scientific approvals are separate; model fitting is not permitted. No model has been fitted and no performance has been computed.

The final artifact is [v6](../../data/processed/v6/stage12_manifest.json), manifest SHA-256 `d74465cbb353af872681cf3c6bbd1055ee0523441a889ec90832d7fc3affa45e`. V6 adds executable source-schema assertions and a source-schema inventory; it does not change source values, target proposals or fitting status. Preserve v3–v5, the hashed pre-execution specification and incomplete/failed versions as historical evidence; v5 remains the source-exact reconstruction that corrected v4 numeric precision.

## Interpretation correction addendum and source authority

The dated [interpretation correction matrix](interpretation-correction-matrix.md)
records all 12 handoff interpretation corrections and 17 required audit changes,
distinguishing wording errors from confirmed code defects. The current audit found
no R01/R02 mixing: a new test proves that every lineage row matches its assay's
`experiment_id`, `reactor_id`, and `run_id`. Time alone is never a sufficient join
key. Inline and offline tables remain distinct until a controlled same-`run_id`,
past-only assay snapshot is explicitly built.

| Source | Authority and allowed role | Not authoritative for |
| --- | --- | --- |
| Original Excel workbooks | Original offline observed/null status, source cells, timestamps, supplied Status fields, duplicates and raw-stream coverage | Publisher synchronization algorithm or result availability time |
| Publisher aligned CSVs | EDA/preparation convenience tables, 48-file coverage and candidate aligned features pending causality review | Replacing original blank cells, raw Status, source-cell lineage, or proving past-only causality |

The executable [schema inventory](../../data/processed/v6/source_schema_inventory.csv)
requires exactly 12 workbooks with the named 16-sheet R01/R02 structure and 48
aligned CSVs: 24 inline files with exactly 41 columns and 24 offline files with
exactly 17. The offline schema contains cell and medium variables—glucose, lactate,
ammonium and osmolality—but no amino-acid profiles. Medium formulation is unknown;
these measurements do not identify a recipe or prove a waste mechanism.

```text
Raw publisher layer: 12 Excel workbooks + 48 aligned CSVs
        | (identified records; original Excel authoritative for assay/null/status)
Canonical audit layer: separate inline lineage and offline assay tables
        | (only controlled same-run, past-only selection after approval)
Modeling snapshot layer: one assay row with eligible same-run features
```

Raw coverage and aligned-export coverage remain separate in
[time policy](../../data/processed/v6/time_policy.csv). The 214 original medium
blanks remain null even where aligned convenience data show zeros; numeric zero is
not missingness. The six original VCD zeros remain recorded values with unresolved
scientific meaning. Missing Status is distinct from a blank Status cell, warning,
null measurement and invalid measurement. The five- and eight-feature cases are
separate feasibility policies; zero strict-eight support is not scientific
invalidity of pH, dissolved oxygen or temperature.

The owner has also enabled the globally available [EGM workflow reference](../../docs/egm-reference.md);
that installation does not retrospectively certify this packet's engineering or
scientific conclusions. This correction work used the ordinary 5.6-class
coding/review role at ordinary reasoning. No 6/6.1 escalation had a concrete
high-impact justification.

The bounded [offline unique-values report](../offline-unique-values/report.md) and
[reproduction script](../../scripts/profile_offline_unique_values.py) enumerate all
16 cell/medium assay fields from frozen source-exact v5 evidence. It reports
glucose/lactate/ammonium/osmolality values and missingness without inferring a
medium recipe, feed composition, assay SOP or biological waste mechanism. A linked
author preprint abstract says medium and initial glutamine varied, but does not map
experiments to formulations and is not peer reviewed; formulation remains unknown.

## Target and assay evidence

Proposed target: recorded **VCD Mean (cells/mL)** at the original offline assay acquisition time, not a validated biological truth. The unit is taken from the header and unverified; SOP, replicates, detection/reporting limits, rounding and QC are unknown for all 378 assays. The proposed recorded-nonnegative mask includes 378; positive-only includes 372 and changes the estimand. Neither is selected as primary. All offline assays and SEMs are forbidden predictors. See [target contract](../../configs/target_decision.json) and [source cells](../../data/processed/v6/assay_source_cells.csv).

| Numeric zero | Original worksheet cell | Assay time (h) |
| --- | --- | ---: |
| EXP002 R02 | R02_offline_CellAnalysis!B16 | 209.5 |
| EXP011 R02 | R02_offline_CellAnalysis!B14 | 148.5 |
| EXP011 R02 | R02_offline_CellAnalysis!B15 | 162.5 |
| EXP011 R02 | R02_offline_CellAnalysis!B16 | 171 |
| EXP011 R02 | R02_offline_CellAnalysis!B17 | 186 |
| EXP011 R02 | R02_offline_CellAnalysis!B18 | 195 |

These are numeric source zeros, each with positive TCD, zero VCD SEM and zero viability. Their meaning is unresolved: neither actual absence nor censoring nor zero uncertainty can be inferred. Separately, 214 original medium cells are blank and retained as null: 135 glucose, 51 lactate and 28 ammonium. They are not target zeros.

## Inputs, support and timing

All 40 candidate sensor fields are unapproved; the categories below describe eligibility proposals, not scientific endorsement. All units and calibration are unverified header information; frequency qualifiers identify channels, not verified physical interpretation. Full run-level detail is in [feature eligibility](../../data/processed/v6/feature_eligibility.csv).

- **Five-core feasibility proposal (5):** Dissolved CO2 (%-sat); Transmission and Reflection (arb. Unit); Conductivity (mS/cm); Permittivity (pF/cm).
- **Semantic review required (22):** fc (kHz), DeltaEps (pF/cm), Alpha, Fitting Quality (Cole fit R2), Fitting Error (Cole fit RMSE), and C at 300, 374, 466, 580, 720, 896, 1118, 1392, 1729, 2155, 2689, 3347, 4158, 5188, 6447, 8030 and 9995 kHz. Fitted and frequency channels require interpretation before use.
- **Blocked under strict status due to unknown status (13):** pH; Dissolved O2 (% air sat); Temperature (°C); Agitation rate (rpm); Aeration rate total (sL/h); O2 fraction inlet (%); CO2 fraction inlet (%); Aeration rate air, O2 and CO2 (sL/h); Liquid volume (L); Cumulative NaOH weight (g); Cumulative feed weight (g).

The original eight-core adds pH, dissolved O2 and temperature to the five. Strict status requires a supplied, nonblank, exact `Ok`; an absent Status column differs from a supplied blank, and warnings/non-Ok are separate evidence. Among 15,120 lineage rows, 4,914 have Status column absent, 50 blank and 504 non-Ok; flags can overlap. `Ok` does not establish assay or instrument validity. At five minutes the prior assumed-status eight-core count is 339, but strict-status eight-core support is zero at every threshold.

| Maximum age | Five-core supported / all 378 | Joint with positive mask / 372 | Joint with nonnegative mask / 378 | Strict eight-core | Strict known availability |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 min | 335 | 330 | 335 | 0 | 0 |
| 5 min | 339 | 333 | 339 | 0 | 0 |
| 15 min | 341 | 335 | 341 | 0 | 0 |

Counts use strict status with the retrospective assumption that acquisition equals availability; see [sample effects](../../data/processed/v6/sample_effects.csv) and [group coverage](../../data/processed/v6/group_coverage.csv) for group denominators and scenarios. Actual sensor and assay result availability, clock origin and synchronization are unknown. Strict known-availability support is zero, so error under that scenario is undefined. A same-reactor acquisition at or before the assay cutoff is used, including ties within `1e-10` hour; tie ordering is unknown. The raw-to-aligned offset and transformation are not established.

EXP004 has 1,680 preserved collision rows across eight streams; none is selected at an assay cutoff. Ambiguous duplicate timestamps are rejected, not silently resolved. EXP011 R02 feed logging ends at 67.13944 h while other sensor streams continue near 195 h; this does not establish feeding or process cessation. See [quality policy](../../configs/data_quality_policy.json) and [time policy](../../data/processed/v6/time_policy.csv).

## Proposed split and evaluation

Hold out whole paired-reactor experiments **EXP004 (batch)** and **EXP010 (fed-batch)**. The target-blind rule maximizes the minimum reactor fraction of all original assay cutoffs with five-core strict-status, assumed-acquisition support at five minutes: EXP004 ranks 15/16, tied with EXP008 and chosen lexicographically; EXP010 ranks 22/23. The denominator does not depend on target values. The same IDs apply across sensitivities. Ten development experiments are EXP001, EXP002, EXP003, EXP005, EXP006, EXP007, EXP008, EXP009, EXP011 and EXP012. Reactors remain nested within their experiment; ten outer leave-one-experiment-out folds and inner grouped folds preserve this boundary. See [split protocol](../../configs/split_protocol.json) and [manifest](../../data/processed/v6/split_manifest.json).

All-group target EDA preceded this reservation; the selection favors well-supported inputs, and one test experiment per mode cannot measure within-mode generalization variance. This is a prospectively reserved **internal** evaluation after exploration, not untouched external validation.

After approval, the proposed primary ranking is equal-weight mean of experiment MAE in cells/mL, pooling scored assays from both reactors within each experiment and also reporting each reactor. All fitted preprocessing, imputation, scaling, feature/window/freshness choices and tuning must occur in grouped inner folds of each outer training partition. Select and freeze using development only, refit on all development groups, then score the two reserved groups once without retuning. Compare on matched support and report intended, target-mask, supported, scored, abstained and failed counts; no prediction or error is invented for unsupported inputs. Secondary metrics and bounded model candidates are in the [benchmark protocol](../../configs/benchmark_protocol.json).

## Gates and questions

**Scientific evidence needed:** What are the assay SOP, replicates, detection/reporting limits, rounding and QC, especially for the six zeros? What are the true result-availability times, clock origins and ordering? What do `Ok`, warning and absent/blank status mean for each instrument? What do each field, unit, calibration and frequency/fitting channel mean? Why did EXP011 R02 feed logging end, and how were aligned exports produced? How should EXP004 collisions be resolved? Exact retrieval event and reuse rights also remain unknown; local research only is recorded pending clarification. See [issue register](../../configs/issue_register.json).

**Owner protocol decisions:** after the scientific evidence is assessed, select a target mask and estimand, feature/status/availability and freshness policies, split and evaluation protocol; decide any acceptance threshold separately. Owner approval cannot substitute for assay validation. Target, features, split and fitting flags remain false. G1/G2/G3, M1/M2, CG1 and component release remain open; rolling features, model selection/evaluation and full characterization are deferred. The bounded requirement mapping is in [requirements status](../../docs/requirements-status.md).

## Review and verification record

Five pre-implementation lenses—science, quality, leakage, provenance and requirements—raised 28 findings, recorded in the [resolution register](resolution_register.json). Five post-implementation lenses reviewed the resulting scope: [science](reviews/post_science.md), [quality](reviews/post_quality.md), [leakage](reviews/post_leakage.md), [provenance](reviews/post_provenance.md) and [requirements](reviews/post_requirements.md). The science/quality precision finding affecting 701 v4 numeric pairs was corrected in v5; the post-requirements v4 reference finding is addressed above. Engineering review agreement is not independent scientific sign-off.

[Verification](verification.json) records the original v5 checks. The new [handoff correction verification](handoff-correction-verification.json) records 38 passing tests, v6 CSV/SQLite logical agreement, unchanged matching source and backup, exact source numeric/null preservation across 6,804 source cells (6,590 numeric and 214 blank), the 60-row exact schema inventory and no-cross-run lineage proof. Synthetic repeat builds exercise stable payloads, but a full-data byte-repeat build was not rerun. These checks establish bounded engineering evidence, not assay validity, deployment readiness or model performance.

## Final correction verification and remaining engineering work — 2026-11-05

The [manifest-bound released-bundle verification](released-isolation-verification.json)
now confirms all 15,120 lineage rows match 378 unique assay parents on experiment,
reactor and run. Five supplemental regression tests pass, including deliberate
crossings and offline-predictor rejection. This closes the fresh packet review's
isolation-test finding. The prior full suite passed 38/38; the updated focused
Stage12 suite passed 12/12. These are separate runs.

Both fresh reviews and every disposition are retained in the
[resolution register](resolution_register.json) and
[final drift addendum](final-spec-drift-check.md). Three engineering topics are
deferred: a fully unmocked synthetic end-to-end schema fixture; pandas null-
comparison normalization (current pinned comparisons pass with FutureWarnings);
and stricter per-family raw-header rejection contracts for future source changes.
They are not evidence of current reactor mixing or source corruption. The
five-hour usage guard prevented broader follow-up; no reset was consumed.

All assay, instrument, formulation, timing, alignment, collision, provenance and
reuse questions remain open. No model or digital twin has been fitted or validated.
**Model fitting remains paused until the owner reviews and approves this packet.**
