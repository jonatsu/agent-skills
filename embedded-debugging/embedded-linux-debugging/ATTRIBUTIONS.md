# Attributions

- Author: Joonas Onatsu
- License: `MIT`

The package adapts material from linux-embedded-dev, whose MIT license requires its notice to travel with the
material; keep `LICENSE.upstream` with the skill.

## First-party Sources

### The Linux kernel developers: Linux kernel

- Source: <https://github.com/torvalds/linux>, chiefly `Documentation/admin-guide/` (`kernel-parameters.txt`,
  `bug-hunting.rst`, `reporting-issues.rst`, `sysctl/kernel.rst`), `Documentation/process/debugging/` (`kgdb.rst`,
  `gdb-kernel-debugging.rst`), `scripts/decode_stacktrace.sh`, and `scripts/faddr2line`
- License: `GPL-2.0-only`
- Version: `v7.2`

The oops and panic decoding, early-boot output, kgdb and kdb, and sysctl guidance in `references/kernel-debugging.md`
and `references/userspace-and-yocto.md` is built on these documents and scripts. Facts are restated in original words;
nothing was copied.

### The U-Boot developers: U-Boot

- Source: <https://github.com/u-boot/u-boot>, `doc/develop/gdb.rst`, `doc/usage/cmd/bdinfo.rst`,
  `doc/develop/crash_dumps.rst`, and `doc/develop/spl.rst`
- License: `GPL-2.0-or-later`
- Version: `v2026.07`

`references/u-boot-debugging.md` is built on the relocation, `bdinfo`, crash-dump, and SPL debugging documentation.
Nothing was copied.

### The Yocto Project: Yocto Project documentation

- Source: <https://docs.yoctoproject.org/6.0/>, the reference, SDK, and migration manuals
- License: `CC-BY-SA-2.0-UK`
- Version: 6.0 (Wrynose)

The guidance on getting debug symbols onto the host (debug packages, SDK, `debuginfod`) and on the removal of
`debug-tweaks` in `references/userspace-and-yocto.md` is built on the manuals. Facts are restated in original words;
nothing was copied.

## Third-party Sources

### heyu-233: linux-embedded-dev

- Source: <https://github.com/heyu-233/linux-embedded-dev>, profiling playbook
- License: `MIT`
- Version: `53e7526e3ba3ffe4018845a58af328f897ffd60a`

The profiling playbook supplied the starting point for the guidance on interpreting profiles in
`references/tracing-and-profiling.md`.

### Bootlin: Linux debugging, profiling and tracing training

- Source: <https://bootlin.com/doc/training/debugging/debugging-slides.pdf>
- License: `CC-BY-SA-3.0`
- Version: slides updated 2026-06-09

The slides shaped the perf probe selection and flame graph guidance in `references/tracing-and-profiling.md`. No slide
prose, sequence, lab, or code is copied.
