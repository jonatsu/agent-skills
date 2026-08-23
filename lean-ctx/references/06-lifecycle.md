# Lifecycle

## Update

1. Update binary by upstream-supported method.
2. Re-run setup/repair that rewires hooks and MCP snippets.
3. Restart the editor/MCP host — see below, this is not optional.
4. Run `status`, `doctor`, and one small tool call.

**An update does not reach the running session.** Updating swaps the on-disk
binary, and a `restart` subcommand respawns any shared daemon, but neither
replaces the **per-session stdio MCP server process** the host launched at session
start. That process holds the old binary in memory until the host itself restarts
and re-launches it.

So after an update, a session continues exercising the previous version while
`status` reports the new one. Any fix you just installed appears not to work, and
any bug you just escaped keeps reproducing. Restart the host before concluding
anything about a version's behavior — and treat a bug report written from a
non-restarted session as untrustworthy.

## Repair

- `doctor` finds config, hook, MCP, cache, and permission issues.
- `doctor --fix` or `setup --fix` can repair common integration drift.
- `doctor integrations` focuses editor/shell/MCP wiring.
- `sessions doctor` checks session state.

## Cache/session hygiene

- Use cache prune when store grows or stale compressed refs confuse recovery.
- Preserve reports/logs for issue filing before destructive cleanup.
- Prefer reversible cleanup and note what was removed.

## Migration

Avoid embedding host-specific paths into reusable skills. Move reference content
under docs, keep every-turn instructions short, and let local config provide
paths, profiles, and editor behavior.
