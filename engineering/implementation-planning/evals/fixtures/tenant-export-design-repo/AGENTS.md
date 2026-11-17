# Repository Instructions

`records` serves tenant record search and administration.

## Checks

- `just test` runs unit tests.
- `just lint` runs ruff.
- `just integration` runs `tests/integration/` against the integration environment described below.

## Environments

The integration environment, `integration.records.example.com`, is an isolated deployment with its own database. It
is reseeded nightly with the synthetic tenants in `seed/tenants.yaml`. Tests may create and delete data there.

Production holds customer records, including personal data. Do not run tests, scripts, or exploratory requests
against production, and never copy production data into tests, fixtures, or the integration environment.
