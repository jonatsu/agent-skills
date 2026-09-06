---
name: direnv-nix-direnv
description: "direnv + nix-direnv for Nix devshells: writing and debugging .envrc (use flake / use nix), nix-direnv's cached print-dev-env and GC-root pinning, direnv.toml options, the allow/deny content-hash trust model, and home-manager/NixOS/nix-profile install routes. Use when a devshell won't load or re-evaluates on every cd, when caching or GC-root protection isn't working, or when editing .envrc or direnv.toml. Triggers on: direnv, nix-direnv, .envrc, use flake, direnv allow, .direnv, gcroot, keep-outputs."
license: MIT
metadata:
  author: Joonas Onatsu
---

IRON LAW: NEVER redefine `use_flake` or `use_nix` inside an `.envrc`. Doing so shadows nix-direnv's
implementation and silently reverts to direnv's uncached, GC-unprotected form — the devshell re-evaluates on every load,
becomes garbage-collectable, and every argument on the `use flake`/`use nix` line is discarded. Let nix-direnv's own
function run; pass options as arguments to it.

# direnv + nix-direnv

nix-direnv is a drop-in replacement for direnv's built-in `use_nix`/`use_flake`. Its two jobs — and the only reasons to
use it over plain direnv — are:

1. **Cache** the `nix print-dev-env` output under `.direnv/`, so re-entering a directory is near-instant instead of
   re-evaluating the flake/shell.
2. **Pin** the resulting devShell derivation _and every flake input_ as GC roots, so `nix-collect-garbage` cannot delete
   a project's build dependencies.

If `.direnv/` is missing or the shell re-evaluates on every `cd`, one of those two is broken — start at the Diagnosing
section.

## Canonical `.envrc`

**Flake project** (nix-direnv installed via home-manager/NixOS — see `references/install-and-integration.md`):

```bash
use flake
```

**Flake project, self-bootstrapping** (portable to machines without a global nix-direnv; pin an exact tag + its sha256):

```bash
if ! has nix_direnv_version || ! nix_direnv_version 3.1.2; then
  source_url "https://raw.githubusercontent.com/nix-community/nix-direnv/3.1.2/direnvrc" "sha256-Di03ad3a0ueGi6CGrfhrQzyGdQIg9APXIPCAMNQgWYM="
fi
use flake
```

**Non-flake** (`shell.nix`/`default.nix`): `use nix`.

Then run `direnv allow`. `flake.nix`, `flake.lock`, `.envrc`, and the direnvrc files are auto-watched — no manual
`watch_file` needed for those.

## Adding options — pass them to `use flake`, never re-wrap it

Extra arguments after the flake expression forward to `nix print-dev-env`:

| Need                                             | Line                                |
| ------------------------------------------------ | ----------------------------------- |
| Select an output                                 | `use flake .#myShell`               |
| External flake                                   | `use flake ~/flakes#project`        |
| Auto-accept the flake's `nixConfig`              | `use flake . --accept-flake-config` |
| Impure eval (flake reads ambient env/paths)      | `use flake . --impure`              |
| Watch an extra input (call _before_ `use flake`) | `watch_file ./nix/foo.nix`          |

`--impure` is a reproducibility smell — add it only if the flake genuinely needs it. The first argument must be the
flake expression; a leading flag is an error.

Full stdlib (watch_file, nix_direnv_manual_reload, nix_direnv_disallow_fallback, nix-direnv-reload, auto-watched files,
use nix arg parsing): `references/envrc-stdlib.md`.

## Global config and trust

`direnv.toml` `[global]` options worth knowing — `warn_timeout` (set `0` to silence the slow-eval warning on cold Nix
builds), `hide_env_diff = true` (recommended for Nix, which emits a huge env diff), `load_dotenv`, `strict_env` — plus
the `allow`/`deny` content-hash trust model and the `[whitelist]` footguns: `references/direnv-toml-and-trust.md`.

## Install and integration

home-manager (`programs.direnv.nix-direnv.enable`), NixOS, `nix profile`, and the `keep-outputs`/`keep-derivations`
companion for GC roots: `references/install-and-integration.md`.

## Diagnosing "won't load / won't cache / keeps rebuilding"

Work top-down; each step isolates a layer:

1. `ls .direnv/` — no `flake-profile-*` symlink + `.rc` file ⇒ nix-direnv isn't caching. Prime suspect: a redefined
   `use_flake`/`use_nix` in `.envrc` (IRON LAW), or nix-direnv not loaded at all.
2. `type -t use_flake` in the dir — must resolve to a `function`. If it's nix-direnv's, editing `.envrc` won't have
   shadowed it.
3. `command -v direnv` + `direnv status` — confirm _which_ direnv is on PATH and that its
   `Loaded RC path`/`warn_timeout` match the config you expect. A mismatch means a different direnv (or config) governs
   the shell than you think you configured.
4. Re-evaluates every `cd`, no obvious override — check that nix-direnv actually loaded:
   `has nix_direnv_version && nix_direnv_version` should print a version. If absent, the install/`source_url` isn't
   taking effect.
5. Stale env after editing `flake.nix` under `nix_direnv_manual_reload` — that's by design; run the `nix-direnv-reload`
   shell command.

## Anti-patterns

- Redefining `use_flake`/`use_nix`, or hand-rolling `eval "$(nix print-dev-env)"` in `.envrc` — defeats caching _and_ GC
  roots (the whole point).
- Putting args on `use flake` while a custom `use_flake` ignores them.
- Reusing a `source_url` sha256 across nix-direnv versions — each tag has its own hash; a mismatch fails the fetch.
- Using `[whitelist] prefix` on a shared/VCS directory — anyone with write access to that tree gets arbitrary code
  execution on `cd`. Prefer `exact`, or plain `direnv allow`.
- `direnv allow`-ing reflexively without reading the `.envrc` diff — trust is per-content-version by design;
  rubber-stamping defeats it.
- Expecting `keep-outputs`/nix-direnv to protect a shell on a host where the option/module isn't actually active.

## Pre-delivery checklist

- [ ] `.envrc` does NOT define `use_flake`/`use_nix`.
- [ ] Options are passed as args to `use flake`, not baked into a wrapper.
- [ ] After `direnv allow`, `.direnv/` contains a `flake-profile-*` symlink, its `.rc` sibling, and a populated
  `flake-inputs/`.
- [ ] Any `source_url` pin uses the sha256 that matches its exact tag.
- [ ] Trust granted via `direnv allow`/`exact` whitelist, not a broad `prefix`.
