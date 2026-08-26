# Appendix: paths and config

## Config principles

- Keep reusable instructions path-neutral.
- Let local lean-ctx config define data dirs, allowed roots, profiles, and editor
  integration details.
- Avoid putting secrets or machine-specific values in skills/docs.

## Path jail

Common controls (all top-level config keys, not members of a `[section]` table —
a root key moved below a table header is silently assigned to that table and
dropped):

- `allow_paths` — explicit readable/editable paths.
- `extra_roots` — additional workspace roots; also added to the jail allow-list.
- `project_root` — explicit root; the only lever that pins the root rather than
  widening the jail. Per-session form: `LEAN_CTX_PROJECT_ROOT`.
- `read_only_roots` — reads allowed, writes always denied.
- `allow_auto_reroot` — re-root on out-of-jail absolute paths; defaults to false,
  though capture has been observed with the default in place.
- `path_jail=false` — disable jail when deliberately needed.
- `allow_ide_config_dirs=true` — permit editor config dirs when safe.

Use least privilege first. Expand path access only for task need and user intent.

The session root can move on its own: touching a foreign tree with `ctx_*` can
re-root the session onto it. See `12-troubleshooting.md` → "Project-root
capture".

## MCP env

Do not hardcode `LEAN_CTX_DATA_DIR` in editor MCP config unless intentionally
using legacy single-dir behavior. Prefer default discovery or host-specific local
config. After env/config changes, reload MCP config; restart editor if tools do
not refresh.

## Shell config

Shell hook setup may edit RC files and create `*.lean-ctx.bak`. If hook behavior
looks wrong, inspect active shell startup chain, stale exports, and backups.

## Docs drift

Counts, profiles, schemas, and command names change. Trust generated config keys,
tool registry, `--help`, and `doctor` output over narrative docs.
