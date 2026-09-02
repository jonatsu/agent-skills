# Attributions

## Current skill

- Skill: `skill-review`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and substantially rewritten

## Original author and source

- Original author: Leonardo Flores
- Copyright holder: `Copyright (c) 2026 Leonardo Flores`, as stated in upstream's `LICENSE`
- Upstream project: [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)
- Source path: `skills/skill-judge`
- Exact source revision: unknown. The initial local attribution in commit `165701f` recorded the upstream
  project, skill path, and MIT license but did not record a commit or tag.
- Later comparison snapshot: `3027f20f3181758385a1bb8c022d4041dfb4de84`, upstream HEAD as observed on
  2026-08-27. It predates the local addition and provides an auditable comparison point; it does not establish
  which revision was originally adapted.

## Adaptation note

Retained the upstream skill's purpose and its concern for actionable review, progressive disclosure, workflow
fit, and concrete evidence. Replaced its fixed structural rubric with a contract-based review that separates
validity, design judgment, and behavioral evidence.

Material changes from the upstream skill:

- Cut the ~40-line philosophy preamble ("what is a Skill", training-cost tables, hot-swappable-LoRA analogy)
  as material the model already holds. Replaced with a two-line statement of intent. This originally
  cross-referenced a sibling skill for vocabulary; those pointers were removed on 2026-08-27, because that
  skill sets `disable-model-invocation: true` and so cannot be reached from here. Every term is now defined in
  place.
- Removed the ASCII-art boxes (activation-flow diagram, quick-check panel), folding their content into tables
  and prose.
- Neutralized provider-specific framing ("Claude" → "the agent/model") so the skill is agent-agnostic.
- Consolidated the useful failure-pattern diagnoses into `references/review-lenses.md`, expressed as
  consequence-based questions rather than score deductions.
- Rewrote frontmatter to the Agent Skills specification's top-level `license` field and retained
  `metadata.author`.
- Retained Expert/Activation/Recoverable/Redundant as qualitative diagnoses, cross-file consistency checks,
  freedom calibration, the acts-now/acts-safely/still-works questions, evidence legibility, and the detailed
  portability distinctions.
- Removed the eight-dimension 120-point grade, line-weighted knowledge ratios, structural quotas, portability
  score caps, and mandatory praise. These measures conflicted with the current `skill-forge` contract by
  rewarding techniques that authoring now treats as conditional.
- Added separate hard gates, consequence-based findings, readiness verdicts, proportional behavioral
  evaluation, and decision-specific metrics.

## Upstream license

MIT. The verbatim upstream `LICENSE` ships beside this file as `LICENSE.upstream` and MUST travel with the
skill when it is redistributed or re-deployed. Upstream publishes no `NOTICE` file, so there is no
`NOTICE.upstream`.

The licence text was previously inlined here **without its copyright line**, which made it neither a verbatim
reproduction nor compliant with MIT's own requirement that the copyright notice travel with the software.
Replaced on 2026-08-27 with the byte-for-byte file.

Verified against the primary source on 2026-08-27 — `gh api repos/softaworks/agent-toolkit/license` reported
`MIT`, and the `LICENSE` blob itself was fetched and copied byte-for-byte. `gh repo view --json licenseInfo`
was NOT used; it misreports repositories that do carry a licence.
