---
name: writing-for-humans
description: "Write, edit, shorten, or review technical prose at the sentence and paragraph level in any language, defaulting to English, preserving every claim and the author's voice and removing AI-writing artifacts. Use for documentation, specs, PRDs, and design documents, reports, issues, commit messages, user-facing errors, and readability or de-bloat passes. Not for document structure or type (writing-documentation), agent instruction files (writing-for-agents), or fiction, poetry, marketing, or chat."
license: MIT AND CC-BY-4.0
metadata:
  author: Joonas Onatsu
---

# Writing for Humans

This skill owns the sentence and the paragraph: whether each sentence adds something the reader needs, and
whether the reader can take it in on the first pass. `writing-documentation` owns the document around them: its
type, what belongs in it, and where each concept is explained. A spec, PRD, or design document needs both
skills, and the skill that owns its content as well.

Write in the language the request, the surrounding text, or the audience establishes, and default to English.
The rules are language-general unless marked as an English convention. In another language, that language's
own conventions govern typography, punctuation, capitalization, heading style, and register.

## Guardrails

These bind every draft, edit, and review, and every other rule yields to them.

**Preserve every claim.** When editing supplied prose, keep every supported claim, distinction, condition,
exception, qualification, and normative requirement. Invent no fact, actor, date, number, cause, citation,
opinion, or personality. Flag an unsupported assertion or an ambiguity rather than resolving it silently. A gap
stays a gap: "the sources do not say" is a complete sentence, and a plausible guess written after it is a
fabrication.

**Do the requested task only.** A review reports; it does not rewrite. Shortening removes text that carries
nothing; it does not drop a condition or a citation. Polishing does not restructure. When the requested depth is
unclear, make the smallest edit that answers the request.

**Write the relation the source supports.** Where the evidence shows only sequence or co-occurrence, write
"coincided with" or "was followed by", never "caused". Where the source is specific, write the specific
relation: "the timeout bounds the retry", never "the timeout is related to the retry". Keep vague wording only
where the source itself is vague.

**Keep quotations exact.** Keep each quotation visibly quoted and separate. Never repair one silently or use an
ellipsis to change what the speaker claimed.

**Edit prose only.** Leave code blocks, inline code, frontmatter, link targets, table syntax, identifiers,
commands, and quotations as they are unless the user includes them in scope. Confirmed AI-writing artifacts are
the exception, below.

**Write inclusively.** Use "they" for a person whose pronouns the text does not state, and never infer pronouns
from a name. Use a gendered term only where the subject requires it.

## Style and Voice

The default style is this skill plus the repository's own conventions. It applies whenever nothing else is
established, which is most of the time.

When you edit someone else's prose, keep their register and terminology and add no personality the source lacks.
That limits your edits; it does not protect a defect.

Voice matching overrides the default only with an explicit request and at least one sample. If the sample is
missing, ask for one. Match the sample's formality, person, terminology, and degree of personality. AI-writing
artifacts are never voice, so removing them outranks matching.

## Classify the Passage

Every passage is procedural or descriptive, and the class sets its sentence limit. Classify the passage in front
of you, not the document: a how-to guide contains explanation, and a commit message contains instructions.

|           | Procedural                   | Descriptive                        |
| --------- | ---------------------------- | ---------------------------------- |
| Job       | Tells the reader what to do  | Explains what something is or does |
| Verb form | Imperative                   | Simple present, past, or future    |
| Limit     | **20 words per sentence**    | **25 words per sentence**          |
| Unit      | One instruction per sentence | One topic per paragraph            |

The limits are ceilings, and they bind commit bodies and error messages too. Split a sentence over its limit
unless splitting makes it less clear. A tighter external limit, such as a 72-character commit subject, governs
where one exists. Never edit verbatim text to fit.

Count a code span, identifier, quotation, heading, or title as one word. In a vertical list, the lead-in and each
item carry their own limit, because the colon closes the lead-in as a period would. Keep procedural and
descriptive items in separate lists.

## Cut Noise

**Noise** is any statement that gives the reader nothing new or useful at the point where they meet it. Judge a
sentence in its context, never in isolation: ask what it adds for a reader who has read everything before it and
reads for this text's purpose. Apply the deletion test. Remove the sentence, and if the reader loses nothing they
need there, it was noise. A true, well-formed sentence is still noise when its context already carries it.

Three forms recur in drafted prose:

- **Restated context:** a fact the text already established, such as repeating the version or scope its opening
  set. State scope once, where the text opens.
