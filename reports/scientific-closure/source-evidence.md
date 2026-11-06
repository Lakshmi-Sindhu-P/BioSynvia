# Scientific-source closure: author/publisher evidence

**Date checked:** 2026-11-05 (America/Chicago)  
**Scope:** bounded primary-source closure for the unresolved scientific questions
in the Stage 1/2 decision packet. This is an evidence register, not assay
validation or approval to fit a model.

## Bottom line

The sources confirm the archive's identity, high-level experimental design,
raw-versus-aligned structure, time origin, methods for cell analysis,
instrument calibration procedure, medium/feed composition, and the supplied
alignment algorithm. They still do **not** provide a formula linking released
SEM fields to replicates, numerical detection/reporting limits, a disposition
for the VCD zeros, per-row calibration/QC records, `Status` semantics,
result-availability clocks, master-axis/tie details, or an EXP004
duplicate-resolution rule. No source permits converting these gaps into a
biological or causal conclusion.

## Sources inspected and retained evidence

| ID | Primary source and exact location inspected | What was inspected | Retained local evidence / integrity |
| --- | --- | --- | --- |
| Z1 | [Zenodo record 20829178](https://zenodo.org/records/20829178), **Description**, paragraphs 1–4; **Files** table; **Rights** field; accessed 2026-11-05 | Record HTML, archive preview, file inventory and record metadata | Existing local `data/raw/Dataset.zip`; 227,627,771 bytes; MD5 `71b2a35b7df2ed11644ec9f177453772` (matches the record); SHA-256 `46a6b92b77883d56df3be015895d93c85b2b2547121af0b8bc0a92f3fbefd17b`. The original retrieval timestamp is not known. A duplicate created during this check was fingerprint-matched then removed. |
| Z2 | [Zenodo archive preview](https://zenodo.org/records/20829178/preview/Dataset.zip?include_deleted=0), directory listing | Names/sizes of all archive members | Confirms the two directories and 12 workbooks plus 48 CSVs. No README, protocol, supplement, manual, or condition-map file appears in that inventory. |
| P1 | [Author preprint v1](https://www.preprints.org/manuscript/202611.0377), DOI [10.20944/preprints202611.0377.v1](https://doi.org/10.20944/preprints202611.0377.v1); **Methods**, printed pp. 2–6/10; **Data Record**, printed pp. 6–7/10; **Technical Validation** and **Usage Notes**, printed pp. 8–9/10; **Tables 1–3**; accessed 2026-11-05 | Complete manuscript was reviewed visually in the publisher's native viewer. The locally retained evidence is 10 viewer screenshots, `sources/preprint-viewer-page02.png` through `...page11.png`; viewer page N is printed manuscript page N-1/10. | Original PDF bytes were not retrievable by command-line download (publisher access denial/403), so the PNGs are browser-viewer evidence, not an archived PDF. The viewer showed the page title/DOI, pagination and CC-BY banner. P1 remains not peer reviewed and was posted 2026-11-04. |

### Explicitly inaccessible / not found

- **Preprint PDF bytes:** direct command-line retrieval remained publisher
  access-denied/403, but full text was subsequently readable in the native
  publisher viewer and visually captured as P1 above. No supplement list was
  visible in the ten-page manuscript screenshots. This does not establish that
  no supplementary material exists.
- **Zenodo supplements:** Z1 lists one deposited file, `Dataset.zip`; Z2 shows
  only its members. No separately deposited supplement/manual/protocol was
  listed. This is a record-inventory finding, not a claim about materials held
  elsewhere by the authors.
- **Linked official dataset publication:** neither inspected Z1 nor P1 lists a
  dataset-specific peer-reviewed version or DOI link. Searches of the exact
  dataset title and full author/title combination returned Z1/P1 and
  author-related but non-dataset-specific publications. Those publications
  were not used as evidence for this dataset.
- **Manufacturer manuals:** the full preprint names instruments, including Countstar BioTech and Hamilton probes. No manufacturer manual was used here. The published procedures do not supply per-row calibration certificates or a complete mapping of exported Status codes to feature-specific validity.

## Confirmed facts

1. **Dataset and design.** Z1 Description ¶1–2 identifies 24 CHO-K1
   cultivations, 12 experiments in parallel reactors, 0.55–0.8 L working
   volume, 161.5–328.5 h duration, 38 continuous inline variables and 10
   offline variables sampled up to twice daily. It says there are nine batch
   and three fed-batch experiments. P1 Abstract independently gives the
   24/12/duplicate design and the 38/10 counts.
2. **Raw and aligned representations.** Z1 Description ¶2–4 and Z2 confirm
   `Dataset.zip` contains 12 raw `.xlsx` workbooks and 48 aligned `.csv`
   files, arranged as one inline and one offline CSV per experiment/reactor.
   The raw workbook time axis starts at inoculation, defined as 0 h (Z1
   Description ¶3). This establishes an acquisition-axis origin only; it does
   not establish when an instrument result became available.
3. **Alignment statement, bounded.** Z1 Description ¶4 says sensor systems
   deviated slightly from nominal intervals, offsets accumulated, and *inline*
   signals were aligned to a common master time axis. The P1 method later
   specifies nearest-neighbor assignment within half a sampling interval and
   discarding points without a match from all streams. It still does not state
   result-availability timing, a master-stream identity, clock precision or
   tie ordering.
4. **Condition variation, bounded.** P1 Abstract says the experiments varied
   cultivation medium, agitation, aeration and process mode, and additionally
   inoculation cell density, glutamine concentration and impeller position.
   P1 Table 2 maps each EXP to process mode and TC-42/TCX6D medium; the
   transcription is retained in `preprint-table2-condition-map.csv`. It does
   not supply medium recipes, all starting glutamine values, feed composition,
   or a factorial-design allocation.
5. **Method and assay facts.** P1 Methods, printed pp. 2–5/10, reports TC-42
   (without growth factors) or TCX6D medium, and says the latter was
   supplemented with 8 mM L-glutamine. P1 says its Basic Feed contained 20
   g/L glucose and 22 mM L-glutamine. It identifies a Countstar BioTech
   (ALIT Biotech, Shanghai, P.R. China) for offline, trypan-blue, image-based cell analysis;
   technical triplicates were performed and averaged. It reports dilution with
   PBS when density exceeded the instrument's working range, but gives no
   numerical cell-assay detection/reporting limit, acceptance criterion, or
   formula defining the released SEM columns. P1 Table 3 names the VCD/TCD
   means and SEM fields, but does not state that a particular SEM is calculated
   from the reported triplicates.
6. **Offline concentration blanks.** P1 Usage Notes, printed p. 9/10, says
   that entries in the offline tables denote concentrations below the
   analytical detection or quantification limit (assay-dependent) and are
   non-quantifiable, rather than missing measurements. It gives neither a
   numerical limit nor an analyte-specific censoring/encoding rule. This is
   author evidence about the observed blank concentration entries; it does not
   explain any VCD zero. The preceding paragraph's qualified discussion of
   technical process gaps/MCAR does not override this explicit analytical-
   limit statement for offline concentration entries.
7. **Inline and process facts.** P1 Methods, printed pp. 3–6/10, identifies a
   DASGIP parallel bioreactor system and reports a two-point pH calibration
   (pH 7 and 4) and one-point dissolved-oxygen calibration (100% air
   saturation in medium) before each experiment. It says permittivity,
   turbidity and dissolved-CO2 sensor condition was monitored, but does not
   define all raw `Status` codes as an acceptance/rejection rule. It reports
   permittivity scans at the 18 released frequencies and a Cole-Cole fit from
   which `fc`, `DeltaEps`, `Alpha` and fitting error were calculated.
8. **Alignment and timing facts.** P1 Computational Processing, printed
   p. 6/10, says DASGIP Control was configured for 60-s recording and only
   stored values that differed from the preceding value; gaps therefore occur.
   It says missing values were forward-filled (last observation carried
   forward). For cross-sensor timing, it says all inline signals were aligned
   to a common master axis by nearest-neighbor assignment within half the
   sampling interval, discarding points without a valid match from all
   streams. This documents the export transformation, not sensor/assay result
   availability, wall-clock origin, or tie ordering. Critically, the original
   logged row time is not a fresh per-variable acquisition time after the
   documented carry-forward operation.
9. **Feed depends on offline assays.** P1 Methods, printed p. 4/10, says
   fed-batch feeding was initiated at 48 h and its exponential feed profile
   was updated after each sampling event using viable-cell number and an
   estimated glucose-consumption rate. Thus cumulative feed is not presently
   eligible as a point-in-time sensor input unless assay-result availability
   and control-update timing have been established.
10. **EXP011 R02.** P1 Technical Validation/Usage Notes, printed pp. 8–9/10,
   says EXP011 reactor 2 was contaminated, feed addition was discontinued,
   and it was excluded from the feed-assessment discussion. It does not give a
   separate author rule for the feed-stream endpoint, nor authorize treating
   the endpoint as process cessation.
11. **Six VCD zero contexts.** Five of the six source-recorded VCD zeros occur
   in EXP011 R02, for which P1 supplies contamination/feed-discontinuation
   context. It does not state that any individual zero is caused by that
   contamination or explain its measurement meaning. The remaining EXP002 R02
   late-batch zero has no comparable source explanation in P1.
12. **Archive observations requiring no biological inference.** The raw
   workbooks in retained Z1 contain the six VCD cells already enumerated in
   the decision packet as numeric `0` values (EXP002/R02 B16; EXP011/R02
   B14:B18). They are source values, not source explanations. The archive
   contains `Status` fields in some raw sensor worksheets and no universal
   status field in all sheets; labels/absence are data facts, not a documented
   validity or calibration rule.
13. **Reuse terms.** P1's landing-page copyright notice says the *preprint* is
   CC BY 4.0. Z1's **Rights → License** field is blank. Therefore CC BY 4.0 is
   confirmed for P1, but no dataset reuse license can be assigned from Z1.

## Question-by-question closure status

| Requested question | Evidence outcome | Safe disposition |
| --- | --- | --- |
| Cell assay instrument/SOP | P1 pp. 4–5/10: Countstar BioTech (ALIT Biotech), trypan-blue, image-based analysis; technical triplicates averaged; PBS dilution beyond stated working range | Instrument/SOP facts are **confirmed**. Instrument configuration, QC criteria and numerical working range remain **unresolved**. |
| Replicates and SEM definition | P1 p. 5/10: technical triplicates performed and averaged; Table 3 supplies SEM columns without formula | **Partly confirmed.** Do not equate an SEM field with a particular triplicate calculation, SD, CI or acceptance criterion without clarification. |
| Detection/reporting limits, rounding, QC | P1 p. 9/10 says offline concentration entries can be below assay-dependent detection/quantification limits; no numeric limits; P1 pp. 4–5/10 gives some dilution/sample steps | **Partly confirmed.** No numerical censoring or rounding rule may be imputed. |
| Six numeric VCD zeros | Raw values confirmed; no source explanation | **Unresolved.** They cannot be classified as true absence, below limit, missingness, or zero uncertainty. |
| Medium name, initial glutamine, experiment map | P1 pp. 2–4/10 + Table 2 name TC-42/TCX6D; reports TCX6D 8 mM L-glutamine and a Table 2 footnote for 6 mM L-glutamine; Table 2 maps EXP to medium but marker scope is now verified against Table 2 and Figure 1 | **Partly confirmed.** Keep the cited Table 2 map; named medium and reported supplement assignments are now mapped; full underlying recipes and unreported minor components remain unresolved. |
| Sensor model, calibration, channel/fitting meaning | P1 pp. 5–6/10 identifies instruments/configuration, pH/DO calibrations and Cole-Cole derived fields/frequencies | **Partly confirmed.** Do not extend these facts to unreported calibration parameters, all channel units, or biological validity. |
| `Status` semantics | P1 p. 8/10 describes warning occurrence/monitoring; no field-by-field semantics or decision rule | **Unresolved.** `Ok`, warning, blank and absent must remain distinct provenance states, not validity claims. |
| Acquisition versus availability clocks | Inoculation is raw time zero; P1 documents change-only logging/LOCF and assay-updated feed, but no measurement/result/control-update availability times | **Unresolved.** Raw/aligned timestamps do not establish strict real-time availability or fresh per-variable acquisition. |
| Alignment algorithm | P1 p. 6/10: forward-fill of logged gaps; nearest-neighbor assignment to a common master axis within half a sampling interval; no-valid-match points discarded | **Confirmed for the supplied aligned export.** The source does not constrain nearest neighbor to the past, so aligned values must not establish a causal/past-only cutoff. Availability, exact clock transformations/tie handling and deployment use remain unresolved. |
| EXP011 R02 feed cutoff | P1 pp. 8–9/10: contamination and feed discontinuation; local endpoint remains a separate observed fact | **Context confirmed.** Do not infer a broader process/sensor termination or unreported remediation chronology. |
| EXP004 duplicate timestamps | Observable source collision; no documented resolution rule | **Unresolved.** Preserve/reject ambiguous candidates under the project policy; do not deduplicate as an author-approved action. |
| File inventory / license | One `Dataset.zip`, verified hash; no Z1 license | Archive inventory is **confirmed**; dataset redistribution/reuse rights remain **unresolved**. |

## Defensible inferences (explicitly limited)

- P1 Table 2 supports assigning the named medium (TC-42 or TCX6D) and process
  mode to an EXP, as recorded in `preprint-table2-condition-map.csv`. It does
  not support assigning a complete recipe, every glutamine level, causal
  effect, or feed recipe to a particular EXP/R reactor.
- Because Z1 says the common-master operation was applied to **inline**
  signals, it is defensible to distinguish publisher-aligned inline exports
  from original raw streams. It is not defensible to treat an aligned value as
  source-exact raw evidence, an assay-result time, or a causal observation.
- Because P1's CC BY statement is attached to the preprint page while Z1 has
  an empty license field, it is defensible to keep local research use and
  citation separate from data redistribution rights.

## Author questions needed for scientific closure

1. Provide any undeposited supplement and complete underlying medium recipes.
2. State the formula/linkage of each released SEM field to the technical
   replicates, numerical detection/quantification limits by analyte, rounding,
   QC acceptance criteria and the disposition of all six VCD zeros.
3. Provide per-row/per-run calibration, maintenance and QC records and define
   `Ok`, `Warning Active`, blank and absent `Status` for each stream.
4. Document measurement, logging, result-availability and control-update
   clocks; master-axis identity; timestamp precision/tie handling; and a
   prescribed EXP004 duplicate resolution.
5. State the license/terms for `Dataset.zip` and any required attribution or
   redistribution limits.

## Non-closure statement

This evidence does not approve a target mask, feature family, status rule,
freshness cutoff, split, model fit, performance claim, or scientific validity
of a soft sensor. Those decisions remain with the owner and require the missing
scientific evidence above.

### Capture-format note

The retained viewer captures have `.png` filenames but their payloads are JPEG.
`SHA256SUMS.txt` fingerprints the actual captured bytes; no original-PDF hash is
claimed. This filename mismatch changes neither the visible page evidence nor
the separately preserved original dataset.

### Table 2 footnote closure

Direct visual inspection of Table 2 (viewer05/printed4), aided by a nearest-neighbor
magnified crop of the unchanged screenshot, resolves markers: EXP006(a), EXP007(b),
EXP009(c), EXP011(c). Marker(a) specifies inoculum6×10^5cells/mL versus the reported
default4×10^5; (b) specifies6mM glutamine supplement versus the reported default8mM;
(c) specifies the lower impeller. Figure1/Methods (viewer06/printed5) reports a
20mm impeller-to-sensing distance reduced to6mm in EXP009/EXP011. The condition CSV
now records these reported conditions. An independent reviewer checked the same
primary images; agreement is not biological validation. Full medium recipes and
case-level QC remain distinct unknowns.
