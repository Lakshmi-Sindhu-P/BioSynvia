<div align="center">

<img src="docs/assets/biosynvia-banner.svg" alt="BioSynvia — Bioprocess Research and Digital Twin Foundations" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![pandas](https://img.shields.io/badge/pandas-DataFrames-150458?style=flat-square&logo=pandas&logoColor=white)](#%EF%B8%8F-tech-stack)
[![NumPy](https://img.shields.io/badge/NumPy-Numerical_Analysis-013243?style=flat-square&logo=numpy&logoColor=white)](#%EF%B8%8F-tech-stack)
[![SQLite](https://img.shields.io/badge/SQLite-Lineage_%26_Queries-003B57?style=flat-square&logo=sqlite&logoColor=white)](#%EF%B8%8F-tech-stack)
[![Version](https://img.shields.io/badge/Version-0.1.0-6f42c1?style=flat-square)](pyproject.toml)
[![Status](https://img.shields.io/badge/Status-Research-FFB300?style=flat-square)](#%EF%B8%8F-research-roadmap)
[![Tests](https://img.shields.io/badge/Core_tests-18_passing-1D9E75?style=flat-square)](tests/test_audit.py)
[![License](https://img.shields.io/badge/License-Proprietary-475569?style=flat-square)](LICENSE)

<br/>

> **A reproducible bioprocess research workbench that preserves measurement provenance,
> exposes quality and timing risks, and builds the foundation for current VCD estimation,
> future forecasting and an eventual digital twin.**

<br/>

<sub><b>Stages 1–2</b> — data auditing, exploratory analysis and scientific-evidence review.<br/>Engineering checkpoint accepted. Model fitting remains paused pending approval.</sub>

<br/>

[📊 Overview](#-overview) &nbsp;·&nbsp;
[🧬 Dataset](#-dataset-at-a-glance) &nbsp;·&nbsp;
[🛠️ Tech Stack](#%EF%B8%8F-tech-stack) &nbsp;·&nbsp;
[⚖️ Feature Policy](#%EF%B8%8F-feature-and-timing-policy) &nbsp;·&nbsp;
[🔑 Findings](#-key-findings) &nbsp;·&nbsp;
[📸 Visuals](#-visual-outputs) &nbsp;·&nbsp;
[🗺️ Roadmap](#%EF%B8%8F-research-roadmap) &nbsp;·&nbsp;
[🚀 Setup](#-setup) &nbsp;·&nbsp;
[📚 Citations](#-research-citations)

</div>

---

## 📊 Overview

Bioreactors produce dense sensor streams, while reference measurements of living
cells are collected much less frequently. Different clocks, sampling intervals,
held process values and quality states make those observations difficult to combine
correctly. A careless join can produce convincing relationships that fail in a new
experiment—or depend on information unavailable at prediction time.

BioSynvia asks: **what can we reliably learn about a culture from information that
would actually be available at the time?** Its first prediction target is **viable
cell density (VCD)**, the concentration of living cells in the culture.

<br/>

| Research layer | Question | Current position |
|:---------------|:---------|:-----------------|
| 📊 **Descriptive** | What was measured, and how do cultures differ? | Reproducible EDA and source audits implemented |
| 🔬 **Scientific / validity** | Which observations and relationships can we trust? | Evidence reviewed; uncertainties and owner choices retained |
| 🤖 **Predictive** | What is current VCD, and what could it be later? | Estimation first, forecasting second; no models fitted yet |
| 🎯 **Exploratory decisions** | Which process scenarios deserve further study? | Later work; observational prediction is not a causal effect |
| 🧬 **Digital twin** | Can observations and dynamics support a validated process representation? | Long-term research goal, not the current release |

The intended benefit is better visibility into culture state and, after prospective
validation, less routine manual interpretation. Unsupported inputs should produce
an explicit quality flag or abstention rather than an unexplained estimate.

---

## 🧬 Dataset at a Glance

| | |
|:---|:---|
| 📁 **Source** | Uhlendorff et al. (2026), [Zenodo CHO cultivation dataset](https://doi.org/10.5281/zenodo.20829178) |
| 🧪 **Experimental units** | **12 experiments**, each with R01/R02: **24 CHO-K1 cultivations** |
| ⚙️ **Modes** | 9 batch experiments and 3 fed-batch experiments |
| 📚 **Raw structure** | 12 workbooks × 16 reactor-specific worksheets |
| 🔗 **Aligned exports** | 24 inline CSVs × 41 columns; 24 offline CSVs × 17 columns |
| 📐 **Reported variables** | 38 continuous inline and 10 primary offline variables, plus timestamps, SEMs and cumulative logs |
| 🎯 **Reference records** | **378 offline assay records**—not 378 independent experiments |
| 🧫 **Named media** | TC-42 and TCX6D, with reported condition variations |

<details>
<summary>🔍 &nbsp;<b>What the measurements contain</b></summary>

<br/>

**Inline/process:** permittivity, turbidity, dissolved CO₂, pH, dissolved oxygen,
temperature and operating variables.

**Offline:** VCD, total cell density, viability, cell properties, glucose, lactate,
ammonium and osmolality. No measured amino-acid profiles are supplied.

Original Excel cells retain assay values, blanks, source timestamps and supplied
quality fields. Publisher-aligned CSVs are useful for descriptive exploration but
are not automatically causal feature tables. The source archive, processed
observation bundles and full reference documents remain local.

Methods: [data-descriptor preprint](https://doi.org/10.20944/preprints202611.0377.v1),
version 1, not peer reviewed. [Full attribution](CITATIONS.md).

</details>

---

## 🛠️ Tech Stack

These technologies are used in the implemented foundation; planned modeling is
listed separately from completed work.

| Layer | Technology | Role in BioSynvia |
|:------|:-----------|:------------------|
| 🐍 **Language / CLI** | Python 3.11+, `argparse` | Local audits, preparation and reproducible command-line workflows |
| 🧹 **Data processing** | pandas, NumPy | Copied working tables, profiling, numeric checks and feature preparation |
| 📗 **Excel ingestion** | openpyxl | Read workbook streams, original cells, headers and coordinates |
| 🗃️ **Storage / queries** | SQLite (`sqlite3`), CSV, JSON | Persistent analysis tables, source lineage and decision artifacts |
| 📈 **Visualization** | Matplotlib | Descriptive EDA, coverage and relationship figures |
| 🔐 **Provenance** | `hashlib`, `zipfile`, `pathlib` | Checksums, archive inspection and source/output preservation |
| 🧪 **Verification** | Python `unittest` | Identity, timing, missingness, reproducibility and failure-path checks |
| 📄 **Document generation** | ReportLab, pypdf | Generate and preserve versioned project specification documents |
| 🗂️ **Version control** | Git, GitHub; Mermaid/SVG documentation | Code history, evidence navigation and workflow presentation |

**Planned after approval:** baseline, Ridge, PLS and bounded nonlinear comparisons,
followed by uncertainty evaluation and a separate forecasting protocol. These are
not completed model results or installed product capabilities.

The core synthetic audit uses the Python standard library only. Analysis workflows
have separate dependencies recorded in [the scripts guide](scripts/README.md).

---

## ⚖️ Feature and Timing Policy

A useful estimate must respect **which reactor produced the observation and when
the information would have been available**.

| Information | Proposed treatment | Reason |
|:------------|:-------------------|:-------|
| Same-reactor sampled sensors | Past-only candidates with freshness and quality checks | Prevent future or cross-reactor information from entering a snapshot |
| pH, oxygen and temperature process states | Distinguish held state from fresh acquisition; absent Status stays unknown | Change-only logging can forward-fill values |
| Publisher-aligned signals | Descriptive use; causal reconstruction required before modeling | Nearest-neighbor alignment can select a future observation |
| Assay-updated feed history | Withhold until point-in-time availability is established | Control updates used offline VCD/glucose information |
| Offline assays and SEMs | Targets/diagnostics, not sensor-only predictors | Avoid target-derived inputs and unknown result latency |
| Experiment/reactor IDs | Grouping and provenance, not predictive shortcuts | Paired reactors stay inside their whole experiment group |

<details>
<summary>⏱️ &nbsp;<b>Retrospective support is not real-time validation</b></summary>

<br/>

Existing support counts assume sensor acquisition equals availability for a
retrospective research scenario. Strictly requiring evidenced result availability
currently yields **zero supported rows**. This is a timing-evidence gap, not a
claim that all sensor measurements are invalid.

Similarly, requiring an explicit `Ok` on every eight-core input yields zero
complete rows because some streams have no Status field. An absent field,
blank status, warning and invalid measurement remain different states.

</details>

---

## 🔑 Key Findings

<details>
<summary>🧪 &nbsp;<b>Six recorded zeros need separate scientific interpretation</b></summary>

<br/>

All six VCD zeros are numeric source values. Five occur in contaminated EXP011 R02;
the EXP002 R02 case is separately unresolved. Contamination supplies context, not
proof of the exact meaning or QC disposition of each zero. Every case is retained
for explicit challenge/sensitivity analysis rather than silently accepted or erased.

</details>

<details>
<summary>🧹 &nbsp;<b>214 original blanks cannot become measured zeros</b></summary>

<br/>

There are **135 glucose**, **51 lactate** and **28 ammonium** blanks. The paper
describes below-detection/quantification concentration results; numerical bounds
are not supplied. Preserve that encoding and uncertainty rather than substituting
measured zeros or assuming random missingness.

</details>

<details>
<summary>📐 &nbsp;<b>A cohort decision changes the research question and sample count</b></summary>

<br/>

At the stated five-minute retrospective policy, separating uncertain zero labels
and choosing a contamination policy produces:

| Proposed cohort | Positive source records | Supported positive records |
|:----------------|------------------------:|---------------------------:|
| Retain all EXP011 | 372 | 333 |
| Quarantine EXP011 R02 | 360 | 322 |
| Quarantine all EXP011 | 343 | **308** |

These are **feasibility counts, not accuracy results**. The conservative proposal
quarantines all EXP011 because contamination and both-reactor antibiotic exposure
complicate interpretation. All alternatives and original observations remain
preserved; owner decisions are pending.

</details>

<details>
<summary>🔗 &nbsp;<b>Lineage records are not additional training samples</b></summary>

<br/>

The released engineering bundle contains **15,120 assay-feature lineage records**
for **378 assays × 40 candidate fields**. Those records document source selection;
they are not 15,120 independent training examples. Whole-experiment grouping
remains the evaluation boundary.

</details>

---

## 📸 Visual Outputs

**Descriptive observations, not predictions.** Data: Uhlendorff et al. (2026);
figures generated by BioSynvia's EDA scripts.

<p align="center">
  <img src="reports/eda-v2/coverage_and_growth.png" alt="Assay coverage and observed growth ranges across experiments" width="49%"/>
  <img src="reports/eda-v2/raw_assay_missingness.png" alt="Original blank concentration cells by analyte" width="49%"/>
</p>

<p align="center">
  <img src="reports/eda-v2/trajectories.png" alt="Batch and fed-batch VCD trajectories alongside aligned sensor examples" width="100%"/>
</p>

Lines between assays are visual guides, not interpolated labels. Sensor overlays
use publisher-aligned values for description, not evidence of causal availability.
Recorded zeros remain uncertain. The blank-cell chart's historical “missing” label
describes source encoding; the later paper review supplies the below-limit context.

[Read the EDA report →](reports/eda-v2/report.md)

---

## 🔄 Research Workflow

```mermaid
flowchart LR
    A[Preserve observations] --> B[Audit schema and quality]
    B --> C[Same-reactor past-only snapshots]
    C --> D[Scientific review and protocol freeze]
    D -. Approval required .-> E[Current VCD estimation]
    E -. Separate evaluation .-> F[Future VCD forecasting]
    F -. Later research .-> G[Process scenario exploration]
    G -. Validation required .-> H[Digital twin]
```

Current estimation comes first, forecasting second and exploratory optimization
third. The end goal is a validated connection between observations, state
estimation and process dynamics. Better prediction alone does not establish causal
control effects or justify automatic actuation.

---

## 🗂️ Project Structure

```text
BioSynvia/
├── biosynvia/           # Audit CLI, source ingestion, preparation and lineage
├── scripts/             # Reproducible analysis and verification entry points
├── configs/             # Proposed target, timing, quality and evaluation policies
├── tests/               # Contract, isolation and reproducibility checks
├── examples/synthetic/  # Invented, dataset-free demonstration inputs
├── reports/             # EDA, scientific inferences and verification records
├── docs/assets/         # Original project visual assets
├── docs/specifications/ # PRD and SRD
├── CITATIONS.md         # Paper and dataset attribution
├── references.bib       # Machine-readable research references
├── THIRD_PARTY_NOTICES.md
└── LICENSE              # Restricted evaluation terms for original work
```

Original datasets, processed observation bundles, internal build/handoff documents
and local ignore rules are not included in the current public snapshot. Some
historical reports refer to those local artifacts.

---

## 🗺️ Research Roadmap

- [x] Source inventory, checksums and separate backup workflow
- [x] Exact workbook/CSV schema inspection and reproducible EDA
- [x] Original blank/zero preservation and source-cell lineage
- [x] Same-reactor snapshots, experiment grouping and leakage safeguards
- [x] Full-paper scientific review and a pre-modeling decision packet
- [ ] Approve cohort, feature/timing policies and experiment split
- [ ] Compare baselines, regularized models and a bounded nonlinear model
- [ ] Evaluate uncertainty, failure cases and prospective real-time availability
- [ ] Develop a separate future-VCD forecasting benchmark
- [ ] Explore bounded process scenarios and mechanistic/hybrid components
- [ ] Validate an eventual digital twin

**Best reliable prediction is the priority.** Scientific interpretation helps
identify mistakes and unrealistic relationships; it does not force a linear model
to outperform a better-supported nonlinear alternative.

---

## 🚀 Setup

Use **Python 3.11+** from the repository root. The synthetic audit requires no
third-party packages, API keys or research dataset.

```bash
python3 -m biosynvia audit \
  --sensors examples/synthetic/sensors.csv \
  --measurements examples/synthetic/measurements.csv \
  --output outputs/synthetic-audit.json

# Dataset-free core checks: 18 passed at the research checkpoint.
python3 -m unittest tests.test_audit tests.test_source -v
```

The invented example contains a deliberate blank assay value and produces an
expected warning. Choose a new output filename when rerunning: existing results
are protected. Full analysis and released-bundle checks require their documented
packages and local artifacts. See [scripts/README.md](scripts/README.md).

---

## 📚 Research Citations

**Data descriptor:** Uhlendorff, S., Fulek, R., Eimler, J., Pein-Hackelbusch, M.,
& Frahm, B. (2026). *Data Descriptor: Multimodal Dataset of Bioreactor Cell
Cultivations Including Turbidity, Permittivity, O₂ and CO₂ Measurements* (Version 1)
[Preprint]. Preprints.org.
[doi:10.20944/preprints202611.0377.v1](https://doi.org/10.20944/preprints202611.0377.v1).
Version 1 is not peer reviewed.

**Dataset:** Uhlendorff, S., Fulek, R., Eimler, J., Pein-Hackelbusch, M., & Frahm, B.
(2026). *Dataset Based on Chinese Hamster Ovary (CHO) Cultivations including
Turbidity, Permittivity, O2 and CO2 Measurements* (Version v1) [Data set]. Zenodo.
[doi:10.5281/zenodo.20829178](https://doi.org/10.5281/zenodo.20829178).

[Full references and attribution](CITATIONS.md) · [BibTeX](references.bib)

---

## 📜 License

Original BioSynvia material is **proprietary, with all rights reserved**, subject
to the limited non-commercial evaluation permission in [LICENSE](LICENSE).
This is **not an open-source release**. Applicable GitHub viewing/forking rights
remain intact. Third-party materials retain their own terms; see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The paper's CC BY notice does not
establish a license for the separate dataset.

---

## 🔎 Explore Further

[Scientific approval packet](reports/scientific-closure/approval-packet.md) ·
[Project report](reports/implementation-report.md) ·
[Preparation findings](reports/preparation/report.md) ·
[Relationship-analysis guide](reports/relationship-analysis-guide.md) ·
[PRD / SRD](docs/specifications/README.md)

---

<div align="center">

**Built by Lakshmi Sindhu P &nbsp;·&nbsp; Bioprocess data engineering and research**

AI-assisted implementation and review. Primary evidence and executable checks
support the work; agent agreement is not scientific validation.

[GitHub](https://github.com/Lakshmi-Sindhu-P)

</div>
