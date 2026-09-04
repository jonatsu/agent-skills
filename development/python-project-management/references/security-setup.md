# Gates: Pre-commit Hooks and CI Security

Read this when wiring the checks that run before a commit and in CI. Dependency auditing and update policy are
in [dependency-maintenance.md](dependency-maintenance.md).

## What Each Tool Catches

| Tool           | Runs           | Catches                                               |
| -------------- | -------------- | ----------------------------------------------------- |
| ruff           | pre-commit, CI | Lint and format violations                            |
| mypy           | pre-commit, CI | Type errors                                           |
| shellcheck     | pre-commit     | Shell bugs: unquoted expansions, masked return values |
| detect-secrets | pre-commit     | Committed API keys, passwords, tokens                 |
| actionlint     | pre-commit, CI | Workflow syntax, invalid action references            |
| zizmor         | pre-commit, CI | Workflow security: excessive permissions, injection   |
| pip-audit      | CI, manual     | Known advisories in dependencies                      |

Adopt the first two always. Add the shell and workflow tools when the repository actually contains shell
scripts or GitHub Actions workflows; a hook over files that do not exist is noise.

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

**mypy is deliberately not a `repos:` entry here.** A hooked mypy runs against only the staged files, which
changes what it can see and produces results that disagree with a full run. Run it as a local hook over a
fixed path instead:

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

`pass_filenames: false` is the load-bearing line. Without it pre-commit appends the staged paths and the
fixed path is ignored.

Install with `uv run pre-commit install`, or `prek install` if the project chose prek.

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
