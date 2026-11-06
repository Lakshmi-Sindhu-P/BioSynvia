# BioSynvia scientific-evidence approval packet — 2026-11-05

**Status:** Stages 1–2 accepted as an **engineering checkpoint only**. Fitting
remains paused. Agreed priorities: **current VCD estimation → forecasting →
exploratory optimization**, progressing toward a digital twin. The immediate
product is a reliable research soft sensor designed for possible real-time use.

## Confirmed facts

The complete [author preprint v1](https://www.preprints.org/manuscript/202611.0377)
was inspected in its browser viewer; ten manuscript-page screenshots are retained.
Original PDF export failed. No separate supplement was listed in the inspected
manuscript, landing page or [Zenodo inventory](https://zenodo.org/records/20829178);
this does not prove none exists. The preprint is not peer reviewed.

| Evidence | Scientific closure |
| --- | --- |
| Methods, printed pp. 4–5 | **Countstar BioTech**, trypan-blue/image analysis; technical triplicates averaged. Replicate count is described; the released SEM formula, numerical limits and case-specific QC remain unconfirmed. |
| Methods/Table 2, pp. 2–4 | **TC-42/TCX6D** media, experiment mapping and Basic Feed formulation are reported. Full basal recipes remain limited; Table 2 footnotes are now mapped. These facts come from the paper, not the medium-analysis columns. |
| Processing, p. 6 | Process variables were logged on change and forward-filled: row time does **not** prove fresh per-variable acquisition. Aligned CSVs use nearest neighbors within half a sampling interval and discard unmatched times; future-neighbor use is possible. Status was removed from aligned inline exports. |
| Validation, pp. 8–9 | EXP011 R02 was contaminated; antibiotics were added to both reactors, and R02 feed and oxygen enrichment were deliberately terminated around 67 h. Its five VCD zeros have context, but no individual explanation. EXP002 R02's zero remains separately unexplained. |
| Validation, pp. 8–9 | Calibration procedures are described, not per-row certification. Offline concentration blanks signify **below detection/quantification limits**, with numerical bounds absent. Preserve blanks; do not substitute measured zeros or assume random missingness. |
| Zenodo Description | Raw **0 h is inoculation**; availability, clock synchronization and ordering remain unverified. |

Detailed citations/provenance: [source register](source-evidence.md).

## Defensible inferences

The aligned cutoff is consistent with the all-stream matching rule and feed
termination; bit-exact reconstruction remains unverified. Feed was updated using
offline VCD/glucose information, so feed history may reveal assay-dependent actions:
withhold it until point-in-time availability is proven. Held process states need
separate age/heartbeat semantics.

[Published CHO studies](supporting-publications.md) demonstrate phase-dependent
dielectric relationships and turbidity contributions from nonviable populations.
These justify error checks, not universal monotonicity or adjudication of the six
zeros. Select the best reliable predictor on grouped validation; interpretability
helps investigate errors. Neither these papers nor agent agreement validates our
labels, predictions or eventual twin.

## Owner decisions requested

Counts are descriptive under v6's row-time convention, **not validated real-time
support**. No mask deletes original data. All defaults remain proposals.

| Decision | Recommended default | Alternatives | Sample-count impact | Modeling consequence |
| --- | --- | --- | --- | --- |
| **D1: uncertain zeros** | Separate six from primary fitting; retain individual challenge predictions and an include-zeros sensitivity. | Include provisionally; wait for author QC. Censoring requires an evidenced bound. | Zero-only mask: **372 positive records / 333 supported** at 5 min; including zeros **378/339**. | Restricted positive-label estimand. Challenge predictions must be experiment-held-out; zero-referenced errors are not confirmed biological errors. |
| **D2: contaminated cohort** | Quarantine **entire EXP011** from primary fitting because contamination and both-reactor antibiotic exposure confound interpretation; retain challenge/sensitivity analyses. | R02-only quarantine; retain all with context. | Joint with D1: **343 positive / 308 supported**; R02-only **360/322**; retain-all **372/333**. | Conservative research scope, not proof every EXP011 label is invalid. Five overlapping zeros are not subtracted twice. Separate oxygen-supply interruptions remain stress cases; EXP011 is a deliberate oxygen-enrichment termination. |
| **D3: inputs/quality** | Compare five sensors with eight adding pH/O2/temperature as **publisher-held states of unknown quality**; optionally compare pre-known medium/mode context inside inner folds. | Strict `Ok` for all eight; five only; expanded channels after QC/count review. | Joint cohort: five/eight **308**; strict eight **0**. Expanded-channel effects uncomputed. | Preserve unknown/blank/warning states. No offline assay/SEM/identity predictors. Warning codes do not universally prove sensor failure. |
| **D4: source/timing** | Raw past-only research snapshots; declare acquisition-as-availability assumption. Withhold aligned values and assay-updated feed. | Strict evidenced availability; later validate reconstructed aligned exports. | Joint cohort **308 retrospective**, strict known availability **0**. | No real-time/intervention claim; original assay cells authoritative; no target interpolation or filling long sensor gaps. |
| **D5: freshness** | Freeze 5 min for sampled core sensors; 1/15 min sensitivities. Separate policy for held process states. | Freeze 1 or 15 min. | Joint cohort **305/308/310** supported positives at 1/5/15 min. | Report error and abstention together. Counts do not validate process-state freshness or unknown latency. |
| **D6: split** | Propose **EXP008 + EXP010** reserved, covering both named media and both modes; freeze before fitting. | Keep v6 EXP004/010, both TC-42; all 11 eligible experiments in nested outer validation without a separate reserve. | Recommended **234 development + 74 reserved**; old pair **233 + 75**; all-group option up to **308** outer-fold predictions. | New condition evidence motivates the proposal, not performance. Nine development groups, only one clean fed-batch development group. Prior global EDA means no untouched external-test claim. |
| **D7: reliable prediction** | Baselines, Ridge, PLS and one bounded nonlinear comparator; experiment-weighted MAE on matched support, plus RMSE/bias, uncertainty and failures. | Simpler-only benchmark; broaden later with evidence. | Same **308** rows before fold-specific losses; no additional independent experiments. | All preprocessing/selection/tuning inside grouped inner folds. Investigate implausible/negative raw outputs before declared constraints. Operational acceptance thresholds remain unset. |
| **D8: forecasting** | After estimation, separate **12 h** task with inputs reconstructed at label time minus 12 h. | 6 or 24 h. | Joint-cohort positive-label ceilings **321/315/293** at 6/12/24 h; actual reanchored input support uncomputed. | No future inputs, interpolated labels or reuse of current-time snapshots. Multiple horizons are not independent samples; prior offline VCD requires evidenced availability. |
| **D9: optimization/autonomy** | Later advisory exploration; automate quality checks/abstention before intervention. | Defer; later controlled/mechanistic studies. | **0 validated intervention-effect examples** identified. | Associations do not establish effects of changing feed/controls. No automatic actuation or validated-twin claim. |

Evidence: [decision counts](decision-counts.json), [run detail](counts-by-run.csv),
[six-case support](zero-case-support.csv), [split alternatives](split-options.json).
Proposed development IDs: EXP001–007, EXP009, EXP012. Paired reactors remain grouped.
The released v6 split, source data and fitting flags have **not** been changed.

**Challenge protocol under the recommended defaults:** the EXP002 zero receives
a prediction from its outer experiment-held-out model, with preprocessing/tuning
restricted to the other eight development experiments. The five EXP011 zeros are
predicted by the frozen model trained on the nine development experiments; EXP011
is entirely unseen by that fit. Neither path uses reserved EXP008/EXP010 labels
or uncertain-zero labels for selection. Report each case and its unsupported/
uncertain status; do not rank models by treating those zeros as validated truth.
The clean-cohort include-zero sensitivity adds only EXP002 (**309 supported**).
Including all six also reverses the EXP011 quarantine and is a distinct broader
sensitivity (**339**), not the primary cohort.

**Split freeze gate:** no D6 option becomes operative until the owner selects it
and an immutable approved fitting protocol records the cohort, source fingerprints,
feature/timing policy, split IDs and evaluation rules. No fitting precedes that
freeze. Challenge findings cannot silently retune the frozen protocol.

## Unresolved author/source questions

- Numerical assay limits, rounding/QC, released SEM computation and each zero's
  disposition. Do not inverse-weight losses by unverified SEMs.
- Per-variable acquisition/availability, synchronization/tie order; exact alignment
  grid/ties; instrument-specific Status and calibration records; EXP004 duplicates.
- Any undeposited supplements, full medium recipes and
  dataset reuse terms. The preprint license does not fill Zenodo's blank dataset
  license. Original retrieval time remains unknown.

No author was contacted. These questions cannot be resolved by an owner vote.
**Approve or amend D1–D9 before fitting.** Approval would authorize only the specified
retrospective research, not deployment, actuation or scientific validation. The
[engineering packet](../stage12/pre-modeling-decision-packet.md) and its deferred
engineering findings remain retained.
