# Repository Instructions

`tokenapi` is the authentication layer of a small internal HTTP API. It stores API tokens in SQLite and checks them on
each request.

## Layout

- `src/tokenapi/` holds the package: `db.py` (connection and migrations), `tokens.py` (token storage), and `auth.py`
  (request authentication).
- `migrations/` holds ordered SQL files named `NNNN_description.sql`.
- `tests/` holds the pytest suite.
- Design documents live in `docs/plans/`, named `<name>-design.md`.

## Rules

- Migrations are append-only. Never edit a migration that has been merged; add a new one.
- Every migration must stay backward compatible with the previous release. The service deploys with rolling restarts,
  so the old code runs against the new schema for a while. Add columns and tables; do not drop, rename, or tighten
  them in the same release that stops using them.
- Never store, log, or return a raw token after it is issued. Store only its hash.
- Authentication failures return the same `AuthError` and the same 401 body whatever the cause.
- Keep time handling in UTC and pass the current time in as an argument so tests need no clock patching.

## Checks

Run `just check` before finishing a change. It runs `ruff check`, `ruff format --check`, and `pytest`.
