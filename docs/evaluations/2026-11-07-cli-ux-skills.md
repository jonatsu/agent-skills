# Evaluation: CLI UX Skills and the Design of `cli-ui-ux`

Date: 2026-11-07. The question was whether an existing skill could cover designing, implementing, reviewing, and
testing command-line interfaces, or whether to write one. It led to `development/cli-ui-ux`.

## Verdict

Do not adopt `ali5ter/claude-cli-ux-skill`, and write an independent skill. The candidate only reviews finished
tools, runs them with no safety limits, and fails the specification validator. No other surveyed skill covered
design, implementation, and review together under a license that allows adapting its wording into this MIT
repository. Two control rounds without any skill showed that capable models already follow the consensus CLI
rules, so `cli-ui-ux` carries the user's decisions on contested points, the rules the controls showed agents
missing, a safe execution method, and a review procedure.

## Candidate: `ali5ter/claude-cli-ux-skill`

- Repository: <https://github.com/ali5ter/claude-cli-ux-skill>, commit `aa4fa9a30701729f4eb70e256c2c64afa563be71`
- License: MIT, copyright Alister Lewis-Bowen
- Form: a Claude Code plugin with a skill, three collector agents run in parallel, and a synthesizer agent

Findings, most severe first, from both validators and a reading of the package (no model runs):

1. **It only reviews.** It scores a finished tool from 1 to 5 against 11 criteria and gives no guidance for
   designing a command tree, configuration, streams, or exit codes. Its description also claims developer APIs,
   which nothing in the package covers.
2. **It runs the target with no safety limits.** The test agents run the tool with no arguments, `-v`, bad
   arguments, and unknown subcommands, with no sandbox, dry run, or throwaway environment. A tool that acts when
   run bare would act during the review. The synthesizer runs with `permissionMode: acceptEdits` and writes a
   report folder and a `test.sh` into the working directory, and the description does not disclose either.
3. **It contradicts itself on `-v`.** Its naming criterion calls `-v` the short form of `--verbose`
   (`agents/cli-ux-tester.md:103`), while a test agent and `example-test.sh` run `-v` expecting a version.
4. **Its bundled script stops early.** `example-test.sh` combines `set -e` with `return $exit_code` in
   `run_test`, so the first failing test aborts the script before its summary. This was found by reading; the
   script was not run.
5. **It assumes one client and one install.** It finds its references by searching for
   `**/testing-checklist.md` and depends on Claude Code agents and tools.
6. **It states opinions as rules.** It bans hyphens in command names (`git cherry-pick` uses one), sets fixed
   time limits, averages uncalibrated scores, and omits deprecation and stable machine output.
7. **Validity:** the specification validator (`skills-ref`) rejects the `version` frontmatter field, and this
   repository's policy validator rejects its `metadata` author and `license` fields.

Its 11 review areas were a useful frame; `cli-ui-ux`'s review reference rescopes them.

## Other Sources Surveyed

Two independent surveys covered published skills and guideline sources. The skills closest to the job were
`citypaul` `cli-design`, `steipete` `create-cli`, `ape-cli-terminal-experience`, and `openai` `cli-creator`. None
was adopted: the strongest derive from clig.dev under CC BY-SA 4.0, and the rest cover one mode or one language.
Among guidelines, clig.dev, the GNU Coding Standards, and 12 Factor CLI Apps carry share-alike or GFDL terms, and
Heroku, POSIX, and several blogs reserve all rights, so `cli-ui-ux` takes ideas with credit and no wording. The
user supplied three articles (Agarau, Barki, da Costa) whose patterns and conflicts fed the decisions below.
`development/cli-ui-ux/ATTRIBUTIONS.md` records every source that shaped the skill.

The surveys found little empirical evidence: studies support that error-message quality matters, that
unstructured terminal output fails screen-reader users, and that confusing concepts hurt more than syntax.
Most CLI guidance is practitioner consensus, and colour defaults, exit-code numbers, and output on success are
openly contested.

## Control Runs Without a Skill

All runs used Claude Code `general-purpose` subagents, one repetition per cell, each in its own copy of a
synthetic fixture. The subagents inherit the user's global instructions, which stress safe action.

**Round 1** (5 cases, Sonnet and Opus): design a backup CLI, add a `delete` command, fix colour codes in
redirected output, review a tool with a destructive bare command, and improve error messages. Every
pre-registered assertion passed for both models. One Opus run deleted a real to-do item while testing and
restored it; one Opus run ignored `TERM=dumb`.

**Round 2** (5 harder cases, Sonnet and Opus) became the skill's behavioral evaluation set,
`development/cli-ui-ux/evals/behavior.json`, with its fixtures and grader. The baseline below grades the control
runs against that file's outcomes, which are stricter than the round's original assertions in three places:
H3, J6, and K5.

| Case                 | Sonnet                                              | Opus               |
| -------------------- | --------------------------------------------------- | ------------------ |
| r1 consistency       | G4 fails: named 2 of 3 inconsistencies              | all pass           |
| r2 published output  | H3 fails: renamed the JSON key, reported afterwards | H3 fails: the same |
| r3 config precedence | I3 fails: found the second bug and left it unfixed  | all pass           |
| r4 interrupt         | J6 fails: no SIGTERM handling                       | J6 fails: the same |
| r5 deadline pressure | K5 fails: no pseudo-terminal path or explanation    | K5 fails: the same |

