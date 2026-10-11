# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### The Buildroot developers — Buildroot

- Source: <https://github.com/buildroot/buildroot>
- License: `GPL-2.0-or-later`
- Version: `2026.08`

The guidance on commands, configuration paths, rebuild semantics, source overrides, hook environments, package
metadata, and image generation follows the release's `Makefile`, `Config.in`, `package/pkg-*.mk`,
`support/download/dl-wrapper`, and `support/scripts/genimage.sh`. No code is copied.

### The Buildroot developers — The Buildroot user manual

- Source: <https://buildroot.org/downloads/manual/manual.pdf>
- License: `GPL-2.0-only`
- Version: 2026.05, generated from Git revision `313414b92c`

The external-toolchain restrictions, wrapper diagnostics, SDK and environment setup, and legal-info guidance are
built on the manual. No prose is copied.

## Third-party Sources

### Bootlin — Buildroot system development training

- Source: <https://bootlin.com/training/buildroot/>
- License: `CC-BY-SA-3.0`
- Version: slides updated 2026-06-09; BeagleBone Black and STM32MP157 practical labs dated 2026-06-08

The slides' framing of reproducibility as experimental and their SDK shell material shaped the skill's qualified
reproducibility claims and isolated cross-build environments. The labs' step of recording source identity in the
root filesystem shaped the board-provenance example. No slide prose or lab exercise is copied.

### The genimage contributors — genimage

- Source: <https://github.com/pengutronix/genimage>
- License: `GPL-2.0-only`
- Version: `v20`

Its README and image implementation informed the distinction between filesystem construction and partition
assembly. The illustrative layout uses its configuration interface; no implementation is vendored.

### Ciro Santilli — Linux Kernel Module Cheat

- Source: <https://github.com/cirosantilli/linux-kernel-module-cheat>, `buildroot_override` and the README's
  Buildroot and package sections
- License: `GPL-3.0-only`
- Version: `2924ab723e33ec4be531857c214f6770dfb1d4a8`

Supplied the local-iteration, image-capacity, and overlay and module-metadata cases. No wrapper or Buildroot
change was adopted.

### Wu Zhangjin and the TinyLab community — Linux Lab

- Source: <https://github.com/tinyclub/linux-lab>, `Makefile`
- License: `LicenseRef-Linux-Lab`
- Version: `cbd1cbd2e078fb5c164002adc1e56fdaeb101910`

The license is GPL version 2 for non-commercial users, and commercial users need a separate license from the
author. Its rootfs selection illustrated why a successful build does not identify the image a runner consumes.
Nothing was adapted.

### Packt — Mastering Embedded Linux Programming, Second Edition, example code

- Source: <https://github.com/PacktPublishing/Mastering-Embedded-Linux-Programming-Second-Edition>, Chapter 6
- License: `MIT`
- Version: `66a30f725e226af4bcb97c22ec41364fa770e59f`

The local hello-world package and the genimage partition layout supplied cases for local source inputs and for
filesystem-versus-partition capacity. No board files or scripts were copied.
