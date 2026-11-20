# Evaluation: Design Mode in `accessibility-engineering` and `usability-engineering`

Date: 2026-11-20. The question was whether the two skills work as design aids, so an interface is built right
from the start rather than repaired after review. Commits 67663ff and f6c7755 gave each skill a design trigger,
and the accessibility skill a seven-step Design mode. This round adds one design case to each skill and runs it.

## Verdict

`ready with risks`. With the skill, every outcome passed in all four runs. Without it, every outcome also passed
in all four runs. So the cases show that design mode works, but they do not show that the skill adds anything
Sonnet lacks for these two briefs. The risks are one model (Sonnet), one client (Claude Code), two repetitions
per cell, and cases that saturate.

## Cases

- **a6-design** (`ui-ux-skills/accessibility-engineering/evals/behavior.json`): a clinic booking widget brief
  with nine planted barriers. Four of them fall under criteria new in WCAG 2.2: dragging (2.5.7), target size
  (2.5.8), redundant entry (3.3.7), and accessible authentication (3.3.8).
- **u6-design** (`ui-ux-skills/usability-engineering/evals/behavior.json`): a thermostat vacation-mode brief
  with stakeholder demands that work against its users. These include firmware jargon, a confirmation on every
  change, a bare toggle, hurried older users and rental guests, and a wall panel that hides the mode.

`evals/grade.py` in each skill checks the scripted outcome, no score or percentage, and the rest are graded from
the design document.

## Runs

Each run was a fresh Sonnet subagent in its own workspace, holding only the brief. The skill arm read the
candidate `SKILL.md` first; the control arm was told to load none of the four UI skills.

| Case      | Arm     | Runs | Outcomes passed |
| --------- | ------- | ---- | --------------- |
| a6-design | skill   | 2    | 5 of 5 in each  |
| a6-design | control | 2    | 5 of 5 in each  |
| u6-design | skill   | 2    | 7 of 7 in each  |
| u6-design | control | 2    | 7 of 7 in each  |

## What Differed Between the Arms

The outcomes did not separate the arms, but the documents did:

- **Structure.** Skill-arm designs followed the skill's steps: the seven accessibility steps, and the usability
  design worked principle by principle. Control designs were
  organised by screen or flow. One usability control wrote an arc42-style architecture document.
- **Target size.** All four accessibility runs chose 44 by 44 pixels and named 24 by 24 as the AA minimum. No run
  mistook 44 for the AA requirement.
- **Success thresholds.** Both usability controls set test pass marks such as "nine in ten start it in under 30
  seconds" and labelled them as proposals. The skill arms named users, tasks, and what would confirm the design
  without inventing figures.

## Remaining Risks

- The briefs list their problems openly, so a capable model finds them without help. A case that separates the
  arms needs a barrier a model misses by default, such as a design request that never mentions accessibility.
- Only Sonnet ran, because every subagent ran on Sonnet while safeguard false positives persist. Smaller models,
  where a skill tends to add more, are untested.
- Run transcripts were not kept with the results.
