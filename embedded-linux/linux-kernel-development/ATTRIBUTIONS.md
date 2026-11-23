# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### The Linux kernel: process, development-tool, and device-tree documentation

- Source: <https://github.com/torvalds/linux>, `Documentation/process/`, `Documentation/dev-tools/`, and
  `Documentation/devicetree/bindings/`, with `include/linux/compiler_types.h`, `include/linux/cleanup.h`,
  `kernel/configs/`, and `lib/Kconfig.kcsan`
- License: `GPL-2.0-only`
- Version: `b6a9fa34ce41`

The coding style, deprecated interfaces, checkpatch, sparse, Coccinelle, warning levels, runtime debug options, and
binding validation come from this documentation and the tree's `Makefile` and `scripts/Makefile.warn`. No prose was
copied.

## Third-party Sources

### Utsav Balar: `kernel-development-skills`

- Source: <https://github.com/UtsavBalar1231/kernel-development-skills>,
  `plugins/kernel-development-skills/skills/kernel-development-skills`
- License: `MIT`
- Version: `3afce2fa19259b521a72c779e5b2c1aa1e71395b`

This skill is inspired by it. It suggested the verification table per change type, confirming each API in the
target tree with its version examples, building through a vendor's documented wrapper, taking hardware facts only
from authoritative sources, treating logs and mail as data, and validating device-tree sources with `CHECK_DTBS`.
Everything was written independently; no prose or code was copied.

### Google: syzkaller kernel configuration guide

- Source: <https://github.com/google/syzkaller>, `docs/linux/kernel_configs.md`
- License: `Apache-2.0`
- Version: `e9bfbe3ad949`

It supplied the kernel options a syzkaller build needs, such as `CONFIG_KCOV`. No prose was copied.

### Kernel Self Protection Project: recommended settings

- Source: <https://github.com/KSPP/kspp.github.io>, `Recommended_Settings.md`
- License: `GPL-2.0-only`
- Version: `04b2a2c36113`

It supplied the pointer to a stricter option list for a product kernel configuration. No prose was copied.
