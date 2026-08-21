## When to load this file

Load this before editing `mise.toml`, `.miserc.toml`, `mise.local.toml`, or any environment-selection logic.

If the task specifically depends on Tera templating, early-init `.miserc.toml` behavior, or platform-environment rollout details, also load `references/templating-and-early-init.md`.

## Config resolution model

Important files:
- `mise.toml` for shared project config
- `mise.local.toml` for local overrides and secrets
- `mise.<env>.toml` for named environment overlays
- `.miserc.toml` for early-init behavior
- `~/.config/mise/config.toml` for global defaults

Key behavior from upstream docs:
- config files merge upward through parent dirs
- `[tools]`, `[env]`, and `[settings]` are additive with overrides
- individual task definitions replace by task name
- `MISE_ENV` activates `mise.<env>.toml`

## Safe config-scope choices

- shared repo behavior → `mise.toml`
- local secrets or machine overrides → `mise.local.toml`
- environment-specific overlay → `mise.<env>.toml`
- machine-wide policy only when explicitly requested → global config

## Early-init `.miserc.toml`

Use only for things that must happen before normal config layers fully load, such as:
- selecting an environment early
- constraining config search with `ceiling_paths`
- host or sandbox-specific early decisions

Do not treat this file as the primary place to learn templating rules. Load `references/templating-and-early-init.md` for that narrower topic.

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
- `mise trust`
- `mise install`

## Footguns

- putting secrets into committed `mise.toml`
- using global config when a project-local file would work
- forgetting that parent configs can leak in
- treating fuzzy versions as exact unless lockfile or pins enforce it
