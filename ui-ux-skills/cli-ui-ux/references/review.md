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

Run `scripts/probe-cli.py` from the skill's directory with the tool's working directory as `--workdir`. Add
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

- **Fit:** the surface suits the job, as `SKILL.md` describes under "Fit the Surface to the Job". A dedicated
  CLI that recipes would serve is a finding, and so is a recipe set that has outgrown recipes.
- **Discovery:** `-h`, `--help`, `help`, and per-command help work; help leads with purpose and examples;
  `--version` works.
- **Safety:** the bare command does nothing destructive; destructive commands confirm, offer `--yes` and
  `--dry-run`, and name their target.
- **Streams:** results on stdout; errors, progress, and prompts on stderr. A wrapper writes nothing of its own
  to stdout.
- **Exit codes:** failures exit non-zero; usage errors are distinguishable; signals give 128 plus the number. A
  wrapper passes its child's status through and keeps only 125, 126, and 127; it forwards signals to the child.
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

Give each finding one tier, by its consequence:

- **Must fix:** data loss, a hang in automation, a broken pipeline or script, or a secret exposed.
- **Should fix:** a misleading error, a missing machine format that scripts need, or an inconsistency that causes
  misuse.
- **Consider:** friction or style that slows a person down. Report at most five, and say how many you left out.

Report a departure from one of this skill's defaults only when the tool is inconsistent with itself or the
choice causes harm. A tool that applies its own convention consistently, such as `-v` for version or verb-noun
grammar, has no finding there.

The review is done when every area above is checked or listed as not checked with its reason, and each finding
carries its evidence.

## Write the Report

1. **Verdict**: `Ready`, `Ready after changes`, or `Not ready`, then one sentence saying why. Any open Must fix
   finding rules out `Ready`; use `Not ready` when the interface needs redesign rather than local fixes.
2. **Scope**: the tool and version reviewed; how you reviewed it, by code reading or by probes and in which modes;
   and each area not checked, with why, such as commands that reach the network.
3. **Findings**, most consequential first, each tagged `F1`, `F2`, and so on. Give each its tier, a one-line
   statement of the problem, the evidence (the command run or the code line, and what it showed), the convention it
   breaks marked as a rule or a default, and the fix as a concrete change. Add a regression test from
   [testing.md](testing.md) when the defect could return as a failure that would otherwise pass silently and cost
   something, or when the user or the repository's test policy asks for one.
4. **Unverified**: behaviour you suspect but could not probe, each with the probe or test target that would
   settle it.
5. **Next checks**: the probes or tests still to run, and the reviews to run next.
6. **What holds**, only when something specific should survive a redesign: at most two sentences, with its
   command or code line.

A tool with no findings gets the verdict, the scope, and the next checks. Write the report where the user asks;
without a stated path, return it inline rather than writing into the project.
