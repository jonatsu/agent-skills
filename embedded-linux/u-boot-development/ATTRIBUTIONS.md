# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### The U-Boot developers — U-Boot

- Source: <https://github.com/u-boot/u-boot>, chiefly `cmd/nvedit.c`, `tools/env/fw_env.c`, `env/`,
  `boot/image-fit-sig.c`, `tools/image-host.c`, `common/main.c`, `common/autoboot.c`, `drivers/bootcount/`,
  `common/spl/`, and the `doc/` tree
- License: `GPL-2.0-or-later`
- Version: `v2025.10`

The environment, FIT signature, boot flow, bootcount, control device tree, and SPL guidance is built on the release's
source and documentation: its failure cases, persistence and verification boundaries, and board-specific limits. No
upstream implementation is vendored, and no board skeleton is copied.

## Third-party Sources

### Michael Opdenacker, Bootlin — Implementing A/B System Updates with U-Boot

- Source: <https://bootlin.com/pub/conferences/2022/elce/opdenacker-implementing-A-B-system-updates-with-u-boot/>
- License: `CC-BY-SA-3.0`
- Version: Embedded Linux Conference Europe 2022, slides PDF created 2022-09-15

Formerly adapted: earlier revisions closely followed the deck's topics and examples on partition-flag selection,
extlinux boot, bootcount, environment access from Linux, and partition management. The deck still shapes the current
treatment of slot activation, health confirmation, and interrupted writes; none of its commands, diagrams, or sequence
is copied.
