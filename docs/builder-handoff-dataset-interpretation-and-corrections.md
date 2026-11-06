# BioSynvia builder handoff: dataset interpretation, corrections and required report updates

Date: 2026-11-05  
Status: user-reviewed handoff for correction and pre-modeling review  
Scope: conversation history, dataset interpretation, Stage 1-2 work, identified mistakes, and instructions for the builder

## 1. Purpose of this handoff

This document records the user's questions, the findings the user independently identified, the explanations subsequently given, the implementation evidence reviewed, and the corrections that must be acknowledged in the project record. It is intended to prevent incorrect interpretations from being repeated or silently carried into modeling.

The builder must:

1. read this document before making further data or modeling changes;
2. audit the current code and outputs against every correction below;
3. update the appropriate project report with an explicit interpretation-corrections section;
4. distinguish an incorrect explanation from an actual implementation defect;
5. preserve negative and unresolved findings;
6. pause before model fitting until the user reviews the corrected pre-modeling packet.

This handoff does not authorize model fitting.

## 2. Project objective and current position

BioSynvia is intended to investigate whether CHO cultivation data can support process-development tools such as soft sensors, data-driven models, mechanistic models, hybrid models and, eventually, digital-twin components.

The practical motivation is that cell-culture experiments take substantial time, labor and material, and unsuccessful experiments are costly. A useful model could eventually help scientists estimate difficult-to-measure biological states, compare process conditions, detect unsupported operating regions, and explore process-development questions before running every possible experiment.

The project is not yet a digital twin. It is currently establishing the data foundation required to investigate one responsibly. Stage 1 and Stage 2 cover data meaning, quality, provenance, timing, feature eligibility, group-aware evaluation design and reproducible preparation. No predictive model has been fitted and no performance claim exists.

## 3. Dataset provenance

Publisher record: https://zenodo.org/records/20829178  
DOI: https://doi.org/10.5281/zenodo.20829178  
Title: *Dataset Based on Chinese Hamster Ovary (CHO) Cultivations including Turbidity, Permittivity, O2 and CO2 Measurements*  
Authors: Uhlendorff, Fulek, Eimler, Pein-Hackelbusch and Frahm.

The local archive is `data/raw/Dataset.zip`. The recorded archive size is 227,627,771 bytes, MD5 is `71b2a35b7df2ed11644ec9f177453772`, and SHA-256 is `46a6...17b` in the existing manifest. The exact retrieval event was not recorded at download time and must not be invented later.

The dataset contains:

- 12 experiments;
- two parallel reactors per experiment, producing 24 cultivation runs;
- EXP001 through EXP009 in batch mode;
- EXP010 through EXP012 in fed-batch mode;
- cultivation durations reported as approximately 161.5 to 328.5 hours;
- working volumes reported as approximately 0.55 to 0.8 L;
- 38 continuous inline variables;
- 10 primary offline variables sampled up to about twice per day.

## 4. Correct workbook structure, identified by the user

The user correctly established the workbook structure after inspecting the source.

There are 12 Excel workbooks, one per experiment. Every workbook has exactly 16 worksheets:

- eight worksheets for reactor R01;
- eight worksheets for reactor R02.

For each reactor, the eight worksheet families are:

1. `inline_CO2`
2. `inline_Turbidity`
3. `inline_Permittivity`
4. `inline_ProcessParameters`
5. `online_NaOH`
6. `online_Feed`
7. `offline_CellAnalysis`
8. `offline_MediumAnalysis`

The reactor prefix is part of each worksheet name. For example, `R01_inline_CO2` belongs to R01 and `R02_inline_CO2` belongs to R02.

Therefore:

```text
2 reactors x 8 worksheet families = 16 worksheets per experiment
12 experiments x 16 worksheets = 192 worksheets in the archive
```

R01 and R02 are parallel physical reactors. They are not dataset versions, repeat numbers to be discarded, or interchangeable streams. They must remain distinct cultivation runs throughout preparation, analysis, splitting and modeling.

The direct archive audit found all 12 workbooks conform to the expected 16-sheet structure. Across the complete archive, each worksheet family occurs 24 times because there are 12 experiments and two reactors per experiment.

## 5. What the eight worksheet families mean

### 5.1 Inline and online records

Inline measurements are produced automatically by sensors operating in or directly connected to the bioreactor. They provide frequent measurements over the course of a cultivation.

