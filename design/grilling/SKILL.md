---
name: grilling
description: One-question-at-a-time grilling interview that stress-tests a proposed design before implementation. Walks each branch of the design tree, recommends an answer per question, forces vague answers to a decision, and closes with a written decision record. Use when the user explicitly asks to be grilled, or to pressure-test, poke holes in, interrogate, or challenge a plan - "grill me", "grill this plan", "pressure-test this", "poke holes in this", "challenge my design", "interrogate this before I build it". NOT for shaping an unformed idea, which is idea-forge, and NOT for reviewing code that already exists.
metadata:
  author: Joonas Onatsu
  license: MIT
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the codebase, look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Do not enact the plan until I confirm we have reached a shared understanding.

## Sharpen a vague answer before moving on

"It depends", "probably", "we'll see" and "maybe later" are not answers — they are the question restated. Ask the follow-up that forces a concrete choice, or ask what it depends on and settle that first. A non-committal answer on a load-bearing decision is itself worth grilling.

If I decline to decide, that is fine — but MUST record it as deferred, carrying what the deferral costs. NEVER let a deferred decision read as resolved.

## Budget the session

Plan for **10–15 questions**, and tell me the shape up front: roughly how many branches, roughly how many questions. Depth beats coverage — a few sharp questions on the decisions that carry risk resolve more than a long checklist of generic ones.

Going past the budget needs my agreement. When you are near it, say so and ask whether to keep going or close out. NEVER overrun silently.

## Stop when

- Every branch is resolved or explicitly deferred.
- I ask to stop.
- The remaining questions are blocked on something outside my control — an external dependency, or a measurement nobody has taken. Blocked is not the same as undecided.

NEVER stop mid-branch without naming which branch is half-finished.

## Close with the decision record

Before enacting anything, write the decisions down — wherever this repository already keeps design notes, to a file I name, or inline if there is nowhere obvious. One table:

```markdown
| Decision | Recommended | Chosen | Why | Status |
|---|---|---|---|---|
```

Status is `resolved`, `deferred` or `open`; a deferred row MUST carry what the deferral costs. Follow the table with what changed about the plan as a result, then stop for my confirmation.

## Anti-patterns

- Leading the witness: presenting your recommendation as the only viable answer. Recommend, then genuinely wait — a grilling that ratifies your own proposal has tested nothing.
- Reading silence on a branch as agreement.
- Recording a decision I never actually made.
- Enacting any part of the plan mid-interview.
