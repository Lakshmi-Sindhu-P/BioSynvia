# EDA follow-up on sensor coverage and recorded VCD zeros

November 5, 2026. Status: unresolved scientific data-quality questions; no model fitting.

## What the original EDA does

Exploratory data analysis checks the contents, structure, ranges, missingness and
time coverage of a dataset before selecting modeling rules. The project-owned
`scripts/eda.py` reads the publisher ZIP, verifies its checksum, profiles all 48
aligned CSVs, inventories all 192 original worksheet headers/dimensions and
compares all original offline assay values against aligned values. It generates
tables, figures, fingerprints and a narrative report. It does not select a final
holdout, impute data, train a model or approve a scientific target.

The first EDA established 274,781 sensor timestamps, 378 assay timestamps and 12
independent experiment groups, with two reactors per experiment. A minute of sensor
recording is a row, not a new independent cultivation. SEM fields are uncertainty
summaries accompanying assay means, not independent samples.

## Investigation method

`scripts/investigate_data_quality.py` now reads every row of all 16 sheets in each
of the EXP011 and EXP002 original workbooks. It preserves the source archive,
records source hashes/cell coordinates, profiles sensor endpoints and Status
categories, and computes the latest prior raw/CSV timestamp at each R02 assay.
It checks source cell types with formula interpretation disabled: the six VCD
zeros are numeric Excel cells, not formula text or blank values converted by this
analysis. This targeted investigation complements the wider descriptive EDA.

## Finding 1 The aligned cutoff does not mean every sensor stopped

EXP011_fed-batch_R02_inline.csv ends at 67.133333 hours, while its offline assay
table continues to 195 hours. Nine assay timestamps in that reactor fall after
the aligned file ends: 73.5, 90.5, 95, 125, 148.5, 162.5, 171, 186 and 195 hours.

The original workbook tells a more detailed story:

| Original EXP011 R02 stream | Last timestamp in hours |
| --- | --- |
| Dissolved CO2 | 195.113611 |
| Turbidity | 195.113611 |
| Permittivity and fitted channels | 195.113611 |
| Process parameters | 195.600000 |
| Cumulative NaOH | 195.166667 |
| Cumulative feed | 67.139444 |
| Offline cell and medium analyses | 195.000000 |

The feed stream ends first, within about 22 seconds of the aligned CSV endpoint.
That is consistent with an export limited by the shortest available stream. The
alignment/export code has not been recovered, so this is an inference, not a
confirmed algorithm or cause. The files do not establish why feed recording ends.
Do not equate an end to feed logging with feed stopping, equipment failure or
experimental termination.

Other original streams retain observations close to later assay times. For example,
at the five zero-VCD assay times, the latest prior raw turbidity and permittivity
records are roughly 11–16 seconds old. The latest prior CO2 record at 195 hours
is about 71 seconds old. Process-parameter records exist at all five assay times.
These are acquisition-time checks; accepted availability semantics, quality and
transformation rules still require review.

Consequences: distinguish aligned_export_coverage from per_stream_raw_coverage.
Do not extend the aligned 40-field row by carrying feed or every other value
forward from 67 hours. A future canonical importer can assess usable raw sensor
families individually under an approved feature contract. It must retain feed
missingness and must not silently infer feed after recording ends.

## Finding 2 Six VCD zeros are recorded measurements pending interpretation

| Experiment and reactor | Assay times with numeric zero VCD in hours | Original VCD cells |
| --- | --- | --- |
| EXP011 R02 | 148.5, 162.5, 171, 186, 195 | R02_offline_CellAnalysis B14 through B18 |
| EXP002 R02 | 209.5 | R02_offline_CellAnalysis B16 |

For all six records, VCD SEM, viability mean and viability SEM are also zero.
Total cell density remains positive: approximately 4.27–6.74 million cells/mL
for the five EXP011 records and 15.5 million cells/mL for EXP002's last record.
The nonzero TCD and other populated assay fields make these different from an
entirely empty assay row, but do not prove assay validity.

