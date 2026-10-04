# Attributions

## Chezmoi documentation

- Source: [chezmoi command overview](https://www.chezmoi.io/user-guide/command-overview/) and
  [reference](https://www.chezmoi.io/reference/).
- Influence: the command contracts for initialization, adding, re-adding, forgetting, and application order
  were checked against the current documentation and the installed chezmoi help. The skill states those facts
  in its own task-oriented terms.

## chezmoi_modify_manager documentation

- Source: [`docs/src`](https://github.com/VorpalBlade/chezmoi_modify_manager/tree/main/docs/src) at commit
  `62a4c18afbe478a7e6691101424ac74058593d7a` (read 2026-10-04).
- License: GPL-3.0, per the repository's `LICENSE.md`.
- Influence: verification only. `references/modify-manager.md` restates the tool's documented behavior, commands,
  and directive syntax in its own words. No documentation prose or example configuration was copied; the
  directive forms shown are the tool's input syntax.

## Paul Sorensen's chezmoi skill

- Source: [`skills/chezmoi`](https://github.com/paulnsorensen/skillz-that-grillz/tree/main/skills/chezmoi).
- License: MIT, copyright Paul Sorensen.
- Influence: its bootstrap and application-order coverage prompted corresponding branches in this skill.
  The wording, examples, and structure were written independently and checked against chezmoi's documentation.

## Terry Li's dotfiles-tools skills

- Source: [`chezmoi-workflows`](https://github.com/terrylica/cc-skills/blob/main/plugins/dotfiles-tools/skills/chezmoi-workflows/SKILL.md)
  and [`chezmoi-sync`](https://github.com/terrylica/cc-skills/blob/main/plugins/dotfiles-tools/skills/chezmoi-sync/SKILL.md).
- License: MIT, copyright Terry Li.
- Influence: their add, forget, diagnosis, and drift branches prompted a review of missing operations. This
  skill keeps its own per-target checks and Git authorization boundaries. No wording or example was copied.
