# agent-skills

Single source of truth for my agent skills, deployed to both **Claude Code** and
**OpenCode** from one place. Edit a skill here once; both agents pick it up.

This repo exists because skills previously lived in two config dirs
(`~/.config/claude/skills` and `~/.config/opencode/skills`) and drifted. Now they live
here and are deployed out via [Kasetto](https://github.com/pivoshenko/kasetto) (`kst`), a
declarative, lock-first skills manager.

> **History:** deployment was previously handled by `skillsmgr`, which kept a central store
> and symlinked each agent's skills dir into it. It is retired; its scripts and the reasons
> for dropping it were removed in favour of git history — `git log --diff-filter=D --
> docs/skillsmgr-legacy/` finds them if ever needed.

## Mental model

Kasetto reads a declarative config (`kasetto/**/kasetto.yaml`), resolves each source, and
installs **real copies** into each agent's skills dir, recording exactly what it installed
in a committed `kasetto.lock`. There is no central store and no symlink layer.

```
this repo (source of truth)
  ├─ shared/  claude/  opencode/     hand-crafted skills (local sources)
  └─ kasetto/*.yaml  ──kst sync──▶   ~/.config/{claude,opencode}/skills/   (real copies)
                                     tracked by kasetto/**/kasetto.lock
```

The edit loop is: **edit a skill here → commit → a post-commit hook syncs the changed scope
→ the live copy refreshes.** Both the hook and `./scripts/kasetto-deploy.sh` re-resolve
local skills by name and leave every remote source pinned to the lock, so warm syncs stay
~instant and need no network. To deploy by hand, run `./scripts/kasetto-deploy.sh`.

## Layout

Hand-crafted skills are grouped by target agent. Each skill is a directory with a
`SKILL.md` (plus optional `references/`, `scripts/`, `ATTRIBUTIONS.md`).

| Group | Deployed to | Contents |
|---|---|---|
| `shared/` | Claude Code + OpenCode | Agent-agnostic skills (the majority) |
| `claude/` | Claude Code only | Claude-coupled skills (e.g. `reflect`) |
| `opencode/` | OpenCode only | OpenCode-coupled skills (e.g. `headroom-management`) |

Third-party skills used **as-is** are not vendored here — they are pulled from their upstream
repos by Kasetto and listed in `kasetto/base.yaml`, so they stay upstream-updatable.

A skill is vendored into a group only when it is **forked**: materially modified and no longer
tracking upstream. A fork keeps the upstream license in frontmatter `metadata.license` and
records provenance plus the list of changes in `ATTRIBUTIONS.md` (see `shared/git-master`,
`claude/claude-automation-recommender`). Forking trades upstream updates for the right to fix
the skill, so take that route only when the upstream cannot be used unmodified.

## The Kasetto config (`kasetto/`)

The deploy uses **four** configs. Kasetto's `extends` inherits a parent's skills only when
the child declares none — a child's own `skills:` *replaces* the parent's, and multi-parent
lists don't merge. Since `shared/` goes to both agents but the agent-coupled skills go to
one each, the two agent-specific skills can't ride on the shared base and need their own
configs.

| Config dir | What it deploys | Destination |
|---|---|---|
| `kasetto/base.yaml` | Common set: 25 third-party + `shared/` (local) | *(inherited, no destination)* |
| `kasetto/claude/` | `extends base.yaml` | `~/.config/claude/skills` |
| `kasetto/opencode/` | `extends base.yaml` | `~/.config/opencode/skills` |
| `kasetto/claude-extra/` | `claude/` group (e.g. `reflect`) | `~/.config/claude/skills` |
| `kasetto/opencode-extra/` | `opencode/` group (e.g. `headroom-management`) | `~/.config/opencode/skills` |

Two mechanics make the per-dir invocation load-bearing — `scripts/kasetto-deploy.sh` and the
post-commit hook both `cd` into each config dir before syncing:

- **Relative local sources resolve against the invoking cwd**, not the config file. So
  `base.yaml`'s `shared/` source is `../../shared` (correct from `kasetto/<agent>/`).
- **The lock is always named `kasetto.lock` and written to the cwd**, so each config keeps
  its own lock beside it.

An extra config targets the **same destination** as its base overlay. That is safe because
`kst sync` prunes only items in its *own* lock, so the two never delete each other's skills
(nor any pre-existing foreign skill already in the agent dir).

Unlike the old `skillsmgr` path, Kasetto needs **no `CLAUDE_CONFIG_DIR`** — each config
carries an explicit `~/.config/.../skills` destination (Kasetto expands `~`, but not `$VARS`).

## Deploy

```bash
./scripts/kasetto-deploy.sh              # sync all four configs to both agents
./scripts/kasetto-deploy.sh --dry-run    # preview without writing
./scripts/kasetto-deploy.sh --check      # audit each lock against its config (CI drift gate)
```

The script requires only `kst` on `PATH`. Set a `GITHUB_TOKEN` in your environment: a **cold**
sync clones ~13 upstream repos and can hit unauthenticated GitHub rate limits (it exits
non-zero and is safe to re-run). Warm syncs use the lock and touch no network.

## Adding a skill

**Hand-crafted:** create `shared/<name>/SKILL.md` (or under `claude/`/`opencode/` if
agent-coupled). No config edit is needed — the configs discover every skill in the group
via `skills: "*"`. But a plain `kst sync` **won't deploy a new skill**: it re-hashes only
skills already in the lock and does not re-resolve glob membership, so the commit hook and
`./scripts/kasetto-deploy.sh` alike report the new skill as absent. Deploy it with the
`--update` step in "Adding or removing a skill" below. Use the `skill-forge` skill for
authoring conventions.

**Third-party:** add a source entry to `kasetto/base.yaml` (Kasetto discovers skills in a
source's root or its `skills/` subdir; use `sub-dir:` for deeper layouts), then deploy.

## Editing a skill

Edit the files here and **commit** — the `post-commit` hook
(`scripts/sync-skills-kasetto.sh`, wired via `.pre-commit-config.yaml`) syncs whichever
scope the commit touched, so edits go live in both agents. Requires `pre-commit install`
once (bootstrap does this). Every file counts, so `references/`/`scripts/` edits propagate
too — not just `SKILL.md`.

The hook passes the touched skill names as `kst sync --project --update <name>`. That
matters: a plain `kst sync` trusts the locked hash and never re-reads a local source, so an
edited skill is reported `unchanged` and silently never deploys. Naming the skills
re-resolves only their sources, leaving third-party moving refs pinned.

## Adding or removing a skill

Changing which skills a `skills: "*"` glob source provides — **adding a new one or
deleting an existing one** — needs an `--update` the edit path doesn't. A plain `kst sync`
re-hashes only the skills already in the lock; it never re-resolves glob membership. So a
new skill deploys as absent and a deleted skill survives (reported `unchanged`, with its
lock entry and live copy intact). The post-commit hook re-resolves only the skills a commit
touched, and `./scripts/kasetto-deploy.sh` re-resolves only the local skills already
present in each scope's group, so neither picks up a membership change on its own.

After `git`-adding or `git rm`-ing the skill directory and committing, re-resolve glob
membership with `--update` for each affected scope — this adds new skills to the lock and
deploys them, and drops deleted skills from the lock and prunes their live copies:

```bash
for scope in claude opencode; do ( cd "kasetto/$scope" && kst sync --project --update ); done
```

Then commit the updated `kasetto.lock` files. `--update` also re-resolves moving refs on
third-party sources, so run it deliberately (or pass skill names, `--update <name>`, to
limit it to the sources you mean).

## Reproducibility & the lock

`kasetto.lock` records each skill's `source`, resolved `source_revision`, content `hash`,
and absolute `destination`. It is committed like `Cargo.lock`.

- **Drift detection, not frozen pins.** Sources without a `ref:` track `branch:main`; the
  lock's content hash lets `kst lock --check` (via `kasetto-deploy.sh --check`) flag when
  upstream `main` drifts from the locked snapshot. Add `ref: <tag-or-sha>` to a source to
  freeze it.
- **The lock bakes absolute destination paths** (this machine's home), so it is somewhat
  machine-specific; a fresh machine regenerates it on first sync.
- **No offline restore.** `kst sync --locked` needs a warm cache and can't rebuild a wiped
  deploy; reproducible restore is a plain `kst sync` (re-fetches at the locked revision).

## Fresh-machine bootstrap

```bash
git clone git@github.com:jonatsu/agent-skills.git ~/src/agent-skills
cd ~/src/agent-skills
cargo install kasetto            # provides `kst`
pre-commit install               # wires pre-commit checks + the post-commit redeploy hook
./scripts/kasetto-deploy.sh      # deploy the whole stack to both agents
```

## Coexistence & rollback

- **Foreign skills are left alone.** Any skill in an agent dir that Kasetto didn't install
  (e.g. ad-hoc `oh-my-opencode` skills) is untouched — scoped per-lock pruning never removes
  what isn't in the config's lock.
- **Rollback:** `kst clean` (per config dir) removes Kasetto-managed skills; deleting
  `kasetto/` and the store leaves nothing behind. Pre-migration copies remain in the
  `~/.config/claude` and `opencode-config` git histories.

## Licensing

Repo `LICENSE` is **MIT** and covers the original works here. Individual skills may carry
their own license via their frontmatter `metadata.license` and `ATTRIBUTIONS.md` — e.g.
`git-master` is **SUL 1.0** per its upstream. Do not assume MIT for a skill that declares
otherwise.

## Future work / TODOs

Tracked separately in [TODO.md](TODO.md).
