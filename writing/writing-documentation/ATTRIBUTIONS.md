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
JSDoc and OpenAPI examples, a README template, changelog structure, and agent rules-file guidance each belong
to another owner in this repository, and carrying them here would break this skill's scope. Its "Common
Rationalizations" and "Red Flags" tables serve a different job again, persuading a reluctant agent to write
documentation at all, rather than composing a document well.

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
