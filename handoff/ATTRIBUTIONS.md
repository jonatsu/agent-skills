# Attributions

## Current skill

- Skill: `handoff`
- Current author: Joonas Onatsu
- Current license: MIT (unchanged from upstream)
- Status: adapted from upstream and substantially rewritten

## Original authors and source

- Original author: Matt Pocock ([@mattpocock](https://github.com/mattpocock))
- Upstream project: [mattpocock/skills](https://github.com/mattpocock/skills)
- Source path: `skills/productivity/handoff/SKILL.md`
- Source commit: `d28dfdc39beadc3142a33359b5cfa4765dcbd0bc` (2026-08-15)
- Upstream license: MIT

## What was kept, and what was rebuilt

Upstream is deliberately minimal — roughly six sentences with no section
structure. What survives here is its discipline rather than its text.

| Element | Relationship to upstream |
|---|---|
| No-duplication rule | Kept, and made operative: it drives the `READ FIRST` section, the length budget, and two anti-patterns |
| Redaction rule | Kept |
| Tailoring to a stated next-session focus | Kept, expanded into the focus table |
| Suggested-skills section | Kept, with a new constraint that only skills available in the current session may be named |
| Save location | Kept in spirit (OS temporary directory, never the workspace), reworded to name fallbacks instead of one command |
| Section structure | New. Upstream names no sections |
| Everything else | New |

## Adaptation note

Three sources were merged. Upstream supplied the no-duplication discipline, the
redaction rule, and the focus-tailoring idea. The section shape comes from this
repository owner's own session-priming workflow, which this skill now owns. It
was then corrected against a real priming brief that had successfully carried a
multi-item lane across a context refresh — the only part of this skill derived
from observed practice rather than from reasoning.

Eleven sections: `MISSION`, `READ FIRST`, `STATE`, `NEXT`, and `CARRIED CONTEXT`
always; `LOCKED`, `SCOPE`, `OPEN`, `DEVIATIONS`, `PROCESS`, and `SKILLS` when
they have content.

Material changes:

- A `PRIME` / `DOCUMENT` mode gate. Upstream only writes a document; the
  paste-ready priming prompt for a fresh context is a second output shape with
  different self-sufficiency and path-writing rules.
- A ground-truth step. Upstream writes from the conversation; this version
  requires confirming paths, branches, and commits in the same turn, on the
  grounds that a stale reference is undetectable by the reader.
- `CARRIED CONTEXT` — the tacit steering, inferred conventions, and ruled-out
  options that survive nowhere else. Upstream has no equivalent.
- `LOCKED` and `DEVIATIONS`, which stop a fresh agent from redesigning settled
  work or reverting deliberate departures from a plan.
- `OPEN` decisions carry the current lean, not just the question.
- Verification anchoring: a "done" claim must name what proved it, or be marked
  unverified.
- Sections are conditional. Only five are always present; the rest are omitted
  when empty rather than emitted hollow.
- `MISSION` and `SCOPE`, and the "pre-empt the misread" discipline, all added
  after a real brief showed them carrying weight that no existing section held.
- `disable-model-invocation: true` was dropped. Upstream restricts this skill to
  the user; here the agent is expected to raise a handoff unprompted when a long
  session reaches a clean seam, which requires model invocation.

## Not derived from the `handoff-engineering` plugin

An intermediate derivative of Matt Pocock's skill was published as
`handoff-engineering` in `alirezarezvani/claude-skills` (MIT, itself crediting
Matt Pocock). It was evaluated and deliberately not used as a base. Its bundled
`skill_recommender.py` hardcodes a skill list from its own publisher's
repository, so it recommends skills that are not installed here; the constraint
in this skill's `SKILLS` section exists because of that failure mode. Two of its
ideas were adopted independently and are credited here: the explicit length
budget, and the "handing off a handoff" anti-pattern.

## Upstream license

The upstream source is used under the MIT License. This skill remains MIT.
Preserve this attribution file with the skill when redistributing.
