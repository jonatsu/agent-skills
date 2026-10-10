---
name: chezmoi-dotfiles
description: Manage dotfiles with chezmoi. Use when setting up a new machine; adding, editing, re-adding, forgetting, applying, or syncing managed files; resolving source/target drift; or working on chezmoi templates, encrypted files, ignores, and scripts; or managing part of a file a program also writes with modify_ scripts, including INI files handled by chezmoi_modify_manager.
license: MIT
compatibility: Requires chezmoi. Git is required for source repositories that use Git. chezmoi_modify_manager is optional and needed only for targets whose modify scripts use it.
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

Inspect automatic Git behavior with `chezmoi dump-config` before changing source state. If `git.autoCommit` or
`git.autoPush` would commit or publish without authorization, stop before a source-changing command. The
configuration does not supply authorization.

Inspect `chezmoi status [target]...` before choosing a direction. Its columns are:

1. last state written by chezmoi to actual state; and
2. actual state to rendered target state, including what `chezmoi apply` will do.

For example, `DA` means the actual entry was deleted after chezmoi last wrote it and apply will create it
again. Do not interpret the columns as Git index and worktree status. `chezmoi diff [target]...` compares the
actual state with the rendered target: removed lines come from the actual file and added lines come from the
target state.

Check `chezmoi source-path <target>` for each target. When its name starts with `modify_`, the target is
produced by a modify script, and the add, re-add, and apply rules below change; read
[Modify Scripts](#modify-scripts) before choosing a direction.

## Choose the Change Direction

### Add a New Target

When an actual file should become managed, inspect it for secrets and check whether its parent directory is
already managed. Use `chezmoi add <target>` for an ordinary file, or select `--template` or `--encrypt` when
needed. Adding an already managed target replaces its source state with the actual file, so check its status
and source diff before doing so; for a modify-script target that destroys the script. After adding, inspect
`chezmoi source-path <target>` and the source repository diff, then verify the rendered target.

For a target that does not yet exist, use `chezmoi add --new <target>` after checking the installed help. A
directory add recurses by default, so limit its scope before it captures unrelated files.

### Change Source State, Then Apply

Use this path when the source should define new target contents:

```bash
chezmoi edit <target>
chezmoi diff <target>
chezmoi apply <target>
chezmoi verify <target>
```

For a deliberately narrow edit, `chezmoi edit --apply <target>` can combine the edit and apply. Before a
broad apply or `init --apply`, review `chezmoi diff` and use `chezmoi apply --dry-run --verbose` when scripts,
removals, permissions, or many targets are involved. Chezmoi runs configured hooks even under `--dry-run`, so
understand and authorize their side effects before running the preview.

Current chezmoi prompts before overwriting a target modified since chezmoi last wrote it. Preserve that
protection. Do not add `--force`, suppress interaction, or rely on an unavailable prompt without confirming
the affected targets and the user's authority. Modify-script targets get no prompt at all, so review their
diff before every apply that includes them.

### Preserve an Intentional Actual-State Change

Use this path when the actual file contains the desired change:

1. Inspect `chezmoi status <target>`, `chezmoi diff <target>`, and `chezmoi source-path <target>` to confirm
   that the actual file is the version to preserve.
2. Run `chezmoi re-add <target>` for a modified managed file. It preserves an `encrypted_` attribute but does
   not overwrite templates or re-add non-file entries. It also skips modify-script targets; capture those as
   [Modify Scripts](#modify-scripts) describes.
3. Inspect the source repository diff and `chezmoi diff <target>`. Confirm that only the intended source path
   changed and that the rendered result matches the desired actual file.

With no target, `chezmoi re-add` captures every modified managed file. A directory target recurses by default;
use `--recursive=false` when that recursion is unwanted. Review each affected path and automatic Git behavior
before either broad form. Update a template with `chezmoi edit <target>` or reconcile it with
`chezmoi merge <target>`, then preview and apply the rendered result.

### Stop Managing a Target

Use `chezmoi forget <target>` when the target should remain in the home directory but leave source state. Check
that it is managed, name the exact target, and review the source repository diff afterward. `forget` cannot
remove an external; change its owning external declaration instead. Confirm the actual file still exists.
Keep interactive confirmation unless the specific operation and target have already been authorized.

### Reconcile Divergence

Use `chezmoi merge <target>` when both actual and source-derived states contain changes worth keeping. Inspect
`merge.command` and `merge.args` in `chezmoi dump-config` first: chezmoi supplies destination, source, and
rendered-target files, while the configured merge tool determines which file receives the result.

After the merge, inspect the actual file, `chezmoi source-path <target>`, and the source repository diff.
Ensure the reconciled content is stored in source state, editing the source or template when necessary. Run
`chezmoi diff <target>` and apply only after the rendered target contains the complete result.

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

Treat `chezmoi update` as pull plus apply, not as a preview. Inspect `update.command`, `update.args`, and
`update.apply` in `chezmoi dump-config`. The default Git path uses `git pull --autostash --rebase`, so do not
run it with dirty source work. Use `chezmoi update --apply=false` to pull without applying, then inspect
`chezmoi diff`, run an authorized dry-run if useful, apply, and verify. A custom update command may have
different side effects; inspect it before execution.

Before committing, inspect the index and source diff. Stage explicit source paths only. Push only when the
user has authorized publishing to the resolved remote and branch.

## Set Up a New Machine

For a new machine or first source initialization, read [references/bootstrap.md](references/bootstrap.md)
before running `chezmoi init`. Resolve the source repository, config template, local changes, secrets, and
scripts before applying. Treat `init --apply` as an apply operation with the same target and side-effect checks
as an ordinary apply.

## Modify Scripts

A `modify_` source entry is a script, not a copy of the file. It receives the current file on standard input and
prints the new contents; when the file does not exist, its input is empty and it must print a complete file. Use
one for a file that a program also writes, when only part of the file should be managed. A script that holds the
`chezmoi:modify-template` comment is a template run against `.chezmoi.stdin` instead, and must not carry a
`.tmpl` suffix.

Three plain-chezmoi commands behave differently on these targets, silently and with exit status 0:

- `chezmoi apply` overwrites local changes without the usual prompt, even when `status` reports the target as
  modified. Review `chezmoi diff <target>` first, and capture any local change worth keeping before applying.
- `chezmoi re-add` skips the target and captures nothing.
- `chezmoi add <target>` replaces the modify script with a plain copy of the file, discarding the script's
  logic.

Capture a change to a modify-script target by editing the script, or the data file it reads, in the source
directory. Then confirm with `chezmoi cat <target>` and `chezmoi diff <target>` that the script reproduces the
wanted file. These three behaviors were verified on chezmoi v2.72.2 on 2026-10-04.

When the script's first line names `chezmoi_modify_manager` as its interpreter, the target is an INI file
managed by that optional tool. Check `command -v chezmoi_modify_manager`. When it is installed, read
[references/modify-manager.md](references/modify-manager.md) before changing the target. When it is missing,
apply fails for that target with exit status 127 and leaves the file unchanged; report that, and leave
installing the tool to the user.

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

Chezmoi computes source, destination, and target states before running `run_before_` scripts. Externals are
updated later with target entries, so a `run_before_` script must not depend on a newly applied external. Put
that work in `run_after_`. Do not let an apply script change source or destination state while chezmoi is
running; chezmoi's behavior is undefined if those states change during the run.

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

## Diagnose Problems

When configuration, dependencies, or unexpected chezmoi behavior need diagnosis, run `chezmoi doctor` and
inspect its findings before changing source or target state. Use `chezmoi doctor --no-network` when network
access is not authorized or needed.

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
