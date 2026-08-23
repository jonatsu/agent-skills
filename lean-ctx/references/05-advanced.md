# Advanced use

## Power tools

- `ctx_compose` — combine multiple lookups in one compressed result.
- `ctx_plan` — generate compact implementation plan.
- `ctx_compile` — pack task context.
- `ctx_radar` — detect likely relevant files/risks.
- `ctx_verify` — verify invariants or expected checks.
- `ctx_load_tools` — expose extra tools/profile capabilities.

Tools available in the binary may differ from active MCP profile. Check current
tool list or load power tools before relying on a name.

## Shell hook

- Disable for session: `lean-ctx-off`.
- Disable one command: `LEAN_CTX_DISABLED=1 command`.
- Force raw output: `LEAN_CTX_RAW=1 command`.
- If behavior persists, inspect stale RC exports and `*.lean-ctx.bak` backups.

## MCP

- Register lean-ctx as an MCP server per editor/host docs.
- Do not hardcode `LEAN_CTX_DATA_DIR` in MCP env unless deliberately preserving
  legacy single-dir behavior.
- Config reload may update settings; tool-list changes often need editor restart.

## Proxy

Use proxy only when routing model/API traffic through lean-ctx is intended.
Know the lifecycle: enable → start → status → disable. Foreground process env
can differ from service env; debug both when keys/proxy vars differ.

## Patching

`ctx_patch` is standard: anchored, batchable, path-safe. `ctx_edit` is legacy or
power-profile only; prefer `ctx_patch` unless upstream docs or active profile
dictate otherwise.

## Write doctrine in ctx_shell

`ctx_shell` rejects shell redirects (`>`, `>>`) outright, pointing at the host's
native write tool instead. This is a write-doctrine gate, not the command
allowlist, so it fires regardless of which binary is being run. Redirects into
temporary directories are exempt.

The consequence worth knowing in advance: `git show <ref>:<path> > <path>` is the
standard way to restore a single file when `git checkout`/`git restore` are
unavailable or blocked, and it does not work through `ctx_shell`. Restore with an
inverse `ctx_patch` (or a native write) instead. `ctx_execute` is not a way around
this — it runs the identical gate.
