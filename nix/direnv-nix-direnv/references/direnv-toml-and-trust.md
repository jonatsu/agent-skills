# `direnv.toml` and the trust model

Source: `direnv.toml(1)`, `direnv(1)`. Config file: `$XDG_CONFIG_HOME/direnv/direnv.toml`
(`~/.config/direnv/direnv.toml`). direnv ≤ 2.21.0 used `config.toml` — rename to flag when reviewing an old setup.

## `[global]`

| Option                      | Semantics                                                                                                                                                                                                          |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `warn_timeout`              | Duration string (default `"5s"`) before warning that `.envrc` is slow. **Set `0` (or any ≤0) to disable** — reasonable for cold Nix evals that legitimately take seconds. Runtime override: `DIRENV_WARN_TIMEOUT`. |
| `hide_env_diff`             | _direnv ≥ 2.34.0._ `true` hides the +/- env diff printed on load. The direnv wiki recommends it **specifically for Nix**, which sets a large number of env vars on activation. Default `false`.                    |
| `load_dotenv`               | _direnv ≥ 2.31.0._ Also load `.env` on top of `.envrc` (`.envrc` wins on conflicts).                                                                                                                               |
| `strict_env`                | Load `.envrc` under `set -euo pipefail`. Docs note this "will be the default in the future."                                                                                                                       |
| `bash_path`                 | Hard-code the `bash` location — avoids failures when `PATH` is being mutated.                                                                                                                                      |
| `disable_stdin`             | Redirect stdin to `/dev/null` during `.envrc` eval — reduces attack surface.                                                                                                                                       |
| `log_format` / `log_filter` | _direnv ≥ 2.36.0._ Log output format / regexp filter; `log_format = "-"` disables normal logging (the TOML equivalent of `DIRENV_LOG_FORMAT=`).                                                                    |

## `[whitelist]` — pre-trust directory trees (use with care)

Marks paths as implicitly allowed, bypassing per-file `allow`/`deny` entirely. direnv's own docs warn: **anyone who can
write files to a whitelisted directory (including VCS collaborators) can execute arbitrary code on your machine.**

- `prefix = [ … ]` — any `.envrc` whose absolute path _starts with_ one of these strings is trusted, recursively.
  Broadest and most dangerous.
- `exact = [ … ]` — only an exact directory/`.envrc` path match is trusted; does not cascade to subdirectories.
  Materially safer than `prefix`.

## Trust model (`allow` / `deny` / `edit`)

- `direnv allow [path]` (aliases `permit`, `grant`) — authorize an `.envrc`/`.env`.
- `direnv deny [path]` (aliases `block`, `disallow`, `revoke`) — de-authorize. `revoke` is an alias, not a separate
  command.
- `direnv edit [path]` — open in `$EDITOR` and re-`allow` automatically if mtime changed.
- **Mechanism:** trust is a SHA-256 of the file's _path + content_, recorded under `$XDG_DATA_HOME/direnv/allow`. Any
  edit changes the hash, so the file is re-blocked until `direnv allow` is re-run. This is the "clone a repo, don't get
  pwned on `cd`" protection.

### Trust bypasses to watch in a review

- `source_env` / `source_up` and their `_if_exists` forms are **not** trust-checked — an allowed `.envrc` that sources
  an arbitrary file gives that file a free pass.
- `[whitelist] prefix`/`exact` — implicit trust of whole trees (see above).
- `require_allowed` (direnv ≥ 2.38.0) exists to _close_ a related gap: when an `.envrc` executes code derived from a
  lockfile (pixi, npm postinstall), listing that lockfile forces re-authorization when it changes.