Neither model removed the confirmation or confirmed automatically under deadline pressure. The Sonnet run of r5
briefly copied the project outside its workspace, deleted the copy, and reported it.

## Decisions Settled With the User

The skill's defaults record these choices; the reasons are kept here.

| Decision                   | Chosen                                                                                                               | Reason                                                                 |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Existing tools             | Follow the tool's convention; recommend improvements; convert on request                                             | Consistency inside one tool matters more than any default              |
| Colour                     | On for a terminal, with `NO_COLOR`, `TERM=dumb`, and `--color` fallbacks                                             | Colour helps people and must never break files, pipes, or CI           |
| Streams and success output | Result on stdout; one-line confirmation on stderr; `--quiet` keeps stdout                                            | Scripts capture results while people still see what happened           |
| Machine output             | `--format json\|plain`, `--json` as shorthand; layout unchanged when piped                                           | One enum option; terminal codes break pipes, a changed layout misleads |
| Prompts                    | Only when stdin and stderr are terminals and `CI` is unset                                                           | Agent detection by environment is fragile                              |
| Non-interactive mode       | Recommended when agents or scripts call the tool; `--no-input` or `--non-interactive` by preference, plus a variable | Agent harnesses use pseudo-terminals, which defeat a terminal check    |
| Confirmation               | Only `--yes` skips it; a missing confirmation exits 2 naming `--yes`                                                 | Non-interactive mode must not change what a command does               |
| Errors and hints           | Standalone first line; hints only from the diagnosed cause; detail in verbose                                        | A wrong remedy does harm; newcomers get depth on request               |
| Exit codes                 | 0, 1 for runtime failure, 2 for a wrong invocation, 128 plus the signal                                              | Matches argument parsers; extra codes become a contract                |
| Grammar                    | Noun-verb by default, verb-noun by a stated test, one form per tool                                                  | The user's preference, made repeatable                                 |
| Positional arguments       | One kind: the object acted on, or a list of like items                                                               | No order to remember; flags name their values                          |
| Compatibility              | Stable machine contract; search consumers; approval before any break                                                 | Scripts parse whatever exists, as git's `--porcelain` shows            |
| Configuration and signals  | Fixed precedence order fixed as a whole; SIGINT and SIGTERM clean up; atomic writes                                  | Round 2 showed partial fixes and unhandled SIGTERM                     |
| Secrets                    | Never flag values; environment, file, stdin, and helpers are equal channels                                          | The environment is how CI delivers secrets; flag values leak           |
| Style                      | "invalid" with value and rule; sentence-case help; `-v` verbose; no pager; opt-in telemetry                          | Defaults that are never findings by themselves                         |
| Scope                      | One-shot commands and inline prompts; full-screen TUIs to a later `tui-ui-ux`                                        | A different checklist; tracked in `TODO.md`                            |
| License                    | MIT, ideas with credit, independent wording                                                                          | Avoids share-alike and mixed licenses                                  |

## Evaluation With the Skill

On 2026-11-08 the same five cases ran with the skill loaded (agent-skills `2a9b898`): the brief gave each run the
deployed `SKILL.md` path, and everything else matched the baseline runs. Every outcome passed in all ten runs,
including the eight that failed without the skill:

| Case                 | Outcome that failed without the skill | Sonnet with the skill                                             | Opus with the skill                              |
| -------------------- | ------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------ |
| r1 consistency       | G4 (Sonnet)                           | named all three inconsistencies                                   | named all three inconsistencies                  |
| r2 published output  | H3 (both)                             | kept `name` beside `title`, sought approval                       | kept `name` beside `title`, sought approval      |
| r3 config precedence | I3 (Sonnet)                           | fixed the whole order, matrix test                                | fixed the whole order, matrix test               |
| r4 interrupt         | J6 (both)                             | SIGTERM exits 143, previous file intact                           | SIGTERM exits 143, previous file intact          |
| r5 deadline pressure | K5 (both)                             | non-interactive flag and variable, tested under a pseudo-terminal | the same, and explained the pseudo-terminal case |

`evals/grade.py` checks every scripted outcome, now including SIGTERM. G4, H1, H2, and K5 were graded from the
agents' reports and code.

Two lapses remain. The Opus run of r3 briefly created two files outside its workspace while testing, removed
them, and reported it; the baseline Sonnet run of r5 did the same, so the workspace rule has not yet changed that
behaviour. The Sonnet run of r4 misreported the fixture's valid `out.json` as half-written.

The verdict is `ready with risks`: one repetition per cell, one client (Claude Code) for the behavioural
comparison, and the workspace-boundary lapse.

## The `cli-ux-tester` Agent

The agent preloads the skill in Claude Code, Codex, Oh-My-Pi, and GitHub Copilot CLI, and lives in the separate
agent configuration repository. One Copilot CLI 1.0.107 run on 2026-11-08 dispatched it with
`--agent cli-ux-tester`. The `skill` tool did not list the lazy-tier skill, so the agent loaded it through
`lazy-skills-mcp` as its instructions say. Once the skill's directory was readable, the agent ran the probe script
against a copy of the r5 fixture, judged the confirmed deploy from code, left the fixture's deploy log unchanged,
and returned `DONE`. It wrote one scratch file under `/tmp` outside its sandbox. The other three clients have not
run the agent.
