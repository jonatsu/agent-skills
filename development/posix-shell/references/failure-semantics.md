# Failure Semantics

Treat shell options and status propagation as part of the program's interface. Their effects depend on syntax
and calling context, so inspect the complete control flow before selecting them.

## Shell Options

- `set -e` has exceptions in conditional lists, `&&` and `||` lists, negation, pipelines, and other contexts.
  Code that is safe only because the shell exits is incomplete at a consequential boundary.
- POSIX.1-2024 defines `pipefail`, but earlier POSIX editions do not. Enable it only when POSIX.1-2024 belongs
  to the declared baseline. Otherwise restructure the operation when an earlier pipeline element's status
  matters.
- `set -u` makes an unset parameter expansion fail. Use `${value-}` when absence is valid, and inspect optional
  positional parameters before expanding them.

Executable programs may select options at their entry point. Libraries should return statuses and leave the
caller's option state unchanged unless their documented interface says otherwise.

## Commands, Pipelines, and Subshells

- Put commands whose status matters in an explicit conditional or capture the status immediately.
- Treat an expected nonzero status as a branch instead of suppressing errors globally.
- A command substitution removes trailing newline characters. An assignment containing only a command
  substitution can expose its status, but surrounding commands and expansions can replace or obscure it.
- Pipeline elements may execute in subshell environments. Do not depend on variable assignments inside a
  pipeline surviving in the parent shell.
- Check redirection and setup failures before the operation they protect. A diagnostic command must not
  accidentally replace the meaningful status.

## Functions, Sourced Files, and Traps

Functions should return the status of the operation they represent. Prefix variables or use a subshell when
the declared portability baseline lacks a suitable function-local extension.

A sourced file shares the caller's variables, positional parameters, traps, options, and working directory.
Save and restore only state the library must change, and avoid changes whose original state cannot be restored
portably.

Install a cleanup trap only after every variable and resource it reads has a safe value. Capture the original
status before cleanup, make cleanup tolerate partial setup and repeated invocation, then preserve that status.
Use trap conditions defined by the declared POSIX edition; `0` is the portable exit condition for older POSIX
targets, while `EXIT` requires a baseline that specifies or verifies it.

Signal handling must account for owned child processes. Do not kill a process identified only by an
unvalidated or possibly reused process ID. Test termination behavior on the required shells because signal and
trap timing can expose implementation differences.