- `inline_CO2`: dissolved carbon dioxide and a supplied status field.
- `inline_Turbidity`: optical transmission and reflection, plus a supplied status field. These signals describe how light interacts with the culture and may change as cells and particles accumulate.
- `inline_Permittivity`: conductivity, permittivity, fitted dielectric quantities, multiple frequency channels and a supplied status field. Permittivity describes how the culture responds to an applied electric field and can be related to viable cell volume, but field meaning and calibration still require scientific confirmation.
- `inline_ProcessParameters`: pH, dissolved oxygen, temperature, agitation, aeration and gas-flow settings, inlet-gas fractions and liquid volume. This sheet does not contain a `Status` column.
- `online_NaOH`: cumulative sodium-hydroxide addition. NaOH is commonly used by the control system to counter acidification and maintain pH.
- `online_Feed`: cumulative feed addition. In fed-batch experiments, feed supplies nutrients during cultivation.

"Online" and "inline" both refer to measurements or equipment records obtained during the process. The publisher's naming distinguishes particular logged systems, but the exact acquisition and availability semantics still require documentation.

### 5.2 Offline records

Offline measurements are obtained by taking a sample from the reactor and analyzing it with separate laboratory equipment. They are sparse because samples are collected much less frequently than sensor signals.

- `offline_CellAnalysis` describes the cell population: viable cell density, total cell density, viability, average cell diameter, compactness and aggregation, including SEM support fields.
- `offline_MediumAnalysis` describes the liquid environment surrounding the cells: glucose, lactate, ammonium and osmolality.

Medium analysis exists because cells both consume nutrients and release waste products. Cell analysis answers what is happening to the population. Medium analysis helps explain the environment in which that population is growing or declining.

## 6. Biological interpretation explained during the discussion

### 6.1 VCD, TCD and viability

- Viable cell density (VCD) is the concentration of living cells per milliliter.
- Total cell density (TCD) includes living and non-living cells counted by the assay.
- Viability is the percentage of counted cells classified as living.

VCD can increase when viable cells divide faster than they die. It can slow, plateau or decrease because of nutrient limitation, waste accumulation, unfavorable pH, inadequate oxygen transfer, temperature changes, osmolality stress, shear or mixing stress, feed strategy, inoculum differences, contamination, the natural growth phase, or measurement uncertainty.

Viability can remain high while growth slows, or decline after stress or nutrient depletion. VCD, TCD and viability must be interpreted together rather than as interchangeable measures.

### 6.2 Diameter, compactness and aggregation

- Average diameter describes estimated cell size.
- Compactness is an instrument-derived description of cell-image morphology and requires the assay/instrument definition before strong biological interpretation.
- Aggregation estimates the proportion of cells appearing in clumps.

These can change with growth phase, cell-cycle distribution, stress, cell death, osmotic conditions, nutrient state, shear, sampling and instrument settings. They must not be treated as direct causal indicators without assay documentation.

### 6.3 Medium variables

- Glucose is a major nutrient and carbon source.
- Lactate is a metabolic by-product whose accumulation or consumption can indicate changes in metabolism.
- Ammonium is a waste product that may become inhibitory.
- Osmolality describes the total dissolved-particle concentration and can change because of feed, base addition, evaporation and metabolite accumulation.

### 6.4 Process variables

- pH describes acidity or alkalinity.
- Dissolved oxygen describes oxygen available in the liquid relative to the instrument scale.
- Temperature affects growth and metabolism.
- Agitation and aeration influence mixing and gas transfer but may also contribute to shear.
- CO2 and O2 measurements describe gas exchange and metabolic respiration conditions.
- Turbidity describes optical cloudiness or light interaction.
- Permittivity and related dielectric measurements describe electrical response and may support viable-biomass estimation.

These explanations are orientation for a new data scientist, not validated definitions of the publisher's exact instruments or calibration.

## 7. Correct time-axis-aligned CSV structure

The publisher also supplied a folder called `Time-axis aligned raw data tables`. This is not a BioSynvia lineage folder. It is a publisher-provided synchronized representation of the measurements.

There are 48 CSV files:

```text
12 experiments x 2 reactors x 2 measurement types = 48 CSV files
```

For every experiment and reactor, there is:

- one aligned inline CSV;
- one aligned offline CSV.

The publisher explains that individual sensors had slightly different sampling intervals and accumulated small timing offsets. The inline streams were placed on a common master time axis. The exact resampling, interpolation, causal-availability and edge-handling algorithm has not been recovered from the supplied documentation.

