# AGENTS.md — skills/

Instructions for agents working under `skills/`; `CLAUDE.md` is a symlink to this file.
The stack itself is described in `README.md`, the backlog in `TODO.md`, and the archive
procedure in `archived/README.md`. What is here is the one thing none of those can be
relied on to have been read first.

## The post-commit redeploy hook can fail silently — verify the deploy, never the exit status

**`scripts/sync-skills-kasetto.sh` reports success in the case where it does nothing.**
It maps the commit's changed paths to Kasetto scopes with
`git diff --name-only HEAD~1 HEAD` (line 168), and git's rename detection collapses a
100% rename to its **destination path only**. So a `git mv` that takes a skill OUT of a
deployed group produces a change set with no `skills/shared/` path in it, no scope is
selected, and the hook exits 0 — no warning, no output, ~0.02s. The deployed copy stays
behind as an orphan.

Reproduced 2026-08-27 on `84cd615`, the `writing-great-skills` archival. pre-commit
printed `redeploy changed skill scopes via Kasetto ... Passed`, and the skill was still
present in `~/.config/claude/skills`, `~/.config/opencode/skills` and `~/.copilot/skills`
afterwards. `git diff --no-renames --name-only 84cd615~1 84cd615` lists the four
`skills/shared/agent-stack/writing-great-skills/*` source paths that the default
invocation hides.

**Which moves this hits:**

| Move | Hook fires? |
|---|---|
| Edit in place, add, delete | Yes — the path keeps its group prefix |
| Between domains inside `shared/` | Yes — both sides are still `skills/shared/…` |
| `shared/` → `archived/` (every archival) | **No** — silently |
| `shared/` → `claude/`, or any cross-group move | **No** for the source scope; the destination scope deploys a second copy |

**Nothing in the normal loop catches it.** `git status` is clean, because the orphan lives
outside this repository. `just skills-owned` cannot catch it either: the lock still claims
the directory, since the deploy that would have rewritten the lock is the one that did not
run — reasoned from the mechanism, NOT measured, because the orphan was recovered before
the gate was run against it. Whether `just skills-deployed` would have flagged it is
untested for the same reason. **So confirm with `ls` against each agent's skills directory,
never with `git status` and never with a green hook.**

Recovery is `./scripts/kasetto-deploy.sh`, which names every local skill in the scope's
group and so re-resolves glob membership. On `84cd615` it reported
`0 updated 0 added 1 removed 64 unchanged` and pruned all three destinations. It only
works while the group still holds a skill to name — see the emptied-group case below.

**Candidate fix, UNAPPLIED: `--no-renames` (or `-M0`) on that diff.** Tracked in
`TODO.md`. It is a runtime change to a gate script and wants its own verification; do not
apply it as a drive-by.

### The two related failures, so they are not confused with this one

- **Emptied-group fallback — loud, and a different cause.** When archiving removes the
  LAST skill from a group there are no names left to pass, `kasetto-deploy.sh` falls back
  to a plain sync that cannot prune, and it says so in three `WARN:` lines naming the
  by-hand command. `archived/README.md` carries it. That one announces itself; the rename
  case does not.
- **A dirty tree can roll the lock rewrite back — also silent, but the SKILLS deploy
  succeeds.** pre-commit stashes unrelated unstaged work and discards hook auto-fixes that
  conflict on restore, leaving a stale committed lock while the deployed bytes are current.
  The root `AGENTS.md` "Deploy / redeploy" section carries it. Opposite shape to the
  rename case: there the lock is wrong and the deploy is right; here the deploy is wrong.

Both of those, and this one, share a single practical rule: **after any commit that moves,
archives or removes a skill, look at the destination directories.**
