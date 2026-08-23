---
name: design-forge
description: Requirements and design documentation as an enforced corpus contract — frontmatter lifecycle, ownership claims, lock semantics, length ceilings, and the operations over them (create, lock, amend, fork-with-pointer, supersede, convert an existing docs tree). Use when writing or revising a requirements or design document, when a document or section has grown too long, when a design should be frozen, when settled content needs changing, when a section should become its own document, or when an existing docs tree needs bringing under the contract. Triggers — 'write requirements', 'requirements doc', 'SRS', 'design doc', 'freeze this design', 'lock this document', 'supersede this', 'amend this', 'fork this section out', 'split this document', 'convert these docs', 'system requirements', 'hardware requirements'. Covers software, system and hardware. NOT for brainstorming an unshaped idea, which is idea-forge. NOT for pressure-testing a written plan, which is grilling. NOT for ADRs or changelogs.
metadata:
  author: Joonas Onatsu
  license: MIT
---

IRON LAW: A LOCKED DOCUMENT MAY GAIN ANNOTATIONS THAT REDIRECT AUTHORITY, AND NOTHING ELSE. NEVER
change the meaning of settled content, and NEVER clear a lock — not to edit and relock, not because
the user "clearly wants this updated". Unlocking is a manual, out-of-band human edit, and its friction
is deliberate.

Red flags (stop and re-read the Iron Law if any appear):

- Reaching for `locked: false` on a document you are about to edit.
- A fork whose moved text is not byte-identical to what left the parent.
- Rewriting a body sentence instead of appending an amendment and marking the affected point.
- Using a document type or an ownership claim the user never minted.
- Producing an audit of everything wrong with the corpus when nothing actually blocked you.
- Applying this skill's own structure to a repo that declared house convention.

## What this governs

A **corpus contract** — how a set of requirements and design documents declares its own structure —
and the **operations** over it. The contract is negotiable; the operations are not. Fork-with-pointer,
the lock protocol, the amendment rules and the length ceilings are structure-agnostic and apply
unchanged inside somebody else's layout.

Domain is a parameter, not a second contract. Structure rules do not change because the subject is a
PCB. What changes is content vocabulary.

### Reference files

Load on demand at the point of need, never up front. Each costs context the operation at hand may not
need, and the protocols in this file are complete without them.

| File | Load when | Do NOT load |
|---|---|---|
| `references/contract.md` | Minting a type or an ownership claim, writing the mode declaration, or checking a field's exact semantics | A routine amend, fork or lock — those protocols are complete below |
| `references/conversion.md` | Converting an existing corpus, after the survey has run | Any single-document operation |
| `references/authoring.md` | Writing or reviewing the text of individual requirements | Corpus-level governance — owning a document says nothing about its requirement wording |
| `references/domains.md` | The subject is hardware or system-level | Software-only requirements. Its verification vocabulary is not the software one, and applying it there produces requirements nobody can verify |

## Workflow

Copy this checklist and check items off as they complete:

```text
Design Forge Progress:

- [ ] Step 1: Establish the contract in force ⛔ BLOCKING
  - [ ] 1.1 Read the recorded mode declaration
  - [ ] 1.2 If absent, present the evidence and ask — imposed or house convention ⚠️ REQUIRED
  - [ ] 1.3 Record the answer where the repo keeps agent instructions
  - [ ] 1.4 Name the enforcement surface, or declare advisory-only out loud
- [ ] Step 2: Route to the operation
- [ ] Step 3: Run that operation's protocol
  - [ ] 3.1 Mint no type and no ownership claim the user has not confirmed ⚠️ REQUIRED
  - [ ] 3.2 Check ownership claims against the index before writing
- [ ] Step 4: Regenerate the index and run the checker
- [ ] Step 5: Report incidents only — never an audit
```

## Step 1: Establish the contract in force ⛔ BLOCKING

Every check in this skill runs against **the active contract, whichever is in force** — never against
a fixed template this skill ships.

Two modes:

- **Imposed** — new designs and deliberate conversions get this skill's contract.
- **House convention** — a repo with an established convention keeps it. This is not "our contract
  with enforcement off"; it is *their* contract, and we comply.

