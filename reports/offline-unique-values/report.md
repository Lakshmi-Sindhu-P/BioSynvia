# Original offline unique values and medium interpretation

Dated November 5, 2026. Descriptive evidence only; no models fitted.

> Subsequent evidence: the full author preprint identifies TC-42/TCX6D media and reports that offline concentration blanks denote below-limit/nonquantifiable results. The original blank encoding and distinct numeric counts below remain unchanged. See `reports/scientific-closure/approval-packet.md` for current interpretation; the earlier recipe-unknown wording below is historical.

This report uses the frozen v5 source-exact `assay_source_cells.csv`, after verifying its manifest hash. Values are decoded from original `raw_value_json`, preserving workbook blanks separately from numeric zero. It supplements the older aligned-CSV distinct-value profile, which includes publisher-inserted zeros for some missing medium measurements. Original data are unchanged.

All 24 reactor runs contribute 378 records per measurement column. The two original time columns are excluded from this measurement-value profile. Cell analysis contains six mean measurements plus six SEM columns; medium analysis contains four measurements. SEM columns describe reported uncertainty, not additional nutrients or cell properties. Their replicate construction is unresolved.

## Counts for every measurement column

| Family | Original column | Distinct numeric values | Missing | Numeric zeros | Range (source units) |
| --- | --- | ---: | ---: | ---: | --- |
| CellAnalysis | Aggregation Mean (%) | 369 | 0 | 0 | 1.476666666666667 to 47.11666666666667 |
| CellAnalysis | Aggregation SEM (%) | 377 | 0 | 0 | 0.04163331998932298 to 7.061485522025645 |
| CellAnalysis | Avg. compactness Mean | 52 | 0 | 0 | 0.65 to 0.9 |
| CellAnalysis | Avg. compactness SEM | 26 | 0 | 103 | 0.0 to 0.01154700538379246 |
| CellAnalysis | Avg. diameter Mean (µm) | 331 | 0 | 0 | 12.01666666666667 to 18.0 |
| CellAnalysis | Avg. diameter SEM (µm) | 338 | 0 | 0 | 0.003333333333333633 to 0.2803767306876788 |
| CellAnalysis | TCD Mean (cells/mL) | 343 | 0 | 0 | 371000.0 to 18833333.33333333 |
| CellAnalysis | TCD SEM (cells/mL) | 332 | 0 | 1 | 0.0 to 1299042.382338279 |
| CellAnalysis | VCD Mean (cells/mL) | 363 | 0 | 6 | 0.0 to 16166666.66666667 |
| CellAnalysis | VCD SEM (cells/mL) | 351 | 0 | 6 | 0.0 to 737706.656545209 |
| CellAnalysis | Viability Mean (%) | 371 | 0 | 6 | 0.0 to 97.26333333333332 |
| CellAnalysis | Viability SEM (%) | 373 | 0 | 6 | 0.0 to 7.375879608561957 |
| MediumAnalysis | Ammonium (mM) | 349 | 28 | 0 | 0.104760909398867 to 48.93362765317522 |
| MediumAnalysis | Glucose (g/L) | 241 | 135 | 0 | 0.1065 to 7.878 |
| MediumAnalysis | Lactate (g/L) | 319 | 51 | 0 | 0.0555 to 8.58 |
| MediumAnalysis | Osmolality (mOsmol/kg) | 140 | 0 | 0 | 154 to 511 |

The full sorted values and frequency counts are in `distinct_values.json`; `distinct_values_by_run.json` retains experiment/reactor separation. `summary_by_run.csv` provides the same descriptive counts separately for each run. Numeric equality is exact after JSON decoding, with no rounding or bins; therefore very close numbers can be distinct. These counts are not independent sample counts or biological categories.

## What this identifies

Glucose is a measured nutrient concentration; lactate and ammonium are measured metabolites commonly associated with metabolic by-product accumulation. Osmolality measures total dissolved-particle concentration and does not identify a particular waste molecule. VCD, TCD, viability, diameter, compactness and aggregation describe cells rather than medium formulation. All source unit labels are preserved; their scientific validation remains pending.

The original medium table has **no recorded numeric zeros** in any of its four measurement columns. Its 135 glucose blanks, 51 lactate blanks and 28 ammonium blanks remain missing. This is distinct from the six recorded VCD zeros, which remain scientifically unresolved. The observed ammonium maximum is reported as recorded, not interpreted as a validated toxicity threshold or confirmed concentration.

## Which medium might produce which by-products?

General CHO biology supports conditional hypotheses, not identification of a medium recipe from unique values:

| Nutrient/process context | Plausible behavior to investigate | Limitation |
| --- | --- | --- |
| Glucose supplied and high glycolytic activity | Lactate accumulation, including when oxygen is available | Glucose concentration alone does not determine lactate production. |
| Glutamine and other nitrogen-containing nutrients | Ammonia/ammonium accumulation can accompany nitrogen metabolism | Glutamine can also degrade chemically; ammonium need not all originate from cells. This dataset has no glutamine time series or amino-acid profiles. |
| Changing medium, cell state and process conditions | Lactate production can switch to net consumption | Lactate is not always merely waste, and this switch is not universal. |

Primary experimental evidence: [Zagari et al., lactate metabolic shift and medium composition](https://pubmed.ncbi.nlm.nih.gov/22683938/) found different lactate behavior across CHO cell lines and media. [Kurano et al., medium components and waste products](https://doi.org/10.1016/0168-1656(90)90055-G) examined glutamine instability and spontaneous ammonia generation as well as cellular metabolism. These studies supply general hypotheses, not validation of the BioSynvia assays.

The [dataset record](https://zenodo.org/records/20829178) establishes the archive identity. A newly located [author data-descriptor preprint, posted November 4, 2026](https://www.preprints.org/manuscript/202611.0377), states that medium and initial glutamine conditions varied; the accessed abstract does not supply experiment-level medium recipes or mappings. It is not peer reviewed. No medium identity has been assigned from this abstract.

## Necessary next interpretation step

Obtain experiment-to-medium names, recipes or product identifiers, initial nutrient supplements, feed composition and schedule, sample handling, and assay methods. Then compare glucose/lactate/ammonium trajectories within each reactor and across appropriately matched experiments. Keep process mode, pH, oxygen conditions, cell density and time visible. Changes in concentration alone are not cell-specific production rates: feeding, volume changes, sampling and dilution require mass-balance treatment. Do not label a medium as causing a waste profile using pooled correlations or unique values alone.

All original scientific questions remain open, including assay SOPs, replicate/SEM definitions, detection/reporting limits, six-zero disposition, result availability, clock synchronization, sensor/status semantics, calibration, feed cutoff, export alignment, timestamp collisions, retrieval provenance and reuse terms. Model fitting remains paused.

## Reproduction and evidence

Run `python3 scripts/profile_offline_unique_values.py --source data/processed/v5/assay_source_cells.csv --output <new-directory>`. The script uses the Python standard library, refuses to overwrite an existing report, verifies its input against the frozen manifest, checks source-blank flags, and preserves run identity. Output fingerprints and source hashes are in `provenance.json`. Descriptive pooling never joins observations across reactors.
