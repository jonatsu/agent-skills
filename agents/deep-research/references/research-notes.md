# The Research Notes File

The notes file is the investigation's memory. Write each entry as it happens, never from recollection at the end, and
keep dead ends and parked threads in it, because they show what the report does not cover. A note points to a source;
before relying on a load-bearing claim, figure, date, or quotation, open the source itself.

Start the file from this skeleton, and keep its sections in this order:

```markdown
# Research: <subject>

Asked: <the user's request, quoted>
Budget: <sources or time agreed, and what is spent>
Round: <current round number>

## Map

| Facet | Question it answers | Status | Evidence |
| ----- | ------------------- | ------ | -------- |

## Threads

| ID | Thread | Origin | Status | Reason | Next action |
| -- | ------ | ------ | ------ | ------ | ----------- |

## Queries

| Round | Where | Query | Result |
| ----- | ----- | ----- | ------ |

## Sources

| ID | Source | Version or date | Kind | Origin of its claims |
| -- | ------ | --------------- | ---- | -------------------- |

## Claims

| Claim | Sources | Confidence and basis | As of |
| ----- | ------- | -------------------- | ----- |
```

Fill each section this way:

- **Map:** one row per facet. Status is open, covered, or searched-none. Evidence names the source IDs.
- **Threads:** one row per thread, with the source ID it came from as its origin. Status is open, followed, dead end, or
  parked. Reason is required for a dead end or a parked thread: budget, blocked, low value, or out of scope.
- **Queries:** every search, with the index or site it ran on. Result is a count or one line, such as "3 relevant, S4
  to S6", so a repeat is easy to spot.
- **Sources:** the URL or citation, the version, commit, edition, or publication date, and whether the source is primary
  or secondary. Origin of its claims names the source it repeats, when it repeats one, so independence can be judged.
- **Claims:** each load-bearing claim with its source IDs, its confidence and the basis for it, and the date the claim
  holds as of.
