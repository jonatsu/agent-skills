---
name: bash-shell
description: Write, review, debug, and harden Bash scripts, sourced libraries, and shell automation embedded in CI or task runners. Use for argument parsing, arrays, quoting, pipelines, exit statuses, errexit, traps, temporary files, cleanup, and safe file operations, including ShellCheck findings and runtime failures. Use posix-shell when the script must remain portable POSIX sh.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Bash Shell

Build the smallest Bash program that preserves data, reports failure truthfully, and behaves correctly in its
declared environment. Follow the repository's existing shell conventions and tools when they are stricter or
more specific.

## Establish the Contract

Before editing, determine:

- whether the file executes as a program, is sourced as a library, or runs inside CI configuration;
- the minimum Bash version and supported operating systems;
- inputs, outputs, exit statuses, side effects, and destructive targets;
- existing formatters, linters, tests, and repository instructions; and
- whether Bash features are required. Route strict POSIX work to `posix-shell`.

Do not add Bash to a task better expressed as one direct command or a clearer existing language. Do not
silently raise the minimum Bash version.

## Implement Deliberately

1. Keep argument parsing, validation, core logic, and side effects distinguishable. Validate before the first
   side effect.
2. Represent argument vectors with arrays. Preserve data boundaries through quoting and NUL-delimited
   interfaces where filenames may contain whitespace or newlines.
3. Make expected nonzero statuses explicit. Choose `errexit`, `nounset`, `pipefail`, and traps only after
   checking how they affect conditionals, functions, substitutions, pipelines, and sourced callers. Read
   [failure-semantics.md](references/failure-semantics.md) for those decisions.
4. Treat paths, temporary resources, signals, and replacement writes as lifecycle concerns. Read
   [data-and-path-safety.md](references/data-and-path-safety.md) before implementing deletion, recursive file
   operations, temporary storage, signal handling, or atomic replacement.
5. Prefer Bash builtins when they improve correctness or remove a process. Prefer readable external tools when
   a pure-Bash replacement would obscure intent. Detect required commands and handle GNU/BSD differences only
   for supported platforms.

### Destructive Operations

**Iron law:** delete or overwrite only a validated path.

Quoting and `--` prevent specific parsing bugs; they do not make a target safe. Resolve the exact target,
reject empty or broad roots, confirm it belongs to the operation, preserve the user's authorization boundary,
and prefer a recoverable operation when practical. A dry run must render the same argument vector the real
operation would execute.

### Error Handling

Do not use `set -Eeuo pipefail` as a ritual or rely on `set -e` as complete error handling. Handle failures
explicitly at security, data-loss, and external-I/O boundaries. Preserve the original status during cleanup
and ensure cleanup cannot erase or replace it accidentally.

For sourced files, do not change the caller's shell options, traps, working directory, positional parameters,
or global variables unless that behavior is the documented interface.

## Verify Behavior

Read [validation.md](references/validation.md), then run the checks available for the affected files. At
minimum:

- parse with the declared Bash version or `bash -n`;
- run the repository's ShellCheck and formatter configuration when present; and
- exercise ordinary success and applicable failure paths in an isolated temporary directory, including
  cleanup and hostile inputs when consequential.

Tests must cover the behavior that makes the script risky or useful. A small script does not automatically
need a new test framework, help generator, packaging, logging subsystem, portability layer, or dry-run mode.

Report the commands run, their results, and any supported environment or failure path that remains untested.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for upstream idea sources reviewed while designing this
original skill.
