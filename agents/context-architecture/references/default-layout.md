# The Named Default Layout

The default documentation organization for a repository with no established layout. It is a default, not
doctrine: an existing repository's conventions always win, and a directory is created on first need, never
for completeness. The names below are prescribed so that layouts stay identical across repositories and walk
tests stay comparable. Other skills that write documents fall back to this layout when the repository has no
convention and the user names no place.

## Contents

- The good-enough starting point
- What a subtree earns, and when
- Genre table
- Where a new document goes
- The floor contract
- Lazy growth order
- Lifecycle duties

```text
AGENTS.md              # the floor: always-loaded rules + routing index (CLAUDE.md -> AGENTS.md symlink)
TODO.md                # open-work ledger, incl. decisions closed on evidence so they are not re-litigated
BACKLOG.md             # wanted work nothing depends on yet; splits off TODO.md when deferrals accumulate
docs/
  README.md            # the hub: one routing index, one entry per genre, reached from the floor
  reference/           # living "how it works now" write-ups; resync to code
  how-to/              # recipes for recurring tasks; updated in place
  specs/               # accepted intended behavior and its proposed revisions
  decisions/           # frozen, dated decision records (ADR-like); amended, never rewritten
  plans/               # design and implementation plans for work not yet (fully) built
    archive/           # finished or abandoned plans, kept for their rejected alternatives
  working-notes/       # live per-lane execution state: progress, open questions, findings
  research/<subject>/  # dated research corpora behind a body of work, each with its own index
  evaluations/         # dated evidence records of assessments: reviews, tests, measurements
  findings/            # symptom-indexed evidence tier: gotchas, non-obvious failure modes, recovery steps
  archive/             # retired documents of every other genre; reference only, never resynced
<subtree>/AGENTS.md    # scoped instructions, only where a subtree's conventions genuinely diverge
<subtree>/README.md    # a subtree index, only when a reader must choose between its files
```

`TODO.md` and `BACKLOG.md` are root ledgers: self-justifying by name and exempt from routing, which is why
they are named here rather than left to improvisation. A ledger under a different name needs a floor route.

## The Good-Enough Starting Point

For a repository with nothing, three genres beat nine. Everything else arrives through the growth order below.

```text
AGENTS.md              # floor: identity, never-miss rules, one routing index, commands
README.md              # humans
TODO.md                # open work
docs/
  README.md            # hub: one entry per genre, and what each genre may not mix with
  findings/
    README.md          # symptom index
  plans/
    README.md          # lifecycle: where an active plan lives, the archive trigger, what must not be archived
    archive/
  decisions/           # dated, frozen
```

Two rules keep it working, and both are cheap now and expensive later:

- **A directory's index is created in the same change as the directory.** An index retrofitted once the floor
  is already over budget gets written to fit a word count rather than to route.
- **The floor routes to `docs/README.md` and to nothing beneath it**, except symptoms an agent meets while
  already in trouble and that belong to no subtree. Those keep a direct floor route; see
  `agents-context-docs` for that split.

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
| `docs/how-to/`        | Updated in place whenever the procedure changes                           | Describes a current procedure; live tooling outranks | Task stops recurring → archive                        |
| `docs/specs/`         | Proposed until accepted; revisions expose affected downstream artifacts   | Accepted intended observable behavior within scope   | Behavior retires or a successor replaces it → archive |
| `docs/decisions/`     | Frozen at write time; dated `## Amendments` section, body never rewritten | Records why; never blocks a new decision             | Never; superseded ones gain amendments                |
| `docs/plans/`         | Living while the work is unbuilt; diverges from reality after             | Proposal only; built code outranks it                | Work completes or is abandoned → `plans/archive/`     |
| `docs/working-notes/` | Continuously, by the lane that owns it; states its own status up top      | Session state; advisory to other lanes               | Lane closes → archive                                 |
| `docs/research/`      | Added to while its question is open; each dated file frozen once written  | Evidence behind a decision; never binding by itself  | Question settles → corpus stays, marked closed        |
| `docs/evaluations/`   | Frozen at write time; a record, never a ledger — it tracks no status      | Evidence; later measurements supersede               | Never                                                 |
| `docs/findings/`      | Entries added on discovery, pruned when fixed upstream or disproven       | Advisory; verify against current state before acting | Per-entry, at consolidation                           |
| Scoped `AGENTS.md`    | As the subtree's conventions change                                       | Binding within its subtree; narrower wins            | Subtree converges with root                           |
| `docs/archive/`       | Never; a retired document keeps its text and gains a retirement banner    | None; history only                                   | Never                                                 |

The user's current instruction outranks stored guidance. For descriptive claims, the repository is right when
documentation disagrees with it. An accepted specification instead governs intended observable behavior within its
scope; disagreement with current code is a gap to reconcile, not automatic evidence that the requirement is stale.

## Where a New Document Goes

Place a document by the question it answers. Each directory below says when a document belongs there and how
to write it there; the directory's own `README.md` indexes what it holds.

- **`reference/`: how does this work now?** A description of a component, interface, or data model that a
  reader needs to understand before changing it. One subject per file, named for the subject. Record what each
  non-obvious fact was verified against, and update the file in the same change as the code it describes.
- **`how-to/`: what are the steps to do this again?** The commands for a task that recurs, such as deploying,
  rotating a secret, restoring a backup, or releasing. Write numbered steps, each with its command and the check
  that shows it worked, and link the reference or decision that explains why. Update it in place when the
  procedure changes. A procedure run once is not a how-to; it belongs in the working notes of the work that
  ran it.
