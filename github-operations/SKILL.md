---
name: github-operations
description: "Work with GitHub through the gh CLI and its APIs — pull requests, merge state, review threads, issues and sub-issues, branch protection and rulesets, auto-merge, token scopes and rate limits, plus a short GitHub Actions reference. Use when a PR will not merge or reports BLOCKED with every check green, a merge gate or automation script silently passes everything, a gh command exits 0 but returns nothing useful, an API call 403s or 404s, auto-merge does not fire for a bot PR, a required status check waits forever, an operation has no gh subcommand and needs GraphQL, or a bulk query returns implausibly few results. Triggers: gh, gh api, gh pr, gh issue, GraphQL, pull request, review thread, mergeStateStatus, BLOCKED, auto-merge, merge queue, branch protection, ruleset, required checks, CODEOWNERS, sub-issue, rate limit, GITHUB_TOKEN, workflow permissions, Dependabot, Renovate. NOT for local git operations, which is git-operations."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# GitHub Operations

IRON LAW: A `gh` COMMAND THAT EXITED 0 IS NOT A `gh` COMMAND THAT ANSWERED.
Check the shape of the result before believing it. GitHub's failure mode is not
a crash — it is a plausible, well-formed, wrong answer, and every expensive
mistake in this file is a script that treated one as data.

**This skill does not restate the `gh` CLI surface.** `gh help`, `gh <cmd>
--help` and the REST/GraphQL reference are reachable and correct whenever this
skill fires, and a copy here would drift while still reading as authoritative.
What follows is what those pages do not tell you.

Local git — commits, rebases, worktrees, recovery — is `git-operations`, not
this skill.

## Establish the tool before using it

`gh` is this skill's subject, so naming it is not an assumption — but everything
else is. MUST probe rather than assume:

```bash
command -v gh || echo "gh absent: report the gap and stop, do not hand-roll curl"
gh auth status   # authenticated? which account? which scopes?
```

Many recipes below pipe through `jq`; probe for it too, and fall back to `gh`'s
own `--jq` (built in, no external dependency) where possible.

When `gh` is absent or unauthenticated, MUST report that and skip. NEVER
substitute raw `curl` with a token scraped from the environment.

## The fail-open catalogue

Each of these returns success while telling you nothing, or something false.
Measured on gh 2.98.0, 2026-08-26.

**`gh api` writes its error BODY to stdout.** A 404 puts well-formed JSON —
`{"message": "Not Found", "status": "404"}` — on **stdout**, a human-readable
`gh: Not Found (HTTP 404)` on **stderr**, and exits 1. So `result=$(gh api …)`
captures the error as though it were data, and `[ -n "$result" ]` passes. MUST
check the exit status, or test for the `.message` key — never for non-emptiness.

**An unknown `--json` field is a hard error, and a gate built on one fails
open.** `gh pr view 1 --repo cli/cli --json reviewThreads` exits 1 with
`Unknown JSON field: "reviewThreads"` and prints the valid field list. A merge
gate that requests a field `gh` does not expose gets an empty result, reads it as
"no unresolved threads", and allows every merge. Verify each `--json` field
resolves before trusting a script built on it.

**Merge fields on a closed PR are stale, not absent.** `cli/cli` PR #1 is
`MERGED` and still reports `mergeStateStatus: DIRTY`, `mergeable: CONFLICTING`.
MUST read `state` first; those fields mean nothing once a PR is closed.

**Search runs on its own small budgets, and there are two of them.** Measured:
`search` allows **30/min** (what `gh search issues|prs|repos` spends) and
`code_search` **10/min**, against `core`'s 5000/hour. Budget against the right
one; a sweep looping over repositories exhausts these long before `core`.

The 1000-result cap, by contrast, is **loud at both layers** and not a silent
truncation: page 11 of a 100-per-page search returns HTTP 422,
`{"message": "Only the first 1000 search results are available"}`, exit 1, and
`gh search repos --limit 1001` refuses client-side without calling the API.
*Separately, `gh search code` under-reporting is reported upstream and not
measured here* — so treat a search-derived count as a lower bound, and confirm a
security-relevant one another way.

## Auth, scopes and 403s

`gh auth status` and the API agree on what your token HAS: both reported
`gist, read:org, repo` in the measured run. The question it cannot answer is what
the ENDPOINT needs — and that is what turns a 403 into a guess.

Ask the endpoint:

```bash
gh api -i <endpoint> 2>/dev/null | grep -i "^x-accepted-oauth-scopes:"
```

`X-Accepted-Oauth-Scopes` lists the scopes that endpoint accepts. Compare it
against `X-Oauth-Scopes` on the same response to see the gap.

**An empty value does NOT mean "requires none".** Measured across five endpoints,
2026-08-26: `/repos/cli/cli` reports `repo` and `/notifications` reports
`notifications, repo`, but `/user`, `/user/repos` and
`/repos/{owner}/{repo}/actions/runs` all report **empty** — and `/user/repos`
cannot list private repositories without `repo`. So a populated header is
evidence; an empty one is no evidence at all, on three of five endpoints tested.
Treating empty as "scopes are not the problem" fails exactly where they are.

A 403 has several distinct causes that look identical: a missing scope, a
secondary rate limit, SAML/SSO authorization not granted for an org, and a
resource that exists but is invisible to this token. Read the response body —
which, per the catalogue above, is on stdout — before concluding.

## Pull requests and merge state

`mergeStateStatus` is available through `gh pr view --json mergeStateStatus` as
of 2.98.0 — it does NOT require GraphQL, and a skill telling you otherwise is
out of date. Its values distinguish "conflicting" from "blocked by policy",
which is the difference between a rebase and a permissions conversation.

