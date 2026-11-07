# Reviewing a CLI

A review judges a tool's interface against [conventions.md](conventions.md) and reports findings the owner can
act on. It changes nothing in the project: findings go into the report, and fixes or tests are separate work.

## Contents

- Read before running
- Probe the tool
- Check each area
- Judge findings
- Write the report

## Read Before Running

1. Read the help text, README, man page, and the argument-parsing code. Note the tool's own conventions: its
   grammar, flag names, output formats, stream use, and exit codes.
2. Sort every command into four groups: read-only, changes data, destroys data, and reaches beyond the machine
   (network, cloud, sending). Read the code paths of the bare command and of `--help`, because some tools act
   there.
3. Note where the tool writes. When it writes to absolute paths, system files such as `/etc`, services, or
   devices, stop and ask the user before running anything; recommend a container or a sandbox such as `bwrap`.

The step is done when every command has a group and you know which ones are safe to run in the sandbox.

## Probe the Tool

Run `scripts/probe_cli.py` from the skill's directory with the tool's working directory as `--workdir`. Add
`--help-for` for each subcommand, `--probe` for each read-only command worth observing, `--skip-bare` when
the bare command acts, and `--home-from` when the tool loads libraries or config from HOME. Use
`--modes pipe,tty,tty-no-color,tty-dumb` to cover colour handling, and `--isolate-network` when the tool might
reach the network and the system supports it.

Run commands from the "changes data" and "destroys data" groups only through `--probe`, so that each one acts on
its own sandbox copy. Never run commands that reach beyond the machine unless the user named and authorized a
test target.

Read the JSON report for each probe: the exit code, stdout and stderr kept apart in `pipe` mode, ANSI escapes
per stream, timeouts in `tty` mode (a prompt waiting for input), and files created, deleted, or modified in the
sandbox copy and HOME.

## Check Each Area

Check every area below. For each one, name the command or code line that shows the behaviour:

- **Discovery:** `-h`, `--help`, `help`, and per-command help work; help leads with purpose and examples;
  `--version` works.
- **Safety:** the bare command does nothing destructive; destructive commands confirm, offer `--yes` and
  `--dry-run`, and name their target.
- **Streams:** results on stdout; errors, progress, and prompts on stderr.
- **Exit codes:** failures exit non-zero; usage errors are distinguishable; signals give 128 plus the number.
- **Errors:** what failed, the cause naming the input, and a next step that follows from the cause.
- **Output:** machine formats exist where scripts need them; piped output carries no terminal codes.
- **Colour:** off when piped, under `NO_COLOR`, and under `TERM=dumb`; meaning never depends on colour alone.
- **Interactivity:** prompts only on terminals; a non-interactive path exists for scripts and agents, including
  under a pseudo-terminal.
- **Consistency:** the same flag means the same thing everywhere; output keys share one style; every command
  uses the streams and exit codes the same way. List every inconsistency.
- **Configuration:** the precedence order holds across flags, environment, and config files; XDG locations.
- **Secrets:** no secret accepted as a flag value; no secret printed.
- **Signals:** Ctrl-C and SIGTERM clean up; output files are never left half-written.
- **Compatibility:** machine output and flags look stable; deprecations warn before removal.

## Judge Findings

Grade each finding by its consequence:

- **High:** data loss, a hang in automation, a broken pipeline or script, a secret exposed.
- **Medium:** a misleading error, a missing machine format that scripts need, inconsistency that causes misuse.
- **Low:** friction or style that slows a person down.

Report a departure from one of this skill's defaults only when the tool is inconsistent with itself or the
choice causes harm. A tool that applies its own convention consistently, such as `-v` for version or verb-noun
grammar, has no finding there.

## Write the Report

Lead with the findings, ordered by severity. Give each finding:

1. a one-line statement of the problem;
2. the evidence: the command run or the code line, and what it showed;
3. the convention it breaks, marked as a rule or a default;
4. the fix, as a concrete change; and
5. a regression test that would catch it, from [testing.md](testing.md).

After the findings, list what was not checked and why, such as commands that reach the network. Write the
report where the user asks; without a stated path, return it inline rather than writing into the project.
