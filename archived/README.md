# Archived skills

Skills kept for reference that no longer deploy anywhere. **Nothing in this
directory reaches any agent.**

Kasetto discovers skills through three configs that name `skills/shared`,
`skills/claude` and `skills/opencode` explicitly — nothing globs `skills/*`. A
directory beside those is therefore invisible to deployment with no exclusion
list to maintain, and it cannot drift back into a deploy by accident. That is the
whole mechanism; there is no separate opt-out to remember.

## What lives here

| Skill | Archived | Why |
|---|---|---|
| `headroom-management` | 2026-08-26 | The Headroom proxy it manages was rejected, so the skill governs a tool this setup no longer runs. See its `ARCHIVED.md`. |
| `lean-ctx` | 2026-08-27 | lean-ctx was removed from this setup, so every `ctx_*` trigger in the skill names a tool that no longer exists. Its three locally-measured reference files are why this is an archive rather than a deletion, and its Apache-2.0 `LICENSE.upstream`/`NOTICE.upstream` must stay with the directory. See its `ARCHIVED.md`. |
| `prompt-optimizer` | 2026-08-27 | Merged into `shared/agent-stack/system-prompts` as its REPAIR branch — same subject, opposite direction, and the two collided on "write a system prompt" and "fix this prompt". Nothing was dropped; `ARCHIVED.md` maps every section to its new home. Archived rather than deleted because its diagnostic table was written against real failures. |
| `writing-great-skills` | 2026-08-27 | Unreachable and unconsumed: `disable-model-invocation: true` meant no skill could invoke it and Claude Code could not preload it, and its only dependents were removed from `skill-judge` in `7704d3e`. It was also a second authority on skill authoring that contradicted `skill-forge` on prohibitions without acknowledging it. Preserved verbatim from upstream, which is why it was never brought up to repo conventions — and why bringing it up would have destroyed the property it was kept for. `ARCHIVED.md` names the four concepts `skill-forge` does not carry. |

## Archiving a skill

1. `git mv skills/<group>/<name> skills/archived/<name>` — use `git mv` so
   history and rename detection survive.
2. Write `skills/archived/<name>/ARCHIVED.md`: the date, why it was archived,
   what it was deployed to last, and where any successor lives. **Leave
   `SKILL.md` byte-identical to what was last deployed** — the reference copy is
   only worth keeping if it is exactly what ran.
3. Add a row to the table above.
4. **Prune the deployed copy by hand.** The post-commit hook will NOT do it, and
   the reason is worth knowing rather than rediscovering — see below.
5. Update whatever named the skill as live: `skills/README.md`, the header
   comment in `scripts/kasetto-deploy.sh`, and any open item in
   `skills/TODO.md` that planned future work on it.

## The prune step is manual, and the automation says so

`scripts/kasetto-deploy.sh` names every local skill in a scope's group as
`--update <name>...`, because a plain `kst sync` trusts the locked hash and never
re-reads a local source. When archiving empties a group, there are no names left
to pass, and the script falls back to a plain sync that **cannot prune**:

```text
WARN: skills/<group> holds no skills, so no locked sibling can be named.
WARN: falling back to a plain sync, which cannot prune. Re-resolve by hand:
WARN:   cd skills/kasetto/<scope> && kst sync --project --update
```

Verified 2026-08-26 while archiving `headroom-management`: with the source
directory deleted from disk, `kst` did not error — it reported
`headroom-management unchanged` and did nothing, because it answered from the
lock rather than the disk. A bare `--update` re-resolved correctly and reported
`removed`.

**So an archived skill stays deployed until someone runs that command**, and two
things that look like they would catch it do not:

- `just skills-owned` skips `~/.config/opencode/skills` entirely — a
  `skip_targets` entry in `scripts/check-skill-ownership.sh` while the OpenCode
  side is reworked.
- `git status` shows nothing, because the orphan is outside this repository.

Confirm the prune with `ls` against the destination, never with `git status`.

A bare `--update` is safe for a scope whose only source is local. **Do not use it
on a scope carrying remote third-party sources** — it re-resolves moving refs
there too, which is a different change than the one you meant to make.
