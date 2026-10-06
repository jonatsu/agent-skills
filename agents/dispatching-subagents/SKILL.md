---
name: dispatching-subagents
description: Orchestrate delegated work as independent subagent lanes and act on what each returns. Use before dispatching several subagents at once or one substantial task, when a subagent returns blocked, needing context, or with concerns, or when sending review findings back for a fix. Not for writing the brief (writing-prompts) or isolating checkouts (using-git-worktrees).
license: MIT
metadata:
  author: Joonas Onatsu
---

# Dispatching Subagents

Run delegated work as **lanes**: one subagent, one bounded task, one boundary no other lane crosses. You keep the
decisions, the reviews, and the integration; each lane gets work it can finish without them. Whether to delegate
at all, and at which tier, is settled before this skill starts. The brief each lane receives is `writing-prompts`'
job; load it before writing one.

## Split the Work

Fan out only work that is **independent**: each task can be understood without the others' context, and finishing
one cannot change another.

- **Related failures stay in one lane.** When fixing one might fix the others, parallel lanes each chase the same
  cause and collide on the fix.
- **Shared state runs in sequence.** Tasks that edit the same files or use the same resource run one lane after
  another, each starting from the last one's result.
- **Investigate before splitting.** When you do not yet know what is broken, one lane finds out first; split once
  the causes are known.
- **Batch same-shape edits.** Several small edits of one kind (the same fix, constant, or field across files) go to
  one lane as one list and come back as one diff. A task earns its own lane when it needs its own judgment, tests,
  or review.

Keep formatters, generators, and hooks you run from your own tree off the files a lane is editing, because they
rewrite the lane's work underneath it. The files each lane owns go in its brief, under `writing-prompts`'
ownership item.

The split is done when every lane has a boundary no other lane crosses and every task sits in exactly one lane.

## Run the Lanes

Default to one lane at a time. Run lanes in parallel only when they passed the independence test and each is
cheap; the harness configuration sets the ceiling, so stay under it rather than assuming a number. Send parallel
dispatches together in one turn so they run concurrently.

Own the only orchestration layer. A lane does its task itself and dispatches no subagents or reviewers of its
own; review comes from you, after it reports. While a lane runs, do other work, never the lane's own task.

Every lane reports with one of four statuses: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`. A
subagent whose definition already carries this contract needs nothing more. Any other gets the contract in its
brief: read [references/status-contract.md](references/status-contract.md) and paste it in verbatim.

## Act on the Return

- **DONE:** verify it (next section) before building on it.
- **DONE_WITH_CONCERNS:** read the concerns first. A doubt about correctness or scope is settled before review;
  an observation is noted and review proceeds.
- **NEEDS_CONTEXT:** supply what is missing and send the same lane back.
- **BLOCKED:** change something before re-dispatching: more context, a stronger tier, a smaller task, or your
  ruling on a plan defect. The same brief to the same tier fails the same way.

Treat every report as claims to check, not facts: a subagent's summary can be incomplete or optimistic.

## Review and Fix Rounds

When a reviewer lane judges another lane's work, hand it the task, the diff, and the report, and let it flag
anything. Keep "do not flag X" and pre-set severities out of its brief: a finding you think is wrong gets rejected
afterwards, with your reason, where the user can see it.

Send findings back to the lane that wrote the code, by their finding tags (`F1`, `F2`), while the harness can
resume it; its context still holds the task and its own choices. Then ask the reviewer for a scoped re-review:
each tagged finding addressed or not, plus new breakage in the fix diff only.

After two fix rounds that leave a finding open, stop repeating them. Reassess: a fresh lane on a stronger tier
with the findings and the prior report, a smaller task, or the work taken back.

## Verify the Combined Result

Before calling delegated work done:

1. Check that no two lanes edited the same code; overlapping edits are resolved by you, not by the last writer.
2. Run the repository's checks once over the combined result when any lane changed code.
3. Spot-check each report's claims against the diff or the sources it cites, because lanes make systematic
   errors a summary hides.

Done when the checks pass on the combined tree, where any lane changed code, and every claim you relied on has
been checked.
