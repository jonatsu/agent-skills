---
name: git-repo-hygiene
description: "Set up, refresh, or clean up Git repository hygiene for any repo — new or long-existing — without assuming a language or framework. Use to bootstrap a new repo's baseline (README, LICENSE, .gitignore, .editorconfig, .gitattributes, pre-commit) OR to add/refresh hygiene and cleanliness hooks on a pre-existing or messy repo, fill missing community files, and detect tracked cruft (committed secrets, gitignored-but-tracked files, large files) for cleanup. Triggers: set up a repo, bootstrap repo, initialize GitHub repository, template repository, add pre-commit hooks, add hygiene/cleanliness hooks, clean up this repo, repo hygiene, refresh repo baseline, add editorconfig/gitattributes/gitignore, scan for committed secrets or large files. NOT for making commits, rebasing, or git-history questions (use git-master)."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Git Repo Hygiene

IRON LAW: NEVER create, overwrite, or modify repository files until the user has
approved a concrete plan. When assessing an existing repo, NEVER mutate tracked
content — DETECT and REPORT cruft (secrets, ignored-but-tracked files, large
files); the user decides what to clean. MUST avoid language/toolchain opinions
unless the user confirms them.

## Mode Gate

Classify the repo first — it decides the workflow shape:

- **BOOTSTRAP**: no `.git/`, or an empty/near-empty repo with little or no
  hygiene. Establish a baseline from scratch.
- **REFRESH**: an existing repo with history and some (possibly stale or partial)
  hygiene. Fill gaps, add/refresh hooks and config, and report tracked cruft —
  do NOT re-scaffold what already exists and is healthy.

Both modes converge on the same propose → apply → validate tail. When unsure,
inspect first (Step 1), then classify.

## Workflow

