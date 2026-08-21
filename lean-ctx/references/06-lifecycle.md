# Lifecycle

## Update

1. Update binary by upstream-supported method.
2. Re-run setup/repair that rewires hooks and MCP snippets.
3. Restart editor/MCP host if tool registry changed.
4. Run `status`, `doctor`, and one small tool call.

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
