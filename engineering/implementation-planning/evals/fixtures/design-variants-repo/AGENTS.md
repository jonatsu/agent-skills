# Repository Instructions

`identity` handles sign-in, password reset, and account recovery.

## Checks

`just test` runs pytest and `just lint` runs ruff. Both must pass before review.

## Documents

Designs live in `docs/design/` and use these headings, in order: Context, Decision, Interfaces, Failure Handling,
Rollout. A design may instead follow arc42 when its author prefers; both forms are accepted.

Implementation plans live in `docs/plans/` as `<feature>-plan.md` and use exactly these top-level sections:

- **Goal**: the outcome and the design it implements.
- **Work packages**: numbered packages in the order they are done, each with its changes and how it is checked.
- **Acceptance**: the checks that show the whole feature works.

See [docs/plans/sign-in-lockout-plan.md](docs/plans/sign-in-lockout-plan.md) for an example.
