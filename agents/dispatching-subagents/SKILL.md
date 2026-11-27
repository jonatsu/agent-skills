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
dispatches together in one turn so they run concurrently. For research, send a second wave of lanes rather
than a wider first one.

When the user asks for speed on several independent plan units, batch builders in parallel even when they are
not cheap, within the harness ceiling. Keep the shared files yourself, such as registries, settings, and
migration tables, and wire in the snippets each builder returns. Brief each builder to point every install path
at a temporary target, because a probe install can write the real home directory. One scoped review and one live
check cover the batch, and each unit keeps its own commit. The batch is done when its live check passes, because
green suites have missed defects that only the live check found.

Before fanning out lanes that build, estimate each lane's build output against free disk. A fresh checkout or
worktree rebuilds every dependency, and a Rust `target/` directory alone can reach gigabytes, so parallel
builders multiply it. Point them at the toolchain's shared cache where one exists. When the total still does not
fit, cap the number of parallel builders, even when the user asked for speed.

Own the only orchestration layer. A lane does its task itself and dispatches no subagents or reviewers of its
own; review comes from you, after it reports. While a lane runs, do other work, never the lane's own task.

Every lane reports with one of four statuses: done, done with concerns, needs context, or blocked. A
subagent whose definition already carries this contract needs nothing more. Any other gets the contract in its
brief: read [references/status-contract.md](references/status-contract.md) and paste it in verbatim.

## Act on the Return

- **Done:** verify it (next section) before building on it.
- **Done with concerns:** read the concerns first. A doubt about correctness or scope is settled before review;
  an observation is noted and review proceeds.
- **Needs context:** supply what is missing and send the same lane back.
- **Blocked:** change something before re-dispatching: more context, a stronger tier, a smaller task, or your
  ruling on a plan defect. The same brief to the same tier fails the same way.

Treat every report as claims to check, not facts: a subagent's summary can be incomplete or optimistic. Tell the
user what a lane did and what remains, in plain words, not its status.

## Review and Fix Rounds

When a reviewer lane judges another lane's work, hand it the task, the diff, and the report, and let it flag
anything. Keep "do not flag X" and pre-set severities out of its brief: a finding you think is wrong gets rejected
afterwards, with your reason, where the user can see it.

Send findings back to the lane that wrote the code, by their finding tags (`F1`, `F2`), while the harness can resume it;
its context still holds the task and its own choices. When you merge reports from parallel lanes, qualify each tag by
its lane, such as `code-reviewer F2`, because every review numbers its findings from `F1`. Then ask the reviewer for a
scoped re-review: each tagged finding addressed or not, plus new breakage in the fix diff only.

After two fix rounds that leave a finding open, stop repeating them. Reassess: a fresh lane on a stronger tier
with the findings and the prior report, a smaller task, or the work taken back.

## Verify the Combined Result

Before calling delegated work done:

1. Check that no two lanes edited the same code; overlapping edits are resolved by you, not by the last writer.
2. Run the repository's checks once over the combined result when any lane changed code.
3. Spot-check each report's claims against the diff or the sources it cites, because lanes make systematic
   errors a summary hides.
4. Move every result a lane left in its working folder into the durable file its brief named. You own what the
   lanes leave behind, and nobody else will move it.
5. Check that each lane left only its result: its worktree, build output, and scratch files are gone, apart
   from what its brief kept for inspection. Remove what remains before reporting the work done.

Done when the checks pass on the combined tree, where any lane changed code, every claim you relied on has been
checked, every result sits in its durable file, and no lane's leftovers remain.
