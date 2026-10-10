# Attributions

## Current skill

- Skill: `writing-skill-descriptions`, named `optimizing-descriptions` until 2026-09-28 and
  `skill-descriptions-and-triggers` until 2026-10-04
- Author: Joonas Onatsu
- License: MIT
- Expression: independently written. No external prose, examples, code, or assets were copied or adapted.

## skill-forge's description guide

- Source: `skill-forge/references/description-guide.md`, same author and license (MIT).
- Absorbed 2026-09-28, when this skill became the single owner of description work: the drafting steps, the
  PDF and Just examples, the form and length rules, and the review checks. That guide drew on the Agent Skills
  pages credited in skill-forge's `ATTRIBUTIONS.md` and on the mizchi skill below.

## mizchi's optimizing-descriptions skill

- Author: mizchi
- Source: [`optimizing-descriptions/SKILL.md`](https://github.com/mizchi/skills/blob/a41865b34b78f2675a6c73178377a5bcc1b492c6/optimizing-descriptions/SKILL.md)
- Revision: `a41865b34b78f2675a6c73178377a5bcc1b492c6`
- License status: the pinned repository README says skills without an individual license default to MIT at
  the owner's discretion; this source has no top-level license field or bundled `LICENSE.txt`.
- Influence: the separate question of automatic versus deliberate invocation, focused description-only
  audits, and close false-trigger cases. This skill treats invocation and portability as independent decisions
  and does not use mizchi's client tools, deployment process, or wording templates.

## Agent Skills documentation

- Source: [Optimizing skill descriptions](https://github.com/agentskills/agentskills/blob/b8d2613ac050aa4aa8bfb2cf28380d81cdfcd1ca/docs/skill-creation/optimizing-descriptions.mdx)
- Revision: `b8d2613ac050aa4aa8bfb2cf28380d81cdfcd1ca`
- License: CC BY 4.0, from the repository's `docs/LICENSE` at that revision.
- Influence: realistic positive and near-miss queries, held-out validation, and measured trigger rates in an
  optional client-specific evaluation. The skill links to the live guide for procedural detail.

## Skill-creator comparison ideas (2026-09-28)

Adopted from the comparison in this repository's
`docs/research/skill-authoring-sources/skill-creator-comparison.md`. The wording is independently written; no
prose, code, examples, or prompts were copied or adapted.

- **Anthropic skill-creator plugin**:
  [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official), path
  `plugins/skill-creator/skills/skill-creator/` (`SKILL.md`, `scripts/run_eval.py`, `scripts/run_loop.py`),
  commit `fa59bc9037741ecfa131aa27938272605710d7b2`, Apache-2.0. Influence: the quality bar for trigger
  queries (concrete, substantive positives; near-miss negatives; trivial one-step requests make poor
  positives), repeated runs per query against a threshold, and keeping held-out scores away from the writer of
  the next description. Its `claude -p` harness and stub-command installation are excluded.
- **obra/superpowers writing-skills**: [obra/superpowers](https://github.com/obra/superpowers), path
  `skills/writing-skills/SKILL.md`, commit `8ca22dba9a94f28898bbce59f2537ff4d87c747d`, MIT
  (`Copyright (c) 2025 Jesse Vincent`). Influence: keeping a workflow summary out of the description because an
  agent may follow the summary instead of the body. This skill keeps the capability statement that superpowers
  omits.
