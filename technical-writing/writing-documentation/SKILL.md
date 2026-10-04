---
name: writing-documentation
description: "Design, draft, review, or restructure documentation so its reader understands or acts on the first pass. Use for tutorials, how-to guides, references, explanations, and sorting content by Diátaxis type; specs, PRDs, SRSs, and design documents alongside the skill owning their content; decision records, ADRs, release notes, runbooks, onboarding, and matching a docs set's house style. Not for READMEs, quickstarts, or docs landing pages (writing-readmes), or sentence-level editing (writing-for-humans)."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Writing Documentation

This skill owns the document: its reader, its type, what belongs in it, where each concept is explained, which
sources govern its claims, and how a reader reaches it. `writing-for-humans` owns its sentences and paragraphs
and runs the final **reader-ready** pass. `writing-readmes` owns a project's front door. A document is done when
its intended reader understands the subject or completes the task on the first pass.

The guidance is general. Where it names commands or interfaces, apply the rule to whatever the document's
subject actually is.

## Establish the Reader and Outcome

Derive the reader from the request, the repository, and the document. Documentation serves operators, support
staff, newcomers, and end users as often as developers, and a wrong assumed reader is the costliest error this
skill can make. Unless something establishes otherwise, write for a capable reader who is new to this subject,
system, and domain.

**The reader does not share your knowledge.** Everything you learned while working on the subject, from its
concepts and terms to its abbreviations, components, and conventions, is opaque to them until the document
explains it. Explain each non-obvious concept, term, or identifier where the document first uses it, and expand
it enough for the reader to follow what comes next. Explain it once per document; later uses rely on that first
explanation. "Explain Concepts Where the Reader Meets Them" below says how.

Identify:

- the reader's existing knowledge;
- the question they need answered or the task they need completed;
- the correct outcome, visible result, or decision; and
- the facts, interfaces, rules, and constraints that need verification.

Ask a focused question when a missing reader, outcome, or product fact would change the document's form or
claims. Flag unsupported assertions, ambiguity, missing prerequisites, and factual gaps; never remove them
silently or fill them with a plausible invention.

## Build the Authority Map

An **authority map** records which source governs each consequential class of claim. Build it before drafting:

1. List the claims whose accuracy affects the reader's understanding or action.
2. Name the governing source for each class of claim.
3. Classify what you hold as confirmed, assumed, unknown, or conflicting.
4. Resolve material unknowns and conflicts, or carry them visibly into the delivery.

Unless the project establishes otherwise, current implementation and schemas govern current behavior, accepted
requirements and decisions govern intended behavior, and released artifacts govern shipped behavior. Existing
documentation establishes terminology and house style, not that a changed behavior is still current.

Check a claim about an upstream mechanism against its pinned source, never against memory or a summary. A
reference that describes upstream behavior names that source and its version, and the source wins where the two
disagree.

When plausible sources conflict, state the conflict and continue the work that does not depend on it. Keep
working notes out of the reader-facing document. The map is complete when every consequential claim is either
supported by its governing source or reported as unresolved.

## Choose the Document Type

Classify content by the reader's need, using the four types of the Diátaxis framework. Two questions place any
piece of content:

- Does it inform **action** (what to do) or **understanding** (what is so and why)?
- Does it serve the reader's **study** (acquiring a skill) or their **work** (applying one)?

| Type         | Informs       | Serves | The reader                              | What tends to leak in  |
| ------------ | ------------- | ------ | --------------------------------------- | ---------------------- |
| Tutorial     | Action        | Study  | A learner following a guided lesson     | Explanation            |
| How-to guide | Action        | Work   | A competent reader doing one real task  | Teaching, reference    |
| Reference    | Understanding | Work   | Someone looking one fact up mid-task    | Instruction, narrative |
| Explanation  | Understanding | Study  | Someone stepping back to understand why | Procedure, reference   |

Give each document one primary type. When content of another type appears, move it to a document of that type
and link to it; never blend the two. Report a classification with its evidence, the sentences or structure that
place it.

- **Tutorial:** build toward a usable result with visible checkpoints. Explain only what keeps progress clear.
  Show file placement when it matters.
- **How-to guide:** address one task for a reader who already has the basics. Put prerequisites, decision forks,
  expected results, and recovery beside the step they affect.