### 7.1 Aligned inline files

There are 24 aligned inline files. Each has 41 columns:

- one `Time (h)` column;
- 40 potential input columns.

The 40 inputs comprise the 38 reported continuous inline variables plus cumulative NaOH and cumulative feed.

The aligned inline tables contain approximately 3,983 to 19,099 data rows each. They do not include the original sensor `Status` columns.

### 7.2 Aligned offline files

There are 24 aligned offline files. Each has 17 columns:

- one `Time (h)` column;
- 10 primary offline variables;
- six SEM support columns.

The 10 primary offline variables are VCD, TCD, viability, diameter, compactness, aggregation, glucose, lactate, ammonium and osmolality. The dataset does not contain amino-acid profiles.

The aligned offline tables contain approximately 12 to 23 assay rows each.

### 7.3 Actual EXP001 samples inspected

The actual source files have these shapes:

- `EXP001_batch_R01_inline.csv`: 11,908 data rows x 41 columns;
- `EXP001_batch_R01_offline.csv`: 15 data rows x 17 columns;
- `EXP001_batch_R02_inline.csv`: 11,839 data rows x 41 columns;
- `EXP001_batch_R02_offline.csv`: 15 data rows x 17 columns.

The first R01 inline record at time 0 includes CO2 17.3037033081055, transmission 0.994854986667633, reflection -0.102288998663425, conductivity 12.0459995269775, permittivity 0.38434100151062, pH 7.03, dissolved oxygen 84.727 and temperature 36.196.

The first R02 inline record at time 0 includes CO2 21.8982925415039, transmission 1.00850999355316, reflection 0.0493279993534088, conductivity 12.6021003723145, permittivity -0.359459012746811, pH 7.024, dissolved oxygen 83.551 and temperature 36.143.

R01 and R02 do not necessarily have the same timestamp sequence. They must never be joined by row position or time alone.

## 8. Correct storage and combination design

The source files must remain unchanged and separate in the raw layer. A working database may stack rows from multiple experiments and reactors into a common table, but stacking must not blend the biological runs.

Correct logical organization:

```text
Raw publisher layer
  24 separate inline CSVs
  24 separate offline CSVs
  12 separate Excel workbooks

Canonical analysis layer
  inline_measurements_all_runs
  offline_assays_all_runs
  raw_sensor_quality_and_lineage

Modeling layer
  one row per selected offline assay
  features drawn only from the same experiment and reactor
  only measurements available at or before the prediction cutoff
```

Every stacked record must carry at least:

- `experiment_id`;
- `reactor_id`;
- `run_id`, such as `EXP001_R01`;
- time;
- source file and, where applicable, source worksheet/cell evidence.

Inline and offline records must remain in separate principal tables. The system must not create a giant table that repeats a sparse offline assay across every high-frequency inline timestamp. A modeling snapshot table may join selected past-only inline features to one offline assay, but only for the same `run_id`.

The term `combined_inline` means row-stacked inline observations with identifiers. It does not mean R01 and R02 were averaged or merged. To reduce confusion, a clearer name such as `inline_measurements_all_runs` is recommended.

## 9. Why both CSV and Excel sources are needed

The aligned CSVs are the convenient synchronized working representation. The Excel workbooks are the original laboratory/source representation.

Use the aligned CSVs for:

- rapid EDA and plotting;
- convenient multivariable sensor tables;
- publisher-aligned time-series inspection;
- a candidate modeling representation, after alignment causality is assessed.

Use the original workbooks for:

- original timestamps;
- sensor Status fields where supplied;
- exact worksheet and cell provenance;
- duplicate-timestamp evidence;
- authoritative offline missingness;
- auditing the aligned representation.

The sources are complementary, not competing.

Important limitations found:

1. The aligned inline CSVs omit the original sensor Status columns.
2. The publisher's exact alignment algorithm is unresolved. It is not yet known whether a value at time `t` can always be constructed using information available by `t`.
3. There are 214 original blank medium-assay cells represented as aligned zeros: 135 glucose, 51 lactate and 28 ammonium. These must remain missing, not observed zero measurements.
4. EXP011 R02's aligned inline export ends near 67.1333 hours, close to the end of its feed stream, while some original sensor streams continue near 195 hours. An aligned-file cutoff does not prove that every sensor or the cultivation stopped.

Recommended pre-modeling protocol:

