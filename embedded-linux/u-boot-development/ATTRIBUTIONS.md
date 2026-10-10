# Attributions

## Current package

- Skill: `u-boot-development`
- Current author: Joonas Onatsu
- Current declared license: MIT, unchanged by the 2026-09-07 repairs
- Repair baseline: [U-Boot v2025.10](https://github.com/u-boot/u-boot/tree/v2025.10)

The replacement explanations and helper are independently expressed. The source influence below is retained even where
no wording is copied. This record does not claim that independently expressed content erases obligations for any
historical adaptation. The original adoption path remains partly unresolved.

**These records are permanent.** A source entry is not closed by a later repair that replaces the material it
describes. Independent replacement changes what the current revision contains; it does not retract the revisions that
carried the adapted material, and those remain in this repository's history. Keep every entry — in the past tense once
the material is gone — so that a reader who reaches an older revision can still establish what the relationship was.
That applies with particular force here, where the original adoption path is only partly known.

## U-Boot implementation and documentation influence

Authors include Wolfgang Denk, DENX Software Engineering, Google/Chromium OS contributors, NVIDIA, Red Hat, Linaro,
Joe Hershberger/National Instruments, Semihalf, TI contributors and other U-Boot contributors named in the files.
The exact baseline is tag v2025.10. Its source archive has SHA-256
`5414ee86562abc5ed524c6dc5e092511ad281441020a88e7027de6e83fd16116`.

These sources changed the repair's decisions, failure cases and explanations; they were not merely consulted to check
spelling. Paths below are relative to that pinned tree:

| Sources                                                                                                            | Retained influence                                                                                            |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| `cmd/nvedit.c`, `tools/env/fw_env.c`, `env/env.c`, `env/nowhere.c`, `env/Kconfig`, `env/flags.c`                   | Export/import formats, replacement versus merge, persistence failures, backend and mutation-policy boundaries |
| `boot/image-fit-sig.c`, `tools/image-host.c`, `tools/mkimage.c`, `doc/usage/fit/signature.rst`                     | FIT signing declaration, required keys in trusted control DT, packaging and negative verification cases       |
| `common/main.c`, `common/autoboot.c`, `boot/fdt_support.c`                                                         | Returning boot commands, interruption versus prompt access, final bootargs fixups                             |
| `doc/usage/cmdline.rst`, `cmd/net.c`, `include/config_distro_bootcmd.h`, `cmd/part.c`                              | Failure sequencing, network side effects, per-prefix selection and multiple bootable partitions               |
| `include/bootcount.h`, `drivers/bootcount/bootcount_env.c`, `drivers/bootcount/bootcount_fs.c`                     | Strict threshold and backend-specific persistence/confirmation                                                |
| `doc/develop/devicetree/control.rst`, `dts/Kconfig`, `drivers/core/uclass.c`                                       | Actual control-DT provider, live/flat representations and bound/probed distinction                            |
| `common/spl/Kconfig`, `common/spl/spl.c`, `configs/imx8mp_evk_defconfig`, `configs/sama5d3_xplained_mmc_defconfig` | Stage localization and distinct board-specific memory/image limits                                            |
| `doc/board/ti/k3.rst`                                                                                              | TI K3 lifecycle and customer-key distinctions                                                                 |

Most implementation sources above declare `GPL-2.0+`; the K3 guide declares `GPL-2.0+ OR BSD-3-Clause`.
[Licenses/README](https://github.com/u-boot/u-boot/blob/v2025.10/Licenses/README) explains per-file terms; the tree's
[GPL-2.0 text](https://github.com/u-boot/u-boot/blob/v2025.10/Licenses/gpl-2.0.txt) was inspected. The repair does not
vendor upstream implementation or transplant an upstream board skeleton. Command/schema identifiers reflect U-Boot's
interfaces; new explanatory text and command templates were written for the repaired contracts.

## Bootlin A/B material and historical uncertainty

- Author: Michael Opdenacker, Bootlin
- Work: *Implementing A/B System Updates with U-Boot*, Embedded Linux Conference Europe 2022
- Source: [Bootlin publication](https://bootlin.com/pub/conferences/2022/elce/opdenacker-implementing-A-B-system-updates-with-u-boot/)
- Inspected local PDF SHA-256: `f3a0a7d298f17ed958429706b3880427593eb263d90698922da1f92ae85dcc31`
- Declared license: Creative Commons BY-SA 3.0, copyright 2004–2022 Bootlin (PDF title page)

Pages 10–16 and 19–25 closely correspond to the old skill's partition-flag selection, extlinux boot, bootcount,
Linux environment access and partition-management topics/examples. The comparison does not establish who adopted what
or when. The historical package changed details and also introduced errors not present in the slides. Neither similarity
nor a missing attribution file alone establishes copying.

The 2026-09-07 comparison influenced the repair's treatment of slot activation, health confirmation and interrupted
writes. That influence is acknowledged here. The old universal partition-flag recipe was replaced with an independently
written contract requiring the selected updater's actual on-media protocol. The repair does not import the slides'
example commands, diagrams or sequence as a new adaptation, and does not represent rewording as permission to relicense.

Commits `26cc26d04c334557be35826fc5c40444dbf9eb6e` and `0d2bf671b519283beac24d40fd1382dffd91ee82` in the
author's private configuration repository introduced the skill and its references as a port from the author's
Copilot configuration. The old port brief calls U-Boot original but also instructs authors generally to reword restricted
material and remove attribution framing. Those statements do not resolve actual derivation. The named original
`copilot/skills/uboot-dev` package was not available at its recorded path during repair; targeted filename/content
searches in the remaining `mystuff` tree did not locate it.

This bounded investigation establishes the known repair influence and preserves historical uncertainty. It does not
claim a comprehensive copyright audit or authorize relicensing. If the original drafts or creation traces establish
copied/adapted material, reassess the affected passages and preserve their actual applicable license/notices before
further adaptation or distribution decisions. No generic GPL or CC license file is supplied as a substitute for that
source-relationship decision.

## Verification-only sources

The Agent Skills specification was used to verify string-valued metadata. NXP AN4547 Rev. 0, section 2.2 (2012), was used
only to verify a HABv3 counterexample to universal non-recoverability; no NXP provisioning procedure or expression was
adopted. These sources do not establish behavior on an untested board or a different security lifecycle.
