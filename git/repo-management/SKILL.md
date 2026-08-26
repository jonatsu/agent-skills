---
name: repo-management
description: "Set up, refresh, or clean up a repository's baseline and hygiene — new or long-existing — without assuming a language or framework. Use to bootstrap a repo (README, LICENSE, .gitignore, .editorconfig, .gitattributes, pre-commit) OR to fill gaps in an existing one, add or refresh hooks and community files, report tracked cruft (committed secrets, gitignored-but-tracked files, large files), and check whether an existing README still describes the repo. Triggers: set up a repo, bootstrap repo, initialize GitHub repository, template repository, add pre-commit hooks, add hygiene hooks, clean up this repo, repo hygiene, refresh repo baseline, add editorconfig/gitattributes/gitignore, scan for committed secrets or large files, stale README, missing LICENSE, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, issue or PR template. NOT for making commits, rebasing, recovering lost work, or git-history questions, which is git-operations."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Repo Management

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
Repo Management Progress:
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
  - [ ] (REFRESH, when a README already exists) check its concrete claims against
        the repo as it is now and REPORT the stale ones — see Stale README
        Detection below
- [ ] Step 6: Validate repository hygiene ⚠️ REQUIRED
  - [ ] Placeholders, links, project name, contact paths, dates
  - [ ] README covers what/why/how/help/maintainer where applicable
  - [ ] Generic config does not force stack-specific tooling
  - [ ] If a pre-commit config was created/changed, run it against changed files
- [ ] Step 7: Report follow-ups
  - [ ] GitHub optional settings: template toggle, branch protection, CODEOWNERS,
        security advisories, Dependabot, discussions, issue/PR settings
  - [ ] Agent onboarding docs (AGENTS.md, llms.txt) → offer the `agents-management` skill
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
`git-operations`, don't perform it here.

## Stale README Detection (REFRESH — report-only)

An existing README is the one hygiene file whose defect a presence check cannot
see: it is there, it is well-formed, and it describes a repo that has since moved.
Nothing else here catches that — Step 6 validates a README this skill just wrote,
and REFRESH otherwise leaves what "already exists and is healthy" untouched
without ever testing healthy.

Read the README and check each concrete claim against the repo as it is now:

- **Commands**, against `package.json` scripts, `Makefile`, `justfile`,
  `mise.toml` tasks, `pyproject.toml`, or CI workflows.
- **Paths and file names**, against the tree.
- **Capabilities, requirements and supported versions**, against the code and its
  dependency manifests.
- **Links**, against their targets.

REPORT each stale claim with the evidence that contradicts it. NEVER rewrite an
existing README's claims here: a claim that reads as stale may be the intended
behaviour and the code the regression, and this skill cannot tell which. Bump a
`Last reviewed` date only when the user approves the content change it attests to
— a fresh date over unverified prose is worse than a stale one, because it
certifies the sentence nobody checked.

## Baseline File Guidance

SHOULD start from a small generic baseline, then trim based on the answers:

- `README.md`: project purpose, status, quick start, usage, contributing, help,
  maintainer/contact. A README serves its reader, so shape it to the repo type
  classified in Step 2 — OSS, personal, internal, or config (XDG/dotfiles).
  Default to the generic `assets/README.template.md`; for a specific audience,
  start from the matching `assets/README.<type>.template.md` and include only the
  sections that type needs. See `references/readme-by-audience.md` for the
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
  When both `.mdformat.toml` and `.markdownlint-cli2.jsonc` are adopted, choose
  the MD013 limit deliberately: mdformat rewrites and markdownlint only reports,
  so a tight `line_length` turns every mdformat rejoin into a failing gate. The
  shipped asset uses 400; a repo choosing 80 or 120 will meet it often.
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
- history rewriting to purge committed secrets or large blobs (hand to `git-operations`)

## Template Assets

Copy or adapt these only after plan approval:

- `assets/README.template.md` (generic default) plus audience variants
  `assets/README.oss.template.md`, `assets/README.personal.template.md`,
  `assets/README.internal.template.md`, `assets/README.config.template.md`
  (see `references/readme-by-audience.md`)
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

## Reference Files

Read `references/readme-by-audience.md` when you are about to write or replace a
README and the repo's audience is settled — it carries the project-type
definitions and the section-by-audience matrix that decides which sections
belong. Reach for it at Step 4, after Step 2 has classified OSS, personal,
internal or config; it answers "which sections", not "which repo type".

Read `references/config-adaptation-notes.md` before trimming or extending any
`assets/*` config — the patch/diff safety rule, when a repo-specific exclusion is
justified, and when a stack hook may be added at all.

**Do NOT load either** to inspect a repo, classify its mode, run the cruft report,
or answer a question about hygiene in the abstract. Both are for the moment you
are about to write a file, and loading them earlier spends context on decisions
Steps 1–3 have not reached yet. Neither is needed to decide whether a change is
safe: that is the Iron Law and the approval gate, which are resident here.

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
- Rewrite an existing README's claims during a REFRESH, or bump its `Last
  reviewed` date, instead of reporting the staleness for the user to decide.
- Copy inspiration repositories or Jinja2 template syntax verbatim.
- Make a private/internal repo look like a public OSS community project.
- Drop a template asset's comments because the file you derived is short. That
  judgement is the trap: a trimmed config looks self-evident precisely when the
  reasoning has been removed. Carry the comment for every rule you keep. In
  `assets/.editorconfig` they are the CommonMark rationale for preserving
  trailing whitespace in Markdown, why Makefiles require tabs, and the fact that
  `[[shell]]` is a non-standard shfmt extension rather than an EditorConfig
  property — each one answers a question the next editor will otherwise resolve
  by guessing. Adapt values freely; keep the reasons attached to what survives.
- Break an inline code span across a line break in Markdown. mdformat will not
  wrap inside one, so it joins the whole paragraph onto a single line instead.
  The file comes back "modified by this hook" and MD013 then fails on one
  over-long line. The tell is a long joined line containing a backtick pair.

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
