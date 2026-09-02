## When to load this file

Load this first for any mise task. It gives the mental model, the decision tree, and the official constraints
that shape every later choice.

## Mise in one page

Mise is a unified tool manager, environment loader, and task runner.

MUST pointer for latest upstream docs:

- `https://raw.githubusercontent.com/jdx/mise/refs/heads/main/llms.txt`

Use that file when freshness matters. It is the upstream LLM-friendly documentation pointer. Treat its
contributing and codebase-architecture sections as upstream internal workflow, not primary guidance for
ordinary mise setup or operations.

Core surfaces:

- tool installation and version selection via `mise.toml`
- environment loading via `[env]` and `env._*` directives
- task execution via `[tasks]` or file tasks
- trust and reproducibility via `mise trust`, `min_version`, and `mise.lock`

Official docs researched from `jdx/mise` main docs tree, current at release `v2026.7.2`.

## Decision tree

Ask in this order:

1. Does this need a shared project environment, a personal machine default, CI bootstrap, or a baked image?
2. Does this workflow need prompt activation, shims, or only command-scoped execution?
3. Does this need exact reproducibility or only a convenient local setup?
4. Does the repo need tasks, hooks, or only tool installs?

## Safe defaults

- Prefer project-local `mise.toml` over global config.
- Prefer `mise exec -- <command>` over shell mutation when automation or agents are involved.
- Prefer committed `mise.toml` plus `mise.lock` for shared reproducibility.
- Prefer `mise.local.toml` for local secrets or developer-specific overrides.
- Prefer file tasks for larger task logic.

## Important facts

- Trust matters. Untrusted config blocks env directives, hooks, and tasks.
- `mise use` writes config. It does not guarantee the current script can immediately call the tool unless you
  also use `mise exec --` or refresh env.
- `mise activate` is interactive-shell oriented. `mise activate --shims` is more suitable for CI, editors, or
  non-interactive shells.
- Containers with mounted home directories often need `mise install --system`.

## Official sources behind this skill

- `llms.txt` at the repo root for latest upstream LLM-oriented docs
- `docs/getting-started.md`
- `docs/configuration.md`
- `docs/environments/index.md`
- `docs/dev-tools/index.md`
- `docs/dev-tools/shims.md`
- `docs/dev-tools/mise-lock.md`
- `docs/tasks/*.md`
- `docs/hooks.md`
- `docs/troubleshooting.md`
- `docs/mise-cookbook/docker.md`
- `docs/mise-cookbook/nodejs.md`
- `docs/mise-cookbook/python.md`
