# The Named Default Layout

The default documentation organization for a repository with no established layout. It is a default, not
doctrine: an existing repository's conventions always win, and a directory is created on first need, never
for completeness. The names below are prescribed so that layouts stay identical across repositories and walk
tests stay comparable.

```text
AGENTS.md              # the floor: always-loaded rules + routing index (CLAUDE.md -> AGENTS.md symlink)
TODO.md                # open-work ledger, incl. decisions closed on evidence so they are not re-litigated
BACKLOG.md             # wanted work nothing depends on yet; splits off TODO.md when deferrals accumulate
docs/
  README.md            # the hub: one routing table, one row per genre, reached from the floor
  reference/           # living "how it works now" write-ups; resync to code
  specs/               # accepted intended behavior and its proposed revisions
  decisions/           # frozen, dated decision records (ADR-like); amended, never rewritten
  plans/               # design and implementation plans for work not yet (fully) built
  working-notes/       # live per-lane execution state: progress, open questions, findings
  evaluations/         # dated evidence records of assessments: reviews, tests, measurements
  findings/            # symptom-indexed evidence tier: gotchas, non-obvious failure modes, recovery steps
  archive/             # anything retired from live use; reference only, never resynced
<subtree>/AGENTS.md    # scoped instructions, only where a subtree's conventions genuinely diverge
<subtree>/README.md    # a subtree index, only when a reader must choose between its files
```

`TODO.md` and `BACKLOG.md` are root ledgers: self-justifying by name and exempt from routing, which is why
they are named here rather than left to improvisation. A ledger under a different name needs a floor row.

## The Good-Enough Starting Point

For a repository with nothing, three genres beat nine. Everything else arrives through the growth order below.

```text
AGENTS.md              # floor: identity, never-miss rules, ONE routing table, commands
README.md              # humans
TODO.md                # open work
docs/
  README.md            # hub: one row per genre, and what each genre may not mix with
  findings/
    README.md          # symptom index
  plans/
    README.md          # lifecycle: where an active plan lives, the archive trigger, what must not be archived
    archived/
  decisions/           # dated, frozen
```

Two rules keep it working, and both are cheap now and expensive later:

- **A directory's index is created in the same change as the directory.** An index retrofitted once the floor
  is already over budget gets written to fit a word count rather than to route.
- **The floor routes to `docs/README.md` and to nothing beneath it**, except symptoms an agent meets while
  already in trouble and that belong to no subtree. Those keep a direct floor row; see
  `agents-management` for that split.

## What a Subtree Earns, and When

Progressive disclosure works downward as well as outward. A subtree file is not decoration, and each kind
answers a different question:

| Give it     | When                                                                                                                                               |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AGENTS.md` | the subtree has a rule an agent can violate *from outside it* — a sudo boundary, a generated tree, a deploy path. Not merely because it is complex |
| `README.md` | a reader arriving there must choose between its files and the filenames do not settle it                                                           |
| Both        | a subsystem with its own gates and its own findings: it indexes its own evidence and stops taxing the floor                                        |

The scoped `AGENTS.md` is the strongest instrument available, because it is a routing root, an evidence index,
and it loads by location. A finding owned by a subtree should never reach the root floor at all.

## Genre Table

Each genre declares its update semantics and authority. Put a document in exactly one genre; when a document
seems to need two, split it.

| Genre                 | Update semantics                                                          | Authority                                            | Dies when                                             |
| --------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------- |
| Floor (`AGENTS.md`)   | Grown from observed failures; accretion-tested                            | Binding rules + routing only                         | Never; it shrinks instead                             |
| `docs/reference/`     | Resyncs to code; wrong the moment code moves without it                   | Describes; live code outranks it                     | Subject removed → archive                             |
| `docs/specs/`         | Proposed until accepted; revisions expose affected downstream artifacts   | Accepted intended observable behavior within scope   | Behavior retires or a successor replaces it → archive |
| `docs/decisions/`     | Frozen at write time; dated `## Amendments` section, body never rewritten | Records why; never blocks a new decision             | Never; superseded ones gain amendments                |
| `docs/plans/`         | Living while the work is unbuilt; diverges from reality after             | Proposal only; built code outranks it                | Work completes or is abandoned → archive              |
| `docs/working-notes/` | Continuously, by the lane that owns it; states its own status up top      | Session state; advisory to other lanes               | Lane closes → archive                                 |
| `docs/evaluations/`   | Frozen at write time; a record, never a ledger — it tracks no status      | Evidence; later measurements supersede               | Never                                                 |
| `docs/findings/`      | Entries added on discovery, pruned when fixed upstream or disproven       | Advisory; verify against current state before acting | Per-entry, at consolidation                           |
| Scoped `AGENTS.md`    | As the subtree's conventions change                                       | Binding within its subtree; narrower wins            | Subtree converges with root                           |

