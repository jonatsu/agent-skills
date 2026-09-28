# Attributions

## Current Skill

- Skill: `dispatching-subagents`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original work with independently expressed idea-level influence

No text, code, or template from any source below was copied or adapted, so no `LICENSE.upstream` ships with the
package. The four status names are shared terminology; their definitions and the escalation rule are written
here.

## superpowers `dispatching-parallel-agents`

- Original author: Jesse Vincent
- Upstream project: [obra/superpowers](https://github.com/obra/superpowers)
- Source path: `skills/dispatching-parallel-agents/SKILL.md`
- Source revision: `6dbbbda3baeff8407f3dddb0cc9e8a9495a273bc`, inspected 2026-09-28
- Source license: MIT
- Relationship: idea-level influence, independently expressed

The source informed the independence test before a parallel run: related failures stay together, shared state
rules out parallel agents, and exploratory debugging comes before splitting. It also informed sending parallel
dispatches together, and checking combined results for conflicting edits, running the full suite, and
spot-checking because agents make systematic errors.

## superpowers `subagent-driven-development`

- Original author: Jesse Vincent
- Upstream project: [obra/superpowers](https://github.com/obra/superpowers)
- Source path: `skills/subagent-driven-development/` (`SKILL.md`, `implementer-prompt.md`,
  `task-reviewer-prompt.md`, `re-review-prompt.md`)
- Source revision: `5bf4e78011075bcfc0dc295f0724994cd123ee71`, inspected 2026-09-28
- Source license: MIT
- Relationship: idea-level influence, independently expressed

The source informed the four report statuses and how to act on each, including changing something before
re-dispatching a blocked task; the rule that a worker dispatches no subagents or reviewers of its own; batching
small same-shape edits into one dispatch; resuming the original implementer with review findings, then escalating
to a fresh one on a stronger model; the scoped re-review of a fix; and keeping "do not flag" instructions out of a
reviewer's prompt. Its plan-execution loop, ledger, rulings list, fix-round cap, scripts, and prompt templates are
not retained.

## `writing-for-agents`

- Relationship: idea-level influence from a skill deployed in this stack, independently expressed

It informed the leading words (lane, independent), the completion criterion on each stage, and positive targets
over negation.
