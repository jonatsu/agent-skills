# Writing individual requirements

Corpus-level rules live in `SKILL.md` and `references/contract.md`. This file is about the text of a single
requirement.

- [Before the requirements exist](#before-the-requirements-exist)
- [The atomic schema](#the-atomic-schema)
- [Identifiers](#identifiers)
- [One requirement per statement](#one-requirement-per-statement)
- [The vague-wording gate](#the-vague-wording-gate)
- [Acceptance criteria](#acceptance-criteria)
- [What does not belong in the document](#what-does-not-belong-in-the-document)

## Before the requirements exist

The schema below assumes you already know what the requirement is. Often what you have is one sentence from a
person. This section is how to get from one to the other. It is not a workflow and it does not replace
`idea-forge`, which shapes an unformed idea, or `grilling`, which pressure-tests a written plan.

### First, decide whether to ask at all

Elicitation is wasted motion on a request that is already concrete, and an agent primed to clarify will
clarify something that needed none — at which point the questions read as obstruction. **Skip it** when the
ask already carries any of these:

- A file path, a line number, or a named existing function or class.
- A code snippet.
- A bug with reproduction steps.
- An acceptance condition already stated.

### Four dimensions a vague ask is missing

Work these rather than asking whatever comes to mind. A genuinely vague ask is usually missing three of the
four, and naming which one a question serves stops the interrogation wandering.

| Dimension      | What is missing                                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------------------------------- |
| Functional     | What it does, for whom, and where the behaviour stops                                                               |
| Technical      | Where it runs, what it integrates with, what it may not change                                                      |
| Implementation | What already exists, what must be built, the constraints on building it, and what it does when something goes wrong |
| Business       | Why now, what it is worth, and what happens if it is never done                                                     |

**Ask the implementation dimension for the off-nominal case explicitly, because nobody volunteers it.** A
requester describes the path where the input is valid, the dependency answers and the operator is present.
Invalid and boundary input, the failure of each dependency named, and behaviour while degraded are
requirements too, and left unasked they get supplied by whoever writes the code. Hardware and system-level
work has the same gap in a different vocabulary — `references/domains.md` states it as operational states and
modes across standby, active, fault and degraded operation.

### Anchor every question with an example

A question offering no example gets an answer in whatever shape the reader guesses. Ask "email and password,
social login, magic link, or SSO?" rather than "what kind of authentication?". The example set narrows the
answer and exposes what you assumed while writing the question.

Ask in rounds of two or three. A dozen questions at once gets one of them answered.

### Do not gate on a completeness score

A pattern in circulation scores the requirement out of 100 and refuses to proceed below 90. **Do not adopt
it.** The agent assigning the score is the agent choosing the questions, so it converges by declaring itself
finished — a stopping condition nothing can check is theatre with a number on it.

The honest stopping condition is that every requirement has an Acceptance field someone who did not write it
could evaluate. That is checkable by reading.

## The atomic schema

Every requirement carries these. Fields with nothing to say are omitted, not filled — the same rule as
sections.

| Field        | Required        | What it holds                                                    |
| ------------ | --------------- | ---------------------------------------------------------------- |
| ID           | yes             | Stable identifier, never reused (see below)                      |
| Statement    | yes             | One testable obligation, one sentence, RFC 2119 keyword          |
| Rationale    | yes             | Why this exists. The field that stops a later reader deleting it |
| Acceptance   | yes             | How someone who did not write it decides whether it is met       |
| Priority     | yes             | `must` / `should` / `may`, matching the statement's keyword      |
| Verification | yes             | How it is confirmed — the method vocabulary is domain-specific   |
| Source       | when it has one | Who or what imposed it — a standard, a customer, a regulation    |
| Depends on   | when it has any | Other requirement IDs this one presumes                          |
| Notes        | rarely          | Anything that is genuinely not one of the above                  |

Rendered:

```markdown
#### FR-AUTH-003 — Session expiry

**Statement.** The service MUST invalidate an idle session after 30 minutes without a request.
**Rationale.** Shared workstations are in scope, and an abandoned session is the named attack path.
**Acceptance.** A session with no request for 31 minutes returns 401 on its next request.
**Priority.** must
**Verification.** Test.
**Source.** Security review 2026-08-14.
**Depends on.** FR-AUTH-001.
```

**Rationale is not optional and is the field most often dropped.** A requirement with no rationale is a
requirement nobody can safely remove, so it survives forever and the document grows monotonically.

**Verification** takes one method. For software that is usually a named test. For hardware and system-level
requirements the vocabulary is Inspection, Analysis, Demonstration and Test, with variants — load
`references/domains.md` for the definitions and for which set a project has declared.

## Identifiers

Format `<CLASS>-<AREA>-<NNN>`, three digits, zero-padded.

| Class | Covers                                                   |
| ----- | -------------------------------------------------------- |
| `FR`  | Functional — what it does                                |
| `NFR` | Non-functional — how well it does it                     |
| `IF`  | Interface — what it exchanges, and with what             |
| `CON` | Constraint — what it may not do, or must be built within |

`AREA` is short, uppercase, and stable: `AUTH`, `PWR`, `THERM`, `CAN`.

**Identifiers are permanent.** Never renumber to close a gap, and never reuse the ID of a deleted requirement
— downstream test plans, tickets and hardware drawings cite them. A retired requirement either stays in place
marked as withdrawn, or leaves via an amendment that records its ID.

The rule is not specific to requirements and `SKILL.md` now states the general case: **any** numbered entry,
in any document type, keeps its number forever. What this section adds is the format and the class vocabulary
below.

## One requirement per statement

Split on every "and", "or", and comma that joins two obligations. Two obligations in one statement cannot be
independently verified, independently prioritised, or independently withdrawn.

Wrong:

> The system MUST log all authentication attempts and alert an operator on three consecutive failures.

Right: two requirements, the second depending on the first.

## The vague-wording gate

These words describe a feeling, not an obligation. Every one of them MUST be replaced with a number, a unit,
and a condition before the requirement is complete.

| Word                                    | Replace with                                                          |
| --------------------------------------- | --------------------------------------------------------------------- |
| fast, quick, responsive                 | A latency figure, at a percentile, under a stated load                |
| robust, reliable, stable                | A failure rate or MTBF, over a stated interval and environment        |
| efficient                               | A consumption figure — watts, bytes, cycles — under a stated workload |
| scalable                                | The dimension, the range, and what may degrade across it              |
| secure                                  | The specific property, the threat, and the control                    |
| user-friendly, intuitive, seamless      | A task-completion measure, or delete the requirement                  |
| flexible, configurable                  | The exact set of things that may vary, and their ranges               |
| appropriate, adequate, sufficient       | The threshold and who set it                                          |
| minimise, maximise, optimise            | The target value and the acceptable band                              |
| as needed, if possible, where practical | Delete. This is not a requirement                                     |

Two more failure shapes worth naming:

- **A requirement with no subject.** "Errors are logged" does not say by what. Name the actor.
- **A design decision wearing a requirement's clothes.** "The system MUST use PostgreSQL" is a constraint if a
  stakeholder imposed it, and a design decision if the team chose it. Constraints get a `CON` ID and a Source;
  design decisions belong in a `design` document, not here.

## Acceptance criteria

The test is whether **someone who did not write the requirement** can decide the outcome without asking. Two
shapes work:

- **Measurable condition** — a value, a unit, a tolerance, and the conditions under which it holds.
- **Given / when / then** — for behavioural requirements, where the interesting part is the state before the
  trigger.

An acceptance criterion that restates the statement in different words is not one. If the statement is
testable as written, say so and cite the test rather than paraphrasing.

## What does not belong in the document

**Per-requirement workflow status** — `in-progress`, `blocked`, `passed`. That state lives in the issue
tracker or the test report, and a second copy inside the document is one nobody updates. The document's own
`lifecycle` field is the only status the contract tracks, and it is document-level on purpose.

**Implementation plans and sequencing.** They are perishable; the requirements are durable. Milestone
documents hold them.

**Verification results.** The requirement declares the method; the run that produced a result belongs with the
result.