The immediately preceding data show very low recorded viable fractions:

- EXP011 R02: at 125 hours, VCD is approximately 1,816.7 cells/mL and reported
  viability is 0.0367%, before the first zero at 148.5 hours.
- EXP002 R02: at 193 hours, VCD is approximately 99,466.7 cells/mL and reported
  viability is 0.59%, before the final zero at 209.5 hours.

This pattern is compatible with a declining measured viable population. It cannot
resolve whether the exact zeros mean no viable cells detected, a detection or
reporting threshold, rounding, an instrument/QC convention, or another documented
experimental condition. A zero SEM does not establish zero measurement uncertainty
or resolve the detection limit.

The source cell-analysis sheets have no Status column. Sensor stream Status
values are therefore not assay QC decisions. The near-cutoff/latest-prior raw
CO2, turbidity and permittivity records at these zero-assay times report Ok, but
that status cannot certify the VCD assay.

### Distinguish three situations

| Situation | Evidence | Treatment before scientific review |
| --- | --- | --- |
| Original blank, aligned zero | 214 medium-assay cells in the full EDA | Preserve missingness; not an observed-zero label |
| Original numeric VCD zero | Six cells identified here | Preserve numeric zero and source; quality pending |
| Numeric nonzero VCD | Other 372 recorded means | Recorded value exists; not automatically scientifically approved |

The issue register marks the six zeros recorded_zero_pending_assay_review with
label_approved false. This is a review disposition, not a scientific rejection or
a replacement of the raw value. No approved training-label set exists yet.

## Finding 3 Sensor Status requires explicit preservation and semantics

All original Status rows in EXP011 and EXP002 were counted, including warning
transitions. EXP011 R02 permittivity has 31 Warning Active rows at startup and
23,383 Ok rows; its warning-to-Ok transition occurs at approximately 0.258333
hours. CO2 and turbidity Status values in this reactor are all Ok. EXP002 R02
permittivity is Ok throughout even though some fitted channels are all zero in
the earlier EDA. Thus Ok alone does not establish that every derived channel is
informative or valid for a particular modeling use.

Use the raw status field alongside field availability, zero/constant-channel
patterns, instrument meaning and reviewed validity rules. Preserve original
status text rather than silently treating every value as accepted. The separate
unique-value profiler scans Status columns in all 12 original workbooks; see
`reports/unique-values/categorical_values.json` for the full-source categories.

## Open questions before modeling

1. What caused the EXP011 R02 feed log to stop near 67.14 hours? Was the aligned
   export intentionally restricted to common support across all streams?
2. How were original sensors resampled, matched or interpolated? Which timestamps
   represent acquisition and when would their values be available for inference?
3. What cell counter/assay protocol, detection limit, rounding, dilution and QC
   rules apply to the six zero-VCD records? Were any records censored or flagged?
4. Are exact zero, below detection limit and no viable cells detected distinct
   source conventions? Are replicate values/counts and experiment notes available?
5. What do Ok and Warning Active mean for each instrument and fitted channel?

The public Zenodo description explains general time-axis alignment but does not
answer these run/assay-specific questions. The preprint landing page likewise
does not establish their scientific meaning. No author has been contacted and
no cause has been assigned from those pages.

Sources checked: https://zenodo.org/records/20829178 and
https://www.preprints.org/manuscript/202611.0377 . The preprint is not peer reviewed.

## Files and reproduction

Run the script using the same optional analysis environment described in
`scripts/README.md`:

```sh
python scripts/investigate_data_quality.py --output reports/quality-review-new
python scripts/profile_unique_values.py --output reports/unique-values-new
```

Existing output directories are protected. Read `stream_profiles.csv`,
`recorded_zero_vcd.csv`, `zero_source_cells.csv`, `sensor_status_counts.csv`,
`sensor_status_transitions.csv`, `assay_stream_support.csv` and
`issue_register.json` beside this report for exact records and scope.
