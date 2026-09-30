# Attributions

## Current skill

- Skill: `embedded-linux-debugging`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original text, plus material moved from `embedded-linux-bringup` on 2026-09-30

## Material moved from embedded-linux-bringup

`references/tracing-and-profiling.md` began as `embedded-linux-bringup`'s `references/debugging.md`. Its kgdb, oops,
crash-dump, and gdbserver sections were folded into `references/kernel-debugging.md` and
`references/userspace-and-yocto.md`. The provenance that file carried moves with it:

- **Bootlin debugging training slides** (CC BY-SA 3.0, updated 2026-06-09; SHA-256
  `5caad435377baa735a9ff653e60c0c2dc793c8915e7e6541285eb92284906977` for the inspected copy), pages 198, 200–204, and
  207–208: perf selection, probes, and flame graphs. The prose was independently replaced in `embedded-linux-bringup`'s
  2026-09-07 repair; subject-selection influence remains acknowledged.
- **heyu-233/linux-embedded-dev** (MIT, Copyright (c) 2026 heyu-233, revision
  `53e7526e3ba3ffe4018845a58af328f897ffd60a`): its profiling playbook influenced the retained guidance on profile
  interpretation. The license text is in [LICENSE.upstream](LICENSE.upstream).

`embedded-linux-bringup`'s `ATTRIBUTIONS.md` holds the full history of both.

## Sources whose reading shaped the new text

No text was copied from these; facts are restated with their source named in each reference.

- Linux v7.2: `Documentation/admin-guide/kernel-parameters.txt`, `bug-hunting.rst`, `reporting-issues.rst`,
  `sysctl/kernel.rst`, `Documentation/process/debugging/kgdb.rst` and `gdb-kernel-debugging.rst`, and
  `scripts/decode_stacktrace.sh` and `scripts/faddr2line`.
- `agent-proxy` 1.94 (git.kernel.org), OpenOCD master's manual and `tcl/target/bcm2711.cfg`.
- U-Boot v2026.07: `doc/develop/gdb.rst`, `doc/usage/cmd/bdinfo.rst`, `doc/develop/crash_dumps.rst`, `doc/develop/spl.rst`.
- systemd v262's `systemd-coredump`, `coredump.conf`, and `coredumpctl` manuals.
- Yocto Project 6.0 "Wrynose" manuals and OpenEmbedded-Core, and Raspberry Pi's serial and `config.txt` documentation.

The research notes, with URLs and commits, are in agent-setup's `docs/research/embedded-debugging/`.
