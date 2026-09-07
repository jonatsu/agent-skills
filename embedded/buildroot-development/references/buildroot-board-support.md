# Buildroot Board Support

Persist board inputs, customize the target filesystem, and verify assembled images. Resolve the source and output
context described in `SKILL.md` before using paths below. Examples show a project-owned board layout, not a supported
hardware definition. Select kernel, bootloader, and image formats for the actual board.

## Project Files and Configuration

Keep the board entry point in `configs/<board>_defconfig`. Group its kernel configuration, overlays, post-build hooks,
and image layout under `board/<company>/<board>/`. In an external tree, reference these files through the named
`BR2_EXTERNAL_<NAME>_PATH` instead of assuming they are inside Buildroot's source tree.

For example, these selections connect an ext4 rootfs and a genimage layout in an external tree named `MYPROJECT`:

```text
BR2_ROOTFS_OVERLAY="$(BR2_EXTERNAL_MYPROJECT_PATH)/board/myboard/rootfs-overlay"
BR2_ROOTFS_POST_BUILD_SCRIPT="$(BR2_EXTERNAL_MYPROJECT_PATH)/board/myboard/post-build.sh"
BR2_ROOTFS_POST_IMAGE_SCRIPT="support/scripts/genimage.sh"
BR2_ROOTFS_POST_IMAGE_SCRIPT_ARGS="-c $(BR2_EXTERNAL_MYPROJECT_PATH)/board/myboard/genimage.cfg"
BR2_TARGET_ROOTFS_EXT2=y
BR2_TARGET_ROOTFS_EXT2_4=y
BR2_PACKAGE_HOST_GENIMAGE=y
BR2_PACKAGE_HOST_DOSFSTOOLS=y
BR2_PACKAGE_HOST_MTOOLS=y
```

This is a configuration fragment: architecture, toolchain, kernel, bootloader, and required filesystem capacity still
come from the board's configuration. Use the selected release's symbols, load the configuration, and save it to the
explicit project defconfig path. Confirm the resulting paths and values before building.

## Rootfs Overlays and Artifact Ownership

