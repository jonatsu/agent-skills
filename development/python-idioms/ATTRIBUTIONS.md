# Attributions

## Current Skill

- Skill: `python-idioms`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: independently written; carries the Python expression of a withdrawn skill's rules

## Predecessor: searchable-code

The findability rules here restate, in Python, the deleted `searchable-code` skill (MIT, same author),
recoverable at `git show aa34532^:skills/shared/development/searchable-code/SKILL.md`. That package was
reviewed, repaired across five findings, validated by every gate, and then **activated in 0 of 13 measured
runs**; `docs/findings/skill-discovery-limits.md` holds the measurement.

Only its authoring rules survived, condensed, in `agents/rules/instructions/workflow.md`. Its diagnostic
half — the recovery procedure for a search that came up empty, and the rule that whichever recovery worked
names the defect to fix in the same change — was lost, and is restored here.

## Deliberate Duplication

The naming and test-writing preferences appear both here and in `agents/rules/instructions/workflow.md`. The
user directed this on 2026-09-04, accepting the drift risk, because the global rules file is likely to be
trimmed later and these patterns would otherwise disappear with it. Nothing detects divergence between the two
copies; `skills/TODO.md` records the open question of where these patterns should ultimately live.

## Activation Risk

This skill's subject is the same one that failed to activate as `searchable-code`. Three things differ: the
enforceable half now lives in a project's ruff configuration rather than in prose, the description names
review and refactor requests rather than authoring, and the empty-search recovery gives it a trigger someone
actually verbalizes. None of that is proven.

**The acceptance test is behavioral.** Measure activation on a review request, a refactor request, and a
failed-grep report. If it does not fire on those three, delete it rather than reword it — that is what the
predecessor's measurement established. `docs/plans/python-skill-set-draft.md` records this as the set's
largest open risk.
