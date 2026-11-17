# Design: `--since` Filter for `auditlog`

Status: Accepted

Tracking issue: #87

## Context

Operators read the whole audit log and filter with other tools. They want the CLI to show only recent events.

## Decision

Add an optional `--since TIMESTAMP` argument. It accepts an ISO 8601 UTC timestamp ending in `Z` (for example
`2026-03-01T00:00:00Z`). Only events whose `timestamp` is at or after it are printed. Without `--since`, output is
unchanged.

Timestamps in the log are always UTC with a `Z` suffix, so comparison parses both sides with
`datetime.fromisoformat` and compares the results; string comparison is not used.

## Failure Handling

An invalid `--since` value exits with status 2 and argparse's usage error, before the file is read. An event whose
`timestamp` cannot be parsed is skipped when `--since` is given, and the tool prints one warning to standard error per
skipped event, naming its line number.

## Compatibility

Output format and exit status for existing invocations do not change.
