# Repository Instructions

`exporter` is a small Python module inside a larger product backend. It creates CSV exports of report data.

- Source is in `src/exporter/`, tests in `tests/`.
- Design documents live in `docs/plans/`, named `<name>-design.md`.
- Run `just check` before finishing a change. It runs `ruff check`, `ruff format --check`, and `pytest`.
- Pass the current time into functions as an argument; do not read the clock inside business logic.
