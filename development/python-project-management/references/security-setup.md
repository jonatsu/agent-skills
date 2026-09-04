# Gates: Where Checks Run

Read this when wiring a project's checks, or when deciding whether a given check belongs in a pre-commit hook,
in CI, or in neither. Dependency auditing and update policy are in
[dependency-maintenance.md](dependency-maintenance.md).

## What Each Tool Catches

| Tool           | Usually runs as              | Catches                                               |
| -------------- | ---------------------------- | ----------------------------------------------------- |
| ruff           | pre-commit hook, CI          | Lint and format violations                            |
| mypy           | direct command, CI, on merge | Type errors                                           |
| shellcheck     | pre-commit hook              | Shell bugs: unquoted expansions, masked return values |
| detect-secrets | pre-commit hook              | Committed API keys, passwords, tokens                 |
| actionlint     | pre-commit hook, CI          | Workflow syntax, invalid action references            |
| zizmor         | pre-commit hook, CI          | Workflow security: excessive permissions, injection   |
| pip-audit      | CI, on demand                | Known advisories in dependencies                      |

Adopt ruff and mypy always. Add the shell and workflow tools when the repository actually contains shell
scripts or GitHub Actions workflows; a hook over files that do not exist is noise.

**This column says where each tool usually fits, not where it must go.** Every one of them is an ordinary
command that runs on demand. A project is free to hook all of them, hook none and rely on CI, or anything
between. Read the repository's existing configuration before assuming which arrangement is in force.

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

Install with `uv run pre-commit install`, or `prek install` if the project chose prek.

## Where to Run mypy

**mypy does not have to be a hook, and often should not be.** It is a command:

```bash
uv run mypy src/
```

Run it that way while working, in CI, or both. Whether it also runs before every commit is a project decision
with a real trade-off, not a default to apply.

| Placement               | Fits when                                               | Cost                                         |
| ----------------------- | ------------------------------------------------------- | -------------------------------------------- |
| Command only            | Small project, or the type surface is still moving      | Nothing stops a broken commit                |
| CI only                 | Type checking is slow, or the codebase is mid-migration | Failure arrives after the push               |
| CI plus pre-commit hook | The tree is already clean and must stay clean           | Every commit waits for a whole-project check |

**If the project does hook it, use a local hook over a fixed path.** The obvious `repos:` entry passes only
the staged files, so mypy analyses a different program than a full run does: it cannot see an unstaged caller,
and it reports errors that disappear on the next full check.

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

A false positive updates the baseline with `detect-secrets scan --update .secrets.baseline`. A real secret is
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

Run the same commands a developer runs, with the frozen install:

```yaml
- run: uv sync --frozen --all-groups
- run: uv run ruff format --check .
- run: uv run ruff check .
- run: uv run mypy src/
- run: uv run pytest
- run: uv run pip-audit .
- run: uv lock --check
```

`--frozen` fails rather than resolving something the lock does not describe, and `uv lock --check` catches a
hand-edited `pyproject.toml`. Together they make "it worked locally" reproducible.

## Installing the Tools

Hooks fetch their own tools. For direct command-line use:

```bash
uv tool install detect-secrets
uv tool install zizmor
brew install actionlint shellcheck     # or: go install github.com/rhysd/actionlint/cmd/actionlint@latest
```
