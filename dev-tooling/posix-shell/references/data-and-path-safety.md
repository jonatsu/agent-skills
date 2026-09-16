# Data and Path Safety

Portable shell code must preserve argument and filename boundaries without Bash arrays. Validation must also
address what a value means, because quoting alone does not make an operation safe.

## Arguments and Data

- Keep an argument vector in positional parameters and forward it with `"$@"`. Use `set -- "$@" value` to
  append one value without reparsing existing arguments.
- Quote expansions that represent one argument. Leave an expansion unquoted only when intentional field
  splitting or pathname expansion is a documented part of the interface.
- Do not store arbitrary arguments or filenames in delimiter-separated variables. Every possible text
  delimiter can occur in a pathname, and shell variables cannot contain NUL bytes.
- Prefer scoped reads such as `while IFS= read -r line` over changing the ambient `IFS`. If a global change is
  unavoidable, preserve whether `IFS` was unset as well as its value and restore both states.
- Validate an option's operand before shifting it. Reject missing operands, unknown options, invalid numbers,
  and extra positional arguments with a useful diagnostic and nonzero status.

POSIX text files end records with newline characters. Processing arbitrary pathnames may require a non-POSIX
NUL-delimited producer and consumer; declare and test those extensions rather than presenting them as portable
POSIX utilities.

## Option and Path Boundaries

`--` is portable only for utilities whose specification or required implementations accept it. When a path
operand may begin with a hyphen and no portable delimiter exists, validate it and pass an equivalent
unambiguous pathname such as `./relative-name`. Do not rewrite arbitrary user data as though it were a path.

Before deleting or recursively modifying a path:

1. Reject empty values and broad roots such as `/`, the home directory, and the workspace root.
2. Resolve the intended parent and target without crossing an attacker-controlled boundary unexpectedly.
3. Verify the target is inside the operation's owned or explicitly authorized scope.
4. Inspect symlinks, mount points, and concurrent replacement when they can change what the path names.
5. Preview the exact resolved targets when confirmation or a dry run is required.

## Temporary Resources and Cleanup

POSIX does not specify `mktemp`. When the environment provides it as a declared dependency, verify the required
interface and check that creation succeeded before installing cleanup. Otherwise use a design appropriate to
the threat model, such as an atomically created private directory with restrictive permissions and collision
handling. Do not invent a predictable temporary-file fallback and call it secure.

Cleanup should operate only on resources created by this invocation. Initialize cleanup variables before
installing traps, validate stored paths again, tolerate partial setup, and preserve the operation's original
status.

## Replacement Writes

Create replacement content completely, apply required permissions, and validate it before changing the
destination. If the replacement must be atomic, confirm that the selected utility and source/destination
filesystem arrangement provide that guarantee. Decide explicitly how symlinks, existing metadata, durability,
and concurrent writers should behave.
