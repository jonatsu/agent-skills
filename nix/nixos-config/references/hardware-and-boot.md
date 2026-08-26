# Hardware and Boot

Load when standing up a new host, or changing bootloader, disk layout, or hardware configuration.

## Generating hardware configuration

```bash
# During installation, with the target mounted at /mnt
nixos-generate-config --root /mnt

# On a running system, to refresh after a hardware change
nixos-generate-config --show-hardware-config > hosts/<host>/hardware-configuration.nix
```

The generated file is machine-specific: filesystem UUIDs, `boot.initrd.availableKernelModules`, CPU microcode, and swap devices. Keep it per-host and never share it between machines — two hosts with the same UUIDs is a boot failure waiting for the first disk swap.

`--show-hardware-config` writes only the hardware half, which is what you want when refreshing an existing host; the plain form also rewrites `configuration.nix`.

## Bootloader

**systemd-boot (UEFI, default choice):**

```nix
{
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;
  boot.loader.systemd-boot.configurationLimit = 10;
}
```

`configurationLimit` matters more than it looks: without it, every generation gets a boot entry and its kernel stays on the ESP. A 512 MB ESP fills after a few dozen generations and rebuilds then fail with a confusing "No space left on device" during bootloader installation.

`canTouchEfiVariables = false` is required when firmware handles EFI variables badly, or when installing from a live system whose EFI vars are not the target's.

**GRUB (BIOS/legacy, or multi-boot):**

```nix
{
  boot.loader.grub.enable = true;
  boot.loader.grub.device = "/dev/sda";      # BIOS: the disk, not a partition
  boot.loader.grub.useOSProber = true;       # detect other OSes
}
```

On UEFI with GRUB, set `boot.loader.grub.efiSupport = true` and `device = "nodev"` instead — passing a disk path on UEFI is a common mis-copy that installs nothing.

## Encrypted and layered disks

LUKS devices must be opened in initrd, keyed by UUID:

```nix
{
  boot.initrd.luks.devices."cryptroot".device =
    "/dev/disk/by-uuid/<uuid-of-the-LUKS-container>";
}
```

Use the UUID of the **encrypted container**, not of the filesystem inside it — `blkid` shows both, and picking the inner one yields an initrd that cannot find the device. LVM on LUKS needs no extra option; the volume group is discovered once the container opens.

For remote unlock, `boot.initrd.network.ssh` needs a host key present in initrd and `boot.initrd.availableKernelModules` containing the NIC driver, or the machine boots to an unreachable password prompt.

## Impermanence and tmpfs roots

If `/` is a tmpfs or is rolled back per boot, machine identity must be persisted explicitly: `/etc/machine-id`, `/var/lib/nixos` (uid/gid stability), and SSH host keys. Losing `/var/lib/nixos` silently renumbers users on the next rebuild, which changes file ownership across the system.

## Cross-architecture builds

Building an `aarch64-linux` configuration on `x86_64-linux` requires either a remote builder or binfmt emulation:

```nix
{ boot.binfmt.emulatedSystems = [ "aarch64-linux" ]; }
```

Emulated builds are roughly an order of magnitude slower; prefer a remote builder for anything larger than a config test.
