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

**Do not substitute a neighboring task.** A review does not authorize a rewrite. Shortening does not authorize
dropping a condition, exception, citation, or qualification. Polishing does not authorize restructuring. When
the requested depth is unclear, make the smallest edit that answers the request.

Keep a direct quotation exact and visibly quoted. Do not merge separate quotations into one, repair a quotation
silently, or use an ellipsis to change what the speaker claimed.

Write inclusively. Do not use a gender-specific pronoun for a person whose pronouns the text does not state,
and do not infer them from a name. Use "they". Use a gendered term for a role or person only where the subject
genuinely requires it.

Flag unsupported assertions and ambiguity rather than resolving them silently.

**Do not assert a cause the source does not support.** Where the evidence shows only sequence or
co-occurrence, write the weaker relation it does support: "coincided with", "appeared alongside", "was followed
by". Cut the relation when even that overstates it. This binds an edit as much as a draft, because promoting
"associated with" to "caused" changes the claim rather than the wording.

**Name a relation the source does state.** Those same weak words are a defect in the opposite direction when
the source is specific. "Associated with", "linked to", "tied to", and "connected with" hide whether someone
chaired the board, consulted for a month, or filed one patch; "the timeout is related to the retry setting"
hides whether it bounds the retry, is derived from it, or merely sits nearby. Write the relation the source
gives. Keep the vague wording only where the source is genuinely vague, and never resolve the vagueness by
inventing the specific.

When editing a file, change prose only. Preserve code blocks, inline code, frontmatter, link targets, table
syntax, identifiers, commands, and quotations unless the user explicitly includes them in scope. AI-writing
artifacts are production residue and are the exception: remove confirmed marks without changing the surrounding
content.

## Set the Style

**The default style is the rest of this skill, plus the repository's own conventions.** Apply it whenever
nothing else is established, which is most of the time. Do not look for a voice to match before you write.

When you edit prose someone else wrote, keep their register and their terminology, and add no personality the
source does not contain. That is a limit on your edits, not a style target. A defect stays a defect, and a
padded passage does not become correct because its author wrote it that way.

**Voice matching is an override, and it needs two things: an explicit request, and at least one sample.**
Without both, apply the default and say nothing about voice. If the request arrives without a sample, ask for
one. Do not infer a voice target from the surrounding text, from the repository, or from what the author seems
to prefer.

Given both, use the sample as the target. Match its formality, person, terminology, and degree of personality.
One sample supports matching a voice. Inferring a repeatable convention needs two or more.

Voice never protects everything in the source. AI-writing artifacts are production residue rather than voice,
so artifact removal outranks voice matching wherever the two conflict. Rewrite the passage and keep the
author's register; do not defend an artifact as a stylistic choice.

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

Use "is", "are", and "has" where they are the true verb. "Serves as", "stands as", "functions as",
"represents", "boasts", and "features" replace a plain verb with a longer one that adds no information:
"`config.py` serves as the validation layer" is "`config.py` validates configuration", and "the release
boasts four new commands" is "the release adds four commands".

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

**Do not reach for an em dash.** It always has an alternative, and the alternative names the relation the dash
leaves implicit. Before keeping one, write the version without it: a comma, colon, semicolon, parentheses,
conjunction, subordinate clause, or full stop. Keep the dash only when that version loses a distinction you can
state in words. Wanting the effect is not such a loss, and neither is preferring the rhythm.

Never pair em dashes as parentheses, and never use two in one paragraph. Density is the signal a reader
actually detects, and a single justified dash is not it.

This default holds in every language, because the failure it prevents is a hidden relation rather than an
English typographic habit.

**In prose someone else wrote, an existing dash is the author's.** Treat it as a weak signal that prompts
inspection of the passage, not as an artifact to strip on sight. Rewrite it only when the passage shows the
relation was genuinely dodged.

An en dash in a numeric or date range falls outside this rule, as does a dash a language requires as a
grammatical construct, such as marking dialogue. Use those where that language uses them.

**Count a list of three before keeping it.** Three is the length a model reaches for when the content has no
length of its own, so the triad arrives by rhythm: "keynotes, panels, and networking opportunities", or three
parallel examples where one carries the point, or three short facts followed by a lesson. Check that each item
adds something the others do not. Merge them, develop the strongest, or let the list be two or four when that
is what the subject has. The parallel-form rule below governs a list the content earned; it does not license
padding one out to three.

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

