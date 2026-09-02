---
name: writing-for-humans
description: "Write and edit human-facing prose so it reads clear, skimmable and free of AI tells. Covers topic sentences, one idea per paragraph, register and person, active voice, positive form, parallel structure, specificity, named actors, deferred provenance, and a budget for em dashes and '--'. Use when drafting, editing, condensing, rewriting or reviewing anything a person reads: READMEs, design docs, ADRs, specs, guides, tutorials, release notes, changelogs, PR descriptions, working notes, essays, posts, commit messages, long-form comments. Triggers on 'make this read better', 'edit this prose', 'tighten this prose', 'remove the AI tells', 'this sounds like ChatGPT', 'stop the slop', 'de-slop this', 'humanize this', 'too many em dashes', 'cut the filler', 'make it skimmable', 'proofread this', 'rewrite this paragraph'. NOT for deciding a document's structure, scope or audience, which is technical-writing."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Writing for Humans

**IRON LAW: a rewrite MUST carry exactly the claims the original carried. These rules remove words, never
meaning, and NEVER add meaning. A rewrite that says less than the original has failed, however clean it reads;
one that says more has fabricated, which is worse.**

Optimize prose for a reader **skimming**, not only for information density. Keep the density and rigor; change
the presentation so a human can navigate it. Applies to any prose a person reads. Does NOT apply to chat
replies or terse tool output, which have their own budget.

**When editing a file, rewrite the prose and nothing else.** Code blocks, inline code, frontmatter, link
targets, table syntax, identifiers, command names and quoted material are all out of scope — a quoted passage
belongs to whoever said it, and "improving" it silently falsifies a quotation. Leave them byte-identical even
where they break a rule below.

This skill has no workflow, so it carries no step checklist. It is a set of decisions to get right while
writing, and a scan to run before delivering.

## Register: decide once, hold it

**This table is where document type is answered, and the only place.** Read your row before the first
sentence; no rule below asks the question again.

| You are writing                           | Person          | Fragments                    | Capitalised MUST / NEVER                       | "Recorded because…"           |
| ----------------------------------------- | --------------- | ---------------------------- | ---------------------------------------------- | ----------------------------- |
| Reference, spec, ADR, API doc, rules file | third           | NEVER                        | RFC 2119 obligations — NEVER edit them as tone | permitted, and often required |
| Instructions, how-to, tutorial            | second          | NEVER                        | RFC 2119 obligations — NEVER edit them as tone | navigation aids only          |
| Argument, essay, post                     | second or first | SPARINGLY, for real emphasis | none — cut as lazy extremes                    | NEVER                         |
| Note to self, working log                 | any             | MAY                          | none — cut as lazy extremes                    | MAY                           |

**Pick one and hold it for the whole document.** Mixed person is the defect; which one you picked rarely is.
Every other rule below applies unchanged whatever the register.

**Document type outranks passage tone.** A design record, ADR or requirements document takes the first row
even where its prose turns argumentative; an argument embedded in reference material inherits the document's
register rather than claiming its own.

**A supplied writing sample outranks this table and the STYLE defaults below it.** When the author gives you
two or three paragraphs of their own prose as the target, match its person, its register and its sentence
rhythm. The rules here describe a good default, NEVER a house style to impose on someone who has already shown
you theirs.

**The override has a floor.** It does NOT reach the Iron Law, the fabrication check, or the scope-protection
rule above. Two or three paragraphs also cannot establish a dash *rate*, which is what the budget measures, so
the dash ladder still applies.

## Structure

- **One idea per paragraph, led by a topic sentence that states the point.** A reader who reads only the first
  sentence of each paragraph MUST still get the argument. Test it: write the paragraph's point as one
  sentence. If that sentence needs an "and" or a "but" to hold two points, split the paragraph.
- Keep paragraphs to about 3–4 sentences and sentences to one main clause. Split qualification pile-ups rather
  than stacking nested parentheticals.
- Use headings, lists and tables for genuine structure that aids navigation. NEVER as a template to fill,
  NEVER with nothing behind them, and NEVER emit a broken or empty table.
- Lead each section with its conclusion, then support it.

## Sentences

