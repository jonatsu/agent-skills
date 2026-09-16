# Attributions

## Current Package

- Author: Joonas Onatsu
- License: MIT
- Scope: Buildroot development and integration guidance, with independently written repair instructions and hook examples.

The 2026-09-07 repair retained useful task boundaries and technical interface facts while replacing the source-corresponding
external-toolchain, SDK, legal-info, reproducibility, and board-provenance explanations. The sources below informed the
guidance and selected failure cases. No third-party wrapper, lab script, or prose passage was copied into this repair.
This record acknowledges influence even where the wording and implementation are independent.

**These records are permanent.** A source entry is not closed by a later repair that replaces the material it
describes. Independent replacement changes what the current revision contains; it does not retract the revisions that
carried the adapted material, and those remain in this repository's history. Keep every entry — in the past tense once
the material is gone — so that a reader who reaches an older revision can still establish what the relationship was.

## First-Party Technical Sources

- **The Buildroot developers — Buildroot user manual 2026.05**, generated 2026-06-08 from revision `313414b92c`.
  The supplied PDF declares GPL-2.0. Historical port records establish its influence on external-toolchain restrictions,
  wrapper diagnostics, SDK/environment setup, and legal-info. The original brief's CC BY-SA/GFDL label was incorrect.
  PDF SHA-256: `155eacba5e65511fb27f2bca502103dd3f9914dea9d4e829eecbe6654bc27144`.
- **The Buildroot developers — [Buildroot 2026.08](https://github.com/buildroot/buildroot/tree/2026.08)**.
  Release code and its manual were checked for command behavior, configuration paths, rebuild semantics, source overrides,
  hook environments, package metadata, and image generation. The release source includes GPL-2.0 terms; the manual
  identifies GPL-2.0. These interfaces were verified from `Makefile`, `Config.in`, `package/pkg-*.mk`,
  `support/download/dl-wrapper`, `support/scripts/genimage.sh`, and the corresponding manual chapters.
- **The genimage contributors — [genimage v20](https://github.com/pengutronix/genimage/tree/v20)**.
  Its README and image implementation informed the distinction between filesystem construction and partition assembly.
  The project declares GPL-2.0. The illustrative layout uses its configuration interface; no implementation is vendored.

Use these projects' release-matched documentation and code to resolve technical disagreements with third-party examples.

## Bootlin Training Material

**Bootlin, Buildroot system development training**, supplied PDFs from June 2026, declaring CC BY-SA 3.0:

- Slides updated 2026-06-09: slide 273 frames reproducibility as experimental; slides 283–284 explain the SDK shell.
  The repair retains the need to qualify reproducibility claims and isolate cross-build environments. It uses the target
  release's implementation for the actual constraints rather than turning a slide's goal into a universal guarantee.
  SHA-256: `1676b8dc1df8a661a92969647dee533061e0ba1e28b377bf37357fd53d60c81a`.
- BeagleBone Black and STM32MP157 practical labs, dated 2026-06-08, page 13: record source identity in the rootfs.
  This is a plausible influence on the old provenance example; the exact original authoring chain is not established.
  The repaired guidance separates deterministic image metadata from volatile execution timestamps.
  BeagleBone PDF SHA-256: `f24b459cc7a3dc5e0e44190bfc3858f21a8fc6dd1850059bd4387d11b7aa8dd6`.
  STM32MP157 PDF SHA-256: `b21670ec87303042e5dae33bb0cde9b07e4bed8104bc73311a2dd1e4ad369c26`.

[Training source and publication information](https://bootlin.com/training/buildroot/).
These are acknowledged idea sources; the exercises and slide prose are not bundled.

## Third-Party Cases Used During the Repair

- **Ciro Santilli, [Linux Kernel Module Cheat](https://github.com/cirosantilli/linux-kernel-module-cheat/tree/2924ab723e33ec4be531857c214f6770dfb1d4a8)**,
  revision `2924ab723e33ec4be531857c214f6770dfb1d4a8`, root license text GPL version 3.
  `buildroot_override` and the README's Buildroot/package sections supplied local-iteration, image-capacity, and
  overlay/module-metadata cases. Their mechanisms were checked against first-party sources. No wrapper or fork-specific
  Buildroot change was adopted.
- **Wu Zhangjin / TinyLab community, [Linux Lab](https://github.com/tinyclub/linux-lab/tree/cbd1cbd2e078fb5c164002adc1e56fdaeb101910)**,
  revision `cbd1cbd2e078fb5c164002adc1e56fdaeb101910`.
  `Makefile` rootfs selection illustrated why a successful build does not identify the image consumed by a runner.
  Its `COPYING` adds a commercial-use licensing requirement to GPL-v2 text. No implementation or expression was adapted;
  the skill independently asks the consuming project to verify its actual artifact selection.
- **Packt, [Mastering Embedded Linux Programming, Second Edition code](https://github.com/PacktPublishing/Mastering-Embedded-Linux-Programming-Second-Edition/tree/66a30f725e226af4bcb97c22ec41364fa770e59f)**,
  revision `66a30f725e226af4bcb97c22ec41364fa770e59f`, repository license MIT, copyright Packt 2017.
  Chapter 6's local hello-world package and genimage partition layout supplied comparison cases for local source inputs
  and filesystem-versus-partition capacity. The old board files and scripts were not transplanted. This repository's
  license is not asserted to cover the book or override notices in individual source files.
