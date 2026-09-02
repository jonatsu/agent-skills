# Converting an existing corpus

Bringing a docs tree that predates the contract under it. Conversion is a corpus-scale sequence of the fork
operation, so it inherits fork's guarantee: **relocation and revision are separate steps, and conversion only
ever does the first.**

- [The one rule](#the-one-rule)
- [Phase 1 — survey](#phase-1--survey)
- [Phase 2 — propose the mapping](#phase-2--propose-the-mapping)
- [Phase 3 — approval gate](#phase-3--approval-gate-%EF%B8%8F-required)
- [Phase 4 — execute](#phase-4--execute)
- [Phase 5 — verify and report](#phase-5--verify-and-report)
- [Phase 6 — govern the corpus](#phase-6--govern-the-corpus)
- [Convert early](#convert-early)

## The one rule

**Conversion labels and moves. It never rewrites.**

Every temptation during a conversion is to fix the prose while you are in there — the section is badly worded,
the two documents contradict each other, the plan is out of date. Do none of it. Revision happens afterwards,
as separate operations on the documents conversion produced, where each change is visible as a change.

A conversion that also rewrites is indistinguishable afterwards from a conversion that lost content. That is
the same laundering failure the two-step fork exists to prevent, applied to a whole corpus at once, which
makes it correspondingly harder to detect.

When conversion surfaces a contradiction between two documents, **record it in the Phase 5 report and in the
commit message** and move on. Do not pick a winner, and do not write it into a document — conversion adds no
content, and an open question written into a document during a conversion is indistinguishable afterwards from
one that was always there. Picking a winner is inventing the user's decision, and conversion is the worst
possible moment to do it, because the evidence is scattered across the very documents being moved.

## Phase 1 — survey

Read-only. Produce an inventory, not an opinion. Start with the checker, which does the structural half
mechanically. `<skill-dir>` is the directory this skill loaded from, per `SKILL.md`'s checker section — never
the working directory:

```bash
python3 <skill-dir>/scripts/check_corpus.py <corpus-dir> --survey
```

It reports each document's length, its sections with line counts, and which sections are fork candidates,
treating absent frontmatter as expected. The default mode would drop every document in a pre-conversion corpus
before analysing it.

Then cover what the survey does not. Several of these are mechanical — a grep, not a read — and are marked as
such:

- Every document, its line count, and its top-level sections with their line counts. *(the survey)*
- Every section past the ceiling, which is a fork candidate. *(the survey)*
- Existing implicit ownership: prose like "this document owns X", routing rules, "see Y for Z". *(grep)*
- Existing implicit lifecycle: status headers, "frozen", "draft", "superseded by", stale dates. *(grep)*
- Existing confidentiality or provenance prose — "customer supplied", "under NDA", "do not distribute", a
  copied standard excerpt. Each becomes a proposed `handling` value. *(grep)*
- Existing spellings of the same idea. Three incompatible spellings of "status" across four documents is
  normal and is exactly what the frontmatter replaces.
- Cross-references between documents, because forks will break some of them. *(grep)*
- Non-markdown artifacts and which document, if any, refers to them.

Report the inventory. Do not propose anything yet.

## Phase 2 — propose the mapping

One document, reviewable in one sitting. **It does not live in the corpus.** Present it in the conversation,
or write it outside the corpus root. Phase 3 forbids executing any part of the mapping before approval, and a
mapping document inside the corpus is a document the next survey inventories and the index has no claim for.

It contains:

**Types to mint** — the smallest set that covers the corpus, each with the per-type rule proposed for it.
Derive them from what the documents already are, not from a standard's taxonomy.

**Ownership claims to mint** — derived from existing prose declarations first, section headings second,
document titles last. Every claim maps to exactly one document. Name any topic that two documents currently
both discuss; that is the collision the contract exists to surface.

**Per-document frontmatter** — the exact block proposed for each file, including the lifecycle read off its
existing status prose and the `locked` value read off its existing freeze prose.

**Forks required** — a table: source document, section, line range, destination document, claim that moves
with it. One row per fork. Each row must be independently executable.

**Supersessions** — documents that are already dead in practice, with the pointer target.

**What does not move** — say this explicitly. A conversion proposal that touches everything is a restructure
wearing a conversion's clothes.

## Phase 3 — approval gate ⚠️ REQUIRED

The user mints the types and the claims, and approves the fork table. This is one confirmation over the whole
mapping, not one per file.

MUST NOT execute any part of the mapping before approval, including the "obviously safe" frontmatter. A
partially converted corpus with no approved map is worse than an unconverted one, because the next agent
cannot tell which half is intentional.

The user MAY approve a subset. Execute exactly that subset and leave the rest in the mapping document for a
later pass.

## Phase 4 — execute

Order matters. Do it in this order and stop at the first thing that does not verify.

1. **Frontmatter first, no content moves.** Every document gets its approved block. Nothing else in the file
   changes. After this step the checker runs and the index generates, so the ownership map exists before any
   content moves against it.
2. **Forks, one at a time.** The heading, title and H1 rules below are stated again in `SKILL.md`'s Fork
   section, deliberately — a single fork must not have to load this file to learn them. Change both copies
   together. For each row of the approved table:
   - Cut the exact line range, heading included. Do not retype it, do not reflow it, do not fix it.
   - Create the destination with its frontmatter, `lifecycle: draft`, unlocked, and the moved claim.
   - Paste the range in verbatim. **The moved heading stays as it is and the child gains no title.** Adding an
     H1 is an edit. A document whose whole body is one section is the expected shape of a fresh fork; the
     checker exempts it from the section ceiling rather than proposing it fork itself.
   - **The parent keeps the heading and puts the pointer under it.** A pointer with no heading floats between
     two unrelated sections, and a reader cannot tell what left.
   - **Strike any jurisdiction claim the departed content leaves behind** — the title, and any sentence
     stating what the document covers. Such a claim describes the document's jurisdiction rather than its
     subject, so striking it is pointer-class annotation — the same primitive as the pointer itself. The title
     is the usual case: "Vault design and implementation plan" becomes "Vault design". The bound is deletion,
     tested literally: **a span is strikeable only if deleting it verbatim leaves valid prose and nothing else
     on the line changes.** NEVER reword, resequence, or improve the remainder — that is a revision, and it
     waits for the separate step.
   - Remove the claim from the parent's `owns` if step 1 put it there — see the note below.
   - Carry the parent's `handling` value onto the child. A restriction travels with its content.
   - Verify byte-identity before starting the next row, after the hygiene hooks have run.
3. **Supersessions.** Set `lifecycle: superseded` and `superseded-by` on each retired document. Leave its
   `locked` value alone.
4. **Repair cross-references** that the forks broke. This is the one content edit conversion makes. A link
   target changed: retarget it. A *prose* reference — "the implementation plan below", "see the section above"
   — is also a broken cross-reference, and repairing it means changing words. Change the fewest that restore
   the reference and nothing else: "the implementation plan below" becomes "the implementation plan in
   roadmap.md". **Report every prose repair by name in Phase 5**, because it is the one place conversion
   touches prose and naming it is the only thing that stops it widening.
5. **Regenerate the index.**

**The parent's approved frontmatter is its post-conversion state.** A claim the fork table moves out is never
written onto the parent in step 1, so step 2's removal is normally a no-op. Where the parent already declared
that claim before conversion, step 2 removes it. Either way the index generated after step 1 may name a claim
whose content has not moved yet; that is expected and resolves at step 5.

**Do not set any lock during conversion.** Freezing is a separate decision that needs shared understanding,
and a conversion is precisely the moment when nobody has re-read the content.

### Verifying byte-identity

The relocated text must be identical to what left. Use the checker:

```bash
python3 <skill-dir>/scripts/check_corpus.py --verify-fork PARENT.md:'## Section' CHILD.md --since HEAD
```

It extracts the section from the parent at `--since` and compares it to the child's body, reporting the first
differing line. **Run it after the repo's hygiene hooks, not before.** A formatter that trims trailing
whitespace or fixes end-of-file newlines rewrites relocated content after you moved it, and a section forked
to the end of a file predictably loses the blank line that separated it from the next heading. `--verify-fork`
normalises trailing blanks for exactly that reason.

**Reading a `git diff` by eye does not work here, so do not.** It fails three ways for the sequence this phase
prescribes: the child is untracked and produces no diff at all without `git add -N`; the parent's diff also
carries the frontmatter step 1 added, because both steps share one working tree; and the retained heading is
coalesced as context, so the two hunks legitimately differ in length. All three read as a mismatch on a
correct fork, and a check that cries wolf is a check people override. *Recorded 2026-08-23 against git 2.43.0
— these are claims about `git diff` output, so re-check them if that behaviour changes.*

For a corpus not under version control, checksum the range before and after.

## Phase 5 — verify and report

- The checker exits 0, or every remaining error is named and explained.
- Every fork row verified byte-identical.
- The index regenerated and every claim resolving to exactly one document.

Report, in this order: what moved, what did not, every prose cross-reference repaired with its before and
after, every title corrected, every collision found and left unresolved, and every ceiling warning that
survived conversion. **Ceiling warnings surviving conversion are expected** — conversion moves what the
approved table said to move and nothing more, so a still-oversized document is a next-pass item, not a
conversion failure.

## Phase 6 — govern the corpus

**The conversion is not finished when the checker exits 0.** Phase 5 verifies the corpus; it does not make the
contract bind anything. Two things are still missing, and both are cheap now and expensive later:

1. **The mode declaration needs a trigger.** Without one the contract reaches only an agent that reads the
   instruction file top to bottom. State when the next agent must load this skill, and name the operations it
   must not improvise — a fork relocates verbatim, the index is generated.
2. **The declaration needs an enforcement surface.** Wire the checker into whatever the repo already runs: its
   task runner, its pre-commit config, its CI. Use `--check-index` so the gate compares rather than writes.
   Where nothing can run it, write `Enforcement surface: none — advisory-only` and say so out loud. A
   declaration that reads as enforced while nothing checks it is worse than an honest advisory one.

Both belong in the same record as the mode. A corpus with neither is labelled, not governed.

## Convert early

A corpus still in design converts far more cheaply than one that has shipped. Nothing is locked yet, the
cross-reference graph is small, and no downstream work has quoted a line number.

The cost curve is the argument for the whole skill: at 200 lines a fork is cheap, at 1000 it is surgery across
many cross-references, and a corpus that has been built against is one nobody wants to move at all. When a
corpus is mid-design and already showing the symptoms, say so — that is the moment conversion is nearly free,
and it does not come back.
