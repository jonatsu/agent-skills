# GitHub Actions: A Short Orientation

Load this for enough Actions grounding to do PR and repository work without getting stuck. It is deliberately
not a reference manual: Actions is large enough to deserve its own skill, and this file covers the structure
plus the traps that cost the most time.

**For authoring or debugging a substantial workflow, go to the official documentation.** Syntax, the
expression functions, the context objects and the runner images all change, and a copy here would be stale and
confident. What follows is shape and failure modes.

## Job Isolation

Workflow YAML in `.github/workflows/`, `on:` triggers, `jobs:`, and `steps:` has a documented structure.
**Each GitHub-hosted job starts on a fresh runner image.** Jobs do not share filesystems; use artifacts,
declared outputs, or caches to transfer intentional state. Self-hosted runner state can persist, but workflows
must not depend on leftovers. Clean it explicitly. `needs:` orders jobs without sharing their filesystems.

## Trigger Effects

The trigger decides which secrets exist, which token permissions apply, and what `GITHUB_SHA` points at. Two
consequences worth holding:

- **A `pull_request` workflow from a fork normally receives a read-only token and no secrets.** Repository
  settings can change the token or secret policy, especially for private repositories, so inspect the run and
  settings before concluding. `pull_request_target` uses the base branch's context and may receive secrets or
  write permission; never run or check out untrusted pull-request code in that privileged context.
- **A job gated on `push` will not run for `merge_group`**, and vice versa. A repository using a merge queue
  therefore needs its required checks to fire on both, or the queue waits on a check that never reports.
  *Reported upstream, not measured here.*

## Token Permissions

`GITHUB_TOKEN` permissions are declared per workflow or per job. Two behaviours that are not obvious:

- **A called reusable workflow can keep or reduce the caller's `GITHUB_TOKEN` permissions; it cannot elevate
  them.** Check permissions across the complete caller chain.
- **Most events created with the repository's `GITHUB_TOKEN` do not create another workflow run.**
  `workflow_dispatch` and `repository_dispatch` are exceptions. GitHub also permits workflow runs for
  `pull_request` events with `opened`, `synchronize`, or `reopened` activity when automation creates or updates
  a pull request; those runs require approval. Check the current trigger documentation before designing
  chained automation. A GitHub App or personal access token can trigger other runs, which restores recursion
  risk.

Declare the narrowest `permissions:` block that works. Use job-level permissions when jobs need different
access; use workflow-level permissions when the same minimum applies throughout.

## Required Checks and Branch Protection

**Renaming a job can change its status-check context**, and a protection rule that still requires the old
context can wait for a check that will never report. When a pull request is blocked despite green visible
checks, compare the required contexts with the current check names.

A check that is *required* but never runs on this event has the same effect.

## Reading a Failed Run

`gh run --help` covers the commands; two things it is easy to miss. Prefer `gh run view <id> --log-failed`
over the full log, which for a matrix build is enormous. And **both `gh run watch` and `gh run view` take
`--exit-status`**, which is what makes them usable in a script. Without it they exit 0 when a run finishes,
including when it finished by failing (measured). Finishing is not passing.

For a rerun, GitHub keeps the original event's `GITHUB_SHA` and `GITHUB_REF`. A rerun that still fails after
the base changed may therefore be testing the original pull-request merge commit. If the user authorized a
new run, update the pull-request head or close and reopen the pull request to create a new event. State the
remote side effect before taking it.

## Pinning Actions

Pin external actions by a full commit SHA when reproducibility or supply-chain protection matters. A tag is
mutable, including a major tag such as `@v4`. Repositories with a full-SHA policy apply it to organization and
GitHub-authored actions too; a tag then fails before the action's steps run. Record the corresponding release
version in a comment or dependency update configuration so maintainers can update the SHA deliberately.

## Scope Boundary

Matrix strategy details, caching design, self-hosted runner setup, reusable workflow authoring, composite
actions, environments and deployment gates, artifact retention, and the expression language. Each is worth
doing properly, and none of it belongs in a file this size. Reach for the documentation, and raise a dedicated
Actions skill if this becomes recurring work.

## Primary References

- [Workflow syntax and token permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Triggering workflows with `GITHUB_TOKEN`](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [Re-running workflows and jobs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs)
- [Managing Actions policies](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
