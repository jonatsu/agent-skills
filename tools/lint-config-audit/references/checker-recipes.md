# Checker Recipes

Commands for the audit's steps, per ecosystem. Read only the sections for the languages in the audit's focus.
Current known: the Python and shell commands were run on 2026-09-30 against ruff 0.12.0, mypy 2.3.0, and
ShellCheck 0.11.0; the others come from each tool's documentation. Confirm a flag with the tool's `--help`
before relying on it.

## Contents

- Python: ruff, mypy, pyright
- JavaScript and TypeScript: ESLint, tsc
- Rust: clippy
- Go: golangci-lint
- Shell: ShellCheck
- Pre-commit
- Other checkers

## Python: ruff, mypy, pyright

List ruff's rules with `ruff rule --all --output-format json`, and its rule families with `ruff linter`.

Count one rule with the repository's configuration but no per-file ignores:

```sh
ruff check --select F401 --config 'lint.per-file-ignores = {}' .
```

Without the `--config` override, a violation in a per-file-ignored file reports `All checks passed!`. Add
`--statistics` for per-rule totals across several selected rules.

Stale inline suppressions: `RUF100` reports each `# noqa` that suppresses nothing. Run it together with the
repository's full rule selection, `ruff check --extend-select RUF100 .`. Run alone with `--select RUF100`, it
reports every directive naming a rule outside the selection as unused, which is not the same as stale.

mypy: `--warn-unused-ignores` reports each `# type: ignore` that suppresses nothing, and `--warn-unused-configs`
reports each per-module section that matches no module. `--strict` includes the first. For a per-module
`ignore_missing_imports`, check whether the package now ships type hints or a stubs package.

pyright: `reportUnnecessaryTypeIgnoreComment` reports unneeded `# type: ignore` and `# pyright: ignore`
comments.

High-value ruff families to consider, by what they catch: `B` (likely bugs), `BLE` and `TRY` (exception
handling), `S` (security), `DTZ` (naive datetimes), `ARG` and `ERA` (dead arguments and commented-out code),
`UP` (outdated syntax), `PERF` and `C4` (performance), `TC` (imports needed only for typing), `PTH` (pathlib),
`SIM` and `RET` (simpler control flow), `FBT` (boolean positional arguments), and `LOG` and `G` (logging calls).

## JavaScript and TypeScript: ESLint, tsc

`--report-unused-disable-directives` on the command line, or `linterOptions.reportUnusedDisableDirectives` in a
flat config, reports each `eslint-disable` comment that suppresses nothing. Count one rule with
`eslint --rule '{"<rule>": "error"}' .`, and confirm on a file that violates the rule that the count can see it.

For an environment override, such as Node globals declared for browser code, search the covered files for the
constructs it allows: `process.`, `Buffer`, `__dirname`, `require(`.

TypeScript: prefer `@ts-expect-error` to `@ts-ignore`, because the compiler reports an expect-error comment
once the error it expects is gone. Stricter compiler options such as `strict`, `noUncheckedIndexedAccess`, and
`exactOptionalPropertyTypes` are tightening candidates; count their errors with `tsc --noEmit`.

## Rust: clippy

Run `cargo clippy --all-targets -- -W clippy::pedantic` to count a lint group, and search for `#![allow(` in
crate roots and `#[allow(` on items. Prefer `#[expect(...)]` to `#[allow(...)]`: the compiler raises
`unfulfilled_lint_expectations` when an expected lint no longer fires, which turns stale suppressions into
warnings. The `clippy::allow_attributes` lint finds the remaining `allow`s. Candidate groups: `clippy::pedantic`,
`clippy::nursery`, and `clippy::cargo`.

## Go: golangci-lint

Enable the `nolintlint` linter to report unused and unexplained `//nolint` directives. Read `.golangci.yml`
for enabled and disabled linters; `golangci-lint linters` lists what the installed version offers. Candidates
commonly worth counting: `errcheck`, `staticcheck`, `gosec`, `gocritic`, and `exhaustive`.

## Shell: ShellCheck

ShellCheck has no unused-directive report. To test a global disable in `.shellcheckrc`, rerun with `--norc`
and the other settings passed as flags, and count that code. To test an inline `# shellcheck disable=`, remove
the directive in a scratch copy of the file and rerun. `--list-optional` lists the checks off by default, and
`--enable=all` counts them.

## Pre-commit

Compare each hook's `rev` with the latest tag of its repository, from `git ls-remote --tags <repo>`.
`pre-commit autoupdate` rewrites the configuration in place, so run it only as an approved change. Check the
`exclude` patterns against the tree: a pattern matching nothing is stale. A Markdown or other format exclusion
must match in every tool that reads the same files, or one tool checks what the other skips.

## Other Checkers

- **Dockerfiles, hadolint:** inline `# hadolint ignore=` directives and the `ignored` list in `.hadolint.yaml`;
  lift one and rerun on the covered file.
- **Terraform, tflint:** disabled rules in `.tflint.hcl`; `tflint --enable-rule=<rule>` counts one.
- **Nix, statix and deadnix:** statix reads its disabled lints from `statix.toml`; deadnix takes its
  exclusions as command-line flags, so read them where the hook or recipe invokes it.
- **Markdown, markdownlint:** inline `<!-- markdownlint-disable -->` comments; the `noInlineConfig` option
  disables them all at once for a count.
