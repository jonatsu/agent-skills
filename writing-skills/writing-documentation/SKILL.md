---
name: writing-documentation
description: "Design, draft, review, or restructure documentation so its reader understands or acts on the first pass. Use for tutorials, how-to guides, references, explanations, and sorting content by Diátaxis type; specs, PRDs, SRSs, and design documents alongside the skill owning their content; decision records, ADRs, release notes, runbooks, onboarding, and matching a docs set's house style. Not for READMEs, quickstarts, docs landing pages, or files such as CONTRIBUTING or CHANGELOG (repo-landing-docs), or sentence-level editing (writing-for-humans)."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Writing Documentation

This skill owns the document. It decides the document's reader, type, and content. It also decides where each concept is
explained, which sources govern its claims, how a reader reaches it, and how its sentences read. `repo-landing-docs`
owns a project's front door and its other landing documents. A document is done when its intended reader understands the
subject or completes the task on the first pass.

Plain language, as ISO 24495-1:2023 defines it, is wording, structure, and design so clear that the intended
readers can easily find what they need. They can also understand what they find and use that information. The
standard groups its guidelines under four principles: relevant, findable, understandable, and usable. This skill
applies all four to a document. It applies relevance in choosing the reader and content, findability in
structure and headings, understandability in prose rules, and usability in review and reader testing.
`writing-for-humans` owns the sentences. Load it before drafting prose, and finish with its reader-ready pass as
well as this skill's review.

The guidance is general. Where it names commands or interfaces, apply the rule to whatever the document's
subject actually is.

## Establish the Reader and Outcome

Derive the reader from the request, the repository, and the document. Documentation serves operators, support
staff, newcomers, and end users as often as developers. A wrongly assumed reader is the costliest error this
skill can make. Unless something establishes otherwise, write for a capable reader who is new to this subject,
system, and domain.

The reader does not share your knowledge. Everything you learned about the subject is opaque to them until the
document explains it, from concepts and terms to abbreviations, components, and conventions. Explain each
non-obvious concept, term, or identifier where the document first uses it. Expand it enough for the reader to
follow what comes next. Explain it once per document; later uses rely on that first explanation. "Explain
Concepts Where the Reader Meets Them" below says how.

Identify:

- the reader's existing knowledge;
- the reading context, such as time pressure, a small screen, a screen reader, or a second language;
- the question they need answered or the task they need completed;
- the correct outcome, visible result, or decision; and
- the facts, interfaces, rules, and constraints that need verification.

When a document has several audiences, name the primary one and let its needs settle every conflict. A runbook
serves the engineer running it at night before the manager who audits it later. Give the secondary reader what
they need without reshaping the main path around them.

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
and link to it. Never blend the two. Report a classification with its evidence, the sentences or structure that
place it.

- **Tutorial:** build toward a usable result with visible checkpoints. Explain only what keeps progress clear.
  Show file placement when it matters.
- **How-to guide:** address one task for a reader who already has the basics. Put prerequisites, decision forks,
  expected results, and recovery beside the step they affect. In a runbook, put the rule that decides the run,
  such as when to rebuild, where every reader sees it. Answer the questions the operator will ask in the guide
  itself. Give commands they can copy as written, with no placeholder such as `NNNN` left to fill in.
- **Reference:** mirror the structure of what it describes. Cover inputs, outputs, options, defaults, limits,
  and failure cases, each stated plainly enough to look up.
- **Explanation:** answer one bounded "why" question: context, constraints, alternatives, and trade-offs.

Two further types fall outside the four. A **decision record** makes a decision reviewable after its conditions
change; see Decision Records below. A **change note** says what changed, who is affected, the required action,
compatibility effects, and migration or recovery. A maintained `CHANGELOG.md` file belongs to
`repo-landing-docs`.

Lead a decision record, change note, runbook notice, or executive summary with the action, result, decision, or
state. Name the owner and deadline when they matter.

## Specs, PRDs, and Design Documents

