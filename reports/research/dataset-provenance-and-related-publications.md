# Dataset provenance and related-publication research

Date: 2026-11-05

## Purpose

This report investigates how the BioSynvia CHO dataset was produced, which research project funded it, which publications from the same group are most relevant, and which experimental details are confirmed versus inferred.

The central conclusion is that the archive was produced within the TH OWL CellSENSING research program and was deliberately released for soft-sensor, data-driven, mechanistic, and hybrid bioprocess modeling. Several publications from the same researchers directly support the intended viable-cell-density modeling direction. However, the public dataset record does not identify the exact culture-medium formulation, cell-analysis instrument, medium-analysis instruments, reactor model, or time-alignment algorithm. Closely related papers provide strong clues, but those clues must not be recorded as exact dataset facts without author confirmation or an exact methods paper.

## Evidence standard used in this report

- **Confirmed exact-dataset fact:** stated in the Zenodo record, the supplied files, or metadata carrying the exact dataset DOI or funding number.
- **Strongly related evidence:** same research group, cell line, sensor type, target, project, or funding, but no explicit citation linking the paper's experimental records to this exact archive.
- **Inference or instrument fingerprint:** a plausible conclusion from column names or related methods, retained as a hypothesis rather than a fact.
- **Not the same dataset:** methodologically useful work involving a different organism or experiment.

This distinction is important because agreement between filenames, publications, and model choices is not enough to prove that two sets of experimental records are identical.

## 1. Confirmed origin of the archive

The official record is:

