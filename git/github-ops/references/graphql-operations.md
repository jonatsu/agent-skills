# GraphQL Operations

Load this when a task needs something `gh` has no subcommand for, or when a `--json` field you expected does
not exist. For ordinary PR and issue work, use `gh`; it is shorter, and reaching for GraphQL first is the
common overreach.

This file does not restate the versioned GraphQL schema. Use current documentation or live introspection when
the host permits it. A copied schema would drift while still reading as authoritative.

## Resolve Required Node IDs

Many mutations take opaque node IDs rather than numbers. Resolve the exact input type and then query the ID
from a human-readable identifier:

```bash
gh api graphql -f query='
  query($owner:String!, $repo:String!, $number:Int!) {
    repository(owner:$owner, name:$repo) {
      issue(number:$number) { id title }
    }
  }' -F owner=OWNER -F repo=REPO -F number=123 --jq '.data.repository.issue.id'
```

Two things bite here:

- **`-f` and `-F` are not the same.** `-f` sends a string; `-F` interprets the value by type, which is what an
  `Int!` or `Boolean!` variable needs. Passing a number with `-f` yields a type error that reads as a schema
  problem.
- **Node IDs are opaque and typed by their use.** Do not construct one or assume that an issue ID is valid
  where a pull-request or review-thread ID is required.

## Discover the Schema

Use live schema introspection when the host permits it. Query narrowly because GitHub limits repeated
introspection fields within one request:

```bash
gh api graphql -f query='{ __type(name:"PullRequest") { fields { name } } }' \
  --jq '.data.__type.fields[].name'
```

Use this when a query reports an unknown field or argument. Consult the host's current GraphQL documentation
when introspection is unavailable or restricted.

## Validate GraphQL Responses and Mutations

GraphQL can return HTTP 200 with top-level `errors` and partial `data`. `gh api graphql` currently exits
non-zero for that response, writes the diagnostic to stderr, and may leave the raw body on stdout. Preserve
the command's exit status before interpreting its output.

Mutation payloads do not share one error shape. Inspect the payload type before selecting fields:

```bash
payload_type='ResolveReviewThreadPayload'
gh api graphql -f query="{
  __type(name:\"$payload_type\") { fields { name } }
}" --jq '.data.__type.fields[].name'
```

Request `userErrors { field message }` only when the payload exposes `userErrors`, and require an empty array.
Many payloads do not expose that field. For those, request the affected object and the state that demonstrates
success. For example, `resolveReviewThread` can return `thread { id isResolved }`.

After a consequential mutation, read the resource back through `gh`, REST, or GraphQL and verify the intended
state. A returned payload proves only what its selected fields show; an empty output is not confirmation.

## Handle Pagination

Connections return the first page and a `pageInfo`, and nothing signals that more exist unless you ask. A
query returning 100 review threads on a PR with 250 is a correct response to the question you asked. Request
`pageInfo { hasNextPage endCursor }` on every connection and loop until it is false, or accept that the result
is a lower bound and say so.

## Track Query Cost

GraphQL charges a computed cost per query against a separate budget from REST. Both limits were 5000 in the
measured run. A deeply nested query over many connections can cost far more than several flat ones. Ask
what a query costs before running it in a loop:

```bash
gh api graphql -f query='{ rateLimit { limit cost remaining resetAt }
  # your real fields go here
}' --jq '.data.rateLimit'
```

Including `rateLimit` in the query itself reports the cost of that same query.

## Operations Known to Need GraphQL

**This list is short and shrinks.** Measured on gh 2.98.0, 2026-08-26:

- Resolving a review thread needs GraphQL because neither `gh` nor REST exposes the operation.
- Replying to a review thread uses REST through `gh api`; it has no dedicated `gh` subcommand.
- Linking a sub-issue uses `gh issue edit --add-sub-issue` or `gh issue create --parent` since v2.94.0.
- Adding a pull request to a required merge queue uses `gh pr merge`.
- Reading `mergeStateStatus` uses `gh pr view --json mergeStateStatus`.

**"No `gh` subcommand" and "needs GraphQL" are different findings**, and the reply row is where conflating
them goes wrong: `gh` has no verb for it, yet REST does, so `gh api --method POST` reaches it without a
mutation. Rule out REST before concluding GraphQL. The CLI is the narrowest of the three surfaces.

The last rows were once widely described as GraphQL-only. Re-run the subcommand-help discovery procedure in
`SKILL.md`, then check the current REST documentation before writing a mutation. An empty discovery result
means the discovery failed; it does not prove that the feature is absent.

## Primary References

- [Forming GraphQL calls](https://docs.github.com/en/graphql/guides/forming-calls-with-graphql)
- [GraphQL pagination](https://docs.github.com/en/graphql/guides/using-pagination-in-the-graphql-api)
- [GraphQL rate and node limits](https://docs.github.com/en/graphql/overview/rate-limits-and-node-limits-for-the-graphql-api)
- [GraphQL mutations](https://docs.github.com/en/graphql/reference/mutations)