- **`specs/`: what must the system do?** Accepted intended behavior. Use `<name>.md`, or `<name>/index.md`
  with children for a large specification, and state its status (proposed or accepted) at the top.
- **`decisions/`: what did we choose, and why?** A settled choice that is expensive to reverse or likely to
  be re-proposed. Use zero-padded sequential files such as `0007-store-reports-in-object-storage.md`. Freeze
  the body once written; a later change adds a dated `## Amendments` entry or a new record that supersedes it.
- **`plans/`: how will we build this?** A design or implementation plan for work not yet fully built, named
  `<name>-design.md` or `<name>-implementation-plan.md`, with its status at the top. Moving it to
  `plans/archive/` is the last step of finishing or abandoning the work. The archive keeps its rejected
  alternatives, which stop old ideas from being re-proposed.
- **`working-notes/`: where does this work stand right now?** The live state of work that spans sessions,
  agents, or lanes: progress, decisions taken along the way, what was tried, open questions, and the next
  step. Create the file when the work starts, not when it ends, as `<lane>.md` named for the work, with a
  status line at the top: active, paused, or done, and the date last updated. List each active file in
  `working-notes/README.md`, and link it from the plan it executes. Update it at every boundary: a slice
  landing, a pause, a handoff. When the work closes, promote what lasts to `findings/`, `decisions/`, or
  `reference/`, then move the file to `archive/`. Working notes are committed; throwaway scratch output that
  may vanish belongs in the repository's untracked scratch space instead.
- **`research/<subject>/`: what did we learn before deciding?** Evidence gathered toward a question: source
  comparisons, surveys, measurements, and notes on third-party material. One directory per subject, with a
  `README.md` stating the question, its status, and an index of dated files. Hold our summaries and short quoted
  excerpts with citations, never vendored copies of third-party sources. The decision or plan that the research
  informs links back to it.
- **`evaluations/`: what did an assessment show, on one day?** A dated record of a review, trial, test run,
  or measurement, named `YYYY-MM-DD-<subject>.md`. Never rewrite one to match a newer observation; write a new
  record instead. Research asks a question before a choice; an evaluation judges something that exists.
- **`findings/`: what goes wrong, and how is it recovered?** One non-obvious failure mode, gotcha, or recovery
  procedure per file, reached from a symptom index. Prune an entry once it is fixed upstream or disproven.
- **`archive/`: what did we retire?** A document of any genre except plans that has left live use. Keep its
  filename and text, and add one line at the top stating when and why it was retired and what replaced it.

## The Floor Contract

`AGENTS.md` carries, in order: an identity paragraph (what this repository is, three to five lines), the hard
rules (each traceable to a failure it prevents), the routing index, the commands block, and an update-triggers
table (when X changes, touch Y — freshness is part of done-ness). Use one list item per route:

```markdown
- Read when <condition>: [<document>](<path>.md) <purpose>.
```

The leading phrase, condition, and Markdown link must remain on the first physical line. Use `Read when`,
`Symptom`, `Read before`, or `If you`; the checker treats another phrase as ordinary prose. Routing tables
remain supported when a compact matrix earns coupled formatting, but their exact headers are a compatibility
contract rather than the default. [Writing rules](writing-rules.md) defines both forms.

Every living document the system wants found has a structural route from this index. Give a destination a
direct entry only when the floor reader must choose it there; route a related group through one focused index
when separate entries would tax unrelated sessions. The trigger is a condition, not a topic.

Once `docs/working-notes/` exists, the floor carries it as a hard rule, not only a route: "Keep the state of
multi-step work in `docs/working-notes/<lane>.md`, listed in its README." An agent writes working state
without first asking where it belongs, so a route it never follows leaves notes scattered where no later
session, or person, can find them.

## Lazy Growth Order

A small repository is complete with the floor alone. Add, in each case on first need:

01. `docs/reference/` — when a how-it-works nuance outgrows a floor line.
02. `docs/how-to/` — when a recurring task's commands outgrow the floor's commands block.
03. `docs/specs/` — when accepted intended behavior needs a durable contract across design or implementation work.
04. `docs/findings/` — on the first non-obvious gotcha worth keeping; add a symptom → file index (in the floor
    or a dedicated index file) at the same time, because an unindexed finding is unreachable at need. This is
    the specific case of the general rule: **every directory added here gets its index in the same change.**
05. `docs/decisions/` and `docs/plans/` — on the first design question that gets settled or scoped.
06. `docs/working-notes/` — when multi-session or multi-lane work needs durable state; add the floor rule
    from the floor contract in the same change.
07. `docs/research/<subject>/` — when evidence gathered toward a question is worth keeping past the session.
08. `docs/evaluations/` — on the first recorded assessment (the first walk test creates it).
09. An architecture map — only when "how does this fit together" questions outgrow the floor's identity
    paragraph. Give it a section index with stable anchors (`§N`, frozen forever once assigned).
10. `docs/archive/` — on the first retirement of a document other than a plan. Archive rather than delete
    anything still revivable.
11. Scoped `AGENTS.md` files — only on genuine divergence, never as decoration.

Conditional additions that are never part of the default: a changelog (add when change history stops being
recoverable from commit messages alone), repository-local skills (route through `skill-forge`; add a floor
routing entry for each), and generated documents (each needs a named generator, a regenerate command in the
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
