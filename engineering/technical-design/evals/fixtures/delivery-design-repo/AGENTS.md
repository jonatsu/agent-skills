# Repository Instructions

`delivery` sends outgoing notification messages to subscriber HTTP endpoints. Messages wait in a SQLite table and a
worker process delivers them.

- Source is in `src/delivery/`, tests in `tests/`.
- Accepted requirements are in `docs/requirements.md`. Design documents live in `docs/design/`.
- Every design document uses exactly these second-level headings, in this order: Purpose, Current behavior, Proposed
  behavior, Decisions, Open questions. Do not add other second-level headings or a second design for the same subject.
- Run `just check` before finishing a change. It runs `ruff check`, `ruff format --check`, `pytest`, and
  `scripts/check_design.py`, which verifies the design headings.
