# Skills

Single source of truth for my agent skills, deployed as real copies to Claude Code, GitHub Copilot CLI and
Codex. Edit a skill here once, commit, and every supported agent picks it up.

[Kasetto](https://github.com/pivoshenko/kasetto) (`kst`) does the deploying. It reads the declarative configs
under `kasetto/`, resolves each source, installs real copies into each agent's skills directory, and records
what it installed in a committed `kasetto.lock`. No central store, no symlink layer.

```text
this repo (source of truth)
  ├─ shared/<domain>/                hand-crafted skills (local sources)
  ├─ claude/                         agent-specific skills (flat)
  └─ kasetto/ configs ──kst sync──▶  ~/.config/claude/skills/   (real copies, flat)
                                     ~/.copilot/skills/  ~/.codex/skills/
                                     tracked by kasetto/**/kasetto.lock
```

**What this does not do.** It does not run anywhere but this machine: the locks bake absolute destination
paths, and the destinations are hard-coded per agent. Real copies can drift from their source, which is why
half of this document is about detecting that. And this file describes the *mechanism*;
[AGENTS.md](AGENTS.md) sets the rules an agent must follow here and wins wherever the two overlap.

Skills are one part of the repository — see [../README.md](../README.md) for the rest.
Skill reviews, comparisons, and repair evidence live under
[../docs/evaluations/skills/](../docs/evaluations/skills/); the dated records preserve their original verdicts.

## Does it work

`just skills-deployed` reads every destination and compares each deployed copy against its committed source:

Run `just skills-deployed` and require zero drift, pending files, backups, remote mismatches, or unresolved
entries.

A remote-sourced skill has no copy under `skills/`, so neither skill validator can see it. Its protection is
approval instead: every remote source is pinned to a reviewed commit recorded in
`kasetto/third-party-skills.yaml`, and `just skills-deployed` reports `REMOTE-MISMATCH` when a deployed remote
skill's lock is not at that commit.

One skill, itemised per destination. Use this rather than a hand-written `diff -rq`, which silently checks
only the destinations you remembered to list:

Run `just skills-deployed --skill git-commits-and-recovery --verbose`; require one `ok` line for every locked
destination and zero drift, pending files, backups, remote mismatches, or unresolved entries.

A name no lock carries exits 2 rather than passing vacuously, so a typo and a genuinely pruned skill both
fail loudly. That failure is how you confirm a removal actually pruned.

Both skill validators over one package:

```console
$ just skill-check skills/shared/tools/git-commits-and-recovery
Agent Skills specification (skills-ref)

1 checked, 0 failed
Skill Forge local policy (quick_validate)

1 checked, 0 failed, 0 with warnings
```

Running only one of them is the mistake the pair exists to prevent: the specification validator passes a file
that breaks every repository policy, and the policy validator does not look at frontmatter shape at all.

## Everyday workflow

The edit loop is **edit here → commit → the post-commit hook syncs the touched scope → `just skills-sync`**.
`pre-commit install` wires that hook (`scripts/sync-skills-kasetto.sh`) alongside the pre-commit checks. Use
the `skill-forge` skill for authoring conventions and for reviews.

### Editing a skill

Edit the files and commit. The hook maps the commit's changed paths to Kasetto scopes and redeploys them, so
edits go live in every supported agent. Every file in the package counts — `references/` and `scripts/`
propagate the same as `SKILL.md`.

Then run **`just skills-sync`**. The redeploy rewrites the scope's `kasetto.lock`, leaving it dirty in an
otherwise clean tree; the recipe settles it with a warm redeploy and a `chore(kasetto):` commit of the locks
alone, staged by explicit path. It never runs `git add -A`, because this checkout is often open in more than
one agent session, and it refuses outright if the index already holds staged changes it did not put there.
Skipping it is safe in the moment — the skills are already live — but a stale committed lock defeats the
`kst lock --check` drift gate the lock exists for.

**A skill edit is always two commits.**

### Adding a skill

Create `shared/<domain>/<name>/SKILL.md`, or a flat directory under `claude/` if the skill is Claude-coupled.
A skill that only works in this repository goes under [repo-local skills](#repo-local-skills) instead.
Then `git add` and commit; that is the whole procedure. The configs discover group
members through `skills: "*"`, so no config edit is needed and the hook deploys the new skill.

**A new domain is the one case that does need a config edit:** add a matching `source: ../../shared` /
`sub-dir: <domain>` / `skills: "*"` entry to `kasetto/base.yaml`, in the same commit that creates the
directory. Kasetto discovers skills exactly one level under a source root, and `sub-dir: "*"` is not
supported. The reverse holds too: removing the last skill from a domain must remove its `base.yaml` entry in
the same commit, because a configured domain that does not exist fails the deploy outright — and since git does
not track empty directories, that failure surfaces on someone's next clone rather than here. On this machine it
can stay hidden: from kasetto 3.9.0 a bare `kst sync` trusts the lock, reports the stale skill `unchanged` and
exits 0, while `./scripts/kasetto-deploy.sh` (which passes `--update`), a fresh clone's first sync, and
`just locks` all fail with `source sub-dir not found`. Re-verified on 3.9.0, 2026-09-27.

A third-party skill used as-is is not vendored: it stays a remote source entry in `kasetto/base.yaml`, pinned
to the upstream commit you reviewed. Vendor a copy into a group only when it is *forked* — materially modified
and no longer tracking upstream — which trades upstream updates for the right to fix the skill.

### Adding or updating a third-party skill

Pinned sources never update on their own. `just skills-updates` reports which approved skills changed upstream
since their approved commit, counting only files under each skill's own folder; it needs network, and
`GITHUB_TOKEN` avoids GitHub's rate limit. Approval and pin then change together, in one commit, and the
pre-commit hook enforces it:

1. Review the upstream skill at one commit: read the repository's `LICENSE`, check for scripts and hidden
   Unicode, and note the full 40-character commit id.
2. In `kasetto/base.yaml`, set the entry's `ref:` to that commit. Do not add `branch:`; Kasetto ignores it once
   `ref:` is set.
3. In `kasetto/third-party-skills.yaml`, add or update the entry keyed by the exact same URL: the same
   `commit`, the upstream `branch` to watch, a quoted ISO `reviewed_on` date, and a `reason` that says what you
   reviewed.
4. Commit both files. `just skills-sources` runs as a pre-commit hook and rejects a remote source that is
   unpinned, unapproved, or pinned to a different commit, and an approval whose source is gone, before the
   post-commit deploy can run.
5. Run `just skills-sync` for the lock-only follow-up commit, then confirm with `just skills-deployed`. The
   post-commit deploy relocks any remote skill whose lock lags its new pin, which Kasetto would otherwise skip
   when the upstream content is identical. A `REMOTE-MISMATCH` here means that deploy did not run or failed;
   re-run `./scripts/kasetto-deploy.sh`.

Removing a third-party skill removes its `base.yaml` entry and its approval in the same commit.

### Removing a skill

`git rm` the directory and commit. The hook drops it from the lock and prunes the live copies. Settle the
lock with `just skills-sync`, then confirm the prune with `just skills-deployed --skill <name> --verbose`
and its exit-2 answer. Archiving instead of deleting has its own procedure in
[archived/README.md](archived/README.md).

**Why a bare add or remove works at all**, since the mechanism is not obvious and an earlier note here got it
wrong: `--update <name>` maps a name to a source *through the lock*, so a brand-new skill matches no source
and re-resolves nothing. Naming the new skill is useless. But per `kst sync --help`, *"updating one asset from
a multi-asset source re-resolves that whole source"*, and the local groups are globs.
`scripts/kasetto-deploy.sh` names **every** local skill in the scope's group, so an already-locked sibling
re-reads the glob from disk and the membership change rides along. Measured 2026-08-23 in both directions,
offline, in single-digit milliseconds.

A bare `kst sync --project --update` re-resolves membership too, but re-resolves moving refs on the remote
sources as well — so reach for it only when pulling upstream drift is what you actually want.

## Fresh machine

```bash
git clone git@github.com:jonatsu/agent-setup.git ~/src/agent-setup
cd ~/src/agent-setup
cargo install kasetto            # provides `kst`
pre-commit install               # pre-commit checks plus the post-commit redeploy hook
just deploy                      # skills to supported agents, plus the dotbot map
```

`just deploy` is skills *and* the dotbot map, which is what puts the Copilot CLI configuration in `~/.copilot`
and the knowledge-vault tooling in `~/.local/share/`. Skills alone are `just deploy-skills`.

A cold sync clones whatever remote sources `kasetto/base.yaml` declares, and unauthenticated GitHub clones are
rate-limited, so set a `GITHUB_TOKEN` first. It exits non-zero and is safe to re-run. Warm syncs resolve from
the lock and touch no network.

**This is the only place that requirement is stated.** How much it matters scales with how many remote sources
`base.yaml` declares: with the few remote sources it carries today, an unauthenticated clone will usually
succeed, and the token is cheap insurance. Add sources and it stops being optional. Read `base.yaml` for the
current set rather than assuming either extreme.

```bash
just deploy-skills                       # skills only: every supported target
./scripts/kasetto-deploy.sh --dry-run    # preview without writing
./scripts/kasetto-deploy.sh --check      # audit each lock against its config (CI drift gate)
```

## Layout

Each skill is a directory with a `SKILL.md`, plus optional `references/`, `scripts/` and `ATTRIBUTIONS.md`.
Hand-crafted skills are grouped by which agents get them.

| Group       | Deployed to                       | Contents                                                         |
| ----------- | --------------------------------- | ---------------------------------------------------------------- |
| `shared/`   | Claude Code + Copilot CLI + Codex | Agent-agnostic skills, organised by domain one level down        |
| `claude/`   | Claude Code only                  | Claude-coupled skills. Flat: too few to need a taxonomy          |
| `archived/` | nothing                           | Kept for reference. See [archived/README.md](archived/README.md) |

There is no `copilot/` group. Copilot CLI gets `shared/` and nothing else, because the Claude-only skills are
about `CLAUDE.md`, `.claude/agents` and Claude subagents — deploying them there would ship skills describing a
different agent. Add the group, and a `kasetto/copilot-extra/` config, the first time a Copilot-coupled skill
is written. Codex likewise receives `shared/` only; its built-in `.system` skills sit beside the
Kasetto-managed ones and are excluded by exact path from the ownership gate.

### Repo-local skills

A skill that only works inside this repository, such as `session-skill-audit`, is not deployed globally. Its one real
directory is `../.agents/skills/<name>/`, where Codex discovers project skills. `../.claude/skills/<name>` and
`../.github/skills/<name>` are relative symlinks to it, for Claude Code and Copilot CLI. The clients read it
straight from the checkout, so Kasetto, the locks, and `just skills-deployed` do not cover it, and an edit needs
no `just skills-sync`. Both validators and the name-uniqueness check still scan it. Claude Code and Codex were
confirmed to discover `session-skill-audit` through this layout on 2026-09-28; Copilot CLI has not been checked yet.

The [scoped Python rule](../agents/shared/rules/python.md) routes work by concern.
[python-style](shared/development/python/python-style/SKILL.md) owns everyday coding defaults;
specialist Python skills own their procedures. Each skill preserves established project conventions and requires
evidence of harm before recommending an unsolicited correction.

### Domains within `shared/`

Skills live at `shared/<domain>/<skill>/`; one flat directory had stopped being a list anyone could read.
`kasetto/base.yaml` lists the eager domains, one entry each, and the `kasetto/lazy/` and `kasetto/claude-lazy/`
scopes list the lazy ones.

| Domain                   | Holds                                                                                           |
| ------------------------ | ----------------------------------------------------------------------------------------------- |
| `agents/`                | Working with agents: prompts, instruction files, context economy, handoffs, the CC safety net   |
| `skills-for-skills/`     | Skill lifecycle: authoring, review, descriptions and triggers, deployment                       |
| `engineering/`           | Shaping ideas, requirements, and technical design before work is built                          |
| `development/`           | Everyday dev craft: coding standards, shells, containers, generated-file checks                 |
| `development/python/`    | Python craft: style, typing, testing, async, architecture, project management                   |
| `development/nix/`       | Nix and NixOS: flakes, packaging, secrets, home-manager, direnv                                 |
| `tools/`                 | Focused tool use: ast-grep, Git, GitHub, task runners, mise, repo hygiene, dotfiles             |
| `review/`                | Reviewing code for security and specification conformance                                       |
| `code-health/`           | Codebase health sweeps and repair — the Brooks-based audit, debt, review, sweep and test skills |
| `testing-and-qa/`        | Verifying behaviour: debugging, TDD, test engineering                                           |
| `system-administration/` | Machines and runtimes: systemd, networking                                                      |
| `embedded-linux/`        | Embedded Linux bring-up, Buildroot, kas, U-Boot, Yocto/OpenEmbedded                             |
| `technical-writing/`     | Human-facing prose                                                                              |

`development/python/` and `development/nix/` are nested groups: a second directory level under `development/`,
next to the skills that sit directly in it. Each nested group is its own Kasetto entry, since Kasetto
discovers skills exactly one level under a source root and a `sub-dir: development` entry skips both groups
silently rather than failing on them.

The lazy domains are rarely needed ones. Claude loads them natively, while Codex and Copilot reach them only
through `lazy-skills-server`, which serves them on demand.
[Its README](../src/tools/lazy-skills-server/README.md) covers how the tier works and how to move a domain into
or out of it.

**The domain level exists only in this repository.** Kasetto deploys flat, so every supported agent reads
`<skills-dir>/<skill>/` and no skill needs to know where its source lives. Two consequences:

- **A skill name must stay unique across every domain.** The lock records no domain, so its keys are
  `../../shared::<name>` and two same-named skills collapse to one key — Kasetto then deploys whichever it
  resolved last, silently. `just skills-deployed` reports that as `ambiguous`; nothing else catches it.
- **Moving a skill between domains is free.** Same lock keys, so a `git mv` produces no lock diff. A lock diff
  after a pure move means something else changed.

## How the deploy works

`kasetto/base.yaml` carries the shared skill list and no destination. One config directory per deploy scope
extends it and adds a destination: one per agent for the shared set, plus an `-extra` scope for each
agent-coupled group. `kasetto/` is the authoritative list.

The extra scopes exist because Kasetto's `extends` inherits a parent's skills only when the child declares
none — a child's own `skills:` *replaces* the parent's, and multi-parent lists do not merge. So agent-coupled
skills cannot ride on the shared base. An extra scope targets the **same destination** as its base overlay,
which is safe: `kst sync` prunes only items in its *own* lock, so the two never delete each other's skills,
nor any pre-existing foreign skill already in the agent's directory.

Two mechanics make the per-directory invocation load-bearing — `scripts/kasetto-deploy.sh` and the post-commit
hook both `cd` into each config directory before syncing:

- **Relative local sources resolve against the invoking cwd**, not the config file. That is why `base.yaml`'s
  shared source is `../../shared`, which is correct from `kasetto/<scope>/`.
- **The lock is always named `kasetto.lock` and written to the cwd**, so each scope keeps its own lock beside
  its config.

Every destination is an explicit tilde path rather than a Kasetto preset. Kasetto expands `~` but not `$VARS`.
The `claude-code` preset targets `~/.claude/skills` and ignores `CLAUDE_CONFIG_DIR`, which is the wrong
directory here; the `github-copilot` preset additionally claims `~/.copilot/copilot-instructions.md` as a file
it generates, and dotbot deploys that file.

The hook does not run a plain `kst sync`. It delegates to `./scripts/kasetto-deploy.sh --scope <name>`, which
names every local skill in that scope as `kst sync --project --update <name>...`. **That matters: a plain
`kst sync` trusts the locked hash and never re-reads a local source, so an edited skill is reported
`unchanged` and silently never deploys.** Naming the local skills re-resolves only their sources and leaves
remote moving refs pinned, which is also why warm syncs need no network.

## The lock

`kasetto.lock` records each skill's `source`, resolved `source_revision`, content `hash`, and absolute
`destination`. It is committed, like `Cargo.lock`.

- **Drift detection, not frozen pins.** A source without a `ref:` tracks `branch:main`; the content hash lets
  `kst lock --check` flag when upstream drifts from the locked snapshot. Add `ref: <tag-or-sha>` to freeze one.
- **Absolute destinations are baked in**, so the lock is somewhat machine-specific. A fresh machine
  regenerates it on first sync.
- **No offline restore.** `kst sync --locked` needs a warm cache and cannot rebuild a wiped deploy. The
  reproducible restore is a plain `kst sync`, which re-fetches at the locked revision.
- **Foreign skills are left alone.** Anything in an agent's directory that Kasetto did not install is
  untouched, because pruning is scoped to the config's own lock. Codex's `~/.codex/skills/.system` is
  platform-owned on the same principle.
- **Rollback** is `kst clean` per config directory; deleting `kasetto/` afterwards leaves nothing behind,
  because there is no store to clear.

## When a skill did not deploy

Start with `kst lock --check` (via `just check`), the backstop for membership drift: it exits 1 and names the
offender, for example `+ ../../shared::my-new-skill`. Then match the symptom.

| Symptom                                                                              | Read                                          |
| ------------------------------------------------------------------------------------ | --------------------------------------------- |
| A skill edit deployed nothing, `kst` reports `unchanged`, or a lock looks stale      | `../docs/findings/kasetto-deploy.md`          |
| A move, archive or removal left a destination wrong, or a description broke the lock | `../docs/findings/skills-hook-and-pruning.md` |
| A validated skill never activates, or you need to measure whether one did            | `../docs/findings/skill-discovery-limits.md`  |

**Do not accept the post-commit hook's exit status, a clean `git status`, or `kst`'s own report as evidence
that a deployed copy changed or disappeared.** All three answer from somewhere other than the destination.
Only `just skills-deployed` reads the destination.

## Licensing

Repository `LICENSE` is MIT and covers the original works here. A skill may carry its own license in its
top-level frontmatter `license` field with provenance and changes in `ATTRIBUTIONS.md` — `agents-context-docs`
is Apache-2.0 per its upstream and ships `LICENSE.upstream` alongside. Do not assume MIT for a skill that
declares otherwise.

Where an upstream licence would block the use we need, the skill is replaced by an independently written one
rather than adapted. `shared/tools/git-commits-and-recovery` is the worked example: its predecessor was SUL
1.0, personal/non-commercial only.

## External references on skill authoring

Consulted on 2026-08-27 to settle a dispute about how skills should be structured, and recorded so the next
reader does not re-find them. Each is pinned, because an unpinned citation to a moving document is not
evidence.

| Source                                                                                                                          | What it settles                                                           | Pinned at        |
| ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------- |
| [Anthropic, *Skill authoring best practices*](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | The platform vendor's own guidance, and the strongest anchor available    | read 2026-08-27  |
| [Claude Code skills reference](https://code.claude.com/docs/en/skills)                                                          | The real frontmatter field list, and which fields belong to which surface | read 2026-08-27  |
| [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices)                                               | A short opinionated distillation that defers to Anthropic's guide         | commit `a0bfa56` |
| [mgechev/skillgrade](https://github.com/mgechev/skillgrade)                                                                     | A comparison point for behavioral evaluation, not an authority; see below | unpinned         |

`skillgrade` was not read in depth. It is an external grading tool that evaluates skills by running them against
fixtures with graders.

The Agent Skills specification is the structural authority. `skill-forge`'s vendored reference validator checks
that contract; its local validator separately checks this repository's policy. Line counts, reference depth,
tables of contents, prose person and package shape can inform a review when they cause a concrete problem, but
they are not universal quality gates.

**Neither source defines a taxonomy of skill types, shapes, categories or tiers**, and that absence is why
`skill-forge` has none. Anthropic's guide legislates character sets, description person and nesting depth, so
a type system is not something it would have left out by accident. `skill-forge` treats sequence, branching,
iteration, delegation, degradation and templates as conditional workflow mechanisms rather than skill
categories.

Two places these sources are wrong, or narrower than they read:

- mgechev's `scripts/validate-metadata.py` rejects any first- or second-person pronoun in a description.
  Measured against this repository's `agent-stack` skills it fired only on false positives, because the
  pronouns sat inside quoted user utterances (`'my CLAUDE.md is too long'`) — which is exactly what a trigger
  list should contain.
- Anthropic's ban on `anthropic`/`claude` in a skill name binds claude.ai uploads and the Skills API, not
  Claude Code. This repository's `claude-code-setup-audit`, archived 2026-09-28, deployed and worked under that
  prefix, so
  `quick_validate.py` warns rather than fails. The warning was not observed during the 2026-09-03 rename, but
  the validator was being reworked concurrently, so treat that as unconfirmed rather than as changed.

## Where to go next

- [AGENTS.md](AGENTS.md) — the rules for agents working here, and the normative source wherever it overlaps
  with this file
- [TODO.md](TODO.md) — operational backlog, review ledgers and unevaluated candidate sources
- [archived/README.md](archived/README.md) — the archive procedure and recovery commands
- [../README.md](../README.md) — the rest of the repository, including the shared toolchain this directory
  inherits
