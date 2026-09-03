---
name: nixos-config
description: "Configure and recover NixOS hosts: flake host wiring, hardware modules, rebuild modes, stateVersion, boot, rollback, and nix-ld. Use when changing a host, diagnosing ignored options or failed builds, recovering boot, or enabling a downloaded binary."
license: MIT
metadata:
  author: Joonas Onatsu
---

# NixOS Config

IRON LAW: SYSTEM CONFIGURATION AND USER CONFIGURATION LIVE IN DIFFERENT MODULE SYSTEMS. `services.*`,
`boot.*`, `hardware.*`, `networking.*`, and `fileSystems.*` are NixOS modules. Dotfiles, user packages, and
`programs.*` user config belong to home-manager. Crossing that line produces evaluation failures and config
that silently does nothing.

> **Using Denful?** Entity declaration and aspect wiring live in the `dendritic-pattern` skill. The
> option-level guidance below applies either way.

## What this skill is for

NixOS option syntax is well known; the failures below are not. Reach for this when an option is set but has no
effect, when a rebuild or boot fails, or when standing up a host from scratch.

## System Mutation Boundary

`nixos-rebuild build` evaluates and builds without changing the running host. `dry-activate` shows what an
activation would do without activating it. `switch`, `test`, `boot`, `--rollback`, `nixos-install`, and garbage
collection change host state, activate services, change the boot default, or remove recovery material.

Before any state-changing command, identify the target host and action, explain its effect, and obtain the user's
explicit approval. Prefer `build` or `dry-activate` while validating a change. On a remote host, use `test` only
after approval and keep a recovery path available.

## Workflow

```text
NixOS Config Progress:

- [ ] Step 1: Wire the host ⚠️ REQUIRED
- [ ] Step 2: Hardware configuration ⛔ BLOCKING (new hosts)
- [ ] Step 3: Resolve overlay and pkgs scope
- [ ] Step 4: Set stateVersion once
- [ ] Step 5: Build, deploy, verify ⛔ BLOCKING
```

## Step 1: Wire the Host ⚠️ REQUIRED

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

## Step 2: Hardware Configuration ⛔ BLOCKING

Generate on the target machine:

```bash
nixos-generate-config --root /mnt      # during install
nixos-generate-config --show-hardware-config > hardware-configuration.nix
```

Treat the generated file as a machine-specific, replaceable baseline. Do not casually edit detected filesystem
UUIDs, mounts, or boot modules: regenerate after hardware changes and compare the result. Put deliberate
hardware policy or overrides in a separate host-specific module where possible. If a machine-specific correction
must stay in the generated file, document it so regeneration does not silently erase it.

Bootloader choice, LUKS/LVM/impermanence layouts, and cross-compilation notes:
[references/hardware-and-boot.md](references/hardware-and-boot.md).

## Step 3: Overlay and pkgs Scope

The most common silent failure in a NixOS + home-manager setup: **an overlay defined in home-manager config
does nothing when `useGlobalPkgs = true`.** No warning is emitted; the package simply resolves unoverlaid, or
is not found.

| `useGlobalPkgs` | Overlay defined in              | Effect                           |
| --------------- | ------------------------------- | -------------------------------- |
| `true`          | NixOS module `nixpkgs.overlays` | System AND home-manager packages |
| `true`          | home-manager `nixpkgs.overlays` | **Nothing — silently ignored**   |
| `false`         | home-manager `nixpkgs.overlays` | home-manager packages only       |
| `false`         | NixOS module `nixpkgs.overlays` | System packages only             |

```nix
# CORRECT when useGlobalPkgs = true — overlay at the NixOS level
{
  home-manager.useGlobalPkgs = true;
  home-manager.useUserPackages = true;
  nixpkgs.overlays = [ inputs.some-flake.overlays.default ];
}
```

`useUserPackages = true` installs user packages into the system profile rather than the user's own profile.
Set it when user packages must be visible to system services or to a display manager started before the user
session.

## Step 4: stateVersion

```nix
{ system.stateVersion = "<release-at-first-install>"; }
```

NEVER raise it to match a newer NixOS release. It selects migration behaviour for stateful services
(databases, `/var` layouts); changing it retroactively tells NixOS that migrations already happened when they
did not. Set it to the release used at the host's first installation. It is not a "current version" field.
home-manager has an independent `home.stateVersion` with the same rule.

## Step 5: Build, Deploy, Verify ⛔ BLOCKING

```bash
nixos-rebuild switch --flake .#host1
nixos-rebuild test  --flake .#host1    # activate without touching the boot menu
nixos-rebuild boot  --flake .#host1    # stage for next boot, do not activate now
```

Prefer `test` when a change could break networking or display on a remote or headless host — it leaves the
previous generation as the boot default, so a power cycle recovers the machine.

Deployment variants, remote deploys, generation management, and rollback:
[references/operations.md](references/operations.md).

## References

Load one ONLY when its trigger fires. **Do NOT load either to add a service, a package, or an option to a
working host** — the body covers that.

| Reference                                                                               | Load when                                                                                                |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [hardware-and-boot.md](references/hardware-and-boot.md)                                 | Standing up a NEW host, or changing bootloader, disk layout, or hardware config                          |
| [operations.md](references/operations.md)                                               | Deploying, rolling back, a failing build, an unbootable system, or a downloaded binary that will not run |
| [settings-trees-and-merges.md](../home-manager/references/settings-trees-and-merges.md) | Writing or gating a nested `settings` tree that a generator renders to a file, in either module system   |

## Anti-Patterns

- **Casually editing generated hardware facts** — regeneration can overwrite filesystem UUIDs, mounts, and boot
  modules. Keep deliberate overrides separately or document why they must remain in the generated file.
- **Bumping `stateVersion` on an existing host** — it is not a version marker; changing it skips migrations
  that never ran.
- **Overlays in home-manager config under `useGlobalPkgs = true`** — silently ignored. Define them in a NixOS
  module.
- **Letting home-manager pull its own nixpkgs** — without `inputs.nixpkgs.follows`, you get two `pkgs` sets,
  doubled builds, and overlays that appear not to apply.
- **Same package in `environment.systemPackages` and `home.packages`** — two copies on `PATH` with ambiguous
  precedence. Pick by whether it must exist before login.
- **`nixos-rebuild switch` on a remote host for a networking change** — use `test` or `boot`, so a reboot
  recovers the machine.
- **Adding a module without `git add` in a flake repo** — it is invisible to evaluation, and the error points
  at the option rather than the file.
- **`//` to combine two config trees** — `//` is a shallow merge in Nix generally: a shared name is replaced,
  not merged, so a gated `lib.optionalAttrs` at the outer level silently deletes sibling groups. Use
  `lib.recursiveUpdate`, or `mkIf` when the value is an option.

## Verifying Options Exist

Verify option paths and package names before writing them; guessing an option path produces an
`attribute missing` error that reads as a syntax problem.

The `mcp-nixos` MCP server answers this directly (`uvx mcp-nixos`, or `nix run github:utensils/mcp-nixos`) —
search options, read option details, confirm package names, check binary cache coverage before committing to a
long build. Without it, `nix repl` with `:lf .` and tab completion on the resolved config is the fallback.
