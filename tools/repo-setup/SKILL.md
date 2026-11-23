---
name: repo-setup
description: Set up a new repository, or add, refresh, or configure an existing one's baseline files and hygiene hooks (.gitignore, .editorconfig, .gitattributes, pre-commit with formatter, linter, and secret-scanning hooks). Use to set up or bootstrap a repository, or when its hooks or baseline config are missing or out of date. Not for the README and other landing documents (repo-landing-docs), auditing an existing repository's checks or tracked files (repo-audit), or commits and history (git-commits-and-recovery).
license: MIT
metadata:
  author: Joonas Onatsu
---

# Repository Setup

Apply an opinionated repository baseline without erasing established project conventions. The bundled
configurations encode the author's personal preferences; treat them as deliberate defaults. Repository evidence
and explicit user choices take precedence when they conflict with those defaults.

This skill owns baseline files and repository-local hygiene hooks. Neighbouring work has its own skill:
`repo-landing-docs` owns the landing documents; `repo-audit` audits an established repository's checkers and
tracked files read-only; `git-commits-and-recovery` owns commits, branches, recovery, and history
rewriting; `git-history-investigation` answers history questions; `using-git-worktrees` covers worktrees; and
`agents-context-docs` covers agent instruction files.

## Choose the Task

- **Targeted change:** add or revise named baseline files or hooks. Inspect only the affected files, their consumers,
  and the repository's existing conventions. A request for one file is not a request for an audit.
- **Bootstrap:** establish a baseline in a new or nearly empty repository, including its landing documents through
  `repo-landing-docs`. In a split from an existing repository, the
  bootstrap is done only when the in-flight state about the moved part has moved or been rewritten. That state includes
  open review items, TODO and backlog entries, notes, and plans. The README must also document every install route and
  state a minimum interpreter version, not an exact one.
- **Refresh:** compare an established repository with the preferred baseline, then fill approved gaps and
  leave healthy files as they are.

## Work Proportionately

1. Inspect the relevant repository state, existing files, configured checks, and instructions.
2. Resolve only the choices that the repository and the request leave open. Ask when a missing choice decides
   the license, public behavior, repository visibility, governance model, toolchain, a destructive target, or
   an outward-facing action.
3. For bootstrap, refresh, or ambiguous work, propose a plan naming each file to create, adapt, preserve, or skip. Get
   approval for the scope the request did not settle. A request naming its files or changes already authorizes them.
4. Apply the smallest coherent delta, and keep existing content unless the user authorized replacing it.
5. Validate each changed artifact with its real consumers and the repository's checks.
6. Report completed work, deferred findings, and external settings that still need the user's action.

## Apply the Preferred Baseline

Use assets as starting points after inspecting the repository. The landing documents (README, LICENSE,
CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, the issue and pull request templates, and their kin) belong to the
`repo-landing-docs` skill, which holds their templates. On a bootstrap or refresh, load it for those files.

- `.gitignore`: Retrieve the applicable official GitHub template and adapt it to confirmed generated files.
- `.editorconfig`: The bundled profile deliberately uses two spaces as the fallback and supplies targeted
  overrides. Preserve these personal defaults for a new baseline; reconcile them with established project
  conventions during refresh work.
- `.gitattributes`: Keep the bundled cross-platform text, script, document, serialization, image, archive, and
  patch rules unless repository evidence requires a narrower adaptation.
- `.pre-commit-config.yaml`: The bundled asset is the full preferred profile: pre-commit-hooks, Betterleaks, Secretlint,
  EditorConfig checking, YAML and Markdown formatting and linting, a local invisible-character check for Markdown,
  ShellCheck, and shfmt. Use the complete profile when the user requests the preferred baseline. Make only the requested
  delta when extending an established configuration. The bundled hook revisions are a snapshot: run
  `pre-commit autoupdate` before first use, unless the user or repository pins them for a reason. Secretlint, configured
  by `.secretlintrc.json`, catches what a credential scanner does not look for: the committing user's home path and
  `.env` files. It needs Node.js 22 or later. When the user wants more data kept out of commits, such as email
  addresses or internal host names, add pattern rules. The adaptation notes below describe how.
- `.shellcheckrc`: The companion to the ShellCheck hook above, and the one place its options belong. The hook, an editor
  extension, and a direct CLI run all read it, so per-tool arguments drift apart. The bundled profile enables every
  optional check and disables two by name, with the reason attached to each. Adopting it in an established repository
  turns the whole shell tree red at once. The file's own comments carry the sweep procedure and the trap that makes a
  sweep look finished when it is not.

Read [config-adaptation-notes.md](references/config-adaptation-notes.md) before copying or changing a
configuration asset.

### Configuration Compatibility

Treat each formatter and linter pair as a pipeline. Run modifying hooks in configured order, run checking
hooks afterward, then repeat the complete sequence. A compatible configuration reaches a fixed point: the
second pass changes nothing and every checker succeeds.

Change a setting that both tools own only after exercising it on a representative fixture. The documentation of either
tool alone does not predict the pair. This matters most for Markdown list markers and numbering, line wrapping, hard
line breaks, frontmatter, tables, YAML aliases and comments, and shfmt's EditorConfig extensions.

Keep explanatory comments attached to retained settings. They record why patches and diffs avoid rewriting,
Markdown may preserve trailing spaces, Makefiles use tabs, and `[[shell]]` is a shfmt extension rather than a
standard EditorConfig section.

### Wrap Markdown Prose With Hard Breaks

The preferred convention wraps Markdown prose at the line limit. Every line of a paragraph but the last ends with a
trailing-backslash hard break (`\`). A soft wrap is short only in the raw file: the rendered page joins it into one long
line. The backslash, rather than two trailing spaces, stays visible and survives editors that trim whitespace. Where a
repository already soft-wraps by convention, keep its convention.

Rewrap long prose with the `markdown-tools` skill's `mdwrap.py`, typically right after the Markdown hooks are
enabled on existing documents.

## Preserve Safety Boundaries

- Leave the license, visibility, governance model, runtime, and framework to the user's choice.
- Take tool versions, paths, and commands from the repository or the user; a placeholder is better than a
  plausible invention.
- Describe a staged-diff secrets hook as covering new commits only, never as a history scan.
- Run one credential scanner: Betterleaks by default, or Gitleaks or Secretlint's recommended preset when the
  repository or the user selects it. Secretlint's home-path, dotenv, and pattern rules may run beside it, since
  they cover what it does not.
- Treat GitHub settings, dependency automation, CI, releases, and history rewrites as separate requests. List
  them as follow-ups rather than applying them as part of setup.

## Verify Completion

Check the exact files changed:

- the official ignore templates were used when applicable;
- configurations contain no unresolved placeholders or settings for tools the repository does not use;
- formatting and linting configurations reach a clean second pass on representative files;
- repository checks pass without weakening existing gates.

Report exact validation results and untested environments.

## Assets

Repository configuration: `.editorconfig`, `.gitattributes`, `.pre-commit-config.yaml`, `.markdownlint-cli2.jsonc`,
`.mdformat.toml`, `.secretlintrc.json`, `.shellcheckrc`, `.yamlfmt.yaml`, and `.yamllint.yaml`.

## Provenance

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources behind the Secretlint guidance.