1. use original workbook offline values as target and assay truth records;
2. retain the aligned inline CSVs as candidate feature tables;
3. overlay original status, provenance, duplicate and support evidence;
4. test whether aligned values can be reproduced from past-only information;
5. compare publisher-aligned and independently constructed past-only snapshots;
6. never reinterpret an original blank as a measured zero;
7. report aligned-export coverage separately from per-stream raw coverage.

## 10. The 378 assay records and 15,120 lineage records

There are 378 original VCD mean measurements across the 24 reactor runs. This means 378 laboratory assay times, not 378 experiments.

- 372 VCD values are positive;
- six VCD values are numeric zero;
- the six zeros occur in EXP002 R02 at 209.5 h and EXP011 R02 at 148.5, 162.5, 171, 186 and 195 h.

The zeros are recorded source values but their scientific meaning is unresolved. Positive TCD, zero viability and zero VCD SEM coexist in these records. This does not prove biological absence, censoring, a detection limit or exact certainty. The assay SOP, replicate method, reporting limit, rounding and QC disposition are required.

The 15,120 lineage records are:

```text
378 assay times x 40 possible sensor input fields = 15,120 audit records
```

Each lineage record says which same-reactor source measurement was considered for one feature at one assay cutoff, along with source file, sheet, row/cell or timestamp evidence, age, status availability and quality flags. These are not 15,120 independent model-training rows. The maximum target-row count remains 378 before filtering.

## 11. pH, dissolved oxygen and temperature Status correction

The original `inline_ProcessParameters` sheets contain numeric pH, dissolved oxygen and temperature values. They do not have a `Status` column.

This is not the same as:

- a numeric value being null;
- a supplied Status cell being blank;
- a sensor warning;
- an invalid measurement.

The correct statement is: the values are present, but the publisher did not supply a separate per-row Status field in that worksheet.

The strict rule requiring an explicit `Ok` status therefore gives zero support for any feature set that includes pH, dissolved oxygen or temperature. That is a consequence of the strict rule and source schema, not evidence that those variables are unusable.

The five-feature feasibility set contains fields with traceable Status columns:

- dissolved CO2;
- transmission;
- reflection;
- conductivity;
- permittivity.

The earlier eight-feature set adds:

- pH;
- dissolved oxygen;
- temperature.

These should be treated as separate data-quality scenarios. The five-feature set is not automatically scientifically superior. The eight-feature set must not be rejected solely because the sheet lacks a Status column. Both need matched-support comparisons and explicit interpretation.

## 12. EDA and preparation work already completed

The preparation workflow preserved the publisher archive and created a verified backup. It produced CSV copies and a queryable SQLite database.

The earlier preparation outputs included:

- 274,781 combined aligned inline observations;
- 378 aligned offline assay rows;
- 378 original offline assay rows;
- 15,120 raw-derived feature-lineage records;
- 378 processed candidate assay records;
- a provisional inspection subset;
- datatype, null, uniqueness, size and descriptive-statistics audits;
- correlation and relationship inspection outputs;
- source issue and manifest records.

Core reusable EDA practices discussed were:

- preserve and hash raw sources;
- inventory every file, sheet, row and column;
- identify units and types;
- distinguish missing, zero, invalid and not-applicable values;
- inspect duplicates, ranges, timestamps and group identifiers;
- understand target meaning and data availability;
- prevent temporal and group leakage;
- create reproducible derived versions and lineage;
- propose evaluation splits before fitting models;
- document assumptions and unresolved questions.

These are broadly reusable initial practices, but they are not an automatic universal checklist that resolves domain-specific meaning. Freshness thresholds, quality rules, target semantics, clinical or scientific interpretations and evaluation designs must be decided explicitly for each project.

The user raised a separate concern about whether similar standards were followed in other projects, including ClueLattice. No compliance conclusion about ClueLattice was established in this BioSynvia discussion. It requires a separate evidence-based audit.

## 13. Stage 1-2 Elephant-Goldfish execution

The user approved autonomous Stage 1-2 work using an Elephant-Goldfish orchestration model. The Elephant was responsible for project memory, specification, coordination, resolution and synchronized records. Fresh-context Goldfish reviewers covered scientific validity, data quality, temporal/group leakage, reproducibility/provenance and requirements scope before and after implementation.

Completed records include:

