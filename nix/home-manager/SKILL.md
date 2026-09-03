---
name: home-manager
description: "Configure home-manager user environments: NixOS-module vs standalone mode, home.packages vs programs.*, dotfile management, overlay scope under useGlobalPkgs, osConfig access, home.stateVersion, and home-manager switch. Use when adding user packages or dotfiles, when a home-manager setting has no effect, when an overlay is ignored, when a setting evaluates fine but is missing from the generated config file, or when choosing between standalone and integrated home-manager. Triggers on: home-manager, home.nix, home.packages, programs.*, homeConfigurations, home-manager switch, useGlobalPkgs, useUserPackages, osConfig, mkOutOfStoreSymlink, xdg.configFile, home.stateVersion, standalone home-manager, programs.*.settings, configFile, plasma-manager, cosmic-manager, lib.optionalAttrs, lib.recursiveUpdate, freeform submodule, emptyValue, has no value defined."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Home Manager

IRON LAW: NEVER PUT SYSTEM-LEVEL CONFIGURATION (`services.*`, `hardware.*`, `boot.*`, `networking.*`,
`fileSystems.*`) IN HOME-MANAGER. Home-manager owns user space only. System configuration belongs to NixOS
modules; crossing the line yields evaluation failures or config that silently does nothing.

> **Using Denful (den)?** Entity declaration and aspect wiring belong to den rather than to this skill; look
> for a dendritic skill in the configuration repository itself. The option-level guidance below applies
> either way.

## What this skill is for

`programs.<name>.enable` syntax is well known; the failures below are not. Reach for this when a home-manager
setting appears to be ignored, when packages resolve to the wrong version, or when choosing a deployment mode.

## Step 1: Choose the Deployment Mode ⚠️ REQUIRED

| Mode             | Wiring                                                                            | Use when                                  |
| ---------------- | --------------------------------------------------------------------------------- | ----------------------------------------- |
| **NixOS module** | `home-manager.nixosModules.home-manager` in the host's `modules` list             | The target runs NixOS and you control it  |
| **Standalone**   | `home-manager.lib.homeManagerConfiguration` producing `homeConfigurations.<name>` | Non-NixOS Linux, macOS, or no root access |

```nix
# NixOS module mode — inside the host's NixOS configuration
{
  home-manager.useGlobalPkgs = true;
  home-manager.useUserPackages = true;
  home-manager.users.alice = import ./home/alice.nix;
}
```

```nix
# Standalone mode — in flake outputs
homeConfigurations."alice@host1" = home-manager.lib.homeManagerConfiguration {
  pkgs = nixpkgs.legacyPackages.x86_64-linux;
  modules = [ ./home/alice.nix ];
};
```

The two modes differ in more than plumbing: **standalone home-manager cannot set anything that requires
root**, including login shell registration in `/etc/shells`, system services, and font caches consumed by
display managers. A config that works integrated can silently under-deliver standalone.

## Step 2: `osConfig` Differs Between Modes

Home-manager exposes the host's NixOS configuration as `osConfig`, and sets
`_module.args.osConfig = lib.mkDefault null`. On a standalone home it is therefore **bound and `null`, not
absent** — a module taking `osConfig` still loads, and any attribute access on it fails.

```nix
# CORRECT — works in both modes
{ osConfig, ... }: {
  programs.foo.enable = osConfig != null && osConfig.services.foo.enable;
}

# WRONG — `osConfig ? services` is a type error on null, and omitting the
# argument does not make the module "standalone-safe"
```

Config that must work in both modes should not reach into `osConfig` at all; pass what it needs through a
module argument or an option instead.

## Step 3: Packages and Programs

| Question                                | Answer | Location                             |
| --------------------------------------- | ------ | ------------------------------------ |
| Needs root, or must exist before login? | yes    | `environment.systemPackages` (NixOS) |
| User-space tool?                        | yes    | `home.packages`                      |
| Does home-manager ship a module for it? | yes    | `programs.<name>.enable` — preferred |

Prefer `programs.<name>.enable` over a raw package: the module generates config files, wires shell
integration, and registers user services. Adding the raw package instead gives you the binary and none of
that, which is why `programs.direnv.enable` works and `home.packages = [ pkgs.direnv ]` appears to do nothing.

**NEVER put the same package in both `environment.systemPackages` and `home.packages`** — two copies land on
`PATH` with ambiguous precedence, and they can be different versions once an overlay applies to only one.

## Step 4: Overlay Scope

The most common silent failure: **an overlay defined in home-manager does nothing when
`useGlobalPkgs = true`.**

