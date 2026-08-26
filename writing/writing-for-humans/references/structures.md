# Structures to Avoid

Sentence and paragraph patterns that read as formulaic. Each entry names the
pattern and what to write instead.

Contents:

- [Binary contrasts](#binary-contrasts)
- [Negative listing](#negative-listing)
- [Rhetorical setups](#rhetorical-setups)
- [Unnamed actors](#unnamed-actors)
- [Passive voice](#passive-voice)
- [Verb and word choice](#verb-and-word-choice)
- [Sentence starters](#sentence-starters)
- [Fragmentation](#fragmentation)
- [Rhythm](#rhythm)
- [Markup and typography](#markup-and-typography)
- [Chat artifacts in a document](#chat-artifacts-in-a-document)
- [Document-level formula](#document-level-formula)

## Binary contrasts

Telegraphed reversals that create drama instead of stating the point.

| Pattern | Problem |
|---|---|
| "Not because X. Because Y." | Telegraphed reversal |
| "[X] isn't the problem. [Y] is." | Formulaic reframe |
| "The answer isn't X. It's Y." | Predictable pivot |
| "It feels like X. It's actually Y." | Setup and reveal cliché |
| "The question isn't X. It's Y." | Rhetorical misdirection |
| "Not X. But Y." / "isn't X, it's Y" | Mechanical contrast |
| "stops being X and starts being Y" | False transformation arc |
| "doesn't mean X, but actually Y" | Negation-then-assertion crutch |
| "not just X but also Y" | Additive hedge |

**Instead:** state Y directly and drop the negation.

**Exception:** a real contrast the reader would otherwise get wrong earns the
construction. "This measures the document, not the prose it produces" corrects an
expectation. The test is whether X is a live misreading or a straw man.

## Negative listing

Listing what something is *not* before revealing what it is.

| Pattern | Problem |
|---|---|
| "Not a X… Not a Y… A Z." | Buildup through negation |
| "It wasn't X. It wasn't Y. It was Z." | Same, past tense |

**Instead:** state Z. The reader does not need the runway.

## Rhetorical setups

These announce insight rather than deliver it.

| Pattern | Problem |
|---|---|
| "What if [reframe]?" | Socratic posturing |
| "Here's what I mean:" | Redundant preview |
| "Think about it:" | Condescending prompt |
| "And that's okay." | Unnecessary permission |
| "By the time X, I was Y." | Narrative template |

**Instead:** make the point and let the reader draw the conclusion.

## Unnamed actors

Giving inanimate things human verbs, or floating above the scene, both hide who
did something. Model prose defaults to this because it avoids committing to an
actor.

| Pattern | Who is missing |
|---|---|
| "a complaint becomes a fix" | Someone fixed it |
| "the decision emerges" | Someone decided |
| "the culture shifts" | People changed behavior |
| "the conversation moves toward" | Someone steered it |
| "the data tells us" | Someone read it and concluded |
| "the market rewards" | Buyers paid for something |
| "People tend to…" | Which people, doing what |
| "Nobody designed this" | Who built it, and in what order |
| "This happens because…" | What causes it, named |

**Instead:** name the actor and put them at the front of the sentence. When no
specific actor fits, address the reader in the person the register calls for.

## Passive voice

Passive hides the actor and drains energy. It is NOT banned: use it when the
actor is unknown or genuinely irrelevant ("the file was deleted", "the token is
signed on the server").

| Pattern | Fix |
|---|---|
| "X was created" | Name who created it |
| "It is believed that" | Name who believes it |
| "Mistakes were made" | Name who made them |
| "The decision was reached" | Name who decided |

## Verb and word choice

Three habits that survive a clean vocabulary pass, because each is about how words
relate to one another rather than about any word being wrong.

### Copula avoidance

Elaborate constructions standing in for "is" and "has". **The tell is clustering,
NOT any single instance** — "the museum serves as both archive and gallery" is an
ordinary sentence. A passage that never says "is" and rotates through "serves
as", "stands as", "represents", "functions as" is the pattern.

| Pattern | Fix |
|---|---|
| serves as, stands as, represents, functions as | is |
| boasts, features, offers | has |

### Synonym cycling

Rotating words for one thing to avoid repeating it: "protagonist… main
character… central figure… hero" inside a paragraph. Pick the clearest term and
repeat it. Repetition of the right noun reads as precision; variation reads as
evasion, and in technical prose it makes the reader ask whether two names mean
two things.

### Forced groups of three

A tricolon is a legitimate device and most groups of three are fine. **Flag only
where the third item adds nothing or restates the first two**: "innovation,
inspiration, and insights". If the third item carries weight, leave it; if it is
padding, cut to two.

### False ranges

"From X to Y" where X and Y are not endpoints of any real scale: "from the
singularity of the Big Bang to the grand cosmic web". The construction promises a
spectrum and delivers two nouns. List what is actually covered.

## Sentence starters

| Pattern | Fix |
|---|---|
| Pseudo-cleft openers: "What makes this hard is…", "What matters here is…", "Why this works is…" | Lead with the subject: "The constraint is…". A wh-word opening a genuine subordinate clause ("When the token expires, the client retries") or a real question is fine. |
| Paragraphs starting with "So" | Start with content |
| Sentences starting with "Look," | Remove |

## Fragmentation

Sentence fragments for emphasis read as manufactured profundity.

| Pattern | Problem |
|---|---|
| "[Noun]. That's it. That's the [thing]." | Performative simplicity |
| "X. And Y. And Z." | Staccato drama |
| "This unlocks something. [Word]." | Artificial revelation |

Fragment tolerance is set by the register table in `SKILL.md`: NEVER in reference
or instructional prose, sparingly in argument, permitted in notes. That table is
the whole rule; this file adds nothing to it.

## Rhythm

| Pattern | Fix |
|---|---|
| Questions answered in the next sentence | Let the question breathe, or cut it |
| A closing line that adds nothing the paragraph did not already say | Cut it. A closing line that compresses the paragraph's point is the paragraph working; leave it alone however quotable it sounds |
| Three consecutive sentences of the same length | Break one |
| "Not always. Not perfectly." | Hedging disguised as reassurance |

For dashes, use the ladder and the per-paragraph budget in `SKILL.md`; a blanket
ban only relocates the habit to `--`.

## Markup and typography

Tells that live in the formatting rather than the words. Each is failable by
looking at the rendered page, and each is a *frequency* judgement — one bolded
term is emphasis, a bolded term in every bullet is a habit.

| Pattern | Fix |
|---|---|
| Boldface on a term in every list item, or several times a paragraph | Keep it for a genuinely important term on first mention |
| Inline-header bullets — `- **Label:** sentence that restates the label` | Cut the label, or cut the sentence. Rarely are both needed |
| Title Case In Every Heading, with no style guide calling for it | Sentence case. Only a tell where nothing else sets the convention |
| Emoji decorating headings or bullets | Remove |
| Curly quotes in plain-text or code contexts | Straight quotes. In formatted prose curly quotes are correct and NOT a tell |

## Chat artifacts in a document

Correspondence that arrived with pasted model output and was never cut. It reads
as addressed to someone who is not the reader.

- "I hope this helps!" / "Let me know if you would like me to expand."
- "Certainly!" / "Of course!" / "Great question!"
- "You're absolutely right!"
- "Here is an overview of…" opening a document that IS the overview
- "Would you like me to…" at the end of a section

Delete outright. Nothing is lost: none of it addresses the document's reader.

## Document-level formula

Every rule above works inside a paragraph. A document can pass all of them and
still announce itself, because the tell a reader notices first is the **section
template repeating**. Check the document as a shape, not only as prose.

| Pattern | Fix |
|---|---|
| Every section ending on a takeaway, a "why it matters", or a bottom line | Let some sections stop when the point is made |
| Sections of near-identical length, or identical paragraph counts | Vary them. Some sections need two paragraphs, some need six |
| Every list carrying the same number of items | Let list length follow the content |
| Every bullet built to the same grammatical shape and length | Let some be a fragment and some a full sentence |
| "Despite its [strength]… faces challenges… Despite these challenges…" | Replace the loop with the specific facts |
| A conclusion balancing good news against bad and closing on uplift | End on one statement, or on the next action |

Judge the shape by frequency, as with dashes: a template repeating across every
section is the tell, one section shaped that way is not. A document where every
entry carries signature, parameters, returns and errors is consistent by design,
and consistency is what the reader came for. Look for a section cut short or
padded out to fit the shape. If none was, the repetition belongs to the content.
