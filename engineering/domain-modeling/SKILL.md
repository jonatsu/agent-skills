---
name: domain-modeling
description: Actively build and sharpen a project's domain model and ubiquitous language while designing - challenge conflicting or vague terms, stress-test relationships with concrete scenarios, cross-check claims against code, and capture resolved vocabulary in a living glossary. Use when defining or editing project terminology, a glossary, or bounded-context boundaries. NOT for reviewing an existing model (brooks skills), system architecture (technical-design), or product scope (requirements-specification).
license: MIT
metadata:
  author: Joonas Onatsu
---

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging
terms, inventing edge-case scenarios, and writing the glossary and its decisions down the moment they crystallize.
Merely *reading* a glossary for vocabulary is not this skill — that is a one-line habit any work can do. This
skill is for when you are *changing* the model, not just consuming it.

## Use this when — and when not

Reach for this while a design is being shaped and the words for it are still moving: a term means two things, two
words mean one thing, or a stated relationship has never been tested against a concrete case. It is the active
counterpart to `grilling`: when a grilling interview surfaces terminology or model decisions, engage this skill
to capture them; when this skill's questioning widens into a full design interrogation, hand back to `grilling`.

Not this skill: reviewing an existing model for decay (the `brooks-*` skills), designing system structure,
interfaces, or data flow (`technical-design`), or fixing product scope and acceptance (`requirements-specification`).

## During the session

- **Challenge against the glossary.** When a term conflicts with the language already recorded, call it out at
  once: "The glossary defines *cancellation* as X, but you mean Y — which is it?"
- **Sharpen fuzzy language.** When a term is vague or overloaded, propose a precise canonical word and force the
  choice: "You said *account* — the Customer or the User? Those are different things."
- **Stress-test with concrete scenarios.** When a relationship is asserted, invent a specific edge case that
  probes the boundary between concepts and forces a precise answer, rather than accepting the general statement.
- **Cross-check against the code.** When behavior is claimed, check whether the code agrees. Surface a
  contradiction as a question: "The code cancels whole Orders, but you said partial cancellation exists — which
  is right?"
- **Capture inline, never batched.** The instant a term resolves, write it to the glossary. A decision captured
  later is a decision remembered wrong.

## The glossary is vocabulary only

The glossary defines what a term *is*, in a sentence or two, and names the words to avoid for it. It is not a
spec, a scratchpad, or a home for implementation decisions — those are code, a design doc, or a decision record.
A term earns a place only when it is specific to this project's domain; general programming concepts do not
belong even when the project uses them constantly. The entry shape is in
[references/glossary-format.md](references/glossary-format.md).

## Where the glossary lives

Find the existing convention before creating anything: a glossary file already in the repository, a terms
section in the documentation set, or a location the contributor guide names. Two or more entries establish a
convention — continue it exactly. Where none exists, create a single glossary file where the documentation set
would look first, and create it **lazily**, only when the first term resolves.

When a codebase holds more than one bounded context — distinct areas where the same word legitimately means
different things — keep a glossary per context and one map of how they relate, rather than forcing a single
glossary to carry conflicting definitions. The multi-context layout is in
[references/glossary-format.md](references/glossary-format.md).

## Recording a decision

When the modeling produces a genuine decision — a boundary, an integration pattern between contexts, a
deliberate deviation — record it as a decision record rather than burying it in the glossary. Use the
`writing-documentation` skill, which owns the record: it gates records on a three-part test (hard to reverse AND
surprising without context AND the outcome of a real trade-off) and tiers their weight from a light note to a
full record. Do not restate that gate here or invent a second template.
