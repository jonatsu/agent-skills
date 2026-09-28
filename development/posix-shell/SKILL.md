---
name: posix-shell
description: Write, review, debug, and test portable POSIX sh scripts and sourced libraries. Use when removing Bashisms, migrating Bash scripts to sh, preserving argument and filename boundaries, handling pipeline failures and traps, or checking compatibility across required shells and systems. Use bash-shell when Bash-specific features are intended.
license: MIT
metadata:
  author: Joonas Onatsu
---

# POSIX Shell

Build the smallest `sh` program that preserves data, reports failure truthfully, and uses only the shell
language and utilities in its declared portability baseline. Follow repository conventions when they are
stricter without silently adding non-standard features.

## Establish the Contract

Before editing, determine:

- whether the file executes as a program, is sourced as a library, or is embedded in CI or another format;
- the oldest POSIX edition, operating systems, shells, and utility implementations that must work;
- inputs, outputs, exit statuses, side effects, destructive targets, locales, and filename assumptions;
- existing formatters, linters, tests, and repository instructions; and
- whether the requirements genuinely need Bash features. Route that work to `bash-shell` unless the user
  chooses a portable alternative with different behavior.

Use POSIX.1-2024 as the language baseline when the target is otherwise unspecified. State that older systems
remain unverified. A script is portable only within its declared standard, utilities, and tested environments.

## Implement Deliberately

1. Keep argument parsing, validation, core logic, and side effects distinguishable. Validate before the first
   side effect.
2. Preserve argument boundaries with positional parameters and `"$@"`. Do not imitate arrays with a delimited
   string when values may contain the delimiter. Read
   [data-and-path-safety.md](references/data-and-path-safety.md) for filename, path, and temporary-resource
   handling.
3. Make expected nonzero statuses explicit. Choose `errexit`, `nounset`, pipelines, subshells, and traps only
   after checking their effect on the complete control flow. Read
   [failure-semantics.md](references/failure-semantics.md) for those decisions.
4. Use syntax and utility options from the declared POSIX edition. Treat `local`, arrays, `[[ ... ]]`,
   process substitution, `source`, brace expansion, and Bash-specific parameter expansions as extensions.
   POSIX.1-2024 specifies `pipefail`; earlier POSIX editions do not.
5. Prefer shell builtins when they improve correctness or remove a process. Use an external utility when it
   makes the operation clearer and belongs to the declared baseline. Check optional dependencies at their
   boundary and report when they are unavailable.
6. When a POSIX-only contract seems to need an extension, restructure the operation or report that the
   requirement cannot be met within the declared baseline.

### Data and Paths

Shell variables cannot preserve NUL bytes, and command substitution removes trailing newlines, so neither can
store an arbitrary filename stream. Read [data-and-path-safety.md](references/data-and-path-safety.md) before
handling filenames, option terminators, deletion, or replacement.

### Error Handling

Do not use `set -eu` as a ritual or rely on `set -e` as complete error handling. Handle failures explicitly at
security, data-loss, and external-I/O boundaries. Without `pipefail`, a pipeline reports the last command's
status. Select `pipefail` only when POSIX.1-2024 belongs to the declared baseline, or restructure the
operation when an earlier status matters.

For sourced files, do not change the caller's shell options, traps, working directory, positional parameters,
`IFS`, or global variables unless that behavior is the documented interface.

## Migrate from Bash

Capture the existing script's behavior before conversion. Inventory Bash syntax, shell-option semantics,
external utilities, and assumptions about process state. Replace one dependency at a time and rerun the
relevant behavior checks after each change.

Preserve argument boundaries and failure behavior rather than transliterating syntax. Bash arrays cannot be
converted losslessly to delimiter-separated strings for arbitrary values, and removing `pipefail` changes a
pipeline's status contract. If POSIX sh cannot preserve a required behavior within the target environment,
report that constraint and keep Bash or revise the requirement with the user.

## Verify Behavior

Read [validation.md](references/validation.md), then run the checks available for the affected files. At
minimum:

- parse with each required shell, using `sh -n` only as the local shell's syntax check;
- run ShellCheck with the `sh` dialect and the repository's formatter when available; and
- exercise ordinary success and applicable failure paths on the required shell and operating-system targets.

Static analysis and one shell implementation cannot certify POSIX portability. Report the exact standard,
shells, operating systems, utilities, and failure paths tested, plus every supported boundary left untested.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the external skill reviewed before this independent
replacement was written.
