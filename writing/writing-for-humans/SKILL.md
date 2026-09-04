---
name: writing-for-humans
description: "Write, edit, or review technical prose at the sentence and paragraph level in any language, defaulting to English; preserve claims and the author's voice, and actively remove AI-writing artifacts. Use for documentation, reports, issues, commits, agent instructions, and user-facing errors. Not for document structure or house style, which is writing-documentation, and not for fiction, poetry, marketing, or ordinary chat."
license: MIT AND CC-BY-4.0
metadata:
  author: Joonas Onatsu
---

# Writing for Humans

Use this skill for prose-level decisions in technical writing. Its unit is the sentence and the paragraph, and
it applies to any prose: documentation, reports, issues, commits, agent instructions, rule files, and
user-facing errors.

Write in the language the request, the surrounding text, or the audience establishes. English is the default
when nothing establishes another, and it is the language this skill's examples and diagnostics are drawn from.

Most rules here are language-general: one term per concept, one topic per paragraph, lead with the point,
preserve the claim, cut what carries no meaning. Some are English conventions, and they are marked where they
appear. **In another language, that language's own conventions govern typography, punctuation, capitalization,
heading style, and register.** Do not carry an English convention into a language that does not share it, and
say which convention you applied when the choice is not obvious.

Use `writing-documentation` as well when the task includes a document's purpose, organization, examples,
document type, or the house style of a documentation set it joins.

This skill does not govern fiction, poetry, marketing, narrative nonfiction, quotations, or ordinary chat.

## Establish the Constraints

Identify the artifact, repository conventions, and requested voice before drafting or editing. Introduce
concepts before relying on them, and define unfamiliar terms and abbreviations before use.

When editing supplied prose, preserve every supported claim, distinction, qualification, and normative
requirement. Do not invent facts, actors, dates, numbers, causes, citations, opinions, or personality.

Flag unsupported assertions and ambiguity rather than resolving them silently.

When editing a file, change prose only. Preserve code blocks, inline code, frontmatter, link targets, table
syntax, identifiers, commands, and quotations unless the user explicitly includes them in scope. AI-writing
artifacts are production residue and are the exception: remove confirmed marks without changing the surrounding
content.

## Preserve the Author's Voice

Use a supplied writing sample as the voice target. Preserve its appropriate formality, person, terminology,
and degree of personality. Do not flatten a distinctive voice or introduce a viewpoint, humor, or familiarity
the source does not contain.

Voice preservation constrains editing; it does not protect everything in the source. AI-writing artifacts are
production residue rather than voice, so artifact removal outranks voice preservation wherever the two
conflict. Rewrite the passage and keep the author's register; do not defend an artifact as a stylistic choice.

Matching the conventions of an existing documentation set is a document-level job. Use `writing-documentation`
for that.

## Write Clear Technical Prose

Prefer active voice when the actor is known and relevant. Use concrete, specific terms and plain language.
Remove needless words, hedges, clichés, prefabricated phrases, and empty promotion.

Use one consistent term per concept. Do not rotate synonyms or redefine abbreviations.

State affirmative claims directly. Avoid rhetorical forms such as “X, not Y” and “not just X, but Y,” and
their equivalents in the target language.

Do not use em or en dashes. The only exception is a construct whose grammar requires the character itself,
such as an en dash in a numeric or date range. A dash that joins, separates, or dramatizes two statements is
not such a construct: name the relation or write two sentences. This holds in every language. Where a language
uses a dash for a purpose English does not, such as marking dialogue, that use is a required construct and is
permitted; wanting the effect is not.

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

For requests, handoffs, and short operational messages, lead with the action, result, decision, or state.
Name the owner and deadline when relevant. `writing-documentation` carries the same rule for decision records,
change notes, and executive summaries.

Follow the repository's heading convention and Markdown line-length rules. When a repository sets neither,
wrap prose at phrase or clause boundaries without orphaning a sentence's final word, and use title case for
English headings. Title case is an English convention: in another language use that language's heading
convention, which is usually sentence case.

In formal English documents, prefer full forms such as “it is,” “does not,” and “cannot.” Terse commits and
error messages may use shorter forms. In another language, apply the equivalent register distinction that
language draws between formal and terse writing rather than looking for contractions it may not have.

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

**The categories of AI-writing artifact carry across languages; the words that signal them do not.** Chat
residue, meta-commentary, empty promotion, canned transitions, manufactured revelation, and false agency all
appear in any language a model generates. Their lexical signatures are specific to each one, and a model's
tells in one language are not translations of its tells in another. Outside English, diagnose by category and
derive the signatures from the text in front of you. Do not translate an English tell and search for the
result, and do not report a passage as clean merely because the English markers are absent.

Load `references/diagnostics.md` for a long draft, difficult diagnosis, or final cleanup scan. Its categories
apply to any language; its example strings are English. Use its patterns as evidence, not as a mechanical word
blocklist.

## Deliver the Result

Before delivery, scan the completed prose for AI-writing artifacts and remove every confirmed mark.

For a rewrite, return the edited text or requested file change.

For a review, separate:

- proposed prose edits;
- factual, structural, or missing-context issues requiring author input; and
- passages left unchanged because their evidence or intended voice is unclear.

Clarity may override stylistic defaults when following them would make the prose awkward, misleading, or less
precise. Scope, factual accuracy, evidence, and claim preservation remain binding.
