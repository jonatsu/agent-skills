# Attributions

## Current Skill

- Skill: `define-goal`
- Current author and adapter: Joonas Onatsu
- Current license: Apache License 2.0, inherited from upstream
- Status: substantially modified from one upstream skill

Keep this file and `LICENSE.upstream` with the skill when redistributing it. The upstream skill directory
supplied no `NOTICE` file when checked on 2026-10-04, and its `LICENSE.txt` is the stock Apache-2.0 text with
the appendix's copyright placeholder unfilled.

## Upstream Source

- Original author: OpenAI
- Project: [openai/skills](https://github.com/openai/skills)
- Source path: `skills/.curated/define-goal/`
- Source commit: `b0401f07213a66414d84a65cb50c1d226f99485a` ("[codex] Add define-goal skill (#417)", 2026-05-21)
- Upstream skill name: `define-goal`
- Upstream licence: Apache-2.0, reproduced verbatim in `LICENSE.upstream` (blob
  `13e25df86ce06eb6488e6a6bc5c5847f5dedc352`)

This package is a modified version under section 4 of Apache-2.0. The upstream skill targets Codex alone and
arms a goal through `get_goal` and `create_goal`. This package keeps its quality bar, its rejection of activity
goals, its per-work-type quantification heuristics, its clarifying-question guidance, and one adapted example
pair. It adds the five-part goal form, a condition written for a transcript-reading judge, a placement in the
engineering pipeline, the closing conformance check, the durable checkpoint copy, the rules for working toward a
goal, and one arming branch per harness. The upstream `agents/openai.yaml` interface file was not carried over.

## File Provenance

| File                               | Relationship to upstream                                                             |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| `SKILL.md`                         | Rewritten; quality bar, heuristics, questions, and one example adapted from upstream |
| `references/harness-goal-loops.md` | Original; written from read-only inspections of each harness on 2026-10-04           |
| `LICENSE.upstream`                 | Upstream `LICENSE.txt`, unmodified                                                   |

The harness facts in `references/harness-goal-loops.md` come from this repository's own research, not from the
upstream skill.
