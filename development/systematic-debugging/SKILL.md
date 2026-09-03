---
name: systematic-debugging
description: Debug non-obvious failures, regressions, and flaky tests through evidence and root-cause fixes.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Systematic Debugging

Investigate the failure before proposing a code change. The goal is convergent reasoning: collect evidence,
test a focused explanation, and fix the cause rather than suppressing the symptom.

## Workflow

1. **Capture the failure.** State the expected and actual behavior. Read the complete error, stack trace, log,
   and recent changes. Make a minimal reproduction when feasible.
2. **Handle unavailable reproduction honestly.** Gather bounded evidence such as exact inputs, versions,
   environment, logs, and frequency. Do not claim a root cause. An explicitly authorized mitigation may proceed
   when it is labeled as a mitigation, its risk is understood, and its result is verified.
3. **Map the failure path.** For a deep stack trace or invalid value, trace callers and values backward to the
   original trigger. In a multi-component system, instrument boundaries to inspect input, output, state, and
   configuration. Redact secrets. For flaky asynchronous work, wait for the observable completion condition
   instead of tuning arbitrary delays.
4. **Test a focused hypothesis.** Predict what a small experiment will show, change one behavioral variable,
   and read the result. Keep investigation notes in the response or task record; do not create repository files
   unless the user asks. After several refuted hypotheses, recheck the reproduction and assumptions, widen the
   search, or consider whether the architecture needs discussion.
5. **Fix and verify.** When the causal chain is supported, state it and make the smallest cause-level change.
   Run the reproduction and relevant regression checks, read their output, and report any remaining uncertainty.

## Guardrails

- Do not stack speculative fixes or refactors on an untested explanation.
- Do not treat a green command, a suppressed error, or a workaround as evidence that the cause is fixed.
- Preserve existing authorization. A mitigation, destructive experiment, or risky architectural change needs the
  authority appropriate to that action.
- Use independent test review when the task, risk, or user requests it. `test-engineer` owns test work and does
  not own production changes.

## Completion

- The failure is reproduced and resolved, or the limits of reproduction are stated clearly.
- The cause is explained when known; otherwise the report distinguishes evidence, hypothesis, and mitigation.
- The implemented change is scoped to the supported cause.
- Relevant verification ran, its output was read, and remaining risk is reported.
