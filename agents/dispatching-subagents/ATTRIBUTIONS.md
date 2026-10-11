# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## Third-party Sources

### Jesse Vincent: superpowers `dispatching-parallel-agents` skill

- Source: <https://github.com/obra/superpowers>, `skills/dispatching-parallel-agents/SKILL.md`
- License: `MIT`
- Version: `6dbbbda3baeff8407f3dddb0cc9e8a9495a273bc`

The source informed the independence test before a parallel run: related failures stay together, shared state rules
out parallel agents, and exploratory debugging comes before splitting. It also informed sending parallel dispatches
together, and checking combined results for conflicting edits, running the full suite, and spot-checking because
agents make systematic errors. Nothing was copied.

### Jesse Vincent: superpowers `subagent-driven-development` skill

- Source: <https://github.com/obra/superpowers>, `skills/subagent-driven-development/` (`SKILL.md`,
  `implementer-prompt.md`, `task-reviewer-prompt.md`, `re-review-prompt.md`)
- License: `MIT`
- Version: `5bf4e78011075bcfc0dc295f0724994cd123ee71`

The source informed the four report statuses and how to act on each, including changing something before
re-dispatching a blocked task; the rule that a worker dispatches no subagents or reviewers of its own; batching
small same-shape edits into one dispatch; resuming the original implementer with review findings, then escalating
to a fresh one on a stronger model; the scoped re-review of a fix; and keeping "do not flag" instructions out of a
reviewer's prompt. Nothing was copied.

### Matt Pocock: `writing-for-agents` skill

- Source: <https://github.com/mattpocock/skills>, `skills/productivity/writing-for-agents/`
- License: `MIT`
- Version: read 2026-09-28

The skill informed the leading words (lane, independent), the completion criterion on each stage, and positive
targets over negation. Nothing was copied.
