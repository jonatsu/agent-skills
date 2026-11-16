# Evaluation: the `usability` Skill

Date: 2026-11-16. The question was how to give agents a general usability skill for any interface people
operate, filling the gaps that medium-specific skills such as `cli-ui-ux` leave. It led to
`ui-ux-skills/usability`. The source survey behind it is
[2026-11-16-usability-sources.md](2026-11-16-usability-sources.md).

## Verdict

`ready with risks`. Without the skill, Sonnet and Opus already find the planted problems and give no invented
score. They miss three things: they do not recommend testing with real users, they over-write a quick check, and
they report a walkthrough as a severity list. With the skill, every outcome passed in all ten runs of the final
round. The risks are one repetition per cell, one client (Claude Code), and no case yet for design mode, review
mode, the holistic review, or a voice interface.

## Decisions Settled With the User

| Decision      | Chosen                                                                                          | Reason                                                                      |
| ------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Scope         | Any interface people operate; a medium-specific skill wins where one exists                     | One catch-all, with `cli-ui-ux` keeping its own CLI questions               |
| Kinds of work | Design, evaluate, review; evaluate by audit, walkthrough, or holistic review                    | The split third-party audit skills use, with one reference per method       |
| Inputs first  | Users, tasks, and context before any judgement                                                  | ISO 9241-11 defines usability for specified users, goals, and context       |
| Principles    | Eight, drawn from where Nielsen, Shneiderman, Norman, and ISO 9241-110 agree                    | Shared ground rather than one author's list                                 |
| Medium        | Translate each principle through words, visuals, physical objects or space, time, and behaviour | Keeps the skill independent of the medium                                   |
| Severity      | Nielsen's 0 to 4 scale, rated by consequence; no total score or percentage                      | An inspection measures nothing, so a score claims a measurement nobody made |
| Depth         | A short quick check, or a full evaluation                                                       | The lesson of `cli-ui-ux` case r6: keep the effort proportionate            |
| Limits        | Every report says an expert review predicts and names the user test that would confirm it       | Real users confirm; several evaluators find more                            |
| Exclusions    | Accessibility conformance and safety-critical domains point elsewhere                           | Each needs its own standard and method                                      |

## Cases

`ui-ux-skills/usability/evals/behavior.json` holds five cases with planted problems:

- **u1:** a web sign-up form for phone users, with seven planted problems.
- **u2:** a two-button thermostat panel specification, before the hardware is built.
- **u3:** a quick check of a three-engineer internal page whose double-click starts parallel rebuilds.
- **u4:** a walkthrough of sharing an album, as a first-time user.
- **u5:** a command-line tool, which should defer to `cli-ui-ux`. It runs only with the skill.

`evals/grade.py` checks the scripted outcomes: no score or percentage, the word limit for u3, and no invented
rates or times for u4. The rest were graded from each report.

## Control Runs Without the Skill

Claude Code `general-purpose` subagents ran each case once per model, in its own copy of the fixture, and were
told not to read the usability skills.

| Case                | Sonnet                                        | Opus                |
| ------------------- | --------------------------------------------- | ------------------- |
| u1 sign-up form     | M4 fails: no user test recommended            | M4 fails: the same  |
| u2 thermostat panel | all pass                                      | all pass            |
| u3 quick check      | P2 fails: 460 words                           | P2 fails: 595 words |
| u4 walkthrough      | W1 and W4 fail: a severity list, no user test | all pass            |

## Evaluation With the Skill

The brief gave each run the skill's path and the same task. Two rounds ran. Between them, an independent review
found that several examples in the skill mirrored the planted problems. The examples were replaced with ones
from outside the fixtures, and the final round reran every case.

| Case                 | Outcomes that failed without the skill | Sonnet with the skill                       | Opus with the skill         |
| -------------------- | -------------------------------------- | ------------------------------------------- | --------------------------- |
| u1 sign-up form      | M4 (both)                              | all pass; recommends a five-user phone test | all pass; the same          |
| u2 thermostat panel  | none                                   | all pass                                    | all pass                    |
| u3 quick check       | P2 (both)                              | all pass; 315 words                         | all pass; 310 words         |
| u4 walkthrough       | W1, W4 (Sonnet)                        | all pass; action by action                  | all pass                    |
| u5 command-line tool | not run                                | all pass; loads `cli-ui-ux`                 | all pass; loads `cli-ui-ux` |

Three changes came from the runs themselves. A quick check first followed the full report shape and ran to 431
words, so it got its own short shape. A run on u5 chose a quick check from a guess that "our" tool had few users,
so depth now rests only on what the request or project states. A run read "about five per round" as five per
user group, so the recruitment rule now spells out the group sizes.

## Remaining Risks

- Quick checks land between 300 and 315 words, slightly over the skill's own target; the eval limit is 400.
- The `SCORE` pattern in `grade.py` would also flag a report that says "no overall score". No run did.
- The description has no trigger for "UX review" or "intuitive"; the 512-character budget left no room.