**Name the most repeated visible move before delivering.** Inspect it when it appears three or more times, or
when it dominates two consecutive paragraphs. Inspection may end in no change: a repeated move that carries the
argument stays.

## Apply Artifact-Specific Rules

For requests, handoffs, and short operational messages, lead with the action, result, decision, or state.
Name the owner and deadline when relevant. `writing-documentation` carries the same rule for decision records,
change notes, and executive summaries.

Follow the repository's heading convention and Markdown line-length rules. When a repository sets neither,
wrap prose at phrase or clause boundaries without orphaning a sentence's final word, and use title case for
English headings. Title case is an English convention: in another language use that language's heading
convention, which is usually sentence case.

Do not open a section with a sentence that restates its heading. A "Performance" heading followed by "Speed
matters." spends a line on what the heading already said. Begin with the first thing the reader does not
know.

Describe what the artifact does now, not what it replaced. A comment, docstring, or reference page written
against the previous approach dates itself the moment the next change lands, and a later reader cannot tell
whether the comparison still holds. Change logs, release notes, migration guides, and decision records are
the documents whose subject is change, and are the exception.

**Emphasis is relative, so bold is a budget rather than a tool.** A bold span reads as strong only because
the text around it is not, and a page where every paragraph carries one has no emphasis left, just texture.
Before adding a mark, look at what is already bold within a screen of it and decide which one the reader most
needs. Prefer the shortest span that carries the decision, and prefer restructuring over a longer bold run:
a heading, a shorter paragraph, or the point moved to the front of the sentence.

Do not give every item in a vertical list a bold label. A label earns its bold where the reader scans for it
and the labels differ in kind. Where a label restates the opening words of its own item, delete the bold or
turn the list into prose.

**In prose someone else wrote, the existing emphasis is the author's.** The same write-versus-edit asymmetry
applies here as to the em dash: density is a prompt to inspect the passage, not a licence to strip marks on
sight.

In formal English documents, prefer full forms such as “it is,” “does not,” and “cannot.” Terse commits and
error messages may use shorter forms. In another language, apply the equivalent register distinction that
language draws between formal and terse writing rather than looking for contractions it may not have.

Formal factual claims require verifiable evidence or citations. Label unverifiable claims as unverified and
disclose them when delivering the work.

## Remove AI-Writing Marks

Remove AI-writing artifacts whenever they appear. They are production residue and do not belong to the
author's voice.

**One account covers most of them: the sentence signals that a point matters instead of adding to it.** A
model continues with what fits the widest range of readers and subjects, and staging fits everywhere. Reach
for the account rather than the lists when a passage reads wrong but matches nothing below. Ask what each
sentence gives a reader who has already read the one before it, and cut the sentence whose answer is
"emphasis".

Act immediately on definitive artifacts:

- chat residue and assistant-facing language;
- meta-commentary that merely announces the text;
- empty promotional language;
- canned transitions and repeated rhetorical setups;
- manufactured revelations or concluding slogans;
- false agency that hides an identifiable actor;
- unresolved placeholders such as "[insert source]", "TK", "TBD", or "202X";
- leaked tool, interface, and citation tokens such as "turn0search0", "oaicite", or "contentReference"; and
- invisible characters or metadata introduced to mark AI-generated text.

Act on one sighting of these structural moves as well. Each stages a point rather than making it, and none
needs a second signal to justify a rewrite:

- a negative half nobody claimed, as in "not just X, but Y" or "this is not X, it is Y", including the form
  split across two sentences and the clipped tail ("…, no guessing"). Keep the contrast where the negative
  half corrects a belief the reader holds, or where both halves carry information;
- a closer that restates the paragraph above it, a one-line dramatic fragment, or the same sign-off after
  every section;
- an aphorism standing in for the claim: "the real question is", "at its core", "what really matters", "X is
  the Y of Z", "the architecture of". Write the specific claim instead;
- a run-up that announces the point instead of making it, including staged candour: "let's dive in", "here's
  what you need to know", "here's the thing", a standalone "Honestly?";
