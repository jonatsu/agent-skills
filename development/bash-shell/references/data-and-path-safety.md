# Data and Path Safety

Shell correctness depends on preserving argument and filename boundaries. Validation must address what a value means, not
only whether the shell parses it safely.

## Arguments and Data

- Store a command and its arguments in an array, then execute it with `"${command[@]}"`. Never build executable syntax in a
  string or pass untrusted data through `eval`.
- Quote expansions that represent one argument. Leave an expansion unquoted only when intentional splitting or globbing is
  part of a documented interface.
- Use `printf '%q'` to render an argument vector for Bash-oriented diagnostics. Do not execute the rendered text.
- Use NUL delimiters for arbitrary filenames. Check the producer's status separately when process substitution would hide
  it.
- Validate option values before shifting them. Reject missing operands, unknown options, invalid numbers, and extra
  positional arguments with a useful diagnostic and nonzero status.

## Temporary Resources and Cleanup

Create a temporary resource successfully before installing a cleanup trap. Keep it in a dedicated variable rather than
overwriting ambient variables such as `TMPDIR`. Restrict permissions when the contents are sensitive.

Cleanup should operate only on resources created and owned by this invocation. Validate the stored path again, use `--`
where the command supports it, and preserve the operation's original exit status. Cleanup must tolerate partial setup and
repeated invocation.

## Deletion and Recursive Operations

Before deleting or recursively modifying a path:

1. Reject empty values and broad roots such as `/`, the home directory, and the repository or workspace root.
2. Resolve the intended parent and target without following an attacker-controlled boundary unexpectedly.
3. Verify the target is inside the operation's owned or explicitly authorized scope.
4. Inspect symlinks, mount points, and concurrent replacement when they can change what the path names.
5. Preview the exact resolved targets when the operation requires confirmation or supports a dry run.

`rm -rf -- "$path"` satisfies only option and word-boundary handling. It does not satisfy these checks.

## Replacement Writes

For an atomic replacement, create the temporary file in the destination directory so the final rename stays on one
filesystem. Set the intended permissions and ownership, write and validate the complete content, then rename over the
destination. Clean up the temporary file on every failure path.

Decide explicitly how symlink destinations, existing metadata, durability requirements, and concurrent writers should be
handled. A rename alone does not settle those policies.
