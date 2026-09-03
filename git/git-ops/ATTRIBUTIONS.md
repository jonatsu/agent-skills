# Attributions

## Current Skill

- Skill: `git-ops`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original skill containing worktree and commit-message guidance adapted from two upstream skills

Two references are adapted, each from a different upstream, and the sections below name them separately. The
remaining `git-ops` guidance was authored independently for this repository.

## Original Author and Source: Worktrees

Applies to `references/worktrees-and-stashes.md`.

- Original author: Jesse Vincent
- Upstream project: [obra/superpowers](https://github.com/obra/superpowers)
- Upstream skill: `using-git-worktrees`
- Source path: `skills/using-git-worktrees/SKILL.md`
- Source commit: `bc868020bbcec32bbaf9d6b51fa0538dba0b487f`
- Source file:
  <https://github.com/obra/superpowers/blob/bc868020bbcec32bbaf9d6b51fa0538dba0b487f/skills/using-git-worktrees/SKILL.md>

## Adaptation Note: Worktrees

The concurrent worktree workflow in `references/worktrees-and-stashes.md` was informed by the upstream
`using-git-worktrees` skill. This version integrates worktrees into a broader Git operations skill and was
rewritten around the official Git worktree model.

Material changes include:

- separating portable Git behavior from an explicitly labeled Claude Code-only branch;
- accounting for shared refs, configuration, objects, and stash state across worktrees;
- replacing automatic setup and project-local placement with repository-directed choices;
- adding mixed-hunk ownership, concurrent `HEAD` movement, generated-file, integration, and cleanup checks;
  and
- correcting the upstream submodule and nested-worktree assumptions against Git's documentation.

## Original Author and Source: Commit Messages

Applies to `references/commit-messages.md`.

- Original author: Muhammad Usman
- Upstream project:
  [MuhammadUsmanGM/claude-code-best-practices](https://github.com/MuhammadUsmanGM/claude-code-best-practices)
- Upstream skill: `conventional-commit`
- Source path: `plugins/commit-helper/skills/conventional-commit/SKILL.md`
- Source commit: `763de2a8e29e8c698eb540337ad1cfb55e734641`
- Source file:
  <https://github.com/MuhammadUsmanGM/claude-code-best-practices/blob/763de2a8e29e8c698eb540337ad1cfb55e734641/plugins/commit-helper/skills/conventional-commit/SKILL.md>

## Adaptation Note: Commit Messages

The upstream skill is a self-contained commit workflow covering staging, message drafting, confirmation, and
committing. Only its message-drafting guidance was adapted, as a reference under this skill.

Material changes include:

- dropping the staging, confirmation, and committing steps, which `SKILL.md` already owns under stricter
  rules, and whose upstream offer to stage everything contradicts this skill's concurrency boundaries;
- dropping the `--no-verify`, push, and amend prohibitions as already covered by `SKILL.md`;
- keeping the upstream rule that attribution trailers require permission, and giving it a section stating why
  it is needed;
- keeping the upstream practice of reading recent history to match repository style, and extending it to
  enforced conventions such as `commitlint` configuration;
- adding specification detail the upstream omits, taken from the Conventional Commits 1.0.0 specification
  rather than from the upstream skill: the `!` breaking-change marker, the uppercase `BREAKING CHANGE`
  requirement and its `BREAKING-CHANGE` synonym, git trailer footer syntax, and the SemVer correlation of
  `feat` and `fix`; and
- adding the effect-over-mechanism subject rule and the body anti-pattern, which the upstream does not cover.

## Upstream Licenses

Both upstream sources are used under the MIT License. See `LICENSE.upstream`, which preserves each license
text under the reference it applies to.