A requirements specification, PRD, SRS, or technical design has its own content owner. `writing-specs` owns
intended behavior and acceptance; `technical-design` owns how a system realizes it. That skill decides what the
document must contain. This skill still governs how it reads. Every rule here applies to it in full:

- the authority map;
- one term per concept;
- concepts explained where first relied on;
- every sentence carrying information;
- the understandable prose rules; and
- the reader-ready pass.

`technical-design` sets the bar a design document must meet before its handoff.

## Match an Established House Style

A document that joins an existing set is judged against that set. Infer the set's conventions from
representative documents of the same type before drafting into it.

One exemplar supports voice matching; a repeatable convention needs two or more. Record a compact style profile
with these parts:

- the covered types and audience;
- the repeated structure, register, formatting, and terminology;
- the exemplar evidence for each convention; and
- what the profile does not govern.

Where no set exists, or no convention has two exemplars, the default is this skill and the repository's own
writing rules. Never build a house style from a single document.

For a numbered series, such as decision records, check these:

- its location, file extension, and markup;
- its numbering and filename pattern; and
- its heading set.

Continue the sequence; surface a conflict between two schemes rather than picking one.

Place a new document where the user says, then where the repository's convention puts its type. Where neither
settles it, use `context-architecture`'s default layout. It puts a how-to guide or runbook in `docs/how-to/`, a
reference or explanation of current behavior in `docs/reference/`, and a decision record in `docs/decisions/`.
That skill's "Where a New Document Goes" section places every other type.

Repository requirements outrank the profile. The profile outranks this skill's defaults for whatever it covers
with evidence, because consistency across a set serves the reader more than one improved page.

## Cut Document-Level Noise

**Noise** is a statement that gives the reader nothing new or useful where they meet it. Judge it in context: a
true sentence is noise when the text before it already carries it. Apply the deletion test: remove the
sentence, and if the reader loses nothing they need there, it was noise. A complex subject makes noise
costlier, because each unneeded sentence makes the what, why, and how harder to follow. At the document level,
noise is content that another section, another document, or the document's type already covers. Cut:

- an announcement of what follows; state it instead.
- a narrated cross-reference ("as the overview describes"); the link alone does that job.
- a restatement of another section; link to the section that owns the point.
- text about the document itself.
- a record of work on it or its subject, such as repairs, reviews, investigations, and their dates.
- a record of what was checked and found irrelevant.
- a list of what the document leaves out, unless the reader would otherwise assume it is covered.
- a rule that governs every document of its kind; keep it once, in the repository's rules.
- an argument for the document's own legitimacy; state the facts and let them stand.
- history of how a choice was reached; the document describes the current state.

State the document's scope, versions, and sources once, where it opens, and never repeat them per claim. A
reference names its upstream source and version in that opening, not beside each fact.

Date a statement only where the date changes its meaning. Such places include a revision history, a measurement,
an evaluation true as of its run, and a record's status line. Elsewhere state the status: "awaits the customer's
review", not "proposed on 25 September". When the measured state has a commit or version, pin the measurement to
that instead of the date.

Any document that states a decision gives each rejected option directly, with the reason it lost: "Stopping the
boot instead would leave the device unrecoverable, because…", not "two alternatives were weighed".

## Explain Concepts Where the Reader Meets Them

On first use of a technical concept in each document, write one or two plain sentences. State what it is and what
it does in this subject, then continue. For example: "IMA, the kernel's Integrity Measurement Architecture, hashes
each file its policy names into a TPM PCR before the file runs, so the PCR records which software ran; the
platform seals the disk key to that record." The last clause is what the concept does here. A glossary holds
the one-line definition, and the document adds why the concept matters here. Repeating the explanation later in
the same document is noise.

In a reference, say what a setting or feature is for before how it works. Give each one that a reader looks up by
name its own heading.

When one word carries two concepts, give each its own durable name and glossary entry. A word such as
"manifest" that means three different files in one project misleads every reader who meets it. When the domain
itself overloads a word, such as slot, key, image, or partition, name the meaning on first use. For example, write
"the SoC's one-time-programmable key slot", not "the slot".

