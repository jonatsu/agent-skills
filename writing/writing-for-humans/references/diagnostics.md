# Copy-Editing Diagnostics

Use this reference for a long draft, a difficult diagnosis, or the final AI-mark cleanup scan. It is a
diagnostic aid, not a blocklist.

The category headings below apply to prose in any language. The example strings under them are English. For
another language, match the category and derive its signatures from the text itself; a translated English
example is not that language's tell, and the absence of the English strings does not make a passage clean.

Remove definitive production residue when found. Treat ordinary stylistic features as weak signals that need
supporting evidence from the surrounding passage.

## Chat Residue

Remove language that belongs to an assistant-user exchange rather than the document's reader:

- "I hope this helps."
- "Let me know if you would like me to expand."
- "Certainly!" or "Great question!"
- "Would you like me to…" at the end of a section
- "Here is an overview of…" when the document itself is the overview

## Meta-Commentary

Consider removing a sentence that announces the document instead of advancing it:

- "In this section, we will…"
- "The rest of this document explains…"
- "Let me walk you through…"
- "As we will see…"

Keep navigation that helps the reader act, such as a pointer to a file, condition, or next step.

## Empty Promotion

Ask what a sentence actually claims when it relies on importance words such as "crucial", "transformative",
"robust", "seamless", or "groundbreaking". Replace the word only when the specific behavior, consequence, or
constraint can be stated without changing the claim.

## False Agency

Flag a sentence when it gives an inanimate abstraction a human action and hides an actor the source can
establish:

| Pattern                       | Safer action                                           |
| ----------------------------- | ------------------------------------------------------ |
| "the complaint becomes a fix" | Name who filed it and who fixed it, if known.          |
| "the decision emerges"        | Name who decided, if known.                            |
| "the data tells us"           | Name who interpreted the data and what they concluded. |

Do not invent the missing actor. Ask the author or state the gap.

## Unnamed Authority

False agency hides the actor inside a mechanism. This hides a claim behind a crowd nobody can check:

- "experts say"
- "research suggests"
- "observers note"
- "critics argue"
- "it is widely accepted that"

Name the source and keep the claim inside what that source establishes. Where no source exists, attribute the
claim to whoever is making it, mark it as unsupported, or cut it.

## Clustered Rhetorical Setup

One contrast or rhetorical question may be deliberate. Inspect a passage when several sentences stage a reveal,
announce insight, or end in a manufactured payoff instead of making the claim directly.

## Editing Distortions

These are the ways an edit changes a claim while appearing to change only its wording. Check an edited passage
against its source for each one.

| Distortion            | Example                                                                  |
| --------------------- | ------------------------------------------------------------------------ |
| Certainty inflated    | "may reduce" becomes "will reduce"                                       |
| Scope widened         | "some teams" becomes "most teams"; "in this sample" becomes "in general" |
| Sequence made causal  | "associated with" becomes "caused"                                       |
| Absence made proof    | "found no evidence" becomes "proved there was none"                      |
| Attribution detached  | "the vendor claims the export completes" becomes "the export completes"  |
| Reported view claimed | "the user reported a hang" becomes "the feature hangs"                   |
| Obligation softened   | "must" becomes "should"; "never" becomes "avoid"                         |
| Negation lost         | a condition, exception, or qualifier drops out of a shortened sentence   |
| Exact term weakened   | a term of art is replaced by a general synonym that does not carry it    |

When shortening, protect every word that carries a limit, condition, exception, or qualification. Those words
are usually the ones a length target reaches for first.

Do not silently repair an inconsistency, inaccuracy, or omission as though the correction came from the author.
Preserve it and flag it, or ask when the answer would change the piece.

## Leaked Machinery and Placeholders

Remove these on sight. They are production residue with no reading under which they belong in delivered text:

- unresolved placeholders: "[insert source]", "[Name]", "TK", "TBD", "XX", "202X";
- leaked tool, interface, and citation tokens: "turn0search0", "oaicite", "oai_citation", "contentReference";
- editorial notes and alternatives left in publication-ready copy; and
- broken fences, empty footnotes, and malformed links introduced during generation.

Replace a placeholder with the real value when the source supplies it. Otherwise state the gap to the author
rather than inventing a plausible filler.

## Invisible Marks and Metadata

Inspect formats that can carry invisible text or metadata when cleaning AI-produced output. Remove a character
or field only when its purpose as an AI-origin marker is established. Preserve legitimate Unicode needed for
language, accessibility, bidirectional text, typography, or emoji composition. Preserve authorship,
interoperability, and application metadata unless the user included it in scope or it is a confirmed AI mark.

When removing a confirmed invisible mark, verify that the rendered text and intended semantics did not change.

## Compound Hyphenation

This section is an English convention. In another language, follow that language's own rules for compounds.

Hyphenate a temporary compound before the noun it modifies, and usually open it after a linking verb:
"a well-known author", but "the author is well known"; "a long-term plan", but "the plan is long term".

Do not hyphenate an "-ly" adverb compound: "highly qualified", not "highly-qualified". Do not hyphenate a set
phrase that reads as one unit: "high school", "real estate", "machine learning".

Keep a conventional or ambiguity-preventing hyphen, such as "state-of-the-art", "cost-effective", and
"user-friendly". Where a project names a dictionary or style guide, that source governs; where none is named,
preserve the established usage in the surrounding text rather than correcting it.
