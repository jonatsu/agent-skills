---
name: github-ops
description: Manage GitHub operations with the gh CLI and REST or GraphQL APIs. Use for pull requests, blocked merges, branch protection and rulesets, Actions workflows and runs, authentication or permission failures, rate limits, and incomplete API or search results. Use git-commits-and-recovery for local commits, rebases, and recovery. Excludes general issue triage.
license: MIT
compatibility: Requires GitHub CLI (gh); jq is optional. GitHub Enterprise features vary by server version.
metadata:
  author: Joonas Onatsu
---

# GitHub Ops

A successful `gh` exit status proves that the command ran. It does not prove that the result is complete or
means what the caller assumes. Check both status and response shape before using output in a decision or gate.

Measurements here were taken on gh 2.98.0 on 2026-08-26. Where a newer `gh` behaves differently, trust its
`--help` and re-measure.

This package records decisions and failure modes that are easy to miss. For the `gh` CLI surface, prefer
`gh help`, `gh <cmd> --help`, and the current REST or GraphQL documentation when available. A copied command
inventory would drift while still reading as authoritative.

Use `git-commits-and-recovery` for local commits, rebases, and recovery, and `using-git-worktrees` for
worktrees. General issue triage is outside this skill.

## Establish the Tool Before Using It

Confirm the required client and its authentication before making requests:

```bash
command -v gh || { echo "gh is required" >&2; exit 1; }
gh auth status
```

`gh auth status` can report several hosts and exits non-zero if any reported host has an authentication
problem. Inspect the entry for the target host; use `--hostname HOST` when the host is known.

Prefer `gh`'s built-in `--jq`. Probe for external `jq` before using it.

When `gh` is absent or unauthenticated, report the limitation and stop. Do not extract a token from the
environment to construct an undeclared fallback.

## Respect Authority

Use read-only calls to establish state. Creating, editing, merging, closing, dispatching, or mutating through
an API changes GitHub for other people. Perform such an operation only when the user's request authorizes the
exact repository, resource, and change. Otherwise, report the proposed action or ask for approval.

Match a pull request's title to the repository's commit convention. When writing a pull-request description, issue
body, or review reply, state what changed and why, link the issue or context that motivates it. Load
`writing-for-humans` before drafting, and finish with its reader-ready pass.

## Recognize Fail-Open Results

Each of these hands a script something that passes a naive check: a non-empty result, a populated field, or a
plausible count. The fail-open lives in the caller, not in `gh`. Some commands exit non-zero, but a caller
that tests only their output can still interpret failure as data.

**`gh api` writes its error body to stdout.** A 404 puts well-formed JSON such as
`{"message": "Not Found", "status": "404"}` on stdout. It puts a human-readable `gh: Not Found (HTTP 404)` on
stderr and exits 1. So `result=$(gh api …)` captures the error as though it were data, and
`[ -n "$result" ]` passes. Check the exit status, then validate the success response's shape.

**An unknown `--json` field is a hard error, and a gate built on one fails open.**
`gh pr view 1 --repo cli/cli --json reviewThreads` exits 1 with `Unknown JSON field: "reviewThreads"` and
prints the valid field list. A merge gate that requests a field `gh` does not expose gets an empty result,
reads it as "no unresolved threads", and allows every merge. Verify each `--json` field resolves before
trusting a script built on it.

**Merge fields on a closed PR are stale, not absent.** `cli/cli` PR #1 is `MERGED` and still reports
`mergeStateStatus: DIRTY`, `mergeable: CONFLICTING`. Read `state` first; those fields mean nothing once a
PR is closed.

**Search runs on its own small budgets, and there are two of them.** Measured: `search` allows 30/min
(what `gh search issues|prs|repos` spends) and `code_search` 10/min, against `core`'s 5000/hour. Budget
against the right one; a sweep looping over repositories exhausts these long before `core`.

The 1000-result cap, by contrast, is loud at both layers and not a silent truncation. Page 11 of a
100-per-page search returns HTTP 422 with `{"message": "Only the first 1000 search results are available"}`,
and the command exits 1. `gh search repos --limit 1001` refuses client-side without calling the API.
Separately, `gh search code` under-reporting is reported upstream and not measured here. Treat a
search-derived count as a lower bound, and confirm a security-relevant one another way.

## Diagnose Authentication and 403 Responses

Start with the response body and headers. Keep the API exit status separate from any filtering step:

