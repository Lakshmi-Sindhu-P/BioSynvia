# Goldfish review — scientific-evidence approval packet

**Reviewer/model:** `gpt-5.6-terra`, medium reasoning  
**Date:** 2026-11-05  
**Scope:** independent, read-only scientific-evidence review of
`approval-packet.md`; no fitting, configuration, dataset, or frozen-v6 edit.

## Disposition

**No scientific approval is issued by this review.** The packet is materially
faithful to the bounded source record and correctly leaves fitting paused pending
owner approval of D1–D9. It may be used as the requested concise *owner decision
packet*, subject to the two clarifications below. It must not be read as assay,
biology, real-time, causal, intervention, or digital-twin approval.

## Verified strengths

- The fact/inference/owner-decision/author-question separation is generally
  sound. In particular, no source is used to declare a VCD zero biological,
  correct a label, certify a row, or validate an eventual twin.
- The retained primary evidence is accurately described as ten browser-viewer
  captures, not a complete-PDF artifact or PDF hash. `SHA256SUMS.txt` contains
  hashes for `preprint-viewer-page02.png`–`...page11.png`; despite their `.png`
  names, `file` identifies the checked images as JPEG payloads. This is a
  naming/provenance detail, not fake-PDF evidence.
- Viewer page 05 / printed p. 4 Table 2 directly supports the transcription:
  EXP008 is Batch/TCX6D and EXP010 is Fed-Batch/TC-42. Thus the proposed
  EXP008+EXP010 reserve covers both named media and both modes; the packet
  correctly says it is unapproved and not a performance-selected split.
- Viewer page 05 / printed p. 4–5 supports Countstar, trypan-blue/image
  analysis and averaged technical triplicates. It does **not** supply the
  released-SEM formula, independent-biological-replicate evidence, assay limit,
  or case-level QC. The packet preserves that distinction.
- Viewer page 07 / printed p. 6 states change-only process logging and
  forward-fill, plus nearest-neighbour alignment within half a sampling interval.
  The packet correctly treats row time as process-state age rather than fresh
  measurement age, and does not claim the neighbour is past-only.
- Viewer pages 09–10 / printed pp. 8–9 support EXP011 R02 contamination,
  antibiotics in both reactors, and R02 oxygen-enrichment/feed termination at
  about 67 h; they do not explain each of the five zeros. The sixth, EXP002 R02,
  remains separately unexplained. `zero-case-support.csv` retains all six rather
  than double-subtracting the five EXP011 cases.
- Viewer page 10 / printed p. 9 supports the qualified below-LOD/LOQ treatment
  for offline concentration entries but gives no numeric bounds. The packet does
  not turn these blanks into zeros or assume MCAR. It also correctly withholds
  feed because the reported feed update uses viable-cell number and estimated
  glucose consumption.
- Counts agree with the cited frozen decision artifacts: whole-EXP011 quarantine
  at 5 min is 343 nominal positive / 308 supported positive; R02-only is
  360/322; retain-all is 372/333. The strict eight-channel status option is 0.
  The forecast 12-h value is correctly labelled a 315-positive-label **ceiling**
  under whole-EXP011 quarantine, not implemented re-anchored support. The split
  file gives 234/74 for EXP008+EXP010 and 233/75 for old EXP004+EXP010.

## Required owner clarifications before authorizing fitting

1. **Define the zero “challenge prediction” protocol.** D1 says every zero gets
   an experiment-held-out challenge prediction, while D2 excludes all EXP011
   from primary fitting and D6 reserves EXP008+EXP010. The packet should state
   explicitly whether challenge predictions are separate leave-one-experiment-out
   sensitivity fits, and which approved training groups are allowed for EXP002
   R02 and EXP011 R02. Otherwise “challenge prediction” can be mistaken for a
   result from the primary fit or for evidence that the zero is a valid target.

2. **Make the split an explicit freeze gate.** D6 appropriately says “propose”
   and that v6 is unchanged, but it should state that neither 234/74 nor the
   EXP008+EXP010 reserve becomes operative until the owner selects it and an
   immutable fitting protocol records it. This matters because previous global
   EDA already precludes an untouched-external-test interpretation.

## Non-blocking precision edits

- In D2, call the event “oxygen-enrichment termination” rather than an “oxygen
  interruption” unless a sensor/control interruption is independently evidenced;
  viewer page 09 describes a deliberate termination.
- In D4/D5, retain the phrase “acquisition-as-availability assumption” in every
  later estimate/forecast deliverable. The 1/5/15-min figures are retrospective
  source-row eligibility only; they do not validate process-state freshness,
  assay latency, or real-time availability.

## Evidence inspected

`source-evidence.md`; `supporting-publications.md`; viewer captures 05, 06, 07,
09 and 10 (with the ten-image manifest); `preprint-table2-condition-map.csv`;
`decision-counts.json`; `split-options.json`; `zero-case-support.csv`; and the
standard-library-only `scripts/summarize_scientific_decision_counts.py`. The
count script was inspected but not run because its fixed output paths would
overwrite the frozen decision-support artifacts.

## Follow-up recheck — 2026-11-05

The two required clarifications are now resolved in the updated packet.

- The challenge protocol is concrete and non-circular: EXP002 R02 is predicted
  only by its outer experiment-held-out fit, trained/tuned on the other eight
  development experiments; EXP011's five cases are scored by the frozen
  nine-development-experiment model with EXP011 unseen. The packet excludes
  reserved EXP008/EXP010 labels and all uncertain-zero labels from selection,
  and says the reported cases cannot rank models as truth. Its 309
  clean-cohort include-EXP002-zero sensitivity and distinct 339 broad
  include-all-zero/EXP011-override sensitivity are correctly distinguished.
- The split is now a genuine owner-selection/immutable-protocol gate: cohort,
  fingerprints, feature/timing policy, split IDs and evaluation rules must be
  frozen before fitting; challenge results cannot retune it. This resolves the
  prior ambiguity.

I also independently inspected the supplied local reading aid
`tmp/pdfs/preprint-table2-reading.png`, a 4× nearest-neighbour enlargement of
the retained viewer-page-05 crop, against the unchanged original page 05 and
Figure 1/caption on viewer page 06 (printed p. 5). The readable Table 2 markers
are EXP006^a, EXP007^b, EXP009^c and EXP011^c. The footnote assigns **a** to
inoculation density of 6×10^5 viable cells/mL, **b** to 6 mM L-glutamine, and
**c** to the lower bottom-impeller position. Figure 1's caption independently
states that EXP009 and EXP011 use the modified 6-mm lower-impeller distance
(versus 20 mm elsewhere), corroborating **c**. This closes those four marker
assignments only; it does not establish complete medium recipes, all other
condition details, or causal effects.

The source register's revised manufacturer paragraph properly names the
published instruments while continuing to state that no generic manufacturer
manual was used and that no per-row certification/Status mapping follows.
One non-blocking wording issue remains in the D2 table: replace “Known oxygen
interruptions” with “known oxygen-enrichment termination” for consistency with
the source and the packet's corrected confirmed-fact row.
