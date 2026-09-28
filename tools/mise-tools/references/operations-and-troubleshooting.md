## Diagnostic sequence

Follow SKILL.md's "Diagnose Before Repairing" sequence and its trust, safe-mode, and auto-install
gates. The patterns below map a symptom to its likely cause.

## Common failure patterns

### Tool installed, but command still not found

Likely causes:

- script used `mise use` or `mise install`, but never executed through `mise exec --`
- shell hook never reloaded
- wrong activation model chosen
- a per-process override like `MISE_<TOOL>_VERSION` points at a different or unavailable version

### Shim reports "No version is set" from a directory that does not declare the tool

A tool declared only in a project `mise.toml` is on `PATH` as a shim everywhere, but the shim resolves a
version only from the config active in the caller's directory. A process the harness launches from
elsewhere — an editor hook, an MCP launcher, a connect-time credential helper — then fails with
`No version is set for shim: <tool>` even though the tool is installed. Move such a tool to the global
config; see `SKILL.md`, "Choose Scope and Execution". Observed on mise 2026.9.7.

### Many existing shims report "No version is set" after one TOML edit

Do not follow each shim's suggestion to add a new global declaration. First inspect the edited file's parsed
`tools` tree. A newly inserted `[tools."backend:configured-tool"]` header can capture every later flat tool
declaration because TOML retains the table scope. The tools remain installed, but mise no longer sees their
declarations at the expected paths.

Move flat sibling declarations before the first tool subtable, then verify the structured config, `mise ls`,
and representative unaffected shims. See `config-and-env.md`, "Preserve TOML ownership".

### Shell activation works in one shell, fails in another

Likely causes:

- activation placed in the wrong startup file
- prompt hooks not running in the actual shell mode
- editor, tmux, or remote shell needs shims instead

### Project env vars missing

Likely causes:

- shims were used, but plain shell commands expected `[env]` values
- wrong config root or environment overlay
- trust blocked env directives

### Parent repo or home config leaks into the project

Likely causes:

- config search walks farther up than expected
- missing monorepo or ceiling-path control

### Container image works until the home directory is mounted

Likely cause:

- tools were installed into user-home locations instead of system-level install paths

### Reproducibility drift

Likely causes:

- fuzzy versions without lockfile
- no `min_version`
- lockfile not regenerated or not committed

### `mise install --force` left the tool gone, not stale

`--force` runs an **uninstall step first**, then installs. A force-reinstall that fails partway leaves the tool removed
rather than at its previous version, and the failure message describes the install, not the removal.

Never force-reinstall a tool you depend on mid-task without a restore plan. If one fails, reinstall without `--force` to
recover.

### A force-reinstall breaks when the installer is itself a mise-managed tool

`mise install --force` with no arguments reinstalls **every** configured tool and exempts nothing — including tools mise
uses for installation. Declare `cargo-binstall` in the config and a forced run replaces cargo-binstall while other
`cargo:` crates are being installed through it. The first forced run fails and plain re-runs then succeed, so it reads as
intermittent.

Observed on mise 2026.8.12 with cargo-binstall 1.21.1:

```text
ERROR ~/.local/share/mise/shims/cargo-binstall failed
  × For crate <name>: Fallback to cargo-install is disabled
```

Two things compound it:

- mise passes `--disable-strategies compile,quick-install` to an external cargo-binstall, and its own `cargo install` retry
  fires **only on exit code 94** ("no prebuilt artifact"). Other binstall errors do not trigger it, and binstall does not
  return 94 when compile is disabled and no artifact exists.
- `cargo.binstall_native` applies only "when cargo-binstall is not installed". Setting it true while cargo-binstall is
  installed leaves it inert, so a config can declare a fallback it never uses.

Check for **every** copy before concluding it is gone. `type -a cargo-binstall` can list a stray `CARGO_HOME/bin` artifact
from a plain `cargo install`, the mise install directory, and the shim — and `CARGO_HOME/bin` often wins on PATH, so removing
only the mise tool entry changes nothing.

### Go tools write to `$HOME/go`

mise sets no `GOPATH` and does not know about `GOMODCACHE`, so `go install` falls back to Go's own `$HOME/go` default
in any context that did not export `GOPATH`. Load `references/go-backend.md`.

### Removing a tool leaves its lockfile entry

Deleting a tool from `mise.toml` does not remove its `[[tools.<name>]]` stanza from `mise.lock`. Neither
`mise install` nor `mise prune` prunes the lock, so it keeps advertising a tool the config no longer
declares. Remove the stanza by hand, then run `mise install` to confirm the lock and config agree.

Changing a version specifier **accumulates** rather than replaces: pinning a tool at `"latest"` after it was
pinned at `"3.13.3"` leaves `specifiers = ["3.13.3", "latest"]` in the lock. Trim the stale specifier by hand.
Observed on mise 2026.9.7.

### `mise prune` uninstalls by the active config and skips the lockfile

`mise prune` with no flags prunes only configuration links; pruning tools needs `--yes`. `mise prune --yes` then
uninstalls every installed tool version not referenced by the config active in the **current directory** — so
running it inside a project can uninstall a version only a global or sibling config still wants, including an
orphaned older version of a tool you depend on. Inspect `mise ls` first, and run prune from a directory whose
config resolution covers everything you mean to keep. Prune also does not edit `mise.lock`. Observed on mise
2026.9.7.

## Practical fixes

- For automation, switch to `mise exec --`.
- For interactive shells, verify the exact rc file and restart or re-source it.
- For CI output clarity, prefer task output modes that preserve logs usefully.
- For nested repos, inspect config resolution with `mise cfg`.
- For secrets, move them into local or dotenv-backed layers instead of committed config.

## Experimental-feature reminder

If the setup uses `mise mcp`, OCI, bootstrap, deps, dotfiles, or task templates, verify that:

- the installed mise version supports them
- the workflow tolerates experimental behavior
- the final answer labels them explicitly as experimental