- **Prefer active voice.** Write "the function returns the parsed token", not "the parsed token is returned".
  Use passive only when the actor is unknown or irrelevant ("the file was deleted"); it is sometimes
  necessary, NOT banned.
- **State positively.** Assert what is, not what is not: "he forgot" over "he did not remember"; "dishonest"
  over "not honest". Reserve *not* for genuine denial or antithesis, NEVER for evasion. A prohibition is
  genuine denial: NEVER rewrite "MUST NOT name the mechanism" into positive form, which changes what the
  document requires.
- **Put the new element last.** End each sentence on the word you want emphasized, with known context first.
- **Keep coordinate ideas parallel.** Similar content takes similar grammatical form, so the reader sees the
  likeness.
- **Omit needless words.** Cut "the fact that", "there is/are … that", and "who is/which was" padding. Every
  word MUST carry meaning.
- **Attach an opening phrase to the subject that follows it.** "Having read the log, the cause was obvious"
  says the cause read the log. Either name the actor — "having read the log, I saw the cause" — or drop the
  participle: "the log made the cause obvious".
- **Keep related words together.** Word order carries relation: a modifier attaches to whatever it sits
  beside, so a phrase wedged between subject and verb, or a relative pronoun stranded from its antecedent,
  changes what the sentence claims. "He only found two" and "he found only two" are different facts.
- **Break a run of loose sentences.** Three or more sentences in a row built as a main clause plus a trailing
  "and", "but" or "which" clause go sing-song, and the shape gives every idea the same weight regardless of
  what it is worth. Recast one as a simple sentence and subordinate another.

### Budget the dash; do NOT ban it

An em dash, a spaced hyphen and `--` are one construction, so forbidding a glyph moves the habit instead of
fixing it. The defect is frequency: a dash is how prose avoids deciding whether an aside is a sentence, a
subordinate clause, or cuttable. Before writing one, take the first option that holds:

1. **Cut the aside.** Most carry nothing the sentence needed.
2. **Make it its own sentence.** Usually the aside was a claim in hiding.
3. **Use a comma** for a simple subordinate clause.
4. **Use parentheses** for a genuine aside the reader may skip.
5. **Use a dash** — earned when a comma would misread (an aside that itself contains commas), or for a
   summarizing appositive at the end of a sentence.

**Budget: at most one per paragraph.** Two in a paragraph means one of them lost the argument at step 1 or 2.
Two in one sentence is always wrong. A dash in every paragraph is a habit, not a choice. When one is earned,
match the form the document already uses, and NEVER substitute `--` for it.

**Count constructions, not glyphs.** A paired parenthetical dash wrapping one aside is ONE construction and
counts once. Two separate asides in a sentence count twice, whatever punctuation each uses.

## Specificity and agency

Most prose that reads as AI-written fails here rather than at the sentence level.

- **Name the actor.** Inanimate things do not perform human verbs. A complaint does not "become a fix" and a
  decision does not "emerge"; someone fixed it, someone decided. "People tend to…" and "Nobody designed this"
  are the same defect wearing a narrator's voice. When no specific actor fits the register, address the
  reader.
- **Name the thing.** "The implications are significant" and "the reasons are structural" announce importance
  without carrying any. State the implication.
- **Prefer a concrete instance to an abstraction.** "The 4 GB upload fails" beats "large uploads may encounter
  issues".
- **Cut lazy extremes.** "Every", "always", "never", "everyone" claim authority the evidence rarely supports.
  Say how many, or how often. Capitalised keywords are governed by the register table, NOT by this rule.
- **Cut decoration, NEVER compression.** A closing line that compresses the paragraph's cost into few words is
  the paragraph working. Cut a closing line only when removing it loses no claim: that is the test, and "it
  sounds quotable" is not.

## Provenance

- Defer heavy provenance — PR and issue numbers, commit hashes, caveats, sources — to a trailing clause, a
  footnote, or a Sources section.
- State the claim first and support it after. Do NOT inline every qualification into the sentence making the
  claim.
