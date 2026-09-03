# Operations: Deploy, Recover, Troubleshoot

Load when deploying, rolling back, diagnosing a failed build, recovering an unbootable system, or running a
downloaded binary.

## Activation Boundary

`nixos-rebuild build` evaluates and builds a configuration without changing the running host. `dry-activate`
shows the activation plan without activating it. `switch`, `test`, `boot`, rollback, installation, and garbage
collection change host state or recovery material. Before running one, name the target host and action, explain
its effect, and obtain the user's explicit approval.

## Rebuild modes

| Command                      | Activates now | Boot default | Use when                                                         |
| ---------------------------- | ------------- | ------------ | ---------------------------------------------------------------- |
| `nixos-rebuild switch`       | yes           | yes          | Local machine, low-risk change                                   |
| `nixos-rebuild test`         | yes           | **no**       | Remote or headless host; networking, display, or kernel changes  |
| `nixos-rebuild boot`         | no            | yes          | Kernel/firmware change to take effect on the next planned reboot |
| `nixos-rebuild dry-activate` | no            | no           | See what activation would restart before committing              |

`dry-activate` is the one worth remembering: it prints which services would restart, which is how you find out
that a small change bounces the database or the display manager.

## Remote deployment

```bash
nixos-rebuild switch --flake .#host1 \
  --target-host root@host1 --build-host localhost
```

`--target-host` applies remotely; `--build-host` decides where the build happens. Building locally and pushing
closures suits a slow remote; building on the target suits a slow uplink. Both need the flake to evaluate
locally, so untracked files still bite here.

## First install

```bash
nixos-install --flake /mnt/etc/nixos#host1
```

Run from the installer with the target mounted at `/mnt`. The flake path must be reachable from the installer
environment. Installation changes the target disk and boot configuration; confirm the target before running it.

## Generations and rollback

```bash
nixos-rebuild switch --rollback                                   # previous generation
nix-env --list-generations --profile /nix/var/nix/profiles/system # inspect
nix-collect-garbage --delete-older-than 30d                        # prune
```

Rollback swaps the system profile and re-activates; it does NOT revert stateful changes a service already made
to its data directory. A database that migrated its schema on the last switch stays migrated.

When the machine will not boot, pick an older generation from the boot menu — every generation kept by
`configurationLimit` is bootable. That is the real recovery path; rollback requires a booted system.

## Reading build failures

| Error                                                | Usual cause                                                                    | Next step                                                                       |
| ---------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| `infinite recursion encountered`                     | A module reads `config.x` while defining `x`, or two modules import each other | Find the cycle with `--show-trace`; break it with `lib.mkIf` or a `let` binding |
| `attribute 'foo' missing`                            | Option path does not exist (renamed or misspelled)                             | Verify the path before assuming a syntax error                                  |
| `The option 'x' is defined multiple times`           | Two modules set the same option without priority                               | `lib.mkForce`, `lib.mkDefault`, or merge the definitions deliberately           |
| `hash mismatch in fixed-output derivation`           | Upstream source changed under a pinned hash                                    | Update the hash, or pin the source properly                                     |
| `error: path ... does not exist` after adding a file | File is untracked in a git flake                                               | `git add` it                                                                    |

`--show-trace` is nearly mandatory for module-system errors; without it the message names a leaf option and
not the module that set it.

## Running non-Nix binaries

NixOS is not FHS-compliant, so a downloaded dynamically-linked binary fails with an interpreter or
shared-library error. Cheapest first:

1. **`nix-ld`** — a stub loader at the standard FHS path, so unpatched binaries find libraries. Best for dev
   machines where IDEs and language servers download their own tooling:

```nix
{
  programs.nix-ld.enable = true;
  programs.nix-ld.libraries = with pkgs; [ stdenv.cc.cc zlib openssl ];
}
```

2. **`steam-run`** — a one-off FHS sandbox: `nix-shell -p steam-run --run "steam-run ./binary"`.
3. **`nix-alien`** — resolves a specific binary's missing libraries automatically
   (<https://github.com/thiagokokada/nix-alien>).

These are runtime escape hatches. To package a binary reproducibly into the store, use the `nix-packaging`
skill's `autoPatchelfHook` flow instead.

## Post-deploy verification

```bash
systemctl --failed          # anything that did not come up
journalctl -b -p err        # errors from this boot only
nixos-version               # confirm the generation actually switched
```
