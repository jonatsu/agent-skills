---
name: idea-brainstorming
description: Collaborate on an unformed idea by widening useful possibilities, narrowing a direction, or saving an active brainstorm as an explicitly incomplete spec or design draft. Use for ideation, shaping an early concept, scoping an opportunity, or preparing its next-phase handoff; not for writing specs, technical design, implementation planning, criticism of a settled plan, or a generic session handoff.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Idea Brainstorming

Turn an unformed idea into a draft that preserves the user's intent and gives a spec or technical design a useful
starting point. The draft stays explicitly incomplete, as "Draft and Handoff" defines.

## Work Conversationally

Read available context before asking questions. Keep the conversation as the working surface rather than exposing a
phase checklist or requiring approval after every exchange.

For a vague seed, make the first substantive response a small widening pass. Offer a few relevant branches, options, or
adjacent ideas before committing to an interpretation. Each branch should state what changes, what it gains, and its
main cost. Say whether branches conflict or can compose. Recommend a direction when useful, but keep live alternatives
visible until the user narrows them.

When a seed proposes a solution before establishing its purpose, surface the affected actor and desired outcome before
widening. Keep the proposed solution as a live branch unless the user already made it a constraint or decision. Treat a
changed framing as a recommendation until the user confirms it.

When the seed is too ambiguous for relevant branches, make the first substantive response one anchoring question and
nothing else; interpretations, branches, examples, and recommendations wait for the answer. Treat an already narrow or
explicitly decided request as narrowed, and continue from it without widening.

After a direction starts to narrow, check whether its goal describes an observable outcome or only an activity. Sharpen
an activity from available context when the interpretation is well supported and reversible. Ask one consequential
question when the missing outcome could change the product direction.

Identify one observable success signal before the next-phase handoff. Use a binary observation or human judgment when
honest measurement is unavailable. Quantify only when the metric, method, and threshold represent genuine success.

Ask one consequential question at a time. Use bounded options when they reveal the decision; use an open question when
options would constrain the idea. A response that asks for user input ends with exactly one question. Keep any other
uncertainties as observations or parked questions for a later turn.

Decompose a request with several independently valuable outcomes before exploring details. Name them, then ask only
which outcome the user wants to consider first; that response carries no other question, cross-cutting or secondary.
Keep the others as named stubs. Combine compatible ideas. Park an attractive tangent when it would expand or displace
the current purpose, and explain why it is deferred.

When the user states a current purpose and mentions another idea as optional or future work, keep the current purpose
selected and present the optional idea as parked, not as an equal choice, unless the user explicitly asks to expand
scope.

Before the user chooses an outcome, keep the discussion at the outcome level. Product shapes, architecture,
implementation approaches, and a recommended direction wait until an outcome is selected, because those comparisons
speculate across work nobody has chosen yet.

Research facts or prior art when they could change the premise, branch set, or recommendation. Keep factual findings,
agent recommendations, provisional assumptions, and user decisions distinguishable. Challenge weak premises,
unnecessary complexity, dependencies, omissions, and difficult-to-reverse choices proportionately, keeping the
challenge exploratory; formal criticism of a settled plan belongs elsewhere.

Order unresolved assumptions by their effect on the direction. Identify which failures would invalidate it, which would
change it materially, and which can wait. For the most consequential unknown, seek or name the smallest evidence that
could change the decision. Keep the affected direction provisional until the evidence settles it or the user accepts
the risk.

Repository evidence establishes current technical behavior and constraints. It does not establish desired product or
business policy. Treat unsupported target users, priorities, entitlements, service levels, retention rules, and
compliance duties as user-supplied constraints or provisional assumptions.

## Preserve User Control

Recommend with reasons, and leave each consequential product decision to the user. Ask for confirmation when a next step
would change an established purpose, intent, desired outcome, or scope; select an unchosen consequential branch; accept
material cost, risk, compatibility loss, or an irreversible direction; or hand a draft to `writing-specs` or
`technical-design`.

When the user asks which consequential product direction to choose, give a conditional recommendation and its reason
before asking for their decision. If the available evidence cannot support a recommendation, identify the smallest
decision-changing evidence to gather instead. A comparison or a follow-up question never stands in for the
recommendation.

A clear choice in the user's ordinary response is already confirmation and needs no repetition. Facts established
through research, labeled recommendations, reversible provisional assumptions, and parked tangents need no separate
confirmation.

If a discovery changes the intended outcome, target user, or product scope while the spec, technical design, or
planning is under way, return to brainstorming. Keep the former direction provisional until the user confirms the
revised intent.

## Draft and Handoff

Synthesize an explicitly incomplete draft when the intended outcome, promising direction, scope, consequential
constraints, observable success signal, and open questions can each be written in one sentence without guessing. It
should let a spec writer or technical designer continue without reconstructing the conversation or inventing purpose or
scope.

Record the original idea, purpose, intent, desired outcome, branches considered, current direction, scope, exclusions,
parked ideas, consequential constraints and assumptions, observable success signal, bounded questions for the spec or
technical design, and whether each item is a user decision, recommendation, or provisional idea. Record consequential
prohibited outcomes when they define success. Add actors, prior art, detailed measurements, or rejected alternatives
only when they help the later reader.

When the work advances a larger initiative, reference its governing overview near the beginning of the saved draft and
state how the selected direction advances that intent. When the direction weakens the governing intent, revise it with
the user before any handoff.

Keep the draft free of unearned detailed requirements, architecture, interfaces, schemas, file layouts, failure
handling, and task breakdowns. An early technical direction is allowed only when it is marked provisional.

Conversation is normally the working surface. Save immediately when the user asks, and save the draft at handoff. When
an unsaved working draft risks being lost as context fills, recommend saving and explain the continuity risk; leave that
write to the user's decision. Chat-only completion is appropriate for an explicitly ephemeral or abandoned idea.

Resolve a saved draft's path in this order:

1. A user-supplied path.
2. An existing draft already in scope.
3. A governing overview's companion-document map.
4. A documented repository convention.
5. One clear convention established by existing plan or design documents.
6. Otherwise, propose `docs/plans/<name>-draft.md`, its place in `context-architecture`'s default layout, and ask
   once.
7. Outside a repository, ask for a destination.

For the fallback, use two or three descriptive kebab-case words plus `-draft.md`. Reuse an existing file only when it is
the same draft. State the resolved location before saving.

Route the handoff to `writing-specs` when user-visible behavior or acceptance needs a durable contract, and straight to
`technical-design` when the direction is small and its behavior already clear. When the direction is large, so that
design would otherwise decide user-visible behavior, user journeys, or acceptance that no spec covers, offer the spec,
say why, and let the user decide. Record the decision in the draft. A spec written only to fill a stage has no reader.

Before the next-phase handoff, ask whether the draft accurately captures what the user wants to refine. This single
fidelity confirmation confirms intent, not completeness or implementation authorization. The handoff is complete when
the draft is saved, its route and the user's decision on any offered spec are recorded, and the user has confirmed its
fidelity.
