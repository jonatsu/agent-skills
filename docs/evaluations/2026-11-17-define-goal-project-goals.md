# Evaluation: define-goal Project Goals Mode

Date: 2026-11-17. The evaluation covered `define-goal` after it gained a project goals mode beside its run goal mode
(`f97ebf3`). It ran the seven behaviour cases in `engineering/define-goal/evals/behavior.json` and a trigger test of
the new description.

## Verdict

The skill improves on the base model on both Sonnet and Opus, and the new description routes project-goal requests
to the skill without losing run-goal requests or catching near misses.

Round 1 scores count a pass as 1 and a partial as 0.5 per outcome:

| Case                                 | Sonnet without | Sonnet with | Opus without | Opus with |
| ------------------------------------ | -------------- | ----------- | ------------ | --------- |
| `new-project-elicitation`            | 0.70           | 1.00        | 0.70         | 0.90      |
| `retrofit-reconstruct`               | 0.80           | 1.00        | 0.80         | 1.00      |
| `confirmed-goals-wiring`             | 0.70           | 0.80        | 1.00         | 0.90      |
| `consolidate-duplicated-goals`       | 0.90           | 1.00        | 0.90         | 0.90      |
| `readme-placement-and-free-approach` | 0.80           | 1.00        | 0.80         | 1.00      |
| `run-goal-from-project-goals`        | 0.80           | 1.00        | 0.80         | 1.00      |
| `run-goal-from-activity`             | 0.88           | 1.00        | 0.75         | 1.00      |
| All cases                            | 0.79           | 0.97        | 0.82         | 0.96      |

The base model already elicits goals well, cites repository evidence, and asks when two copies of the goals
disagree. The skill adds the parts a project's goals need to steer later sessions: a line saying who decides a
change, one question per turn with a recommendation, a placement that follows the repository, a pointer from
`AGENTS.md`, and a run goal that stays a goal rather than turning into a plan file.

## Trigger Test

Fifteen held-out requests were written from the skill body by a separate agent: six asking for project goals, five
for run goals, and four near misses that belong to `idea-brainstorming`, `writing-specs`, `writing-readmes`, and
`implementation-planning`. Each ran three times as an Opus main session with skills enabled, once with the deployed
description and once with the new one:

| Requests           | Old description loads `define-goal` | New description loads `define-goal` |
| ------------------ | ----------------------------------- | ----------------------------------- |
| Project goals (18) | 0                                   | 17                                  |
| Run goals (15)     | 15                                  | 15                                  |
| Near misses (12)   | 0                                   | 0                                   |

Each near miss loaded its intended skill in all runs on both descriptions. The one miss was a request that never
says "goals": someone with no domain knowledge asking what a family medication app should and should not promise,
and how they would know it works.

## Fixes and Rechecks

Round 1 skill runs had two gaps on `confirmed-goals-wiring`. Runs added an agent rule the user had not confirmed to
the goals file ("an agent that finds work outside them stops and asks"), and one run placed the goals in `docs/`,
which the fixture's README reserves for runbooks.

The reference now tells the agent to write the confirmed wording as it stands. It places a dedicated goals file
beside the README when the documentation folders each hold a stated kind of document. It also gives the stop-and-ask
instruction one home, the `AGENTS.md` pointer line. Three recheck rounds ran on the affected cases:

- Placement is fixed: all 18 recheck runs on the wiring case put the goals file beside the README.
- Opus stopped adding the rule after the first fix (0 of 8 runs).
- Sonnet kept adding it to the goals file in 2 of 3, 3 of 3, and 3 of 4 runs across the three fixes. The added
  sentence restates the agreed who-decides line as agent behaviour, so it is harmless, and the wording was not
  iterated further.

The recheck of `new-project-elicitation` (three runs per model) had two partials: one Sonnet run listed three
further questions after its one open question, and one Opus run asked an architecture question (which backup engine
to use) as its main question. The reference now names the choice between technologies as work for the later
skills.

## Method

The method is that of `2026-11-17-pipeline-skills-round-2.md`: headless `claude -p` sessions with slash commands
disabled, one run per case, arm, and model in round 1, fixtures copied into an empty working directory, and blind
bundles of whole files graded by a Sonnet subagent. Round 1 was 28 runs; the rechecks were 12, 6, and 6 skill-arm
runs. Every skill-arm trace read the skill, and no control trace held its text. Rounds 1 to 3 were graded blind; the
last recheck was checked only by a text search of the written goals file for the added rule.

The trigger test temporarily replaced the deployed skill with the candidate and restored it afterwards, verified
byte-identical with `diff -r`.

## Limits

Each case is single-turn, so the evaluation does not show a whole interactive session from an empty repository to
wired goals. The fixtures are small, synthetic, and agent-written. The trigger test ran on Opus only, with fifteen
requests.

## Acceptance Test

The user's acceptance test takes one new project and one existing repository through the project goals mode, accepts
both results, and confirms that a fresh session in each cites its goals unprompted when choosing scope or method.

The retrofit passed on a personal NixOS configuration. The request loaded `define-goal`, and the user accepted goals
placed in the README by their choice: a purpose with an ordered conflict rule, a binary version 1.0 done-check, scope
in and out, and the user as sole decider, with the method left to the existing `AGENTS.md`. The pointer in `AGENTS.md`
carries the stop-and-ask instruction, and the goals hold no rule the user did not confirm. A fresh session asked "what
should I work on next" read the goals first and proposed tasks aligned with them. The new-project half is still
open.
