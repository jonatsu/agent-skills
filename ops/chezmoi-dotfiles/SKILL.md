---
name: chezmoi-dotfiles
description: Manage chezmoi edits, applies, syncs, templates, scripts, ignores, secrets, and conflicts.
license: MIT
compatibility: Requires chezmoi. Git is required for source repositories that use Git.
metadata:
  author: Joonas Onatsu
---

# Chezmoi Dotfiles

Manage the source state, actual files, and rendered target state without losing local changes. Treat the
installed chezmoi version as the authority for command behavior. Check `chezmoi --version` and
`chezmoi <command> --help` before relying on version-sensitive flags, then use the official documentation
when help does not answer the question.

## Establish Ownership and State

Read the repository and machine instructions before changing files. Determine:

- which target paths the request covers;
- whether the source directory uses Git, templates, encryption, scripts, or automatic apply and push;
- whether the actual file contains changes that chezmoi did not write.

Inspect automatic Git behavior with `chezmoi dump-config` before changing source state. If `git.autoPush` is
enabled and the user has not authorized publishing, stop before a source-changing command. Disclose an
enabled `git.autoCommit` when the requested edit did not already authorize a commit.

Inspect `chezmoi status [target]...` before choosing a direction. Its columns are:

1. last state written by chezmoi to actual state; and
2. actual state to rendered target state, including what `chezmoi apply` will do.

For example, `DA` means the actual entry was deleted after chezmoi last wrote it and apply will create it
again. Do not interpret the columns as Git index and worktree status. `chezmoi diff [target]...` compares the
actual state with the rendered target: removed lines come from the actual file and added lines come from the
target state.

## Choose the Change Direction

### Change Source State, Then Apply

Use this path when the source should define new target contents:

```bash
chezmoi edit <target>
chezmoi diff <target>
chezmoi apply <target>
chezmoi verify <target>
```

For a deliberately narrow edit, `chezmoi edit --apply <target>` can combine the edit and apply. Before a
broad apply, `update`, or `init --apply`, review `chezmoi diff` and use
`chezmoi apply --dry-run --verbose` when scripts, removals, permissions, or many targets are involved.

Current chezmoi prompts before overwriting a target modified since chezmoi last wrote it. Preserve that
protection. Do not add `--force`, suppress interaction, or rely on an unavailable prompt without confirming
the affected targets and the user's authority.

### Preserve an Intentional Actual-State Change

Use this path when the actual file contains the desired change:

1. Inspect `chezmoi status <target>` and `chezmoi source-path <target>`.
2. Run `chezmoi re-add <target>` for a managed non-template file.
3. Inspect the source repository diff and confirm that only the intended source path changed.

Current `re-add` does not overwrite templates. Update a template with `chezmoi edit <target>` or reconcile it
with `chezmoi merge <target>`, then preview and apply the rendered result. Check live help when supporting an
older chezmoi version.

### Reconcile Divergence

Use `chezmoi merge <target>` when both actual and source-derived states contain changes worth keeping. Review
the merged source, run `chezmoi diff <target>`, and apply only after the rendered target is correct.

For Git conflicts, published rollback, or history repair, use the available Git operations guidance. Preserve
dirty work before changing history. Revert published commits with `git revert`; do not prescribe destructive
reset or checkout recovery.

## Sync a Git-Backed Source

Inspect the source repository before pulling or publishing:

```bash
chezmoi git -- status --short
chezmoi git -- diff
```

Preserve unresolved or unrelated work before pulling. After a safe pull, review `chezmoi diff`, run a dry-run
when the change is broad or includes scripts, apply, and verify.

Before committing, inspect the index and source diff. Stage explicit source paths only. Push only when the
user has authorized publishing to the resolved remote and branch. Automatic `git.autoCommit` or
`git.autoPush` configuration does not supply missing authorization.

## Templates, Scripts, and Ignores

Use templates for machine-dependent content. Test a rendered value with `chezmoi execute-template`, and
inspect a complete rendered target with `chezmoi cat <target>`.

`.chezmoiscripts/` keeps scripts out of the target state; its subdirectory names do not select an operating
system. Gate an operating-system-specific script in its rendered content. An empty rendered script does not
run:

```gotemplate
{{ if eq .chezmoi.os "linux" -}}
#!/bin/sh
command ...
{{ end -}}
```

Scripts that call chezmoi should use the executable path supplied by chezmoi:

```sh
"$CHEZMOI_EXECUTABLE" age decrypt ...
```

`run_once_` records each successfully executed rendered-content hash. A changed rendered script can run
again, even with the same filename. `chezmoi state delete-bucket --bucket=scriptState` clears the history for
all `run_once_` scripts, so disclose that broad effect and obtain approval before using it.

`.chezmoiignore` patterns match target paths. Use `.config/nvim/**`, for example, rather than the source path
`dot_config/nvim/**`. The ignore file is always a template, so gate target paths there for machine-specific
selection. Verify the result with `chezmoi --no-tty ignored`.

## Protect Secrets

Never store plaintext credentials in source state. Prefer password-manager template functions or
`chezmoi add --encrypt <target>`. Configure additions to fail closed where practical:

```toml
[add]
  secrets = "error"
```

Treat rendered output, diffs, logs, and temporary merge files as sensitive when templates or encrypted files
produce secrets. Do not publish source changes until secret checks and the staged diff are clean.

## Completion

Verify the requested scope rather than assuming a successful command covered it:

```bash
chezmoi status <target>...
chezmoi diff <target>...
chezmoi verify <target>...
```

Confirm that remaining status entries are understood, the source repository contains only intended changes,
scripts and ignores select the expected machines, and no plaintext secret entered the source or Git index.
Report any skipped apply, unavailable prompt, unresolved drift, or unverified platform.

## Live References

Use [references/official-docs.md](references/official-docs.md) to reach the relevant official reference when
installed help does not settle version-sensitive behavior. Load only the section needed for the active task.
