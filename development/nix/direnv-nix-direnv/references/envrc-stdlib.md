# `.envrc` stdlib — nix-direnv + direnv core

Functions and behaviors relevant to Nix devshells. Sources: nix-direnv `direnvrc` and README; direnv `direnv-stdlib(1)`.

## nix-direnv functions

| Call                                                      | Effect                                                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `use flake [installable] [args…]`                         | Cached `nix print-dev-env` for a flake devShell. GC-roots the shell derivation and every flake input under the layout dir. Extra args forward verbatim to `print-dev-env`. Default installable is `.` (current flake, default devShell for the system).                                                                                                                                          |
| `use nix [nixfile] [-p pkg…] [-A attr] [-I path] [args…]` | Same caching/GC-root treatment for a `shell.nix`/`default.nix` (or `-p` package list). Emulates `nix-shell`-style arg parsing for historical reasons: only a fixed allowlist of flags is understood (`-p`/`--packages`, `-I`/`--include`, `-A`/`--attr`, `-o`/`--option`, `--arg`, `--argstr`); `--command`, `--run`, `--pure`, `--keep`, `-i` are silently ignored. Sets `IN_NIX_SHELL=impure`. |
| `nix_direnv_version <min>`                                | Compares the loaded nix-direnv version against `<min>`; the standard `source_url` guard uses it to force a re-source when too old.                                                                                                                                                                                                                                                               |
| `nix_direnv_manual_reload`                                | Call _before_ `use flake`/`use nix`. Switches off auto-rebuild on staleness: nix-direnv warns that the cache is stale instead of rebuilding, and you reload explicitly with the `nix-direnv-reload` shell command.                                                                                                                                                                               |
| `nix_direnv_disallow_fallback`                            | Call _before_ `use flake`/`use nix`. Disables the default "serve the last-good devShell if the current one fails to evaluate" behavior — a broken `flake.lock` bump then hard-fails loudly instead of silently masking itself.                                                                                                                                                                   |
| `nix_direnv_watch_file …`                                 | **Deprecated** — it logs a warning and forwards to core `watch_file`. Use `watch_file` directly.                                                                                                                                                                                                                                                                                                 |

`nix-direnv-reload` is a shell command (not an `.envrc` function): it forces a cache rebuild. It's the companion to
`nix_direnv_manual_reload`.

### `use flake` argument forms

- `use flake` / `use flake .` — current flake, default devShell.
- `use flake .#myShell` — a named devShell output.
- `use flake ~/flakes#project` — an external flake by path + output.
- `use flake . --impure` / `use flake . --accept-flake-config` — flags forwarded to `nix print-dev-env`.
- A leading flag (`use flake --impure`) is rejected: the first arg must be the flake expression.

## Relevant direnv-core stdlib

| Call                                                | Effect                                                                                                                                                   |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `watch_file <path>…`                                | Add file(s) to the reload trigger list. MUST be called _before_ `use flake`/`use nix` to be picked up.                                                   |
| `watch_dir <dir>`                                   | Recursively watch a directory.                                                                                                                           |
| `PATH_add <path>` / `path_add <var> <path>`         | Prepend to `PATH` / an arbitrary path-like var without clobbering it.                                                                                    |
| `source_env <f>` / `source_up [f]` (+ `_if_exists`) | Load another `.envrc` by path / from a parent dir. **Not** checked by the trust framework — see `direnv-toml-and-trust.md`.                              |
| `dotenv [path]` (+ `_if_exists`)                    | Load a `.env` file.                                                                                                                                      |
| `env_vars_required <var>…`                          | Error for each missing/empty var — assert required secrets loaded.                                                                                       |
| `on_git_branch [name]`                              | True inside a git repo (optionally a branch); watches `.git/HEAD`.                                                                                       |
| `require_allowed <path>…`                           | _direnv ≥ 2.38.0._ Force re-`allow` if a listed file (e.g. a lockfile whose contents get executed) changes — closes the `source_env`/lockfile trust gap. |
| `strict_env` / `unstrict_env [cmd…]`                | Toggle `set -euo pipefail` strictness.                                                                                                                   |
| `direnv_version <min>`                              | Assert a minimum direnv version for a shared `.envrc`.                                                                                                   |
| `has <cmd>`                                         | True if a binary or shell function exists.                                                                                                               |
| `source_url <url> <hash>`                           | Fetch-verify-and-source a remote script via content-addressed storage — the mechanism behind nix-direnv's `source_url` install.                          |

Note: `layout` calls are unnecessary alongside `use nix`/`use flake` — Nix already provides the full language
environment.

## Auto-watched files (no `watch_file` needed)

- `use flake`: `~/.direnvrc`, `~/.config/direnv/direnvrc`, `.envrc`, `flake.nix`, `flake.lock`, and `devshell.toml` if
  present.
- `use nix`: the same direnvrc/`.envrc` set plus the resolved nix file (`shell.nix`/`default.nix`/explicit arg).

## Cache layout (`.direnv/`)

- `flake-profile-<hash>` — a `nix build --out-link` result (itself a GC root) pointing at the devShell env.
- `flake-profile-<hash>.rc` — the captured `nix print-dev-env` shell environment.
- `flake-inputs/<store-path>` — one GC-root symlink per flake input.
- `bin/nix-direnv-reload` — the generated force-reload command (added to PATH).
- Reload is mtime-based: any watched file newer than the `.rc` invalidates the cache. On a cache _hit_, nix-direnv
  `touch -h`es the GC-root symlinks so active environments don't look stale to external GC (e.g. `nh`).
- Relocate the cache by overriding `direnv_layout_dir` in `~/.config/direnv/direnvrc`.

## Environment variables

- `NIX_DIRENV_DID_FALLBACK` — set when a fallback to the last-good devShell occurred (useful for a prompt/status
  indicator).
- `NIX_DIRENV_FALLBACK_NIX` — path to a fallback `nix` binary when none is on PATH.
- `NIX_DIRENV_SKIP_VERSION_CHECK` — skip the bash/direnv minimum-version preflight.