- **A date that marks the sentence is not provenance and MUST lead.** "Added 2026-08-24 after a review…" and
  "Measured on 2026-08-24…" tell the reader what kind of sentence they are reading before they read it. Only a
  date that merely supports the claim gets deferred.

## Delivery checks

Run this scan before handing prose over:

- Does the first sentence of each paragraph carry the paragraph's point?
- Count the dashes. More than one in a paragraph, or one in every paragraph? Reopen the ladder above.
- Any sentence whose subject is not the thing acting? Name the actor.
- Any sentence that says something matters without saying what? Replace it with the specific thing.
- Any adverb or intensifier that would not be missed? Cut it.
- Is the person consistent with the register chosen at the top?
- Did anything get shorter by losing a claim rather than losing words? Restore it.
- Does the rewrite assert any actor, date, number or causal link the original did NOT support? Remove it, or
  go and find the source.

If two or more of these fire, load `references/phrases.md` and rescan the whole draft rather than patching the
lines you noticed.

**Require converging signals before rewriting for STYLE.** One dash, one pseudo-cleft opener or one adverb is
not evidence of anything: any single style check fires constantly on good writing, and prose that reads as
machine-written fails several at once. Rewrite where two or more independent style tells land on the same
passage; leave a lone style signal alone.

**This gate covers the style checks ONLY.** The last two checks above enforce the Iron Law. A single dropped
claim, or a single actor, date, number or causal link the original did not support, is acted on alone and
immediately — there is no threshold, and nothing converges with it.

## References

Load one when its symptom appears, NOT while drafting:

- `references/phrases.md` — load when a draft reads padded, promotional or throat-clearing, or when scanning
  finished prose against a blocklist.
- `references/structures.md` — load when sentences read formulaic: telegraphed contrasts, negation runways,
  rhetorical questions, staccato fragments.
- `references/examples.md` — load when a rewrite is not landing and a worked before/after would settle it.

**Do NOT load all three to write one paragraph.** The rules above are the whole discipline; the references are
lookup tables for a scan pass over finished prose. Skip them entirely for short drafts.

## Anti-patterns

- **Rewriting a passage to satisfy the checks while dropping its argument.** The Iron Law outranks every rule
  in this file.
- **Inventing an actor, a date or a number to satisfy "name the actor".** That rule is a retrieval
  instruction, NEVER a licence to supply what the draft does not have. Ask, or drop the unsupported claim.
- **Rewriting a normative statement into a descriptive one.** MUST, NEVER and SHOULD carry defined
  obligations. Changing one is a decision, not an edit.
- **Banning a glyph instead of budgeting the construction.** Forbidding em dashes produces `--` spam;
  forbidding both produces comma splices.
- **Applying a blocklist mechanically.** "Explicitly", "deliberately" and "measured" change what a sentence
  claims. Cut the empty ones.
- **Flattening a distinctive voice into generic correct prose.** These rules remove tells, NEVER personality.
- **Injecting personality the source did not have.** Several sibling skills instruct exactly this — add
  opinions, use "I", let some mess in. Applied to a spec it is vandalism, and applied anywhere it manufactures
  a stance the author never took. Match a voice; NEVER supply one.

## Keeping this skill honest

Two invariants for whoever edits this file next. Both exist because a genre-generic writing skill decays by
accumulating exceptions until no rule constrains anything.

1. **Document type is a conditional axis ONLY in the register table.** Every rule keyed on what kind of
   document you are writing MUST become a column of that table, so a reader answers the genre question once
   and never again. A rule MAY narrow its own predicate — "the tell is clustering, not any single instance" —
   because that is answered from the passage in front of you, not from the document's kind. Audited
   2026-08-25: five stray genre clauses across three files had each invented their own vocabulary for the axis
   ("rules file", "normative prose", "evidential prose", "a long reference document"), none of which the table
   defined. Folding them in is what makes this invariant true.
2. **Every rule MUST name the span it is failable against — a sentence, a paragraph, a passage or the document
   — and MUST be failable by inspecting that span alone.** A rule needing the author's intent, or a fact not
   present in the span, has already decayed. Cut it or make it concrete. Reworded 2026-08-25: "sentence" was
   always too narrow, since the dash budget is per paragraph and the formula table is per document.
