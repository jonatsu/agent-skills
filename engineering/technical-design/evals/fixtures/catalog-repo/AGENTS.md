# Repository Instructions

`catalogcheck` is a small command-line tool with a Python entry point.

- Source is in `src/catalogcheck/`, tests in `tests/`.
- Use only the Python standard library at runtime.
- Run `just check` before finishing a change. It runs `ruff check`, `ruff format --check`, and `pytest`.
- Keep the README and `docs/api.md` true to the code.