Add a diagram beside the text it explains when a design or plan covers:

- more than two components; or
- a flow whose order matters.

Use a flowchart for structure and decisions, a sequence diagram for ordered interactions, and a state diagram for
a lifecycle. In Markdown, use Mermaid unless the set follows another convention. Explain any diagram or
screenshot the reader must act on, and never rely on color alone. Give every image and diagram a text alternative
that states what the reader should take from it.

## Write Understandable Prose

Apply these rules to every sentence and paragraph of the document, including one that joins a house style.

Choose the word the intended reader already knows. Keep a technical term the reader's field uses, and explain it
where first used, as the previous section describes. Give each concept one term throughout.

Lead each sentence with its claim, action, or result, and put new or important information at its end. Use the
verb that carries the meaning: "analyze the log", not "perform an analysis of the log". Prefer active voice when
the actor is known and relevant. Keep every article, "that", subject, and verb the grammar needs.

Classify each passage as procedural, telling the reader what to do, or descriptive, explaining what something is
or does. Give a procedural sentence one imperative instruction within 20 words, with any condition before its
command. For example: "If the build fails, read the log." Keep a descriptive sentence within 25 words. Split a
longer sentence unless splitting makes it less clear, and never merge sentences to save words.

Count a code span, identifier, or quotation as one word. These limits are this skill's proxies, adapted from
ASD-STE100. ISO 24495-1 judges a document by how well its readers use it, not by readability formulas.

Give each paragraph one topic, opened by the sentence that states it, and at most six sentences. State how
sentences relate, such as cause, condition, or contrast, in words the reader does not have to reconstruct. Join
two clauses with a semicolon only where the second turns on the first, and never chain two semicolons.

Use prose for connected ideas and a list for discrete items in parallel grammar. Bold only the shortest span
that carries a decision or warning, never as a lead-in or decoration. Back any meaning carried by bold, color, or
position with words. In formal English documents, write full forms such as "it is" and "does not".

## Identifiers and Links

Write the document so its meaning survives when an identifier changes or disappears. Lead with the behavior,
decision, or consequence and append the key only for traceability: "Keep cached values for five minutes
(decision A-003)", not "A-003 is confirmed". A table or status list may keep identifiers for lookup, provided
every row also states its meaning in plain language.

Keep identifiers the reader uses directly: API fields, configuration keys, error codes, and formal traceability
keys. Introduce each with its meaning. A numbered series may keep its key in a title that also states the
subject, as in `ADR-0014: Store rendered reports in object storage`.

In evidence or a list of findings, cite only the identifiers whose presence changes the conclusion. Summarize
the rest in one clause, such as "the other names agree", instead of listing them.

Link every source the document names. A reader must reach every document they need by following links; one who
needs a text search to find it has hit a defect.

Pin a source with an identifier that survives regeneration. Use a release, tag, or commit, or the version or date
the material carries. Never use the hash of a file rebuilt on each update. Keep the precision the evidence
supports. When no pin was recorded, give the read date, because a commit derived afterwards claims an
observation nobody made.

Cite only what the reader can open. A private repository, a deleted file, or a working note is no source for a
published document.

## Make the Content Findable and Actionable

- Write each heading so it predicts what follows. Where the section's message fits, state it: "Refunds take five
  working days", not "Refund information".
- Keep supplementary material, such as background, full data, and edge-case detail, apart from the main path.
  Place it in a later section, an appendix, or a linked document.
- Make the document work when read straight through as well as when skimmed. A listener or a reader in a second
  language cannot skim, so each passage must make sense without jumping ahead.
- Put prerequisites, irreversible effects, limits, and caveats before the reader meets them.
- Use a realistic example where it settles a concept, decision, or task, and omit setup that does not affect it.
- Validate instructions the reader will follow when the environment or access is available; otherwise name what
  remains unverified.