- **Reference:** mirror the structure of what it describes. Cover inputs, outputs, options, defaults, limits,
  and failure cases, each stated plainly enough to look up.
- **Explanation:** answer one bounded "why" question: context, constraints, alternatives, and trade-offs.

Two further types fall outside the four. A **decision record** makes a decision reviewable after its conditions
change; see Decision Records below. A **change note** says what changed, who is affected, the required action,
compatibility effects, and migration or recovery; for a maintained changelog, read
[references/changelog.md](references/changelog.md).

For a decision record, change note, runbook notice, or executive summary, lead with the action, result, decision,
or state, and name the owner and deadline when they matter.

## Specs, PRDs, and Design Documents

A requirements specification, PRD, SRS, or technical design has its own content owner:
`writing-specs` for intended behavior and acceptance, `technical-design` for how a system realizes
it. That skill decides what the document must contain. This skill still governs how it reads, and every rule
here applies to it in full: the authority map, one term per concept, concepts explained where first relied on,
every sentence carrying information, and the `writing-for-humans` **reader-ready** pass.

`technical-design` sets the bar a design document must meet before its handoff.

## Match an Established House Style

A document that joins an existing set is judged against that set. Infer the set's conventions from
representative documents of the same type before drafting into it.

One exemplar supports voice matching; a repeatable convention needs two or more. Record a compact style profile:
the covered types and audience, the repeated structure, register, formatting, and terminology, the exemplar
evidence for each convention, and what the profile does not govern.

**Where no set exists, or no convention has two exemplars, the default is `writing-for-humans` and the
repository's own writing rules.** Never build a house style from a single document.

For a numbered series, such as decision records, check its location, file extension, and markup, its numbering
and filename pattern, and its heading set. Continue the sequence; surface a conflict between two schemes rather
than picking one.

Place a new document where the user says, then where the repository's convention puts its type. Where neither
settles it, use `context-architecture`'s default layout: a how-to guide or runbook goes to `docs/how-to/`, a
reference or explanation of current behavior to `docs/reference/`, and a decision record to `docs/decisions/`.
Its "Where a New Document Goes" section places every other type.

Repository requirements outrank the profile. The profile outranks this skill's defaults for whatever it covers
with evidence, because consistency across a set serves the reader more than one improved page.

## Cut Document-Level Noise

`writing-for-humans` defines **noise**: a statement that gives the reader nothing new or useful where they meet
it. A complex subject makes noise costlier, because each unneeded sentence makes the what, why, and how harder to
follow. At the document level, noise is content that another section, another document, or the document's type
already covers. Cut:

- an announcement of what follows; state it instead;
- a narrated cross-reference ("as the overview describes"); the link alone does that job;
- a restatement of another section; link to the section that owns the point;
- text about the document itself or how it came to be written; and
- history of how a choice was reached; the document describes the current state.

State the document's scope, versions, and sources once, where it opens, and never repeat them per claim. A
reference names its upstream source and version in that opening, not beside each fact.

Date a statement only where the date changes its meaning: a revision history, a measurement, an evaluation true
as of its run, or a record's status line. Elsewhere state the status: "awaits the customer's review", not
"proposed on 25 September".

Any document that states a decision gives each rejected option directly, with the reason it lost: "Stopping the
boot instead would leave the device unrecoverable, because…", not "two alternatives were weighed".

## Explain Concepts Where the Reader Meets Them

On first use of a technical concept in each document, spend one or two plain sentences on what it is and what it
does in this subject, then continue. For example: "IMA, the kernel's Integrity Measurement Architecture, hashes
each file its policy names into a TPM PCR before the file runs, so the PCR records which software ran; the
platform seals the disk key to that record." The last clause is what the concept does here. A glossary holds
the one-line definition, and the document adds why the concept matters here. Repeating the explanation later in
the same document is noise.

In a reference, say what a setting or feature is for before how it works, and give each one a reader looks up by
name its own heading.

When one word carries two concepts, give each its own durable name and glossary entry. A word such as
"manifest" that means three different files in one project misleads every reader who meets it.

