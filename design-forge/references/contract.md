# The corpus contract

Full field reference, the mode declaration, per-type rules, the section catalogue, and placement.
`SKILL.md` carries the summary; this file carries the detail and the failure modes.

- [Frontmatter fields](#frontmatter-fields)
- [The mode declaration](#the-mode-declaration)
- [Per-type rules](#per-type-rules)
- [Section catalogue](#section-catalogue)
- [Placement and naming](#placement-and-naming)
- [Worked examples](#worked-examples)

## Frontmatter fields

| Field | Required | Shape | Answers |
|---|---|---|---|
| `type` | always | freeform name | What kind of document is this? |
| `lifecycle` | always | `draft`, `active`, `stale`, `superseded` | Is this still authoritative? |
| `owns` | always | list of names, at least one | What content does this document claim? |
| `locked` | optional, default `false` | boolean | May this be edited? |
| `superseded-by` | iff `lifecycle: superseded` | path relative to the document | Where did authority go? |
| `supersedes` | optional | list of paths | What did this replace? |
| `handling` | optional | one of three fixed values | May this content leave the corpus? |

Nothing else. An unknown key is a warning rather than an error, because a repo may carry its own
metadata — but this skill's operations read only the fields above, and an unknown key MUST NOT be
treated as enforcement.

### `lifecycle` and `locked` are orthogonal

They answer different questions and come apart in both directions.

| | `locked: false` | `locked: true` |
|---|---|---|
| `active` | Design in flight | **The normal frozen case** |
| `superseded` | Old document left editable, usually a mistake | Retired and frozen |

`locked` is what gates an agent's write. `lifecycle` is what tells a reader whether to believe the
document. Collapsing them into one enum loses the ability to ask "is this still true?" separately from
"may I change it?".

There is deliberately no lifecycle value for "finished". A document that is complete and still true is
`active` and `locked` — the normal frozen case. Finishing is not a claim about authority, so it is not
a lifecycle event. An evidence record that will gain no further evidence is exactly this cell.

### `owns` — the ownership claim

The root cause of two documents disagreeing is that neither declared what it owns, so an ad-hoc
subdirectory and a section inside a frozen document can both claim the same material.

- A claim is a topic name, kebab-case, stable. `fetch-mechanics`, `write-path`, `thermal-budget`.
- A claim belongs to exactly one document. The checker treats a duplicate as an error.
- Claims are **human-minted**. Propose freely; never create one unilaterally.
- When content forks out, **the claim moves with it**. The parent stops claiming jurisdiction.

**Size a claim to what a fork would move.** The fork protocol carries the claim out with the content,
so a claim that cannot move alone is the wrong size. In practice this is a top-level section: a
document with three forkable sections declares three claims. A document with one subject declares one
claim. NEVER mint a claim per heading — a claim nothing could ever collide with constrains nothing.

**A heading that recurs across documents is not a claim.** Three documents each carrying
`## Open questions` is structure, not overlap — they hold different open questions. A collision is two
documents claiming the same *subject matter*, which is why claims are minted from what a document is
about and never from its headings.

There is no central registry mapping topics to documents. The index is generated from these
declarations, so a registry would be a second copy that rots. Overlap is caught at fork time and by
the checker, not by a maintained vocabulary list.

### `superseded-by`

A `superseded` document with no pointer tells the reader to look elsewhere without saying where. The
checker requires the field when `lifecycle: superseded`, requires the target to exist, and rejects the
field on any other lifecycle.

Superseding does **not** change `locked`. Retirement is not permission to edit.

### `handling` — an advisory restriction, not a control

Some documents are not yours to hand around: a customer-supplied specification under obligation, a
contractor deliverable, an excerpt from a paywalled standard, a vendor datasheet. `handling` marks
them. Absent is the normal case and means nothing was declared.

| Value | Meaning |
|---|---|
| `internal` | Belongs in this repository and no further. Do not transmit it outside the machine |
| `customer-confidential` | Supplied under an obligation to a third party. Do not quote it into documents outside this corpus, and do not transmit it anywhere |
| `third-party` | Owned by someone else. Do not reproduce beyond fair citation, and do not transmit it |

**Unlike `type`, the value set is fixed.** A field whose purpose is to be a signal must not be
freeform, because a typo would silently disable it. The checker validates the spelling and rejects
anything else.

What an agent must do when a document carries any `handling` value:

- **NEVER send its content to an external service.** Web search, a fetch tool, an MCP server, and a
  research subagent that may search all count as external. Report and stop instead.
- **NEVER copy its content into a document with a weaker restriction**, including one with none.
  Content carries its restriction; a quotation launders it otherwise.
- Say out loud that the restriction stopped the operation, rather than silently routing around it.

**This is advisory and cannot be anything else. Do not treat it as a security control.** Nothing
enforces it: the agent that reads the field is the same agent that could paste the content into a
search query, and the checker verifies spelling only. It is a signal that makes the obligation visible
at the point of work, which is worth having — but a flag honoured by good intentions offers no
guarantee, and treating it as one is worse than not having it. Where a real guarantee is needed, keep
the material out of the repository.

## The mode declaration

Declared once by a human, recorded where the repo already keeps agent instructions. Paste this into
`CLAUDE.md`, `AGENTS.md`, or the repo's equivalent:

```markdown
## Design documentation contract

- Mode: imposed
- Trigger: load the `design-forge` skill before writing or restructuring anything under a corpus root
- Corpus roots: `docs/design/`
- Index: `docs/design/INDEX.md` — generated, never hand-edited
- Enforcement surface: <the command this repo already runs, or `none — advisory-only`>
- Types in use: `design`, `requirements`, `milestone`
- Ownership claims: see the generated index
```

**A trigger and an enforcement surface are both required.** A declaration with no trigger reaches
only an agent that reads the instruction file top to bottom; one that opens a design document directly
never learns a fork relocates verbatim or that the index is generated. A declaration with no
enforcement surface *reads* as enforced while nothing checks it — this skill's own anti-pattern,
reached by following this skill. `none — advisory-only` is a valid value for the second; omitting it
is not.

**Required content, not required form.** The rows above are how a bulleted declaration carries them.
An instruction file that states the trigger as the sentence opening its contract section satisfies the
requirement, and usually serves it better — a trigger at the head of the section reaches a reader who
never gets as far as the list. What does NOT satisfy it is writing the same rule twice in one file to
match this shape: two copies drift, and the one nobody reads is the one that goes stale.

**`Corpus roots:` is plural.** A repo may have more than one — a live corpus and an archive, say. Each
needs its own index line, or an explicit note that it sits below the two-document index threshold.

**Name what this repo actually runs.** That row is left as a placeholder deliberately, because it is
the one row that fails silently when it is wrong: a pasted-in runner name reads as enforcement while
nothing runs. Every other row fails loudly. A pre-commit hook, a `make` target, an npm script, a
`just` recipe, a CI job — all are enforcement surfaces. What matters is that the named command
exists, that it invokes the checker, and that something already runs it without being asked. A
command nobody invokes is not a surface, and naming one that does not exist is the same failure as
naming none. NEVER invent a runner the repo does not have: where nothing suitable exists,
`none — advisory-only` is the honest value.

For a repo that keeps its own convention:

```markdown
## Design documentation contract

- Mode: house convention
- Trigger: load the `design-forge` skill before forking, locking, amending or superseding a document
- The existing layout under `doc/` is authoritative. Do not restructure it.
- Enforcement surface: none. The lock, amendment and fork protocols still apply, advisory-only.
```

House convention is *their* contract, and we comply. It is not this contract with enforcement turned
off. The operations still apply, because they are structure-agnostic — a fork leaves a pointer whether
or not the repo has frontmatter.

## Per-type rules

Types are freeform, so the rules attached to each type live in the mode declaration next to the type
list. This keeps one source of truth and makes the rules readable by a human opening `CLAUDE.md`.

```markdown
- Types in use:
  - `design` — the durable shape. MUST NOT carry an implementation plan.
  - `requirements` — atomic requirements only, per `references/authoring.md`.
  - `milestone` — perishable. Plans, task lists, sequencing. Expected to go `stale`.
```

The `design` rule above is the worked example from a real corpus: a document titled "design **and
implementation plan**" announced in its own title that it owned two lifecycles, and grew past 2400
lines because the perishable half kept accreting into the durable one.

Freeform types are **reversible and expected to tighten.** They were chosen because no adequate fixed
vocabulary existed yet, not because a fixed set is wrong. When real use supplies the vocabulary,
narrow the list.

## Section catalogue

Recommended starting points, **never a template to fill**. An absent or empty section is a correct and
complete state. Delete any heading with nothing under it.

**The catalogue covers `design` and `requirements` only.** Types are freeform, so most corpora mint
types it says nothing about — `evaluation`, `milestone`, `explainer`. That is expected: a minted type
gets its rule in the mode declaration, not a section list here. Do not read the two catalogues below
as the menu of available types.

For `design`:

- Goal
- Decisions inherited, not reopened
- Decisions made here
- The shape
- Boundaries
- Risks and traps
- Open questions
- Amendments *(append-only, grows over the document's life)*

For `requirements`:

- Purpose and scope
- Definitions *(only when a term is genuinely contested)*
- Requirements *(atomic schema — see `references/authoring.md`)*
- Interfaces
- Constraints and assumptions
- Verification
- Open questions
- Amendments

A 43-heading standard template plus an agent told to keep the document complete produces a document
where every leaf is filled, because an empty heading reads as an omission. That is a bloat mechanism,
not a thorough document. The catalogue above is deliberately short for the same reason.

## Placement and naming

**Split directories by lifecycle, not by topic.** Design is durable; milestone directories hold the
perishable. A `m1/` directory beside `design.md` is correct. A `fetching/` directory beside it is a
second ownership hierarchy competing with `owns`.

**Name a document after the claim it owns.** `capture-and-fetch.md` owning `fetch-mechanics` is
legible; `notes-2.md` is not.

**The index exists from document two.** Not at a size threshold — its job is stating relationships,
and a relationship exists as soon as a second document does.

**Non-markdown artifacts are owned, not declared.** A diagram, an exported spreadsheet or a
customer-supplied PDF is content that some markdown document owns and points at. It carries no
frontmatter and needs none. Never add a sidecar metadata file: it is a second source of truth nobody
is forced to update, and the stale copy wins by default.

The known limit, accepted deliberately: an artifact no document claims is invisible to the contract.
Report it as an incident when one blocks the operation at hand; do not sweep for them.

## Worked examples

A frozen design that has forked one aspect out:

```yaml
---
type: design
lifecycle: active
owns:
  - vault-shape
  - write-path
locked: true
---
```

The child it forked:

```yaml
---
type: design
lifecycle: draft
owns:
  - fetch-mechanics
---
```

A retired predecessor:

```yaml
---
type: requirements
lifecycle: superseded
owns:
  - legacy-import
locked: true
superseded-by: import-v2.md
---
```

And its replacement:

```yaml
---
type: requirements
lifecycle: active
owns:
  - import-pipeline
supersedes: [import-v1.md]
---
```

Note that `owns` differs across the supersession. The claim was renamed with the redesign, which is
allowed — but the rename is a minting event, so a human confirms it.
