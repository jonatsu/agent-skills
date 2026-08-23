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

### `owns` — the ownership claim

The root cause of two documents disagreeing is that neither declared what it owns, so an ad-hoc
subdirectory and a section inside a frozen document can both claim the same material.

- A claim is a topic name, kebab-case, stable. `fetch-mechanics`, `write-path`, `thermal-budget`.
- A claim belongs to exactly one document. The checker treats a duplicate as an error.
- Claims are **human-minted**. Propose freely; never create one unilaterally.
- When content forks out, **the claim moves with it**. The parent stops claiming jurisdiction.

There is no central registry mapping topics to documents. The index is generated from these
declarations, so a registry would be a second copy that rots. Overlap is caught at fork time and by
the checker, not by a maintained vocabulary list.

### `superseded-by`

A `superseded` document with no pointer tells the reader to look elsewhere without saying where. The
checker requires the field when `lifecycle: superseded`, requires the target to exist, and rejects the
field on any other lifecycle.

Superseding does **not** change `locked`. Retirement is not permission to edit.

## The mode declaration

Declared once by a human, recorded where the repo already keeps agent instructions. Paste this into
`CLAUDE.md`, `AGENTS.md`, or the repo's equivalent:

```markdown
## Design documentation contract

- Mode: imposed
- Corpus root: `docs/design/`
- Index: `docs/design/INDEX.md`
- Types in use: `design`, `requirements`, `milestone`
- Ownership claims: see the generated index
```

For a repo that keeps its own convention:

```markdown
## Design documentation contract

- Mode: house convention
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
