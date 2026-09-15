---
name: grilling
description: One-question-at-a-time grilling interview that stress-tests a proposed design before implementation. Walks each branch of the design tree, recommends an answer per question, forces vague answers to a decision, and closes with a written decision record. Use when the user explicitly asks to be grilled, or to pressure-test, poke holes in, interrogate, or challenge a plan - "grill me", "grill this plan", "pressure-test this", "poke holes in this", "challenge my design", "interrogate this before I build it". NOT for shaping an unformed idea, which is brainstorming, and NOT for reviewing code that already exists.
license: MIT
metadata:
  author: Joonas Onatsu
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down
each branch of the design tree, resolving dependencies between decisions one-by-one. For each question,
provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple
questions at once is bewildering.

If a *fact* can be found by exploring the codebase, look it up rather than asking me. The *decisions*, though,
are mine — put each one to me and wait for my answer.

Do not enact the plan until I confirm we have reached a shared understanding.

## Grill something real

Grilling needs something with shape on the table — a plan, a design doc, a draft, or even a rough idea with a
discernible direction. A draft is a valid target: grilling sharpens it, and its gaps and soft spots are exactly
what the questions surface. An explicitly incomplete design handed over from brainstorming is squarely in scope.

Before the first question, restate what is on the table in two or three sentences — including what is still open
in it — and confirm I recognize it. Name it as a draft if it is one, so we both know we are hardening it, not
ratifying it.

Bounce out only when there is no shape to grill at all: no direction, no candidate approach, just a topic. That
is brainstorming, not this — say so and ask whether I want to shape the idea first.

Read what exists and the code it touches before questioning. A question whose answer is already written wastes a
slot in the budget.

## Map the branches before you ask

Before the first question, enumerate the decision branches the design contains and order them: dependencies
first — a choice that constrains later ones — then by risk, the decisions hardest to reverse or most likely to
be wrong. Show me this map and the rough question count per branch. That map is the "shape up front" the budget
promises.

Question in that order. A decision that constrains three others is worth settling before any of them. When an
answer reshapes the tree — opening a branch or closing one — say so and re-show the map rather than pressing on
against a stale one.

If the map already holds more branches than the budget can cover, say so before the first question — do not
start and hope to fit. Recommend a budget that matches the tree, or a split into sessions, and let me choose.

## Sharpen a vague answer before moving on

"It depends", "probably", "we'll see" and "maybe later" are not answers — they are the question restated. Ask
the follow-up that forces a concrete choice, or ask what it depends on and settle that first. A non-committal
answer on a load-bearing decision is itself worth grilling.

If I decline to decide, that is fine — but MUST record it as deferred, carrying what the deferral costs. NEVER
let a deferred decision read as resolved.

## Recommend without anchoring

Give your recommendation, but on a load-bearing or hard-to-reverse decision state the strongest case *against*
it in the same breath — the condition under which the other choice wins. A recommendation with no live
alternative is an anchor, and an interview that anchors has tested nothing.

Where a decision is genuinely close, ask for my instinct before you show your pick, then react to it. Order
matters: your recommendation first shifts my answer; my answer first tests yours.

## Budget the session

Plan for **10–15 questions**. The branch map from the previous section is the shape up front; the budget paces
walking it, it does not replace it.

The budget paces the session; it never defines when the design is done. Depth beats coverage means spending
questions on sharp decisions rather than padding with generic ones — it never means leaving a branch unresolved
because the count ran out.

Going past the budget needs my agreement. When you near the budget with branches still open, stop and put the
choice to me: keep going, split the design across more sessions, or narrow its scope. Truncating is my decision
to take with its cost in view, never yours to reach by running out. A design tree larger than one budget is a
signal to re-scope or continue, not to ship half-walked. NEVER overrun silently.

If mid-interview you see the design is larger than budgeted — a branch forks, or a decision opens a subtree —
raise it as soon as you spot it, not when the count runs out. Spotting the overrun early and asking to extend is
expected, not an interruption.

NEVER close with a branch resolved on an assumption about an upstream branch that is still open — that is how a
session ends self-contradictory. Reconcile the two, or mark both `open` together and say what downstream
decisions now rest on nothing settled.

## Stop when

- Every branch is resolved or explicitly deferred.
- I ask to stop.
- The remaining questions are blocked on something outside my control — an external dependency, or a
  measurement nobody has taken. Blocked is not the same as undecided.

NEVER stop mid-branch without naming which branch is half-finished.

## Close with the decision record

Before enacting anything, write the decisions down — wherever this repository already keeps design notes, to a
file I name, or inline if there is nowhere obvious. One table:

```markdown
| Decision | Recommended | Chosen | Why | Status |
|---|---|---|---|---|
```

Status is `resolved`, `deferred`, or `open`. `open` is a branch we never reached or one whose upstream is
unsettled; `deferred` is one I reached and chose not to settle, and a deferred row MUST carry what the deferral
costs. Follow the table with what changed about the plan as a result, then stop for my confirmation.

## Anti-patterns

- Leading the witness: a recommendation with no live alternative. See "Recommend without anchoring".
- Reading silence on a branch as agreement.
- Recording a decision I never actually made.
- Enacting any part of the plan mid-interview.
