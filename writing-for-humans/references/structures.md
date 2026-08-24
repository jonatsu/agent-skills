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

A repeated shape is only a defect when it is imposed. A reference document whose
sections genuinely share a structure — every API entry carrying signature,
parameters, returns, errors — is consistent, and consistency is what a reader
came for. Ask whether the shape follows the content or the content was cut to
fit the shape.
