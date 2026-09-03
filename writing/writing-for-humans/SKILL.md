---
name: writing-for-humans
description: "Write, edit, or review English technical prose; preserve claims and voice, match an established style, and actively remove AI-writing artifacts. Use for documentation, reports, issues, commits, and user-facing errors. Not for document structure, fiction, poetry, marketing, or ordinary chat."
license: MIT AND CC-BY-4.0
metadata:
  author: Joonas Onatsu
---

# Writing for Humans

Use this skill for prose-level decisions in English technical writing. Use `technical-writing` as well when the
task includes document purpose, organization, examples, or document type.

This skill does not govern fiction, poetry, marketing, narrative nonfiction, quotations, or ordinary chat.

## Establish the Constraints

Identify the audience, artifact, repository conventions, and requested voice before drafting or editing.
Introduce concepts before relying on them, and define unfamiliar terms and abbreviations before use.

When editing supplied prose, preserve every supported claim, distinction, qualification, and normative
requirement. Do not invent facts, actors, dates, numbers, causes, citations, opinions, or personality.

Flag unsupported assertions, ambiguity, missing prerequisites, and factual gaps. Do not silently remove them.

When editing a file, change prose only. Preserve code blocks, inline code, frontmatter, link targets, table
syntax, identifiers, commands, and quotations unless the user explicitly includes them in scope. AI-writing
artifacts are production residue and are the exception: remove confirmed marks without changing the surrounding
content.

## Preserve Voice and Established Style

Use a supplied writing sample as the voice target. Preserve its appropriate formality, person, terminology,
and degree of personality. Do not flatten a distinctive voice or introduce a viewpoint, humor, or familiarity
the source does not contain.

For a requested author or house style, use representative exemplars from the same document type. One exemplar
supports voice matching; require two or more before inferring repeatable conventions.

Record a compact style profile:

- the covered document types and audience;
- repeated structure, register, formatting, and terminology conventions;
- exemplar evidence for each convention; and
- aspects the profile does not govern.

Apply only supported conventions. Repository requirements outrank the profile, and the source author's voice
governs wherever the profile is silent.

## Write Clear Technical Prose

Prefer active voice when the actor is known and relevant. Use concrete, specific terms and plain English.
Remove needless words, hedges, clichés, prefabricated phrases, and empty promotion.

Use one consistent term per concept. Do not rotate synonyms or redefine abbreviations.

State affirmative claims directly. Avoid rhetorical forms such as “X, not Y” and “not just X, but Y.” Do not
use em or en dashes unless a language construct requires them.

In sentences and paragraphs:

- use parallel grammatical form for coordinate ideas;
- keep subjects near verbs and modifiers near their referents;
- place new or important information last when that improves emphasis;
- split sentences over 30 words unless splitting reduces clarity;
- vary sentence length;
- keep one clear topic per paragraph;
- change paragraphs when the topic, purpose, speaker, or argumentative stage changes;
- keep tense consistent unless the time relationship changes; and
- use paragraphs for connected ideas and bullets for genuine lists.

Avoid repeated sentence openings, formulaic transitions, manufactured revelations, and routine concluding
sentences that merely restate the paragraph.

## Apply Artifact-Specific Rules

For requests, handoffs, operational notices, executive summaries, and decision summaries, lead with the
action, result, decision, or state. Name the owner and deadline when relevant.

Follow the repository's heading convention. Otherwise, use title case.

Follow the repository's Markdown line-length rules. Otherwise, wrap prose near 120 characters at phrase or
clause boundaries without orphaning a sentence's final word.

In formal documents, prefer full forms such as “it is,” “does not,” and “cannot.” Terse commits and error
messages may use shorter forms.

Formal factual claims require verifiable evidence or citations. Label unverifiable claims as unverified and
disclose them when delivering the work.

## Remove AI-Writing Marks

Remove AI-writing artifacts whenever they appear. They are production residue and do not belong to the
author's voice.

Act immediately on definitive artifacts:

- chat residue and assistant-facing language;
- meta-commentary that merely announces the text;
- empty promotional language;
- canned transitions and repeated rhetorical setups;
- manufactured revelations or concluding slogans;
- false agency that hides an identifiable actor; and
- invisible characters or metadata introduced to mark AI-generated text.

Rewrite the affected passage while preserving its claims, qualifications, normative force, and intended voice.
Remove confirmed invisible marks without changing visible text. Remove format metadata only when its purpose as
an AI-origin marker is established; preserve legitimate accessibility, authorship, interoperability, and
application metadata.

Treat weak signals such as one dash, adverb, transition, or rhetorical question as prompts to inspect the
surrounding passage. A weak signal alone does not establish an AI-writing artifact.

Load `references/diagnostics.md` for a long draft, difficult diagnosis, or final cleanup scan. Use its patterns
as evidence, not as a mechanical word blocklist.

## Deliver the Result

Before delivery, scan the completed prose for AI-writing artifacts and remove every confirmed mark.

For a rewrite, return the edited text or requested file change.

For a review, separate:

- proposed prose edits;
- factual, structural, or missing-context issues requiring author input; and
- passages left unchanged because their evidence or intended voice is unclear.

Clarity may override stylistic defaults when following them would make the prose awkward, misleading, or less
precise. Scope, factual accuracy, evidence, and claim preservation remain binding.