- `docs/stage12-executable-spec.md`;
- reviewed configuration contracts;
- `biosynvia/stage12.py`;
- `scripts/build_stage12.py`;
- `tests/test_stage12.py`;
- versioned processed outputs culminating in `data/processed/v5`;
- `reports/stage12/pre-modeling-decision-packet.md`;
- pre-review, post-review, resolution, verification and drift-check records.

Reported verification includes 37 passing tests and exact numeric/null agreement across 6,804 original offline source cells in v5. V4 contained small numeric reconstruction differences in 701 source/decision pairs; v5 rebuilt them from physical workbook cells and corrected the issue.

The proposed, not approved, holdout experiments are EXP004 for batch and EXP010 for fed-batch. No model was fitted. Scientific and owner approvals remain false.

## 14. Interpretation mistakes and corrections that must enter the project report

The builder must add a dated section titled approximately `Interpretation corrections and lessons learned`. It must include the following without defensiveness or concealment.

### Correction 1: workbook structure was initially communicated incorrectly or ambiguously

Correct structure: each experiment workbook has 16 sheets, comprising eight R01 sheets and eight R02 sheets. References to 24 sheets of a type meant 24 occurrences across the entire 12-workbook archive, not 24 sheets in one workbook.

Required action: add an executable archive assertion for the exact expected 16 sheet names in every workbook, even though the present archive passed the independent audit.

### Correction 2: R01 and R02 must be described as parallel reactors, not versions

They are separate biological cultivation runs and must remain isolated by `run_id`.

Required action: assert that joins, interpolation, snapshots, folds and evaluation never cross a `run_id` boundary.

### Correction 3: the time-axis-aligned folder is not the lineage dataset

It contains publisher-aligned CSV exports. BioSynvia lineage is a separately created audit mapping from assay-feature pairs to their source evidence.

Required action: correct terminology in reports and diagrams.

### Correction 4: an amino-acid-profile claim was unsupported and incorrect

The supplied aligned offline schema contains glucose, lactate, ammonium and osmolality, not amino-acid profiles.

Required action: remove any amino-acid statement unless a new verified source is added.

### Correction 5: the aligned CSVs were not initially inspected before some explanations were offered

This led to avoidable generalization. Direct inspection later established the exact 41-column inline and 17-column offline structures and the real EXP001 samples.

Required action: future dataset explanations must cite direct inspection evidence before interpretation.

### Correction 6: absent Status was at risk of being confused with null measurement values

pH, dissolved oxygen and temperature have numeric values but no supplied Status column. `Status not supplied`, `Status blank`, `Status warning`, `measurement null` and `measurement invalid` are distinct states.

Required action: retain these states separately in schemas, reports and eligibility logic.

### Correction 7: the five-versus-eight feature question was initially framed too narrowly

The five-feature scenario is feasible under an exact-Status rule because those source families have Status fields. The eight-feature scenario fails that strict rule because three process variables lack a Status column. This is a policy result, not evidence that pH, dissolved oxygen and temperature are poor predictors.

Required action: compare explicit scenarios and avoid calling strict-status failure scientific invalidity.

### Correction 8: the role of the aligned CSVs was under-explained

The preparation and EDA code did use all 48 aligned CSVs. The later Stage 1-2 evidence builder deliberately used original workbooks for source-exact lineage and used aligned data mainly for coverage information. Saying simply that the CSVs were not used would be inaccurate.

Required action: document the dual-source design and assign each source an explicit authority role.

### Correction 9: `combined` can be misunderstood as biological mixing

The existing code stacks reactor rows with `experiment_id`, `reactor_id` and `run_id`; it does not average R01 and R02. Nevertheless, the name can confuse nontechnical reviewers.

Required action: define `combined` as row-stacked, consider clearer names, and prove key-preserving isolation with tests.

### Correction 10: aligned values must not automatically be treated as original observations

The 214 original medium blanks represented as aligned zeros demonstrate that aligned convenience data cannot replace source interpretation.

Required action: original offline workbook cells remain authoritative for observed-versus-missing status.

### Correction 11: agreement among agents is engineering review, not scientific evidence

Fresh-context reviews can detect contradictions, leakage and implementation drift. They cannot validate assay biology, instrument calibration or undocumented laboratory procedures.

Required action: retain unresolved scientific questions even when all reviewers agree.

### Correction 12: current code was checked and did not show reactor mixing

The implementation extracts reactor identity from sheet names, selects assays by matching `run_id`, builds feature lineage for that run and requires both reactors when proposing an experiment group. This is a confirmed distinction between an explanation problem and an implementation defect.

