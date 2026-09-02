# Skills

Single source of truth for my agent skills, deployed to **Claude Code**, **OpenCode**,
**GitHub Copilot CLI** and **Codex** from one place. Edit a skill here once; every agent picks it up.

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

Kasetto reads a declarative config (`kasetto/base.yaml` plus the six overlays at
`kasetto/*/kasetto.yaml`), resolves each source, and
installs **real copies** into each agent's skills dir, recording exactly what it installed
in a committed `kasetto.lock`. There is no central store and no symlink layer.

```
this repo (source of truth)
  ├─ shared/<domain>/                hand-crafted skills (local sources)
  ├─ claude/  opencode/              these two groups stay flat
  └─ kasetto/ configs ──kst sync──▶  ~/.config/{claude,opencode}/skills/   (real copies, flat)
                                     ~/.copilot/skills/  ~/.codex/skills/
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
| `shared/` | Claude Code + OpenCode + Copilot CLI + Codex | Agent-agnostic skills (the majority), organised by domain one level down — see below |
| `claude/` | Claude Code only | Claude-coupled skills (e.g. `reflect`). Flat: two skills do not need a taxonomy |
| `opencode/` | OpenCode only | OpenCode-coupled skills. **Currently empty** — `headroom-management` was archived 2026-08-26, and git does not track empty directories, so the group is absent until the next OpenCode-only skill recreates it |
| `archived/` | nothing | Kept for reference, deployed nowhere. See `archived/README.md` |

There is no `copilot/` group. Copilot CLI gets `shared/` and nothing else: the Claude-only
skills are Claude-coupled by the placement rule — they are about `CLAUDE.md`, `.claude/agents`
and Claude subagents — so deploying them there would ship skills describing a different agent.
Add the group, and a `kasetto/copilot-extra/` config, the first time a Copilot-coupled skill
is written.

Codex also receives `shared/` and nothing agent-specific. Its built-in `.system` skills remain
platform-owned beside the Kasetto-managed global skills and are excluded by exact path from the
ownership gate.

### Domains within `shared/`

Since 2026-08-26 the shared group is organised by subject: `shared/<domain>/<skill>/`. Forty-three
skills in one directory had stopped being a list anyone could read.

| Domain | Holds |
|---|---|
| `agent-stack/` | Authoring the setup itself — skills, prompts, agent instruction files |
| `context/` | Context and token economy: handoffs, compression, token budgets |
| `design/` | Shaping and recording a design before it is built |
| `development/` | Doing the work: debugging, testing, dev-environment tooling |
| `review/` | Judging work already done — the brooks-lint lanes and security-audit |
| `embedded/` | Embedded Linux build systems and bring-up |
| `nix/` | Nix, NixOS, home-manager, and the flake ecosystem |
| `git/` | Git, GitHub, and repository hygiene |
| `ops/` | Machines and runtimes: containers, systemd, dotfiles |
| `writing/` | Human-facing prose |

**The domain level exists only in this repository.** Kasetto deploys flat, so every agent still
reads `<skills-dir>/<skill>/` and no skill needs to know where its source lives.

Three consequences worth knowing before you move anything:

- **A skill name MUST stay unique across all domains.** The lock records no domain, so two
  same-named skills collapse to one key and Kasetto silently deploys whichever it resolves last.
  `just skills-deployed` reports that as `ambiguous`; nothing else catches it.
- **Moving a skill between domains is free.** Lock keys are `../../shared::<name>`, so a `git mv`
  produces no lock diff. A lock diff after a pure move means something else changed.
- **Adding or emptying a domain needs a `kasetto/base.yaml` edit.** Kasetto discovers skills
  exactly one level under a source root, so each domain is its own `sub-dir:` entry there, and
  `sub-dir: "*"` is not supported. A named domain that does not exist fails the sync outright —
  which, since git does not track empty directories, is a failure that appears on the next clone
  rather than here.

Third-party skills used **as-is** are not vendored here — they are pulled from their upstream
repos by Kasetto and listed in `kasetto/base.yaml`, so they stay upstream-updatable.

A skill is vendored into a group only when it is **forked**: materially modified and no longer
tracking upstream. A fork keeps the upstream license in the top-level frontmatter `license` field and
records provenance plus the list of changes in `ATTRIBUTIONS.md` (see
`shared/agent-stack/agents-management`, `claude/claude-automation-recommender`). Forking trades upstream updates for the right to fix
the skill, so take that route only when the upstream cannot be used unmodified.

## The Kasetto config (`kasetto/`)

The deploy uses **seven** configs. Kasetto's `extends` inherits a parent's skills only when
the child declares none — a child's own `skills:` *replaces* the parent's, and multi-parent
lists don't merge. Since `shared/` goes to every agent but the agent-coupled skills go to
one each, those skills can't ride on the shared base and need their own configs.

| Config dir | What it deploys | Destination |
|---|---|---|
| `kasetto/base.yaml` | Common set: 24 third-party + `shared/` (local, one entry per domain) | *(inherited, no destination)* |
| `kasetto/claude/` | `extends base.yaml` | `~/.config/claude/skills` |
| `kasetto/opencode/` | `extends base.yaml` | `~/.config/opencode/skills` |
| `kasetto/copilot/` | `extends base.yaml` | `~/.copilot/skills` |
| `kasetto/codex/` | `extends base.yaml` | `~/.codex/skills` |
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

**Hand-crafted:** create `shared/<domain>/<name>/SKILL.md`, picking an existing domain (or
under `claude/`/`opencode/`, which are flat, if the skill is agent-coupled). No config edit is
needed — the configs discover every skill in the group via `skills: "*"`, and committing is
enough to deploy it: the post-commit hook re-resolves glob membership along with the content
hashes, so a new skill reaches every agent dir with no extra step. See "Adding or removing a
skill" below for why that works. Use the `skill-forge` skill for authoring conventions.

**A new domain is the one case that does need a config edit:** add a matching
`- source: ../../shared` / `sub-dir: <domain>` / `skills: "*"` entry to `kasetto/base.yaml`, in
the same commit that creates the directory.

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
- **Codex system skills remain platform-owned.** Kasetto does not claim or prune
  `~/.codex/skills/.system`; the ownership gate recognizes that exact built-in path.
- **Rollback:** `kst clean` (per config dir) removes Kasetto-managed skills; deleting
  `kasetto/` afterwards leaves nothing behind — there is no store to clear. Pre-migration
  copies remain in the `~/.config/claude` and `opencode-config` git histories.

## Licensing

Repo `LICENSE` is **MIT** and covers the original works here. Individual skills may carry
their own license via their top-level frontmatter `license` field and `ATTRIBUTIONS.md` — e.g.
`agents-management` is **Apache-2.0** per its upstream, and ships `LICENSE.upstream`
alongside. Do not assume MIT for a skill that declares otherwise. A skill whose upstream
licence would block the use we need is replaced by an independently written one rather than
adapted: `git-master` (SUL 1.0, personal/non-commercial only) was retired on 2026-08-26 in
favour of `shared/git/git-operations`, which is MIT.

## External references on skill authoring

Consulted on **2026-08-27** to settle a dispute about how skills should be structured, and
recorded here so the next reader does not re-find them. Each is pinned, because an unpinned
citation to a moving document is not evidence.

| Source | What it settles | Pinned at |
|---|---|---|
| [Anthropic, *Skill authoring best practices*](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | The platform vendor's own guidance, and the strongest anchor available | read 2026-08-27 |
| [Claude Code skills reference](https://code.claude.com/docs/en/skills) | The real frontmatter field list, and which fields belong to which surface | read 2026-08-27 |
| [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) | A short opinionated distillation that defers to Anthropic's guide | commit `a0bfa56` |
| [mgechev/skillgrade](https://github.com/mgechev/skillgrade) | Not read in depth. An external grading tool that evaluates skills by running them against fixtures with graders; useful as a comparison point for behavioral evaluation, but not treated here as an authority | unpinned |

The Agent Skills specification is the structural authority. `skill-forge`'s vendored reference
validator checks that contract; its local validator separately checks this repository's policy.
Line counts, reference depth, tables of contents, prose person, and package shape can inform a
review when they cause a concrete problem, but they are not universal quality gates.

**What neither has, and the finding that mattered most: no taxonomy of skill types, shapes,
categories or tiers.** Anthropic's guide legislates character sets, description person and
nesting depth, so a five-way type system is not something it would have left out by accident.
That absence — together with the fact that three of `skill-review`'s five former "shapes" were
re-scoring other dimensions — is why the shape taxonomy and the four complexity tiers were
deleted on 2026-08-27. The current `skill-forge` instead treats sequence, branching, iteration,
delegation, degradation, and templates as conditional workflow mechanisms rather than skill
categories.

**Two places they are wrong, or narrower than they read.** mgechev's
`scripts/validate-metadata.py` rejects any first- or second-person pronoun in a description;
measured against this repo's six `agent-stack` skills it fired on three, **every one a false
positive**, because the pronouns sat inside quoted user utterances (`'my CLAUDE.md is too
long'`) — which is exactly what a trigger list should contain. And Anthropic's ban on
`anthropic`/`claude` in a skill name binds claude.ai uploads and the Skills API, not Claude
Code: this repo's own `claude-automation-recommender` is deployed and working, so
`quick_validate.py` warns rather than fails.

## Future work / TODOs

Tracked separately in [TODO.md](TODO.md).