When a design or plan covers more than two components, or a flow whose order matters, add a diagram beside the
text it explains: a flowchart for structure and decisions, a sequence diagram for ordered interactions, a state
diagram for a lifecycle. In Markdown, use Mermaid unless the set follows another convention. Explain any diagram
or screenshot the reader must act on, and never rely on color alone.

## Identifiers and Links

Write the document so its meaning survives when an identifier changes or disappears. Lead with the behavior,
decision, or consequence and append the key only for traceability, as `writing-for-humans` specifies. A table or
status list may keep identifiers for lookup, provided every row also states its meaning in plain language.

Keep identifiers the reader uses directly: API fields, configuration keys, error codes, and formal traceability
keys. Introduce each with its meaning. A numbered series may keep its key in a title that also states the
subject, as in `ADR-0014: Store rendered reports in object storage`.

Link every source the document names. A reader must reach every document they need by following links; one who
needs a text search to find it has hit a defect.

## Make the Content Usable

- Put prerequisites, irreversible effects, limits, and caveats before the reader meets them.
- Use a realistic example where it settles a concept, decision, or task, and omit setup that does not affect it.
- Validate instructions the reader will follow when the environment or access is available; otherwise name what
  remains unverified.
- For a failure, state the failed condition, its known cause, and the next action. Name the invalid value,
  required form, limit, or conflicting state when known.
- Use link text that names its target.

## Decision Records

Write one when a decision is hard to reverse, surprising without context, and the outcome of a real trade-off.
When any of the three is missing, skip it. Do not wait to be asked: a decision that clears the gate and goes
unwritten gets argued again.

Read [references/decision-record.md](references/decision-record.md) before writing one, for the light and full
forms, freezing and supersession, numbering and file conventions, and a worked example.

## Notes and Safety Instructions

A reader who misreads either one acts wrongly or gets hurt.

**A note carries information only.** An instruction, requirement, limit, tolerance, or step result belongs in
the step it governs. Verify by deleting every note: a reader must still complete the procedure correctly.
Anything that fails that test becomes a step.

**Match the signal word to the risk.** A warning signals a risk of injury or death; a caution, a risk of damage
to equipment, data, or systems. Where both apply, use a warning.

**Order a safety instruction in three parts:** the signal word, then the command or condition, then the
consequence of ignoring it. A reader who stops after the first line must still have the instruction. Put it
before the step it protects.

## Improve an Existing Set in Place

Restructure a documentation set from the inside, one piece at a time. Pick one document or section, place it with
the two type questions, make the single change that serves its reader best, and repeat. A new structure emerges
from these changes. Never create empty per-type sections or directories up front, and never split a mixed
document into four files in one move.

## Review and Finish

1. Settle the document's claims, type, examples, and organization.
2. Check it against the list below, and report structural defects before any prose edit.
3. Apply `writing-for-humans` to the complete draft and resolve every defect its **reader-ready** pass finds.
4. Repeat that pass after each material revision.

Check that:

- the type matches the reader's need, and no other type has leaked in;
- a document joining a set follows that set's evidenced conventions;
- the reader finds the outcome, prerequisites, constraints, and next action without prior knowledge beyond
  their own;
- every consequential claim is supported by its governing source or reported as unresolved;
- every concept is explained where first relied on, and every term names one concept;
- the document holds no noise, and each decision gives its rejected options with reasons;
- every example, step, interface detail, and failure path matches the subject as it is;
- the document reads correctly without resolving any internal identifier elsewhere;
- every named source is linked, and every needed document is reachable by links;
- the procedure still works with every note deleted, and each warning or caution matches its risk; and
- accessibility information and recovery guidance cover what the reader needs.

When reviewing a high-stakes document, or delegating any review or readability pass to a subagent, read
[references/review-sequence.md](references/review-sequence.md) first.

The document is complete when it is **reader-ready** and every remaining evidence gap is visible in the delivery.

## Response Modes

- **Draft:** produce the document in its selected type.
- **Review:** report missing context, type leaks, structural problems, inaccurate examples, accessibility gaps,
  and unclear recovery before suggesting edits.
- **Condense:** remove noise and misplaced content; keep reader-critical context, decisions,
  prerequisites, examples, caveats, and recovery.
- **Expand:** add confirmed context, examples, constraints, or recovery, never invented ones.

For an existing file, return text or a diff unless the user asked for an in-place edit.
