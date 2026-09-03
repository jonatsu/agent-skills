---
name: brainstorming
description: Collaborate on an unformed idea by widening useful possibilities, narrowing a direction, and producing an explicitly incomplete design or plan draft. Use for ideation, shaping an early concept, scoping an opportunity, or deciding what an idea could become; not for technical design, implementation planning, or criticism of a settled plan.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Brainstorming

Turn an unformed idea into a design or plan draft that preserves the user's intent and gives technical design a useful
starting point. The draft stays explicitly incomplete: it does not settle architecture, interfaces, failure handling, or
implementation order.

## Work Conversationally

Read available context before asking questions. Keep the conversation as the working surface rather than exposing a
phase checklist or requiring approval after every exchange.

For a vague seed, make the first substantive response a small widening pass. Offer a few relevant branches, options, or
adjacent ideas before committing to an interpretation. Each branch should state what changes, what it gains, and its
main cost. Say whether branches conflict or can compose. Recommend a direction when useful, but keep live alternatives
visible until the user narrows them.

When the seed is too ambiguous for relevant branches, ask one anchoring question first. Do not invent alternatives for
an already narrow or explicitly decided request merely to demonstrate brainstorming.

Ask one consequential question at a time. Use bounded options when they reveal the decision; use an open question when
options would constrain the idea. A response that asks for user input ends with exactly one question. Keep any other
uncertainties as observations or parked questions for a later turn. Do not ask questions to complete a checklist.

Decompose a request with several independently valuable outcomes before exploring details. Ask which outcome the user
wants to consider first as the first question after naming them; do not substitute a cross-cutting question. Keep the
others as named stubs. Do not ask any cross-cutting or secondary question in that response. Combine compatible ideas.
Park an attractive tangent when it would expand or displace the current purpose; explain why it is deferred.

Research facts or prior art when they could change the premise, branch set, or recommendation. Keep factual findings,
agent recommendations, provisional assumptions, and user decisions distinguishable. Challenge weak premises,
unnecessary complexity, dependencies, omissions, and difficult-to-reverse choices proportionately. Brainstorming is
exploratory, so do not turn this into formal plan criticism.

## Preserve User Control

Recommend with reasons but do not silently make a consequential product decision. Ask for confirmation when a next step
would change an established purpose, intent, desired outcome, or scope; select an unchosen consequential branch; accept
material cost, risk, compatibility loss, or an irreversible direction; or hand a draft to technical design.

A clear choice in the user's ordinary response is already confirmation. Do not ask them to repeat it. Facts established
through research, labeled recommendations, reversible provisional assumptions, and parked tangents do not need a
separate confirmation.

If a discovery changes the intended outcome, target user, or product scope while technical design or planning is under
way, return to brainstorming. Keep the former direction provisional until the user confirms the revised intent.

## Draft and Handoff

Synthesize an explicitly incomplete draft when the intended outcome, promising direction, scope, consequential
constraints, and open questions are legible. It should let a technical designer continue without reconstructing the
conversation or inventing purpose or scope.

Record the original idea, purpose, intent, desired outcome, branches considered, current direction, scope, exclusions,
parked ideas, consequential constraints and assumptions, bounded questions for technical design, and whether each item
is a user decision, recommendation, or provisional idea. Add actors, prior art, success measures, or rejected
alternatives only when they help the later reader.

When the work advances a larger initiative, reference its governing overview near the beginning of the saved draft and
state how the selected direction advances that intent. Do not hand a draft to technical design when its direction weakens
the governing intent. Return to brainstorming to revise the direction with the user instead.

Keep the draft free of unearned architecture, interfaces, schemas, file layouts, and task breakdowns. An early technical
direction is allowed only when it is marked provisional.

Conversation is normally the working surface. Save immediately when the user asks. Save a draft advancing to technical
design at handoff. When an unsaved working draft risks being lost as context fills, recommend saving and explain the
continuity risk; leave that write to the user's decision. Chat-only completion is appropriate for an explicitly ephemeral
or abandoned idea.

Resolve a saved draft's path in this order:

1. A user-supplied path.
2. An existing draft already in scope.
3. A governing overview's companion-document map.
4. A documented repository convention.
5. One clear convention established by existing plan or design documents.
6. Otherwise, propose `docs/plans/<name>-draft.md` and ask once.
7. Outside a repository, ask for a destination.

For the fallback, use two or three descriptive kebab-case words plus `-draft.md`. Reuse an existing file only when it is
the same draft. State the resolved location before saving.

Before technical-design handoff, ask whether the draft accurately captures what the user wants to refine. This single
fidelity confirmation confirms intent, not completeness or implementation authorization.