| `useGlobalPkgs` | Overlay defined in              | Effect                           |
| --------------- | ------------------------------- | -------------------------------- |
| `true`          | NixOS `nixpkgs.overlays`        | System AND home-manager packages |
| `true`          | home-manager `nixpkgs.overlays` | **Nothing — silently ignored**   |
| `false`         | home-manager `nixpkgs.overlays` | home-manager packages only       |
| `false`         | NixOS `nixpkgs.overlays`        | System packages only             |

`useGlobalPkgs = true` makes home-manager reuse the system `pkgs` wholesale, so its own nixpkgs settings —
overlays, `config.allowUnfree` — are never consulted. Keep it `true` unless users genuinely need different
package sets; the cost of `false` is a second nixpkgs evaluation and a second copy of every shared package.

`useUserPackages = true` installs user packages into the system profile instead of `~/.nix-profile`, which is
what makes them visible to services and display managers that start before the user session.

## Step 5: Dotfiles

For **hand-written** config you edit often (Neovim, Emacs, shell), a normal `source = ./path` copies into the
Nix store, so every tweak needs a rebuild. Symlink the live path instead:

```nix
{ config, ... }: {
  xdg.configFile."nvim".source =
    config.lib.file.mkOutOfStoreSymlink "${config.home.homeDirectory}/dotfiles/nvim";
}
```

MUST use ONLY for native config that Nix does not generate. For Nix-generated files (`programs.*` output,
templated config) the store copy IS the source of truth and a symlink breaks it. The linked file is no longer
reproducible — a deliberate trade for iteration speed.

## Step 6: stateVersion and Build

```nix
{ home.stateVersion = "25.11"; }   # release at FIRST home-manager use
```

Independent of `system.stateVersion`, same rule: it selects migration behaviour, not "current version". NEVER
bump it on an existing home.

```bash
# NixOS module mode
nixos-rebuild switch --flake .#host1

# Standalone
home-manager switch --flake .#alice@host1
```

Verify: no evaluation errors; no system-level options set in home-manager; no package duplicated with
`systemPackages`; overlays at the right level for the `useGlobalPkgs` setting; **and for anything a generator
renders, the generated file read back — not just a clean eval** (see references/settings-trees-and-merges.md).

## References

Load ONLY when the trigger fires. **Do NOT load it to add a package, a dotfile, or a plain
`programs.<name>.enable`** — the body covers those.

| Reference                                                               | Load when                                                                                                                                                                                   |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [settings-trees-and-merges.md](references/settings-trees-and-merges.md) | Writing a nested `settings`/`configFile` tree, gating part of one, using a third-party module's typed options, or a setting that evaluates correctly but is missing from the generated file |

## Anti-Patterns

- **System config in home-manager** — `services.*`, `boot.*`, `networking.*` belong to NixOS modules.
- **Overlays in home-manager under `useGlobalPkgs = true`** — silently ignored; define them at the NixOS
  level.
- **Attribute access on `osConfig` without a null guard** — standalone binds it to `null`, so it is a type
  error, not a missing argument.
- **Raw package where a `programs.*` module exists** — you get the binary without config generation, shell
  integration, or services.
- **Same package in `systemPackages` and `home.packages`** — ambiguous `PATH` precedence, potentially
  different versions.
- **Bumping `home.stateVersion`** — it is not a version marker; changing it skips migrations that never ran.
- **`mkOutOfStoreSymlink` for Nix-generated files** — the store copy is the source of truth; the symlink
  breaks regeneration.
- **Assuming a standalone home can do what an integrated one does** — anything needing root silently does not
  happen.
- **`//` to combine two settings trees** — `//` is a shallow merge in Nix generally: it replaces a shared name
  instead of merging it, silently dropping sibling groups. Gate at the deepest shared name, or use
  `lib.recursiveUpdate` / `mkIf`.
- **Setting one field of a `nullOr (submodule …)` group** — the parent flips non-null and every sibling with a
  non-null default gets written too, possibly contradicting the program's own default.
- **Trusting a freeform submodule's type check to catch a misspelled setting** —
  `freeformType = attrsOf anything` accepts unknown keys silently.
- **Treating a clean `nix eval` as proof a generated file is right** — eval proves the option is set, nothing
  about what was rendered.

## Verifying Options Exist

Verify home-manager option paths before writing them; they diverge from NixOS option names more often than
expected (`programs.git.userName`, not `users.users.<name>.name`).

The `mcp-nixos` MCP server searches home-manager options directly (`uvx mcp-nixos`, or
`nix run github:utensils/mcp-nixos`). Without it, the home-manager option search page or `nix repl` on the
resolved `homeConfigurations.<name>.config` is the fallback.
