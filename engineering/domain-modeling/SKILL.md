---
name: domain-modeling
description: Build and sharpen a project's domain model and ubiquitous language while designing, and keep its glossary current. Use when a term is ambiguous or overloaded, when defining or editing project terminology or a glossary, or when drawing bounded-context boundaries. Not for reviewing an existing model (brooks skills), system architecture (technical-design), or product scope (requirements-specification).
license: MIT
metadata:
  author: Joonas Onatsu
---

# Domain Modeling

Build and sharpen the project's domain model while a design is being shaped and its words are still moving: a
term means two things, two words mean one thing, or a stated relationship has never been tested against a
concrete case. This skill changes the model; consulting the glossary for vocabulary is ordinary reading and needs
no skill.

It is the active counterpart to `interview-me`: when an interview surfaces terminology or model decisions, use
this skill to capture them; when this skill's questioning widens into a full design interrogation, hand back to
`interview-me`. Reviewing an existing model for decay is the `brooks-*` skills, system structure is
`technical-design`, and product scope is `requirements-specification`.

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
- **Capture each term the moment it resolves.** A decision captured later is a decision remembered wrong.

Done when every term whose meaning moved in the session has its glossary entry, and every conflict still open is
listed back to the user as a question.

## The glossary is vocabulary only

The glossary defines what a term *is*, in a sentence or two, and names the words to avoid for it. It is not a
spec, a scratchpad, or a home for implementation decisions — those are code, a design doc, or a decision record.
A term earns a place only when it is specific to this project's domain; general programming concepts do not
belong even when the project uses them constantly. Write each definition for a newcomer to the domain. The entry
shape and its rules are in [references/glossary-format.md](references/glossary-format.md).

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

When the modeling produces a genuine decision (a boundary, an integration pattern between contexts, a deliberate
deviation), record it as a decision record, not in the glossary. `writing-documentation` owns the gate for writing
one and its forms.
