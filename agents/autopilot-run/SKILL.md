---
name: autopilot-run
description: Run an agreed task list unattended, from the handover before the user leaves to the report when they return, without stalling on permission prompts or questions nobody can answer. Use when the user says to keep going without them, work through a list overnight or while they are away, or run on autopilot, and when such a run resumes after compaction. Not for writing a goal condition alone (define-goal) or planning the list (implementation-planning).
license: MIT
metadata:
  author: Joonas Onatsu
---

# Autopilot Run

An autopilot run works through a task list the user agreed, while nobody watches. The user's absence changes
three things. A permission prompt or a question dialog waits forever, so the run must never raise one. A decision
the user would normally make must be found in the documents, made reversibly, or parked. The run must end on its
own, at a point the user can read in one pass when they return.

The run starts when the user tells you to keep going without them. The list may arrive now, sit in a file they
name, or be one settled earlier in the conversation. The list is the settled design, and each item is a
confirmed draft. Build each item without drafting it first.

## Hand Over Before the User Leaves

Work through these steps while the user can still answer. Each one removes a stall the run cannot recover from
alone.

1. **Fix the ledger.** Name the file that holds the list. Name the ledger for progress, judgement calls, and
   parked questions: the plan, the TODO file, or the session checkpoint. Create the ledger entry when none
   exists. At its top, write the run rules from [During the Run](#during-the-run) as five short lines. Some
   harnesses drop a loaded skill at compaction, and the ledger is what the run re-reads.

2. **Write the goal condition.** Tie it to the ledger, and give it three parts:

   - the end state: every item shows a landed commit or a parked question in the ledger;
   - the closing evidence: a command whose output proves the end state, run after the last commit. For example,
     `git status --short` prints nothing and the test command exits 0;
   - the stop clause: the goal also counts as met when every remaining item waits on a blocker only the user can
     remove. Record each such blocker in the ledger. End the run at such a stop; do not continue or retry.

   Add the boundaries the run keeps, such as no push, no deploy, and no real credentials. Pair them with the
   instruction "park those steps and continue". Without the stop clause, a judge keeps rejecting a run that can
   only wait, and the agent repeats a status line for hours. The `define-goal` skill covers condition writing in
   depth.

3. **Preflight the commands.** List the commands the run will need: tests, builds, commits, and anything a
   subagent will run. Run each one once now, in the exact shape the run will use, and watch for a prompt. When
   one prompts, rewrite it into a shape that does not, or ask the user to allow it. Confirm that anything the run
   needs unlocked lasts until morning, such as a commit-signing agent or an MCP server login.

4. **Name the harness settings.** Some settings make a stall end on its own. Name the ones that apply from
   [references/harnesses.md](references/harnesses.md), such as a question-tool timeout or allow rules for the
   run's commands. Changing them is the user's decision, so leave them unchanged.

5. **Arm the loop.** Identify the harness from your tool list and system prompt, then read its section of
   [references/harnesses.md](references/harnesses.md). Hand the user the exact command that arms the goal loop
   on the condition. Where the harness allows it, set the goal yourself instead.

The handover is done when all of these hold:

- the ledger holds the list and the run rules;
- the condition has all three parts;
- every preflight command ran without a prompt, or the user knows which one will prompt;
- the user knows which harness settings apply;
- the user has the arming command.

## During the Run

These are the run rules. Copy them into the ledger in step 1.

- **Answer from the documents.** Look for the answer to a question in the task document, the files it names,
  its plan, and the ledgers. A question they settle is answered.
- **Make reversible calls yourself.** Record each judgement call in the ledger with its reason and how to undo
  it.
- **Park what only the user can answer.** Write the question in the ledger with the options and your
  recommendation. Then take the next item that does not depend on it. Park the question instead of opening a
  question dialog, because nobody will answer it.
- **Run every command standalone.** Give each command its own call, starting in the working directory. Use no
  `cd <dir> &&` prefix and no `git -C`. Add no pipe or chain after a push or commit. When a guard denies a command,
  rewrite it into the shape the denial names instead of repeating it.
- **Write back at each slice.** Commit the ledger update with each landed item. Keep working past a progress
  report, which does not end a turn.

Brief every subagent with:

- the success criteria its lane owns;
- the standalone-command rule;
- an instruction to return a blocker in its result rather than wait on it.

No harness passes the goal to a subagent, and a prompt in a subagent lane stalls the whole run.

A compaction, a resume, or any sign that earlier context is gone is a trigger. Before the next action, re-read the
ledger and its run rules. Where the harness has a goal read-back tool, call it too.

Run the closing checks after the last change, so their passing output is the latest evidence in the transcript.
A check that passed before a later edit proves nothing.

## End the Run

The run ends when every item has landed or waits on a parked question. It also ends before a step that is
irreversible, reaches beyond this machine, or leaves the list's scope. Park that step instead of taking it.

To end, run the closing evidence after the last commit, then mark the goal met the way the harness expects. The
stop clause makes a run whose remaining items are all parked count as met, so the normal completion path applies
in every harness. Then end the turn with a report the returning user can act on:

- each landed item with its commit;
- each parked question, with its options and your recommendation;
- each judgement call, with how to undo it;
- each blocker, with what the user must do to remove it.
