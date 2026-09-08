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

**How the public key reaches U-Boot is the step people skip.** Signing produces a FIT; refusing an unsigned
one needs the verifying key inside U-Boot's own control device tree, together with the `required` property.
U-Boot ships `tools/key2dtsi.py` to turn a key into a `.dtsi`, and `CONFIG_DEVICE_TREE_INCLUDES` names extra
`.dtsi` files folded into the control DTB at build time. In a Yocto build that means the key must be an input
to the **U-Boot** recipe, not only to the kernel FIT recipe — two recipes, one key, and a mismatch between
them is a board that happily boots anything. The mechanics belong to `u-boot-development`; the build-side
obligation is making sure the same key material feeds both.

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

For *device-held* keys — a per-unit identity rather than the signing key — the portable abstraction is
**PKCS#11**, which lets the same code address a TPM, a discrete HSM, or a TEE-backed token without knowing
which it has. On ARM parts with a secure world, `meta-arm` packages OP-TEE (`optee-os`, `optee-client`, and a
TA devkit for building trusted applications), and a PKCS#11 trusted application then acts as an on-device soft
HSM. The property that makes it worth the complexity: **generate the key on the device rather than importing
one**, so the private key never exists outside the secure world, and ship only a certificate request off it.
Where a platform has no secure world, the equivalent is a TPM or an external secure element — and where it has
neither, the key is a file, and the design should say so.

**Verify the produced artefact, then the negative case:**

```bash
mkimage -l tmp/deploy/images/<machine>/fitImage     # signature nodes and the algorithms actually used
fdtget -l tmp/deploy/images/<machine>/fitImage /configurations/conf-1
# and in the U-Boot control dtb: the key node, and whether it carries required = "conf" / "image"
```

Then boot a deliberately corrupted or unsigned FIT and confirm the board **refuses** it, with U-Boot naming
the missing required signature rather than silently falling back. A signed image that boots proves the
signature was accepted; only a rejected bad image proves verification was required.

Two negative cases, not one, because they fail differently: an **unsigned** image and an image signed with the
**wrong key** should produce distinguishable errors. If both produce the same message, or one of them boots,
the configuration is not doing what you think.

## Below the FIT: the platform's own first stage

Everything above starts at U-Boot. What authenticates U-Boot itself is the SoC's boot ROM, and that layer is
**not portable** — the container format, the key hierarchy, the fuse or OTP store and the vendor tooling
differ per part, and this skill will not pretend otherwise. What generalises is the shape a platform must
provide, and the questions to ask of it:

| The platform must have                                      | Ask                                                                |
| ----------------------------------------------------------- | ------------------------------------------------------------------ |
| A ROM-verified first-stage container format                 | What does the ROM actually verify, and what does it skip?          |
| A one-time-programmable store for the root key hash         | Where, how many, and is it revocable?                              |
| **A lifecycle state that makes verification mandatory**     | Is the part still in an open state that verifies and boots anyway? |
| A host tool that both builds and offline-verifies the image | Can CI check the artefact without a board?                         |

**The third row is the trap, and it is the same shape as `CONFIG_FIT_SIGNATURE`.** On typical parts, burning
the root-key hash changes nothing on its own: the ROM keeps booting unsigned or badly-signed images until the
device is transitioned to a closed lifecycle state. A build pipeline that signs correctly, fuses correctly and
never transitions is producing devices with no secure boot at all — and every functional test passes.

The verification shape that survives across vendors: **read the ROM's own authentication event log, not the
boot outcome.** A part that boots is not evidence; a log with no authentication events is. Expect a good
implementation to distinguish "no signature was checked" from "bad key hash" from "bad signature", and check
which of the three you are looking at before concluding anything. Where a vendor exposes no such log, say that
the property cannot be observed on that platform rather than inferring it from a successful boot.

Where a platform provides none of this, the chain starts at whatever the ROM does load unconditionally, and
the honest statement is that the FIT-level verification protects against a modified kernel but not against a
replaced bootloader.

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

**Three parts of it are build-side and therefore ours**, because they are decided in metadata rather than on
the device:

- **The on-device keyring should hold the CA certificate, not the signing leaf.** A pinned leaf means every
  certificate rotation is a field update; a CA lets you rotate signers without touching deployed devices.
  Where a fleet's clock cannot be trusted, an updater that validates against the bundle's signing time rather
  than the current time is the difference between a working update and a mass failure at certificate expiry.
- **The A/B slot definition exists in two places that must agree** — the partition layout in the `.wks`, and
  the updater's own configuration plus whatever `fw_env.config` tells `libubootenv` where the U-Boot
  environment lives. A mismatch is not a build failure; it is a device that installs to the wrong slot or
  cannot record which slot it booted.
- **Bundle signing needs the same key custody as FIT signing**, and usually the same answer.

Slot state itself belongs outside the update tooling: the U-Boot environment is not written atomically, which
is the argument for keeping the one fact that must survive a bad update somewhere else. That trade-off is
`u-boot-development`'s.

## x86 targets: a different first stage

Where the target boots UEFI rather than U-Boot, the FIT machinery above does not apply and the equivalent is
Secure Boot's key hierarchy — the platform key, key-exchange keys, and the allow and forbid databases — with
firmware-owned state readable at runtime through the EFI variables that report whether Secure Boot is enabled
and whether the platform is still in setup mode. Enrolling your own keys is the step that turns a
vendor-trusted chain into one you control, and the tooling for it has changed hands, so check what is current
and maintained rather than following an older guide.

**This skill's coverage here is thinner than its U-Boot coverage**, and that is a stated limit rather than a
judgement that UEFI targets matter less. Confirm the mechanism against current documentation before advising.

Two adjacent facts worth knowing when the boundary comes up: bootcount-based rollback state lives outside the
U-Boot environment for a reason (saving that environment is not atomic), and `libubootenv` is the Yocto recipe
providing `fw_printenv`/`fw_setenv`. Both are `u-boot-development`'s subject.
