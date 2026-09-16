# Attributions

## Current Skill

- Skill: `handoff`
- Current author: Joonas Onatsu
- Current license: MIT, unchanged from upstream
- Status: adapted from upstream and substantially rewritten

## Original Author and Source

- Original author: Matt Pocock ([@mattpocock](https://github.com/mattpocock))
- Copyright holder: `Copyright (c) 2026 Matt Pocock`, as stated in the upstream `LICENSE`
- Upstream project: [mattpocock/skills](https://github.com/mattpocock/skills)
- Source path: `skills/productivity/handoff/SKILL.md`
- Source commit: `d28dfdc39beadc3142a33359b5cfa4765dcbd0bc` (2026-08-15)
- Upstream license: MIT

## Adaptation

Upstream supplied the core no-duplication discipline, redaction rule, and temporary save-location guidance.

The current skill adds:

- pointer and stateful handoff branches so routine transfers remain short;
- a mandatory scan for undocumented preferences, agreements, nuances, rejected approaches, scope, and
  unfinished reasoning;
- paste-ready `PRIME` and saved `DOCUMENT` delivery modes;
- verification requirements for factual state included in a handoff;
- conditional sections for complex work without imposing a fixed template;
- an ephemerality guardrail requiring durable knowledge to reach a version-controlled artifact before the
  handoff, rather than surviving only in a gitignored note or prompt;
- a default refusal to emit oversized `PRIME` prompts that a terminal can silently corrupt on paste; and
- explicit carry-forward of standing session-start operating instructions.

The repository owner's session-priming workflow informed these additions. A successful multi-item priming
brief supplied the initial stateful shape, and later routine skill-review handoffs exposed the need for a
separate pointer form.

## Related Work Not Used as the Base

The `handoff-engineering` skill in `alirezarezvani/claude-skills` is an intermediate MIT-licensed derivative
of Matt Pocock's skill. It was evaluated but was not used as the base because its recommender hardcodes skills
from its own publisher's repository. Two ideas were evaluated. Scaling length to the work was adopted
independently and remains credited here. Avoiding handoffs that merely summarize an earlier handoff was not
carried into this skill.

## Upstream License

The upstream source is used under the MIT License. The verbatim license text ships as `LICENSE.upstream`;
preserve it and this attribution file when redistributing the skill.

The license and copyright holder were verified against the pinned source on 2026-09-02 with
`gh api repos/mattpocock/skills/contents/LICENSE?ref=d28dfdc39beadc3142a33359b5cfa4765dcbd0bc`. The upstream
repository root at that revision contains no `NOTICE` file.
