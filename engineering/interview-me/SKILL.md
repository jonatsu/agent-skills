---
name: interview-me
description: Interview the user one question at a time until you both share an understanding of a plan, design, problem, requirement, or decision, recommending an answer to each question and closing with a written record of what was decided. Use when asked to grill, interview, pressure-test, or poke holes in something, or to make sure you understand it the same way before acting. Use idea-brainstorming to shape an idea that has no direction yet; not for reviewing existing code.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Interview Me

Interview me relentlessly about every aspect of the subject until we reach a shared understanding. The subject
can be a plan, a design, a problem, a requirement, a decision, or a concept. Walk down each branch of its
decision tree, resolving dependencies between decisions one by one. For each question, provide your recommended
answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple
questions at once is bewildering.

If a *fact* can be found by exploring the codebase or the material at hand, look it up rather than asking me.
The *decisions*, though, are mine: put each one to me and wait for my answer.

Act on the subject only after I confirm we have reached a shared understanding.

## Interview Something Real

The interview needs something with shape on the table: a plan, a design doc, a draft, a problem statement, or
even a rough idea with a discernible direction. A draft is a valid target: the interview sharpens it, and its
gaps and soft spots are exactly what the questions surface. An explicitly incomplete draft handed over from
`idea-brainstorming` is squarely in scope.

Before the first question, restate what is on the table in two or three sentences, including what is still open
in it, and confirm I recognize it. Name it as a draft if it is one, so we both know we are hardening it, not
ratifying it.

When there is no shape at all (no direction, no candidate approach, just a topic), that is `idea-brainstorming`:
say so and ask whether I want to shape the idea first.

Read what already exists before questioning: the subject itself, the code or system it touches, and any
specification, decision record, or document it must conform to. A question whose answer is already written
wastes a slot in the budget; a place where the subject contradicts a document it must honor is the sharpest
question you have. Bring each such contradiction to me as a question, naming the document and the conflict,
rather than assuming which side wins.

## When a Decision Turns on Its Words

If a decision hangs on what a term means (two words for one concept, or one word stretched over two), that is a
domain-model question. Engage the `domain-modeling` skill to settle the term and capture it, then carry the
settled term back into the interview.

## Map the Branches Before You Ask

Before the first question, enumerate the decision branches and order them: dependencies first (a choice that
constrains later ones), then by risk (the decisions hardest to reverse or most likely to be wrong). Show me this
map and the rough question count per branch; it is the shape of the session up front.

Question in that order. A decision that constrains three others is worth settling before any of them. When an
answer reshapes the tree, opening a branch or closing one, say so and re-show the map.

## Sharpen a Vague Answer Before Moving On

"It depends", "probably", "we'll see" and "maybe later" are the question restated. Ask the follow-up that forces
a concrete choice, or ask what it depends on and settle that first. A non-committal answer on a load-bearing
decision is itself worth questioning. Silence on a branch is not agreement: ask.

If I decline to decide, record the decision as deferred, together with what the deferral costs. A deferred
decision MUST never read as resolved.

## Recommend Without Anchoring

Give your recommendation, but on a load-bearing or hard-to-reverse decision state the strongest case *against*
it in the same breath: the condition under which the other choice wins. A recommendation with no live
alternative is an anchor, and an interview that anchors has tested nothing.

Where a decision is genuinely close, ask for my instinct before you show your pick, then react to it. Order
matters: your recommendation first shifts my answer; my answer first tests yours.

## Budget the Session

Plan for **10–15 questions**. The budget paces the session; it never defines when the subject is done. Spend
questions on sharp decisions rather than generic ones, and never leave a branch unresolved because the count ran
out.

Raise a budget overrun as soon as you see it: when the map already holds more branches than the budget covers,
or when a branch forks mid-interview. Then put the choice to me: keep going, split the subject across more
sessions, or narrow its scope. Truncating is my decision to take with its cost in view.

A branch can only close on settled upstream branches. When one rests on an assumption about an upstream branch
that is still open, reconcile the two, or mark both `open` together and say which downstream decisions now rest
on nothing settled.

## Stop When

- Every branch is resolved or explicitly deferred.
- I ask to stop.
- The remaining questions are blocked on something outside my control, such as an external dependency or a
  measurement nobody has taken. Blocked is not the same as undecided.

When stopping mid-branch, name the branch that is half-finished.

## Close With the Decision Record

Before acting on anything, write the decisions down: wherever this repository already keeps design notes, to a
file I name, or inline if there is nowhere obvious. One table:

```markdown
| Decision | Recommended | Chosen | Why | Status |
|---|---|---|---|---|
```

Status is `resolved`, `deferred`, or `open`. `open` is a branch we never reached or one whose upstream is
unsettled; `deferred` is one I reached and chose not to settle, and a deferred row MUST carry what the deferral
costs. Record only decisions I actually made. Follow the table with what changed about the subject as a result,
then stop for my confirmation.
