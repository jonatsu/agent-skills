---
name: direnv-nix-direnv
description: "Set up and debug direnv with nix-direnv for cached, garbage-collection-protected Nix development shells. Use when writing or fixing an .envrc with use flake or use nix, when a devshell will not load or re-evaluates on every cd, when caching or GC roots are not working, when configuring direnv.toml or direnv allow trust, or when installing nix-direnv through home-manager, NixOS, or nix profile."
license: MIT
metadata:
  author: Joonas Onatsu
---

# direnv + nix-direnv

Let nix-direnv's own `use_flake` and `use_nix` run, and pass options as arguments to them. An `.envrc` that defines
either function replaces nix-direnv's version with one that neither caches nor protects the shell's dependencies
from garbage collection, and the arguments on the `use flake` line are lost.

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

Each tag has its own sha256; take the hash for the exact tag you pin, or the fetch fails.

**Non-flake** (`shell.nix`/`default.nix`): `use nix`.

Then run `direnv allow`. `flake.nix`, `flake.lock`, `.envrc`, and the direnvrc files are auto-watched — no manual
`watch_file` needed for those.

## Adding options as arguments to `use flake`

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

Read the `.envrc` diff before each `direnv allow`: trust is granted per content version, so the review is the
control. Grant standing trust with an `exact` whitelist entry; a `prefix` entry over a shared or version-controlled
tree lets anyone who can write there run code on your `cd`.

## Install and integration

home-manager (`programs.direnv.nix-direnv.enable`), NixOS, `nix profile`, and the `keep-outputs`/`keep-derivations`
companion for GC roots: `references/install-and-integration.md`. GC protection holds only on a host where that module
or option is actually active.

## Diagnosing "won't load / won't cache / keeps rebuilding"

Work top-down; each step isolates a layer:

1. `ls .direnv/` — no `flake-profile-*` symlink + `.rc` file ⇒ nix-direnv isn't caching. Prime suspect: an `.envrc`
   that defines its own `use_flake`/`use_nix`, or a hand-rolled `eval "$(nix print-dev-env)"`.
2. Run `direnv reload` and read its output. nix-direnv logs `nix-direnv: Using cached dev shell` or
   `nix-direnv: Renewed cache`. When no `nix-direnv:` line appears at all, nix-direnv did not run, so the install
   or `source_url` is not taking effect. Diagnose from this log: `.envrc` runs in a subshell, so its functions, such
   as `use_flake` and `nix_direnv_version`, never exist in your interactive shell.
3. `command -v direnv` + `direnv status` — confirm _which_ direnv is on PATH and that its
   `Loaded RC path`/`warn_timeout` match the config you expect. A mismatch means a different direnv (or config) governs
   the shell than you think you configured.
4. Stale env after editing `flake.nix` under `nix_direnv_manual_reload` — that's by design; run the `nix-direnv-reload`
   shell command.

## Done

- [ ] `.envrc` calls `use flake` or `use nix` with any options as arguments, and defines neither function.
- [ ] After `direnv allow`, `.direnv/` contains a `flake-profile-*` symlink, its `.rc` sibling, and a populated
  `flake-inputs/`.
- [ ] Any `source_url` pin uses the sha256 that matches its exact tag.
- [ ] Trust granted via `direnv allow` or an `exact` whitelist entry.
