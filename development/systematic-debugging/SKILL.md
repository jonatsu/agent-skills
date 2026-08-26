---
name: systematic-debugging
description: "Disciplined, convergent debugging method for deep-dive bug hunts — stops the agent from wandering, guessing, and shotgun-editing. Use when debugging a failure whose cause is not obvious: 'debug this', 'why is this failing', 'why does this crash', 'track down the bug', 'find the root cause', 'it worked before', 'flaky test', 'intermittent', 'heisenbug', 'race condition', 'not sure why', a stack trace, exception, or regression to investigate. Actions: debug, diagnose, reproduce, isolate, bisect, root-cause, investigate a failure. NOT for obvious one-line typo fixes with a known cause."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Systematic Debugging

IRON LAW: NO FIX WITHOUT (1) A RELIABLE REPRODUCTION AND (2) A ROOT CAUSE YOU CAN EXPLAIN OUT LOUD. If you cannot reproduce the failure, or cannot explain why your change fixes it, you are still debugging — editing code is forbidden.

Purpose: this skill exists to prevent **wandering** — poking at code, changing several things at once, acting on hunches, and declaring victory on a green run you never read. Debugging is the scientific method, not trial and error.

## Workflow

```text
Systematic Debugging Progress:

- [ ] Step 1: Reproduce ⛔ BLOCKING — reliable repro before ANY code change
- [ ] Step 2: Observe — read the actual error/stack/logs/state; expected vs actual
- [ ] Step 3: Hypothesize — ONE falsifiable hypothesis + prediction, logged
- [ ] Step 4: Test the hypothesis — one variable, confirm/refute, log result
- [ ] Step 4a: Reassess ⛔ CHECKPOINT after 3 refuted hypotheses
- [ ] Step 5: Confirm root cause ⚠️ REQUIRED — full causal chain explained
- [ ] Step 6: Confirm fix scope ⚠️ REQUIRED — minimal change at the cause
- [ ] Step 7: Verify — repro now passes; regressions run; no new breakage
```

## Step 1: Reproduce ⛔ BLOCKING

Get a reliable, ideally minimal, reproduction — a command, test, or input that triggers the failure on demand. If it is intermittent, find what makes it deterministic (seed, ordering, concurrency, environment).

If you CANNOT reproduce it, that is the first problem to solve — gather more data (logs, env, versions, exact inputs). MUST NOT attempt a fix against a bug you cannot trigger.

## Step 2: Observe

Read the evidence before theorising. Ask:
- What does the error message / stack trace / log actually say? (Read it fully, top frame to root.)
- What is the precise expected behaviour vs. the actual behaviour?
- What changed? (recent diffs, deploys, data, dependency bumps — `git log -S`, bisect)

Collect facts, not guesses. NEVER act on "I think it might be…" as if it were established.

## Step 3: Hypothesize

Form exactly ONE falsifiable hypothesis with a concrete prediction: "If the cause is X, then doing Y will produce Z." Write it to a hypothesis log:

```text
# | observation | hypothesis | prediction | test | result
```

One hypothesis at a time. No parallel guessing.

## Step 4: Test the hypothesis

Run the smallest experiment that confirms or refutes the prediction. Change **one variable**. Prefer instrumentation (logging, asserts, a probe) over behavioural edits while investigating. Revert any experimental change before the next one. Record the result in the log, then loop to Step 3.

### Step 4a: Reassess ⛔ CHECKPOINT

After 3 refuted hypotheses, STOP. Do not keep poking. Question the foundations:
- Is the reproduction actually exercising the failure?
- Is an assumption in Step 2 wrong?
- Is the fault in a layer you have not looked at (data, config, dependency, environment, the test itself)?
- Widen the search or bisect harder before forming new hypotheses.

## Step 5: Confirm root cause ⚠️ REQUIRED

State the root cause in one sentence and explain the full causal chain from cause to observed symptom. If there is a gap you cannot explain, you have not found it — return to Step 3.

## Step 6: Confirm fix scope ⚠️ REQUIRED

Before editing, state: the root cause, the minimal change that addresses it, and why it works. MUST fix the cause, not the symptom. NO speculative refactors, NO "while I'm here" changes, NO shotgun edits. For a large or risky change, ask the user first.

## Step 7: Verify

- The reproduction from Step 1 now passes.
- Related/regression tests run and pass — read the output, don't trust the colour.
- No new failures introduced.
- Per the global rule, hand material fixes to the `test-engineer` lane for adversarial verification.

## Red Flags — return to the named step if any appear

- Editing code before a reproduction exists → Step 1
- "Let me just try changing X and see" → Step 3 (no hypothesis)
- Two or more changes in flight at once → Step 4 (one variable)
- Added logging but never read it → Step 4
- Fix works but you cannot explain why → Step 5 (not root cause)
- 3+ tries with no convergence → Step 4a (reassess, don't grind)

## Anti-Patterns

- Shotgun debugging: changing many things hoping one works.
- Symptom-patching: silencing the error instead of fixing the cause.
- Treating a hunch as a finding without a test that confirms it.
- Declaring done on a green run you did not read.
- Refactoring or reformatting unrelated code mid-hunt.
- Removing the instrumentation/repro before verifying the fix.

## Pre-Delivery Checklist

- [ ] A reproduction existed before the fix and now passes.
- [ ] Root cause stated in one sentence; causal chain explained end to end.
- [ ] The change is minimal and targets the cause, not the symptom.
- [ ] No unrelated edits, refactors, or reformatting included.
- [ ] Regression/related tests run and read; no new failures.
- [ ] For hard cases, the hypothesis log shows the path taken.
