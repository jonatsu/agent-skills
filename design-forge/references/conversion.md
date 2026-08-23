# Converting an existing corpus

Bringing a docs tree that predates the contract under it. Conversion is a corpus-scale sequence of the
fork operation, so it inherits fork's guarantee: **relocation and revision are separate steps, and
conversion only ever does the first.**

- [The one rule](#the-one-rule)
- [Phase 1 — survey](#phase-1--survey)
- [Phase 2 — propose the mapping](#phase-2--propose-the-mapping)
- [Phase 3 — approval gate](#phase-3--approval-gate)
- [Phase 4 — execute](#phase-4--execute)
- [Phase 5 — verify and report](#phase-5--verify-and-report)
- [Convert early](#convert-early)

## The one rule

**Conversion labels and moves. It never rewrites.**

Every temptation during a conversion is to fix the prose while you are in there — the section is
badly worded, the two documents contradict each other, the plan is out of date. Do none of it.
Revision happens afterwards, as separate operations on the documents conversion produced, where each
change is visible as a change.

A conversion that also rewrites is indistinguishable afterwards from a conversion that lost content.
That is the same laundering failure the two-step fork exists to prevent, applied to a whole corpus at
once, which makes it correspondingly harder to detect.

When conversion surfaces a contradiction between two documents, **record it as an open question in the
document that will own the topic** and move on. Do not pick a winner. Picking one is inventing the
user's decision, and conversion is the worst possible moment to do it, because the evidence is
scattered across the very documents being moved.

## Phase 1 — survey

Read-only. Produce an inventory, not an opinion. Start with the checker, which does the structural
half mechanically:

```bash
python3 scripts/check_corpus.py <corpus-dir> --survey
```

It reports each document's length, its sections with line counts, and which sections are fork
candidates, treating absent frontmatter as expected. The default mode would drop every document in a
pre-conversion corpus before analysing it.

Then read for what a script cannot see:

- Every document, its line count, and its top-level sections with their line counts. *(the survey)*
- Every section past the ceiling, which is a fork candidate. *(the survey)*
- Existing implicit ownership: prose like "this document owns X", routing rules, "see Y for Z".
- Existing implicit lifecycle: status headers, "frozen", "draft", "superseded by", stale dates.
- Existing confidentiality or provenance prose — "customer supplied", "under NDA", "do not
  distribute", a copied standard excerpt. Each becomes a proposed `handling` value.
- Existing spellings of the same idea. Three incompatible spellings of "status" across four documents
  is normal and is exactly what the frontmatter replaces.
- Cross-references between documents, because forks will break some of them.
- Non-markdown artifacts and which document, if any, refers to them.

Report the inventory. Do not propose anything yet.

## Phase 2 — propose the mapping

One document, reviewable in one sitting. It contains:

**Types to mint** — the smallest set that covers the corpus, each with the per-type rule proposed for
it. Derive them from what the documents already are, not from a standard's taxonomy.

**Ownership claims to mint** — derived from existing prose declarations first, section headings
second, document titles last. Every claim maps to exactly one document. Name any topic that two
documents currently both discuss; that is the collision the contract exists to surface.

**Per-document frontmatter** — the exact block proposed for each file, including the lifecycle read
off its existing status prose and the `locked` value read off its existing freeze prose.

**Forks required** — a table: source document, section, line range, destination document, claim that
moves with it. One row per fork. Each row must be independently executable.

**Supersessions** — documents that are already dead in practice, with the pointer target.

**What does not move** — say this explicitly. A conversion proposal that touches everything is a
restructure wearing a conversion's clothes.

## Phase 3 — approval gate ⚠️ REQUIRED

The user mints the types and the claims, and approves the fork table. This is one confirmation over
the whole mapping, not one per file.

MUST NOT execute any part of the mapping before approval, including the "obviously safe" frontmatter.
A partially converted corpus with no approved map is worse than an unconverted one, because the next
agent cannot tell which half is intentional.

The user MAY approve a subset. Execute exactly that subset and leave the rest in the mapping document
for a later pass.

## Phase 4 — execute

Order matters. Do it in this order and stop at the first thing that does not verify.

1. **Frontmatter first, no content moves.** Every document gets its approved block. Nothing else in
   the file changes. After this step the checker runs and the index generates, so the ownership map
   exists before any content moves against it.
2. **Forks, one at a time.** For each row of the approved table:
   - Cut the exact line range. Do not retype it, do not reflow it, do not fix it.
   - Create the destination with its frontmatter, `lifecycle: draft`, unlocked, and the moved claim.
   - Paste the range in verbatim.
   - Leave the pointer in the parent, and remove the claim from the parent's `owns`.
   - Carry the parent's `handling` value onto the child. A restriction travels with its content.
   - Verify byte-identity before starting the next row.
3. **Supersessions.** Set `lifecycle: superseded` and `superseded-by` on each retired document. Leave
   its `locked` value alone.
4. **Repair cross-references** that the forks broke. This is the one content edit conversion makes,
   and it is mechanical: a link target changed. Never adjust the surrounding sentence.
5. **Regenerate the index.**

**Do not set any lock during conversion.** Freezing is a separate decision that needs shared
understanding, and a conversion is precisely the moment when nobody has re-read the content.

### Verifying byte-identity

The relocated text must be identical to what left. Check it the cheap way:

```bash
git diff -- PARENT.md CHILD.md
```

The hunk removed from the parent and the hunk added to the child must match line for line, allowing
only the pointer added to the parent and the frontmatter added to the child. When they do not, the
move rewrote something. Revert the row and redo it.

For a corpus not under version control, checksum the range before and after.

## Phase 5 — verify and report

- The checker exits 0, or every remaining error is named and explained.
- Every fork row verified byte-identical.
- The index regenerated and every claim resolving to exactly one document.

Report, in this order: what moved, what did not, every collision found and left unresolved as an open
question, and every ceiling warning that survived conversion. **Ceiling warnings surviving conversion
are expected** — conversion moves what the approved table said to move and nothing more, so a
still-oversized document is a next-pass item, not a conversion failure.

## Convert early

A corpus still in design converts far more cheaply than one that has shipped. Nothing is locked yet,
the cross-reference graph is small, and no downstream work has quoted a line number.

The cost curve is the argument for the whole skill: at 200 lines a fork is cheap, at 1000 it is
surgery across many cross-references, and a corpus that has been built against is one nobody wants to
move at all. When a corpus is mid-design and already showing the symptoms, say so — that is the moment
conversion is nearly free, and it does not come back.
