---
name: writing-documentation
description: "Design, draft, or review documentation of any kind so its reader understands or acts on the first pass, and match the house style of an existing documentation set. Use for tutorials, how-to guides, READMEs, references, explanations, decision records, release notes, runbooks, onboarding and process documents, and technical documentation specifically. Not for prose-level editing, which is writing-for-humans."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Writing Documentation

Use this skill to design, draft, or review documentation of any kind: tutorials, how-to guides, README and
setup guides, references, explanations, design and decision records, release notes, runbooks, and onboarding
or process documents. Technical documentation for developers is one case among these, not the boundary.

The goal is a document that lets its intended reader understand the subject or complete the task on the first
pass. This skill owns the document: its purpose, reader, organization, examples, document type, and the house
style of the set it joins.

Its guidance is general. Where a passage names commands, code, or interfaces, treat it as the technical case
of a general rule and apply the rule to whatever the document's subject actually is.

Use `writing-for-humans` for prose-level drafting, editing, and review. That skill owns the sentence and the
paragraph, and it applies to text that is not documentation at all.

## Establish the Reader and Outcome

Derive the reader from the request, the repository, and the document itself. Do not assume a technical reader:
documentation serves operators, support staff, new team members, and end users as often as it serves
developers, and the wrong assumed reader is the most expensive error this skill can make.

Unless something establishes otherwise, write for a capable reader who is unfamiliar with the specific
subject, system, process, and domain.

Identify:

- the reader's existing knowledge;
- the question they need answered or task they need completed;
- the correct outcome, visible result, or decision; and
- the facts, interfaces, rules, and constraints that require verification.

When the reader's subject knowledge is unknown, take the conservative explanatory path:

- Define subject-specific concepts and terms before relying on them.
- State assumptions, prerequisites, and consequences that affect correct action.
- Explain why a step, constraint, or decision matters when the reason is not apparent from the task.
- Link or separate deeper background rather than interrupting the primary task with general instruction.

Ask a focused question when the missing reader, outcome, or product fact would materially change the
document's form or claims.

Flag unsupported assertions, ambiguity, missing prerequisites, and factual gaps. Do not silently remove them.

## Match an Established House Style

A document that joins an existing set is judged against that set, not against a general standard. Before
drafting into one, infer its conventions from the documents already there.

Use representative exemplars from the same document type. One exemplar supports voice matching; require two or
more before inferring a repeatable convention. A convention drawn from a single document is a coincidence
until a second one confirms it.

Record a compact style profile:

- the covered document types and audience;
- repeated structure, register, formatting, and terminology conventions;
- exemplar evidence for each convention; and
- aspects the profile does not govern.

Apply only supported conventions. Repository requirements outrank the profile, and the source author's voice
governs wherever the profile is silent. When the profile and this skill's defaults conflict, the profile wins
for anything it covers with evidence: consistency within a documentation set serves the reader more than an
isolated improvement to one page.

`writing-for-humans` preserves an individual author's voice at the sentence level. This section is the
document-set counterpart: it governs conventions repeated across many documents.

## Choose a Document Shape

Choose one primary mode. Split and link material when another mode would interrupt the reader's task.

- **Tutorial:** teach a newcomer through a working result. State what they will build, use visible checkpoints,
  and explain only enough context to keep progress clear.
- **How-to guide:** help a competent reader complete a specific task. Put prerequisites, decision forks,
  expected results, and recovery near the action they affect. Link background rather than teaching it inline.
- **Reference:** support lookup. Mirror the structure of whatever is being described, whether an interface, a
  system, or a process. Cover inputs, outputs, options, limits, defaults, and failure cases accurately.
- **Explanation:** answer one bounded why question. Cover context, constraints, alternatives, and trade-offs.
- **Decision record:** make a decision and its consequences reviewable. State the context, decision,
  alternatives considered, and resulting obligations.
- **Change note:** explain what changed, who is affected, required action, compatibility effects, and recovery or
  migration steps.

A README or setup guide may begin with orientation, then link to the mode-specific material its reader needs.

## Make the Content Usable

- Put prerequisites, irreversible effects, limits, and caveats before readers encounter them.
- For decision records, change notes, operational notices, and executive summaries, lead with the action,
  result, decision, or state. Name the owner and deadline when relevant.
- Use examples when they settle an important concept, decision, or task. Keep them realistic and omit setup that
  does not affect the result.
- Build a tutorial toward a usable result. For an implementation tutorial, show file placement when it
  matters.
- Explain consequential decisions and the reasoning behind them, not only the final steps, commands, or code.
- Validate instructions the reader will follow when the required environment or access is available.
  Otherwise identify what remains unverified.
- For errors, failures, and recovery, state the failed condition, known cause, and next action. Name the
  invalid value, required form, limit, or conflicting state when known.
- Make informative images understandable without color alone. Use meaningful link text and explain screenshots or
  diagrams that readers need to act on.
- Surface missing facts rather than inventing examples, commands, limits, or recovery steps.

## Write Notes and Safety Instructions

These two elements carry their own rules, because a reader who misreads either one acts wrongly or gets hurt.

**A note carries information only.** It must not contain an instruction, a requirement, a limit, a tolerance,
or the result of a step. Those belong in the step itself, next to the action they govern. Verify by deleting
every note and confirming a reader can still complete the procedure correctly. Anything that fails that test
was never a note, and becomes a step.

**Match the signal word to the risk.** A warning signals a risk of injury or death. A caution signals a risk of
damage to equipment, data, or systems. Where both risks apply at once, use a warning.

**Order a safety instruction in three parts:** the signal word, then the command or the condition the reader
must satisfy, then the consequence of not obeying. Never open with the explanation. A reader who stops after
the first line must still have the instruction, not the rationale.

Put a safety instruction before the step it protects, never after.

## Review

Check:

- Does the selected mode match the reader's purpose?
- When the document joins an existing set, does it follow that set's evidenced conventions?
- Can the reader find the outcome, prerequisites, constraints, and next action?
- Does the document assume more reader knowledge than the identified reader has?
- Does each example, step, interface detail, and failure path match the subject as it actually is?
- Do tutorials provide visible progress and a usable result?
- Do references mirror what they describe and cover its important limits and failures?
- Do explanations and decision records make the relevant reasoning and consequences visible?
- Does the document provide the accessibility information and recovery guidance its reader needs?
- Does the procedure still work with every note deleted, and does each warning or caution match its risk level?

Flag missing context or structural defects before proposing prose-only edits.

## Response Modes

- **Draft:** produce the requested document in its selected mode.
- **Review:** report missing context, structural problems, inaccurate examples, accessibility gaps, and unclear
  recovery paths before suggesting edits.
- **Condense:** preserve reader-critical context, decisions, prerequisites, examples, caveats, and recovery
  guidance while removing redundant material.
- **Expand:** add confirmed context, examples, constraints, or recovery guidance without inventing them.

For an existing file, return text or a diff unless the user requested an in-place edit.
