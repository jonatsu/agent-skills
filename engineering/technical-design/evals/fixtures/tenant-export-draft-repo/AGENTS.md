# Repository Instructions

`dashboard` is the backend of a multi-tenant analytics dashboard. Each tenant is a customer organization; its
administrators and viewers see only that tenant's records.

- Source is in `src/dashboard/`, tests in `tests/`.
- Plans, drafts, and designs live in `docs/plans/`, named `<name>-draft.md` or `<name>-design.md`.
- Every read of tenant data goes through `RecordStore`, which takes the tenant from the caller's `Principal`.
- Run `just check` before finishing a change. It runs `ruff check`, `ruff format --check`, and `pytest`.