- **Process residue:** how the writer checked the text, such as "verified against U-Boot v2026.01", "as
  confirmed in the source", or "checked on the target". Write the checked fact. Where the reader needs the
  source, name it once, in a source line or a citation.
- **A self-cancelling claim:** a statement followed in the same sentence by its retraction, or by a hedge that
  empties it. Write the claim at the strength the evidence supports, with its real limit stated as a condition.

Filler clauses, announcements, restating closers, and most AI-writing artifacts below are noise too. Apply the
test to each clause as well as each sentence.

## Sentences

**Lead with the information.** State the claim, action, or result first, and put new or important information
at the end of the sentence. Keep the subject near its verb and a modifier near what it modifies.

**Use the verb that carries the meaning.** Write "analyze the log", not "perform an analysis of the log". Use
"is", "are", and "has" where they are the true verb: "`config.py` validates configuration", not "`config.py`
serves as the validation layer". Prefer active voice when the actor is known and relevant.

**Name the mechanism.** "The security module releases the key only when the measurements match" beats "measured
boot seals the key release". Test each sentence by asking whether the reader could act on it.

**Keep every word the grammar needs.** Keep articles, "that", subjects, and verbs. "Rotary switch to INPUT" is
shorter and ambiguous. Meet a limit by splitting the sentence, never by compressing its grammar.

**Put a condition before its command.** Write "If the build fails, read the log", with a comma after the
condition. A reader who meets the condition after the instruction has already acted.

**Write one instruction per procedural sentence.** Two actions share a sentence only when they happen together,
or when the second is the immediate result of the first.

**Give each concept one term.** Define a term or abbreviation on first use, never rotate synonyms, and never
redefine an abbreviation. Prefer the precise technical term over shorthand, metaphor, or jargon.

**Link clauses by their real relation.** Put a cause, condition, or qualification in a subordinate clause. Give
equal ideas parallel clauses. Join two clauses with a colon or a semicolon only where the second explains or
turns on the first. Never chain semicolons: a sentence that needs two becomes two sentences. The exception is an
inline list whose items contain commas.

**Prefer simple tenses.** Keep a compound tense where it carries information: "the job has finished" asserts a
current relevance that "the job finished" drops.

**Use "-ing" words as nouns only.** A participial clause hung off a comma ("…, making it easy to configure")
becomes its own sentence. "Logging" and "the mounting bracket" are fine.

**Keep a noun cluster to three words.** Break a longer one with a preposition: "the timeout value for the
connection pool", not "the connection pool timeout configuration value".

**Backtick identifiers, not concepts.** Commands, file names, configuration symbols, and versions (`dm-verity`,
`v2026.01`) are code. Concepts (secure boot, initramfs) stay prose, and a codename beside a version stays bare.

**Lead with the meaning, then the key.** An internal identifier names a fact without carrying it. Write "Keep
cached values for five minutes (decision A-003)", not "A-003 is confirmed". A question restates the concrete
choice rather than its key. A commit hash comes with its subject, and a file reference with the claim it
supports. Omit a key the reader does not need.

**State claims directly.** Write the affirmative claim rather than "not X but Y" against a claim nobody made.

**Choose the plain word.** Cut hedges, clichés, empty promotion, and prefabricated phrases. In formal English
documents, write full forms such as "it is" and "does not". Terse commits and error messages may contract.

**Replace the em dash.** Write the version without it first: a comma, colon, semicolon, parentheses,
conjunction, or full stop. Keep the dash only when that version loses a distinction you can state in words.
Never pair dashes as parentheses or use two in one paragraph. In someone else's prose, an existing dash is the
author's: rewrite it only when the passage shows it dodged a relation. Ranges and dashes a language requires
grammatically fall outside this rule.

## Paragraphs, Lists, and Emphasis

**Give a paragraph one topic,** opened by the sentence that states it, and at most six sentences. Change
paragraphs when the topic, purpose, speaker, or argumentative stage changes. Vary sentence length. Keep tense
consistent unless the time relationship changes.

**Open sentences differently.** Two or more sentences in a paragraph never open with the same word, and none
opens with "Additionally", "Furthermore", "Moreover", or "In addition". Name the real relation instead, or none.

**Use prose for connected ideas and lists for discrete items.** Fold items that depend on each other into
sentences. Never write a run of very short bullets. Give list items parallel grammatical form.

**Count a list of three.** Three is the length a model reaches for when content has no length of its own. Check
that each item adds something the others do not, then merge them, develop the strongest, or let the list be two
or four.

**Spend bold as a budget.** Bold reads as strong only against plain text around it. Bold the shortest span
carrying a decision, and prefer restructuring to a longer bold run. Never use bold as a lead-in or decoration,
and never give every list item a bold label. In someone else's prose, dense emphasis prompts inspection, not
stripping.

