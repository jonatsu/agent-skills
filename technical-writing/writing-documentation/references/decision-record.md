# Decision Records

Read this before writing a decision record, joining an existing series, or choosing a format for a set that has
none. `SKILL.md` holds the gate that decides whether to write one.

## Match the Record's Weight to the Decision

A record that clears the gate but stays contained needs only the **light form**: a title and a few sentences
saying what was decided, why, and the main alternative rejected with its reason. Most records need no more. The
value is recording that a decision was made and why.

Use the **full form** when wide later work builds on the decision, such as a framework, dependency, data model,
protocol, authentication or authorization strategy, hosting or build platform, or cross-boundary contract. Use it
too when the rejected alternatives carry most of the weight and a reviewer needs them separable. The full form
carries five elements:

- **Status and date:** proposed, accepted, superseded, or deprecated, and when. Without a status a record cannot
  be superseded; without a date it cannot be read against the conditions that produced it.
- **Context:** the problem, requirements, and constraints in force at the time.
- **Decision:** what was chosen, plainly enough to act on.
- **Alternatives, each with the reason it was rejected:** the reason is what stops the alternative being proposed
  again. An alternative without one records that you looked, not what you learned.
- **Consequences in both directions:** what the decision obliges, what it lets the reader stop doing, and costs
  that arrive later, such as knowledge the team must acquire.

Freeze a record once it is accepted. When the decision changes, write a new record that references and
supersedes the old one, and never rewrite or delete the original. It is the evidence for why the earlier choice
was reasonable under its conditions.

## Find the Existing Convention First

An established series outranks every default here. Before writing, look for:

- records already in the repository, and the directory holding them;
- configuration naming that directory, such as an `.adr-dir` file or an `adr-tools` installation;
- the project's contributor or agent instructions; and
- a template the series was generated from.

Two or more existing records establish a convention; one establishes only voice. Where the evidence conflicts,
say so rather than introducing a third scheme.

## Numbering and Files

Continue the series exactly as it runs. Do not restart the sequence, renumber earlier records, or add a second
pattern alongside the first. Take the next number when you start writing rather than when you finish, so two
records written at once do not collide.

Common patterns appear in these forms:

| Pattern             | Example                                         |
| ------------------- | ----------------------------------------------- |
| Zero-padded slug    | `0014-store-reports-in-object-storage.md`       |
| Prefixed and titled | `ADR-014-Store-Reports-In-Object-Storage.rst`   |
| Dated               | `2026-03-11-store-reports-in-object-storage.md` |

Where no convention exists, use `docs/decisions/` with zero-padded sequential Markdown files. Match the markup
of the surrounding documentation set, not this default, when the two differ.

## Format Standards

- **Nygard**, the original short form: title, status, context, decision, consequences. Choose it when records
  should stay under a page.
- **MADR**, which adds explicit decision drivers and itemized options with their pros and cons. Choose it when
  the alternatives carry most of the weight and reviewers need them separable.

Both express the full form's five elements. Neither is better in the abstract. Match the series being joined.
For a series with no convention, start with the light form and let a record grow into one of these standards only
where its blast radius or its alternatives require it.

## Status and Supersession

A status is one of proposed, accepted, superseded, or deprecated. Superseded means another record replaced the
decision; deprecated means it no longer applies and nothing replaced it. Both keep their original body.

Record supersession from both ends: the new record names what it supersedes, and the old record's status names
what replaced it. A one-directional pointer leaves a reader who finds the old record first with no way forward.

Some sets amend rather than supersede, adding dated entries beneath a frozen body for facts that changed
without reversing the decision. Follow the set's convention where it has one, and keep the original body intact
either way.

## Worked Example

The subject here is a software decision, but the shape holds for a process or organizational one: what was
decided, under which conditions, against what alternatives, and at what cost.

```markdown
# ADR-0014: Store rendered reports in object storage

## Status

Accepted. Supersedes ADR-0009, which put rendered reports in the database.

## Date

2026-03-11

## Context

Rendered reports are stored as binary columns in the `reports` table. Three constraints now conflict:

- The largest tenants generate reports above the 40 MB row limit, and those requests fail outright.
- Nightly database backups have grown to 6 hours, most of it report bytes that are never restored on their own.
- Support needs to hand a customer a time-limited download link without proxying the bytes through the API.

The team runs one database administrator and no dedicated storage operations.

## Decision

Store rendered reports in the existing S3-compatible object store, keyed by tenant and report ID. Keep report
metadata and the storage key in the `reports` table. Serve downloads as presigned URLs with a one-hour expiry.

## Alternatives Considered

### Keep reports in the database, raise the row limit

- Pros: no migration, no second durability story, transactional consistency with metadata.
- Cons: does not address backup duration, and the row limit rises again with tenant size.
- Rejected: it defers the size problem rather than removing it, and leaves backup duration untouched.

### Write reports to a shared network filesystem

- Pros: simple file semantics, no new client library.
- Cons: needs its own replication and backup, and presigned links have no equivalent.
- Rejected: it converts an application problem into an operations one the team has no capacity to own.

### Render on demand and store nothing

- Pros: no storage decision at all.
- Cons: the largest reports take four minutes to render, and audit rules require the exact delivered artifact.
- Rejected: the audit requirement makes a reproducible re-render insufficient.

## Consequences

- Backups shrink to metadata, and their duration stops tracking report volume.
- Support links no longer proxy bytes through the API, removing that timeout class entirely.
- Report writes are no longer transactional with their metadata. A failed upload must leave no `reports` row,
  which the writer now enforces explicitly.
- Deleting a tenant requires deleting objects as well as rows. The existing deletion job gains a second step.
- The team takes on object-store lifecycle rules and access-policy review, which nobody currently owns.
```

The rejection lines carry the record. A reader who proposes a network filesystem next year finds the reason it
was declined and the condition that would change the answer, which is the capacity to operate one.