```bash
api_endpoint='repos/{owner}/{repo}'
if response=$(gh api --include "$api_endpoint"); then
  printf '%s\n' "$response"
else
  printf '%s\n' "$response" >&2
  echo "request failed; inspect the response status, body, and permission headers" >&2
fi
```

Capture the API call, then filter. A direct pipe into `grep` or `jq` can hide the API failure. Select the
diagnostic that matches the credential type:

- OAuth tokens and classic personal access tokens use `X-OAuth-Scopes` and `X-Accepted-OAuth-Scopes`.
  Compare populated values. An absent or empty accepted-scopes header does not prove that no scope is needed.
- Fine-grained personal access tokens and GitHub App tokens use `X-Accepted-GitHub-Permissions` for endpoint
  requirements. Confirm the token or app installation's actual repository access and permissions separately.
- A workflow's `GITHUB_TOKEN` derives permissions from enterprise, organization, repository, workflow, job,
  event, and fork settings. Inspect those layers rather than treating it as a personal token.

A 403 can also have causes other than missing permissions. These include a primary or secondary rate limit,
missing SAML single sign-on authorization, repository selection that excludes the resource, and deliberate
not-found masking. Use the status, body, rate-limit headers, credential type, and endpoint documentation
together, never one absent header alone.

## Diagnose Pull Requests and Merge State

`mergeStateStatus` is available through `gh pr view --json mergeStateStatus`. It does not
require a custom GraphQL query. Its values distinguish "conflicting" from "blocked by policy", which is the
difference between a rebase and a permissions conversation.

**"BLOCKED with every visible check green" is a category of its own.** The usual causes are policy, not CI:

- A required status check whose context no longer reports. A renamed job wedges the branch indefinitely.
- A required review from CODEOWNERS that no reviewer satisfies.
- A check configured as required that never runs on this event.

These causes are reported upstream, not measured here. Verify the repository's protection settings before
acting.

Guard the call because `--jq` is bypassed on an error and the error body reaches stdout:

```bash
if protection=$(gh api repos/{owner}/{repo}/branches/{branch}/protection \
                  --jq '.required_status_checks.contexts[]?'); then
  printf '%s\n' "$protection"
else
  printf '%s\n' "$protection" >&2
  echo "classic protection was unavailable; inspect the error and check rulesets" >&2
fi
```

`--jq` goes inside the guard. It still applies on the success path, so external `jq` is unnecessary. The
`if` preserves the API status. On the error path `--jq` is bypassed, and the raw body reaches stdout regardless
of where the filter sits. Leave `{owner}`, `{repo}` and `{branch}` as written: `gh api` expands them from the current
repository, so the command runs verbatim.

**Rulesets and classic branch protection are separate systems.** A repository can be governed by a ruleset
that the classic endpoint does not report. The miss is a 404, not an empty response, so an unguarded
`--jq` hands you `{"message":"Not Found"}` as though it were data. Verified 2026-08-26: `cli/cli` 404s on
classic protection while `gh api repos/cli/cli/rulesets` returns an active ruleset. Check both before
concluding a branch is unprotected.

Before force-updating an open pull request, compare the proposed head with its base. Keep the head different
from the base. GitHub has been reported to close a zero-diff pull request and refuse reopening afterward. This
behavior remains unverified locally, so inspect the pull request state and report uncertainty if recovery is
needed.

## Find Operations with No `gh` Subcommand

Some GitHub features exist only in GraphQL, but far fewer than the internet says. The `gh` CLI gains
subcommands steadily, and the advice does not get retracted. Establish it by measurement, and measure the right
thing:

> **A noun's help is not the CLI surface. Flags live on the subcommands.** Measured: `gh issue --help` contains
> zero occurrences of "sub-issue". `gh issue edit --help` documents `--add-sub-issue` and
> `--remove-sub-issue`, and `gh issue create --help` documents `--parent`. A grep of the parent noun would have
> concluded, wrongly and with a measurement to point at, that sub-issues need GraphQL.

So search subcommand help, not the noun's:

```bash
noun=issue   # or pr, repo, release, run, workflow…
subs=$(gh "$noun" --help 2>&1 |
       awk '/^[A-Z ]*COMMANDS$/{f=1;next} /^[A-Z]/{f=0} f&&NF{gsub(/:$/,"",$1);print $1}')
[ -n "$subs" ] || { echo "subcommand discovery failed for $noun" >&2; exit 1; }
for c in $subs; do
  gh "$noun" "$c" --help 2>&1 | sed "s/^/$c: /"
done | grep -i "<the thing you want>"
```

