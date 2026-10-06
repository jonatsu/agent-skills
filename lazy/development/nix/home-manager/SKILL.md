---
name: home-manager
description: "Configure user environments with home-manager, as a NixOS module or standalone. Use when choosing between those modes, adding packages, programs, or dotfiles, when a setting has no effect or is missing from the generated config file, when home-manager ignores an overlay, when reading the host's NixOS config through osConfig, or when setting home.stateVersion. System services and boot belong to nixos-config."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Home Manager

Home-manager owns user space: packages, dotfiles, and `programs.*`. Put `services.*`, `boot.*`, `hardware.*`,
`networking.*`, and `fileSystems.*` in NixOS modules; set in home-manager, they fail evaluation or do nothing.

> **Using Denful (den)?** Entity declaration and aspect wiring belong to den rather than to this skill; look
> for a dendritic skill in the configuration repository itself. The option-level guidance below applies
> either way.

## Step 1: Choose the Deployment Mode

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
absent** — a module taking `osConfig` still loads. The hazard is **plain attribute selection**:
`osConfig.services` throws `expected a set but found null`. The `?` and `or` forms are null-tolerant along
their whole attrpath — `osConfig ? services` is `false`, and `osConfig.services.foo.enable or false` yields
the default even with `osConfig` null at the first step — but only for the single attrpath the `or` is
attached to: a split selection (`(osConfig.services).foo or false`) and `builtins.hasAttr "x" osConfig` both
still throw on null.

```nix
# CORRECT — works in both modes; the explicit null check reads clearest
{ osConfig, ... }: {
  programs.foo.enable = osConfig != null && osConfig.services.foo.enable;
}
# `osConfig.services.foo.enable or false` is equivalent when null-or-missing
# should mean false

# WRONG — plain selection throws standalone, and omitting the `osConfig`
# argument does not make the module "standalone-safe"
{ osConfig, ... }: {
  programs.foo.enable = osConfig.services.foo.enable;
}
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

Put each package in exactly one of `environment.systemPackages` and `home.packages`. A package in both lands on
`PATH` twice with ambiguous precedence, and the copies can differ in version once an overlay applies to only one.

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

Use `mkOutOfStoreSymlink` for hand-written config that Nix does not generate. For Nix-generated files
(`programs.*` output, templated config) the store copy is the source of truth, and a symlink breaks
regeneration. The linked file is no longer reproducible — a deliberate trade for iteration speed.

## Step 6: stateVersion and Build

```nix
{ home.stateVersion = "25.11"; }   # release at FIRST home-manager use
```

Independent of `system.stateVersion`, same rule: it selects migration behaviour, not "current version". Set it
once, at the first home-manager use, and keep it there; raising it skips migrations that never ran.

```bash
# NixOS module mode
nixos-rebuild switch --flake .#host1

# Standalone
home-manager switch --flake .#alice@host1
```

Verify: no evaluation errors; no system-level options set in home-manager; no package duplicated with
`systemPackages`; overlays at the right level for the `useGlobalPkgs` setting; **and for anything a generator
renders, the generated file read back — not just a clean eval** (see references/settings-trees-and-merges.md).

## Settings Trees and Generated Files

Load [settings-trees-and-merges.md](references/settings-trees-and-merges.md) when writing a nested
`settings`/`configFile` tree, gating part of one, using a third-party module's typed options, or chasing a setting
that evaluates correctly but is missing from the generated file. A package, a dotfile, or a plain
`programs.<name>.enable` needs only the body. Its traps, in brief:

- **`//` combines two settings trees shallowly** — it replaces a shared name instead of merging it, silently
  dropping sibling groups. Gate at the deepest shared name, or use `lib.recursiveUpdate` / `mkIf`.
- **Setting one field of a `nullOr (submodule …)` group** flips the parent non-null, and every sibling with a
  non-null default gets written too, possibly contradicting the program's own default.
- **A freeform submodule's type check accepts misspelled settings** — `freeformType = attrsOf anything` takes
  unknown keys silently.
- **A clean `nix eval` proves only that the option is set**, nothing about what was rendered.

## Verifying Options Exist

Verify home-manager option paths before writing them; they diverge from NixOS option names more often than
expected (`programs.git.userName`, not `users.users.<name>.name`).

The `mcp-nixos` MCP server searches home-manager options directly (`uvx mcp-nixos`, or
`nix run github:utensils/mcp-nixos`). Without it, the home-manager option search page or `nix repl` on the
resolved `homeConfigurations.<name>.config` is the fallback.

MCP and API indexes for home-manager options are often empty or stale; an empty lookup does NOT mean the
option is absent. Fall back to an options index site (e.g. searchix.ovh), and cross-check the hit against the
home-manager source at the revision the user's flake pins — options move between releases.
