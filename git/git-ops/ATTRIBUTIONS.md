# Attributions

## Current Skill

- Skill: `git-ops`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original skill containing worktree guidance adapted from an upstream skill

## Original Author and Source

- Original author: Jesse Vincent
- Upstream project: [obra/superpowers](https://github.com/obra/superpowers)
- Upstream skill: `using-git-worktrees`
- Source path: `skills/using-git-worktrees/SKILL.md`
- Source commit: `bc868020bbcec32bbaf9d6b51fa0538dba0b487f`
- Source file:
  <https://github.com/obra/superpowers/blob/bc868020bbcec32bbaf9d6b51fa0538dba0b487f/skills/using-git-worktrees/SKILL.md>

## Adaptation Note

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

The remaining `git-ops` guidance was authored independently for this repository.

## Upstream License

The upstream source is used under the MIT License. See `LICENSE.upstream` for the preserved license text.