**Open a section with new information.** A "Performance" heading followed by "Speed matters." spends a line on
the heading.

**Describe what the subject does now,** not what it replaced. Changelogs, release notes, migration guides, and
decision records are the exceptions, because change is their subject.

**Follow the repository's heading and line-length conventions.** Where none exists, wrap at phrase or clause
boundaries and use title case for English headings. Other languages usually use sentence case.

**Support formal claims with evidence.** Cite a verifiable source, or label the claim as unverified and say so
at delivery.

## Shorten by Removing Noise

Shortening removes noise, as defined above. Readability is the target, never word count. A dense technical text
often shortens little, because most of its length is content. The remaining lever is structural, which is the
author's decision.

Besides the three recurring forms, the usual noise is a filler clause ("is documented in", "as described above",
"it is worth noting"), a closer that restates its paragraph, and a sentence announcing the next one.

Split sentences while shortening, and never merge them. Merging short sentences into a semicolon chain saves
words and makes the text denser. Protect every word that carries a limit, condition, exception, or
qualification: a length target reaches for exactly those first.

## Remove AI-Writing Artifacts

Remove AI-writing artifacts wherever they appear. They are production residue, never the author's voice.

**One account covers most of them: the sentence signals that a point matters instead of adding to it.** That makes
it noise, and the deletion test finds it: cut the sentence whose only contribution is "emphasis".
Reach for this account when a passage reads wrong but matches nothing listed.

Act on one sighting of:

- chat residue, assistant-facing language, and meta-commentary announcing the text;
- empty promotion, canned transitions, manufactured revelations, and concluding slogans;
- a negative half nobody claimed ("not just X, but Y"), unless it corrects a belief the reader holds;
- an aphorism standing in for the claim ("at its core", "the real question is");
- a run-up announcing the point ("here's the thing") or an objection nobody raised ("to be clear");
- process residue reporting how the writer checked the text;
- false agency hiding an actor the source can name;
- unresolved placeholders ("TBD", "[insert source]") and leaked tool or citation tokens ("oaicite"); and
- invisible characters or metadata inserted to mark AI-generated text.

Rewrite the passage while keeping its claims, qualifications, normative force, and voice. Remove a confirmed
invisible mark without changing visible text, and keep legitimate accessibility, authorship, and application
metadata.

Treat one dash, adverb, transition, rhetorical question, bold run, stacked qualifier, or repeated opening as a
prompt to inspect the
passage, not as a finding. Several sharing a passage are a finding. **Surface style is never evidence of
authorship:** settle that question from draft history, revision history, or disclosed AI use.

Outside English, diagnose by category and derive the signatures from the text. A model's tells in one language
are not translations of its tells in another.

Load [references/diagnostics.md](references/diagnostics.md) for a long draft, a difficult diagnosis, or the final
scan; its categories apply to any language and its examples are English. Load
[references/rewrites.md](references/rewrites.md) when the size of an edit is the question rather than its
target.

## Deliver a Reader-Ready Result

A result is **reader-ready** when one complete reading pass, as its intended reader, confirms that:

- each section and paragraph leads with the point the reader needs;
- explanations precede the terms, conclusions, and instructions that depend on them;
- relationships between claims are stated rather than left for the reader to rebuild;
- every sentence is within its limit, and none fails the deletion test;
- every unfamiliar term or identifier has its meaning at first use;
- every confirmed AI-writing artifact is gone; and
- every supported claim, condition, qualification, and normative requirement survived.

When a condition fails, revise the passage and run the complete pass again, because a revision can introduce a
defect. **Check each replacement, not only the defect it removed:** a rewrite of a key-first opener can arrive
in the passive, and a merged triad can drop a number. Then search once more for the five marks that most often
survive: a not-X-but-Y contrast, a restating closer, an em dash, an unearned triad, and a bold run. Name the
most repeated visible move, and inspect it when it appears three or more times or dominates two consecutive
paragraphs; a repeated move that carries the argument stays.

**Leave a working sentence alone.** A limit is a ceiling, not a quota of edits. Check for over-correction as
well: fabricated informality, variation for its own sake, and roughness added to look handmade.

For a rewrite, return the edited text or file change with no change summary, self-review, or confidence
statement unless asked. For a review, separate proposed prose edits, issues that need the author's input, and
passages left unchanged because their evidence or intended voice is unclear.

Clarity may override a stylistic default that would make the prose awkward, misleading, or less precise. The
guardrails always bind.
