---
name: repo-management
description: "Set up or refresh repository baseline files and hygiene hooks: bootstrap, .gitignore, .editorconfig, .gitattributes, pre-commit configuration, community templates, and read-only audits of tracked cruft, large files, and committed secrets. Not for tuning an existing repository's linter rules (lint-config-audit), checking whether docs are still true (context-architecture), or commits and history (git-commits-and-recovery)."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Repository Management

Apply an opinionated repository baseline without erasing established project conventions. The bundled
configurations and templates encode the author's personal preferences; treat them as deliberate defaults.
Repository evidence and explicit user choices take precedence when they conflict with those defaults.

This skill owns baseline files, repository-local hygiene hooks, community templates, and read-only hygiene
audits. Neighbouring work has its own skill: `lint-config-audit` audits and tightens the checkers an
established repository already runs; `git-commits-and-recovery` owns commits, branches, recovery, and history
rewriting; `git-history-investigation` answers history questions; `using-git-worktrees` covers worktrees; and
`agents-context-docs` covers agent instruction files.

## Choose the Task

- **Targeted change:** add or revise named baseline files or hooks. Inspect only the affected files, their
  consumers, and the repository's existing conventions, since a request for one file is not a request for an
  audit.
- **Bootstrap:** establish a baseline in a new or nearly empty repository.
- **Refresh:** compare an established repository with the preferred baseline, then fill approved gaps and
  leave healthy files as they are.
- **Audit:** report tracked cruft, large files, committed secrets, or missing hygiene, and change nothing.

## Work Proportionately

1. Inspect the relevant repository state, existing files, configured checks, and instructions.
2. Resolve only the choices that the repository and the request leave open. Ask when a missing choice decides
   the license, public behavior, repository visibility, governance model, toolchain, a destructive target, or
   an outward-facing action.
3. For bootstrap, refresh, or ambiguous work, propose a plan naming each file to create, adapt, preserve, or
   skip, and get approval for the scope the request did not settle. A request naming its files or changes
   already authorizes them.
4. Apply the smallest coherent delta, and keep existing content unless the user authorized replacing it.
5. Validate each changed artifact with its real consumers and the repository's checks.
6. Report completed work, deferred findings, and external settings that still need the user's action.

An audit stays read-only through all of this. Report remediation separately, because untracking files,
deleting content, publishing settings, and rewriting history each need their own authorization.

## Apply the Preferred Baseline

Use assets as starting points after inspecting the repository:

- `README.md`: Start with `assets/README.template.md`. When audience-specific structure helps, read
  [readme-by-audience.md](references/readme-by-audience.md) and use the matching OSS, personal, internal, or
  configuration template. The templates settle which sections a type needs; apply `writing-readmes` to make
  the result worth reading, and `writing-for-humans` for prose quality.
- `LICENSE`: Add only the license the user selected, using its canonical text.
- `.gitignore`: Retrieve the applicable official GitHub template and adapt it to confirmed generated files.
- `.editorconfig`: The bundled profile deliberately uses two spaces as the fallback and supplies targeted
  overrides. Preserve these personal defaults for a new baseline; reconcile them with established project
  conventions during refresh work.
- `.gitattributes`: Keep the bundled cross-platform text, script, document, serialization, image, archive, and
  patch rules unless repository evidence requires a narrower adaptation.
- `.pre-commit-config.yaml`: The bundled asset is the full preferred profile: pre-commit-hooks, Betterleaks,
  EditorConfig checking, YAML and Markdown formatting and linting, a local invisible-character check for
  Markdown, ShellCheck, and shfmt. Use the complete profile when the user requests the preferred baseline. Make
  only the requested delta when extending an established configuration. The bundled hook revisions are a
  snapshot: run `pre-commit autoupdate` before first use, unless the user or repository pins them for a reason.
- `.shellcheckrc`: The companion to the ShellCheck hook above, and the one place its options belong — the hook,
  an editor extension, and a direct CLI run all read it, so per-tool arguments drift apart. The bundled profile
  enables every optional check and disables two by name, with the reason attached to each. Adopting it in an
  established repository turns the whole shell tree red at once; the file's own comments carry the sweep
  procedure and the trap that makes a sweep look finished when it is not.
- Community files: Use the bundled contribution, security, conduct, pull-request, and issue templates when
  their workflow applies. Replace every placeholder, remove irrelevant sections, and apply `writing-for-humans`
  to the text you write.

Read [config-adaptation-notes.md](references/config-adaptation-notes.md) before copying or changing a
configuration asset.

