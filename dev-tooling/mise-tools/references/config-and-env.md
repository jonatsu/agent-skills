## When to load this file

Load this before editing `mise.toml`, `.miserc.toml`, `mise.local.toml`, or any environment-selection logic.

If the task specifically depends on Tera templating, early-init `.miserc.toml` behavior, or
platform-environment rollout details, also load `references/templating-and-early-init.md`.

## Config resolution model

Important files:

- `mise.toml` for shared project config
- `mise.local.toml` for local overrides and secrets after confirming the local config and lock are ignored
- `mise.<env>.toml` for named environment overlays
- `.miserc.toml` for early-init behavior
- `~/.config/mise/config.toml` for global defaults

Key behavior from upstream docs:

- config files merge upward through parent dirs
- `[tools]`, `[env]`, and `[settings]` are additive with overrides — with one exception for `tools = true`,
  below
- individual task definitions replace by task name
- `MISE_ENV` activates `mise.<env>.toml`

## Safe config-scope choices

- shared repo behavior → `mise.toml`
- local secrets or machine overrides → an ignored `mise.local.toml`
- environment-specific overlay → `mise.<env>.toml`
- machine-wide policy only when explicitly requested → global config

## Early-init `.miserc.toml`

Use only for things that must happen before normal config layers fully load, such as:

- selecting an environment early
- constraining config search with `ceiling_paths`
- host or sandbox-specific early decisions

Do not treat this file as the primary place to learn templating rules. Load
`references/templating-and-early-init.md` for that narrower topic.

Real-repo examples for inspiration only:

- `auto_env = true` for automatic environment selection behavior
- `ceiling_paths = ["{{ config_root | dirname }}"]` to stop parent-config leakage
- conditional `env = ["claude-code-web", "dev"]` in `.miserc.toml` based on external env vars

When citing these, label them as examples rather than official guidance.

## Environment model

Use `[env]` for project env values.

Important features:

- ordinary key/value env vars
- `false` to unset a value
- `{ default = "..." }` for keep-if-set semantics
- `{ required = "message" }` for required envs
- `env._.file` for dotenv loading
- `env._.path` for PATH augmentation
- `env._.source` for sourced shell snippets when truly needed
- `redactions` or per-var redaction controls for secret-safe output

## `tools = true` breaks the layering rule

An `[env]` entry written as `{ value = "...", tools = true }` renders a `{{ tools.* }}` template, so mise
resolves it in a pass that runs *after* every plain `[env]` layer has merged, global and project alike. A
global entry carrying `tools = true` therefore **cannot** be overridden by an ordinary project assignment: the
project value merges first and the global template lands on top. Only a project entry that also carries
`tools = true` wins.

Measured on mise 2026.9.6. With `UV_PYTHON = { value = "{{ tools.python.path }}", tools = true }` in the global
config, a project `mise.local.toml` setting `UV_PYTHON = "3.12"` had no effect, while a plain `ZZTEST` in the
same file applied normally. Switching the project entry to `{ value = "3.12", tools = true }` made it win.

Prefer a plain value in global config. Where a global entry must template on a tool, every project needing to
override it has to repeat the `tools = true` form — say so where the entry is defined.

## `[env]` applies during installation, not just activation

`[env]` is resolved before tools, so it reaches tool-installation subprocesses — upstream states this in
`docs/environments/index.md`, and the code path runs `dependency_env` → `full_env_without_tools` →
`Toolset::env`, where the config `[env]` block is applied last and therefore overrides a tool's own
`exec_env`.

The carve-out is mise's own self-configuration: `MISE_DATA_DIR`, `MISE_INSTALLS_DIR` and friends are read at
process start, so set those in the shell or CI environment rather than in `[env]`.

This is the supported way to control an install subprocess's environment — for example redirecting `GOPATH` so
`go:` backend installs stop writing to `$HOME/go`. Load `references/go-backend.md` for that case.

`install_env` on a `[tools]` entry is a different scope: it applies to **that tool's own install and
postinstall only**. Putting `install_env` on the `go` entry configures the installation of Go itself and never
reaches tools installed through the `go:` backend.

## Important path and expansion facts

- `{{config_root}}` is the portable anchor for project-relative paths.
- shell-style expansion and Tera-style templating can both participate.
- for templating details and `.miserc.toml` limitations, load `references/templating-and-early-init.md`.

## Reproducibility controls

- use `min_version` when feature support matters
- use exact pins or `mise.lock` when reproducibility matters
- keep secrets out of committed config

## Verification commands

- `mise cfg`
- `mise env`
- `mise trust --show`
- `mise install --dry-run`

## Footguns

- putting secrets into committed `mise.toml`
- storing secrets in `mise.local.toml` before confirming local config and lock patterns are ignored
- using global config when a project-local file would work
- forgetting that parent configs can leak in
- treating fuzzy versions as exact unless lockfile or pins enforce it
- a global `[env]` entry carrying `tools = true`, which no plain project assignment can override
- assuming `mise exec` gives a clean environment: it overrides only the variables the config declares, so an
  inherited value for anything unmentioned passes straight through