Three things in that loop are load-bearing, and a hand-written version misses them:

- **The section header differs across nouns.** Measured: `gh run` and `gh workflow` use
  `AVAILABLE COMMANDS`, while `gh issue`, `gh pr`, `gh repo` and `gh release` use `GENERAL COMMANDS` and
  `TARGETED COMMANDS`. A loop keyed on `AVAILABLE COMMANDS` alone iterates zero times on the four nouns
  you most want it for. It then prints exactly what "no such flag" prints.
- **The `/^[A-Z]/{f=0}` reset** stops the extraction running past the commands block into `FLAGS` and
  `LEARN MORE`.
- **The `gsub`** strips the trailing colon `gh` puts on each name.

Without the reset or the `gsub`, every invocation in the loop fails.

**Report an empty subcommand list as discovery failure, not as "not found".** That guard applies
the status-and-shape rule. A loop that matched nothing and a loop that searched
everything and found nothing produce identical silence, and only one of them is an answer. Piping through
`sed` names which subcommand carries the flag, which is the part you actually need next.

**Rule out REST before concluding GraphQL.** "No `gh` subcommand" is a fact about the CLI and says nothing
about the API beneath it. Replying to a review thread has no `gh` verb
but does have a REST endpoint (`POST /repos/{owner}/{repo}/pulls/{n}/comments/{id}/replies`), reachable with
`gh api --method POST`. Resolving one has neither, and is GraphQL-only. Same noun, two
different answers.

Verified as available without a custom GraphQL query: sub-issues (above), merge-queue enqueueing, and
`mergeStateStatus`. `gh pr merge` adds a pull request to the queue when the target branch requires one.

Read `references/graphql-operations.md` when the check above finds no subcommand, or when a `--json` field you
expected does not exist. It covers node-ID resolution and mutation-specific result validation.

Skip it for ordinary PR and issue work that `gh` already covers, because the CLI is shorter. Reaching
for GraphQL first is the commonest overreach here.

## GitHub Actions

Read `references/actions-basics.md` whenever a task touches Actions, for example:

- a workflow that will not run
- a fork PR failing where branch PRs pass
- a token permission that appears granted but is not
- a required check that never reports
- a rerun that keeps failing after the base was fixed

For substantial workflow authoring or debugging, pair the orientation with current official documentation.

Skip it for PR, issue, or repository work that never reaches a workflow.

## Handle Bulk and Cross-Repository Work

- Prefer server-side filtering to fetching and filtering locally. The difference is one request against
  hundreds, on a 5000/hour budget.

- Check all relevant budgets before a sweep:
  `gh api rate_limit --jq '.resources | to_entries[] | {resource: .key, remaining: .value.remaining}'`.
  `core`, `graphql`, `search`, and `code_search` are separate buckets. Inspect the bucket used by the planned
  request rather than assuming the `core` result applies.

- Paginate explicitly with `--paginate`. A default-page result that happens to hold 30 items is
  indistinguishable from a complete one.

- **A rate limit presents as a `403` or a `429`, and the status does not tell you which limit you hit.**
  GitHub's REST documentation states both codes for both the primary and the secondary limit. A backoff
  handler matching only one code retries straight into the other. Read the headers instead:

  - Honour `retry-after` if present.
  - Else if `x-ratelimit-remaining` is `0`, wait until `x-ratelimit-reset`.
  - Else wait at least a minute.

  A secondary limit is identified by its error message, not its status code. Documented, not
  measured here. Triggering a limit to observe it is abuse. Checked against the REST rate-limit
  documentation 2026-08-26.

## Before Reporting Done

- Every `gh` call used for a decision or gate had its exit status and response shape checked.
- Any `--json` field a script depends on was confirmed to exist.
- Counts from search or unpaginated list endpoints are labelled as lower bounds, naming the query they came
  from.
- Claims about protection or policy name whether they came from the classic endpoint, a ruleset, or both.
- Anything that could not be checked read-only is named as unverified rather than asserted.

## Primary References

- [GitHub CLI `gh api` manual](https://cli.github.com/manual/gh_api)
- [Troubleshooting REST API permissions](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api)
- [REST API rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)
