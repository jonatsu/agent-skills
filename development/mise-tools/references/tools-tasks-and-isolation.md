## When to load this file

Load this before adding tools, tasks, lockfiles, hooks, bootstrap logic, or container-oriented mise workflows.

## Tool and backend guidance

Prefer explicit, documented backends when they materially improve reproducibility or verification.

High-value backend families from upstream docs:

- core runtimes for first-party managed languages
- `aqua:` and `github:` for many binary tools with stronger provenance support
- ecosystem-specific backends like `npm:`, `pipx:`, `cargo:`, `go:` when appropriate

Useful tool options:

- exact or fuzzy version selection
- OS or arch restrictions
- install-order dependencies
- postinstall hooks when truly needed

Useful command and override reminders from upstream docs:

- `mise exec -- <command>` is the canonical automation form, with `mise x` as shorthand
- `MISE_<TOOL>_VERSION` can override a tool version for the current process

## Isolation patterns

### Project-local reproducible environment

Use committed `mise.toml` plus `mise.lock`.

### Local override layer

Use `mise.local.toml` for local env or secrets after confirming its config and lock files are ignored.

### Command-scoped automation

Use `mise exec -- <command>`.

### CI or vendored bootstrap

Use vendored bootstrap when you want predictable acquisition of the mise binary itself.

### Container or image bake

Use `mise install --system` when home-directory mounts would otherwise hide baked user installs.

### Experimental OCI environment

Exists, but label clearly as experimental and Linux-oriented.

## Tasks

Mise supports:

- TOML tasks in `[tasks]`
- file tasks in `mise-tasks/` and related directories

Prefer TOML tasks for small, declarative commands. Prefer file tasks for larger or more script-like logic.

High-value task features:

- `depends`
- `sources` and `outputs`
- aliases and descriptions
- task-scoped `tools`
- task-scoped env
- output-mode control
- watch workflows

`mise watch` is useful for file-watching task loops and is worth considering before adding custom watcher
scripts.

Prefer tasks over hooks when the action should be explicit and repeatable.

## Hooks

Available hooks include `cd`, `enter`, `leave`, `preinstall`, `postinstall`, and file-watching workflows.

Only use hooks when automatic behavior is essential. Default to tasks first.

## Lockfile and strict mode

Use `mise.lock` when the environment must reproduce reliably.

Important points:

- commit `mise.lock` for shared workflows
- strict or locked modes should match the team or CI expectation
- lockfile workflows reduce resolver drift and external API dependence
- exact pins plus lockfile is the strongest general setup

## Real-repo examples

Real repos can be useful for examples, but never as official guidance.

Reusable ideas gathered during research:

- task-first `mise.toml` files that orchestrate formatting, linting, and test pipelines
- `dir = "subdir"` task scoping for nested toolchains
- per-platform templating for native-library paths
- `auto_install = false` in curated or CI-focused repos

## Verification commands

- `mise install --dry-run` before an installation when a preview is useful
- `mise tasks`
- `mise tasks deps <name>`
- `mise run <task>`
- `mise exec -- <tool> --version`
- `mise lock --dry-run` before updating a lockfile

Run installation, task, and lockfile-writing commands only when the request authorizes their effects.

## Footguns

- using hooks where explicit tasks would be clearer
- adding tasks without descriptions or reproducibility expectations
- using fuzzy versions in a supposedly deterministic CI workflow
- relying on experimental features without labeling them
