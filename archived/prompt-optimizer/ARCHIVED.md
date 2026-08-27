# Archived: prompt-optimizer

- **Archived**: 2026-08-27
- **Last deployed to**: Claude Code, OpenCode and GitHub Copilot CLI, via the
  `shared` group (`skills/shared/agent-stack/prompt-optimizer`)
- **Successor**: `skills/shared/agent-stack/system-prompts`, REPAIR branch

## Why

Merged rather than retired. `prompt-optimizer` and `system-prompts` had the same
subject — the prompt text a model reads — and differed only in direction:
`system-prompts` wrote from a specification, `prompt-optimizer` repaired against
an observed failure. Two skills competing for "write a system prompt" and "fix
this prompt" is a trigger collision, and the user's own use of this skill never
touched anything but agent prompts, which the other skill already owned.

`SKILL.md` here is byte-identical to what was last deployed. It is kept because
its diagnostic table and technique catalog were written against real failures,
and the reference copy is only worth having if it is exactly what ran.

## What moved, and where

| Content | New home |
|---|---|
| Iron Law (change targets a named failure, checked against a concrete input) | Folded into `system-prompts`' unified Iron Law, which now covers both adding and changing a sentence |
| Six-step workflow | `system-prompts` → "Branch: REPAIR", unchanged in substance |
| Symptom → cause → fix table | `system-prompts/references/failure-modes.md`, plus two new rows routing rank and authority failures back to the main file |
| Technique catalog | Same reference file, with a new rule: apply the minimum, because three techniques at once make the verification step uninterpretable |
| General prompt anatomy, few-shot, prefill, temperature, stop, caching | `system-prompts/references/api-prompts.md`, loaded only when the target is an API call |
| `claude-api` handoff for model IDs, params and caching | Kept in both the scope section and the API section |
| Anti-patterns | Merged into `system-prompts`' single anti-pattern table |
| Pre-delivery checklist | `system-prompts`, split into a shared list and a REPAIR-only list |

Nothing was dropped in the merge.

## Reviving it

There is no reason to. If the REPAIR branch ever needs to be a separate skill
again — for instance if a non-agent prompt-engineering workflow grows its own
tooling — take the branch and the reference file out of `system-prompts` rather
than restoring this copy, which predates the corrections made to the shared
craft material on 2026-08-27.
