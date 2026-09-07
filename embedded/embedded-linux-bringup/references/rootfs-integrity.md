# Rootfs Integrity with dm-verity

A read-only, cryptographically verified rootfs is the rootfs link of a verified-boot chain: the bootloader authenticates
the kernel and its command line, and the kernel in turn refuses to run a rootfs whose blocks do not match a known-good
root hash. This reference covers dm-verity as applied to the *installed, running* rootfs — how to build the hash tree,
bring it up at boot, and anchor its root hash to the trust chain.

It does NOT re-teach FIT signing or SoC secure boot. That is the U-Boot half of the chain; cross-link to
`u-boot-development` `references/uboot-security-and-provenance.md` for how the root hash becomes trusted.

## Contents

- [What dm-verity gives you](#what-dm-verity-gives-you)
- [Building the hash tree: `veritysetup`](#building-the-hash-tree-veritysetup)
- [Bringing the rootfs up at boot](#bringing-the-rootfs-up-at-boot)
- [Anchoring the root hash to the trust chain](#anchoring-the-root-hash-to-the-trust-chain)
- [Interaction with A/B OTA](#interaction-with-ab-ota)
- [Read-only rootfs consequences](#read-only-rootfs-consequences)
- [Safety](#safety)

---

## What dm-verity gives you

dm-verity is a device-mapper target that provides transparent, block-level integrity checking of a read-only block
device using a cryptographic digest from the kernel crypto API. Verified against the kernel admin guide
([docs.kernel.org/admin-guide/device-mapper/verity](https://docs.kernel.org/admin-guide/device-mapper/verity.html)).

The mechanism is a Merkle (hash) tree. Leaf nodes hash the data blocks; each higher level hashes the level below it, up
to a single **root hash** that anchors the whole device. On every block read, the kernel recomputes the hash and walks
it up the tree to the root; if any hash fails to verify, the I/O fails. This detects both deliberate tampering and
on-media bit-rot at the moment a block is read, not on a periodic scan.

The target is inherently **read-only** — a verified device cannot be written through the dm-verity mapping, because a
write would invalidate the tree. What happens on a mismatch is configurable via table flags (kernel admin guide):

| Corruption mode                       | Behaviour on a bad block                           |
| ------------------------------------- | -------------------------------------------------- |
| default (no flag)                     | Log the corrupted block; allow the read to proceed |
| `restart_on_corruption`               | Restart the system when a corrupted block is found |
| `panic_on_corruption`                 | Panic the kernel when a corrupted block is found   |
| `ignore_zero_blocks`                  | Do not verify blocks expected to be all-zero       |
| `restart_on_error` / `panic_on_error` | React the same way to I/O errors                   |

For a rootfs you almost always want `restart_on_corruption` or `panic_on_corruption`: a tampered production rootfs
SHOULD refuse to run, not log and continue. The trade-off is deliberate — see [Safety](#safety).

Kernel config: `CONFIG_DM_VERITY=y` (or `=m`) plus the hash algorithm the tree uses, e.g. `CONFIG_CRYPTO_SHA256`. For
the in-kernel root-hash-signature path (below) add `CONFIG_DM_VERITY_VERIFY_ROOTHASH_SIG`, and
`CONFIG_DM_VERITY_VERIFY_ROOTHASH_SIG_SECONDARY_KEYRING` if the key lives in the secondary keyring. Confirm these
against the running kernel with `zcat /proc/config.gz | grep -i DM_VERITY`.

---

## Building the hash tree: `veritysetup`

`veritysetup` (from the cryptsetup project) builds and opens verity devices. Verified against `veritysetup(8)`.

The `format` action computes the hash tree for a data device, stores it on a hash device, and prints the **root hash** —
the value you must later anchor in a trusted place:

```bash
# Illustrative — build host or a provisioning step, not the running target.
# format <data_device> <hash_device>; prints "Root hash: <hex>".
veritysetup format rootfs.img rootfs.hash
```

`format` accepts the tuning that fixes the on-disk layout — you MUST reuse the identical values at open time or the root
hash will not match:

- `--hash <algo>` — digest algorithm (default `sha256`).
- `--data-block-size <bytes>` / `--hash-block-size <bytes>` — capped at the kernel page size.
- `--data-blocks <n>` — how much of the data device is covered (default: all).
- `--salt <hex>` — salt mixed into the hashes.
- `--hash-offset <bytes>` — offset of the hash area, for storing the tree *appended* to the data device instead of on a
  separate partition.

The `open` action creates the dm-verity mapping and hands it to the kernel; `verify` checks a device in userspace
without creating a mapping:

```bash
# Illustrative.
# open <data_device> <name> <hash_device> <root_hash>
veritysetup open rootfs.img vroot rootfs.hash <root_hash>   # -> /dev/mapper/vroot
veritysetup verify rootfs.img rootfs.hash <root_hash>       # userspace check only
```

`--root-hash-signature <file>` attaches a PKCS#7 signature of the root hash that the kernel verifies against its trusted
keyring (requires kernel 5.4+ and `CONFIG_DM_VERITY_VERIFY_ROOTHASH_SIG`). This is one way to anchor trust; the FIT
route below is the other.

---

## Bringing the rootfs up at boot

The kernel must map the verity device *before* it mounts root, so the setup runs either from the kernel command line or
from an initramfs.

**Kernel command line via `dm-mod.create=`.** With `CONFIG_DM_INIT=y`, the kernel can create device-mapper targets
directly from a `dm-mod.create=` cmdline argument — no initramfs needed. The argument encodes the full verity table (the
same fields `veritysetup` uses):

```text
# Illustrative dm-mod.create table (single line on the real cmdline).
# <name>,<uuid>,<minor>,<flags>,<table>
# table = <start> <len> verity <version> <data_dev> <hash_dev> \
#         <data_block_sz> <hash_block_sz> <#data_blks> <hash_start_blk> \
#         <algo> <root_hash> <salt>
dm-mod.create="vroot,,,ro, 0 <#sectors> verity 1 /dev/mmcblk0p2 /dev/mmcblk0p3 \
  4096 4096 <#data_blks> <hash_start_blk> sha256 <root_hash> <salt>"
root=/dev/dm-0 ro
```

**initramfs.** An initramfs runs `veritysetup open …` (optionally with `--root-hash-signature`) and then mounts
`/dev/mapper/vroot` as root. This suits boards that already use an initramfs and lets you layer signature checking and
recovery logic in userspace.

Two typical partition layouts:

| Layout                  | Data                                 | Hash tree                                      | Notes                                    |
| ----------------------- | ------------------------------------ | ---------------------------------------------- | ---------------------------------------- |
| Separate hash partition | rootfs partition (e.g. `p2`)         | its own partition (e.g. `p3`)                  | Cleanest; hash device is independent     |
| Appended hash           | rootfs image + tree in one partition | tail of the same partition via `--hash-offset` | One partition; offset MUST match at open |

The root hash is NOT stored on either partition as authoritative — it must arrive from a trusted source, which is the
whole point of the next section.

---

## Anchoring the root hash to the trust chain

dm-verity proves the rootfs matches *a* root hash. It says nothing about whether that root hash is the one you shipped.
An attacker who can rewrite both the rootfs and an untrusted, mutable root hash simply re-runs `veritysetup format` and
produces a self-consistent malicious pair. The root hash therefore MUST come from a source the earlier boot stages
already authenticated.

The standard integration folds the root hash into the kernel command line and lets U-Boot's FIT signature cover it:

```text
U-Boot verifies the signed FIT  (kernel + DTB + initramfs + bootargs/cmdline)
        │   the cmdline — carrying dm-mod.create=/root hash — is inside the
        │   signed configuration, so tampering with the root hash breaks the
        ▼   FIT signature and U-Boot refuses to boot
Kernel boots, reads the verified root hash from its cmdline
        │
        ▼
Kernel brings up the dm-verity rootfs against that trusted root hash
```

Because the FIT signature covers the configuration (kernel + FDT + ramdisk + cmdline together), embedding the root hash
in the signed cmdline makes it as trusted as the kernel itself. This reference does NOT cover how to build or require
that FIT signature — see `u-boot-development` `references/uboot-security-and-provenance.md` ("Make the FIT Signature
Required" and "Extend Trust to the SPL") for the U-Boot half of the chain.

The in-kernel alternative is `veritysetup --root-hash-signature` / `root_hash_sig_key_desc` with
`CONFIG_DM_VERITY_VERIFY_ROOTHASH_SIG`: the kernel verifies a PKCS#7 signature of the root hash against a keyring it
trusts. Either way the invariant is the same — the root hash is trusted only because something already trusted vouches
for it.

### Worked example: root hash in a signed FIT cmdline

An A/B eMMC board where slot A's rootfs lives on `mmcblk0p2` with its hash tree on `mmcblk0p3`:

```bash
# Illustrative — provisioning host.
# 1. Build the tree and capture the root hash.
veritysetup format slotA-rootfs.img slotA-rootfs.hash   # note the printed Root hash

# 2. Put the dm-mod.create table (with that root hash) into the bootargs the
#    .its file bakes into the signed FIT configuration, then sign the FIT with
#    mkimage -r as in u-boot-development. Tampering with the root hash now invalidates
#    the FIT signature and U-Boot rejects the image.
```

The verity setup is illustrative; the FIT authoring and signing steps are owned by `u-boot-development` and are only
referenced here.

---

## Interaction with A/B OTA

Each rootfs slot is a distinct image with its own hash tree and therefore its own root hash. An A/B update that writes
the inactive slot MUST also deliver that slot's new root hash into the slot's signed boot configuration — otherwise the
freshly written rootfs either fails verification or, worse, is verified against a stale hash. Anchoring and slot
activation move together. See `references/ota-updates.md` for the A/B update mechanics and framework choice.

**Distinct use of dm-verity — do not conflate the two.** RAUC's `verity` *bundle* format is a DISTINCT use of dm-verity:
it protects the update ARTIFACT (the bundle's SquashFS) while it is read during install — not the installed, running
rootfs. This file covers running-rootfs dm-verity; the artifact-at-install use is described in
`references/ota-updates.md` → "RAUC bundle formats". Same kernel mechanism, two different deployment points; RAUC
configures only the former, not rootfs dm-verity.

---

## Read-only rootfs consequences

A dm-verity rootfs cannot be written, so every writable path must live elsewhere. Plan this before enabling verity, or
the first boot fails on a service that expects to write `/`.

- **Writable state on a separate partition.** Mount a dedicated read-write partition (ext4/f2fs) for `/var`, `/etc`
  overrides, application data, and anything that changes. This partition is NOT covered by dm-verity — protect its
  confidentiality/integrity separately if it matters (e.g. dm-crypt, or an fs-verity/IMA policy).
- **Overlays for a writable-looking `/`.** An overlayfs with the verified rootfs as the read-only lower layer and a rw
  partition (or tmpfs, for discard-on-reboot state) as the upper layer gives services a writable view without breaking
  the integrity guarantee of the lower layer.
- **Logging and updates.** Logs, journald state, and OTA scratch space must target the rw partition or a tmpfs; a full
  rw partition then becomes an availability concern, not an integrity one. Updates never modify the running rootfs in
  place — they write the *other* slot (see A/B above).

---

## Safety

A verified rootfs deliberately trades availability for integrity: any mismatch makes the rootfs refuse to run. RFC 2119
keywords are normative.

- You MUST anchor the root hash in a signed boot configuration (signed FIT cmdline, or a kernel-verified
  `--root-hash-signature`). An unsigned or mutable root hash defeats the entire purpose — an attacker rewrites the
  rootfs and the hash together and dm-verity happily verifies the forgery.
- You MUST keep the rootfs mounted read-only. A writable verified rootfs is a contradiction; route all writes to a
  separate rw partition or an overlay upper layer.
- dm-verity makes the rootfs unbootable on ANY block mismatch — tampering or bit-rot alike. This is a FEATURE, not a
  bug. Because of it you MUST provide a recovery/rescue path (a second verified slot, or a signed rescue image reachable
  via the SoC ROM/boot-mode strap) so a genuine corruption or a botched update does not permanently strand the device.
  Choosing `panic_on_corruption` / `restart_on_corruption` without a rescue path is how a single bad block bricks a
  field unit.
- The root hash is trusted only because an earlier, already-trusted stage vouches for it. For how the bootloader
  establishes that trust — required FIT signatures, SPL trust, SoC secure boot — see `u-boot-development`
  `references/uboot-security-and-provenance.md`.
