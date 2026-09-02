# Failure Semantics

Use shell options and status propagation as part of the program's interface. Their effects depend on syntax
and calling context, so inspect the whole control flow before enabling them.

## Shell Options

- `set -e` has exceptions in conditional tests, `&&` and `||` lists, negation, and pipeline elements. Code
  that is safe only because the shell exits is incomplete at a consequential boundary.
- `set -o pipefail` makes a pipeline return the rightmost failing element's status. Enable it when that
  behavior matches the script's contract, then inspect pipelines whose early termination or probing failures
  are expected.
- `set -u` turns an unset expansion into an error. Use `${value-}` or `${value:-default}` where absence is
  valid, and check optional positional parameters before expanding them.
- `set -E` changes `ERR` trap inheritance. It does not make `ERR` a universal exception handler.

Executable scripts may select options near their entry point. Libraries should return statuses and leave the
caller's option state alone unless their documented API says otherwise.

## Commands, Pipelines, and Substitutions

- Put commands whose status matters in an explicit conditional or capture the status immediately.
- Treat an expected nonzero result as a branch, not as an error to suppress globally.
- Command substitution exposes the substitution's final status through the containing assignment only in
  specific forms. Keep the assignment separate when its status matters.
- Process substitution does not automatically propagate the producer's failure to the consumer. Use an
  observable process status, a temporary file, or another design when producer success is required.
- A pipeline can run elements in subshells. Do not assume variable mutations inside a pipeline survive in the
  parent shell.

## Functions and Traps

Functions should return meaningful statuses. Do not let a final diagnostic command replace the status of the
operation the function represents.

Capture `$?` as the first cleanup action, make cleanup idempotent, and exit with the captured status after
cleanup. Install a trap only after every variable and resource it reads has a safe value. Prefer one lifecycle
dispatcher over several traps that overwrite one another.

Forward termination signals to owned child processes, wait for them, and clean up on ordinary exit as well as
signals. Never kill processes identified only by a reused or unvalidated PID.

## Version Checks

Compare version components lexicographically. A test for Bash 4.4 or newer must accept Bash 5.0:

```bash
if ((BASH_VERSINFO[0] < 4 ||
      (BASH_VERSINFO[0] == 4 && BASH_VERSINFO[1] < 4))); then
  printf 'Bash 4.4 or newer is required\n' >&2
  exit 2
fi
```

Prefer feature avoidance or a documented minimum version over scattered version branches.
