## What the schemas are

The mise repository ships JSON Schema definitions for every TOML config file it accepts. They live at
`https://github.com/jdx/mise/tree/main/schema` and are also published to SchemaStore for IDE/editor
auto-completion.

Consult the relevant schema when:

- authoring a new config file from scratch
- unsure whether a key exists or what type it accepts
- validating that a hand-edited TOML file is structurally sound
- confirming task, plugin, or registry-tool field shapes before suggesting them

Fetch one relevant schema and inspect only the keys in question. Do not reproduce the entire schema inline.

## Schema files and what they cover

Base URL for raw schema files:

```text
https://raw.githubusercontent.com/jdx/mise/refs/heads/main/schema/
```

Browse URL:

```text
https://github.com/jdx/mise/tree/main/schema
```

| File                      | Applies to                                           | Purpose                                                                                                                                                                                     |
| ------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mise.json`               | `mise.toml`, `mise.local.toml`, `mise.<env>.toml`    | Main project config: `[tools]`, `[env]`, `[tasks]`, `[settings]`, hooks, aliases. This is the schema consulted most often.                                                                  |
| `miserc.json`             | `.miserc.toml`                                       | Early-init settings loaded before normal config layers: `env`, `auto_env`, `ceiling_paths`, ignored paths. Limited context — see `references/templating-and-early-init.md`.                 |
| `mise-settings.json`      | global `settings.toml` / `[settings]` block          | Mise runtime settings: install behavior, trust, shims, lockfile mode, telemetry, and other operational toggles.                                                                             |
| `mise-task.json`          | `[tasks.<name>]` blocks and `mise-tasks/` file tasks | Task definition fields: `run`, `depends`, `sources`, `outputs`, `description`, `alias`, `dir`, `env`, `tools`, `hide`, `raw`, `file`. Docs: <https://mise.en.dev/tasks/#task-configuration> |
| `mise.plugin.json`        | `mise.plugin.toml` in plugin repos                   | Config file shipped inside a mise plugin repository. Rarely needed for end-user setups.                                                                                                     |
| `mise-registry-tool.json` | per-tool files in the mise registry                  | Schema for tool definitions in the official mise registry. Only relevant when authoring or reviewing a registry tool entry — not for normal project config.                                 |

## How to fetch a schema

```bash
# Example: fetch the main mise.toml schema
curl -sL https://raw.githubusercontent.com/jdx/mise/refs/heads/main/schema/mise.json
```

The schemas are large JSON documents. When consulting one, fetch it and inspect only the section relevant to
the current task rather than pasting the whole file into context.

## IDE and editor integration

The same schemas are published to SchemaStore, so editors with YAML/TOML schema support (VS Code with the Even
Better TOML extension, Neovim with schemastore.nvim, JetBrains, etc.) can auto-complete and validate mise
config files automatically. No manual URL wiring is needed in most editors that respect SchemaStore.

For explicit schema binding in editors that require it, point the relevant file pattern at the raw URL:

- `mise.toml`, `mise.local.toml`, `mise.*.toml` → `mise.json`
- `.miserc.toml` → `miserc.json`
- `mise-tasks/*.toml` → `mise-task.json`

## How schemas relate to other references

- For config resolution, scoping, and layering → `references/config-and-env.md` (schemas define keys; that
  file defines how files merge)
- For templating context and `.miserc.toml` limitations → `references/templating-and-early-init.md` (schemas
  define fields; that file defines what template variables are available)
- For task features and isolation patterns → `references/tools-tasks-and-isolation.md` (schemas define task
  fields; that file defines when to use tasks vs hooks)

## Footguns

- Treating the schema as the only documentation: it defines structure, not behavior or intent. Pair with the
  narrative references.
- Treating schema acceptance as proof of intended TOML ownership. A wrongly nested tool is structurally valid;
  inspect the parsed tree as described in `config-and-env.md`.
- Assuming a key absent from the schema is valid just because a repo example used it — it may be experimental,
  deprecated, or plugin-specific.
- Fetching and holding all six schemas in context at once. Fetch only the one relevant to the file being
  edited.
- Editing a registry-tool or plugin schema when the task is ordinary project config — those are specialized
  and rarely needed.
