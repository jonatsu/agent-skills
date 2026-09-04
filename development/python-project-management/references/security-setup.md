# Gates: Where Checks Run

Read this when wiring a project's checks or working out how an existing project runs them. Dependency auditing
and update policy are in [dependency-maintenance.md](dependency-maintenance.md).

## What Each Tool Catches

| Tool           | Catches                                               |
| -------------- | ----------------------------------------------------- |
| ruff           | Lint and format violations                            |
| mypy           | Type errors                                           |
| shellcheck     | Shell bugs: unquoted expansions, masked return values |
| detect-secrets | Committed API keys, passwords, tokens                 |
| actionlint     | Workflow syntax, invalid action references            |
| zizmor         | Workflow security: excessive permissions, injection   |
| pip-audit      | Known advisories in dependencies                      |

Adopt ruff and mypy always. Add the shell and workflow tools when the repository actually contains shell
scripts or GitHub Actions workflows; a hook over files that do not exist is noise.

**Check how the project already runs each tool before invoking or configuring it.** Look at
`.pre-commit-config.yaml`, the CI workflows, and any `justfile`, `Makefile` or `tox.ini`. Each tool is an
ordinary command, and a project may run it as a hook, in CI, through a task runner, on demand, or in several
of those. Match what is there rather than assuming an arrangement.

## Hook Configuration

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict
      - id: check-toml
      - id: check-yaml

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.6
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: [--baseline, .secrets.baseline]
```

Every `rev` is a pin that ages. These were the current releases on 2026-09-04; check each project's releases
page rather than copying them forward, or run `pre-commit autoupdate` and review the diff.

The ruff hook id is `ruff-check`. A bare `ruff` id still exists as a deprecated alias, so a config copied from
an older source keeps working and stops matching the documentation.

Install the hooks with `uvx pre-commit install`, or `prek install` if the project chose prek. Use `uv run`
instead only when pre-commit is itself a declared dependency group member.

## mypy

mypy is a command:

```bash
uv run mypy src/          # use the project's own package path
```

**If the project hooks it, use a local hook over a fixed path.** The obvious `repos:` entry passes only the
staged files, so mypy analyses a different program than a full run does: it cannot see an unstaged caller, and
it reports errors that disappear on the next full check.

```yaml
  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: uv run mypy src/
        language: system
        types: [python]
        pass_filenames: false
```

`pass_filenames: false` is the load-bearing line. Without it pre-commit appends the staged paths to the
command and the fixed path is ignored, which reintroduces exactly the problem the local hook avoids.

Strictness settings, per-module overrides, and the progression for an existing codebase belong to
`python-typing`.

## Secret Scanning

detect-secrets works against a baseline of known, reviewed findings:

```bash
detect-secrets scan > .secrets.baseline   # first time
cat .secrets.baseline                     # review before committing it
git add .secrets.baseline
```

When the hook fires:

```bash
detect-secrets audit --report .secrets.baseline
```

A false positive is re-baselined with `detect-secrets scan --baseline .secrets.baseline`. A real secret is
removed from the code **and rotated** — a committed credential is compromised even after the commit is
rewritten, because it existed in a working tree and possibly a push.

## Workflow Auditing

```bash
actionlint .github/workflows/
zizmor .github/workflows/
```

actionlint catches what will fail at run time: invalid triggers, undefined inputs, shell syntax inside `run:`
blocks, bad action references. zizmor catches what will not fail but should worry you.

The finding you will see first is `excessive-permissions`. Workflows default to broad write access, so declare
what each one needs:

```yaml
permissions:
  contents: read          # lint, test, audit

permissions:
  contents: write         # release, tag, push

permissions:
  contents: read
  pull-requests: write    # comment on a PR
```

Other recurring findings: `template-injection` from interpolating `${{ github.event.* }}` into a shell line,
`unpinned-action` where an action is referenced by tag rather than commit SHA, and `dangerous-triggers` from
`pull_request_target` combined with a checkout of the pull request's code.

## CI

Run the same commands a developer runs, asserting the lock is current:

```yaml
- run: uv sync --locked --all-groups
- run: uv run ruff format --check .
- run: uv run ruff check .
- run: uv run mypy src/     # use the project's own package path
- run: uv run pytest
- run: uv run pip-audit
- run: uv lock --check
```

`--locked` fails when the lock does not match `pyproject.toml`. `--frozen` does not: it installs the stale
lock and exits 0. Verified against uv 0.12.5.

## Installing the Tools

Hooks fetch their own tools. For direct command-line use:

```bash
uv tool install detect-secrets
uv tool install zizmor
# whatever this platform uses; e.g. on macOS or Linuxbrew:
brew install actionlint shellcheck
# or, without a package manager:
go install github.com/rhysd/actionlint/cmd/actionlint@latest
```
