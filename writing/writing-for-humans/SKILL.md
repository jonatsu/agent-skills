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

Write inclusively. Do not use a gender-specific pronoun for a person whose pronouns the text does not state,
and do not infer them from a name. Use "they". Use a gendered term for a role or person only where the subject
genuinely requires it.

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

## Classify the Passage First

Every passage is procedural or descriptive, and the distinction sets the sentence-length limit. Decide before
you edit.

|           | Procedural                   | Descriptive                        |
| --------- | ---------------------------- | ---------------------------------- |
| Job       | Tells the reader what to do  | Explains what something is or does |
| Verb form | Imperative                   | Simple present, past, or future    |
| Limit     | **20 words per sentence**    | **25 words per sentence**          |
| Unit      | One instruction per sentence | One topic per paragraph            |

This is a property of the passage, not of the document. A how-to guide still contains descriptive explanation,
and a commit message still contains instructions. Classify what is in front of you.

Do not mix the two inside one vertical list.

**Counting words.** A code span, an identifier, quoted text, a heading, and a title each count as one word,
however long. In a vertical list, the lead-in and each item carry their own limit rather than summing: the
colon closes the lead-in as a period would.

The limits bind everywhere this skill applies, commit bodies and error messages included. A tighter external
constraint governs instead where one exists, such as the 72-character Conventional Commits subject. Verbatim
text is never edited to fit a limit; the rule against altering quotations already protects it.

## Write Clear Technical Prose

Prefer active voice when the actor is known and relevant. Use concrete, specific terms and plain language.
Remove needless words, hedges, clichés, prefabricated phrases, and empty promotion.

Express an action with a verb rather than a noun built from one. Write "analyze the log", not "perform an
analysis of the log".

Use one consistent term per concept. Do not rotate synonyms or redefine abbreviations.

State affirmative claims directly. Avoid rhetorical forms such as “X, not Y” and “not just X, but Y,” and
their equivalents in the target language.

Prefer simple tenses. **Keep a compound tense where it carries information the simple form cannot.** "The job
has finished" asserts a current relevance that "the job finished" drops, and losing that changes the claim
rather than the style. Drop the compound form only when the simple one says the same thing.

Do not use an "-ing" form as a verb. The common case is a participial clause hung off a comma, as in "…, making
it easy to configure", which becomes its own sentence. An "-ing" word is fine as a noun or inside a compound
noun: "logging", "the mounting bracket".

Keep a noun cluster to three words, breaking a longer one with a preposition: "the timeout value for the
connection pool", not "the connection pool timeout configuration value".

Do not use em or en dashes. The only exception is a construct whose grammar requires the character itself,
such as an en dash in a numeric or date range. A dash that joins, separates, or dramatizes two statements is
not such a construct: name the relation or write two sentences. This holds in every language. Where a language
uses a dash for a purpose English does not, such as marking dialogue, that use is a required construct and is
permitted; wanting the effect is not.

In sentences and paragraphs:

- use parallel grammatical form for coordinate ideas;
- keep subjects near verbs and modifiers near their referents;
- place new or important information last when that improves emphasis;
- split a sentence over its limit unless splitting reduces clarity;
- vary sentence length;
- give a paragraph one topic, open it with the sentence that states that topic, and keep it to six sentences;
- change paragraphs when the topic, purpose, speaker, or argumentative stage changes;
- keep tense consistent unless the time relationship changes; and
- use paragraphs for connected ideas and bullets for genuine lists.

In procedural text, write one instruction per sentence. Two actions share a sentence only when they happen at
the same time, or when the second is the immediate result of the first.

**State a required condition before the command it governs, separated by a comma.** Write "If the build fails,
read the log", never "Read the log if the build fails". A reader who meets the condition after the instruction
has already acted on it.

Do not drop a noun, verb, subject, or article to shorten a sentence. "Rotary switch to INPUT" is shorter and
ambiguous. Meet the limits above by splitting sentences, never by compressing grammar out of them.

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
