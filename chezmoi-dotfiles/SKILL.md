---
name: chezmoi-dotfiles
description: Generic chezmoi dotfiles management across machines. Use for init, add, edit, apply, sync, templates, encryption, secrets, run scripts, conflict resolution, manage dotfiles, dotfile sync, chezmoi apply, chezmoi edit, chezmoi init, chezmoi diff, chezmoi update, chezmoi add. Triggers on chezmoi, dotfiles, dotfile management, cross-machine config sync.
---

# Chezmoi Dotfiles Management

IRON LAW: NEVER run `chezmoi apply` without `chezmoi diff` first. Blind apply overwrites uncommitted home dir changes.

## Workflow

```
Chezmoi Workflow Progress:

- [ ] Step 1: Assess ⛔ BLOCKING ⚠️ REQUIRED
  - [ ] 1.1 `chezmoi status` — check drift
  - [ ] 1.2 `chezmoi doctor` — verify env (if new machine)
- [ ] Step 2: Edit ⚠️ REQUIRED
  - [ ] 2.1 `chezmoi edit <file>` — edit source state
  - [ ] 2.2 `chezmoi diff` — preview changes BEFORE apply
- [ ] Step 3: Apply ⚠️ REQUIRED
  - [ ] 3.1 Confirm `chezmoi diff` output reviewed — no unexpected changes
  - [ ] 3.2 `chezmoi apply` — write source → home dir
- [ ] Step 4: Sync (if remote repo) (conditional)
  - [ ] 4.1 `chezmoi git -- pull` + `chezmoi diff` — review remote changes
  - [ ] 4.2 `chezmoi apply` — apply remote changes
  - [ ] 4.3 `chezmoi git -- add -A && commit && push` — push local changes
- [ ] Step 5: Verify
  - [ ] 5.1 `chezmoi verify` — confirm all files match source
```

## Quick Reference

```bash
chezmoi init                          # initialize (empty source)
chezmoi init --apply <repo-url>       # clone existing repo + apply
chezmoi add ~/.bashrc                 # track a file
chezmoi edit ~/.bashrc                # edit source in $EDITOR
chezmoi apply                         # apply source → home directory
chezmoi diff                          # preview pending changes
chezmoi update                        # pull + apply (one step)
chezmoi status                        # drift overview
chezmoi cd                            # shell into source dir
chezmoi doctor                        # diagnose environment
chezmoi unmanaged ~                   # list untracked files in home dir
```

## Source Filename Conventions

Chezmoi encodes metadata in source filenames — no separate config database.

| Prefix / Suffix   | Effect on target                        | Example                              |
| ----------------- | --------------------------------------- | ------------------------------------ |
| `dot_`            | Leading `.` in target name              | `dot_zshrc` → `.zshrc`              |
| `private_`        | 0600 (files) / 0700 (dirs) permissions  | `private_dot_ssh/`                   |
| `executable_`     | +x (755) permissions                    | `executable_setup.sh`                |
| `encrypted_`      | Decrypted transparently on apply        | `encrypted_private_key.age`          |
| `.tmpl` suffix    | Rendered as Go template before writing  | `dot_gitconfig.tmpl`                 |
| `run_once_`       | Run only on first apply (state-tracked) | `run_once_install-pkgs.sh`           |
| `run_onchange_`   | Run when script content changes         | `run_onchange_setup.sh`              |
| `run_always_`     | Run on every apply                      | `run_always_reload.sh`               |
| `run_before_`     | Run before files are written            | `run_before_decrypt.sh`              |
| `run_after_`      | Run after files are written             | `run_after_rehash.sh`                |

Prefixes compose: `private_dot_ssh/private_executable_deploy-key` → `~/.ssh/deploy-key` (0600, +x).

## Core Workflows

### Initialize

```bash
# Fresh start
chezmoi init
chezmoi add ~/.zshrc ~/.gitconfig
chezmoi git -- remote add origin git@github.com:<user>/dotfiles.git
chezmoi git -- push -u origin main

# Clone existing repo
chezmoi init --apply git@github.com:<user>/dotfiles.git

# Universal one-liner (installs chezmoi + inits)
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply <user>
```

### Daily edit loop

```bash
chezmoi edit ~/.zshrc          # edit source; does not apply automatically
chezmoi edit -a ~/.zshrc       # edit + auto-apply on save
chezmoi diff                   # preview before applying
chezmoi apply                  # apply all pending changes
```

### Absorb home dir changes

```bash
chezmoi re-add ~/.zshrc        # single file
chezmoi re-add                 # all managed files
```

Prefer `re-add` over `add` for already-managed files — tends to produce fewer extraneous diffs.

### Push to remote

```bash
chezmoi git -- add -A
chezmoi git -- commit -m "update dotfiles"
chezmoi git -- push
```

### Safe remote sync

```bash
chezmoi git -- pull              # pull source only, no apply
chezmoi diff                     # review what would change
chezmoi apply --dry-run --verbose
chezmoi apply
```

## Untrack / Remove

```bash
chezmoi forget --force ~/.config/app/config.local.toml  # stop tracking, keep file
chezmoi destroy ~/.config/app/config.local.toml         # remove source + delete file
```

## Validation

```bash
chezmoi verify                         # exit 0 = all files match source
chezmoi diff                           # empty = no drift
chezmoi managed                        # list all tracked files
chezmoi doctor | grep -v "^ok"         # warnings and errors only
chezmoi git -- log --oneline -5        # recent commit history
```

## Anti-Patterns

- ❌ `chezmoi apply` without `chezmoi diff` first
- ❌ `chezmoi re-add` on `.tmpl` files — clobbers template syntax with rendered output
- ❌ Plaintext secrets in source — use encryption or password manager template functions
- ❌ `chezmoi update` when review needed — use `git pull` + `diff` + `apply` separately
- ❌ Editing files in home dir directly then `apply` — home dir changes get overwritten

## Key Gotchas

- `chezmoi re-add` on `.tmpl` files: expands rendered dest → source, overwrites `.tmpl` syntax. Check `chezmoi source-path <file>` first — if ends in `.tmpl`, use `chezmoi edit` instead.
- `chezmoi status` columns: `[source][dest]` format — `MM` = both changed, ` M` = dest only changed, `DA` = deleted in source but exists in dest (often junk like `node_modules/`). Read both columns to understand drift direction.
- `chezmoi diff` direction: `-` lines = current dest (will be removed), `+` lines = target after apply (will be added). Not a standard git diff — the "from" is your live home dir, the "to" is the rendered source state.
- `run_once_` scripts won't re-run: already recorded in state. Reset with `chezmoi state delete-bucket --bucket=scriptState`.
- `forget` needs TTY: use `chezmoi forget --force <path>`.
- Flood of `DA` in status: untracked dirs (e.g. node_modules). Add patterns to `.chezmoiignore`.

## Pre-Delivery Checklist

- [ ] `chezmoi diff` run and reviewed before any `chezmoi apply`
- [ ] `chezmoi verify` exits 0 after apply
- [ ] No plaintext secrets in source state
- [ ] Template files checked with `chezmoi source-path` before `re-add`

## On-Demand References

Load these when workflow needs deeper detail:

| Topic | File |
|-------|------|
| Templates, variables, partials | `references/templates.md` |
| Encryption, password managers | `references/encryption-secrets.md` |
| Run scripts, ignore rules | `references/scripts-ignores.md` |
| Troubleshooting, conflicts, validation | `references/troubleshooting.md` |
| External docs URL index | `references/external-docs.md` |