- Title: *Dataset Based on Chinese Hamster Ovary (CHO) Cultivations including Turbidity, Permittivity, O2 and CO2 Measurements*
- DOI: [10.5281/zenodo.20829178](https://doi.org/10.5281/zenodo.20829178)
- Repository page: [Zenodo record 20829178](https://zenodo.org/records/20829178)
- Creators: Selina Uhlendorff, Ruwen Fulek, Jonas Eimler, Miriam Pein-Hackelbusch, and Björn Frahm
- Institutions: Institute for Life Science Technologies (ILT.NRW), Institute Industrial IT (inIT), and Biotechnology and Bioprocess Engineering at OWL University of Applied Sciences and Arts (TH OWL), Lemgo, Germany
- License: CC BY 4.0
- Funding identifier: 13FH045KX2, Federal Ministry of Education and Research
- Publication date: 2026-08-11

The Zenodo metadata contains no related-publication identifier and no reference list. Therefore, no paper can currently be declared the official companion paper solely from the repository metadata.

## 2. What the experiment archive contains

The dataset contains 24 CHO-K1 cultivations arranged as 12 experiments with two parallel reactors per experiment:

- EXP001–EXP009: nine batch experiments
- EXP010–EXP012: three fed-batch experiments
- R01 and R02: the two separate parallel reactor records inside each experiment
- Working volume: 0.55–0.8 L
- Cultivation duration: 161.5–328.5 h

The raw workbook folder contains 12 `.xlsx` files. Each workbook has 16 sheets: eight measurement groups for R01 and the same eight groups for R02.

The eight groups are:

1. `inline_CO2`
2. `inline_Turbidity`
3. `inline_Permitivity` (spelling retained from the supplied workbook)
4. `Inline_ProcessParameters`
5. `online_NaOH`
6. `online_Feed`
7. `offline_CellAnalysis`
8. `Offline_MediumAnalysis`

The aligned folder contains 48 CSVs: 12 experiments × 2 reactors × 2 file types. Reactors remain separate. For example, `EXP001_batch_R01_inline.csv` contains only EXP001/R01 records, while `EXP001_batch_R02_inline.csv` contains only EXP001/R02 records.

### Why the visible CSV column counts exceed 38 inline plus 10 offline

The official description counts underlying variables, not every exported statistical or operational column.

An aligned inline CSV has 41 columns in total:

- one `Time (h)` column
- 38 inline sensor/process variables
- two online addition records: `Cumulative NaOH weight (g)` and `Cumulative feed weight (g)`

An aligned offline CSV has 17 columns in total:

- one `Time (h)` column
- ten underlying offline measurements
- six extra SEM columns because six cell-analysis measurements are exported as a mean and a standard error of the mean

The ten underlying offline measurements are:

1. viable cell density (VCD)
2. total cell density (TCD)
3. viability
4. average cell diameter
5. average compactness
6. aggregation
7. glucose
8. lactate
9. ammonium
10. osmolality

For the first six, the aligned file stores `Mean` and `SEM`. This produces 12 cell-analysis columns plus four medium-analysis columns, or 16 visible measurement columns after `Time (h)`.

## 3. Inline, online, and offline in this dataset

### Inline

An inline sensor measures the culture or process directly in or at the bioreactor without requiring a sample to be removed. These signals are recorded frequently and can support near-real-time monitoring.

Examples in the aligned files include:

- dissolved CO2
- turbidity transmission and reflection
- conductivity
- permittivity and derived Cole-Cole parameters
- capacitance at multiple frequencies
- pH
- dissolved oxygen
- temperature
- agitation and aeration conditions
- inlet gas fractions and individual gas-flow components
- estimated liquid volume

### Online

Terminology varies across laboratories. In these workbooks, `online` is used for automatically recorded actions of connected equipment, specifically NaOH and feed additions. These values describe what the running system added, rather than a laboratory assay of the cells.

- `Cumulative NaOH weight (g)` tracks the accumulated base addition, usually associated with pH control.
- `Cumulative feed weight (g)` tracks the accumulated nutrient-feed addition. It is particularly meaningful in fed-batch runs.

Although the aligned export places these columns inside the file named `_inline.csv`, the original workbook keeps them in separate `online_NaOH` and `online_Feed` sheets. The CSV is therefore a convenient reactor-level modeling table, not evidence that the authors considered pump records identical to immersed sensor measurements.

### Offline

Offline measurements require a sample to be removed and analyzed on separate laboratory equipment. They occur much less often—up to twice per day according to the official description—but serve as biological and chemical reference measurements.

The cell-analysis fields describe the cells themselves. The medium-analysis fields describe the liquid environment and cell metabolism.

The role of the offline measurements is crucial: the inline sensors continuously observe indirect physical effects, while the offline assays provide the reference values needed to teach or validate a soft sensor.

## 4. The CellSENSING project connection

The dataset's exact funding number, 13FH045KX2, matches the TH OWL CellSENSING project. This is confirmed by the [TH OWL ILT.NRW 2024 annual report](https://www.th-owl.de/files/webs/ilt-nrw/Jahresberichte/Jahresbericht_2024.pdf) and the [CellSENSING project page](https://transformern.de/cellsensing/).

CellSENSING began in 2024 and focuses on soft-sensing systems for three bioprocess areas:

1. yeast viability and vitality in brewing
2. beer-maturation metabolites such as diacetyl
3. viable cell density and viability in mammalian-cell cultivation for biopharmaceutical production

The project combines hardware sensors, sensor fusion, data processing, mathematical modeling, and machine learning. Its industrial partners include Hamilton Bonaduz AG and Schneider Electric GmbH, among others.

This makes the BioSynvia direction scientifically aligned with the source project's purpose. Estimating VCD or viability from continuous reactor signals is not an arbitrary downstream use; it is one of the project's stated goals.

## 5. Closest publications from the same group

### 5.1 Strongly related: phase-aware VCD models using dielectric spectroscopy

**Publication:** Selina Uhlendorff, Tatsiana Burankova, Katharina Dahlmann, Björn Frahm, and Miriam Pein-Hackelbusch, *Application Constraints of Linear Multivariate Regression Models for Dielectric Spectroscopy in Inline Bioreactor Viable Cell Analysis*.

- DOI: [10.1109/IWIS69004.2025.11339388](https://doi.org/10.1109/IWIS69004.2025.11339388)
- Official institutional record: [TH OWL ELSA 13475](https://www.th-owl.de/elsa/record/13475)
- Venue: 2025 International Workshop on Impedance Spectroscopy; proceedings published in 2026

The institutional abstract reports comparison of partial least squares and Ridge regression across cultivation phases, followed by a segmented model with a learned phase transition and gradual switching. It uses 11 mammalian-cell-culture datasets and highlights heterogeneity between cultivations.

**Relationship assessment:** very strong, but not proven exact. It has the same lead researcher, research group, sensor technology, VCD target, and Hamilton collaborators. The count of 11 datasets is close to the archive's 12 experiments. However, neither the paper metadata nor Zenodo record explicitly states that those 11 datasets are 11 of these 12 experiments.

**What it means for BioSynvia:** Ridge and PLS are scientifically justified baselines. Phase-adaptive or segmented modeling should be considered after simpler baselines because a single global relationship may change between growth, stationary, and decline phases.

### 5.2 Strongly related precursor: dielectric preprocessing and VCD estimation

**Publication:** Selina Ramm, Tanja Hernández Rodríguez, Björn Frahm, and Miriam Pein-Hackelbusch, *Systematic Preprocessing of Dielectric Spectroscopy Data and Estimating Viable Cell Densities*.

- DOI: [10.1109/INDIN51400.2023.10218012](https://doi.org/10.1109/INDIN51400.2023.10218012)
- Official institutional record: [TH OWL ELSA 10788](https://www.th-owl.de/elsa/record/10788)

This paper examines five preprocessing strategies for dielectric spectroscopy and compares single-frequency linear regression, Cole-Cole modeling, and multi-frequency partial least squares regression for VCD. The abstract specifically mentions capacitance at 3347 kHz, which is also an exact frequency column in this archive. PLS performed better on average than the simpler linear approach in that study.

Selina Ramm and Selina Uhlendorff share ORCID 0000-0002-0502-8032 in the institutional records, establishing that these are publications by the same researcher under different surnames.

**Relationship assessment:** same researcher, group, target, sensor family, and exact frequency channel. It predates the CellSENSING grant and does not prove use of this 12-experiment archive. It is best treated as a methodological precursor.

**What it means for BioSynvia:** preprocessing order, normalization, smoothing, frequency selection, and use of multiple frequency channels should be tested explicitly. The project should not treat every dielectric channel as automatically reliable or independent.

### 5.3 Related method evidence: how the group counts CHO-K1 cells

**Publication:** Selina Uhlendorff, Ulrich Odefey, Björn Frahm, and Miriam Pein-Hackelbusch, *Performance Comparison between Semi-Automated and Manual Cell Counting for Animal Cell Culture*.

- DOI and full article: [10.1002/cite.70048](https://onlinelibrary.wiley.com/doi/10.1002/cite.70048)

This separate CHO-K1 experiment reports:

- CHO-K1 cells supplied by Bielefeld University's Cell Culture Technology Group
- TC-42 w/o GF medium supplemented with 8 mM L-glutamine
- trypan-blue exclusion
- semi-automated counting using a Countstar BioTech instrument
- three measurement chambers per test sample
- output and comparison of total cell density and viability
- calculation and reporting of standard errors

The BioSynvia dataset's cell-analysis columns—density, viability, diameter, compactness, aggregation, means, and SEMs—are compatible with an image-based cell-counting workflow such as Countstar. The related paper also comes from the same group and cell line.

**Relationship assessment:** related method evidence only. This publication describes a separate shake-flask dilution-series experiment, not the 24 bioreactor cultivations. It does not prove that the Zenodo archive used TC-42 medium, 8 mM L-glutamine, Countstar, or the exact same staining and replication procedure.

**High-priority hypothesis:** the dataset's cell-analysis columns may be exports summarized from Countstar BioTech measurements. A Cedex-style analyzer can produce similar morphology fields, so the exact instrument remains unresolved.

### 5.4 Same funded project, different organism: permittivity anomaly handling

**Publication:** Emils Bolmanis, Selina Uhlendorff, Miriam Pein-Hackelbusch, Vytautas Galvanauskas, and Oskars Grigs, *Anomaly detection and removal strategies for in-line permittivity sensor signal used in bioprocesses*.

- DOI and open article: [10.3389/fbioe.2025.1609369](https://pmc.ncbi.nlm.nih.gov/articles/PMC12343699/)

This study is funded partly under the exact CellSENSING grant and explains that permittivity probes respond to cells with intact membranes. It also discusses disturbances caused by process changes, antifoam addition, and bubbles near the sensor tip, and proposes real-time anomaly detection and correction.

**Relationship assessment:** methodologically relevant but not the same dataset. The experiments involve *Pichia pastoris*, and their data are deposited under a different Zenodo DOI.

**What it means for BioSynvia:** spikes and shifts in permittivity must not automatically be interpreted as true biological changes. Anomaly review should be tied to nearby changes in agitation, gas flow, additions, and other process events.

## 6. What can and cannot be concluded about how the data were obtained

### Confirmed

- CHO-K1 cells were cultured in 24 parallel-reactor cultivations.
- The experiments include batch and fed-batch operation.
- The work used multiple continuous sensors and separate offline reference analyses.
- Sensor streams had slightly different sampling intervals and accumulated timing offsets.
- The authors produced a common master time axis and aligned all inline signals to it.
- The archive is designed for soft sensors and data-driven, mechanistic, and hybrid models.
- The exact grant and research program target continuous estimation of VCD and viability.

### Strongly suggested but not confirmed for the exact archive

- The dielectric sensor system is likely from Hamilton's process-analytics family because Hamilton is a CellSENSING partner and coauthors appear on the 2025/2026 VCD-modeling paper. The derived Cole-Cole and multi-frequency fields are also compatible with that technology.
- Cell counts may have been generated with Countstar BioTech and summarized over replicate chambers.
- The cell line may have come from Bielefeld University's Cell Culture Technology Group.
- The base medium may have been TC-42 w/o GF with L-glutamine.

These points must remain hypotheses until an exact methods source or author response confirms them.

### Still unresolved

- exact basal medium and lot/formulation
- exact feed composition and feeding strategy for EXP010–EXP012
- exact cell-analysis instrument and settings
- exact glucose, lactate, ammonium, and osmolality analyzers and assay methods
- reactor manufacturer/model and control-system architecture
- inoculation density and seed-train details for every run
- experimental differences intentionally introduced across EXP001–EXP012
- calibration and maintenance details for pH, dissolved oxygen, gas, turbidity, and dielectric sensors
- whether pH, dissolved oxygen, and temperature quality flags existed upstream but were omitted from the release
- the exact interpolation/resampling method, master interval, tolerance, and missing-value policy used to create aligned CSVs
- whether the 11 datasets in the IWIS publication are a subset of the 12 released experiments

## 7. Consequences for BioSynvia's data and modeling plan

1. **The present VCD soft-sensor goal is well aligned.** The source program explicitly seeks real-time estimates of CHO VCD and viability.
2. **PLS and Ridge are meaningful baselines.** The same group has used these models for dielectric spectroscopy and VCD.
3. **Experiment-grouped evaluation remains essential.** The related work reports strong heterogeneity across cultivations. Random row splitting would let neighboring time points from the same cultivation leak into both training and test sets.
4. **Culture phase matters.** A single model may not preserve the same relationship during growth, stationary, and decline phases.
5. **Permittivity requires anomaly checks.** Sensor spikes or shifts can come from bubbles or process interventions rather than biology.
6. **Offline VCD is a measured reference with uncertainty.** Mean and SEM columns show that repeated readings were summarized. The target is not an error-free truth value.
7. **NaOH and feed should be treated as interventions.** They are automated addition histories, useful as process-event features but conceptually different from a direct biological sensor.
8. **Do not interpolate offline labels by default.** Filling the long gaps between samples can manufacture target values. It may be acceptable for visualization or carefully defined state-estimation work, but model evaluation should remain anchored to actual assay timestamps unless a separate interpolation protocol is justified.
9. **Preserve reactor identity.** R01 and R02 are parallel but distinct cultivations and should never be silently averaged or merged as if they were one reactor.
10. **Keep exact-method uncertainty visible.** Missing metadata about medium, feed, and assays limits mechanistic interpretation and cross-study generalization.

## 8. Recommended next research actions

### Highest value

1. Obtain the full IWIS paper and inspect its methods, experiment identifiers, sample counts, medium, instruments, and data split.
2. Ask the dataset authors whether the 11 datasets in that paper correspond to 11 of the 12 Zenodo experiments.
3. Ask for an experimental run sheet describing what varied between EXP001–EXP012.
4. Ask for the exact cell counter, metabolite analyzers, osmolality instrument, medium, feed, reactor, and sensor models.
5. Ask for the time-alignment script or a precise description of the master grid, interpolation/hold method, and maximum allowed temporal gap.

### Useful author questions

- Which basal medium and supplements were used in each experiment?
- What was the feed composition and schedule for EXP010–EXP012?
- Were VCD, TCD, viability, diameter, compactness, and aggregation measured on Countstar BioTech or another analyzer?
- How many replicate readings produced each mean and SEM?
- Which instruments produced glucose, lactate, ammonium, and osmolality values?
- Which pH, dissolved-oxygen, gas, turbidity, and dielectric probes were used?
- What changes were intentionally made between experiments and between parallel reactors?
- How were online NaOH/feed weights synchronized with the inline master time axis?
- Were missing or failed sensor readings interpolated, forward-filled, or left missing?
- Do the 11 datasets in DOI 10.1109/IWIS69004.2025.11339388 overlap this archive?

No external message has been sent. Author contact would require a separate user-approved action.

## 9. Research-process note

A background fresh-context research reviewer was started to independently inspect provenance and related publications. That reviewer stopped because its usage allowance was exhausted and produced no usable report. The primary agent therefore completed the source review directly. This is a workflow limitation, not scientific evidence, and should remain recorded rather than silently omitted.

## 10. Primary sources

- [Zenodo dataset record and description](https://zenodo.org/records/20829178)
- [Official Zenodo API metadata for record 20829178](https://zenodo.org/api/records/20829178)
- [TH OWL ILT.NRW annual report 2024: CellSENSING project](https://www.th-owl.de/files/webs/ilt-nrw/Jahresberichte/Jahresbericht_2024.pdf)
- [CellSENSING project page](https://transformern.de/cellsensing/)
- [TH OWL institutional record: Application Constraints of Linear Multivariate Regression Models](https://www.th-owl.de/elsa/record/13475)
- [TH OWL institutional record: Systematic Preprocessing of Dielectric Spectroscopy Data](https://www.th-owl.de/elsa/record/10788)
- [Wiley: Performance Comparison between Semi-Automated and Manual Cell Counting](https://onlinelibrary.wiley.com/doi/10.1002/cite.70048)
- [Frontiers/PMC: Anomaly detection and removal strategies for in-line permittivity](https://pmc.ncbi.nlm.nih.gov/articles/PMC12343699/)

