# Repository Instructions

`ledger` owns account records and publishes account events for the billing and notification services.

- Run `just test` and `just lint` before asking for review.
- Database changes go in `migrations/` as numbered SQL files. Every migration must be reversible or state why not.
- The event schema in `src/ledger/events.py` is consumed by other services; any change to it needs an entry in
  `docs/consumers.md` naming which consumers are affected.
- Deploys go through the staged release train (canary, 25 percent, all); see `docs/release.md`.
