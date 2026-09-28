# Attributions

## Current skill

- Skill: `domain-modeling`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and materially modified

## Original authors and source

- Original author: Matt Pocock
- Upstream project: <https://github.com/mattpocock/skills>
- Source path: `skills/engineering/domain-modeling/SKILL.md`, with its co-located `CONTEXT-FORMAT.md`
- Source commit: `959a8e9f1edc3adbe2f7e3054bb6fbefa6696260`

## Adaptation note

This skill is derived from the upstream `domain-modeling` skill and has been modified for this repository.

Retained from upstream, adapted and reworded:

- the core distinction that this is the *active* modeling discipline, not passive reading of a glossary;
- the four in-session moves — challenge conflicting terms, sharpen vague or overloaded terms, stress-test
  relationships with invented edge-case scenarios, and cross-check claims against the code;
- capturing resolved vocabulary inline the moment it crystallizes, never batched;
- the glossary being vocabulary only, free of implementation detail, decisions, or spec content;
- lazy, discovery-first file creation, and the single- versus multi-context (context-map) layout;
- the glossary entry shape — term, tight definition, and an `_Avoid_` list of words to reject — in
  `references/glossary-format.md`, adapted from the upstream `CONTEXT-FORMAT.md`. No text was copied verbatim; the
  worked terms are illustrative and independent.

Changed for this repository:

- ADR authoring is **not** carried here. Upstream bundled an `ADR-FORMAT.md` and an ADR gate; this skill instead
  points to the repository's existing decision-record owner, `writing-documentation`, which now carries the
  three-part gate this repository adopted from the same upstream. See that skill's `ATTRIBUTIONS.md`.
- Upstream's fixed filenames (`CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`) are treated as illustrative, not
  prescribed: the skill discovers the repository's own convention and falls back to a documented default.
- A session finish line and a rule that definitions use words a newcomer already has, checked with
  `writing-for-humans`.
- Frontmatter description rewritten for this repository's routing, with explicit exclusions against the
  `brooks-*` review skills, `technical-design`, and `requirements-specification`.

## Upstream license

The upstream source is MIT-licensed. See `LICENSE.upstream` in this directory for the full notice, reproduced
verbatim from the upstream repository's own `LICENSE` at the source commit above.
