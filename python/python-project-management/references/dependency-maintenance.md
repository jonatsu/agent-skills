# Dependency Maintenance and Releases

## Refreshing the Lock

```bash
uv lock --upgrade                 # re-resolve everything within declared constraints
uv lock --upgrade-package httpx   # re-resolve one package only
uv sync                           # install what the new lock says
```

`uv lock --upgrade` does not change `pyproject.toml`. It moves within the constraints already declared there,
so a dependency capped at `<2.0` stays on 1.x. Raising the cap is a separate, deliberate edit through
`uv add 'httpx>=2'`.

Prefer `--upgrade-package` when chasing one fix. A full `--upgrade` moves everything at once, which makes a
resulting failure expensive to attribute.

## Checking for Drift

```bash
uv lock --check    # nonzero if the lock does not match pyproject.toml
uv tree            # what depends on what
uv tree --outdated # show newer versions available
```

`uv lock --check` belongs in CI. It catches the common failure where someone edited `pyproject.toml` by hand
and the lock no longer describes it.

## Auditing

`pip-audit` checks installed packages against the Python Advisory Database.

```bash
uv run pip-audit          # audit the current environment
uv export --format pylock.toml -o pylock.toml && uv run pip-audit --locked .   # audit the lock instead
uv run pip-audit --fix    # upgrade vulnerable packages where a fix exists
```

`pip-audit --locked` reads `pylock.toml` or `pylock.*.toml`, not `uv.lock`, and exits 1 with
`no lockfiles found` when neither exists; export the lock first. Verified against pip-audit 2.10.1 and
uv 0.12.10 on 2026-09-24.

When it reports something:

1. Check whether the advisory reaches your usage. Many affect a code path a project never calls.
2. If it does, take the fix: `uv add 'package>=<fixed version>'`, then `uv sync` and rerun the audit.
3. If no fix exists, decide deliberately: accept the risk, pin away from the affected version, or replace the
   dependency. Record the decision and its reason, including for any advisory ignored to keep a gate green.

## Automated Updates

Dependabot opens pull requests for outdated dependencies on a schedule. `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: uv
    directory: /
    schedule:
      interval: weekly
    cooldown:
      default-days: 7
    groups:
      dev-dependencies:
        dependency-type: development
        update-types: [minor, patch]
      production-dependencies:
        dependency-type: production
        update-types: [patch]

  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
    cooldown:
      default-days: 7
    groups:
      actions:
        patterns: ["*"]
        update-types: [minor, patch]
```

Two settings earn their place. The **cooldown** delays adoption of a brand-new release, which is the window an
attacker who has published a malicious version is counting on. **Grouping** minor and patch updates into one
pull request keeps the review queue small enough that the updates actually get reviewed. Production
dependencies group only patches, so a minor bump to something users run arrives as its own reviewable change.

**Use `package-ecosystem: uv` for a uv project, not `pip`.** Dependabot lists them as separate ecosystems, and
the `pip` one does not update `uv.lock` — so a project configured with `pip` keeps the very lock this skill
insists on committing permanently stale. Confirmed against GitHub's Dependabot options reference on
2026-09-04; check the current ecosystem list if the project uses a different package manager.

Audit and automation cover different failures:

| Tool        | Answers                              |
| ----------- | ------------------------------------ |
| `pip-audit` | "Is something vulnerable right now?" |
| Dependabot  | "Are we falling behind?"             |

## Version Bumps

```bash
uv version                # show the current version
uv version --bump patch   # 0.1.0 -> 0.1.1
uv version --bump minor   # 0.1.1 -> 0.2.0
uv version --bump major   # 0.2.0 -> 1.0.0
```

Before 1.0 the compatibility guarantees are weaker; say so in the README. Static versus VCS-derived versions
are covered under `[build-system]` in [pyproject-reference.md](pyproject-reference.md).

## Publishing

```bash
uv build                              # wheel and sdist into dist/
uv publish --publish-url https://test.pypi.org/legacy/ --token $TEST_TOKEN
uv publish --trusted-publishing automatic   # preferred in CI
uv publish --token $PYPI_TOKEN              # only where trusted publishing is unavailable
```

The order that avoids a bad release:

1. Every gate green: lint, format check, type check, tests, audit.
2. Bump the version and record what changed.
3. `uv build`, then install the built wheel into a scratch environment and import it.
4. Publish to TestPyPI and install from there.
5. Publish to PyPI, then tag the commit.

A published version is immutable. PyPI will not let you replace it, only yank it, so the scratch-install step
is the cheapest insurance available.

## Routine Health Check

Run `uv lock --check`, then `uv sync --all-groups`, then every command under Wire the Gates in `SKILL.md`.
Do it before a release, after taking a batch of dependency updates, and when returning to an idle project.
