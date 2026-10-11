# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### Agent Skills project: "Optimizing skill descriptions"

- Source: <https://agentskills.io/skill-creation/optimizing-descriptions>, from
  <https://github.com/agentskills/agentskills>, `docs/skill-creation/optimizing-descriptions.mdx`
- License: `CC-BY-4.0`
- Version: `b8d2613ac050aa4aa8bfb2cf28380d81cdfcd1ca`

The guide supplied the method of realistic positive and near-miss queries, held-out validation, and measured trigger
rates in an optional client-specific evaluation. The skill links to the live guide for procedural detail, and no prose
was copied.

## Third-party Sources

### mizchi: `optimizing-descriptions` skill

- Source: <https://github.com/mizchi/skills>, `optimizing-descriptions/SKILL.md`
- License: `MIT`
- Version: `a41865b34b78f2675a6c73178377a5bcc1b492c6`

The skill supplied the separate question of automatic versus deliberate invocation, focused description-only audits,
and close false-trigger cases. This skill treats invocation and portability as independent decisions, and nothing was
copied.

### Anthropic: `skill-creator` plugin

- Source: <https://github.com/anthropics/claude-plugins-official>, `plugins/skill-creator/skills/skill-creator/`
- License: `Apache-2.0`
- Version: `fa59bc9037741ecfa131aa27938272605710d7b2`

The plugin supplied the quality bar for trigger queries: concrete, substantive positives, near-miss negatives, repeated
runs per query against a threshold, and held-out scores kept from the writer of the next description. The wording is
independently written, and nothing was copied.

### Jesse Vincent: superpowers `writing-skills` skill

- Source: <https://github.com/obra/superpowers>, `skills/writing-skills/SKILL.md`
- License: `MIT`
- Version: `8ca22dba9a94f28898bbce59f2537ff4d87c747d`

The skill supplied the rule of keeping a workflow summary out of a description, because an agent may follow the summary
instead of the body. Nothing was copied.
