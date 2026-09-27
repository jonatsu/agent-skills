# Attributions

## Current Skill

- Skill: `using-git-worktrees`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from an upstream skill of the same name

## Original Author and Source

- Original author: Jesse Vincent
- Upstream project: [obra/superpowers](https://github.com/obra/superpowers)
- Upstream skill: `using-git-worktrees`
- Source path: `skills/using-git-worktrees/SKILL.md`
- Source commit: `bc868020bbcec32bbaf9d6b51fa0538dba0b487f`
- Source file:
  <https://github.com/obra/superpowers/blob/bc868020bbcec32bbaf9d6b51fa0538dba0b487f/skills/using-git-worktrees/SKILL.md>

## Adaptation Note

This package reached its current form in two stages. The upstream skill was first adapted into the `git-ops`
skill as its worktree reference, rewritten around the official Git worktree model. On 2026-09-27 that material
moved here as a standalone skill, and the upstream's detect-then-prefer-the-harness flow, name, and
rationalization table were restored around it.

Retained from the upstream: detecting an existing linked worktree before creating one, preferring the
harness's own worktree mechanism over `git worktree add`, asking before isolating unless a preference is
declared, the location priority of declared preference over an existing project-local directory, verifying that
a project-local directory is ignored, recording a baseline, the ready report, and the rationalization table.

Material changes include:

- removing product-specific tool names so the skill stays portable across agent harnesses;
- replacing automatic dependency installation with the repository's documented setup, because the upstream
  mapped every `pyproject.toml` to Poetry and every `requirements.txt` to an unscoped `pip install`;
- replacing the upstream's edit-and-commit of `.gitignore` with a sibling directory outside the repository;
- replacing the silent fall back to working in place after a sandbox denial with a report and a question;
- correcting the upstream claim that a submodule makes `--git-dir` and `--git-common-dir` differ, which does
  not hold on Git 2.43.0, and stopping on submodules because Git documents their multiple checkouts as
  incomplete;
- adding start-state recording, explicit start points, collision checks, post-creation verification, shared
  state across worktrees, and the finishing, maintenance, and problem guidance in
  `references/finish-and-maintain.md`.

## Upstream License

The upstream source is used under the MIT License. See `LICENSE.upstream`.
