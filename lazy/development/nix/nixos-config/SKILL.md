---
name: nixos-config
description: "Configure and recover NixOS hosts. Use when adding or changing a host in a flake, generating hardware configuration, choosing a rebuild mode, setting stateVersion, diagnosing an ignored option or a failed system build, rolling back or recovering an unbootable system, or running a downloaded binary that NixOS cannot execute. User-level dotfiles and programs belong to home-manager."
license: MIT
metadata:
  author: Joonas Onatsu
---

# NixOS Config

NixOS modules own the system: put `services.*`, `boot.*`, `hardware.*`, `networking.*`, and `fileSystems.*` there.
Dotfiles, user packages, and `programs.*` user config belong to home-manager; set in the wrong module system, an
option fails evaluation or does nothing.

> **Using Denful (den)?** Entity declaration and aspect wiring belong to den rather than to this skill; look
> for a dendritic skill in the configuration repository itself. The option-level guidance below applies
> either way.

## System Mutation Boundary

`nixos-rebuild build` evaluates and builds without changing the running host. `dry-activate` shows what an
activation would do without activating it. `switch`, `test`, `boot`, `--rollback`, `nixos-install`, and garbage
collection change host state, activate services, change the boot default, or remove recovery material.

Before any state-changing command, identify the target host and action, explain its effect, and obtain the user's
explicit approval. Validate a change with `build` or `dry-activate` first. On a remote host, use `test` only
after approval and keep a recovery path available.

## Step 1: Wire the Host

```nix
# flake.nix
{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.home-manager = {
    url = "github:nix-community/home-manager";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, home-manager, ... }: {
    nixosConfigurations.host1 = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        ./hosts/host1/hardware-configuration.nix
        ./hosts/host1/configuration.nix
        home-manager.nixosModules.home-manager
      ];
    };
  };
}
```

`inputs.nixpkgs.follows` on home-manager is not optional in practice: two nixpkgs instances double evaluation
time and produce two distinct `pkgs` sets, which is a common source of "the same package built twice" and of
overlays appearing not to apply.

**In a git-backed flake, untracked files are invisible to evaluation.** A new module that is not `git add`-ed
does not exist as far as `nix` is concerned, and the error names the option, not the missing file. Rule this
out before debugging module logic.

## Step 2: Hardware Configuration

For a new host, generate the file on the target machine before the first build:

```bash
nixos-generate-config --root /mnt      # during install
nixos-generate-config --show-hardware-config > hardware-configuration.nix
```

Treat the generated file as a machine-specific, replaceable baseline: regenerate it after hardware changes and
compare the result. Keep deliberate hardware policy and overrides in a separate host module, so regeneration
leaves them intact. If a machine-specific correction must stay in the generated file, document it so regeneration
does not silently erase it.

Bootloader choice, LUKS/LVM/impermanence layouts, and cross-compilation notes:
[references/hardware-and-boot.md](references/hardware-and-boot.md).

## Step 3: Overlay and pkgs Scope

With `home-manager.useGlobalPkgs = true`, define overlays in a NixOS module. Home-manager then reuses the system
`pkgs`, so an overlay set in home-manager config is silently ignored.

```nix
# CORRECT when useGlobalPkgs = true — overlay at the NixOS level
{
  home-manager.useGlobalPkgs = true;
  home-manager.useUserPackages = true;
  nixpkgs.overlays = [ inputs.some-flake.overlays.default ];
}
```

The `home-manager` skill has the full overlay-scope table for both `useGlobalPkgs` settings and what
`useUserPackages` changes.

Put each package in one place: `environment.systemPackages` when it must exist before login or for system
services, `home.packages` otherwise. A package in both lands on `PATH` twice with ambiguous precedence.

## Step 4: stateVersion

```nix
{ system.stateVersion = "<release-at-first-install>"; }
```

Set it once, to the release used at the host's first installation, and keep it there through upgrades. It
selects migration behaviour for stateful services (databases, `/var` layouts), so raising it tells NixOS that
migrations already happened when they did not. home-manager has an independent `home.stateVersion` with the
same rule.

## Step 5: Build, Deploy, Verify

```bash
nixos-rebuild build        --flake .#host1   # build only; changes nothing
nixos-rebuild dry-activate --flake .#host1   # show what activation would restart
# The commands below change the host; each needs the user's approval
nixos-rebuild test         --flake .#host1   # activate without touching the boot menu
nixos-rebuild boot         --flake .#host1   # stage for next boot, do not activate now
nixos-rebuild switch       --flake .#host1   # activate and make the boot default
```

Use `test` or `boot` for a change that could break networking or display on a remote or headless host: the
previous generation stays the boot default, so a power cycle recovers the machine.

The step is done when the build succeeds and the activated host passes the post-deploy checks in
[references/operations.md](references/operations.md), which also covers deployment variants, remote deploys,
generation management, and rollback.

## References

Load a reference when its trigger fires; the body covers adding a service, a package, or an option to a working
host.

| Reference                                                 | Load when                                                                                                |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [hardware-and-boot.md](references/hardware-and-boot.md)   | Standing up a NEW host, or changing bootloader, disk layout, or hardware config                          |
| [operations.md](references/operations.md)                 | Deploying, rolling back, a failing build, an unbootable system, or a downloaded binary that will not run |
| `../home-manager/references/settings-trees-and-merges.md` | Writing or gating a nested `settings` tree that a generator renders to a file, in either module system   |

The last row lives in the companion `home-manager` skill and resolves only when both are deployed side by
side; if it is missing, its core is: nested attrsets in `settings`-style options shallow-merge per module —
they do not deep-merge, so a shared name is replaced wholesale. The same holds for `//` on any two config trees:
combine them with `lib.recursiveUpdate`, or `mkIf` when the value is an option.

## Verifying Options Exist

Verify option paths and package names before writing them; guessing an option path produces an
`attribute missing` error that reads as a syntax problem.

The `mcp-nixos` MCP server answers this directly (`uvx mcp-nixos`, or `nix run github:utensils/mcp-nixos`) —
search options, read option details, confirm package names, check binary cache coverage before committing to a
long build. Without it, `nix repl` with `:lf .` and tab completion on the resolved config is the fallback.
