---
name: technical-writing
description: "Design, draft, or review technical documents that help engineers understand or act on the first pass."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Technical Writing

Use this skill to design, draft, or review technical documents for developers and technical users: tutorials,
how-to guides, README and setup guides, references, explanations, design and decision records, and release
notes.

The goal is a document that lets its intended reader understand the relevant system or complete the relevant
task on the first pass. Follow active global and repository writing requirements for prose. Use
`writing-for-humans` only for a separate copy-editing pass over supplied prose.

## Establish the Reader and Outcome

Unless the request, repository, or document establishes otherwise, write for a technically capable reader who
is unfamiliar with the specific system, domain, and document subject.

Identify:

- the reader's existing knowledge;
- the question they need answered or task they need completed;
- the correct outcome, visible result, or decision; and
- the facts, interfaces, and constraints that require verification.

When the reader's subject knowledge is unknown, take the conservative explanatory path:

- Define subject-specific concepts and terms before relying on them.
- State assumptions, prerequisites, and consequences that affect correct action.
- Explain why a step, constraint, or decision matters when the reason is not apparent from the task.
- Link or separate deeper background rather than interrupting the primary task with general technical
  instruction.

Ask a focused question when the missing reader, outcome, or product fact would materially change the
document's form or claims.

## Choose a Document Shape

Choose one primary mode. Split and link material when another mode would interrupt the reader's task.

- **Tutorial:** teach a newcomer through a working result. State what they will build, use visible checkpoints,
  and explain only enough context to keep progress clear.
- **How-to guide:** help a competent reader complete a specific task. Put prerequisites, decision forks,
  expected results, and recovery near the action they affect. Link background rather than teaching it inline.
- **Reference:** support lookup. Mirror the interface or system being described. Cover inputs, outputs, options,
  limits, defaults, and failure cases accurately.
- **Explanation:** answer one bounded why question. Cover context, constraints, alternatives, and trade-offs.
- **Decision record:** make a decision and its consequences reviewable. State the context, decision,
  alternatives considered, and resulting obligations.
- **Change note:** explain what changed, who is affected, required action, compatibility effects, and recovery or
  migration steps.

A README or setup guide may begin with orientation, then link to the mode-specific material its reader needs.

## Make Technical Content Usable

- Put prerequisites, irreversible effects, limits, and caveats before readers encounter them.
- Use examples when they settle an important concept, decision, or task. Keep them realistic and omit setup that
  does not affect the result.
- For implementation tutorials, show file placement when it matters and build toward a usable result.
- Explain consequential implementation and architectural decisions, not only the final commands or code.
- Validate runnable instructions when the required environment is available. Otherwise identify what remains
  unverified.
- For errors and recovery, state the failed condition, known cause, and next action. Name the invalid value,
  required form, limit, or conflicting state when known.
- Make informative images understandable without color alone. Use meaningful link text and explain screenshots or
  diagrams that readers need to act on.
- Surface missing facts rather than inventing examples, commands, limits, or recovery steps.

## Review

Check:

- Does the selected mode match the reader's purpose?
- Can the reader find the outcome, prerequisites, constraints, and next action?
- Does each example, command, interface detail, and error path match the system?
- Do tutorials provide visible progress and a usable result?
- Do references mirror the described interface and cover its important limits and failures?
- Do explanations and decision records make the relevant reasoning and consequences visible?
- Does the document provide the accessibility information and recovery guidance its reader needs?

Flag missing context or structural defects before proposing prose-only edits.

## Response Modes

- **Draft:** produce the requested document in its selected mode.
- **Review:** report missing context, structural problems, inaccurate examples, accessibility gaps, and unclear
  recovery paths before suggesting edits.
- **Condense:** preserve reader-critical context, decisions, prerequisites, examples, caveats, and recovery
  guidance while removing redundant material.
- **Expand:** add confirmed context, examples, constraints, or recovery guidance without inventing them.

For an existing file, return text or a diff unless the user requested an in-place edit.
