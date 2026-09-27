# Attributions

## Current skill

- Skill: `to-questionnaire`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and modified

## Original authors and source

- Original author: Matt Pocock
- Upstream project: <https://github.com/mattpocock/skills>
- Source path: `skills/productivity/to-questionnaire/SKILL.md`
- Source commit: `959a8e9f1edc3adbe2f7e3054bb6fbefa6696260`

## Adaptation note

This skill is derived from the upstream `to-questionnaire` skill and has been modified for this repository.

Retained from upstream, adapted and reworded:

- the core inversion — "grill the send, not the subject": interview the user only about the recipient and the
  required outputs, and aim the document's questions at the gap between them;
- the three-step flow (recipient identity → what is needed back → write the document) and the
  `to-questionnaire-<slug>.md` output convention;
- the discovery-questionnaire document structure and its template — purpose, from/to/use line, context,
  how-to-answer, most-important-first themed questions with answer stubs and optional _why this matters_ lines,
  and a closing catch-all.

Changed for this repository:

- Frontmatter description rewritten for this repository's routing, with explicit exclusions against `interview-me`
  (which interrogates the user's own design) and `requirements-specification`.
- The upstream `disable-model-invocation: true` flag was not carried: this skill produces only a Markdown file
  and benefits from ordinary description-based discovery here.
- The template's example question is illustrative and independent; no other text was copied verbatim.

## Upstream license

The upstream source is MIT-licensed. See `LICENSE.upstream` in this directory for the full notice, reproduced
verbatim from the upstream repository's own `LICENSE` at the source commit above.
