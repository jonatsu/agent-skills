---
name: technical-writing
description: "Design, draft, or review technical documents: structure, examples, accessibility, and errors."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Technical Writing

This skill owns document-level decisions. Follow the active global and repository writing requirements for
prose; this skill does not repeat or override them. For a copy-editing pass over supplied prose, use
`writing-for-humans` when it is available.

## Establish the Reader and Outcome

Identify the reader, their existing knowledge, and what they need to understand or do after reading. State the
document's purpose early. Ask a focused question when the missing reader, task, or decision would change the
document's shape.

## Choose a Document Shape

Use the shape that lets the reader find the needed information:

- **Task guide, tutorial, or onboarding:** prerequisites, ordered actions, expected result, recovery.
- **Explanation or design document:** problem, model or decision, consequences, and worked examples where they
  settle an important point.
- **Reference:** stable entries for commands, APIs, schemas, limits, parameters, outputs, and failure cases.
- **Comparison:** a table only when matching the same fields across options is faster than prose.

Do not force a stock outline onto a document whose reader task needs a different order.

## Make Technical Content Usable

- Put prerequisites, limits, caveats, and irreversible effects before the reader can encounter them.
- Use the smallest realistic example that demonstrates the point. Explain its consequence when it is not
  obvious; omit setup that does not affect the decision or task.
- Make informative images understandable without color alone. Provide meaningful link text and text that
  explains any screenshot or diagram needed to complete the task.
- For an error or recovery path, state the failed condition, known cause, and next action. Name the invalid
  value, required form, limit, or conflicting state when known.
- Do not invent absent technical details, examples, or recovery steps. Surface the gap under the applicable
  evidence policy.

## Review

Check that the document gives its intended reader enough context to act, uses a shape that matches the task,
and includes the prerequisites, constraints, examples, accessibility information, and recovery guidance the
reader needs. Flag missing information and structural defects before proposing prose-only edits.

## Response Modes

- **Draft:** produce the requested document in the selected shape.
- **Review:** report missing context, structural problems, weak examples, accessibility gaps, and unclear
  recovery paths before suggesting edits.
- **Condense:** preserve the reader's required context, decisions, prerequisites, examples, and caveats while
  removing redundant material.
- **Expand:** add confirmed prerequisites, examples, constraints, or recovery guidance without inventing them.

For an existing file, return text or a diff unless the user requested an in-place edit.
