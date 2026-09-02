## When to load this file

Load this only when example-only real-repo patterns would help with layout or workflow ideas. Do not use this
file as authority for official mise behavior.

## Rule for this file

Everything here is illustrative. Official behavior must still come from upstream mise docs.

## Example-only `mise.toml` patterns collected during research

### Task-first repo patterns

Useful example-only ideas:

- task pipelines that compose formatting, linting, tests, and release steps
- `dir = "subdir"` task scoping for nested toolchains
- task naming by workflow phase or namespace

### Tool and env-heavy repo patterns

Useful example-only ideas:

- explicit backend-pinned tool definitions
- per-platform asset or path handling
- curated install behavior such as `auto_install = false`
- templated native-library paths for cross-platform builds

## Example-only `.miserc.toml` patterns collected during research

Useful example-only ideas:

- `auto_env = true` for platform environment adoption
- `ceiling_paths = ["{{ config_root | dirname }}"]` to stop parent-config leakage
- conditional environment selection based on external environment variables in remote or sandbox contexts

## How to use examples safely

- borrow structure, not authority
- label examples as example-only if you mention them in final guidance
- prefer upstream docs for semantics, precedence, and feature guarantees
- do not infer official support or stability from a single repo pattern
