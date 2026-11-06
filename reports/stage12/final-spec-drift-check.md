# Final specification drift check

> Current correction release: **v6**. The initial v5 assessment below is historical; the dated correction close-out records current verification and deferred work.

Final engineering artifact: **data/processed/v5**, manifest SHA-256
`411f451675c7986caa43f06826cbda3bb22b9600b839a582bb32aa42c30d035e`.
The execution specification remains unchanged from the bytes captured in the v5
producer snapshot. This disposition is an explicit addendum, not a rewrite of the
historical execution record.

| Specification area | Final evidence and disposition |
| --- | --- |
| Preserved originals, source/backup, null/zero distinctions | Raw and backup SHA-256 match; v5 has 378 assays, six recorded numeric zeros, 214 original blanks and 6,804 physical source-cell records. All 6,590 populated source values and 214 blanks agree exactly with decisions. Passed. |
| Acquisition/availability and independent quality flags | 15,120 same-reactor past-only snapshots; absent/blank/non-Ok Status distinct; strict availability unknown and unsupported. Actual 1/5/15-minute sample effects and all 144 raw-stream cadence/source collisions retained. Passed for retrospective engineering scenario; scientific assumptions unapproved. |
| Units/fields/inference | Forty distinct sensor field IDs retain 960 source/sheet eligibility mappings, all approvals false; frequency qualifiers are distinct from unverified units. All offline assays/SEMs forbidden inputs and IDs/mode/time context only. Passed as proposed contracts, not accepted scientific features. |
| Target-blind paired splits and evaluation | EXP004/EXP010 proposal uses exact minimum-reactor five-core coverage fractions (15/16 and 22/23), all assay cutoffs as denominator, no target values. Ten outer grouped development folds with inner memberships; fixed sensitivities, prior global EDA and favorable-support limitations recorded. No fitting or performance results. Passed as unapproved protocol. |
| Reproduction and atomic promotion | All 27 consumed inputs, 25 payload digests, 11 CSV/SQLite tables and producer snapshots verified. Thirty-seven software tests passed, including synthetic repeatability and injected validation failure without promotion. Extra individual mid-run backup/config/producer mutation injections deferred and explicitly not claimed executed. |
| Reviews and gates | Five separate fresh pre-review lenses and five new fresh post-review lenses saved. Engineering findings resolved/dispositioned; eight owner/scientific questions retained. G1/G2/G3, M1/M2, CG1, target/feature/split approval and model fitting remain open/false. |

**Accepted version change (POST-REQ-01).** The specification planned a v4 output.
V4 was produced and retained, but its postreview exposed CSV-parser precision drift
in 701 numeric source/decision pairs, including one VCD. Corrected v5 reconstructs
original values from raw source cells and verifies exact agreement; it supersedes
v4 as the current protocol bundle. This change strengthens original-preservation
requirements without changing target masks, coverage counts or split IDs. V4,
v3 and failed named `.incomplete` directories remain preserved; none is silently
promoted as scientific acceptance.

**Boundary.** No unrecorded scope expansion or unresolved implementation defect was
found in the final review scope. Full raw-to-aligned export semantics, assay SOP/QC,
units/calibration, result timing, scientific acceptance and later characterization/
model/component releases remain unresolved or deferred exactly as recorded.
Agent agreement is engineering review evidence and supplies no assay validity.


## Correction close-out — 2026-11-05

Current released engineering bundle: **v6**, manifest SHA-256
`d74465cbb353af872681cf3c6bbd1055ee0523441a889ec90832d7fc3affa45e`.
The v5 analysis above is historical. V6 adds source-schema enforcement and inventory;
its original assay-source table is byte-identical to v5. Original archives, backups,
historical producers and the original execution specification remain preserved.
The handoff correction matrix is the supplemental specification for this bounded
change, not a retrospective rewrite of the historical execution specification.

Two fresh review records are saved in `reviews/handoff-code-review.md` and
`reviews/handoff-packet-review.md`. Configured delegated models were
`gpt-5.6-terra`, medium reasoning; the engineering reviewer could self-identify only
as GPT-5, so backend self-identification is not claimed. Coordinator backend model
accounting is not exposed. Agent agreement supplies no scientific validity.

Verification: the full prior suite passed 38/38; the focused Stage12 suite passed
12/12 after additional missing/unexpected-sheet cases; the supplemental released-
bundle suite passed 5/5. These are separate runs, not a claimed new combined full-
suite count. The manifest-bound released-data check found **zero identity mismatches
in 15,120 lineage rows linked to 378 unique assays** and rejects deliberate reactor,
experiment and source crossings, duplicate identities, offline predictors and a
wrong manifest. See `released-isolation-verification.json`. V6 was not rebuilt.

Accepted review gaps are resolved. Three engineering follow-ups remain explicitly
deferred: a fully unmocked synthetic full-build schema fixture, pandas null-
normalization for future compatibility (current pinned verification passes with
FutureWarnings), and per-family raw-header rejection contracts beyond the recorded
headers of this checksum-pinned archive. See `resolution_register.json`. The usage
guard stopped broader work; no quota reset was consumed. No unresolved observation
was converted into scientific approval, and all fitting gates remain false.