- an objection or alternative nobody raised: "to be clear", "don't get me wrong", "a tempting approach would
  be", "you might think… but". These are usually leftovers from an earlier draft. Keep an objection the text
  attributes and answers, and an option a reader would genuinely weigh; and
- a gap filled with a plausible guess. "The sources do not say" is an acceptable sentence. "It likely began
  in the 1990s", written straight after admitting no source exists, is a fabrication wearing a hedge. Cut the
  guess or state the gap, and remove knowledge-cutoff disclaimers with it.

Rewrite the affected passage while preserving its claims, qualifications, normative force, and intended voice.
Remove confirmed invisible marks without changing visible text. Remove format metadata only when its purpose as
an AI-origin marker is established; preserve legitimate accessibility, authorship, interoperability, and
application metadata.

Treat weak signals as prompts to inspect the surrounding passage rather than as findings. One dash, adverb,
transition, rhetorical question, bold run, stacked qualifier, or repeated sentence opening does not establish
an AI-writing artifact; several sharing a passage do.

**Surface style is not evidence of authorship.** A dash, a semicolon, a clean paragraph, or a word from any
diagnostic list says nothing about who wrote the text. Settle an authorship question from draft history,
revision history, source traces, or disclosed AI use. The marks in this skill exist to improve prose, never to
decide who produced it.

**The categories of AI-writing artifact carry across languages; the words that signal them do not.** Chat
residue, meta-commentary, empty promotion, canned transitions, manufactured revelation, and false agency all
appear in any language a model generates. Their lexical signatures are specific to each one, and a model's
tells in one language are not translations of its tells in another. Outside English, diagnose by category and
derive the signatures from the text in front of you. Do not translate an English tell and search for the
result, and do not report a passage as clean merely because the English markers are absent.

Load `references/diagnostics.md` for a long draft, difficult diagnosis, or final cleanup scan. Its categories
apply to any language; its example strings are English. Use its patterns as evidence, not as a mechanical word
blocklist.

Load `references/rewrites.md` when the size of an edit is the question rather than its target. It works this
skill's rules through paired before-and-after passages of technical prose, which is what settles how far to
cut once a mark is identified.

## Deliver a Reader-Ready Result

A result is **reader-ready** when a complete reading pass confirms all of these conditions:

- each section and paragraph leads with the point the reader needs;
- explanations precede the terms, conclusions, and instructions that depend on them;
- relationships between claims are stated rather than left for the reader to reconstruct;
- connected ideas flow through paragraphs, while lists contain genuinely discrete items;
- every unfamiliar term or identifier receives enough context at first use;
- every confirmed AI-writing artifact has been removed; and
- every supported claim, condition, qualification, and normative requirement has survived the revision.

Read the complete result as its intended reader. When any condition fails, revise the affected passage and run
the complete reader-ready pass again. A material revision can expose or introduce another defect.

Finish when one complete pass finds no material defect. Leave working prose unchanged; revision serves the
reader rather than demonstrating that editing occurred.

After the reader-ready pass, search for the five artifacts that most often survive revision: a not-X-but-Y
contrast, a closer that restates its paragraph, an em dash, an unearned list of three, and a bold run.

Use the same pass to check what the edit dropped. A change of shape is where a claim goes missing, so after
merging a triad, cutting a closer, or unbolding a labelled list, verify that every fact, number, ranking, and
simultaneity claim survived. A lost claim is an error unless a rule above called for cutting it.

**Leave a sentence alone when it already works.** Do not rewrite one to match a neighbour's cadence, to satisfy
a preference nobody requested, or to show that editing happened. A limit in this skill is a ceiling on the
prose, not a quota of changes to make, and a passage that meets every rule needs no edit.

Check the finished work for over-correction as well: fabricated informality, variation introduced for its own
sake, and roughness added to make the prose look handmade. Each is as much an artifact as the marks above.

For a rewrite, return the edited text or requested file change. Do not append a change summary, a self-review,
or a confidence statement unless the user asked for one.

For a review, separate:

- proposed prose edits;
- factual, structural, or missing-context issues requiring author input; and
- passages left unchanged because their evidence or intended voice is unclear.

Clarity may override stylistic defaults when following them would make the prose awkward, misleading, or less
precise. Scope, factual accuracy, evidence, and claim preservation remain binding.
