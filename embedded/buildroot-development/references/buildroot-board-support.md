# Buildroot Board Support

Board directory layout, defconfig structure, rootfs overlays, post-build and post-image scripts, build-provenance
logging, `genimage` partition layout, device/permission tables, init-system choice, and kernel-config persistence.

For `BR2_EXTERNAL` mechanics, external toolchains, SDK, and legal-info, see `buildroot-advanced.md`. For a Kconfig
symbol that will not appear, see `kconfig-troubleshooting.md`.

## Contents

- [Board Directory Layout](#board-directory-layout)
- [Defconfig Structure](#defconfig-structure)
- [Rootfs Overlay](#rootfs-overlay)
- [Post-Build Script](#post-build-script)
- [Build-Provenance Logging](#build-provenance-logging)
- [Post-Image Script](#post-image-script)
- [genimage Partition Layout](#genimage-partition-layout)
- [Device / Permission Tables](#device--permission-tables)
- [Init System Selection](#init-system-selection)
- [Kernel Config Persistence](#kernel-config-persistence)
- [U-Boot Config (see u-boot-development)](#u-boot-config-see-u-boot-development)

## Board Directory Layout

A workable structure for board files inside a `BR2_EXTERNAL` tree (or directly in the Buildroot tree for upstream board
support):

```
board/<company>/<board>/
├── <board>_defconfig           → referenced from configs/
├── linux.config                → kernel defconfig (full or fragment)
├── busybox.config              → BusyBox config
├── genimage-<board>.cfg         → partition/image layout for genimage
├── rootfs-overlay/             → merged over $(TARGET_DIR) after pkg install
│   ├── etc/
│   │   └── network/interfaces
│   └── usr/
│       └── share/
├── post-build.sh               → runs before filesystem image creation
└── post-image.sh               → runs after all filesystem images created
```

The user-visible entry point is `configs/<board>_defconfig`. It points at the board's kernel config, overlays, and
scripts through non-default `BR2_*` values.

## Defconfig Structure

A minimal board defconfig that references board-specific files:

```
BR2_arm=y
BR2_cortex_a9=y
BR2_ARM_FPU_NEON=y

BR2_TOOLCHAIN_BUILDROOT_GLIBC=y
BR2_TOOLCHAIN_BUILDROOT_CXX=y

BR2_LINUX_KERNEL=y
BR2_LINUX_KERNEL_CUSTOM_VERSION=y
BR2_LINUX_KERNEL_CUSTOM_VERSION_VALUE="6.6.30"
BR2_LINUX_KERNEL_USE_CUSTOM_CONFIG=y
BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE="board/mycompany/myboard/linux.config"

BR2_TARGET_UBOOT=y
BR2_TARGET_UBOOT_CUSTOM_VERSION=y
BR2_TARGET_UBOOT_CUSTOM_VERSION_VALUE="2024.04"
BR2_TARGET_UBOOT_BOARD_DEFCONFIG="myboard"
BR2_TARGET_UBOOT_NEEDS_DTC=y

BR2_ROOTFS_OVERLAY="board/mycompany/myboard/rootfs-overlay"
BR2_ROOTFS_POST_BUILD_SCRIPT="board/mycompany/myboard/post-build.sh"
BR2_ROOTFS_POST_IMAGE_SCRIPT="support/scripts/genimage.sh"
BR2_ROOTFS_POST_SCRIPT_ARGS="-c board/mycompany/myboard/genimage-myboard.cfg"
```

This defconfig is the persistable artifact — regenerate it with `make savedefconfig` after any `menuconfig` change, per
the Iron Law.

## Rootfs Overlay

The overlay is copied verbatim over `$(TARGET_DIR)` after every package is installed, just before image creation.

```
board/myboard/rootfs-overlay/
├── etc/
│   ├── hostname                        → sets hostname
│   ├── network/interfaces              → static IP or DHCP
│   ├── inittab                         → BusyBox init config (BusyBox init only)
│   └── systemd/system/
│       └── myapp.service               → custom systemd unit
└── usr/
    └── share/
        └── myapp/
            └── default.conf
```

Rules that bite people:

- Overlay paths MUST mirror the exact absolute target path. `overlay/etc/foo` lands at `/etc/foo`; a missing leading
  path segment copies the file to the wrong place with no error.
- Overlay files OVERWRITE files a package installed — handy for replacing a default config, but it silently masks
  package updates to that file.
- The overlay directory itself is never copied — only its contents are.
- `BR2_ROOTFS_OVERLAY` takes a space-separated list of paths.

## Post-Build Script

Runs after every package installs into `$(TARGET_DIR)` but BEFORE the filesystem image is built. Use it to strip files
you do not ship, generate config from a template, or patch installed files.

```bash
#!/bin/bash
# board/myboard/post-build.sh
set -euo pipefail

TARGET_DIR="$1"

# Drop locale data you do not need
rm -rf "${TARGET_DIR}/usr/share/locale"
```

Make it executable (`chmod +x`). Extra tokens in `BR2_ROOTFS_POST_SCRIPT_ARGS` are appended after `$(TARGET_DIR)` when
the script runs.

## Build-Provenance Logging

Stamp a provenance record into the image from the post-build script so a fielded device can tell you exactly what
produced its rootfs. Capture the defconfig, the Buildroot revision (with a dirty flag), the toolchain, the kernel
version, and hashes of the key output artifacts.

```bash
#!/usr/bin/env bash
# board/myboard/post-build.sh — provenance block
set -Eeuo pipefail

TARGET_DIR="${1:?target dir}"
INFO="${TARGET_DIR}/etc/build-info"

# Resolve the git checkout that holds your board/config files WITHOUT assuming how
# deep this script sits under it. Prefer an explicit BR2_ROOT override; otherwise ask
# git for the enclosing repo's top level from the script's own location (depth-agnostic).
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
src_root="${BR2_ROOT:-$(git -C "$script_dir" rev-parse --show-toplevel 2>/dev/null || true)}"
if [[ -n "$src_root" ]]; then
    source_rev="$(git -C "$src_root" describe --always --dirty 2>/dev/null || echo unknown)"
else
    source_rev=unknown
fi

{
    printf 'build_date=%s\n'      "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'defconfig=%s\n'       "${BR2_DEFCONFIG:-unknown}"
    printf 'buildroot_version=%s\n' "${BR2_VERSION:-unknown}"  # Buildroot's own release
    printf 'source_rev=%s\n'      "$source_rev"                # your board/config tree
    printf 'kernel_version=%s\n'  "${BR2_LINUX_KERNEL_CUSTOM_VERSION_VALUE:-unknown}"
    printf 'toolchain=%s\n'       "${BR2_TOOLCHAIN_EXTERNAL_PREFIX:-buildroot-internal}"
} > "$INFO"
```

Hash the flashable outputs in the post-IMAGE script instead (the images do not exist yet at post-build time); write the
digests next to the images so a release can be verified byte-for-byte:

```bash
# in post-image.sh, after images exist
( cd "${BINARIES_DIR}" && sha256sum ./*.img ./*.dtb zImage 2>/dev/null ) \
    > "${BINARIES_DIR}/build-manifest.sha256"
```

Keep the record honest: a dirty `git describe`, an unknown defconfig, or a missing hash MUST show up in the file rather
than being papered over.

## Post-Image Script

Runs AFTER every filesystem image (ext4, squashfs, cpio, ...) is built. Use it to assemble images into one flashable
artifact, call `genimage` for a partitioned disk image, or sign and checksum for OTA.

```bash
#!/bin/bash
# Typical pattern: hand off to Buildroot's genimage helper
set -euo pipefail

BOARD_DIR="$(realpath "$(dirname "$0")")"
GENIMAGE_CFG="${BOARD_DIR}/genimage-myboard.cfg"

support/scripts/genimage.sh -c "${GENIMAGE_CFG}"
```

The `support/scripts/genimage.sh` helper stages a temporary root, points `genimage` at `BINARIES_DIR` for its inputs,
and needs `genimage` on the host (the `host-genimage` package). Its path can move between releases — check the tree
rather than assuming it.

## genimage Partition Layout

`genimage` builds a block-device image with a partition table, one or more filesystems, and raw regions. Its config
syntax is a genimage concern, not a Buildroot one.

```
# board/myboard/genimage-myboard.cfg

image boot.vfat {
    vfat {
        files = {
            "zImage",
            "myboard.dtb",
            "extlinux/extlinux.conf"
        }
    }
    size = 64M
}

image rootfs.ext4 {
    ext4 {
        mountpoint = "/"
    }
}

image myboard-sdcard.img {
    hdimage {
        partition-table-type = "dos"
    }
    partition u-boot {
        in-partition-table = "no"
        image = "u-boot-with-spl.bin"
        offset = 8K
    }
    partition boot {
        partition-type = 0xC    # FAT32
        bootable = true
        image = "boot.vfat"
        size = 64M
    }
    partition root {
        partition-type = 0x83   # Linux
        image = "rootfs.ext4"
    }
}
```

Enable `host-genimage` from the config or your `BR2_EXTERNAL` `Config.in`:

```
select BR2_PACKAGE_HOST_GENIMAGE
```

## Device / Permission Tables

Permission/device tables set ownership and mode on target files and create static device nodes:

```bash
# Default table (always applied)
BR2_ROOTFS_DEVICE_TABLE="system/device_table.txt"

# Append extra entries (space-separated)
BR2_ROOTFS_DEVICE_TABLE="system/device_table.txt board/myboard/device_table.txt"

# Static /dev nodes (only when not using devtmpfs/mdev/udev)
BR2_ROOTFS_STATIC_DEVICE_TABLE="system/device_table_dev.txt"
```

Whitespace-delimited format:

```
# path        type  mode  uid  gid  major  minor  start  inc  count
/dev/ttyUSB0  c     660   0    20   188    0      -      -    -
/var/log      d     755   0    0    -      -      -      -    -
```

Types: `f` file, `d` directory, `c` char device, `b` block device, `p` FIFO.

## Init System Selection

Set the init system in Buildroot's system configuration:

| Init system  | Option                       | Notes                                              |
| ------------ | ---------------------------- | -------------------------------------------------- |
| BusyBox init | `BR2_INIT_BUSYBOX` (default) | `/etc/inittab`, minimal, no dep tracking           |
| systemd      | `BR2_INIT_SYSTEMD`           | Full features, larger, glibc only                  |
| OpenRC       | `BR2_INIT_OPENRC`            | Dependency-aware, lighter than systemd             |
| sysvinit     | `BR2_INIT_SYSV`              | Classic SysV, `/etc/init.d/` scripts               |
| None         | `BR2_INIT_NONE`              | Custom init; also set `BR2_ROOTFS_SKELETON_CUSTOM` |

The skeleton package (`BR2_ROOTFS_SKELETON_DEFAULT` or a custom one) lays down the initial rootfs structure. It is
copied at the very start of the build, so any skeleton change forces a FULL rebuild — prefer overlays or the post-build
script for file-level tweaks.

## Kernel Config Persistence

```bash
# menuconfig against the kernel (edits the build-tree .config only)
make linux-menuconfig

# Write the full kernel config back to BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE
make linux-update-config

# Write a minimal kernel defconfig back
make linux-update-defconfig
```

Config fragments layer on top of the base kernel config:

```
BR2_LINUX_KERNEL_CONFIG_FRAGMENT_FILES="board/myboard/linux-extra.config"
```

`linux-menuconfig` touches only the build-tree `.config`. Those edits vanish on the next clean unless you run
`linux-update-config` or `linux-update-defconfig` to persist them to the board's config file — the kernel-side of the
Iron Law.

## U-Boot Config (see u-boot-development)

Buildroot only SELECTS the U-Boot version and board defconfig, through `BR2_TARGET_UBOOT_*` (see the defconfig above).
For U-Boot menuconfig, `extlinux.conf`, boot flow, environment, FIT images, and porting — and their safety contract —
use the **u-boot-development** skill. Do NOT drive U-Boot configuration from here.
