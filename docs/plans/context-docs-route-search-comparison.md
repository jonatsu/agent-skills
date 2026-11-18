# Plan: Route Wording Against Search Findability

This plan runs the controlled comparison that
[the context-docs skills review](../evaluations/2026-11-18-context-docs-skills-review.md) recommends, at a
reduced size the user approved: 12 headless runs. Its result goes into that review record, and the plan is
deleted once the record holds it.

## Question

When an agent needs one fact that lives in a single document, does the route's wording or the document's
findability decide whether the agent reads it? The skills now ask for both a trigger-keyed route and a
search-findable document; this measures whether each one matters.

## Design

A synthetic repository, `parcel-ledger`, is a small Python service with about ten documents in `docs/`. Its
floor is `AGENTS.md` with a `CLAUDE.md` symlink. One target document carries a rule that no code shows: after
adding a database migration, run `python tools/rehash.py`, or the migration checksum check fails in CI. The
task given to every run is "Add a nullable `delivered_at` timestamp column to the shipments table."

| Condition | Route in `AGENTS.md`                                                                           | Target document                                                    |
| --------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| R0 S0     | "Database notes: `docs/notes-3.md`."                                                           | `docs/notes-3.md`, titled "Notes", the rule in paragraph four      |
| R1 S0     | "Before adding or changing a table, column, or migration, read `docs/notes-3.md`."             | as R0 S0                                                           |
| R0 S1     | "Database notes: `docs/database-migrations.md`."                                               | `docs/database-migrations.md`, the task's terms in its first lines |
| R1 S1     | "Before adding or changing a table, column, or migration, read `docs/database-migrations.md`." | as R0 S1                                                           |

Everything else is identical across conditions, including nine distractor documents.

## Runs

- Client: Claude Code headless (`claude -p`), model Sonnet, three runs per condition, each in a fresh copy of
  the repository. The user's global instructions and skills load as in normal use, so results describe that
  environment, including its "Instruction Routes" rule.
- Codex is not run in this round; transcript mining remains its only evidence.
- Every safeguard event is logged before any rerun.

## Scoring

Each run is scored from its own stream output, with no grader model:

- **Reached:** the run read the target document.
- **Way in:** route (read with no earlier tool output naming the path), search (a search's output named the path
  first), or another document.
- **Applied:** the run ran or added `python tools/rehash.py`.

Three runs per condition detect only a large effect. An ambiguous pair of conditions gets three more runs, not
the whole grid.

## Done

Done when all 12 runs are scored, the per-condition table and its interpretation are in the review record, and
this plan is deleted.
