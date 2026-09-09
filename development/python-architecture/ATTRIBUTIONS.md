# Attributions

## Current skill

- Skill: `python-architecture`
- Current author: Joonas Onatsu
- Current license: MIT

## Origin

Adapted on 2026-09-09 from the author's own `python-architecture` skill in a separate Claude Code setup
(`~/.claude/skills/python-architecture` on the Windows host). Same author, so no third-party licence applies;
this entry records the lineage rather than an obligation.

Changes made while porting:

- Added the frontmatter this repository requires (`license`, `metadata.author`) and a description written for
  discovery rather than as a summary.
- Rewrote the cross-references. The original delegated to a single `python-style` skill, which does not exist
  here; each pointer now names the skill that actually owns the subject — `python-typing`,
  `python-error-handling`, `python-testing`, and `python-project-management`.
- Added the boundary statement against `python-project-management`, which owns `pyproject.toml` and the
  project's tooling. The overlap is `[project.scripts]` and the `src` layout, where this skill decides the
  shape and that one configures it.
- Turned the cycle guidance into an ordered procedure, and stated why a function-local import is a defect
  rather than asserting it.
- Added the "Before Calling Structural Work Done" checks, matching the other Python skills in this repository.
- Dropped the original's "account for each rule before reporting the work done" preamble. It asks for an
  enumeration of compliance, which inflates every report, and this repository's workflow rules already require
  reporting what was and was not verified.

## Verified external sources

Both are cited in the skill and were used to confirm the packaging and pytest claims, not as material to adapt:

- <https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/>
- <https://docs.pytest.org/en/stable/explanation/goodpractices.html>
