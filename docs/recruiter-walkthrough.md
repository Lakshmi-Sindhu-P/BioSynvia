# Recruiter walkthrough

BioSynvia is a research software project for CHO bioprocess data and eventual
soft sensing. Current work establishes a reproducible scientific foundation;
predictive models have not been fitted and no digital twin has been validated.

## A two-minute review

1. Run the synthetic audit from the README. It preserves a deliberately blank
   assay cell and checks experimental identity without needing a dataset or API key.
2. Inspect `biosynvia/stage12.py`: controlled same-reactor snapshots, explicit
   quality states, provenance, experiment grouping and closed fitting gates.
3. Read `reports/scientific-closure/approval-packet.md`: published methods,
   uncertain cases, sample-count tradeoffs and pending research decisions.
4. Review `tests/test_audit.py`, `tests/test_stage12.py` and
   `tests/test_released_isolation.py` for adversarial identity, timing and
   source-preservation checks. Release-data tests require the local frozen bundle.

## What this demonstrates

- Python data engineering across heterogeneous Excel/CSV streams.
- Preservation of original observations, missingness and provenance.
- Scientific literature review that changes proposed modeling assumptions.
- Prevention of time and experiment leakage.
- Reproducible analysis, explicit uncertainty and reviewable engineering decisions.

## Suggested project description

Built a reproducible CHO bioprocess data-auditing and preparation pipeline with
source-cell lineage, reactor isolation and leakage safeguards. Audited twelve
experiments and developed an evidence-based pre-modeling decision packet covering
uncertain labels, sensor availability and grouped evaluation. Predictive modeling
is the next gated stage.

## How to present it

Pin this repository on your GitHub profile. Link it under Projects on your resume
and LinkedIn. A short screen recording can show the synthetic audit, one lineage
check and a scientific decision that changed after reading the source paper.
Discuss the tradeoffs and reproducibility evidence; report prediction accuracy
only after approved modeling and evaluation actually produce it.

AI tools assisted development and review. Executable checks and cited source
material provide the evidence; agent agreement does not validate biology.
