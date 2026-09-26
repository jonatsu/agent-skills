Mise supports Tera templating in configuration and environment workflows, but early-init `.miserc.toml` runs
before normal config loading and therefore has a narrower context. Agents must not assume full project config
state is available there.

Normal config templating and early-init `.miserc.toml` templating are both official mise features, but they do
not expose the same variables and functions.

Upstream Tera language reference:

- <https://keats.github.io/tera/#template>

## Standard environment and config templating

Use templating when:

- env values need portable project-relative paths
- paths depend on OS, arch, or home-directory context
- shared config needs computed values without shell scripting

Mise uses Tera templates for most configuration values. The TOML file structure itself must still be valid
TOML.

Common safe patterns:

- `{{config_root}}` for project-relative paths
- `{{ env.HOME }}` or XDG-derived values for user-space paths
- `os()` and `arch()` when platform-aware config is unavoidable

Common normal-context variables from upstream docs:

- `env`
- `cwd`
- `config_root`
- `mise_bin`
- `mise_pid`
- `mise_env` when explicitly set
- XDG directory variables
- task or tool-specific context such as `tools`, `usage`, or `vars` where supported

Common normal-context functions from upstream docs:

- `get_env`
- `arch`
- `os`
- `os_family`
- `num_cpus`
- `choice`
- `exec`
- `read_file`

Keep templating readable. If a value becomes hard to reason about, prefer a simpler env or task design.

If literal `{{`, `{%`, or `{#` text must survive, wrap it in a Tera raw block.

## Early-init `.miserc.toml` templating

`.miserc.toml` is loaded very early, before normal config discovery is complete. It supports templating, but
only with early-init-safe context.

From current upstream docs:

- `.miserc.toml` may set `env = ["development"]` or multiple environments
- templating is supported there for things like `ceiling_paths` or ignored config paths
- only OS-level or early-init context is available at that stage
- settings from `mise.toml` are not loaded yet

Documented early-init variables available in `.miserc.toml` include:

- `env`
- `config_root`
- `cwd`
- XDG directory variables

Documented early-init functions available there include standard safe helpers like:

- `arch`
- `os`
- `os_family`
- `num_cpus`
- `choice`

Documented early-init omissions include:

- no `mise_env`
- no `exec()`
- no `read_file()`
- no `mise_bin` or `mise_pid`

Implication:

- use `.miserc.toml` templating for early environment choice or search-boundary control
- do not expect project-defined settings, env layers, or later config-derived values to exist there
- do not build clever early-init logic that depends on runtime inspection functions unavailable at that stage

## Environment layering

Important order from upstream docs:

- explicit `MISE_ENV` can be supplied by CLI flag, env var, or `.miserc.toml`
- `mise.{MISE_ENV}.local.toml`
- `mise.local.toml`
- `mise.{MISE_ENV}.toml`
- `mise.toml`

Multiple environments can be specified, with later entries taking precedence.

`MISE_ENV` cannot be set in `mise.toml` because it determines which config files get loaded in the first
place.

## Platform environments and `auto_env`

When `auto_env` is enabled, mise can automatically treat platform names such as `unix`, `linux`, `macos`,
`windows`, or `linux-x64` as active config environments.

Use this only when platform-specific overlays are truly needed. Label it clearly because upstream docs
describe it as an early-init behavior with version-sensitive rollout semantics.

Important upstream nuance:

- platform environments affect config-file discovery and lockfile selection
- they do not populate `mise_env` for templates or subprocesses
- explicit `MISE_ENV` entries still take precedence over auto platform environments

## Footguns

- assuming `.miserc.toml` can access full project config context
- assuming `.miserc.toml` can call `exec()` or `read_file()`
- using templating where a plain literal would be clearer
- hiding important environment decisions inside clever templates
- forgetting that explicit `MISE_ENV` can override `.miserc.toml` choices
- forgetting that `auto_env` is early-init and version-sensitive