### Configuration Compatibility

Treat each formatter and linter pair as a pipeline. Run modifying hooks in configured order, run checking
hooks afterward, then repeat the complete sequence. A compatible configuration reaches a fixed point: the
second pass changes nothing and every checker succeeds.

Change a setting that both tools own only after exercising it on a representative fixture, because the
documentation of either tool alone does not predict the pair. This matters most for Markdown list markers and
numbering, line wrapping, hard line breaks, frontmatter, tables, YAML aliases and comments, and shfmt's
EditorConfig extensions.

Keep explanatory comments attached to retained settings. They record why patches and diffs avoid rewriting,
Markdown may preserve trailing spaces, Makefiles use tabs, and `[[shell]]` is a shfmt extension rather than a
standard EditorConfig section.

### Wrap Markdown Prose With Hard Breaks

The preferred convention wraps Markdown prose at the line limit and ends every line of a paragraph but the last
with a trailing-backslash hard break (`\`). A soft wrap is short only in the raw file: the rendered page joins it
into one long line. The backslash, rather than two trailing spaces, stays visible and survives editors that trim
whitespace. Where a repository already soft-wraps by convention, keep its convention.

Rewrap with `scripts/mdwrap.py` whenever a line-length rule reports long prose, typically right after the
Markdown hooks are enabled on existing documents. Run it with the files to list the blocks it would change, then
again with `--write`, then run the hook pipeline twice to its fixed point. Set `--width` to the repository's
markdownlint `line_length`; it defaults to 120. The script leaves front matter, headings, tables, code,
reference definitions, HTML blocks and alert markers alone, keeps every code span and link on one line, and keeps
list, heading, quote and fence markers off the start of a wrapped line. In report mode it exits 1 when a block
would change, so it can also gate a commit.

## Run Hygiene Audits When Requested

Run the full audit only when the user requests an audit, cleanup assessment, or broad refresh that includes
hygiene. Keep it read-only:

- Gitignored but tracked files: `git ls-files -ci --exclude-standard`.

- Large tracked files: `git ls-files -z | xargs -0 du -k -- | sort -rn | head`. The NUL separators and the
  `--` keep a file name such as `-big file` from being read as an option.

- Committed secrets: use `betterleaks git .`, or the repository's established scanner.

- Historical large blobs: offer this heavier scan of every object in history, and run it only when requested:

  ```sh
  git rev-list --objects --all |
    git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' |
    awk '$1 == "blob"' | sort -k2 -rn | head
  ```

Report paths and remediation without exposing secret values. Rotate a leaked credential before removing it
from history. Hand history rewriting to `git-commits-and-recovery`.

When the audit should also check whether the README or other documents are still true, run
`context-architecture`'s truth audit alongside it.

## Preserve Safety Boundaries

- Leave the license, visibility, governance model, runtime, and framework to the user's choice.
- Take project names, badges, links, contacts, commands, and supported versions from the repository or the
  user; a placeholder is better than a plausible invention.
- Describe a staged-diff secrets hook as covering new commits only, never as a history scan.
- Run one secrets scanner: Betterleaks by default, or Gitleaks when the repository or the user selects it.
- Treat GitHub settings, dependency automation, CI, releases, and history rewrites as separate requests. List
  them as follow-ups rather than applying them as part of setup.

## Verify Completion

Check the exact files changed:

- project names, links, contacts, dates, badges, commands, and license references agree;
- canonical license and official ignore sources were used when applicable;
- templates contain no unresolved placeholders or irrelevant sections;
- formatting and linting configurations reach a clean second pass on representative files;
- repository checks pass without weakening existing gates; and
- audits changed no repository state.

Report exact validation results and untested environments.

## Assets

- README templates: `README.template.md` and the OSS, personal, internal, and configuration variants
- Community templates: `CONTRIBUTING.template.md`, `SECURITY.template.md`,
  `CODE_OF_CONDUCT.template.md`, `PULL_REQUEST_TEMPLATE.md`, and `ISSUE_TEMPLATE/*`
- Repository configuration: `.editorconfig`, `.gitattributes`, `.pre-commit-config.yaml`,
  `.markdownlint-cli2.jsonc`, `.mdformat.toml`, `.shellcheckrc`, `.yamlfmt.yaml`, and `.yamllint.yaml`
- Script: `scripts/mdwrap.py`, the Markdown prose rewrapper; standard library only, tested on Python 3.12 and 3.13

## Provenance

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) and [LICENSE.upstream](LICENSE.upstream) for the adapted README taxonomy
and templates.
