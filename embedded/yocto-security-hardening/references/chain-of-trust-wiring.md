# Chain of Trust: What the Build Produces and Wires

The build's job is to produce the signed artefacts and put the right hashes, keys and image types in the right
places. Whether the boot ROM and bootloader **enforce** any of it is not a Yocto question.

| Layer                                                  | Owner                                  |
| ------------------------------------------------------ | -------------------------------------- |
| ROM/SoC secure boot, fuses, key hashes                 | vendor documentation; **out of scope** |
| U-Boot verification, FIT `required`, console lockdown  | **u-boot-development**                 |
| Producing and signing the FIT, verity image, initramfs | **this skill**                         |
| Runtime verity/IMA behaviour on a booted board         | **embedded-linux-bringup**             |

The chain has one property worth stating before any mechanism: **dm-verity protects rootfs integrity only.**
Without a verified boot chain above it authenticating the bootloader, kernel and initramfs, an attacker
replaces the kernel or the initramfs and the verity check never runs, or runs against their root hash. A
verity image with no secure boot beneath it is an integrity check the attacker controls.

## Signed FIT images

`kernel-fitimage.bbclass` builds the FIT and, when `UBOOT_SIGN_ENABLE = "1"`, signs it:

```bash
${UBOOT_MKIMAGE_SIGN} -F -k "${UBOOT_SIGN_KEYDIR}" -r ${KERNEL_OUTPUT_DIR}/$2 ${UBOOT_MKIMAGE_SIGN_ARGS}
```

Three facts to carry:

- **`-r` is passed**, so OE writes the `required` property into the U-Boot control dtb it patches. That closes
  the "`CONFIG_FIT_SIGNATURE` does not require anything" trap on the build side — *provided* the dtb carrying
  that key is the one the deployed U-Boot boots.
- **All of it is inside the `UBOOT_SIGN_ENABLE` test.** With it at `0`, the FIT is assembled unsigned, and
  `FIT_GENERATE_KEYS = "1"` only warns that the keys will not be used. A build with keys configured and
  signing disabled looks configured and ships nothing signed.
- **`FIT_SIGN_INDIVIDUAL` signs each sub-image as well as the configuration.** Upstream's editorial advice on
  it differs by release — 5.0 documents a use case for verification somewhere other than U-Boot, 6.0 calls it
  a complexity increase for little benefit. Name the release when advising.

Set the image type so the signed FIT is what boots:

```bitbake
KERNEL_IMAGETYPE = "fitImage"
UBOOT_SIGN_ENABLE = "1"
UBOOT_SIGN_KEYDIR = "<a path outside the build tree>"
UBOOT_SIGN_KEYNAME = "<key basename>"
```

**Key handling is the part to get right and the part this file will not automate.** `FIT_GENERATE_KEYS = "1"`
generating an RSA key into the build directory is a development convenience; a release key belongs in an HSM
or a signing service, is never committed, and never reaches `DL_DIR` or sstate. If a build needs a private key
present, say so explicitly rather than leaving it implied.

**Verify the produced artefact, then the negative case:**

```bash
mkimage -l tmp/deploy/images/<machine>/fitImage     # signature nodes and the algorithms actually used
fdtget -l tmp/deploy/images/<machine>/fitImage /configurations/conf-1
# and in the U-Boot control dtb: the key node, and whether it carries required = "conf" / "image"
```

Then boot a deliberately corrupted or unsigned FIT and confirm the board **refuses** it. A signed image that
boots proves the signature was accepted; only a rejected bad image proves verification was required.

## dm-verity through `meta-security`

`dm-verity-img.bbclass` builds a hash tree over an image and can emit a separate hash device
(`DM_VERITY_SEPARATE_HASH`), with `DM_VERITY_IMAGE_DATA_BLOCK_SIZE ?= "1024"`,
`DM_VERITY_IMAGE_HASH_BLOCK_SIZE ?= "4096"` and GPT type GUIDs for the root and hash partitions. The layer
also ships `dm-verity-image-initramfs.bb`, an initramfs that sets up the mapping at boot, plus four
`docs/dm-verity*.txt` files that are the layer's own reference.

The build-shaped problem this creates, and the reason it is worth a section rather than a pointer:

> **The root hash is only known once the rootfs image is final, and something has to carry it before that** —
> the kernel command line or an initramfs. That is a circular dependency between the initramfs and rootfs
> tasks, and the tempting fix (rebuild everything unconditionally to avoid a stale hash) discards sstate and
> hides the problem rather than solving it.

Two ways out, both build-shaped:

1. **Read the hash at boot from a footer attached after signing** — the approach `meta-avb` takes, stamping
   the hash tree, root hash and signature into an AVB footer so initramfs and rootfs build independently. Its
   tooling (`avb_sign.py` on the host, `avb_verify` on the target) also supports a PKCS#7 root-hash signature
   for `CONFIG_DM_VERITY_VERIFY_ROOTHASH_SIG`, and its signing algorithms include ML-DSA alongside RSA. Layer
   licence reports as `NOASSERTION`; **resolve that before adopting it**, and treat it as an alternative to
   the upstream path, not a replacement for it.
2. **Bundle the initramfs into the signed kernel** — `INITRAMFS_IMAGE_BUNDLE = "1"`, so kernel verification
   implicitly covers the initramfs, or ship the initramfs inside the signed FIT. This is what closes the gap
   named at the top of this file.

A vendor kernel needs the symbols too: `CONFIG_MD`, `CONFIG_BLK_DEV_DM`, `CONFIG_DM_INIT`, `CONFIG_DM_VERITY`,
and `CONFIG_DM_VERITY_VERIFY_ROOTHASH_SIG` for the signed-root-hash path.

**Verify:**

```bash
veritysetup verify <data-image> <hash-image> <root-hash>   # host-side, before anything boots
```

```sh
dmsetup status                     # on target: verity target, and corruption counters
veritysetup status <name>
```

and then corrupt one block of the data image and confirm the read fails. A verity setup never observed
rejecting anything has not been shown to work.

## IMA/EVM and measured boot

`meta-integrity` packages IMA/EVM; the mechanisms and their runtime behaviour are build-system-agnostic and
belong to `embedded-linux-bringup`'s `rootfs-integrity.md`. The Yocto-owned half is signing file hashes at
image-creation time and getting the keys into the image — which has the same key-handling problem as FIT
signing above, and the same answer.

## A/B, rollback and update integrity

RAUC, SWUpdate and Mender are packaged as ordinary recipes; the security question they raise — that an update
mechanism able to write a new rootfs is an execution primitive, so its signature verification and its
key store are part of the trust chain — is covered by `embedded-linux-bringup`'s `ota-updates.md`. Route
there rather than duplicating it.

Two adjacent facts worth knowing when the boundary comes up: bootcount-based rollback state lives outside the
U-Boot environment for a reason (saving that environment is not atomic), and `libubootenv` is the Yocto recipe
providing `fw_printenv`/`fw_setenv`. Both are `u-boot-development`'s subject.
