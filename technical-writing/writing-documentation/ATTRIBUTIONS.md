# Attributions

## Current skill

- Skill: `writing-documentation`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and materially narrowed; renamed from `technical-writing` on 2026-09-04

## Original authors and sources

- Primary source (structure, workflow, checklists — used as the direct
  basis for this skill, adapted and trimmed):
  - Original author: peizh
  - Upstream project: [tech-writing](https://github.com/peizh/tech-writing)
  - Source file: <https://github.com/peizh/tech-writing/blob/main/SKILL.md>
  - Upstream license: MIT
- Secondary source (two narrow ideas only — the "choose the right document
  shape" taxonomy and a couple of review-checklist items; structure, tone,
  and content were NOT carried over):
  - Upstream project: [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
  - Source file: <https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/technical-writer.md>
  - Upstream license: MIT

## Adaptation note

This skill retains the upstream's document-composition job, task taxonomy,
examples, accessibility, error-recovery guidance, and response modes. It no
longer carries a general prose style or rewriting discipline.

The VoltAgent `technical-writer.md` source was deliberately NOT used for
structure or tone: it is a generic multi-agent "persona" template containing
fabricated metrics (e.g. "92% user satisfaction", "127 pages written") and a
simulated inter-agent JSON protocol that don't apply here, and which would
contradict this skill's own "never invent facts or numbers" guardrail. Only
its documentation-type taxonomy and a couple of non-duplicate review-checklist
ideas were mined from it.

## Additional idea-level influences

The following sources informed the independently written 2026-09-03 rewrite's
reader-outcome framing, document-mode distinctions, tutorial checkpoints, and
implementation placement guidance. No text was copied or adapted. Their
licenses were not established during review, so this record does not claim a
license grant.

- [Cursor pstack technical-writing](https://github.com/cursor/plugins/blob/7314f723a487ec406b6369fe5865ba034cfed166/pstack/skills/technical-writing/SKILL.md)
- [awesomekoder technical_writer](https://github.com/awesomekoder/awesome-llm-apps/blob/1fcfb4fab8e20f8b543189059de2fac6d0e71720/awesome_agent_skills/writing/technical_writer.md)
- [Mindrally technical-writing](https://github.com/Mindrally/skills/blob/main/technical-writing/SKILL.md)

## House-Style Section, Received From `writing-for-humans`

The "Match an Established House Style" section moved here from `writing-for-humans` on 2026-09-04, when the
boundary between the two skills was redrawn: that skill preserves an individual author's voice at the sentence
level, and this one owns conventions repeated across a documentation set. The section's exemplar-evidence
approach was informed by
[mohitagw15856/pm-claude-skills house-style-enforcer](https://github.com/mohitagw15856/pm-claude-skills/blob/main/skills/house-style-enforcer/SKILL.md).
No text was copied or adapted. The source license was not established during review, so this record does not
claim a license grant.

## ASD-STE100 as an Inspirational Source

ASD-STE100 Simplified Technical English, Issue 9 (2025-01-15), was read directly on 2026-09-04 and informed the
"Write Notes and Safety Instructions" section. The standard is an inspirational source, not a dependency: this
skill does not implement it, does not cite its rule numbers, and makes no claim of conformance.

It informed three things specifically: the rule that a note carries information only, together with the
delete-every-note verification test; the distinction between a warning for risk of injury and a caution for risk
of damage, with a warning taking precedence where both apply; and the required order of a safety instruction,
signal word before command or condition before consequence.

The standard's remaining rules are sentence-level and belong to `writing-for-humans`, whose `ATTRIBUTIONS.md`
records them and the rules deliberately declined.

No rule text and no dictionary entry is reproduced here or in `SKILL.md`. The standard is free to obtain and not
free to redistribute. `docs/plans/archived/ste-adoption.md` records the decisions, including the rejected
alternatives.

## Decision-Record Section and Reference

The "Write a Decision Record" section, the decision-record additions to "Match an Established House Style" and
"Review", and `references/decision-record.md` were written on 2026-09-09 after reading
[addyosmani/agent-skills `documentation-and-adrs`](https://github.com/addyosmani/agent-skills/blob/main/skills/documentation-and-adrs/SKILL.md)
(Copyright (c) 2025 Addy Osmani, MIT). No text, template, or example was copied or adapted; the worked example
is independent and shares no subject with the upstream's.

Five ideas came from that source and are recorded here because reading it changed what this skill contains:

- writing a decision record on a cost-to-reverse trigger, with concrete decision classes, rather than only on
  request;
- an explicit status field and the proposed, accepted, superseded, deprecated lifecycle;
- never deleting a superseded record, and superseding by writing a new one that references it;
- requiring a per-alternative rejection reason rather than a bare list of alternatives considered; and
- checking an existing series for its location and markup, its numbering and filename pattern, and its heading
  set before writing into it, including configuration such as `.adr-dir` or an `adr-tools` setup.

The upstream's remaining subjects were deliberately declined, not overlooked. Inline code-comment discipline,
JSDoc and OpenAPI examples, a README template, and agent rules-file guidance each belong to another owner in
this repository, and carrying them here would break this skill's scope. Its "Common Rationalizations" and "Red
Flags" tables serve a different job again, persuading a reluctant agent to write documentation at all, rather
than composing a document well.

## Decision-Record Gate and Tiering

The "Write a Decision Record" section was revised on 2026-09-15 after reading
[mattpocock/skills `domain-modeling`](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md)
and its `ADR-FORMAT.md` (Copyright (c) 2026 Matt Pocock, MIT, HEAD
`959a8e9f1edc3adbe2f7e3054bb6fbefa6696260`). No text, template, or example was copied or adapted.

Two ideas came from that source and are recorded here because reading it changed what this skill contains:

- the three-part gate for whether a decision warrants a record at all — hard to reverse AND surprising without
  context AND the outcome of a real trade-off — which sharpened and replaced the earlier cost-to-reverse-only
  trigger adopted from addyosmani; and
- tiering the record's weight to the decision's blast radius, defaulting to a light title-plus-a-few-sentences
  form and escalating to the full five-element record only where wide later work or the alternatives require it.

The upstream's file-layout conventions (`docs/adr/NNNN-slug.md`, a co-located `ADR-FORMAT.md`) were not adopted:
this repository's decision-record location and format discovery already live in `references/decision-record.md`.

## Changelog Reference

`references/changelog.md` was added on 2026-09-09 from the same upstream reading. Two ideas came from it: that
a maintained changelog belongs to this skill's change-note subject at all, and grouping entries by kind of
change under a dated, versioned release heading. No text or example was copied; the worked example is
independent.

The grouping vocabulary — added, changed, deprecated, removed, fixed, security — and the `Unreleased` section
are the [Keep a Changelog](https://keepachangelog.com) convention, named here as the widely used standard the
reference describes rather than as a source it reproduces. The entry-writing guidance, the
effect-versus-commit-subject distinction, and the omission rules are this skill's own.

The decision about whether a project warrants a changelog defers to `context-architecture`, which owns it as a
conditional addition to a repository's documentation layout. This reference covers composition only.

## Evidence Workflow and Agent-Facing Instruction Design

[Eren Suner, "Agent Skill for Documentation"](https://www.skillfully.sh/blog/agent-skill-for-documentation),
published 2026-05-17 and read 2026-09-23, informed the authority-map workflow, explicit source-conflict handling,
classification of confirmed, assumed, unknown, and conflicting information, and delivery of unresolved evidence
gaps. The article states no content license. The retained ideas are expressed independently; no text, example, or
structure was copied or adapted.

[Matt Pocock's `writing-for-agents`](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/writing-for-agents/SKILL.md)
(Copyright (c) 2026 Matt Pocock, MIT) informed the use of the `authority map`, `locator`, and `reader-ready`
leading words, the checkable completion criteria, and the single-owner pointer from this skill to
`writing-for-humans`. Every instruction and example is independently written; no upstream text was copied or
adapted.

## Diátaxis Document Types and In-Place Improvement

The 2026-09-28 refresh rebuilt "Choose the Document Type" and added "Improve an Existing Set in Place" after
reading two sources. Both are licensed CC BY-SA 4.0, so only ideas were taken: every sentence, the table, and
the examples are independently written, and no text was copied, adapted, or translated.

- [Diátaxis](https://diataxis.fr/) by Daniele Procida, source repository
  [evildmp/diataxis-documentation-framework](https://github.com/evildmp/diataxis-documentation-framework) at
  `957c09ca40b4a1edc23874f713e01937d50d54d5`. It supplied the four-type classification this skill already used
  without credit, the two classifying questions (action or understanding, study or work), the content that
  typically leaks into each type, and the method of improving a set one piece at a time rather than creating an
  empty structure first.
- [keithpatton/diataxis-agent-skill](https://github.com/keithpatton/diataxis-agent-skill) at
  `5b095a5e7aebe77ce4af855809123e12d92b9efd`. It prompted reporting a classification with its evidence and moving
  leaked content out rather than blending it. Its fix for a mixed document, splitting it into four files at once,
  was declined because it contradicts Diátaxis's own advice against restructuring first.

The same refresh added "Cut Document-Level Noise", "Explain Concepts Where the Reader Meets Them", the specification
and design-document section, the link-reachability rule, and `references/review-sequence.md`. These came from the
user's own corrections during documentation work in another repository, not from an external source. The light
and full decision-record forms moved from `SKILL.md` to `references/decision-record.md` unchanged in substance.

Material changes from peizh/tech-writing include:

- Folded a short documentation-type taxonomy into the "choose the right
  document shape" workflow step.
- Removed generic prose rules, rewrite heuristics, and style guardrails. The
  `writing-for-humans` skill governs prose-level drafting, editing, and review;
  this skill retains document-level decisions, including the house style of a
  documentation set.
- Dropped the Chinese-technical-prose reference branch.

## Upstream license (MIT, both sources)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
