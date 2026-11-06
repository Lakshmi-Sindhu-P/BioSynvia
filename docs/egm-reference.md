# Elephant Goldfish plugin reference

Saved November 5, 2026 as a private personal plugin:
[Elephant-Goldfish Model](https://chatgpt.com/plugins/plugins_6aecfe9cbaa4819193a512608e93437b).

This is a private packaged copy of Google's Apache-2.0 upstream EGM runtime,
pinned to commit `ccf79c5c0fb5df7815685d5e4994fd9aad8954bd` from
https://github.com/google/elephant-goldfish-model . It is not an officially
supported Google product. The upstream instructions, personas, standards and
license are preserved. Local adaptations are recorded in the package's
`UPSTREAM_SOURCE.json`; only the portable manifest schema declaration was added.

## Available workflows

- egm-brainstorm: explore a proposed change and its assumptions.
- egm-draft: draft the specification.
- egm-review: conduct the staged fresh-context design review.
- egm-review-loop: run a configured review task.
- egm-resolve: work through review findings.
- egm-bootstrap: create/update documentation for an existing codebase.
- egm-drift-report: compare documented behavior with implementation.

All seven skills, nine reviewer/orchestrator personas and shared document standards
were verified in the saved account package. The local archive is
`integrations/egm-private.zip`; the runtime is `integrations/egm`. Exact plugin,
release and archive identifiers are in `integrations/egm-registration.json`.

## Global availability verified November 5, 2026

The official upstream plugin is installed and enabled in the personal Codex
configuration as `egm@egm`, version `0.1.0`, pinned to the same source commit.
Its runtime is `/Users/sindhu/.codex/plugins/cache/egm/egm/0.1.0`, independent
of BioSynvia. A plugin listing run from `/private/tmp` confirmed it is installed
and enabled. All seven skills and installed source files match the pinned upstream
(excluding Git internal metadata). Evidence is saved in
`integrations/egm-global-installation.json`. This is personal availability across
projects; the existing private account package is unchanged.

## Future use

Select the saved plugin in a future chat and name the task, document path and
desired workflow. For example: use EGM to review the saved specification with a
consolidated report. The host may need a new chat to load the saved skills.
No new chat was created automatically by this installation task.

The skills use the host's models, tools and permissions. A review requires actual
fresh-context subagents; it must not be simulated in the coordinator's existing
context. Parent-turn isolation does not prove exclusion of host instruction files.
Reviews do not replace tests, scientific evidence or authorized human decisions.
The package does not deploy a server, add a separate model API or enforce quotas.

## BioSynvia operating preferences

These project preferences are separate from the unchanged upstream plugin:

- Apply the Karpathy guidelines to engineering changes.
- Use the 5.6 family for implementation/code writing when available; verify actual
  runtime availability and disclose a mismatch instead of silently escalating.
- Use Luna for bounded extraction and Terra for scoped reporting. Do not use Luna
  to approve scientific interpretations.
- Follow the latest handoff policy: use 5.6-class models for ordinary coding and
  review; use 6/6.1 only for a concrete high-impact conflict or scientific-review
  need. Record actual model, reasoning level and role for substantial work.
- Monitor both five-hour and weekly limits where telemetry is available. Retain
  the requested weekly reserve and leave five-hour headroom for verification and
  handoff; do not assume a lower-priced model consumes a particular quota amount.
- Keep source data, model approval gates and uncertainties intact. The current
  BioSynvia pre-modeling packet remains the authority for unresolved decisions.

The native Stage 1/2 workflow previously completed in this project is recorded
under `reports/stage12`; installing this plugin does not rerun or retrospectively
certify those reviews. Future upstream updates require an explicit source/package
update and reuse of the saved plugin ID, not creation of duplicate plugins.
