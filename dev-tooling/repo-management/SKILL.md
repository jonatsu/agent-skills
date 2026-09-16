---
name: repo-management
description: Set up or refresh repository baseline files and hygiene hooks. Use for repository bootstrap, .gitignore, .editorconfig, .gitattributes, pre-commit configuration, community templates, or read-only hygiene and README-accuracy audits. Use git-ops for commits and history operations.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Repository Management

Apply an opinionated repository baseline without erasing established project conventions. The bundled
configurations and templates encode the author's personal preferences; treat them as deliberate defaults.
Repository evidence and explicit user choices take precedence when they conflict with those defaults.

This skill owns baseline files, repository-local hygiene hooks, community templates, and read-only hygiene
audits. Use `git-ops` for commits, branch or worktree operations, history investigation, recovery, and history
rewriting. Use `agents-management` for agent instruction files.

## Choose the Task

- **Targeted change:** Add or revise named baseline files or hooks. Inspect only the affected files, their
  consumers, and existing repository conventions.
- **Bootstrap:** Establish a baseline in a new or nearly empty repository.
- **Refresh:** Compare an established repository with the preferred baseline, then fill approved gaps without
  regenerating healthy files.
- **Audit:** Report tracked cruft, stale README claims, or missing hygiene without changing repository state.

A narrow request needs only a narrow inspection. Do not turn a request for one file into a full repository
audit. For broad or ambiguous work, inspect first and propose a concrete file-level plan before editing.

## Preserve Authorization

Reuse authorization already present in the request. A request naming the files or changes authorizes those
edits; do not require a second approval for the same scope. Ask when a missing choice would determine the
license, public behavior, repository visibility, governance model, toolchain, destructive target, or
outward-facing action.

An assessment or audit remains read-only. Report remediation separately because untracking files, deleting
content, publishing settings, and rewriting history require their own authority.

## Work Proportionately

1. Inspect the relevant repository state, existing files, configured checks, and instructions.
2. Decide whether the request is targeted, bootstrap, refresh, or audit work.
3. Resolve only choices that the repository and request do not already settle.
4. For broad work, identify each file to create, adapt, preserve, or skip and obtain approval for unresolved
   scope. For targeted work, proceed within the supplied authorization.
5. Apply the smallest coherent delta. Preserve existing content unless replacement is explicitly authorized.
6. Validate the changed artifacts with their actual consumers and repository checks.
7. Report completed work, deferred findings, and any external settings that still need user action.

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
  only the requested delta when extending an established configuration.
- Community files: Use the bundled contribution, security, conduct, pull-request, and issue templates when
  their workflow applies. Replace every placeholder and remove irrelevant sections.

Read [config-adaptation-notes.md](references/config-adaptation-notes.md) before copying or changing a
configuration asset.

### Configuration Compatibility

Treat each formatter and linter pair as a pipeline. Run modifying hooks in configured order, run checking
hooks afterward, then repeat the complete sequence. A compatible configuration reaches a fixed point: the
second pass changes nothing and every checker succeeds.

Do not customize a setting owned by both tools from documentation alone. Exercise a representative fixture
first. This is especially important for Markdown list markers and numbering, line wrapping, hard line breaks,
frontmatter, tables, YAML aliases and comments, and shfmt's EditorConfig extensions.

Keep explanatory comments attached to retained settings. They record why patches and diffs avoid rewriting,
Markdown may preserve trailing spaces, Makefiles use tabs, and `[[shell]]` is a shfmt extension rather than a
standard EditorConfig section.

## Run Hygiene Audits When Requested

Run the full audit only when the user requests an audit, cleanup assessment, or broad refresh that includes
hygiene. Keep it read-only:

- Gitignored but tracked files: `git ls-files -ci --exclude-standard`.
- Large tracked files: inspect a NUL-safe list without allowing pathnames to become command options.
- Committed secrets: use `betterleaks git .`, or the repository's established scanner. State that staged-diff
  hooks do not cover history.
- Historical large blobs: offer the heavier history scan and run it only when requested.

Report paths and remediation without exposing secret values. Rotate a leaked credential before removing it
from history. Hand history rewriting to `git-ops`.

### Check an Existing README

This check answers **is it still true**, not **does it read well**. A request to review a README for quality —
whether it reads flat, generic, or fails to make its case — belongs to `writing-readmes`. A thorough review
runs both.

When README accuracy is in scope, compare concrete claims with authoritative repository evidence:

- commands against task runners, package scripts, build files, and CI workflows;
- paths and file names against the tree;
- capabilities and supported versions against code and dependency manifests; and
- links against their intended targets.

For an audit, report each stale claim and the contradicting evidence. When the user authorizes a README
update, correct the claim only after deciding whether documentation or implementation represents the intended
behavior. Update a “Last reviewed” date only after verifying the content it attests to.

## Preserve Safety Boundaries

- Never choose a license, visibility, governance model, runtime, or framework for the user.
- Never invent project names, badges, links, contacts, commands, or supported versions.
- Never replace an existing healthy file merely to match a template.
- Never present a staged-diff secrets hook as a history scan.
- Never enable both Betterleaks and Gitleaks. Retain Betterleaks by default unless the repository or user
  selects Gitleaks.
- Never apply GitHub settings, dependency automation, CI, releases, or history rewrites as an implied part of
  repository setup.
- Never leave template placeholders in delivered files.

## Verify Completion

Check the exact files changed:

- project names, links, contacts, dates, badges, commands, and license references agree;
- canonical license and official ignore sources were used when applicable;
- templates contain no unresolved placeholders or irrelevant sections;
- formatting and linting configurations reach a clean second pass on representative files;
- repository checks pass without weakening existing gates; and
- audits changed no repository state.

Report exact validation results and untested environments. List relevant GitHub settings as follow-ups rather
than changing them without authorization.

## Assets

- README templates: `README.template.md` and the OSS, personal, internal, and configuration variants
- Community templates: `CONTRIBUTING.template.md`, `SECURITY.template.md`,
  `CODE_OF_CONDUCT.template.md`, `PULL_REQUEST_TEMPLATE.md`, and `ISSUE_TEMPLATE/*`
- Repository configuration: `.editorconfig`, `.gitattributes`, `.pre-commit-config.yaml`,
  `.markdownlint-cli2.jsonc`, `.mdformat.toml`, `.yamlfmt.yaml`, and `.yamllint.yaml`

## Provenance

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) and [LICENSE.upstream](LICENSE.upstream) for the adapted README taxonomy
and templates.
