# Validation

Portability is a contract over a POSIX edition, shell implementations, utilities, operating systems, and
runtime inputs. Each check covers only part of that contract.

## Establish the Baseline

Record the oldest required POSIX edition and any optional profiles or extensions. Use the current
[POSIX.1-2024 Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html)
and its linked utility specifications when POSIX.1-2024 is the target. Consult the edition matching an older
target instead of assuming the current standard is backward-compatible in every detail.

Inventory every external utility and option the script uses. A POSIX shell grammar does not make a script
portable when its utilities, flags, filesystem assumptions, locale behavior, or data formats fall outside the
declared baseline.

## Static Checks

- Parse every affected file with each available required shell. `sh -n` checks only the implementation bound
  to `sh` on that machine.
- Run ShellCheck with `-s sh` and the repository configuration. Read each diagnostic instead of suppressing it
  to obtain a green result; ShellCheck is an analyzer, not a conformance certificate.
- Run the configured formatter, commonly shfmt with its POSIX language mode. Formatting does not prove
  behavior or portability.
- Run `checkbashisms` when available as an additional extension detector. Its success does not establish that
  all language constructs and utility options satisfy the selected POSIX edition.
- Validate embedded shell inside CI or configuration with the owning format's checker as well as shell tools.

## Behavioral Checks

Run the script in an isolated temporary directory with real inputs. Inspect output, diagnostics, exit status,
files, permissions, and cleanup. Cover the consequential cases among:

- ordinary success and expected nonzero outcomes;
- missing, empty, malformed, repeated, and leading-hyphen arguments;
- values containing spaces, tabs, wildcard characters, newlines, and empty strings;
- pipeline, substitution, redirection, and external-utility failures;
- partial setup, interrupted child processes, and repeated cleanup;
- symlinks and paths outside the allowed root;
- every required shell and operating-system family; and
- sourced-library behavior when the file can be sourced.

Use the repository's existing test framework when present. A framework implemented in Bash may still test a
POSIX script as a subprocess, but the test file itself is not thereby portable `sh`.

## Evidence

Record exact commands and fresh results. Name the POSIX edition, shells, operating systems, utility versions,
locales, signals, privileges, and external dependencies exercised. State which declared environments and
failure paths remain untested. Do not infer broad Unix portability from success under `dash`, BusyBox `ash`,
or `bash --posix` alone.
