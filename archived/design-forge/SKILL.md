---
name: design-forge
description: Requirements and design documentation as an enforced corpus contract — frontmatter lifecycle, ownership claims, lock semantics, length ceilings, and the operations over them (create, lock, amend, fork-with-pointer, supersede, convert an existing docs tree). Use when writing or revising a requirements or design document, when a document or section has grown too long, when a design should be frozen, when settled content needs changing, when a section should become its own document, or when an existing docs tree needs bringing under the contract. Triggers — 'write requirements', 'requirements doc', 'SRS', 'design doc', 'freeze this design', 'lock this document', 'supersede this', 'amend this', 'split this document', 'convert these design docs', 'customer confidential', 'system requirements', 'hardware requirements'. Covers software, system and hardware. NOT for brainstorming an unshaped idea, which is idea-forge. NOT for pressure-testing a written plan, which is grilling. NOT for ADRs or changelogs.
metadata:
  author: Joonas Onatsu
  license: MIT
---

IRON LAW: A LOCKED DOCUMENT MAY GAIN ANNOTATIONS THAT REDIRECT AUTHORITY, AND NOTHING ELSE. NEVER change the
meaning of settled content, and NEVER clear a lock — not to edit and relock, not because the user "clearly
wants this updated". Unlocking is a manual, out-of-band human edit, and its friction is deliberate.

Red flags (stop and re-read the Iron Law if any appear):

- Reaching for `locked: false` on a document you are about to edit.
- A fork whose moved text is not byte-identical to what left the parent.
- Rewriting a body sentence instead of appending an amendment and marking the affected point.
- Using a document type or an ownership claim the user never minted.
- Producing an audit of everything wrong with the corpus when nothing actually blocked you.
- Applying this skill's own structure to a repo that declared house convention.

## What this governs

A **corpus contract** — how a set of requirements and design documents declares its own structure — and the
**operations** over it. The contract is negotiable; the operations are not. Fork-with-pointer, the lock
protocol, the amendment rules and the length ceilings are structure-agnostic and apply unchanged inside
somebody else's layout.

Domain is a parameter, not a second contract. Structure rules do not change because the subject is a PCB. What
changes is content vocabulary.

### Reference files

Load on demand at the point of need, never up front. Each costs context the operation at hand may not need,
and every protocol in this file is complete without them — except Convert, which says so where it routes.

| File                       | Load when                                                                                                 | Do NOT load                                                                                                                                    |
| -------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `references/contract.md`   | Minting a type or an ownership claim, writing the mode declaration, or checking a field's exact semantics | A routine amend, fork or lock — those protocols are complete below                                                                             |
| `references/conversion.md` | Converting an existing corpus, after the survey has run                                                   | Any single-document operation                                                                                                                  |
| `references/authoring.md`  | Writing or reviewing the text of individual requirements                                                  | Corpus-level governance — owning a document says nothing about its requirement wording                                                         |
| `references/domains.md`    | The subject is hardware or system-level                                                                   | Software-only requirements. Its verification vocabulary is not the software one, and applying it there produces requirements nobody can verify |

## The decisions

This is a routing skill, not a workflow, and it deliberately has no progress checklist: pick the operation and
run its protocol. Exactly one thing is ordered — **the contract in force is established before any operation
runs.** The rest are decisions, each with the trap that makes it one.

**Before anything, ask: which contract is in force?** Never "does this repo look organised" — that question
has a wrong answer that looks right, and answering it from evidence is the one move this skill forbids
outright.

**Before minting a type or a claim, ask: did the user confirm this one?** Mint freely and a freeform
vocabulary becomes per-document config, at which point the contract constrains nothing.

**Before writing an ownership claim, ask: does the index already carry it?** A collision is an incident to
report, never a tie to break.

**Before changing settled content, ask: is this a sentence or an aspect?** A sentence is an amendment, an
aspect is a fork. When clearing the lock starts to look like the answer, the question is wrong.

**Before reporting, ask: did this actually block me?** The trigger is "I would have to guess to proceed", not
"this looks bad". An audit nobody asked for trains the reader to skim past the one report that mattered.

Close by regenerating the index and running the checker. The pre-delivery checklist at the end of this file is
the exit gate.

## Establish the contract in force ⛔ BLOCKING

Every check in this skill runs against **the active contract, whichever is in force** — never against a fixed
template this skill ships.

Two modes:

- **Imposed** — new designs and deliberate conversions get this skill's contract.
- **House convention** — a repo with an established convention keeps it. This is not "our contract with
  enforcement off"; it is *their* contract, and we comply.

