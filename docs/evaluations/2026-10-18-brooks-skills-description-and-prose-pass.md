# Evaluation: Brooks Skills Description and Prose Pass

Date: 2026-10-18. A review-lite pass with skill-forge's review mode over the six skills vendored from
brooks-lint: `brooks-audit`, `brooks-debt`, `brooks-health`, `brooks-review`, `brooks-sweep`, and `brooks-test`.
It covers the description pass and the prose pass that the backlog ledger tracks.

## Verdict

All six are `ready with risks`. No model ran, so triggering and execution were not measured. Both passes are
recorded as no change, because the skills are vendored: editing their content would make every upstream sync
conflict, as with `cc-safety-net`.

## Source

- Repository: <https://github.com/hyhmrright/brooks-lint>, vendored at commit
  `29fd7761cdb59a1bd9d2b5b6458277807c674c4f`
- License: MIT. The vendored `LICENSE.upstream` is byte-identical to the upstream file at that commit.
- Upstream head when reviewed: `c85f65eada5c56721275ef89e2dd41ac453dcba2`, 42 commits ahead of the pin.

## Evidence

Both validators pass for all six packages: the Agent Skills specification check and the skill-forge policy
check, run separately (executable check).

A word-level diff of every vendored file against the pinned upstream file shows only packaging and formatting
changes (executable check). The packaging changes are an inline `description`, added `license` and
`metadata.author` fields, and `../_shared/` paths rewritten to `references/`. The formatting changes come from
this repository's Markdown formatter: padded tables, blank lines before lists, and normalized list indentation
that renders the same. The six copies of the shared reference files are identical to each other.

## Findings

- **Provenance, fixed.** The attributions said the files were adapted only for the flat layout and omitted the
  formatter changes. Each `ATTRIBUTIONS.md` now names them (`f925aa52`, `e3c48194`, `042f69b7`, `b465472d`,
  `81f027d9`, `f23636e6`).
- **Description budget, accepted.** The descriptions run from 640 to 923 characters, over the repository's
  512-character warning threshold but within the 1,024-character specification cap. They stay as vendored.
- **Routing overlap, accepted as a risk.** The `brooks-review` description claims general requests to review
  code or check a pull request, which the author's code-review skill and reviewer agents also serve. A plain
  review request may load it alongside them. If that proves unwanted, the installing configuration decides what
  loads where.
- **Upstream changes, not synced.** Since the pin, upstream changed the skill files to accept configuration
  supplied by a CI runner and added an opencode slash-command metadata key. Neither changes behavior for this
  repository's use.

## Limits

The books' claims behind the guidance were not checked against the books, because the skills cite no primary
source per rule. Triggering was not measured on any client.
