# Attributions

## Current Skill

- Skill: `python-style`
- Current author: Joonas Onatsu
- Current license: MIT

## Repository Lineage

The author's scoped Python defaults and archived `python-idioms` informed this focused replacement.
The archive is preserved at commit `6c4fa3b9cbeee6880f7efae7180622d7c3e06890` under
`archived/python-idioms/`. Both sources are MIT work by the same author.

Retained preferences include searchable naming, useful docstrings, `attrs` with a stdlib exception, and simple control flow.
The predecessor's findability guidance came from the same author's MIT `searchable-code` skill, recoverable at
`git show 8431703de957^:development/searchable-code/SKILL.md`.
Its automatic repair after a failed search is not retained.
General search recovery and test policy remain outside this skill.

## Independently Expressed Ideas

Integralist's `.claude/rules/python.md` in `Integralist/agent-skills`, commit
`07155927c4a44cf97b050ea4f728fce840822ce9`, was reviewed on 2026-09-11:

<https://github.com/Integralist/agent-skills/blob/07155927c4a44cf97b050ea4f728fce840822ce9/.claude/rules/python.md>

The review informed resource ownership, standard logging with deferred formatting, guard clauses, and conditional enums.
The wording and organization are independently written; no upstream text or code is copied or adapted.
No license covering the rules was found in the pinned tree. The separate MCP component's license does not cover these rules.

Python's datetime documentation was used to verify aware and naive datetime semantics:
<https://docs.python.org/3/library/datetime.html#aware-and-naive-objects>.