Mode is **declared once and recorded** where the repo already keeps agent instructions (`CLAUDE.md`,
`AGENTS.md`, or the repo's equivalent). Evidence informs the question; a human answers it.

**The request itself may be the declaration.** When the user's own instruction states the mode — "convert this
tree to the contract" is *imposed*, "keep our existing layout" is *house convention* — record it and name the
words that carried it. Asking anyway is theatre, and a ⚠️ REQUIRED gate that is theatre gets substituted for
by judgement rather than followed. The *recording* is never optional.

**NEVER auto-detect the mode.** The false positive is the dangerous direction: a tree with seven documents,
consistent naming and a milestone subdirectory scores as "established convention" under any plausible
detector, and the detector then blesses as canonical the very structure that needed fixing.

Where no enforcement surface exists — documents that cannot carry frontmatter, or a house convention with no
machine-readable field — **say so and run advisory-only**. Announced degradation beats silent pretence. The
named failure this prevents is an agent claiming a rule is in force while enforcing nothing.

**The declaration MUST carry a trigger and an enforcement surface.** Without a trigger it binds only an agent
that reads the instruction file top to bottom; one that opens a design document directly gets no signal that a
fork relocates verbatim or that the index is generated. Without an enforcement surface the declaration *reads*
as enforced while nothing checks it — this skill's own anti-pattern, committed by following this skill.
`none — advisory-only` is a valid answer to the second. Silence is not.

**This skill governs structure, lifecycle and the operations over them — not prose.** The section catalogue in
`references/contract.md` is a heading list, and `references/authoring.md` is scoped to requirement text;
nothing here says how a design document should read. That is deliberate: voice is corpus-specific, and a
hardware requirements corpus and a software design corpus should not share one. **The mode declaration is
where a corpus records its own**, next to the type list, if it wants the conventions to survive the agent that
established them. Say so when asked — silence reads as "no rules exist" when the answer is "your corpus
declares them, and has not yet".

## Route to the operation

| The user wants                                                                  | Operation     |
| ------------------------------------------------------------------------------- | ------------- |
| A new requirements or design document                                           | **Create**    |
| A design frozen — shared understanding reached                                  | **Lock**      |
| One wrong sentence or paragraph corrected in settled content                    | **Amend**     |
| A section that has outgrown its document, or an aspect that needs real revision | **Fork**      |
| The whole document replaced                                                     | **Supersede** |
| An existing docs tree brought under the contract                                | **Convert**   |

Amend and Fork are the two answers to "this locked document is wrong". Amend is for a sentence; Fork is for an
aspect. If unlocking looks like the answer, the operations layer is being asked the wrong question — re-read
the routing table.

## The contract

**Frontmatter is the enforcement surface.** Machine-readable beats prose, because every failure this skill
exists to fix is a rule that existed with no enforcement surface.

```yaml
---
type: design            # REQUIRED — freeform, human-minted
lifecycle: active       # REQUIRED — draft | active | stale | superseded
owns:                   # REQUIRED — at least one claim
  - fetch-mechanics
locked: true            # OPTIONAL — defaults to false
superseded-by: new.md   # REQUIRED when lifecycle is superseded, forbidden otherwise
supersedes: [old.md]    # OPTIONAL — back-link
handling: internal      # OPTIONAL — internal | customer-confidential | third-party
---
```

- `lifecycle` answers *is this still authoritative?*
- `locked` answers *may this be edited?* — **an orthogonal flag, never a lifecycle value.** The two come apart
  in both directions: a design can be `active` and locked (the normal case), or `superseded` and locked.
  `locked` is what gates an agent's write.
- `owns` is the self-declared list of claimed topics. **The index is generated from these declarations, never
  hand-typed.**
- `type` is freeform, with rules attached per type in the contract declaration. This is deliberate and
  reversible, chosen because no adequate fixed vocabulary existed yet. Expect it to tighten.

**Minting is human.** An agent MAY use an existing type or ownership claim freely and MAY propose new ones,
but creating either is the user's call — one confirmation, since the two events usually coincide. Without that
gate, freeform types degenerate into per-document config and the contract stops constraining anything.

**A type name MUST NOT reuse a `lifecycle` value.** `type: draft` beside `lifecycle: active` reads as a
contradiction and beside `lifecycle: draft` as a tautology; either way the reader stops being able to tell
which axis a word belongs to. Type and lifecycle are orthogonal for the same reason `locked` is — what a
document *is* does not move when its state does. Reject `draft`, `active`, `stale` and `superseded` as type
names and pick one that says what the document holds.

**An absent or empty section is a correct and complete state.** NEVER fill a heading to avoid leaving it
empty; delete the heading instead. An agent told to keep a document complete will fill every leaf of a large
template, and that is the mechanism behind documents nobody can read.

**A numbered entry keeps its number forever, in any document type.** NEVER renumber to close a gap left by a
closed or withdrawn entry, and NEVER give a new entry a number that has been used before. Everything that
cites an entry — another document, a commit message, a ticket, a test plan — cites the number, and reuse
silently redirects those citations to unrelated content. The observed failure: a corpus that reused two
settled open-question numbers ended up with *as then numbered* appended to every back-reference, forever, as
the cheapest available repair. `references/authoring.md` states the same rule for requirement IDs and adds
their format; this is the general case, and it governs open questions, decisions, invariants and anything else
a document numbers.

**`handling` marks content that may not leave the corpus** — a customer-supplied specification, a contractor
deliverable, a standard excerpt. When a document carries any value, NEVER send its content to an external
service (web search, a fetch tool, an MCP server, a subagent that may search), and NEVER copy it into a
document with a weaker restriction. Report that the restriction stopped you.

**It is advisory and cannot be otherwise, so NEVER present it as a security control.** Nothing enforces it —
the agent reading the field is the agent that could paste the content into a search query, and the checker
validates spelling only. Where a real guarantee is needed, the material does not belong in the repository.

**Non-markdown artifacts do not carry frontmatter and do not need it.** A diagram, an exported spreadsheet or
a customer-supplied PDF is content that a markdown document owns and declares. NEVER introduce a sidecar
metadata file — it is a second source of truth nobody is forced to update, and the stale one wins by default.

Load `references/contract.md` for the full field reference, the mode-declaration format, per-type rule
declarations, and the document section catalogue.

## Operations

### Lock ⚠️ REQUIRED confirmation

An agent MAY propose a lock and MAY set it on explicit in-session confirmation. **An agent may NEVER clear
one.** Setting is low-risk; clearing is the entire guard.

The lock point is *shared understanding reached and user-confirmed* — not a date, not a phase.

What the lock forbids is changing the **meaning** of settled content. It permits **meaning-preserving
annotation**, and only that. This is forced by the fork case: leaving a pointer in the parent is an edit to a
locked document, so `locked` cannot mean immutable.

When asked to unlock, report and stop. A locked document that needs to change is the amendment case or the
fork case. If unlocking starts to look routine, say so — that is evidence the operations layer is inadequate,
and surfacing it is the point of the friction.

### Amend

Trigger: one wrong sentence or paragraph, where forking would be absurd overhead.

1. Append an entry to a `## Amendments` section at the end of the document. **The body is never rewritten.**
2. Add an inline marker `[amended A<n>]` at the affected sentence or paragraph. **Not optional** — without it
   a reader hits the stale sentence with no signal to look further, and an amendment nobody finds is worse
   than none, because the document now looks maintained.

```markdown
## Amendments

### A3 — Fetch timeout is 30 seconds, not 10
The figure under "Fetch mechanics" was measured against the wrong endpoint. Thirty seconds is the
observed p99 including redirects.
```

Every `### A<n>` MUST have at least one matching `[amended A<n>]` in the body — one at every point the
amendment invalidates. A correction that lands in three places is marked in three places. Zero is an error: an
amendment nobody finds is worse than none. The checker verifies this mechanically.

**At five amendments, warn and propose a named successor document.** Never block. A document with fifteen
amendments should have been replaced, and an append-only section grows without bound.

### Fork ⚠️ REQUIRED confirmation

**Fork and revise are two distinct steps, never one.**

1. **Verbatim relocation.** The aspect moves out byte-identical to what left. The locked parent gains a
   pointer. The new document gets its own frontmatter, `lifecycle: draft`, unlocked, and the ownership claim
   that moved with it.
2. **Revision**, in the new document only, as a separate visible step.

The testable form: **after the relocation, the parent plus the new document together must still say what the
parent said** — nothing dropped, added, or altered in the move.

NEVER combine the steps. "Fork it out and rewrite it" looks like relocation going in and is a rewrite coming
out, and nothing can tell afterwards. When asked for both, do them as two steps the user can see.

The pointer in the parent, under the heading that stayed:

```markdown
## Fetch mechanics

> Authority on fetch mechanics moved to [capture-and-fetch.md](capture-and-fetch.md).
```

**The heading stays and the pointer goes under it** — one floating between two unrelated sections leaves a
reader unable to tell what left. **The child gains no title:** the moved heading arrives as it is, and adding
an H1 is an edit in a step that makes none. A document whose whole body is one section is a fresh fork's
expected shape, and the checker exempts it from the section ceiling rather than proposing it fork itself.
**Strike any jurisdiction claim the departed content leaves behind** — the title, and any sentence stating
what the document covers. Such a claim describes the document's jurisdiction rather than its subject, so
striking it is pointer-class annotation and permitted on a locked parent. The title is the usual case: "Vault
design and implementation plan" becomes "Vault design". The bound is deletion, tested literally — **a span is
strikeable only if deleting it verbatim leaves valid prose and nothing else on the line changes.** Anything
needing a word substituted or a sentence resequenced is a revision, and waits for the separate step.

**Authority transfers with the content.** The pointer means *this content now lives at X*, not *this content
is still true*. The locked parent stays honest not by staying correct but by no longer claiming jurisdiction.

The pointer and the amendment marker are **the same primitive** — an in-body annotation that redirects
authority without altering a claim. One rule, two uses.

**A `handling` restriction travels with the content.** The child inherits the parent's value; a fork that
drops it launders the restriction exactly as a one-step fork launders a rewrite.

### Create

1. Ask which type and which ownership claims, minting per the rule above.
2. Check the claims against the index. A collision is an incident — report it and ask; do not pick.
3. Write the frontmatter first, then the body.
4. Place by lifecycle, not topic: design is durable, milestone directories hold the perishable. A document
   whose title announces two lifecycles ("design **and implementation plan**") is the defect.
5. **An index exists from document two**, not at a size threshold. Its job is stating relationships, and
   relationships exist as soon as a second document does.

### Supersede

1. The new document is created normally and takes over the ownership claims.
2. The old document gets `lifecycle: superseded` and `superseded-by: <path>`.
3. The old document's `locked` value is **unchanged**. Superseded is not a licence to edit.

### Convert an existing corpus ⚠️ REQUIRED confirmation

Conversion is a corpus-scale sequence of the fork operation, so it inherits fork's guarantees. It is **plan,
approve, then execute** — never a single rewriting pass.

Start with the checker's `--survey` mode, which produces the Phase 1 inventory. Then load
`references/conversion.md` before going further. Do not improvise conversion from this summary.

## Length ceilings

**They warn and propose. They never block.** A skill that refuses to work is a skill that stops being invoked.

| Scope    | Threshold      | Response                                                 |
| -------- | -------------- | -------------------------------------------------------- |
| Section  | ~150–200 lines | Primary trigger — warn and name the section to extract   |
| Document | ~1000 lines    | Backstop warning for death by a thousand sections        |
| Document | ~2000 lines    | Backstop limit — propose a split plan, still never block |

Section length is primary because a document-level count arrives too late to be actionable and cannot say
*what* to extract. At 200 lines a fork is cheap; at 1000 it is surgery across many cross-references.

**A warning MUST carry a specific fork proposal naming the section.** A warning that leaves the reader to find
the remedy is noise.

## Reporting

**Incident-driven, never an audit.** The trigger is *"I would have to guess to proceed"*, not *"this looks
bad"*. A general audit becomes a nag, and a nag trains the reader to skim past everything including the one
report that mattered.

| Trigger                                    | Response                                                           |
| ------------------------------------------ | ------------------------------------------------------------------ |
| Repo or convention quality                 | Report, take the conservative option, name the assumption, proceed |
| Genuine ambiguity in the operation at hand | Ask — choosing would invent the user's decision                    |
| Corpus is messy                            | Never refuse to work                                               |

"Genuine ambiguity" means **the alternatives lead to materially different outcomes and no conservative default
exists.** Where a default exists, take it and say so.

## The checker

**`<skill-dir>` below is the directory this file was loaded from — resolve the script against it, never
against the working directory.** `scripts/check_corpus.py` is a path inside the skill package, while the
agent's cwd is the project root, where that path either misses or hits an unrelated `scripts/` the project
owns. Substitute the real directory; NEVER type these commands literally.

```bash
python3 <skill-dir>/scripts/check_corpus.py <docs-dir>
```

**Four modes, and `--help` is the authority on their exact flags** — this file deliberately does not copy
them, because a transcribed flag list is wrong from the next change onward while still reading as
authoritative. The default validates; `--survey` inventories a corpus not yet under the contract;
`--check-index` compares without writing; `--verify-fork` checks a relocation. What follows is why each exists
and when to reach for it, which `--help` does not carry.

The default mode validates every frontmatter block against the contract, reports ownership collisions,
verifies amendment markers, reports ceiling breaches, and regenerates the index from the `owns` declarations.
Standard library only.

`--survey` is the pre-conversion inventory: it reports each document's length, its sections with their line
counts, and which sections are fork candidates, treating absent frontmatter as expected rather than as an
error. Use it on any corpus not yet under the contract — the default mode drops a document with no frontmatter
before analysing it, which is useless on exactly the corpus that needs the help. It covers the structural half
of Phase 1 and no more: the ownership, lifecycle and confidentiality prose and the cross-reference graph are
separate reads.

`--check-index` regenerates the index in memory and compares it to the file, never writing. It is what a
read-only gate wants, and it suppresses the warning the plain mode emits about a missing index.

`--verify-fork` replaces reading a `git diff` by eye. It extracts the named section from the parent at
`--since` (default `HEAD`) and compares it to the child's body, normalising trailing blank lines because
hygiene hooks trim them. It shells out to `git`; where `git` is absent it says so and skips.

**Get the baseline right or the check reports a mismatch that has nothing to do with the fork.** `--since`
must name a revision where the parent still holds the section, and the default `HEAD` is that revision in
neither of the two common situations:

- **The parent is dirty**, which is the normal case — you fork the document you were just editing, so `HEAD`
  predates the session and a correct relocation compares against the wrong text.
- **The fork is already committed**, so `HEAD` holds the retained heading and its pointer, and there is
  nothing left in the parent to compare against.

The check detects both and appends the explanation to any failure it reports, so a confusing mismatch names
its own cause. The already-forked hint wins when both apply, being conclusive where dirtiness is only likely.
Neither fires on success: a dirty parent whose edits fell outside the moved section compares perfectly well,
and warning anyway would put a hint on every fork.

**Commit the parent's pre-fork state before forking.** That is what makes `--since` usable at all, and it is
the one preparation step this check needs. Without it the tool can only tell you *why* it cannot verify the
relocation, which is better than a bare mismatch and still not a verification.

Exit 1 on contract errors; exit 0 on warnings, because ceilings never block.

MUST establish two things before running: the interpreter, with `command -v python3`, and the script itself,
by confirming `<skill-dir>/scripts/check_corpus.py` exists. When either is missing, say the checker was
skipped, name which one was absent, and perform the checks by reading — NEVER claim they ran, and NEVER read a
`No such file` as a clean corpus.

The generated index carries a marker comment. The script refuses to overwrite an index file that lacks it, so
a hand-written file is never silently destroyed.

## Anti-patterns

- Clearing a lock, or proposing "unlock, edit, relock" as a workflow.
- Combining relocation and revision into one fork.
- Rewriting a body sentence and calling it an amendment.
- Appending an amendment without the inline marker at the affected point.
- Auto-detecting the mode instead of asking, or asking without presenting the evidence.
- Applying this contract inside a repo that declared house convention.
- Minting a document type or an ownership claim the user never confirmed.
- Filling every heading of a template because an empty section looks like an omission.
- Introducing a sidecar metadata file, a central topic registry, or a hand-typed index.
- Presenting `handling` as a security control, dropping it across a fork, or routing around it quietly.
- Blocking on a length ceiling, or warning about one without naming the section to extract.
- Auditing the corpus when nothing blocked the operation at hand.
- Recording a mode declaration that names no trigger and no enforcement surface.
- Claiming a rule is enforced when no enforcement surface exists.
- Claiming the checker ran when `python3` was never probed or the script was never located.
- Invoking the checker by a working-directory-relative path instead of resolving it against the skill.
- Treating `locked` as a lifecycle value, or `superseded` as permission to edit.

## Pre-delivery checklist

- [ ] The mode in force was read or asked, and recorded where the repo keeps agent instructions.
- [ ] The recorded declaration names a trigger and an enforcement surface, or says advisory-only.
- [ ] Every document touched carries `type`, `lifecycle` and at least one `owns` claim.
- [ ] `superseded-by` is present on every superseded document and absent everywhere else.
- [ ] No lock was cleared, and any lock set was explicitly confirmed in-session.
- [ ] Every fork happened in two steps, and the relocated text is byte-identical.
- [ ] Every amendment entry has a marker at every point it invalidates.
- [ ] No type and no ownership claim was minted without confirmation.
- [ ] The index was regenerated from declarations, not edited by hand.
- [ ] The checker ran and its errors are resolved, or its absence was reported.
- [ ] Warnings named specific sections; no warning left the remedy to the reader.
- [ ] No placeholder text remains (TODO, FIXME, xxx).
