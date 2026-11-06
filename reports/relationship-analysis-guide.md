# How we will investigate relationships in BioSynvia

November 5, 2026. This is an analysis protocol and explanation, not model results.

## Your workflow and the important adjustment

Backing up data, working on copies, checking shape/types/unique values/nulls,
understanding features, preparing inputs/outputs and saving the result is a sound
foundation. There is no single universally mandated EDA sequence. This project
adds source provenance, assay quality, time/availability rules, sensor statuses,
experiment dependence and a reproducible transformation log.

The main sequencing adjustment is to reserve experiment groups before using
relationships to choose model inputs. Initial source/quality auditing can inspect
all files; transformations that learn from data, such as imputation, scaling,
PCA and feature selection, must be fitted on development/training folds only.
The earlier whole-dataset EDA was descriptive and must be disclosed when defining
the later evaluation protocol. No pristine untouched-data claim should be made.

Source: [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls).

## Nonlinear relationships

Pearson correlation measures linear association. A feature can be useful when the
relationship is curved, changes direction or depends on another variable. In a
synthetic example, y = x squared is strongly related to x, yet the linear
correlation is zero when x is symmetrically distributed around zero. That is a
mathematical example, not a finding about any BioSynvia sensor.

| Method | What it can reveal | Important limitation |
| --- | --- | --- |
| Scatterplots and per-experiment smooth trends | Curves, thresholds, clusters, outliers and differing trajectories | A pooled curve can reflect experiment or culture-age differences |
| Spearman or Kendall rank association | Whether one variable tends to increase as another increases, without requiring a straight line | Can still miss a U-shaped or interacting relationship; dependent rows require appropriate uncertainty |
| Mutual information | Dependence that need not be linear or monotonic | Estimates need adequate samples; high scores do not prove causation or generalization |
| Splines or generalized additive models | Flexible, inspectable curves | Complexity must be controlled within grouped validation |
| Tree-based models with feature-family ablations | Thresholds, interactions and incremental predictive value | Can overfit small numbers of independent experiments |
| Partial dependence, ICE and permutation importance | How a fitted model responds or relies on inputs | Describe the model, not causation; correlated features can mislead interpretation |

We will start with plots by experiment and process mode, compare rank/linear
summaries descriptively, then compare a simple baseline against a limited set of
nonlinear models under the same group-safe validation. A low individual
correlation is not an automatic deletion rule. Correlated channels may be grouped
into a feature family and tested by ablation or handled by regularization/PLS.

Sources: [feature selection and mutual information](https://scikit-learn.org/stable/modules/feature_selection.html),
[partial dependence and ICE](https://scikit-learn.org/stable/auto_examples/inspection/plot_partial_dependence.html),
[correlated-feature permutation importance](https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance_multicollinear.html).

## Time-dependent relationships

Two signals can track culture age without one usefully predicting the other.
A sensor can also respond earlier or later than an assay-associated change.
The investigation must preserve reactor identity, actual elapsed time, sampling
support and the prediction cutoff.

1. Plot sensor and assay trajectories within each reactor, with acquisition gaps,
   quality flags and actual assay timestamps visible.
2. Compare relationships within reactors and across experiments. Remove run means
   as a descriptive sensitivity check; this alone does not remove time trends.
3. Inspect scientifically motivated earlier sensor values and past-only window
   summaries: means, variability, slopes and age/support counts. Use elapsed-time
   windows rather than a fixed number of rows when sampling is irregular.
4. Examine lag relationships after checking trends, sampling and autocorrelation.
   Do not apply a standard regularly sampled cross-correlation formula directly
   to irregular laboratory assays or create interpolated target labels to do so.
5. Evaluate phase/lag/window choices only within development folds. The final
   holdout cannot determine the best lag or feature window.

For a prediction at time t, a candidate can use a sensor value from t minus two
hours, if supported and available, but not a reading after t. Smoothing with future
points, centered rolling windows and backward filling from future observations
would leak information. A correlation peak at a lag does not establish causality.

Sources: [statsmodels cross-correlation interface](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html),
[grouped and time-dependent validation](https://scikit-learn.org/stable/modules/cross_validation.html).

## Biological and instrument understanding

| Feature family | Why investigate it | Current disposition |
| --- | --- | --- |
| Permittivity and frequency-derived channels | Dielectric signals can reflect polarizable cell properties and viable biovolume; cell size and calibration matter | Keep primary permittivity for inspection; review fitted channels, statuses, units and redundancy |
| Transmission and reflection | Optical measurements can carry cell-density information, with instrument/sample dependence | Keep for inspection; do not assume they exclusively measure viable cells |
| Dissolved O2/CO2 | Culture/process signals that may carry information about operating conditions and biological activity | Keep as candidates; check gas inputs, control and temporal behavior |
| pH and temperature | Operating-state/context signals | Retain for initial inspection; low variance or weak pooled correlation is not sufficient to exclude |
| Conductivity | Medium/process context and sensor-family information | Retain as a candidate; inspect dilution/feed and overlap with other signals |
| Process settings, volume and cumulative additions | Context, possible dilution/feeding effects, or experiment-design proxies | Separate extended candidates; availability and generalization need review |
| Offline assays, SEM columns and identifiers | Targets, uncertainty summaries, lineage and group structure | Not default sensor-only model inputs; do not encode experiment ID as a predictive feature |

Manufacturer sources provide general measurement principles, not confirmation of
the exact instrument/protocol used in this dataset. No field's scientific unit or
calibration is approved solely from its header or a product page.

Sources: [Hamilton measurement principles](https://www.hamiltoncompany.com/knowledge-base/article/incyte-cell-density-measurement-principles),
[Hamilton cell-density monitoring manual](https://assets-sensors.hamiltoncompany.com/File-Uploads/624702-12_Manual_CellDensityMonitoring_LR.pdf?v=1632906127),
[optek optical/process measurement products](https://www.optek.com/en/products.asp).

## Applying this to the saved preparation pipeline

The initial persisted preparation uses eight domain-motivated core inspection
fields and retains all other raw-derived feature candidates separately. It saves
Pearson feature matrices, target Pearson/Spearman associations, within-run-centered
Pearson values and a nonzero-target sensitivity comparison. These summaries do
not select features, establish causality or account fully for time dependence.

A five-minute freshness setting is an explicitly provisional inspection assumption,
not a scientifically approved universal limit. No target imputation, model fitting,
final feature approval or train/test partition has occurred. The saved outputs
are suitable for inspection and protocol review, not an approved training release.

Before fitting, settle the six recorded-zero assay interpretations, original sensor
status/unit policy, availability assumptions, independent-group protocol and
scientific error criteria. These are data/validation needs rather than missing
advanced algorithms.
