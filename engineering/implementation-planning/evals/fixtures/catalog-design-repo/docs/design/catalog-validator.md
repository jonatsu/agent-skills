# Design: Catalog Validator

Status: Accepted

## Purpose

Broken catalog files reach the storefront and fail at startup. `catalog-validate PATH` checks a catalog file before it
is published and reports every problem in one run.

## Input

A catalog file is UTF-8 JSON whose top level is an array of entry objects. An entry is valid when:

- it is a JSON object,
- its `id` is a nonempty string, and
- no earlier entry in the file has the same `id`.

Other fields are not checked by this tool.

## Behavior

The validator distinguishes two error classes.

**Read or parse failure.** The file cannot be opened, is not valid UTF-8, is not valid JSON, or its top level is not an
array. Validation stops; no entry is checked. The tool prints one line, `error: <path>: <reason>`, to standard error
and exits with status 2.

**Entry issues.** The file parses but one or more entries are invalid. Every invalid entry is reported, not only the
first, one line per issue on standard output: `entry <index>: <issue>`, where `<index>` is the zero-based position.
An entry may have more than one issue. For a duplicate, the issue names the index of the first entry with that id. The
tool exits with status 1.

**Valid input.** No output, exit status 0.

The validator never writes to, renames, or replaces the input file, in any of these cases.

## Structure

- `catalog.parser.load(path) -> list[object]` reads and decodes the file and raises `CatalogReadError` with a reason
  for every read or parse failure. It does no entry checking.
- `catalog.entries.check(entries) -> list[EntryIssue]` takes the decoded array and returns every issue in index order.
  It does no I/O.
- `catalog.cli.main` calls `load`, then `check`, and maps the outcome to output and exit status as described above.

Keeping parsing separate from entry checking lets each be tested alone and keeps the two error classes from mixing.

## Out of Scope

Schema checks beyond `id`, automatic fixing, and validating more than one file per run.