The user's current instruction outranks stored guidance. For descriptive claims, the repository is right when
documentation disagrees with it. An accepted specification instead governs intended observable behavior within its
scope; disagreement with current code is a gap to reconcile, not automatic evidence that the requirement is stale.

## The Floor Contract

`AGENTS.md` carries, in order: an identity paragraph (what this repository is, three to five lines), the hard
rules (each traceable to a failure it prevents), the routing table, the commands block, and an update-triggers
table (when X changes, touch Y — freshness is part of done-ness). The routing table's shape:

```markdown
| File | What it holds | Read when |
```

The header words are part of the checker contract, not illustrative labels. A target column must be named
`File` or `Read` (case-insensitive). A trigger column must start with `Read when`, `Symptom`, `Read before`, or
`If you`. Keep that vocabulary narrow: a `Document` or `Directory` column does not establish structural
reachability merely because its cells contain links, and the checker reports such a near miss at the table.

**A table routes only when it carries both columns**, and this applies to every genre index as much as to the
floor. A target column beside a topic column — `| File | What it decided |` — describes a set of documents
without saying when to open one, which is the thing a route is for. The checker reports that near miss too,
once such a table links two or more documents, so the diagnostic lands at the table rather than surfacing later
as children that happen to be reachable by some other link.

Every living document the system wants found has a structural route from this table. Give a destination a
direct row only when the floor reader must choose it there; route a related group through one focused index
when separate rows would tax unrelated sessions. The read-when cell is a trigger condition, not a topic, and
links deeper in the route must use the structural forms in [writing-rules.md](writing-rules.md).

## Lazy Growth Order

A small repository is complete with the floor alone. Add, in each case on first need:

1. `docs/reference/` — when a how-it-works nuance outgrows a floor line.
2. `docs/specs/` — when accepted intended behavior needs a durable contract across design or implementation work.
3. `docs/findings/` — on the first non-obvious gotcha worth keeping; add a symptom → file index (in the floor
   or a dedicated index file) at the same time, because an unindexed finding is unreachable at need. This is
   the specific case of the general rule: **every directory added here gets its index in the same change.**
4. `docs/decisions/` and `docs/plans/` — on the first design question that gets settled or scoped.
5. `docs/working-notes/` — when multi-session or multi-lane work needs durable state.
6. `docs/evaluations/` — on the first recorded assessment (the first walk test creates it).
7. An architecture map — only when "how does this fit together" questions outgrow the floor's identity
   paragraph. Give it a section index with stable anchors (`§N`, frozen forever once assigned).
8. `docs/archive/` — on the first retirement. Archive rather than delete anything still revivable.
9. Scoped `AGENTS.md` files — only on genuine divergence, never as decoration.

Conditional additions that are never part of the default: a changelog (add when change history stops being
recoverable from commit messages alone), repository-local skills (route through `skill-forge`; add a floor
routing row for each), and generated documents (each needs a named generator, a regenerate command in the
floor's commands block, and a never-hand-edit marker in its header).

## Lifecycle Duties

Every durable tier needs all four stages, not just the first:

- **Capture gate:** entries are verified or labelled unverified; no secrets, no speculation, no bare
  imperatives (see [writing-rules.md](writing-rules.md)).
- **Stamp:** non-obvious facts record what they were verified against — a revision, a schema, a run — because
  that, not the write date, decides staleness.
- **Consolidation:** on a schedule or at natural breaks, deduplicate, resolve conflicts by recency of
  verification, and merge session-scoped notes into durable tiers or drop them.
- **Forgetting:** prune entries that are fixed upstream, disproven, or superseded. An append-only store
  degrades the system it serves; removal is maintenance, not loss — git history keeps the body.
