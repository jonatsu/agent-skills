# Attributions

## Current skill

- Skill: `technical-writing`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and materially narrowed

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

Material changes from peizh/tech-writing include:

- Folded a short documentation-type taxonomy into the "choose the right
  document shape" workflow step.
- Removed generic prose rules, rewrite heuristics, style guardrails, and the
  `writing-for-humans` delegation. Global and repository writing policy govern
  prose; `writing-for-humans` is an optional, separate copy-editing pass.
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
