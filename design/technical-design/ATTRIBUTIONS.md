# Attributions

## Current Skill

- Skill: `technical-design`
- Current author: Joonas Onatsu
- Current package license: MIT AND CC-BY-SA-4.0
- MIT: independently authored workflow in `SKILL.md` and evaluation cases.
- CC-BY-SA-4.0: `assets/arc42-design-template.md`, `references/arc42-writing-guide.md`, and
  `references/arc42-example.md`.
- Status: original workflow with attributed influences and adapted arc42 resources

## arc42

- Original authors: Gernot Starke and Peter Hruschka
- Template source:
  [English template](https://github.com/arc42/arc42-template/tree/8dff0d9b1f9640684df8c3bbcdc2ee45f989ca0f/EN)
- Template revision: `8dff0d9b1f9640684df8c3bbcdc2ee45f989ca0f`, inspected 2026-09-14
- Documentation source:
  [docs.arc42.org](https://github.com/arc42/docs.arc42.org-site/tree/e8f892861345170beb04d1929b2a3ec7692960be)
- Documentation revision: `e8f892861345170beb04d1929b2a3ec7692960be`
- Tailoring source:
  [FAQ](https://github.com/arc42/faq.arc42.org-site/tree/2941af019bc2d4ea51db3a6ea9e3ac27cbab46d7)
- FAQ revision: `2941af019bc2d4ea51db3a6ea9e3ac27cbab46d7`
- Example source:
  [examples.arc42.org](https://github.com/arc42/examples.arc42.org-site/tree/567ba486db4dc5f10f90996e19c5b9b41d225670)
- Examples revision: `567ba486db4dc5f10f90996e19c5b9b41d225670`
- Source license: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- Upstream license statement: [LICENSE.upstream](LICENSE.upstream), copied from the pinned template revision
- Relationship: adapted template and section guidance; original fictional example within that structure

The template preserves arc42's twelve-section organization with condensed Markdown prompts, a design-basis
preamble, and a planning handoff. The guide adapts the section purposes and advice about depth, responsibilities,
runtime scenarios, rationale and avoiding duplication. The specific online guidance used is linked in that guide.
These resources and the worked example are distributed under CC BY-SA 4.0. No upstream example prose, diagrams,
code or system requirements are copied into the fictional catalog design.

The workflow's repository-convention exception and its requirements/design/planning authority boundaries are
independently expressed local guidance. The mixed package license identifies distinct resources; it does not
relicense historical MIT workflow material. Architecture content users write remains their own, as explained
in [arc42's license guidance](https://arc42.org/license/).

## Superpowers Design and Planning Sources

- Original author: Jesse Vincent
- Upstream project: [obra/superpowers](https://github.com/obra/superpowers)
- Source paths:
  [`skills/writing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md),
  [`docs/plans/2025-11-22-opencode-support-design.md`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/docs/plans/2025-11-22-opencode-support-design.md),
  and the paired
  [`implementation plan`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/docs/plans/2025-11-22-opencode-support-implementation.md)
- Source revision: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`, inspected 2026-09-04
- Source license: MIT
- Relationship: idea-level influence, independently expressed

The source pair demonstrated the reader value of separate design and implementation-plan artifacts. Its boundary leaks
also informed this skill's prohibition on task sequencing and its explicit design-to-plan handoff. The skill retains no
upstream prose, examples, code, fixed template, execution protocol, or harness-specific workflow.

## ECC `intent-driven-development`

- Original author: Affaan Mustafa
- Upstream project: [affaan-m/ECC](https://github.com/affaan-m/ECC)
- Source path:
  [`skills/intent-driven-development/SKILL.md`](https://github.com/affaan-m/ECC/blob/e04ea0b9cc8248686edf5ac751cadff550e162b8/skills/intent-driven-development/SKILL.md)
- Source revision: `e04ea0b9cc8248686edf5ac751cadff550e162b8`, inspected 2026-09-04
- Source license:
  [MIT](https://github.com/affaan-m/ECC/blob/e04ea0b9cc8248686edf5ac751cadff550e162b8/LICENSE)
- Relationship: idea-level influence, independently expressed

The source informed the boundary between current behavior and intended policy, risk-scaled depth, and explicit negative
system guarantees. This skill retains no source prose, acceptance-brief template, criterion identifiers, revision
protocol, or combined requirements and implementation workflow.

## Addy Osmani, “How to write a good spec for AI agents”

- Source: [addyosmani.com/blog/good-spec/](https://addyosmani.com/blog/good-spec/)
- Published: 2026-01-13; read 2026-09-11
- Source license: no reuse license stated on the page; not relied on
- Relationship: idea-level influence, independently expressed

The article informed the accepted-specification input and traceability seam added between requirements and technical
design. This skill independently preserves architecture as a separate artifact rather than adopting the article's
blended PRD/SRS/technical-plan shape. No source prose, examples, images, templates, code, or assets are copied, adapted,
translated, or vendored.
