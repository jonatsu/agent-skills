---
name: cli-ui-ux
description: Design, build, and review the user-facing interface of command-line tools, covering commands and flags, help text, output and JSON formats, errors, exit codes, colour, prompts, configuration, and signals. Use when designing a new CLI, adding or changing a command, fixing output that breaks pipes or hangs automation, or reviewing or testing a CLI's usability. Use bash-shell or posix-shell for shell scripting technique; full-screen terminal UIs are out of scope.
license: MIT
compatibility: The probe script needs Python 3.9 or later; its terminal modes need a POSIX system.
metadata:
  author: Joonas Onatsu
---

# CLI UI and UX

Shape the contract a command-line tool offers to the people, scripts, and agents that call it: its commands,
arguments, help, output, errors, exit codes, configuration, prompts, and signal handling. The same standard
serves three modes, and each mode applies it at a different moment:

- **Design** a new interface or command before code exists.
- **Implement** a new command, or change an existing one.
- **Review** an existing tool, or test its behaviour.

Full-screen terminal interfaces with their own layout and keybindings are out of scope. Inline prompts, progress
lines, and terminal detection are in scope, because every CLI meets them.

## Whose Conventions Apply

An existing tool keeps its own conventions, because consistency inside one tool matters more than any default.
Where a convention gives poor UX, recommend the improvement and name the default it would move to. A new tool
uses the defaults below. When the user asks to convert an existing tool to these defaults, convert it, and treat
every change to the machine contract as a breaking change (see [Change the Contract
Deliberately](#change-the-contract-deliberately)).

## The Defaults

Each line is this skill's default; [references/conventions.md](references/conventions.md) gives the detail and
the reason for each, area by area. Read it when designing, converting, or reviewing a tool.

- **Streams:** the command's result goes to stdout. Errors, warnings, progress, prompts, and confirmations go to
  stderr. A command that creates something prints its capturable result (a bare ID or path) on stdout.
- **Success output:** a command that changes state prints a one-line confirmation on stderr. `--quiet` silences
  that line and never the stdout result. A read command prints only its data.
- **Machine output:** scripts get a format only on request: `--format json` or `--format plain`, with `--json`
  as shorthand. Plain output is tab-separated unless the data needs NUL or CSV.
- **Piped output:** when stdout is not a terminal, drop colour, spinners, and width truncation, and keep the
  layout the same.
- **Colour:** on for a terminal, off when the stream is not a terminal, `NO_COLOR` is set and non-empty, or
  `TERM=dumb`. `--color auto|always|never` overrides. Colour adds to text and never carries meaning alone.
- **Prompts:** prompt only when stdin and stderr are both terminals, `CI` is unset, and the run is not
  non-interactive.
- **Non-interactive mode:** when agents, scripts, or CI will call the tool, strongly recommend one flag
  (`--no-input` or `--non-interactive`, the user's choice) plus a `<TOOL>_NO_INPUT` or `<TOOL>_NON_INTERACTIVE`
  variable. It stops prompts and never changes what the command does.
- **Confirmation:** only `--yes`, or `--force` where the project already uses it, skips a confirmation. A run
  that needs a confirmation it cannot ask for exits 2 at once and names `--yes`.
- **Errors:** the first line stands alone, as `tool: error: <what failed>: <cause naming the input>`. Hint lines
  follow only when a fix is known. Tracebacks appear only in verbose or debug mode.
- **Exit codes:** 0 for success, 1 when a valid invocation fails, 2 when the invocation itself is wrong, and 128
  plus the signal number after a signal (130 for Ctrl-C). Add other codes only when scripts must act on them.
- **Grammar:** noun-verb (`tool item create`) when several kinds of thing each have their own actions. Use
  verb-noun when a few uniform verbs apply to many resource types, and bare verbs for a single kind of thing.
  Use one form throughout a tool.
- **Arguments:** at most one kind of positional argument: the object acted on, or a list of like items such as
  `FILE...`. Everything else is a flag, including required values.
- **Configuration:** precedence runs flags, then environment, then project config, then user config (XDG), then
  system config, then built-in defaults.
- **Signals:** SIGINT and SIGTERM both clean up. Write output files to a temporary file and rename it on
  success. A second Ctrl-C exits at once.
- **Secrets:** never accepted as flag values. Environment variables, files, stdin, and credential helpers are
  equal channels, and help text names each one's risks. Print a secret only redacted.

## Rules for Every Mode

Capable agents commonly miss these rules, so apply each one deliberately.

### Change the Contract Deliberately

The machine contract is what scripts depend on: command and flag names and meanings, exit codes, machine-format
output, environment variables, config keys, and error codes. Human-readable text may change, except in a tool
that has no machine format. There, its plain output is the contract until one exists.

Before changing anything in the contract, search the project's scripts, tests, and CI files for its consumers.
Then propose a transition, such as keeping the old JSON key beside the new one for a release, or an alias with a
deprecation warning on stderr. Get the user's approval for the break before making it. Never make the breaking
change and report it afterwards, because the user can no longer choose the transition. Before changing
human-readable output, run the same search for scripts that parse it.

### Assume Agents Run Commands Under a Pseudo-terminal

An agent harness often gives commands a pseudo-terminal, so `isatty()` reports a terminal and a prompt hangs
the run. A terminal check alone therefore does not fix an agent hang. Recommend the non-interactive mode, and
tell the user exactly what the calling pipeline must pass, such as `--yes` or the variable.

### Keep the Safeguard

Never remove a confirmation, or confirm automatically, to make a hang or a failure go away. Deadline pressure
does not change this, because the confirmation is the only guard against an unintended destructive run. Make
the caller confirm explicitly instead.

### Fix the Whole Mechanism

When the reported defect sits in a mechanism, such as a precedence order, a signal handler, or a naming
convention, check the whole mechanism. Fix every broken part of it in the same change, or name each remaining
part as an open question for the user.

### Report Every Inconsistency

When adding to an existing tool, list the conventions its commands use for flags, output keys, streams, and exit
codes. Report every inconsistency you find, even when the change follows the majority.

## Design

Write the interface before the code, because help text is a specification a reviewer can read:

1. List the users and callers: people, scripts, CI, agents. Note which ones cannot answer a prompt.
2. Map tasks to a command tree, and choose the grammar by the rule above.
3. Draft the help text for every command, with at least one realistic example each.
4. Write the exit-code table, the machine output shapes, and the config and environment variables.
5. Mark each destructive operation with its confirmation, `--yes`, and `--dry-run`.

The design is done when every command has help text and every failure has an exit code and an error message.

## Implement

Before writing code, read the existing commands and record their conventions. Follow them, and report every
inconsistency. Apply the defaults to new behaviour only where the tool has no convention. Then test the
behaviour the change touches; [references/testing.md](references/testing.md) gives a test recipe for each area.

## Review

Follow [references/review.md](references/review.md). It covers reading before running, the probe pass, the areas
to check, and the report shape.

## Run a CLI Safely

Before running a tool you are testing or reviewing, sort its commands into four groups: read-only, changes data,
destroys data, and reaches beyond the machine. Use its help text and code to sort them. Then:

- Run probes through `scripts/probe_cli.py`, which gives every run a sandbox copy of the working directory, a
  temporary HOME, an environment without inherited credentials, a timeout, and a killed process group.
- Run data-changing and destroying commands only against a disposable copy, inside the agreed workspace or a
  temporary directory. Leave the user's real data untouched, because restoring it after the fact is not safe.
- Judge commands that reach beyond the machine from code, unless the user names and authorizes a test target.
- When the tool writes to absolute paths, system files such as `/etc`, services, or devices, stop. Recommend a
  container or a sandbox such as `bwrap`, and ask the user before running it.

From this skill's directory, run `python3 scripts/probe_cli.py --help` for its options. A typical call is
`python3 scripts/probe_cli.py --workdir . --help-for deploy --modes pipe,tty -- ./bin/tool`.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources this skill is based on.
