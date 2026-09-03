## When to load this file

Load this whenever the `go:` backend is involved, whenever a `go.*` setting is being chosen, or whenever Go
writes files somewhere unexpected — most often `$HOME/go`.

## What the `go:` backend actually does

It shells out to `go install`. It does not reimplement the Go toolchain, and it requires a `go` already on
`PATH` (mise-managed or not).

Environment applied to that subprocess, lowest precedence to highest:

1. mise's own inherited process env — the install command is not `env_clear`ed
2. the `go` core plugin's `exec_env` — `GOROOT`/`GOBIN`/`GOPATH` per the `go.*` settings
3. the config `[env]` block, which lands last inside the toolset env and therefore beats the plugin's
   `exec_env`
4. `GOROOT` deleted unconditionally
5. per-tool `install_env`
6. `GOBIN` forced to that tool's own install directory

Two consequences fall out of that ordering:

- **`GOROOT` is the one variable `[env]` cannot set for a `go:` install.** It arrives at layer 3 and is
  removed at layer 4. Only `install_env` can set it, and upstream ordered it that way deliberately so a
  `GOROOT` set there still wins. The removal exists because an inherited `GOROOT` pointing at a different Go
  than the one on `PATH` fails every compile.
- **`GOBIN` is not user-controllable at all for `go:` installs.** Layer 6 always wins, so `[env]`, ambient,
  and `install_env` values are all overwritten.

## Where the module cache goes, and why it lands in `$HOME/go`

mise sets **no** `GOPATH` by default and has **no** concept of `GOMODCACHE` — the variable appears nowhere in
its source. Both are inherited from the ambient environment.

Go's own default `GOPATH` is `$HOME/go` whenever the variable is unset, and `GOMODCACHE` defaults to
`$GOPATH/pkg/mod`. So a `go:` install from any context that did not export `GOPATH` writes its module cache to
`$HOME/go/pkg/mod`. A shell rc file is not enough: installs spawned by editors, run scripts, CI, or agents
never source it.

The signature of this happening is a `$HOME/go` containing `pkg/mod` and **no** `bin/` — because layer 6 sent
the binaries elsewhere.

Set `GOPATH` in the config `[env]` block to fix it for every mise-spawned process, install included.

## `go.*` settings

| Setting                    | Default                        | What it actually governs                                                                                                                                                                                                                      |
| -------------------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `go.set_gopath`            | `false`                        | **Deprecated.** True sets `GOPATH` to `installs/go/<ver>/packages`, inside the toolchain dir — discarded on every Go upgrade. Fires a runtime deprecation warning.                                                                            |
| `go.set_gobin`             | unset (tri-state)              | Only the **go toolchain's** exec env, never the `go:` backend. Unset sets `GOBIN` only when `GOBIN` is absent from the pre-activation env; `true` always sets it; `false` never does, so a hand-run `go install` falls back to `$GOPATH/bin`. |
| `go.set_goroot`            | `true`                         | Sets `GOROOT` to the active toolchain. Safe to leave on: the `go:` backend strips an inherited `GOROOT` before every install anyway.                                                                                                          |
| `go.skip_checksum`         | unset                          | Skips checksum verification on SDK tarball download.                                                                                                                                                                                          |
| `go.download_mirror`       | `https://dl.google.com/go`     | SDK tarball mirror.                                                                                                                                                                                                                           |
| `go.repo`                  | `https://github.com/golang/go` | Git source for `go`.                                                                                                                                                                                                                          |
| `go.default_packages_file` | `~/.default-go-packages`       | Deprecated; warn 2027.11.0, remove 2028.11.0. Use tool postinstall hooks or the `go:` backend.                                                                                                                                                |

`go.set_gopath`'s deprecation string is the authoritative guidance and worth quoting when someone reaches for
it:

> mise no longer manages GOPATH. Set GOPATH in [env] if you need a specific value.

## A documented contradiction to expect

Upstream describes the `GOBIN` forcing in two incompatible ways, and neither page says which code path it
means:

- `docs/dev-tools/backends/go.md` states it unconditionally: "mise still sets `GOBIN` to the tool install
  directory after applying `install_env`."
- `settings.toml` under `[go.set_gobin]` presents it as a toggle: "Set to `false` to not set GOBIN (default is
  `${GOPATH:-$HOME/go}/bin`)."

Both are locally true of **different** things. The backend doc describes the `go:` backend, where the forcing
is unconditional. The setting describes the `go` toolchain's exec env, where it is a toggle. Do not try to
reconcile them into one rule, and do not conclude from the settings page that `go.set_gobin = false` will
change where `go:` tools install — it will not.

A smaller one: `go.set_gopath`'s `description` field still documents live behavior while its `deprecated`
field on the same entry says mise no longer manages `GOPATH`. The setting is still wired and still works; it
is deprecated, not inert.

## Verification

Confirm that the selected Go toolchain is already installed before these checks. If installation is not
authorized, set `MISE_EXEC_AUTO_INSTALL=false` in the process environment and stop when Go is absent. Apply
the safe-mode gate from `SKILL.md` when project config is outside the user's trust boundary.

```bash
mise exec -- go env GOPATH GOMODCACHE GOBIN
```

To prove a redirect holds under the conditions that actually break, run it from a context with nothing
inherited:

```bash
env -i HOME="$HOME" PATH=/usr/bin:/bin mise exec -- go env GOPATH GOMODCACHE
```

## Footguns

- assuming a shell rc export of `GOPATH` covers installs — it only covers shells that source it
- reaching for `go.set_gopath` to relocate `GOPATH`; it is deprecated and points inside the toolchain dir
- putting `install_env` on the `go` toolchain entry expecting it to reach `go:` tools; it scopes to installing
  Go itself
- trying to redirect `GOBIN` for a `go:` tool by any mechanism
- reading a `$HOME/go` that merely still exists as proof the leak is ongoing; check mtimes before concluding
  anything
