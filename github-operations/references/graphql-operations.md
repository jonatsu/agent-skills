# GraphQL operations

Load this when a task needs something `gh` has no subcommand for, or when a
`--json` field you expected does not exist. For ordinary PR and issue work, use
`gh` — it is shorter, and reaching for GraphQL first is the common overreach.

This file does NOT restate the GraphQL schema. GitHub's schema is introspectable
and versioned, and a copy here would be wrong from the next release. What follows
is the shape of the work and the steps people miss.

## Everything starts with a node ID

Almost every mutation takes opaque node IDs rather than numbers, so the first
call is always a query that trades the human-readable identifier for the ID:

```bash
gh api graphql -f query='
  query($owner:String!, $repo:String!, $number:Int!) {
    repository(owner:$owner, name:$repo) {
      issue(number:$number) { id title }
    }
  }' -F owner=OWNER -F repo=REPO -F number=123 --jq '.data.repository.issue.id'
```

Two things bite here:

- **`-f` and `-F` are not the same.** `-f` sends a string; `-F` interprets the
  value by type, which is what an `Int!` or `Boolean!` variable needs. Passing a
  number with `-f` yields a type error that reads as a schema problem.
- **Node IDs are opaque and not stable across resource types.** Do not construct
  one, cache one across a rename, or assume the ID of an issue is usable where a
  PR ID is wanted — a PR is also an issue in some contexts and not in others.

## Discovering the schema instead of guessing

The schema answers questions about itself, which is faster than searching docs
and cannot go stale:

```bash
gh api graphql -f query='{ __type(name:"PullRequest") { fields { name } } }' \
  --jq '.data.__type.fields[].name'
```

Use this when a mutation reports an unknown field or argument. It is also how you
check whether a feature has reached GraphQL at all before concluding it is
impossible.

## Errors arrive with HTTP 200

The API returns HTTP 200 with an `errors` array and a partial `data` object
beside it. **`gh` handles that case for you, and it is not the one to worry
about.** Measured on gh 2.98.0, 2026-08-26, querying a nonexistent repository:

- exit status **1**,
- the message on **stderr** (`gh: Could not resolve to a Repository...`),
- the raw body on stdout with `--jq` **not applied at all**.

So a `.data`-shaped `--jq` filter never runs on the error path, and an
`if .errors then error(…)` guard never fires. Checking the exit status is
sufficient here.

**The real fail-open is one level down, in mutations.** A mutation that rejects
its input returns `userErrors` INSIDE the payload with no top-level `errors`
array — so the request is a success by every outer measure, `gh` exits **0**, and
the mutation did nothing. In a file about mutations, that is the check that
matters:

```bash
gh api graphql -f query='mutation {...}' --jq '.data.<mutationName>.userErrors'
```

Empty array means it took effect. Anything else means it did not, whatever the
exit status said. MUST request `userErrors { field message }` in every mutation
you write — a mutation that does not ask for them cannot report them.

## Pagination is not optional

Connections return the first page and a `pageInfo`, and nothing signals that more
exist unless you ask. A query returning 100 review threads on a PR with 250 is a
correct response to the question you asked. Request `pageInfo { hasNextPage
endCursor }` on every connection and loop until it is false, or accept that the
result is a lower bound and say so.

## Rate limiting is by query cost, not by call count

GraphQL charges a computed cost per query against a separate budget from REST
(both 5000 in the measured run — see `SKILL.md`). A deeply nested query over many
connections can cost far more than several flat ones. Ask what a query costs
before running it in a loop:

```bash
gh api graphql -f query='{ rateLimit { limit cost remaining resetAt } … }' --jq '.data.rateLimit'
```

Including `rateLimit` in the query itself reports the cost of that same query.

## Operations known to need GraphQL

**This list is short and shrinks.** Measured on gh 2.98.0, 2026-08-26:

| Operation | Needs GraphQL? |
|---|---|
| Resolve or reply to a review thread | **Yes** — `gh pr review` has no resolve verb |
| Link a sub-issue | **No** — `gh issue edit --add-sub-issue`, `gh issue create --parent`, since v2.94.0 |
| Add a PR to a merge queue | **No** — `gh pr merge` enqueues when the target branch requires a queue |
| Read `mergeStateStatus` | **No** — `gh pr view --json mergeStateStatus` |

The last three are all widely documented as GraphQL-only. **Re-measure before
writing a mutation**, and measure the SUBCOMMAND help, not the noun's — `gh issue
--help` has zero occurrences of "sub-issue" while `gh issue edit --help`
documents two flags for it, which is precisely how the wrong answer above gets
produced with a real measurement behind it:

```bash
for c in $(gh <noun> --help 2>&1 | awk '/AVAILABLE COMMANDS/{f=1;next} f&&NF{print $1}'); do
  gh <noun> "$c" --help 2>&1
done | grep -i "<the thing you want>"

gh pr view --json 2>&1 | head -20   # prints the valid field list on error
```
