# Writing Rules for Agent-Facing Documents

How to write any document in the context system so a cold-started agent can use it. Most rules here are
mechanically checkable; the checker enforces the subset it can, and an audit applies the rest by reading.

## Write for the Cold-Start Reader

The test for every sentence: does it work for an agent with zero session history? No debugging narratives, no
"as discussed", no state-as-it-was. State the configuration or fact as it stands; provenance belongs to the
changelog and git history. If understanding requires knowing what some earlier session did, the document has
leaked session state and fails the test.

## Plain Language, and Detail Sized to Consequence

Use ordinary words and precise terms, and prefer the specific noun to the general one. Cut filler, repetition,
hedging, and praise for the project or its tools: a document that admires its subject spends the reader's
attention proving nothing. Every sentence carries a fact, a constraint, a consequence, or an action.

Length is not the target — the cost of being wrong is. These documents are read deliberately, by someone who
followed a route to get here, so they owe more detail than the floor does: the reader came for exactly what the
floor could not afford to carry, and arriving at a summary of it is a wasted trip. Write what the reader must
not get wrong in as much detail as getting it wrong would cost, and leave out what would merely be nice to
know. Shorten by deleting a passage that changes nobody's decision, never by thinning a qualifier inside one
that does.

## Read-When Lines Are Trigger Conditions

Every routing entry, document header, and skill description answers "when should I load this" — not "what is
this about". "Verification gates" fails; "which gate proves what — read before gating a change, not after a
result surprises you" routes. Front-load the discriminating words. Cover each distinct trigger once; add an
exclusion only when it prevents likely misrouting. One owner per trigger across the whole system: when two
descriptions claim the same phrase, move the trigger to the document that carries the full treatment and cut
it from the other.

## Separate Structural Routes From References

A trigger-keyed list item is the default structural route. Keep the trigger and Markdown document link on its
first physical line, and put the link immediately after the separating colon. Wrap only the purpose text that
follows. Use one of these exhaustive leading phrases:

```markdown
- Read when <condition>: [<document>](<path>.md) <purpose>.
- Read before <condition>: [<document>](<path>.md) <purpose>.
- If you <condition>: [<document>](<path>.md) <purpose>.
- Symptom <condition>: [<document>](<path>.md) <purpose>.
```

The list form keeps each route independently editable. Adding or widening one entry does not reformat its
neighbors.

Trigger-keyed tables remain structural routes when a compact matrix is worth coupled formatting. A target
column must be named `File` or `Read`; a trigger column must start with `Read when`, `Symptom`, `Read before`,
or `If you`. **That vocabulary is exhaustive, and a table outside it routes nothing while looking perfectly
serviceable.** A readable `Item | Where` table is invisible to the checker and to an agent scanning for the
pattern. Rename the columns rather than inventing a synonym.

Outside the trigger-keyed forms, use a Markdown link alone on its line
when the current document should act as a parent index for the target. Put the load condition or relationship
immediately before that link, so the parent explains why the child belongs in this context. The same child may
have more than one parent when each route serves a distinct task.

An inline Markdown link cites related material; it does not make that material reachable from the floor.
Likewise, a backticked `.md` path outside a routing-table target cell is only an identifier. This distinction
keeps incidental mentions from satisfying the reachability check and lets an index expose focused child
routes without copying their contents into the floor.

## Summary First, Fractally

Progressive disclosure applies inside documents, not only between them. A document's first paragraph answers
"should I keep reading"; a section's first sentence answers it for the section. The reader who stops early
should leave with a correct, if shallow, model — never a wrong one.

## Maximize the Search Surface

Half of agent navigation is text search. Quote error messages verbatim rather than paraphrasing them; backtick
every path, binary, option, and identifier; prefer distinctive literal names over generic descriptions. A
symptom route that paraphrases its symptoms is invisible to the agent grepping the actual error.

## Pointers in the Most Durable Form

Mechanism > stable identity > file path > never a line number. Point at the option, command, or anchor that
survives refactors; use a file path when nothing stabler exists; a line number is stale before it is read.
Two exemptions: frozen genres (decisions, evaluations), where a line number is a dated snapshot coordinate;
and a living document that declares, in its head, the pinned revision (the word "pinned" plus a backticked
commit hash) its citations are valid at — that converts line references into stamped facts with a
re-validation trigger.
State predicates, never countable inventories: "every aspect gated on the desktop capability", not "the seven
desktop aspects" — a count is wrong at the next addition and nothing flags it.

## Stamp What Facts Were Verified Against

A non-obvious claim carries the revision, schema version, or test run it was checked against. "Verified
against nixpkgs `af8ad534`" ages honestly; "checked recently" does not. When re-verification happens, move the
stamp; when it cannot happen, add a dated unverified-since caveat.

## Declare Authority

A document that could be mistaken for outranking something must say it does not. Frozen records state they are
historical; findings state they are advisory and need re-verification; plans state that built code supersedes
them. The two global rules — the user's current instruction outranks stored guidance, and the repository
outranks its own documentation — hold everywhere and need not be restated per file, but nothing may contradict
them.

## Memory Is Fact Plus Rationale, Never Bare Imperative

A stored note written as a command ("always delete X before Y") executes as an instruction in a later session
with none of its original context. Write the fact, the why, and the condition: "X caches Y; deleting X before
Y prevented Z on <date> — applies only when W." The reading agent decides; the note informs.

## Every Claim Is Verified, Generated, or Flagged

Confident prose from recall is the failure mode that fabricated configuration options and wrong defaults enter
by. A claim about external behavior cites what verified it; a claim derivable from code should be generated or
should point at the code; anything else is labelled unverified. When editing a document, the claims you did
not check keep their existing status — do not silently launder them into verified.

## Checkable Subset

The package checker enforces: every living load-at-need document reachable through structural routes from the
routing roots (dated records are reached by browsing their genre directory and are exempt), trigger conditions
present and non-topical (heuristically: non-empty), and no line-number references in living unpinned
documents. It recognizes trigger-keyed list items, compatible routing-table rows, and standalone Markdown
inclusion links as structural. Inline links and incidental backticked paths remain references. An audit
additionally reads for cold-start violations, genre mixing, missing stamps, missing authority lines,
inventory counts, and paraphrased error messages.
