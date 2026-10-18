# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### The Yocto Project: meta-security

- Source: <https://git.yoctoproject.org/meta-security>, chiefly `classes/check_security.bbclass`,
  `recipes-scanners/`, `recipes-compliance/`, `recipes-core/images/`, `kas/`, and `lib/oeqa/runtime/cases/`
- License: `MIT`
- Version: `b13f1705d723650de61277670c8a76aadea4cfdd` (tip of the `scarthgap` branch)

The guidance on running the layer's scanners and auditors, on its `oeqa` runtime security suites, and on what a green
suite does and does not prove is built on the layer's classes, recipes, and test cases. No code is copied.

### OpenEmbedded: openembedded-core

- Source: <https://git.openembedded.org/openembedded-core>, chiefly `meta/conf/distro/include/security_flags.inc`,
  `meta/classes-recipe/rootfs-postcommands.bbclass`, `meta/classes-recipe/image_types.bbclass`, and
  `meta/lib/oe/package_manager/`
- License: `MIT`
- Version: `b4f06303e55c7270a8482a610927a1c41d5dbf9c` (`scarthgap` branch)

The exemption list, the deployed `testdata.json` and manifest, the tar image type, and the removal of the package
database are described from these files. No code is copied.

### Brian Davis and contributors: checksec.sh

- Source: <https://github.com/slimm609/checksec.sh>, `checksec`
- License: `BSD-3-Clause`
- Version: tag `2.6.0`, the release `meta-security` packages

The option syntax, the JSON keys, and how the FORTIFY result is computed are described from the script. No code
is copied.

## Third-party Sources

### Michael Opdenacker, Root Commit: "Securing Yocto Built Systems"

- Source: <https://rootcommit.com/pub/conferences/2025/elce/yocto-security/yocto-security.pdf>
- License: `CC-BY-SA-4.0`
- Version: Embedded Linux Conference Europe 2025, slides dated 2025-08-26

Surfaced the subject of auditing a built image with Lynis and OpenSCAP, and the claim that the scanners in
`meta-security` are broken. No wording, structure, or examples were copied.

### Bootlin: Embedded Linux Security training

- Source: <https://bootlin.com/training/security/>, `security-slides.pdf`; sources at
  <https://github.com/bootlin/training-materials>
- License: `CC-BY-SA-3.0`
- Version: read 2026-09-08

Gave background on what an audit of an embedded image is expected to cover. No prose, sequence, or example was copied.
