# Repository Instructions

`hooksvc` delivers outbound webhooks for the platform. Python 3.12, managed with `uv`.

## Python Rules

- Type every public function; `mypy --strict` must pass.
- Keep I/O at the edges: `sender.py` owns HTTP, `store.py` owns SQLite. Domain logic stays pure and testable.
- Raise the specific exceptions in `hooksvc.errors`; never catch bare `Exception`.
- Never log a webhook secret, signature, or full payload body.
- Write tests with pytest. Use the in-memory store fixture in `tests/conftest.py`; never reach a real endpoint.

## Required Gates

Every change must pass all three recipes before review:

- `just test` runs the pytest suite.
- `just lint` runs `ruff check` and `ruff format --check`.
- `just type` runs `mypy --strict src`.

Schema changes to the SQLite store need a numbered migration in `src/hooksvc/migrations/` and a test that applies it
to a copy of the previous schema.

Changes that touch delivery, persistence, or endpoint validation are reviewed by another maintainer before they merge.

## Skills

Agents working here can use the skills listed in [docs/skills.md](docs/skills.md). Load only the ones the task needs.
