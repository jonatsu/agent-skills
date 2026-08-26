# Skills

Single source of truth for my agent skills, deployed to **Claude Code**, **OpenCode** and
**GitHub Copilot CLI** from one place. Edit a skill here once; every agent picks it up.

The skills previously lived in two config dirs (`~/.config/claude/skills` and
`~/.config/opencode/skills`) and drifted. Now they live here and deploy out via
[Kasetto](https://github.com/pivoshenko/kasetto) (`kst`), a declarative, lock-first skills
manager.

This directory is where the repository started, as `agent-skills`. It was renamed to
`agent-setup` on 2026-08-21 to become the base the other config repositories merge into, so
the repository is no longer only skills — see [../README.md](../README.md) for the whole of
it, and [../docs/plans/repo-consolidation.md](../docs/plans/repo-consolidation.md) for what
has merged and what has not.

> **History:** deployment was previously handled by `skillsmgr`, which kept a central store
> and symlinked each agent's skills dir into it. It is retired; its scripts and the reasons
> for dropping it were removed in favour of git history — `git log --diff-filter=D --
> docs/skillsmgr-legacy/` finds them if ever needed.

## Mental model

Kasetto reads a declarative config (`kasetto/base.yaml` plus the five overlays at
`kasetto/*/kasetto.yaml`), resolves each source, and
installs **real copies** into each agent's skills dir, recording exactly what it installed
in a committed `kasetto.lock`. There is no central store and no symlink layer.

```
this repo (source of truth)
  ├─ shared/  claude/  opencode/     hand-crafted skills (local sources)
  └─ kasetto/ configs ──kst sync──▶  ~/.config/{claude,opencode}/skills/   (real copies)
                                     ~/.copilot/skills/
                                     tracked by kasetto/**/kasetto.lock
```

The edit loop is: **edit a skill here → commit → a post-commit hook syncs the changed scope
→ the live copy refreshes.** The hook delegates to `./scripts/kasetto-deploy.sh`, which
re-resolves local skills by name and leaves every remote source pinned to the lock, so warm
syncs stay ~instant and need no network. To deploy by hand, run the same script.

## Layout

Hand-crafted skills are grouped by target agent. Each skill is a directory with a
`SKILL.md` (plus optional `references/`, `scripts/`, `ATTRIBUTIONS.md`).

| Group | Deployed to | Contents |
|---|---|---|
| `shared/` | Claude Code + OpenCode + Copilot CLI | Agent-agnostic skills (the majority) |
| `claude/` | Claude Code only | Claude-coupled skills (e.g. `reflect`) |
| `opencode/` | OpenCode only | OpenCode-coupled skills. **Currently empty** — `headroom-management` was archived 2026-08-26, and git does not track empty directories, so the group is absent until the next OpenCode-only skill recreates it |
| `archived/` | nothing | Kept for reference, deployed nowhere. See `archived/README.md` |

There is no `copilot/` group. Copilot CLI gets `shared/` and nothing else: the Claude-only
skills are Claude-coupled by the placement rule — they are about `CLAUDE.md`, `.claude/agents`
and Claude subagents — so deploying them there would ship skills describing a different agent.
Add the group, and a `kasetto/copilot-extra/` config, the first time a Copilot-coupled skill
is written.

Third-party skills used **as-is** are not vendored here — they are pulled from their upstream
repos by Kasetto and listed in `kasetto/base.yaml`, so they stay upstream-updatable.

A skill is vendored into a group only when it is **forked**: materially modified and no longer
tracking upstream. A fork keeps the upstream license in frontmatter `metadata.license` and
records provenance plus the list of changes in `ATTRIBUTIONS.md` (see
`shared/agents-management`, `claude/claude-automation-recommender`). Forking trades upstream updates for the right to fix
the skill, so take that route only when the upstream cannot be used unmodified.

## The Kasetto config (`kasetto/`)

The deploy uses **six** configs. Kasetto's `extends` inherits a parent's skills only when
the child declares none — a child's own `skills:` *replaces* the parent's, and multi-parent
lists don't merge. Since `shared/` goes to every agent but the agent-coupled skills go to
one each, those skills can't ride on the shared base and need their own configs.

| Config dir | What it deploys | Destination |
|---|---|---|
| `kasetto/base.yaml` | Common set: 24 third-party + `shared/` (local) | *(inherited, no destination)* |
| `kasetto/claude/` | `extends base.yaml` | `~/.config/claude/skills` |
| `kasetto/opencode/` | `extends base.yaml` | `~/.config/opencode/skills` |
| `kasetto/copilot/` | `extends base.yaml` | `~/.copilot/skills` |
| `kasetto/claude-extra/` | `claude/` group (e.g. `reflect`) | `~/.config/claude/skills` |
| `kasetto/opencode-extra/` | `opencode/` group — **empty since 2026-08-26**, scope kept deliberately | `~/.config/opencode/skills` |

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
carries an explicit tilde destination (Kasetto expands `~`, but not `$VARS`). The Copilot
overlay names its destination rather than using Kasetto's `github-copilot` preset, because
that preset also claims `~/.copilot/copilot-instructions.md` as a file it generates, and
dotbot deploys that file from `copilot/`.

## Deploy

The root `justfile` is the entry point. `just deploy` runs the Kasetto sync **and** the dotbot
map, which is what puts the Copilot CLI configuration in `~/.copilot` and the knowledge-vault
tooling in `~/.local/share/` — skills alone are not the whole deploy any more.

```bash
just deploy                              # skills + the dotbot map
just deploy-skills                       # skills only: sync every config to every agent
./scripts/kasetto-deploy.sh --dry-run    # preview without writing
./scripts/kasetto-deploy.sh --check      # audit each lock against its config (CI drift gate)
```

The script requires only `kst` on `PATH`. Set a `GITHUB_TOKEN` in your environment: a **cold**
sync clones 12 upstream sources across 9 repositories and can hit unauthenticated GitHub rate
limits (it exits non-zero and is safe to re-run). Warm syncs use the lock and touch no network.

## Adding a skill

**Hand-crafted:** create `shared/<name>/SKILL.md` (or under `claude/`/`opencode/` if
agent-coupled). No config edit is needed — the configs discover every skill in the group
via `skills: "*"`, and committing is enough to deploy it: the post-commit hook re-resolves
glob membership along with the content hashes, so a new skill reaches every agent dir with
no extra step. See "Adding or removing a skill" below for why that works. Use the
`skill-forge` skill for authoring conventions.

**Third-party:** add a source entry to `kasetto/base.yaml` (Kasetto discovers skills in a
source's root or its `skills/` subdir; use `sub-dir:` for deeper layouts), then deploy.

## Editing a skill

Edit the files here and **commit**, then run **`just skills-sync`**. The `post-commit` hook
(`scripts/sync-skills-kasetto.sh`, wired via `.pre-commit-config.yaml`) syncs whichever
scope the commit touched, so edits go live in every agent. Requires `pre-commit install`
once (bootstrap does this). Every file counts, so `references/`/`scripts/` edits propagate
too — not just `SKILL.md`.

That deploy rewrites the scope's `kasetto.lock`, leaving it dirty in an otherwise clean
commit. `just skills-sync` settles it: warm redeploy, then a `chore(kasetto):` commit of
the locks alone, staged by explicit path (never `git add -A` — the checkout is often open
in more than one agent session, and it refuses if the index already holds staged changes
it did not put there). Skipping the recipe is safe in the moment, since the skills are
already live, but a stale committed lock defeats the `kst lock --check` drift gate the
lock exists for.

The hook maps the commit's changed paths to Kasetto scopes and delegates to
`./scripts/kasetto-deploy.sh --scope <name>`, which names every local skill in that scope's
group as `kst sync --project --update <name>...`. That matters: a plain `kst sync` trusts the
locked hash and never re-reads a local source, so an edited skill is reported `unchanged` and
silently never deploys. Naming the local skills re-resolves only their sources, leaving
third-party moving refs pinned.

## Adding or removing a skill

`git add` (or `git rm`) the skill directory and commit. That is the whole procedure: the
post-commit hook adds a new skill to the lock and deploys it, and drops a deleted one from
the lock and prunes its live copies. Settle the resulting `kasetto.lock` changes with
`just skills-sync`, the same as for an edit.

**Why that works**, because the mechanism is not obvious and the old note here got it wrong:
`--update <name>` maps a name to a source **through the lock**, so a brand-new skill — which
is in no lock — matches no source and re-resolves nothing. Naming the new skill is therefore
useless. But per `kst sync --help`, *"updating one asset from a multi-asset source re-resolves
that whole source"*, and the local groups are `skills: "*"` globs. `kasetto-deploy.sh` names
**every** local skill in the group, so an already-locked sibling re-reads the glob from disk
and the membership change comes with it. Measured 2026-08-23 in both directions, offline and
in single-digit ms.

A bare `kst sync --project --update` also re-resolves membership, but re-resolves moving refs
on the remote third-party sources too — so reach for it only when pulling upstream drift is
what you actually want.

If a skill ever fails to appear, `kst lock --check` (via `just check`) is the backstop: it
exits 1 on membership drift and names the offender, e.g. `+ ../../shared::my-new-skill`.

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
git clone git@github.com:jonatsu/agent-setup.git ~/src/agent-setup
cd ~/src/agent-setup
cargo install kasetto            # provides `kst`
pre-commit install               # wires pre-commit checks + the post-commit redeploy hook
just deploy                      # skills to every agent, plus the dotbot map
```

## Coexistence & rollback

- **Foreign skills are left alone.** Any skill in an agent dir that Kasetto didn't install
  (e.g. ad-hoc `oh-my-opencode` skills) is untouched — scoped per-lock pruning never removes
  what isn't in the config's lock.
- **Rollback:** `kst clean` (per config dir) removes Kasetto-managed skills; deleting
  `kasetto/` afterwards leaves nothing behind — there is no store to clear. Pre-migration
  copies remain in the `~/.config/claude` and `opencode-config` git histories.

## Licensing

Repo `LICENSE` is **MIT** and covers the original works here. Individual skills may carry
their own license via their frontmatter `metadata.license` and `ATTRIBUTIONS.md` — e.g.
`agents-management` is **Apache-2.0** per its upstream, and ships `LICENSE.upstream`
alongside. Do not assume MIT for a skill that declares otherwise. A skill whose upstream
licence would block the use we need is replaced by an independently written one rather than
adapted: `git-master` (SUL 1.0, personal/non-commercial only) was retired on 2026-08-26 in
favour of `shared/git-operations`, which is MIT.

## Future work / TODOs

Tracked separately in [TODO.md](TODO.md).
