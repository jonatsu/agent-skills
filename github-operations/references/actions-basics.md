# GitHub Actions — a short orientation

Load this for enough Actions grounding to do PR and repository work without
getting stuck. It is deliberately NOT a reference manual: Actions is large enough
to deserve its own skill, and this file covers the structure plus the traps that
cost the most time.

**For authoring or debugging a substantial workflow, go to the official
documentation.** Syntax, the expression functions, the context objects and the
runner images all change, and a copy here would be stale and confident. What
follows is shape and failure modes.

## The structural fact that catches people

Workflow YAML in `.github/workflows/`, `on:` triggers, `jobs:`, `steps:` — the
shape is unremarkable and needs no explanation here. The part that surprises
people: **each job starts on a clean machine**, so nothing carries from one job
to the next except artifacts, declared outputs, and whatever you cache
explicitly. A file written in job A is simply not there in job B, and `needs:`
orders jobs without sharing their filesystems.

## Triggers determine everything downstream

The trigger decides which secrets exist, which token permissions apply, and what
`GITHUB_SHA` points at. Two consequences worth holding:

- **`pull_request` from a fork runs with a read-only token and no access to
  repository secrets.** A workflow that works for branch PRs and fails for fork
  PRs is usually this, not a bug in the workflow.
- **A job gated on `push` will not run for `merge_group`**, and vice versa. A
  repository using a merge queue therefore needs its required checks to fire on
  both, or the queue waits on a check that never reports. *Reported upstream, not
  measured here.*

## The permissions trap

`GITHUB_TOKEN` permissions are declared per workflow or per job. Two behaviours
that are not obvious:

- **For a reusable workflow, the effective token is the INTERSECTION of the
  caller's permissions and the callee's declaration.** Granting a permission in
  only one of the two grants nothing. *Reported upstream, not measured here.*
- **Actions taken with the default `GITHUB_TOKEN` do not raise events.** A
  workflow that pushes a commit or opens a PR with it will not trigger the
  workflows listening for that push or PR. This is a deliberate guard against
  recursive runs, not a misconfiguration — using a PAT or an app token is the
  documented way around it, and it re-enables the recursion the guard prevents.
  *Reported upstream, not measured here.*

Declare the narrowest `permissions:` block that works, at job level rather than
workflow level, and expect to widen it once with evidence rather than starting
broad.

## Required checks and branch protection

**Renaming a job renames its status-check context**, and any branch protection
rule still requiring the old context waits forever on a check that will never
report. The PR sits BLOCKED with everything visibly green — see `SKILL.md`'s
merge-state section, where this is the leading cause. Renaming a job is therefore
a protection-settings change, not just a workflow edit.

A check that is *required* but never runs on this event has the same effect.

## Reading a failed run

`gh run --help` covers the commands; two things it is easy to miss. Prefer
`gh run view <id> --log-failed` over the full log, which for a matrix build is
enormous. And **both `gh run watch` and `gh run view` take `--exit-status`**,
which is what makes them usable in a script — without it they exit 0 when a run
finishes, including when it finished by failing (verified present on gh 2.98.0,
2026-08-26). That is the Iron Law again: finishing is not passing.

For a rerun: **a rerun of a `pull_request` workflow uses the merge commit
computed when the run was first created**, so it tests against the old base. A
rerun that "still fails after the base was fixed" is usually this. *Reported
upstream, not measured here* — push an empty commit or close/reopen to force a
fresh merge commit.

## Pinning actions

Pin third-party actions by commit SHA rather than tag: a tag is mutable, so
`@v4` can become different code without any change on your side. Repositories
under a `sha_pinning_required` policy will fail at `Set up job` — before any of
your steps run — if a tag is used, which reads as an infrastructure error rather
than a policy one. *Reported upstream, not measured here.*

First-party `actions/*` are conventionally pinned by major tag; that is a
deliberate trust decision, not an inconsistency.

## What is out of scope here

Matrix strategy details, caching design, self-hosted runner setup, reusable
workflow authoring, composite actions, environments and deployment gates,
artifact retention, and the expression language. Each is worth doing properly,
and none of it belongs in a file this size. Reach for the documentation, and
raise a dedicated Actions skill if this becomes recurring work.
