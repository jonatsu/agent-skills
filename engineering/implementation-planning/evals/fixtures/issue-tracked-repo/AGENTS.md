# Repository Instructions

`auditlog` is the command-line tool operators use to read the service audit log.

## Checks

`just test` runs pytest and `just lint` runs ruff.

## How Work Is Tracked

- Designs live in `docs/design/` and plans in `docs/plans/`. Both describe intended work only.
- Each feature has one GitHub issue, opened from the
  [implementation template](.github/ISSUE_TEMPLATE/implementation.md). The issue's checklist is the execution record:
  tick an item only when its work is merged, and attach the check output (test run, lint run, review link) as a
  comment on the issue.
- Deviations from the plan and unresolved review findings are recorded as issue comments and linked from the
  checklist item they affect.
- The design for a feature names its tracking issue.
