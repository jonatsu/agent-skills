# CLI Conventions by Area

Each area states this skill's default and the reason for it. A **rule** comes from a standard or a convention
that tools and users rely on, and breaking it causes failures. A **default** is a recommended choice: an
existing tool may keep a different one that it applies consistently, and a review reports only inconsistency
or harm, never the difference alone.

## Contents

- Streams and success output
- Machine-readable output
- Output to pipes and files
- Colour and decoration
- Prompts and non-interactive mode
- Destructive actions and confirmation
- Errors
- Exit codes
- Command grammar and names
- Arguments and flags
- Help and version
- Configuration and environment
- Secrets
- Signals and output files
- Progress
- Compatibility and deprecation
- Paging and telemetry
- Accessibility

## Streams and Success Output

- **Rule:** the command's result goes to stdout. Errors, warnings, progress, prompts, and status messages go to
  stderr, so that redirecting or piping stdout yields only the result.
- **Default:** a command that creates or changes something prints its capturable result on stdout, such as a
  bare ID or path, and a one-line confirmation on stderr. A script captures the ID with `$(tool item create)`,
  and a person still sees what happened.
- **Default:** `--quiet` (`-q`) silences the stderr confirmation only. It never silences the stdout result,
  because a script that passes `--quiet` still needs the ID.
- **Default:** a read command prints its data and nothing else.
- **Default:** next-step hints ("Next, run `tool login`") appear only after onboarding steps such as `init` or
  first login, and only when stderr is a terminal.

## Machine-Readable Output

- **Default:** `--format` is the one option that selects an output format, such as `--format json` or `--format plain`.
  `--json` is allowed as shorthand for `--format json`. One enum option avoids interacting boolean flags
  and completes well in shells.
- **Default:** `--format plain` prints one record per line with tab-separated fields. Use NUL separators where
  values can contain newlines, as file names can, or CSV where the data's consumers expect it. Document the
  choice per tool.
- **Rule:** a machine format, once published, is part of the contract (see Compatibility below). Keep keys
  stable and in one case style across commands; snake_case is the default for new tools.

## Output to Pipes and Files

- **Rule:** when stdout is not a terminal, drop terminal-only features: colour codes, spinners, cursor
  movement, carriage-return progress, and truncation to the window width. These corrupt files and break
  parsers.
- **Default:** keep the layout the same as on a terminal. A tool that switches to a different layout when piped
  surprises users who check their pipe by eye; scripts that need a stable shape ask for a machine format.

## Colour and Decoration

- **Default:** colour is on when the stream it is written to is a terminal.
- **Rule:** colour is off when that stream is not a terminal, when `NO_COLOR` is set to a non-empty value, or
  when `TERM=dumb`. `--color always` and `CLICOLOR_FORCE` or `FORCE_COLOR` force it on; `NO_COLOR` beats
  `CLICOLOR_FORCE`. Decide colour per stream: stdout may be a file while stderr is a terminal.
- **Default:** `--color auto|always|never`, with `auto` as the default. `--no-color` may exist as an alias for
  `--color never`.
- **Default:** use the basic 16 ANSI colours, so terminal themes control contrast. Use no background colours,
  which clash with light or dark themes.
- **Rule:** colour and symbols add to text and never replace it. Status words stay in the text so that they
  survive `grep`, screen readers, and colour blindness.

## Prompts and Non-interactive Mode

- **Rule:** prompt only when stdin and stderr are both terminals. Otherwise fail at once with an error that
  names the flag that supplies the missing value.