Overlay contents are copied over the target tree after package installation. `overlay/etc/foo` becomes `/etc/foo`;
the overlay directory itself does not become a path component. Multiple overlays are space-separated. Buildroot excludes
some bookkeeping files; see its [overlay documentation](https://github.com/buildroot/buildroot/blob/2026.08/docs/manual/customize-rootfs.adoc).

Overlays intentionally replace package-installed files. Inspect binary, library, and module-metadata collisions as well
as configuration files: an overlay containing `modules.order` can replace the package-generated metadata.
Verify that the boot/deploy command selects the image just assembled and that packaged modules match its kernel.
Runtime driver and module-load diagnosis belongs to `embedded-linux-bringup`.

Respect the target's merged-directory configuration: for merged `/usr`, place overlay programs and libraries under
`/usr` rather than creating competing `/bin`, `/sbin`, or `/lib` directories. Check the release's additional merged-bin
rules when enabled. Use overlays or hooks for file-level customization; skeleton changes require a fresh/full build.

## Post-Build Script

Buildroot invokes post-build hooks with the target directory as their first argument, before filesystem creation.
Use `BR2_ROOTFS_POST_BUILD_SCRIPT_ARGS` for hook-specific arguments; `BR2_ROOTFS_POST_SCRIPT_ARGS` is shared with other
hook stages. Make scripts executable and use the documented hook environment rather than guessed exported config values.

This example removes only the locale subtree when that removal is a deliberate product choice. It requires Buildroot's
`BASE_DIR` and `BR2_CONFIG`, verifies the target belongs to that output, and rejects redirected paths. Run as the normal
build user in a trusted, non-concurrently-mutated output tree; it is not a privileged filesystem-cleaning service.

```bash
#!/usr/bin/env bash
set -euo pipefail

fail() { printf '%s\n' "$*" >&2; exit 1; }
[[ -n ${1:-} && -n ${BASE_DIR:-} && -f ${BR2_CONFIG:-} ]] || fail 'Expected Buildroot target and context'
base_dir=$(realpath -e -- "$BASE_DIR")
target_dir=$(realpath -e -- "$1")
[[ "$base_dir" != / && "$target_dir" == "$base_dir/target" && ! -L "$base_dir/target" ]] ||
  fail "Unexpected target directory: $1"
[[ -d "$target_dir" ]] || fail "Not a target directory: $target_dir"
locale_dir=$(realpath -m -- "$target_dir/usr/share/locale")
[[ "$locale_dir" == "$target_dir/usr/share/locale" && ! -L "$locale_dir" ]] ||
  fail "Redirected locale path: $locale_dir"
rm -rf -- "$locale_dir"
```

## Build Provenance

Prepare provenance in the build orchestration, where the source and configuration contexts are known, and pass the
record or explicit values to the post-build hook. Do not assume `BR2_DEFCONFIG`, kernel configuration values, or the
external-toolchain prefix are exported to hooks. Query effective values before generating the record:

```bash
make -s printvars VARS='BR2_VERSION BR2_DEFCONFIG BR2_TOOLCHAIN_EXTERNAL BR2_TOOLCHAIN_BUILDROOT TOOLCHAIN_EXTERNAL_PREFIX LINUX_VERSION'
```

Record the actual defconfig and its revision, Buildroot source revision, external-tree revisions, selected toolchain,
and kernel identity. Ask Git for each known repository's revision and dirty state; do not derive a repository by counting
parent directories or assume the board repository is the Buildroot repository. For tarball inputs, retain their release
and content hash. Missing evidence is `unknown`, never a guessed `buildroot-internal` value.

Keep any in-image record deterministic. Omit wall-clock build time or derive it from the build's fixed
`SOURCE_DATE_EPOCH`. Put volatile execution timestamps in the external build log. When copying a prepared record into
the target, validate the destination as in the post-build example and reject redirected output paths.

Hash flashable artifacts only after image assembly succeeds. Use the board's explicit artifact list; avoid globs that
silently omit a required file. This example publishes a manifest atomically, or fails while preserving the old manifest:

```bash
#!/usr/bin/env bash
set -euo pipefail

images_dir=$(realpath -e -- "${BINARIES_DIR:?missing images directory}")
[[ "$images_dir" != / ]] || { printf 'Refusing root as images directory\n' >&2; exit 1; }
cd -- "$images_dir"
# Example board artifacts; replace this list with the board's expected outputs.
artifacts=(myboard-sdcard.img rootfs.ext4 zImage myboard.dtb)
for artifact in "${artifacts[@]}"; do
  [[ -f "$artifact" && ! -L "$artifact" ]] || {
    printf 'Missing or redirected artifact: %s\n' "$artifact" >&2
    exit 1
  }
done
manifest_tmp=$(mktemp "$images_dir/.build-manifest.XXXXXX")
trap 'rm -f -- "$manifest_tmp"' EXIT
sha256sum -- "${artifacts[@]}" >"$manifest_tmp"
chmod 0644 -- "$manifest_tmp"
mv -fT -- "$manifest_tmp" "$images_dir/build-manifest.sha256"
```

## Post-Image Assembly with genimage

Post-image hooks receive the images directory as their first argument and run from the Buildroot source directory.
The configuration above invokes `support/scripts/genimage.sh` directly. Its implementation in 2026.08 supplies an
empty root directory and assembles prebuilt filesystem images; do not ask that helper to construct the rootfs from
`TARGET_DIR`. Verify the helper's contract when using another release.

For a direct invocation of genimage, `--rootpath` is instead your responsibility. These entry points are not
interchangeable. See the [Buildroot helper](https://github.com/buildroot/buildroot/blob/2026.08/support/scripts/genimage.sh)
and [genimage's documentation](https://github.com/pengutronix/genimage/blob/v20/README.rst).

The following hypothetical board layout expects `rootfs.ext4` to have already been generated by Buildroot. The kernel,
DTB, and extlinux configuration must already exist in `BINARIES_DIR`. The extlinux file must name paths and a root
partition appropriate to this board. This example does not install a board-specific bootloader.

```text
image boot.vfat {
    vfat {
        files = {
            "zImage",
            "myboard.dtb"
        }
        file extlinux/extlinux.conf {
            image = "extlinux/extlinux.conf"
        }
    }
    size = 64M
}

image myboard-sdcard.img {
    hdimage {
        partition-table-type = "dos"
    }
    partition boot {
        partition-type = 0xC
        bootable = true
        offset = 1M
        image = "boot.vfat"
    }
    partition root {
        partition-type = 0x83
        image = "rootfs.ext4"
    }
}
```

Inspect the partition table and verify expected files inside the assembled image. A successful genimage invocation
proves assembly, not that the board boots. Keep bootloader placement, offsets, and bootability tied to board evidence.

## Image Capacity Failures

When image creation runs out of space, identify whether the failure is in filesystem creation or partition assembly.
For ext2/3/4, inspect `BR2_TARGET_ROOTFS_EXT2_SIZE` and the failing tool's output; distinguish space from inode or host-disk
exhaustion. Separately compare the filesystem image's logical size with its genimage partition allocation.
A larger partition does not enlarge the filesystem inside it. Correct the relevant limits, regenerate affected images,
and verify the resulting layout. Do not select a different filesystem or wipe the build merely to bypass the symptom.

## Device and Permission Tables

Use `BR2_ROOTFS_DEVICE_TABLE` for a space-separated list of tables defining target modes and ownership; include the
project's required base table. Static device nodes use `BR2_ROOTFS_STATIC_DEVICE_TABLE` when static `/dev` is selected.
Do not use host ownership changes as a substitute for the image-generation metadata.

```text
# path        type  mode  uid  gid  major  minor  start  inc  count
/dev/ttyUSB0  c     660   0    20   188    0      -      -    -
/var/log      d     755   0    0    -      -      -      -    -
```

Consult the release's makedev syntax documentation for supported types and fields. This example's group ID must match
the target's account configuration.

## Init System Selection

Choose the init system in the board's system configuration and satisfy its release-specific toolchain constraints.
`BR2_INIT_BUSYBOX`, `BR2_INIT_SYSTEMD`, `BR2_INIT_OPENRC`, `BR2_INIT_SYSV`, and `BR2_INIT_NONE` are alternatives, not
simultaneous settings. Inspect `system/Config.in`; avoid copying a stale matrix of supported libc combinations.
A custom init and a custom filesystem skeleton are independent choices.

## Kernel Config Persistence

Inspect `BR2_LINUX_KERNEL_USE_CUSTOM_CONFIG`, `BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE`,
`BR2_LINUX_KERNEL_USE_DEFCONFIG`, and any fragments before saving changes from `linux-menuconfig`.

- With a project-owned custom config, use `linux-update-config` for the full config or `linux-update-defconfig` for
  the minimal form when supported. Verify the copy-back destination before running either target.
- With a named kernel defconfig, use `linux-savedefconfig` where supported to produce the minimal config in the kernel
  build tree, then copy it to a project-owned file and select that custom config, or maintain intentional overrides as
  fragments. Do not assume `linux-update-config`/`linux-update-defconfig` exist in this mode.
- With fragments, preserve their intended separation. Inspect the release's Kconfig-package update behavior and review
  the resulting base/fragment diffs rather than flattening them into an upstream base file accidentally.

Reconfigure from the persisted inputs and verify the effective settings before cleanup or handoff. Edits remaining only
in the kernel build tree disappear when that tree is removed. Apply the same persistence principle to BusyBox and U-Boot
using their own supported targets.

## U-Boot Integration

Buildroot owns version selection, package configuration, dependencies, and deployment of the bootloader artifacts.
Keep those settings in the board configuration. U-Boot source porting, environment/boot-flow behavior, and verified-boot
implementation belong to `u-boot-development`.
