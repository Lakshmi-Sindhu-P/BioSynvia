# Supporting scientific publications — 2026-11-05

These primary research publications support checks and hypotheses for BioSynvia.
They do not establish the methods, calibration, label validity or performance of
the deposited dataset. The cited abstracts were inspected; full-paper methods
and supplements are not claimed reviewed here.

| ID | Primary publication / inspected location | Supported finding | Consequence proposed for BioSynvia |
| --- | --- | --- | --- |
| L1 | [Opel, Li and Amanullah (2010), Biotechnology Progress, DOI 10.1002/btpr.425](https://pubmed.ncbi.nlm.nih.gov/20730773/), abstract; [publisher abstract](https://aiche.onlinelibrary.wiley.com/doi/10.1002/btpr.425) | Linear, Cole–Cole and PLS biomass models lost accuracy to varying degrees in stationary/decline phases; correcting with offline radius did not remove deviations. | Inspect errors across time and cell states. A single positive permittivity–VCD relationship is not a universal validity test. Do not use future/offline size measurements as sensor-only inputs. |
| L2 | [Kroll, Stelzer and Herwig (2017), Biotechnology Letters, DOI 10.1007/s10529-017-2408-0](https://pubmed.ncbi.nlm.nih.gov/28786039/), abstract | A combined permittivity/turbidity soft sensor was investigated using two fed-batch processes; turbidity contained information from viable, dead and lysed populations. | A turbidity signal need not vanish at recorded zero VCD. The six uncertain cases cannot be adjudicated by turbidity alone. Results from two other processes do not validate our model. |
| L3 | [Salimi et al., Sensitivity of bulk electrical impedance spectroscopy probes to cell and culture properties, DOI 10.1002/btpr.3519](https://aiche.onlinelibrary.wiley.com/doi/full/10.1002/btpr.3519), abstract, published online 2024 and journal issue 2025 | The study's sensitivity analysis links permittivity increment to cell size and concentration and critical frequency to several changing cellular properties. | Use physical interpretation to investigate suspicious relationships and phase failures; do not equate every dielectric channel with a direct viable-cell count or impose a universal monotonic constraint. |

These are defensible reasons to compare a transparent baseline and flexible
predictors, retain uncertainty, and perform error analysis. Choosing a model,
threshold, feature policy or target mask remains an owner protocol decision.
No publication here explains the six deposited VCD zeros or verifies a digital
twin for BioSynvia. No models were fitted during this research.