```text
Git Repo Hygiene Progress:
- [ ] Step 1: Inspect repo state ⚠️ REQUIRED
  - [ ] Check `.git/` presence, commit count, current branch, remote
  - [ ] Inventory existing hygiene: README, LICENSE, .gitignore, .editorconfig,
        .gitattributes, pre-commit config, CONTRIBUTING, SECURITY,
        CODE_OF_CONDUCT, .github/ templates
  - [ ] Note pre-commit hooks and formatters already wired (don't duplicate them)
  - [ ] Note project name from directory, package metadata, or remote if present
- [ ] Step 2: Classify mode + ask only missing material questions ⛔ BLOCKING
  - [ ] Decide BOOTSTRAP vs REFRESH from Step 1
  - [ ] (BOOTSTRAP, if unknown) public/private; local-only/GitHub-backed;
        language/runtime or intentionally generic; OSS/community or internal;
        minimal/standard/advanced baseline; license choice or none
  - [ ] (REFRESH) ask only what the gap analysis cannot infer — e.g. which
        missing pieces to add, whether to add or upgrade pre-commit hooks
  - [ ] If repo-local checks are wanted, default pre-commit to include secrets
        scanning — propose `betterleaks`, offer `gitleaks` as the alternative;
        allow opt-out only with a brief risk note
- [ ] Step 3: Propose the plan ⛔ BLOCKING
  - [ ] (BOOTSTRAP) baseline file plan: create / adapt / leave / skip
  - [ ] (REFRESH) delta plan: what to ADD, what to REFRESH, what to LEAVE as-is
  - [ ] Separate baseline/delta from explicit follow-ups
  - [ ] Explain why each file/hook belongs; ask for explicit approval before editing
- [ ] Step 4: Generate/adapt files
  - [ ] Use `assets/*` as starting points; preserve existing content unless
        replacement is approved
  - [ ] Official GitHub `.gitignore` templates; canonical license text (NEVER
        invent license language)
  - [ ] pre-commit default: `pre-commit-hooks` + `betterleaks` (or `gitleaks`
        if chosen); stack hooks, linters, formatters opt-in only after
        stack/tooling confirmation
- [ ] Step 5: Cruft report ⚠️ REQUIRED when the repo has history (report-only)
  - [ ] Detect committed secrets, gitignored-but-tracked files, and large files
  - [ ] REPORT findings plus the remediation command for each; flag which are
        history-rewriting. NEVER untrack, delete, or rewrite tracked content
        without a separate explicit request
- [ ] Step 6: Validate repository hygiene ⚠️ REQUIRED
  - [ ] Placeholders, links, project name, contact paths, dates
  - [ ] README covers what/why/how/help/maintainer where applicable
  - [ ] Generic config does not force stack-specific tooling
  - [ ] If a pre-commit config was created/changed, run it against changed files
- [ ] Step 7: Report follow-ups
  - [ ] GitHub optional settings: template toggle, branch protection, CODEOWNERS,
        security advisories, Dependabot, discussions, issue/PR settings
  - [ ] Agent onboarding docs (AGENTS.md, llms.txt) → offer the `agent-repo-docs` skill
  - [ ] Any cruft the user chose to defer
```

## Cruft Detection (REFRESH — report-only)

Run these read-only checks and REPORT results. NEVER act on them without a
separate explicit request; several remediations rewrite history.

- **Gitignored-but-tracked files** (ignored patterns that were committed anyway):
  `git ls-files -ci --exclude-standard`
  Remediation: `git rm --cached <path>` (does not rewrite history).
- **Large tracked files** in the working tree (review before they grow):
  `git ls-files -z | xargs -0 du -h 2>/dev/null | sort -rh | head -20`
- **Committed secrets** across history: `betterleaks git .` (or `betterleaks
  dir .` for current filesystem state); with Gitleaks installed instead, the
  equivalents are `gitleaks git --no-banner` and `gitleaks detect`. Either
  pre-commit hook scans only the staged diff, so it NEVER covers history — run
  the history scan separately and say so when reporting.
  Remediation: rotate the secret first, then purge from history.
- **History bloat** (optional, heavier): largest blobs ever committed —
  mention it, run only on request.

Purging secrets or large blobs from history (`git filter-repo`, BFG) is
**history-rewriting and out of this skill's scope** — flag it and hand off to
`git-master`, don't perform it here.

## Baseline File Guidance

SHOULD start from a small generic baseline, then trim based on the answers:

- `README.md`: project purpose, status, quick start, usage, contributing, help,
  maintainer/contact. A README serves its reader, so shape it to the repo type
  classified in Step 2 — OSS, personal, internal, or config (XDG/dotfiles).
  Default to the generic `assets/README.template.md`; for a specific audience,
  start from the matching `assets/README.<type>.template.md` and include only the
  sections that type needs. See `reference/readme-by-audience.md` for the
  section-by-audience matrix.
- `LICENSE`: only when the user chooses a license; use canonical text.
- `.gitignore`: use official GitHub templates, not a baked-in generic file.
- `.editorconfig`: safe lowercase file with `root = true`, UTF-8, LF, trailing
  whitespace trimming, final newline. NEVER force one global indent style across
  mixed-language repos. If customizing sections, check EditorConfig glob syntax
  against the docs/spec.
- `.gitattributes`: keep core small: `* text=auto`, explicit shell/batch EOL
  rules if relevant, optional `export-ignore` only when source-archive hygiene
  matters. Avoid stack-specific diff drivers by default.
- `.pre-commit-config.yaml`: optional generic quality gate when repo-local checks
  are wanted. Default to `pre-commit-hooks` plus a secrets scanner; stack hooks,
  linters, and formatters are opt-in only after stack/tooling confirmation.
  `assets/.pre-commit-config.yaml` ships Betterleaks active with a commented
  Gitleaks block beneath it: propose Betterleaks, and if the user prefers
  Gitleaks, uncomment that block and delete the Betterleaks one. MAY
  add `editorconfig-checker` when `.editorconfig` is used and enforcement is
  desired. Prefer `types`/`types_or` for file selection; use Python-regex
  `files`/`exclude` only when type selection is insufficient. Optional format
  configs ship in `assets/` (`.markdownlint-cli2.jsonc`, `.mdformat.toml`,
  `.yamlfmt.yaml`, `.yamllint.yaml`) — add only the ones the approved plan wants.
- `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`: add for public, shared,
  or community repos as appropriate.
- `.github/PULL_REQUEST_TEMPLATE.md` and `.github/ISSUE_TEMPLATE/*`: lightweight
  templates when an issue/PR workflow is relevant.

## Explicit Follow-Ups, Not Baseline

MAY suggest these after the pass, but MUST NOT add unless the user explicitly
approves:

- `.github/dependabot.yml`
- `CODEOWNERS`
- branch protection and required checks
- GitHub security advisories / private vulnerability reporting
- template repository toggle
- stack-specific CI, lint, format, release, or dependency automation
- history rewriting to purge committed secrets or large blobs (hand to `git-master`)

## Template Assets

Copy or adapt these only after plan approval:

- `assets/README.template.md` (generic default) plus audience variants
  `assets/README.oss.template.md`, `assets/README.personal.template.md`,
  `assets/README.internal.template.md`, `assets/README.config.template.md`
  (see `reference/readme-by-audience.md`)
- `assets/CONTRIBUTING.template.md`
- `assets/SECURITY.template.md`
- `assets/CODE_OF_CONDUCT.template.md`
- `assets/PULL_REQUEST_TEMPLATE.md`
- `assets/ISSUE_TEMPLATE/bug_report.md`
- `assets/ISSUE_TEMPLATE/feature_request.md`
- `assets/.editorconfig`
- `assets/.gitattributes`
- `assets/.pre-commit-config.yaml`
- `assets/.markdownlint-cli2.jsonc`, `assets/.mdformat.toml`,
  `assets/.yamlfmt.yaml`, `assets/.yamllint.yaml` (optional format configs)

See `reference/config-adaptation-notes.md` for how to keep these generic.

## Anti-Patterns

NEVER:
- Mutate tracked content during an assessment — untrack, delete, or rewrite
  history — without a separate explicit request.
- Re-scaffold a file that already exists and is healthy in a REFRESH.
- Scaffold CI, release automation, package config, Docker, dependency managers,
  stack linters, stack formatters, or stack hooks without explicit user request.
- Create a pre-commit config without a basic secrets scanner (`betterleaks` or
  `gitleaks`) unless the user explicitly opts out after a brief risk note.
- Enable both secrets scanners at once. They scan the same staged diff for the
  same result; pick one and delete the other block.
- Present the secrets hook as history coverage. It scans the staged diff only;
  a secret committed three commits ago passes it.
- Choose a license, runtime, framework, GitHub visibility, or governance model
  for the user.
- Force one global indent style in a mixed-language repository.
- Add stale placeholders like `TODO`, `your-email@example.com`, or fake URLs.
- Replace existing repo files silently.
- Copy inspiration repositories or Jinja2 template syntax verbatim.
- Make a private/internal repo look like a public OSS community project.

## Pre-Delivery Checklist

Before final response, MUST verify:

- User approved the exact files changed.
- In REFRESH, no tracked content was mutated; cruft was reported, not silently
  cleaned, and existing healthy files were left untouched (not regenerated).
- No unresolved placeholders, fake links, fake emails, or template syntax remain.
- Project name, links, badges, contact paths, and license references agree.
- `.gitignore` and `LICENSE` came from official/canonical sources when used.
- `.editorconfig` does not create mixed-repo indentation mistakes.
- `.gitattributes` stays generic unless repo context justifies additions.
- Pre-commit config includes exactly one secrets scanner if created —
  `betterleaks` unless the user chose `gitleaks` — or records an explicit user
  opt-out, and has no unapproved stack hooks.
- GitHub follow-up settings are listed if relevant, not applied silently.