- For a failure, state the failed condition, its known cause, and the next action. Name the invalid value,
  required form, limit, or conflicting state when known.
- Use link text that names its target.
- Group content by what it is, never by when or why it was gathered. Give each section a question its reader
  has.
- Summarize to the points the reader needs rather than listing every item. Name the kind of a change in a clause
  rather than listing each change.
- Put the fact a reader scans for, such as a license or version, first or in its own field.

## Decision Records

Write one when a decision is hard to reverse, surprising without context, and the outcome of a real trade-off.
When any of the three is missing, skip it. Write one unprompted: a decision that clears the gate and goes
unwritten gets argued again.

Read [references/decision-record.md](references/decision-record.md) before writing one. It covers the light and
full forms, freezing and supersession, numbering and file conventions, and a worked example.

## Notes and Safety Instructions

A reader who misreads either one acts wrongly or gets hurt.

A note carries information only. An instruction, requirement, limit, tolerance, or step result belongs in the
step it governs. Verify by deleting every note: a reader must still complete the procedure correctly. Anything
that fails that test becomes a step.

Match the signal word to the risk. A warning signals a risk of injury or death; a caution, a risk of damage to
equipment, data, or systems. Where both apply, use a warning.

Order a safety instruction in three parts: signal word, command or condition, then consequence of ignoring it. A
reader who stops after the first line must still have the instruction. Put it before the step it protects.

## Improve an Existing Set in Place

Restructure a documentation set from the inside, one piece at a time. Pick one document or section and place it
with the two type questions. Make the single change that serves its reader best, and repeat. A new structure
emerges from these changes. Never create empty per-type sections or directories up front. Never split a mixed
document into four files in one move.

## Review and Finish

1. Settle the document's claims, type, examples, and organization.
2. Check it against the list below, and report structural defects before any prose edit.
3. Run the reader-ready pass over the complete draft and resolve every defect it finds.
4. Repeat that pass after each material revision, because a revision can introduce a defect.

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
- every pin is one the evidence recorded, and every cited source is one the reader can open;
- the procedure still works with every note deleted, and each warning or caution matches its risk; and
- accessibility information and recovery guidance cover what the reader needs.

A document is **reader-ready** when one complete reading pass, as its intended reader, confirms that:

- the intended reader can say, after one reading, what the document wants them to know or do;
- each section and paragraph leads with the point the reader needs;
- explanations precede the terms, conclusions, and instructions that depend on them;
- relationships between claims are stated rather than left for the reader to rebuild;
- every sentence is within its limit, and none fails the deletion test;
- every unfamiliar term or identifier has its meaning at first use; and
- every supported claim, number, condition, qualification, and normative requirement survived.

Check each replacement as well as the defect it removed. A rewrite can arrive in the passive or drop a number.
Run `writing-for-humans`' reader-ready pass on the same draft; it carries the AI-writing diagnostics.

The reader-ready pass shows that the document should work, not that its readers can use it. ISO 24495-1
completes the usable principle by evaluating a document with its readers and in use. When a document guides
consequential action, recommend that test. Give a person from the intended readership, or a subagent holding
only the document, a real task. Record where they fail.

A subagent run is a proxy for reader testing, not a substitute. State in the delivery which evaluation the
document received.

When reviewing a high-stakes document, or delegating any review or readability pass to a subagent, read
[references/review-sequence.md](references/review-sequence.md) first.

The document is complete when it is reader-ready and every remaining evidence gap is visible in the delivery.

## Response Modes

- **Draft:** produce the document in its selected type.
- **Review:** report missing context, type leaks, structural problems, inaccurate examples, accessibility gaps,
  and unclear recovery before suggesting edits.
- **Condense:** remove noise and misplaced content, judging each passage by what it gives the reader rather
  than by its section's label. Keep reader-critical context, decisions, prerequisites, examples, caveats, and
  recovery.
- **Expand:** add confirmed context, examples, constraints, or recovery, never invented ones.

For an existing file, return text or a diff unless the user asked for an in-place edit.
