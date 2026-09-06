# Installing and integrating nix-direnv

Source: nix-direnv README; home-manager `programs.direnv` module.

Requirements: bash ≥ 4.4, Nix ≥ 2.4, direnv ≥ 2.21.3. macOS ships bash 3.2 — install direnv itself via Nix or Homebrew
there, not the system bash.

## Install methods

| Method                         | Mechanism                                                                                                                           | Notes                                                                                                                                     |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **home-manager** (recommended) | `programs.direnv.enable = true; programs.direnv.nix-direnv.enable = true;`                                                          | Drops `~/.config/direnv/lib/hm-nix-direnv.sh`. Version tracks the nixpkgs pin — use `source_url` if you need an exact nix-direnv version. |
| NixOS module                   | `programs.direnv.enable`/`.nix-direnv.enable` (NixOS ≥ 23.05)                                                                       | System-wide. Its option surface (`silent`, `loadInNixShell`, `direnvrcExtra`) differs from the home-manager one.                          |
| `.envrc` `source_url`          | `source_url "…/nix-direnv/<tag>/direnvrc" "<sha256>"`                                                                               | Per-project pin; works even where no global nix-direnv is installed.                                                                      |
| `nix profile`                  | `nix profile install nixpkgs#nix-direnv`, then `source $HOME/.nix-profile/share/nix-direnv/direnvrc` in `~/.config/direnv/direnvrc` | Imperative, non-root.                                                                                                                     |

## home-manager options (`programs.direnv.*`)

| Option                                     | Purpose                                                                                                                          |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `enable` / `package`                       | Enable direnv / choose the package.                                                                                              |
| `nix-direnv.enable` / `nix-direnv.package` | The caching, GC-root-protecting `use_nix`/`use_flake`.                                                                           |
| `enable{Bash,Zsh,Fish,Nushell}Integration` | Shell hook. Gate each on the matching `programs.<shell>.enable` — the hook only works for a shell home-manager actually manages. |
| `config`                                   | Written to `direnv.toml` (i.e. the `[global]`/`[whitelist]` settings).                                                           |
| `stdlib`                                   | Custom stdlib written to `~/.config/direnv/direnvrc`.                                                                            |
| `silent`                                   | Disable direnv's per-cd load logging (declarative `DIRENV_LOG_FORMAT=`).                                                         |
| `mise.enable`                              | `use_mise` integration — a _different_ tool; do not enable alongside nix-direnv unless you intend both.                          |

Canonical home-manager snippet:

```nix
programs = {
  direnv = {
    enable = true;
    enableBashIntegration = true; # match the shell HM manages
    nix-direnv.enable = true;
    config.global.hide_env_diff = true; # tame Nix's large env diff
  };
  bash.enable = true;
};
```

Renamed/removed upstream options to know: `enableNixDirenvIntegration` → `nix-direnv.enable` (old name redirects);
`nix-direnv.enableFlakes` was removed — flake support is now always on.

## Keep GC roots effective — `keep-outputs` / `keep-derivations`

nix-direnv GC-roots the devShell and inputs, but the outputs/derivations they point at also need to survive GC. Set, on
the system (NixOS) or in `nix.conf`:

```nix
nix.settings = {
  keep-outputs = true;
  keep-derivations = true;
};
```

This is the correct companion to nix-direnv — set both together, and only where nix-direnv is actually active.

## Conflicts and caveats

- nix-direnv and Nixify both redefine `use_nix` — only one can be active. Lorri and Lorelei coexist alongside either.
- direnv does not work inside Nix FHS environments (`buildFHSEnv`) — a known upstream limitation.
- A specific behavior set is only guaranteed by pinning via `source_url` + sha256; each tag has its own hash (a mismatch
  fails the fetch).
