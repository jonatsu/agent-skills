# Appendix: CLI map

Command names may drift. Prefer `lean-ctx --help` and generated CLI docs for the
active version.

## Setup/lifecycle

- `lean-ctx wrap` — prepare command/editor wrapping where supported.
- `lean-ctx onboard` — guided first-run onboarding.
- `lean-ctx setup` — configure integrations.
- `lean-ctx setup --fix` — repair setup drift.
- `lean-ctx bootstrap` — initialize required state/assets.
- `lean-ctx init` — project/session initialization where supported.
- `lean-ctx update` — update binary/integrations where supported.

## Diagnostics

- `lean-ctx status` — current state summary.
- `lean-ctx doctor` — general diagnostics.
- `lean-ctx doctor --fix` — safe automated fixes.
- `lean-ctx doctor integrations` — editor/shell/MCP wiring.
- `lean-ctx sessions doctor` — session health.
- `lean-ctx cache prune` — prune cached/compressed artifacts.
- `lean-ctx report-issue` — collect report for upstream.

## Shell/proxy

- `lean-ctx -c "command"` — run command through lean-ctx wrapper.
- `lean-ctx-off` — disable shell hook in current shell.
- `lean-ctx proxy enable|start|status|disable` — manage proxy lifecycle.

## Environment flags

- `LEAN_CTX_DISABLED=1` — bypass hook/wrapper for one command.
- `LEAN_CTX_RAW=1` — request raw shell output.
- `LEAN_CTX_DATA_DIR` — data dir override; avoid in editor MCP env unless
  legacy single-dir behavior is intentional.
