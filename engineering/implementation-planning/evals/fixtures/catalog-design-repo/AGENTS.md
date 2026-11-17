# Repository Instructions

`catalog` holds tooling for the product catalog files that the storefront loads at startup.

## Coding Checks

Run all of these before a change is reviewed:

- `just test`: pytest over `tests/`.
- `just lint`: `ruff check` and `ruff format --check`.
- `just type`: `mypy --strict src`.

## Conventions

- Python 3.12, standard library only for runtime code.
- Command-line tools live in `src/catalog/` and are exposed through `[project.scripts]` in `pyproject.toml`.
- Tests that need files create them under pytest's `tmp_path`; never edit files in `examples/` from a test.
- Designs live in `docs/design/`.
