# OTA and Update Strategy

The userspace framework layer that sits ABOVE the bootloader. RAUC and swupdate
own the download, verify, write-to-inactive-slot, and confirm-or-roll-back
sequence; U-Boot owns the boot decision. This reference covers strategy choice,
both frameworks, and how they drive the slot/bootcount environment that
`uboot-dev` documents. It does NOT re-teach the bootloader mechanics — cross-link
to `uboot-dev` for those.

## Contents

- [Choosing an update strategy](#choosing-an-update-strategy)
- [RAUC](#rauc)
- [swupdate](#swupdate)
- [RAUC vs swupdate](#rauc-vs-swupdate)
- [Bootloader integration](#bootloader-integration)
- [Build-system integration](#build-system-integration)
- [Signing, keys, and rollback verification](#signing-keys-and-rollback-verification)
- [Safety](#safety)
- [Worked examples](#worked-examples)

---

## Choosing an update strategy

Pick the layout FIRST; the framework choice follows from it. Three base
strategies, plus delta as an optional overlay on any of them.

| Strategy | Flash cost | Downtime | Atomic | Rollback |
|----------|-----------|----------|--------|----------|
| Redundant A/B (dual-copy) | 2× rootfs | Near-zero (update inactive slot while running) | Yes — bootloader flips one slot | Yes — keep last-known-good slot |
| Single-copy + recovery/rescue | 1× rootfs + small rescue (~2.5–8 MB) | Update window: reboot into rescue, device offline | Only via the rescue mediator | Rescue can re-flash, but no online fallback |
| Delta (overlay) | Same as base layout | Same as base | Same as base | Same as base |

Decision path:

1. **Enough flash for two full rootfs copies AND you need zero-downtime updates
   with instant rollback?** Choose **redundant A/B**. This is the default for
   field devices that must stay serviceable. The running slot is the rollback;
   the update writes the inactive slot and the bootloader switches atomically.
2. **Flash-constrained, and a short reboot-into-rescue window is acceptable?**
   Choose **single-copy + recovery/rescue**. A compact rescue kernel+rootfs (a
   few MB, far cheaper than a second full rootfs) boots the updater, which
   rewrites the single production copy. Interrupted updates recover because the
   rescue image is always bootable — but there is no online, already-working
   fallback the way A/B gives you.
3. **Bandwidth-constrained (cellular, large fleet, big images)?** Layer **delta**
   on top of whichever base you chose. Delta cuts what you download, not what you
   store: RAUC via casync/adaptive block updates, swupdate via a delta/zchunk
   handler. It adds server-side and build-side complexity — justify it with real
   bandwidth cost.

Atomicity is the property that matters most: an update is atomic when a power
loss at any point leaves the device booting a complete, valid image. A/B gets
this from the bootloader slot switch. Single-copy is atomic only because the
rescue path can always restart the write; the production copy itself is
transiently invalid mid-write.

---

## RAUC

RAUC (Robust Auto-Update Controller) is an opinionated A/B framework built around
a signed bundle and a declarative slot description. Primary docs:
[rauc.readthedocs.io](https://rauc.readthedocs.io).

### system.conf — slots and bootloader backend

The target-side `/etc/rauc/system.conf` declares the compatible string, the
bootloader backend, and every slot. Verified against the RAUC reference.

```ini
[system]
compatible=myboard-armhf
bootloader=uboot
# optional: bundle-formats=, mountprefix=, data-directory=,
#           boot-attempts=, activate-installed=

[keyring]
path=/etc/rauc/keyring.pem

[slot.rootfs.0]
device=/dev/mmcblk0p2
type=ext4
bootname=A

[slot.rootfs.1]
device=/dev/mmcblk0p3
type=ext4
bootname=B
```

- `[system] bootloader` accepts `barebox`, `grub`, `uboot`, `efi`, `custom`, or
  `noop`.
- `[slot.<class>.<idx>]` requires `device`; `type` (e.g. `raw`, `nand`, `ext4`,
  `vfat`, `ubifs`, or the bootloader-switch types `boot-emmc`,
  `boot-mbr-switch`, `boot-gpt-switch`, `boot-raw-fallback`) and `bootname` are
  optional but needed for a bootable slot. `bootname` registers the slot with the
  bootloader backend under that name. `parent` links a non-bootable child slot
  (e.g. a kernel/appfs) to its bootable rootfs parent.

### Bundle, manifest, and signing

A bundle is a single signed `.raucb` file. Build it on the host from an input
directory containing the images and a `manifest.raucm`:

```bash
# Illustrative — build host, not the target.
rauc bundle --cert=cert.pem --key=key.pem input-dir/ update.raucb
```

`manifest.raucm` describes the bundle content (verified against the RAUC docs):

```ini
[update]
compatible=myboard-armhf
version=2026.07-1

[image.rootfs]
filename=rootfs.ext4
```

RAUC records size and sha256 per image at bundle time and stores the signature in
the bundle. `--cert`/`--key` are PEM files or PKCS#11 URIs (for an HSM-held key).

### RAUC bundle formats

RAUC has three bundle formats, selected on the target via `bundle-formats=` in the
`[system]` section (a space-separated list, or `+`/`-` prefixes relative to the
built-in defaults). Verified against the RAUC docs (advanced/reference). Do not
assume `verity` is the compiled default — historically bundles were `plain`; pick
per your security and streaming needs.

| Format | Structure | Kernel need | Notes |
|--------|-----------|-------------|-------|
| `plain` | SquashFS with an APPENDED CMS signature | none | Simplest; has a manipulation caveat (below) |
| `verity` | dm-verity hash tree over the SquashFS + a DETACHED CMS signature | `CONFIG_DM_VERITY` | Recommended for security; REQUIRED for streaming |
| `crypt` | `verity` plus symmetric encryption of the payload | `CONFIG_DM_VERITY` + `CONFIG_DM_CRYPT` | Adds confidentiality on top of `verity` |

- **`plain`** verifies the whole SquashFS against the appended signature, then
  re-opens it to install. That gap is a documented manipulation caveat: an
  unprivileged process that rewrites the SquashFS *after* the signature check but
  *before* install could elevate privilege, so RAUC adds ownership/permission
  guards around the bundle. `plain` needs no dm-verity.
- **`verity`** stores a dm-verity hash tree over the SquashFS and a detached CMS
  signature over the root hash. The kernel checks each SquashFS block as it is
  read, closing the `plain` manipulation gap; it requires `CONFIG_DM_VERITY`.
- **`crypt`** builds on `verity` and additionally encrypts the payload (dm-crypt),
  with the symmetric key carried in the manifest, itself asymmetrically encrypted
  to a set of recipients — use it when the update needs confidentiality, not just
  integrity.

The `verity` format is what enables **HTTP/adaptive streaming install**: RAUC can
install directly from a URL (`rauc install https://…`) without downloading a full
local copy, and adaptive block-based updates fetch only changed blocks. A `plain`
bundle cannot be streamed (`Bundle format 'plain' not supported in streaming
mode`).

**Distinct from rootfs dm-verity — do not conflate the two.** The `verity` BUNDLE
format applies dm-verity to the update ARTIFACT (the bundle's SquashFS) as it is
read during install — NOT to the installed, running rootfs. Rootfs dm-verity (a
read-only verified running rootfs whose root hash is anchored in signed boot
config, set up OUTSIDE RAUC) is a separate use of the same kernel mechanism; see
`references/rootfs-integrity.md`.

### Install, verify, and boot confirmation

```bash
# Illustrative — on the target.
rauc install update.raucb          # verify signature, write INACTIVE slot, set it primary
rauc status --detailed             # inspect slots, boot state, last error
rauc status mark-good              # confirm the CURRENT boot after a health check
rauc status mark-bad               # reject this boot, fall back
```

- Verification is signature-based against the configured `[keyring]` (an X.509
  cert/CA in PEM). `rauc info --keyring=<cert> update.raucb` verifies a bundle
  out-of-band.
- `rauc install` writes the inactive slot and marks it primary for the next boot;
  it never touches the running slot.
- `mark-good`/`mark-bad` take an optional target (`booted`, `other`, or a slot
  name); `mark-active` switches the primary slot manually.

### hawkBit integration

`rauc-hawkbit-updater` is the separate agent that polls an Eclipse hawkBit server,
downloads the assigned `.raucb`, and calls `rauc install`. RAUC itself is the
local installer; hawkBit is the deployment-management server.

---

## swupdate

swupdate is a flexible framework that handles A/B, single-copy+rescue, and exotic
partition layouts through a scripted manifest and pluggable handlers. Primary
docs: [sbabic.github.io/swupdate](https://sbabic.github.io/swupdate),
[swupdate.org](https://swupdate.org).

### sw-description manifest

The manifest is a libconfig document (JSON is also supported) rooted in a
`software` block. Verified against the swupdate docs:

```libconfig
software =
{
    version = "2026.07-1";
    hardware-compatibility: [ "1.0", "1.2" ];

    images: (
        {
            filename = "rootfs.ext4";
            device = "/dev/mmcblk0p3";   // write the inactive slot
            sha256 = "<hash>";
        }
    );
    scripts: ( { filename = "post.lua"; type = "lua"; } );
    bootenv: ( { name = "BOOT_ORDER"; value = "B A"; } );
};
```

- **images** write to a `device` or UBI `volume`, optionally through a named
  `handler` and with `compressed`/`encrypted` set. **files** drop individual files
  onto a mounted path. **scripts** run Lua or shell pre/post-install. **bootenv**
  writes bootloader environment variables. **partitions** define UBI volumes.
- swupdate selects entries by board/mode using `/etc/hwrevision`
  (`<boardname> <revision>`), matching most-specific first
  (`<boardname>.<selection>.<mode>.<entry>` down to `<entry>`). This is how ONE
  `.swu` serves several boards or a "stable"/"test" mode.
- `install-if-different` skips an image whose version already matches;
  `install-if-higher` rejects downgrades.

### Dual-copy vs single-copy+recovery

swupdate supports both base strategies from section 1 directly:

- **Double-copy (A/B):** writes the inactive copy while the running copy stays
  untouched; the bootloader selects the copy. A working copy always survives an
  interrupted or power-lost update, at the cost of 2× storage.
- **Single-copy + recovery:** one production copy plus a compact rescue kernel and
  rootfs (~2.5–8 MB). The bootloader enters upgrade mode and loads swupdate from
  RAM, which rewrites the whole storage. Recovery is guaranteed because the rescue
  image is always bootable.

### .swu format

A `.swu` is a **cpio archive** (built with `cpio -H crc`). The `sw-description`
manifest MUST be the FIRST file in the archive, so swupdate can extract and verify
metadata before it streams the image payloads — cpio is used precisely because it
streams. A signed bundle adds `sw-description.sig` as the second entry.

### Delivery: local and remote

- **suricatta** daemon mode (`-u`) pulls updates from a backend server; the
  reference backend is Eclipse **hawkBit** (with TLS support). This is the
  swupdate counterpart to `rauc-hawkbit-updater`.
- **mongoose** webserver mode (`-w`) exposes an embedded web server for local
  browser-upload updates.
- **Handlers** extend swupdate to new image types (raw, ubi, bootloader env, rdiff
  delta, custom); Lua or C. This extensibility is swupdate's main lever over RAUC
  for unusual layouts.

---

## RAUC vs swupdate

Both do secure, atomic A/B on the same bootloader mechanics. Choose on model fit,
not capability — either can ship a correct A/B update.

| Dimension | RAUC | swupdate |
|-----------|------|----------|
| Bundle model | Single signed `.raucb`; images + `manifest.raucm` | `.swu` cpio stream; `sw-description` first |
| Config style | Declarative slots in `system.conf` + manifest | Scripted `sw-description` (libconfig/JSON) + handlers |
| Layouts | A/B-centric, opinionated | A/B, single-copy+rescue, exotic partitioning |
| Delta | casync / adaptive block updates | delta/zchunk/rdiff handler |
| Signing | Mandatory X.509 bundle signature | Optional (CONFIG_SIGNED_IMAGES): CMS or RSA PKCS#1 |
| Server | hawkBit via `rauc-hawkbit-updater` | hawkBit via suricatta; embedded webserver (mongoose) |
| Learning curve | Lower for standard A/B; less flexible | Steeper; more flexible for non-standard cases |

Rule of thumb: **RAUC** when you want a clean, signed-by-default A/B rollout on a
conventional two-slot board and hawkBit fleet management. **swupdate** when the
partition layout is unusual, you need single-copy+rescue, or you need custom
handlers/scripting the declarative model cannot express.

Mender is a third option (integrated client + server, opinionated A/B); this
reference does not cover it — evaluate it separately if a hosted management server
is the priority.

---

## Bootloader integration

Both frameworks stop at the slot boundary: they write the inactive slot and then
flip the SAME bootloader state that U-Boot reads to pick a slot and count boot
attempts. The framework owns userspace; U-Boot owns the boot decision.

- **RAUC's `uboot` backend** drives exactly the env `uboot-dev` documents:
  `BOOT_ORDER` (slot priority list) and `BOOT_x_LEFT` (remaining attempts per
  slot). `mark-bad` sets `BOOT_x_LEFT=0` and drops the slot from `BOOT_ORDER`;
  `mark-good` resets `BOOT_x_LEFT` to its default; marking a slot primary moves
  it to the front of `BOOT_ORDER` with that same count. That reset count defaults
  to 3 but is configurable in `[system]` via `boot-attempts` (mark-good) and
  `boot-attempts-primary` (install-time primary). RAUC writes these through
  `fw_setenv`/libubootenv.
- **swupdate** writes the same class of variables via its `bootenv` manifest
  section and a bootloader handler, or a post-install script calling `fw_setenv`.

For the U-Boot side of this contract — the `bootcount`/`bootlimit`/`altbootcmd`
mechanism, the `BOOT_ORDER`-style env, and the `fw_setenv bootcount 0` reset after
a healthy boot — see `uboot-dev`:

- `references/uboot-environment.md` → "A/B slot via environment" and the
  `bootcount`/`altbootcmd` / `fw_setenv bootcount 0` reset pattern.
- `references/uboot-porting.md` → "A/B partition update patterns" (slot selection
  via bootable flag or bootcount, GPT attributes).

Do NOT reimplement that env logic here — the framework's job is to set it
correctly, U-Boot's job is to act on it.

---

## Build-system integration

Both frameworks are packaged in the major build systems; enabling them is a build
task, not an OTA task. Brief pointers:

- **Yocto/OpenEmbedded:** `meta-rauc` (and `meta-rauc-community` for BSP glue) or
  `meta-swupdate` provide the recipes and bundle/`.swu` image classes. Route recipe
  and layer work to **yocto-oe-dev**.
- **Buildroot:** `BR2_PACKAGE_RAUC` or `BR2_PACKAGE_SWUPDATE` (plus the
  `BR2_TARGET_ROOTFS_*` sizing for two slots). Route defconfig/package work to
  **buildroot-dev**.

The build system produces the two-slot image layout and the framework binary; this
reference covers what the framework does at runtime.

---

## Signing, keys, and rollback verification

**Signing and verification.**

- **RAUC:** bundle signing is mandatory. Sign with an X.509 cert/key
  (`rauc bundle --cert --key`); the target verifies against `[keyring]` before
  writing anything. Keep the signing key off the device and ideally in an HSM
  (PKCS#11 URI). Only the CA/verification cert ships in the image keyring.
- **swupdate:** signing is opt-in via `CONFIG_SIGNED_IMAGES`; when set, swupdate
  always verifies the compound image. `sw-description` is signed to
  `sw-description.sig` (CMS/X.509 via `openssl cms -sign`, or RSA PKCS#1 via
  `openssl dgst -sha256 -sign`), and every sub-image carries a `sha256` the signed
  manifest binds. Verifying the manifest + per-image hashes secures the whole
  stream. Enable `CONFIG_SIGNED_IMAGES` in production — an unsigned build installs
  anything.

**Rollback verification (the part teams get wrong).** A slot switch alone is not a
successful update. The sequence MUST be: boot the new slot → run a real health
check (services up, hardware reachable, app functional) → only THEN confirm.

- RAUC: call `rauc status mark-good` only from a health-check service that has
  proven the system works. Until then the boot is unconfirmed.
- swupdate / raw U-Boot: reset `bootcount`/`BOOT_x_LEFT` (via `fw_setenv
  bootcount 0` or the framework's mark-good) only after the health check passes.
- **Watchdog + bootcount interplay:** arm a hardware watchdog early so a hang in
  the new image forces a reboot; U-Boot's `bootcount`/`bootlimit` then counts the
  failed attempts and runs `altbootcmd` to fall back to the good slot once the
  limit is hit. Confirming the boot (mark-good) is what clears the counter. If the
  health check never runs, the device rolls back on its own — which is the point.

---

## Safety

OTA mutates boot slots and bootloader environment; a wrong step bricks the device
in the field. RFC 2119 keywords are normative.

- You MUST push an update ONLY to the INACTIVE slot and keep the running slot
  intact as the rollback target. You MUST NOT overwrite the active/running slot.
- You MUST verify the bundle/`.swu` signature BEFORE writing any slot. You MUST NOT
  disable signature verification (`--no-verify`, unset `CONFIG_SIGNED_IMAGES`) on a
  production device.
- You MUST mark a boot good ONLY after a real health check confirms the new image
  works. You MUST NOT call `mark-good` / reset `bootcount` unconditionally at
  startup — that destroys the rollback guarantee.
- You MUST NOT disable the rollback path (watchdog, `bootlimit`/`BOOT_x_LEFT`,
  `altbootcmd`) to "simplify" an update.
- Editing slot layout, `system.conf`/`sw-description`, or the bootloader env on a
  live device is a mutating action. You MUST back up the current env and pair the
  change with its restore, per the `SKILL.md` confirmation gates and the `uboot-dev`
  safety contract. You MUST NOT change these unprompted.
- SHOULD prove the update path on a spare/bench unit (including a forced-failure
  rollback test) before any fleet rollout.

---

## Worked examples

Illustrative only — adapt device paths, slot names, and sizes to your board. Any
shell shown is minimal and unverified against your target.

### Worked example: eMMC A/B layout with RAUC (`uboot` backend)

An eMMC-based board, two rootfs slots plus persistent data:

```
/dev/mmcblk0p1  boot   (FAT)   SPL + U-Boot + boot script
/dev/mmcblk0p2  rootfs A (ext4)  slot rootfs.0, bootname=A
/dev/mmcblk0p3  rootfs B (ext4)  slot rootfs.1, bootname=B
/dev/mmcblk0p4  data   (ext4)  persistent, never touched by OTA
```

`system.conf` uses `bootloader=uboot` and the two `[slot.rootfs.N]` blocks shown
above. U-Boot is built with the RAUC `BOOT_ORDER`/`BOOT_x_LEFT` boot-selection
script (see `uboot-dev` `references/uboot-porting.md`). Update flow on the target:

```bash
# Illustrative.
rauc install update.raucb     # verifies, writes the inactive slot, sets it primary
reboot
# ... new slot boots, health-check service runs ...
rauc status mark-good         # only after the check passes; clears BOOT_x_LEFT
```

If the new slot fails to reach the health check, U-Boot exhausts `BOOT_x_LEFT` and
boots the old slot — no manual intervention.

### Worked example: single-copy + rescue with swupdate

A flash-constrained SoC that cannot fit two full rootfs copies: ship one
production rootfs plus a small rescue image. The bootloader boots rescue on demand;
rescue runs swupdate from RAM and rewrites the production partition from the
streamed `.swu`. The rescue image itself is the recovery guarantee — it is always
bootable, so an interrupted rewrite is recoverable on the next boot into rescue.
