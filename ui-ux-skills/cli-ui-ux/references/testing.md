# Testing CLI Behaviour

Lock the interface in with tests in the project's own test framework. Run the tool as a subprocess with a
temporary working directory, HOME, and XDG directories, and an environment you build for the test, so that a
test never touches the user's real data or inherits their credentials. Keep test copies inside the project's
test temporary directory or the agreed workspace.

## Contents

- Streams and exit codes
- Help and errors
- Colour and terminals
- Prompts and non-interactive mode
- Configuration precedence
- Signals and output files
- Machine output contract

## Streams and Exit Codes

Capture stdout and stderr separately and assert on both:

- a success writes its result to stdout and nothing else there;
- a failure writes nothing to stdout, an error to stderr, and exits 1;
- an unknown flag, a missing argument, and an out-of-range value each exit 2.

## Help and Errors

- Assert that `--help` exits 0 with usage on stdout, for the tool and each command.
- Keep golden files for help text when the project accepts them, so that a change to help shows up in review.
- For each error the change adds, assert on the first line's form and that it names the input.

## Colour and Terminals

Run the command once with stdout piped and assert that no `\x1b[` escape appears. Run it again under a
pseudo-terminal, which Python's `pty` module or a library such as `pexpect` provides, and assert that colour
appears. Repeat under the pseudo-terminal with `NO_COLOR=1` and with `TERM=dumb`, and assert no escapes.

## Prompts and Non-interactive Mode

- With stdin from `/dev/null`, assert that a command needing input exits at once (use a timeout of a few
  seconds), exits 2, and names the flag that supplies the value.
- Under a pseudo-terminal, assert that the prompt appears, and that answering "no" leaves no change.
- Under a pseudo-terminal with the non-interactive flag or variable set, assert that no prompt appears and the
  command fails naming the flag. This is the agent-harness case; a terminal check alone fails it.
- With `--yes`, assert that the confirmed action happens without a prompt.

## Configuration Precedence

Test the order as a matrix rather than one link: for one setting, set every source to a distinct value (flag,
environment, project config, user config under a temporary `XDG_CONFIG_HOME`, system config if any), then remove
the highest one at a time and assert that the next source wins. Repeat for a second setting to show the order is
general.

## Signals and Output Files

Start the command with a pre-existing, valid output file and its own process group. Send SIGINT after it begins
writing, then assert:

- the exit status is 130, or the process died from SIGINT;
- stderr holds no traceback;
- the previous output file is byte-identical;
- no temporary file is left behind.

Repeat with SIGTERM (exit 143). Run once without interruption and assert that the output is complete and valid.

## Machine Output Contract

Parse the `--format json` output and assert on the keys and types scripts rely on. When the project has
scripts, CI steps, or tests that consume the tool's output, run them against the changed tool, because they are
the contract's real consumers.
