# Troubleshooting, Conflicts, Validation

## Conflict Resolution

### Source vs. destination diverged (3-way merge)

When file edited both in `~/` and in source:

```bash
chezmoi merge ~/.zshrc          # 3-way merge: dest | source | rendered target
```

Configure merge tool in `~/.config/chezmoi/chezmoi.toml`:

```toml
[merge]
  command = "nvim"
  args = ["-d", "{{ .Destination }}", "{{ .Source }}", "{{ .Target }}"]
```

Unset → consults `git config merge.tool`, falls back to vimdiff.

### Git-level conflicts (after pull / update)

```bash
chezmoi git -- status           # identify conflicted files
chezmoi git -- diff             # review
# manually resolve in $(chezmoi source-path)
chezmoi git -- add <file>
chezmoi git -- commit -m "resolve conflict"
chezmoi apply
chezmoi git -- push
```

## Rollback (No Undo)

Chezmoi has no built-in undo. Roll back via git on the source side:

```bash
chezmoi cd                           # enter source dir
git reset --hard HEAD~1              # revert last commit
chezmoi apply                        # re-apply old state to home dir
```

For single-file rollback:

```bash
chezmoi cd
git checkout HEAD~1 -- <source-path>  # restore one file from prior commit
chezmoi apply <target-path>
```

## Troubleshooting Table

| Issue                     | Cause                             | Solution                                                          |
| ------------------------- | --------------------------------- | ----------------------------------------------------------------- |
| `chezmoi` not found       | Not installed                     | `sh -c "$(curl -fsLS get.chezmoi.io)"` or `brew install chezmoi` |
| Source path empty         | Not initialized                   | `chezmoi init`                                                    |
| Git remote not set        | Missing repo                      | `chezmoi git -- remote add origin <url>`                          |
| Apply fails               | Template error                    | `chezmoi diff` or `chezmoi execute-template` to inspect           |
| Merge conflicts           | Diverged source and target        | `chezmoi merge <file>` for 3-way merge                            |
| Secrets in diff           | Plaintext credentials in source   | Use encryption or password manager template functions             |
| `forget` needs TTY        | Interactive confirmation           | Use `chezmoi forget --force <path>`                               |
| Template not found        | Missing `.tmpl` suffix            | `chezmoi add --template` or `chezmoi chattr +template`            |
| `re-add` clobbers `.tmpl` | Expands rendered dest → source    | Check `chezmoi source-path <file>` before re-adding               |
| `MM` in status output     | Both source and dest changed      | Use `chezmoi merge <file>` for 3-way merge                        |
| `run_once_` won't re-run  | Already recorded in state         | `chezmoi state delete-bucket --bucket=scriptState`                |
| Flood of `DA` in status   | Untracked dirs (e.g. node_modules)| Add patterns to `.chezmoiignore`                                  |