- **Rule:** never prompt when the non-interactive flag or variable is set, or when `CI` is set.
- **Default:** do not try to detect agents from environment variables; such detection is fragile.
- **Default:** when agents, scripts, or CI will call the tool, strongly recommend a non-interactive mode, and
  leave the decision to the user. Name it `--no-input` (short, and clig.dev's name) or `--non-interactive`
  (states the behaviour), by the user's preference, and use one name per tool. Reserve `--no-tty` for a tool
  that turns off every terminal feature, because the name describes a mechanism rather than the behaviour.
- **Default:** a variable named after the flag, `<TOOL>_NO_INPUT` or `<TOOL>_NON_INTERACTIVE`, turns the mode on
  for any non-empty value except `0`. A harness can set it once instead of adding a flag to every call. The flag
  wins over the variable, an optional opposite flag (`--input` or `--interactive`) overrides the variable for one
  call, and `--help` documents both.
- **Rule:** non-interactive mode only stops prompts. It never changes what the command does: a value that would
  have been asked for makes the command fail, naming its flag.
- **Why the pseudo-terminal matters:** an agent harness often runs commands under a pseudo-terminal, where
  `isatty()` is true and a prompt waits forever. The terminal check alone cannot catch that case.

## Destructive Actions and Confirmation

- **Rule:** an action that deletes or overwrites data the user cares about asks for confirmation on a terminal.
  The prompt names the exact target, its location (environment, project, path), the effect, and whether it can
  be undone. For the riskiest actions, ask the user to type the target's name.
- **Rule:** only `--yes` skips the confirmation, or `--force` where the project already uses it. A
  non-interactive run that needs a confirmation exits 2 at once and names `--yes`.
- **Default:** offer `--dry-run` for destructive or bulk operations. It renders exactly what the real run would
  do.
- **Rule:** a bare command with no arguments never performs a destructive action. It prints help or a usage
  error instead.

## Errors

- **Default:** the first line stands alone and can be searched: `tool: error: <what failed>: <cause naming the input>`,
  such as `mytool: error: cannot read config '/etc/mytool.toml': permission denied`. An error at a
  location in a file starts with `file:line:col:`, which editors and CI understand.
- **Default:** hint lines follow only when a fix is known, each giving one exact command or flag:
  `mytool: hint: pass --config PATH, or run as a member of the 'mytool' group`.
- **Rule:** a hint follows from the diagnosed cause. When the cause is unknown, say what to check. Never suggest
  a destructive command as a generic remedy, such as deleting a cache or a lock file, because a wrong remedy
  destroys data the error never involved.
- **Default:** tracebacks and debug data appear only with the tool's verbose flag or a debug variable. The
  verbose flag may also expand hints or add a short explanation of what the error means; judge from the tool's
  complexity whether that earns its code.
- **Default:** an unexpected internal error says it is a bug and gives a log path or the issue tracker.
- **Default:** stable error codes such as `E1042` are optional, for tools with documentation to search.
- **Default:** say whose problem it is: the user's input, the tool, or an outside service.
- **Default:** drop "illegal" and "bad". Keep "invalid" when the message names the value and the rule it broke:
  `invalid port '99999': must be 1-65535`.
- **Default:** suggest the nearest command or flag on a typo.

## Exit Codes

- **Rule:** 0 means success and any other value means failure.
- **Default:** 2 means the invocation itself is wrong and the tool can tell before doing any work: an unknown
  command or flag, a missing or malformed argument, a value out of range, or a missing confirmation in
  non-interactive mode. Most argument parsers already use 2.
- **Default:** 1 means a valid invocation failed while running: permission denied, a missing file, a network
  error, bad config content. A file named on the command line that does not exist is a runtime failure (1),
  because the tool learns it only when opening the file.
- **Rule:** after a signal, exit with 128 plus the signal number: 130 for SIGINT, 143 for SIGTERM. Re-raising
  the signal after cleanup has the same effect.
- **Default:** add other codes only when a script must act on the difference, such as "retry later" versus
  "give up". Document them; they become part of the contract.
- **Default:** use `sysexits.h` codes (64 to 78) only where the project already does.
- **Default:** a yes-or-no predicate command may follow `grep`: 0 for yes, 1 for no, 2 or more for an error.

## Command Grammar and Names

- **Default:** choose one grammar per tool with this test:
  - noun-verb (`tool item create`) when several kinds of thing each have their own set of actions;
  - verb-noun (`tool get item`) when a few uniform verbs apply across many resource types, so the noun acts as
    a parameter;
  - bare verbs (`tool sync`) when the tool manages one kind of thing.
- **Rule:** the same flag means the same thing in every command, and the same action has the same verb.
- **Default:** command names are lowercase words, with hyphens where needed. Avoid abbreviations except
  established ones (`ls`, `rm`), and avoid two commands whose names differ only subtly.

## Arguments and Flags

- **Default:** at most one kind of positional argument: the single object the command acts on (`delete <id>`),
  or a repeatable list of like items (`rm FILE...`). Use two different positionals only under a strong
  convention, such as `cp SRC DEST`. Everything else is a flag, including required values, because a flag names
  its value and the order stops mattering.
- **Rule:** every flag has a long form. Short forms are for the most-used flags only.
- **Rule:** `--` ends option parsing, and a file argument accepts `-` for stdin or stdout where that makes
  sense.
- **Default:** for new tools, `-v` means `--verbose`, `-V` means `--version`, and `-q` means `--quiet`. An
  existing tool keeps its meaning of `-v`; review reports only inconsistency within one tool.
- **Default:** validate all input before the first side effect, so that a usage error never leaves partial
  work.

## Help and Version

- **Rule:** `-h` and `--help` work on the tool and on every command. Requested help goes to stdout and exits 0.
  Help shown because of a usage error goes to stderr and exits 2.
- **Default:** help opens with one line on what the command does, then usage, then the most common examples,
  then options. A large tool may keep the full option list behind per-command help.
- **Default:** offer `help <command>` as well when the tool has subcommands.
- **Default:** in short lists, descriptions use sentence case with no final period; longer text uses full
  sentences. An existing tool keeps its style, and only inconsistency within one tool is a finding.
- **Rule:** `--version` prints the version to stdout and exits 0.

## Configuration and Environment

- **Rule:** precedence, highest first: flags, environment variables, project config, user config, system
  config, built-in defaults. A fix to one link restores the whole order, and the help text or documentation
  states the order.
- **Rule:** user config, data, cache, and state follow the XDG base directories (`XDG_CONFIG_HOME` and its
  siblings, with `~/.config` and the other defaults when unset) on Linux and other Unix systems.
- **Default:** environment variables use the tool's name as a prefix, such as `MYTOOL_REGION`, and each has a
  matching flag or config key.
- **Default:** when a consequential default comes from config or context, such as the target environment, say
  so in the output: `deploying to production (from .mytool.toml)`.

## Secrets

- **Rule:** never accept a secret as a flag value. Shell history keeps it, and `ps` shows it to other users.
- **Default:** environment variables, a file flag (`--token-file PATH`), stdin (`--password-stdin`), and a
  credential helper or keychain are equal channels. Help text names each channel's risks: child processes
  inherit environment variables, and debug output can expose them.
- **Rule:** never print a secret in an error, verbose or debug output, or a log. Show it redacted, such as
  `token=****abcd`.

## Signals and Output Files

- **Rule:** SIGINT and SIGTERM both stop the work, remove temporary files, and exit with 128 plus the signal
  number, without a traceback.
- **Rule:** write each output file to a temporary file in the same directory, and rename it over the target only
  on success. An interrupted run then leaves the previous file intact, and the next step of a pipeline never
  reads half a file.
- **Default:** a second Ctrl-C during cleanup exits at once.
- **Default:** on interrupt, print one line on stderr saying what was and was not written.

## Progress

- **Default:** work that takes longer than about a second shows progress on stderr, and only when stderr is a
  terminal.
- **Default:** prefer a count or phase (`[2/4] uploading`, `120/400 files`) over a bare spinner, and give a
  spinner a description of the work.

## Compatibility and Deprecation

- **Rule:** the machine contract stays stable: command and flag names and meanings, exit codes, machine-format
  output, environment variables, config keys, and error codes. Documentation states that human-readable text
  may change.
- **Rule:** a tool without a machine format treats its plain output as the contract until it adds one. Scripts
  parse human output whenever nothing else exists, which is why git added `--porcelain`.
- **Rule:** before changing human-readable output, search the project's scripts, tests, and CI files for code
  that parses it, and report what you find. For a widely used tool with no machine format, recommend adding one
  in the same change.
- **Rule:** additions are safe: a new flag, a new JSON key, a new command. Never give an existing flag, key, or
  exit code a new meaning.
- **Rule:** remove or rename through deprecation: keep the old form working, print a deprecation warning on
  stderr, and remove it at the next major version.
- **Rule:** the user may decide to break the contract to improve it. Before such a change or a conversion, list
  every breaking change with its alias or deprecation path, and get approval.

## Paging and Telemetry

- **Default:** no pager. A tool whose output is routinely long, such as logs or diffs, may page on a terminal
  only, honouring `PAGER` and offering `--no-pager`.
- **Default:** telemetry is opt-in. A project that insists on opt-out tells the user before the first data is
  sent, honours `DO_NOT_TRACK=1` and a tool-specific variable, and documents exactly what is sent.

## Accessibility

- **Rule:** meaning never depends on colour or symbols alone.
- **Default:** offer the plain format and the non-interactive mode as the path for assistive technology.
