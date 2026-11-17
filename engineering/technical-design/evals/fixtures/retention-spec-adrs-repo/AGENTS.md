# Repository Instructions

This repository holds the documentation for the team archive service, which stores files for workspaces of a few dozen
people. The implementation lives in separate repositories.

- Accepted requirements specifications live in `docs/specs/`.
- Architecture decision records (ADRs) live in `docs/adr/`, numbered `NNNN-title.md`. An accepted ADR changes only
  through a new ADR that supersedes it.
- Designs live in `docs/design/`, named `<name>-design.md`.
- Write in plain English, wrap Markdown at 120 columns, and link to a document instead of repeating its content.
- Run `just check` before finishing a change. It runs `scripts/check_docs.py`, which verifies that every relative link
  resolves and that every ADR states its status.