Required action: record that the audit found no current R01/R02 mixing, while still adding stronger schema and join assertions.

## 15. Required builder audit and report changes

Before proposing Stage 3, the builder must produce a correction addendum that includes:

1. the exact 12-workbook, 16-sheet-per-workbook structure;
2. the exact 48 aligned-CSV structure;
3. a source-authority matrix for aligned CSV versus original Excel;
4. a diagram of raw, canonical and modeling layers;
5. a list of all keys used in joins and a declaration that time alone is never a sufficient join key;
6. tests proving no R01/R02 cross-join;
7. tests proving no experiment cross-join;
8. tests proving inline and offline remain distinct until a controlled assay snapshot is built;
9. tests preserving original blank versus numeric zero;
10. tests or evidence for exact expected workbook sheet names;
11. separate counts for aligned-export coverage and raw-stream coverage;
12. explicit handling of missing Status columns without treating them as measurement nulls;
13. the five-feature and eight-feature scenarios without scientific overclaiming;
14. a direct statement that amino-acid profiles are not present;
15. a direct statement that no model or digital twin has yet been fitted or validated;
16. a dated correction ledger linking every prior wording problem to its corrected statement;
17. confirmation that all existing negative and unresolved findings remain retained.

## 16. Scientific and owner questions still unresolved

The builder must not fill these gaps with assumptions:

- assay SOP and instrument method;
- replicate counts and SEM construction;
- VCD detection/reporting limits and rounding;
- scientific meaning and QC disposition of the six VCD zeros;
- result-availability time versus acquisition time;
- clock origin and synchronization across systems;
- meanings of `Ok`, blank and warning for each status-bearing instrument;
- calibration and exact interpretation of frequency/fitting channels;
- reason EXP011 R02 feed logging ends near 67.14 h;
- publisher's precise alignment and resampling algorithm;
- correct resolution of EXP004 duplicate timestamps;
- exact retrieval event and data-reuse terms.

## 17. Modeling direction after correction and approval

The planned modeling work should begin with bounded baselines rather than claiming a digital twin immediately:

1. define the approved target mask and estimand;
2. approve aligned versus independently reconstructed past-only features;
3. freeze whole-experiment development and holdout groups;
4. compare simple baselines, Ridge and PLS;
5. add only a limited nonlinear alternative if justified;
6. fit all preprocessing inside grouped development folds;
7. evaluate reserved experiments once after freezing the approach;
8. report per-experiment and per-reactor errors, unsupported cases and abstentions;
9. proceed to mechanistic or hybrid digital-twin research only when scientific interpretation and data support are sufficient.

The objective is a defensible progression from data audit to soft-sensor research and then, if eligible, to hybrid or digital-twin components. Current Stage 1-2 work is foundational and relevant to that goal, but it is not itself a digital twin.

## 18. Model-orchestration and usage policy to retain

The user wants usage-aware orchestration. Fresh-context Goldfish reviews should occur at specification and stage boundaries, not for every routine file. The current user preference is to use the available 5.6-class Codex model for ordinary coding and review and avoid 6/6.1-class models unless a concrete high-impact conflict or scientific-review need justifies them. Luna must not approve scientific interpretations. Model, reasoning level and role must be recorded for substantial tasks.

Earlier instructions referenced an 83% weekly allowance and retaining at least 60%. Later telemetry after a reset was reported as 85% five-hour and 98% weekly, subject to telemetry lag. Those numbers are historical observations, not current guaranteed balances. The workflow must check live limits when available and avoid unnecessary high-reasoning calls.

## 19. Final checkpoint requested from the builder

Return one corrected consolidated packet before model fitting. It must contain:

- the interpretation-corrections ledger;
- target recommendation and both treatments of the six zero-VCD records;
- aligned-CSV versus original-workbook authority rules;
- sensor quality, status and availability rules;
- five-feature and eight-feature eligibility scenarios;
- usable-sample effects by experiment and reactor;
- verified experiment split IDs and grouping logic;
- evaluation protocol;
- unresolved scientific questions;
- updated review findings and resolutions;
- verification evidence for schema, keys, source preservation and no cross-reactor mixing;
- a clear statement that model fitting remains paused.

The user must be able to trace every important claim to the actual source structure or a named project artifact. Any statement that remains an assumption must be labeled as an assumption.
