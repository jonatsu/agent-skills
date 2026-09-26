# Validation

Use the repository's configured commands and versions first. Add tools only when the task requires them and
the user has authorized the dependency change.

## Static Checks

- Parse every affected script with its declared Bash version. `bash -n path/to/script` is the usual minimum.
- Run ShellCheck with the repository configuration and declared dialect. Read each diagnostic rather than
  suppressing it to obtain a green result.
- Run the configured formatter, commonly shfmt. Formatting does not prove behavior.
- Validate embedded Bash in CI or configuration with the owning format's checker as well as Bash tooling when
  practical.

## Behavioral Checks

Run scripts in an isolated temporary directory with real inputs and inspect output, exit status, files,
permissions, and cleanup. Cover the consequential cases among:

- ordinary success and expected nonzero outcomes;
- missing, empty, malformed, and repeated arguments;
- values containing spaces, globs, leading hyphens, newlines, and empty strings;
- pipeline and substitution producer failures;
- partial setup, failed writes, interrupted child processes, and repeated cleanup;
- symlinks and paths outside the allowed root;
- `/`, the home directory, and the workspace root as rejected destructive targets;
- supported Bash-version and operating-system boundaries; and
- sourced-library behavior when the file can be sourced.

Use an existing shell test framework when present. Bats or ShellSpec can help a substantial CLI, but a focused
repository test or direct integration scenario may be clearer for a small script. Test pure transformation
logic directly; reserve mocks for genuine side-effect boundaries.

## Evidence

Record the exact commands and fresh results. State which Bash versions, operating systems, signals,
privileges, or external dependencies were not exercised. A parser, linter, formatter, and happy-path run cover
different risks and cannot substitute for one another.
