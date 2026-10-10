# Attributions

## Current Skill

- Skill: `python-project-management`
- Current author: Joonas Onatsu
- Current license: CC-BY-SA-4.0
- Status: adaptation of an upstream skill, restructured and repaired, deployed to every agent

## Upstream Source

This skill is an adaptation of
[`trailofbits/skills`](https://github.com/trailofbits/skills) `plugins/modern-python/skills/modern-python`,
pinned at `d3323cefbcf645678b8dc481de204b02ad3d02dc` and read on 2026-09-04. Upstream author: William Tan,
Trail of Bits. Upstream skill version 1.6.0, derived in turn from
[`trailofbits/cookiecutter-python`](https://github.com/trailofbits/cookiecutter-python).

**The upstream repository is licensed CC BY-SA 4.0, so this adaptation carries the same license.** Share-alike
propagates: this package cannot be relicensed to the repository's MIT default, and any further adaptation of
it must also be CC BY-SA 4.0 with attribution. The full license text is in `LICENSE.upstream`.

Adapted material: the tool-and-replacement framing, the task-based routing between scripts, minimal projects,
packages and migrations, the `pyproject.toml` shape including the PEP 735 dependency-group layout and the
former Ruff `select = ["ALL"]` starting point, the uv command reference, the PEP 723 script guidance, the security
tool matrix, and the migration checklist's structure.

## Changes From Upstream

Deliberate divergences, each with its reason:

- **mypy is the default type checker; `ty` is named as a conditional alternative.** Upstream lists
  `mypy / pyright → ty` as an anti-pattern. On 2026-09-04 `ty` was version 0.0.78 and classified Beta on PyPI,
  which is not a dependency to put in a project's gate by default.
- **pre-commit is the default hook runner; `prek` is named the same way.** Same reasoning, weaker stakes:
  `prek` 0.5.2 is classified Production/Stable, so the choice is about startup time rather than maturity.
- **`[tool.pytest]` corrected to `[tool.pytest.ini_options]`.** Measured 2026-09-04: pytest 9.1.1 honours the
  bare table, pytest 8.3.5 silently ignores it, so a `--cov-fail-under` gate reports success while never
  running. Upstream carries the bare form in three files.
- **PEP 723 scripts can be locked.** Upstream lists "no lockfile" as a limitation; `uv lock --script` exists
  and writes `<script>.py.lock`, verified against uv 0.12.5 on 2026-09-04.
- **Test configuration removed.** `[tool.pytest.ini_options]` and coverage settings belong to
  `python-testing`, and type-checker configuration to `python-typing`, so each has one home.
- **Dropped:** the cookiecutter template recommendation, the Trail of Bits mark asset, the standalone `prek`
  and Dependabot references, and the `templates/` directory whose contents are now inline where they are read.
- **Added:** ongoing maintenance, which upstream does not cover — lock refreshes, `uv lock --check` drift
  detection, `--upgrade-package`, advisory triage, `uv version --bump`, and the publishing sequence.
- **Added:** the mypy pre-commit hook must run as a local hook with `pass_filenames: false`, because a
  file-scoped invocation sees a different program than a full run.

Every uv command in this package was verified against uv 0.12.5 on 2026-09-04. The pre-commit revisions were
read from each project's latest release on the same date.

## Python Defaults Review, 2026-09-11

Reviewed Integralist's `.claude/rules/python.md` in `Integralist/agent-skills` at commit
`07155927c4a44cf97b050ea4f728fce840822ce9`:

<https://github.com/Integralist/agent-skills/blob/07155927c4a44cf97b050ea4f728fce840822ce9/.claude/rules/python.md>

The comparison informed the focused Ruff baseline and code-specific lint suppressions.
The expression is independent; no upstream text or code is copied or adapted.
No license covering these rules was found in the pinned tree; the MCP component has separate licensing.

The former `ALL` baseline was replaced with focused rule families. Library locks now cover development and CI.
The HTTP-client preference moved from the author's scoped Python rule, as approved in the 2026-09-06 consolidation.
That rule recorded idea influence from Tim Vink's `dot_claude/rules/httpx2.md`:
<https://github.com/timvink/dotfiles/blob/main/dot_claude/rules/httpx2.md>.
The historical record did not pin a revision or establish that source's license; no additional text was copied from it.

## Fact Corrections, 2026-09-24

- `pip-audit --locked` reads `pylock*.toml`, not `uv.lock`: read in pip-audit 2.10.1's `_cli.py` and run in a
  scratch uv 0.12.10 project, where it failed without an exported `pylock.toml` and passed with one.
- PEP 723 scripts accept local path and editable dependencies through `[tool.uv.sources]` but not dependency
  groups: run with `uv add --script` in uv 0.12.10.
- Default `GITHUB_TOKEN` permissions depend on repository and organization settings: GitHub's "Managing GitHub
  Actions settings for a repository" page, read on this date.
- The Full Project commands now create the `lint`, `test` and `audit` groups the example configuration
  includes; the `include-group` layout synced in a scratch uv 0.12.10 project.