Mode is **declared once and recorded** where the repo already keeps agent instructions (`CLAUDE.md`,
`AGENTS.md`, or the repo's equivalent). Evidence informs the question; a human answers it.

**NEVER auto-detect the mode.** The false positive is the dangerous direction: a tree with seven
documents, consistent naming and a milestone subdirectory scores as "established convention" under any
plausible detector, and the detector then blesses as canonical the very structure that needed fixing.

Where no enforcement surface exists — documents that cannot carry frontmatter, or a house convention
with no machine-readable field — **say so and run advisory-only**. Announced degradation beats silent
pretence. The named failure this prevents is an agent claiming a rule is in force while enforcing
nothing.

## Step 2: Route to the operation

| The user wants | Operation |
|---|---|
| A new requirements or design document | **Create** |
| A design frozen — shared understanding reached | **Lock** |
| One wrong sentence or paragraph corrected in settled content | **Amend** |
| A section that has outgrown its document, or an aspect that needs real revision | **Fork** |
| The whole document replaced | **Supersede** |
| An existing docs tree brought under the contract | **Convert** |

Amend and Fork are the two answers to "this locked document is wrong". Amend is for a sentence; Fork
is for an aspect. If unlocking looks like the answer, the operations layer is being asked the wrong
question — re-read the routing table.

## The contract

**Frontmatter is the enforcement surface.** Machine-readable beats prose, because every failure this
skill exists to fix is a rule that existed with no enforcement surface.

```yaml
---
type: design            # REQUIRED — freeform, human-minted
lifecycle: active       # REQUIRED — draft | active | stale | superseded
owns:                   # REQUIRED — at least one claim
  - fetch-mechanics
locked: true            # OPTIONAL — defaults to false
superseded-by: new.md   # REQUIRED when lifecycle is superseded, forbidden otherwise
supersedes: [old.md]    # OPTIONAL — back-link
---
```

- `lifecycle` answers *is this still authoritative?*
- `locked` answers *may this be edited?* — **an orthogonal flag, never a lifecycle value.** The two
  come apart in both directions: a design can be `active` and locked (the normal case), or
  `superseded` and locked. `locked` is what gates an agent's write.
- `owns` is the self-declared list of claimed topics. **The index is generated from these
  declarations, never hand-typed.**
- `type` is freeform, with rules attached per type in the contract declaration. This is deliberate and
  reversible, chosen because no adequate fixed vocabulary existed yet. Expect it to tighten.

**Minting is human.** An agent MAY use an existing type or ownership claim freely and MAY propose new
ones, but creating either is the user's call — one confirmation, since the two events usually
coincide. Without that gate, freeform types degenerate into per-document config and the contract stops
constraining anything.

**An absent or empty section is a correct and complete state.** NEVER fill a heading to avoid leaving
it empty; delete the heading instead. An agent told to keep a document complete will fill every leaf
of a large template, and that is the mechanism behind documents nobody can read.

**Non-markdown artifacts do not carry frontmatter and do not need it.** A diagram, an exported
spreadsheet or a customer-supplied PDF is content that a markdown document owns and declares. NEVER
introduce a sidecar metadata file — it is a second source of truth nobody is forced to update, and the
stale one wins by default.

Load `references/contract.md` for the full field reference, the mode-declaration format, per-type rule
declarations, and the document section catalogue.

## Operations

### Lock ⚠️ REQUIRED confirmation

An agent MAY propose a lock and MAY set it on explicit in-session confirmation. **An agent may NEVER
clear one.** Setting is low-risk; clearing is the entire guard.

The lock point is *shared understanding reached and user-confirmed* — not a date, not a phase.

What the lock forbids is changing the **meaning** of settled content. It permits **meaning-preserving
annotation**, and only that. This is forced by the fork case: leaving a pointer in the parent is an
edit to a locked document, so `locked` cannot mean immutable.

When asked to unlock, report and stop. A locked document that needs to change is the amendment case or
the fork case. If unlocking starts to look routine, say so — that is evidence the operations layer is
inadequate, and surfacing it is the point of the friction.

### Amend

Trigger: one wrong sentence or paragraph, where forking would be absurd overhead.

1. Append an entry to a `## Amendments` section at the end of the document. **The body is never
   rewritten.**
2. Add an inline marker `[amended A<n>]` at the affected sentence or paragraph. **Not optional** —
   without it a reader hits the stale sentence with no signal to look further, and an amendment nobody
   finds is worse than none, because the document now looks maintained.

```markdown
## Amendments

### A3 — Fetch timeout is 30 seconds, not 10
The figure under "Fetch mechanics" was measured against the wrong endpoint. Thirty seconds is the
observed p99 including redirects.
```

Every `### A<n>` MUST have exactly one matching `[amended A<n>]` in the body. The checker verifies
this mechanically.

**At five amendments, warn and propose a named successor document.** Never block. A document with
fifteen amendments should have been replaced, and an append-only section grows without bound.

### Fork ⚠️ REQUIRED confirmation

**Fork and revise are two distinct steps, never one.**

1. **Verbatim relocation.** The aspect moves out byte-identical to what left. The locked parent gains a
   pointer. The new document gets its own frontmatter, `lifecycle: draft`, unlocked, and the ownership
   claim that moved with it.
2. **Revision**, in the new document only, as a separate visible step.

The testable form: **after the relocation, the parent plus the new document together must still say
what the parent said** — nothing dropped, added, or altered in the move.

NEVER combine the steps. "Fork it out and rewrite it" looks like relocation going in and is a rewrite
coming out, and nothing can tell afterwards. When asked for both, do them as two steps the user can
see.

The pointer in the parent:

```markdown
> Authority on fetch mechanics moved to [capture-and-fetch.md](capture-and-fetch.md).
```

**Authority transfers with the content.** The pointer means *this content now lives at X*, not *this
content is still true*. The locked parent stays honest not by staying correct but by no longer
claiming jurisdiction.

The pointer and the amendment marker are **the same primitive** — an in-body annotation that redirects
authority without altering a claim. One rule, two uses.

### Create

1. Ask which type and which ownership claims, minting per the rule above.
2. Check the claims against the index. A collision is an incident — report it and ask; do not pick.
3. Write the frontmatter first, then the body.
4. Place by lifecycle, not topic: design is durable, milestone directories hold the perishable. A
   document whose title announces two lifecycles ("design **and implementation plan**") is the defect.
5. **An index exists from document two**, not at a size threshold. Its job is stating relationships,
   and relationships exist as soon as a second document does.

### Supersede

1. The new document is created normally and takes over the ownership claims.
2. The old document gets `lifecycle: superseded` and `superseded-by: <path>`.
3. The old document's `locked` value is **unchanged**. Superseded is not a licence to edit.

### Convert an existing corpus ⚠️ REQUIRED confirmation

Conversion is a corpus-scale sequence of the fork operation, so it inherits fork's guarantees. It is
**plan, approve, then execute** — never a single rewriting pass.

Start with `check_corpus.py <dir> --survey`, which produces the Phase 1 inventory. Then load
`references/conversion.md` before going further. Do not improvise conversion from this summary.

## Length ceilings

**They warn and propose. They never block.** A skill that refuses to work is a skill that stops being
invoked.

| Scope | Threshold | Response |
|---|---|---|
| Section | ~150–200 lines | Primary trigger — warn and name the section to extract |
| Document | ~1000 lines | Backstop warning for death by a thousand sections |
| Document | ~2000 lines | Backstop limit — propose a split plan, still never block |

Section length is primary because a document-level count arrives too late to be actionable and cannot
say *what* to extract. At 200 lines a fork is cheap; at 1000 it is surgery across many
cross-references.

**A warning MUST carry a specific fork proposal naming the section.** A warning that leaves the reader
to find the remedy is noise.

## Reporting

**Incident-driven, never an audit.** The trigger is *"I would have to guess to proceed"*, not *"this
looks bad"*. A general audit becomes a nag, and a nag trains the reader to skim past everything
including the one report that mattered.

| Trigger | Response |
|---|---|
| Repo or convention quality | Report, take the conservative option, name the assumption, proceed |
| Genuine ambiguity in the operation at hand | Ask — choosing would invent the user's decision |
| Corpus is messy | Never refuse to work |

"Genuine ambiguity" means **the alternatives lead to materially different outcomes and no conservative
default exists.** Where a default exists, take it and say so.

## The checker

```bash
python3 scripts/check_corpus.py <docs-dir> [--index <path>] [--quiet]
python3 scripts/check_corpus.py <docs-dir> --survey
```

The default mode validates every frontmatter block against the contract, reports ownership collisions,
verifies amendment markers, reports ceiling breaches, and regenerates the index from the `owns`
declarations. Standard library only.

`--survey` is the pre-conversion inventory: it reports each document's length, its sections with their
line counts, and which sections are fork candidates, treating absent frontmatter as expected rather
than as an error. Use it on any corpus not yet under the contract — the default mode drops a document
with no frontmatter before analysing it, which is useless on exactly the corpus that needs the help.

Exit 1 on contract errors; exit 0 on warnings, because ceilings never block.

MUST establish the interpreter with `command -v python3` first. When it is absent, say the checker was
skipped and perform the checks by reading — NEVER claim they ran.

The generated index carries a marker comment. The script refuses to overwrite an index file that lacks
it, so a hand-written file is never silently destroyed.

## Requirement-level authoring

Load `references/authoring.md` when writing individual requirements rather than governing the corpus —
it carries the atomic requirement schema, the identifier scheme, acceptance-criteria patterns, and the
vague-wording gate.

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
- Blocking on a length ceiling, or warning about one without naming the section to extract.
- Auditing the corpus when nothing blocked the operation at hand.
- Claiming a rule is enforced when no enforcement surface exists.
- Claiming the checker ran when `python3` was never probed.
- Treating `locked` as a lifecycle value, or `superseded` as permission to edit.

## Pre-delivery checklist

- [ ] The mode in force was read or asked, and recorded where the repo keeps agent instructions.
- [ ] Every document touched carries `type`, `lifecycle` and at least one `owns` claim.
- [ ] `superseded-by` is present on every superseded document and absent everywhere else.
- [ ] No lock was cleared, and any lock set was explicitly confirmed in-session.
- [ ] Every fork happened in two steps, and the relocated text is byte-identical.
- [ ] Every amendment entry has exactly one matching inline marker.
- [ ] No type and no ownership claim was minted without confirmation.
- [ ] The index was regenerated from declarations, not edited by hand.
- [ ] The checker ran and its errors are resolved, or its absence was reported.
- [ ] Warnings named specific sections; no warning left the remedy to the reader.
- [ ] No placeholder text remains (TODO, FIXME, xxx).
