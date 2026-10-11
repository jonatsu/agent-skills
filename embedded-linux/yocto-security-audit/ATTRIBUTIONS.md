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
