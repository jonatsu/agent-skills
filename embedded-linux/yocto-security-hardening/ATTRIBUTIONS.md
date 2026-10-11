# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### The Yocto Project: OpenEmbedded-Core

- Source: <https://git.openembedded.org/openembedded-core>, chiefly `meta/classes-recipe/` (`rootfs-postcommands`,
  `image`, `kernel-yocto`, `kernel-fitimage`, `testimage`), `meta/classes-global/`, `meta/conf/distro/include/`, and
  `meta/lib/oe/`
- License: `MIT AND GPL-2.0-only`
- Version: 5.0 (Scarthgap) release series, with the 6.0 development branch (`master`) for forward-looking differences

The guidance on image features, root credentials, read-only rootfs, compiler and linker flags, kernel fragments, signed
FIT images, and sstate trust is built on the release's own classes and configuration. No code is copied.

### The Yocto Project: meta-security

- Source: <https://git.yoctoproject.org/meta-security>, chiefly `classes/`, `recipes-core/images/`,
  `recipes-kernel/linux/`, `recipes-scanners/`, `recipes-compliance/`, `recipes-mac/`, and `lib/oeqa/runtime/cases/`
- License: `MIT`
- Version: 5.0 (Scarthgap) branch, `scarthgap`

The layer map, the kernel hardening fragments, dm-verity wiring, and the MAC and scanner recipes are described from the
layer's own metadata. No code is copied.

## Third-party Sources

### Michael Opdenacker, Root Commit: "Securing Yocto Built Systems"

- Source: <https://rootcommit.com/pub/conferences/2025/elce/yocto-security/yocto-security.pdf>
- License: `CC-BY-SA-4.0`
- Version: Embedded Linux Conference Europe 2025, slides dated 2025-08-26

Surfaced the subject list: attack-surface reduction, unique credentials, read-only rootfs, kernel hardening checks, and
the observation that several controls do not do what their names say. No wording, structure, or examples were copied.

### Michael Opdenacker, Root Commit: Yocto Project and OpenEmbedded Training Course

- Source: <https://rootcommit.com/pub/training/yocto/yocto-lectures.pdf>
- License: `CC-BY-SA-4.0`
- Version: revision dated 2026-06-13

Its security chapter confirmed that firewalls, block-device and filesystem encryption, extended attributes, and Linux
security modules were open subjects. Nothing was copied.

### Bootlin: Embedded Linux Security training (slides and i.MX93 FRDM lab manual)

- Source: <https://bootlin.com/training/security/>, `security-slides.pdf` and `security-imx93-frdm-labs.pdf`; sources at
  <https://github.com/bootlin/training-materials>
- License: `CC-BY-SA-3.0`
- Version: read 2026-09-08

Supplied the verification shapes the skill relies on: the signing key must reach U-Boot's control device tree as well
as the FIT recipe, and an unsigned image and a wrong-key image must fail distinguishably. It also supplied ROM-stage
verification, the build side of an A/B updater, PKCS#11 key custody, and SELinux relabel and login-mapping facts.
Nothing board-specific and no prose was copied.

### Alexandre Belloni, Bootlin: "OpenEmbedded and Yocto Project best practices"

- Source: <https://bootlin.com/pub/conferences/2020/elce/belloni-yocto-best-practices/>
- License: `CC-BY-SA-3.0`
- Version: Embedded Linux Conference Europe 2020, slides dated 2020-10-26

Informed which subjects the skill covers. Nothing was copied.

### Jérémie Dautheribes, Bootlin: "10 best practices for Yocto"

- Source: <https://bootlin.com/pub/conferences/2024/meetup/dautheribes-yocto-best-practices/>
- License: `CC-BY-SA-3.0`
- Version: Toulouse Embedded Linux, IoT & Android meetup 2024, slides dated 2024-12-19

Informed which subjects the skill covers. Nothing was copied.

### Michael Opdenacker, Bootlin: Implementing A/B System Updates with U-Boot

- Source: <https://bootlin.com/pub/conferences/2022/elce/opdenacker-implementing-A-B-system-updates-with-u-boot/>
- License: `CC-BY-SA-3.0`
- Version: Embedded Linux Conference Europe 2022, slides PDF created 2022-09-15

Informed which subjects the skill covers. Nothing was copied.

### Embetrix: meta-avb

- Source: <https://github.com/embetrix/meta-avb>
- License: `MIT`
- Version: read 2026-09-08

Its README supplied the problem statement that a dm-verity root hash creates a circular dependency between the
initramfs and rootfs build tasks, and its AVB-footer approach is described in `references/chain-of-trust-wiring.md` as
one of two options. No code or configuration was adopted.

### National Instruments: meta-selinux

- Source: <https://github.com/ni/meta-selinux>
- License: `MIT`
- Version: read 2026-09-08

A maintained downstream SELinux layer, used as the worked example of a product distribution that ships SELinux while
the dependency stays on the upstream layer. No code or configuration was copied.

### Embedded.com: "Securing a Yocto-Linux Implementation in Embedded Systems"

- Source: <https://www.embedded.com/securing-a-yocto-linux-implementation-in-embedded-systems/>
- License: `LicenseRef-Proprietary`
- Version: read 2026-09-08

The article has no author or publication date and no license notice, so all rights are reserved. It pointed to a
`meta-encrypted-storage` layer for LUKS, which the skill records as stale. Nothing was copied.

### Matt St. Onge: The Embedded Linux Security Handbook

- Source: <https://www.packtpub.com/en-us/product/the-embedded-linux-security-handbook-9781835885642>
- License: `LicenseRef-Proprietary`
- Version: first edition, Packt Publishing, April 2025

A commercially published book, all rights reserved. It supplied a named anti-pattern for LUKS automation that stores a
key file in cleartext on an unencrypted root filesystem, plus the key-recovery, non-IP exposure, and UEFI Secure Boot
subjects. Every finding was restated independently and no prose was copied.