**"BLOCKED with every visible check green" is a category of its own.** The
usual causes are policy, not CI: a required status check whose context no longer
reports (a renamed job wedges the branch indefinitely), a required review from
CODEOWNERS that no reviewer satisfies, or a check configured as required that
never runs on this event. All *reported upstream, not measured here* — verify
against the repo's protection settings before acting:

Guard the call, because this is the Iron Law's own trap — `--jq` is bypassed on
an error and the error body reaches stdout:

```bash
if out=$(gh api repos/{owner}/{repo}/branches/{branch}/protection 2>/dev/null); then
  printf '%s' "$out" | jq -r '.required_status_checks.contexts[]?'
else
  echo "no classic protection (or no permission) — check rulesets"
fi
```

**Rulesets and classic branch protection are separate systems.** A repository can
be governed by a ruleset that the classic endpoint does not report — and the miss
is a **404**, not an empty response, so an unguarded `--jq` hands you
`{"message":"Not Found"}` as though it were data. Verified 2026-08-26: `cli/cli`
404s on classic protection while `gh api repos/cli/cli/rulesets` returns an
active ruleset. Check both before concluding a branch is unprotected.

**NEVER force-update an open PR's head ref to a commit equal to its base.** A
zero-diff head causes GitHub to auto-close the PR, and reopening fails
permanently — a new PR is the only path. *Reported upstream, not measured here*,
and untestable read-only, but the failure is unrecoverable, so treat it as a
hard rule rather than a caution.

## Operations with no `gh` subcommand

Some GitHub features exist only in GraphQL — but **far fewer than the internet
says**, because `gh` gains subcommands steadily and the advice does not get
retracted. Establish it by measurement, and measure the right thing:

> **A noun's help is not the CLI surface. Flags live on the subcommands.**
> Measured on gh 2.98.0, 2026-08-26: `gh issue --help` contains **zero**
> occurrences of "sub-issue", while `gh issue edit --help` documents
> `--add-sub-issue` and `--remove-sub-issue`, and `gh issue create --help`
> documents `--parent`. They shipped in **v2.94.0 on 2026-06-10**. A grep of the
> parent noun would have concluded, wrongly and with a measurement to point at,
> that sub-issues need GraphQL.

So search subcommand help, not the noun's:

```bash
for c in $(gh issue --help 2>&1 | awk '/AVAILABLE COMMANDS/{f=1;next} f&&NF{print $1}'); do
  gh issue "$c" --help 2>&1
done | grep -i "<the thing you want>"
```

Verified GraphQL-only as of 2.98.0: **resolving a review thread** (`gh pr review
--help` has no resolve verb). Verified NOT GraphQL-only, against common advice:
sub-issues (above), merge-queue enqueueing (`gh pr merge` adds to the queue when
the target branch requires one), and `mergeStateStatus`.

Read `references/graphql-operations.md` when the check above finds no
subcommand, or when a `--json` field you expected turns out not to exist. It
covers node-ID resolution, which every mutation needs and which is the step
people miss.

**Do NOT load it** for ordinary PR and issue work that `gh` already covers; the
CLI is shorter, and reaching for GraphQL first is the commonest overreach here.

## GitHub Actions

Read `references/actions-basics.md` whenever a task touches Actions at all — a
workflow that will not run, a fork PR failing where branch PRs pass, a token
permission that appears granted but is not, a required check that never reports,
or a rerun that keeps failing after the base was fixed. It is a short orientation
carrying the traps, not a reference manual, and it says so: for authoring a
substantial workflow it will not be enough on its own, so pair it with the
official documentation rather than skipping it.

**Do NOT load it** for PR, issue or repository work that never reaches a
workflow — which is most of this skill.

## Bulk and cross-repository work

- Prefer **server-side filtering** to fetching and filtering locally: it is the
  difference between one request and hundreds against a 5000/hour budget.
- Check the budget before a sweep, not after it fails:
  `gh api rate_limit --jq '.resources.core.remaining'`. `core` and `graphql` are
  **separate buckets** (both 5000 in the measured run), so exhausting one leaves
  the other usable.
- Paginate explicitly with `--paginate`. A default-page result that happens to
  hold 30 items is indistinguishable from a complete one.
- A secondary rate limit presents as a **403**, not a 429, and asks you to slow
  down rather than stop. Back off; do not retry immediately in a loop.

## Anti-patterns

NEVER:

- Test a `gh api` result for non-emptiness. The error body is JSON on stdout and
  will pass.
- Build a gate on a `--json` field without confirming `gh` exposes it; the
  failure mode is allowing everything.
- Read `mergeable` or `mergeStateStatus` without checking `state` first.
- Conclude a branch is unprotected from an empty classic-protection response
  without also checking rulesets.
- Treat a search result count as complete — 1000-result cap, 10/min budget.
- Force-update an open PR's head ref to its base commit.
- Retry into a 403 that is a secondary rate limit.
- Hand-roll `curl` with a scraped token because `gh` was missing.
- Transcribe `gh --help` output into a script's comments as though it were a
  contract; it changes between minor versions.
- Report a repository-wide finding from one search query without saying which
  query, and that a search is a lower bound.

## Before reporting done

- Every `gh` call's exit status was checked, not just its output.
- Any `--json` field a script depends on was confirmed to exist.
- Counts from search or unpaginated list endpoints are labelled as lower bounds.
- Claims about protection or policy name whether they came from the classic
  endpoint, a ruleset, or both.
- Anything that could not be checked read-only is named as unverified rather
  than asserted.
