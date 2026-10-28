# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### Arm: Procedure Call Standard for the Arm Architecture

- Source: <https://github.com/ARM-software/abi-aa/blob/main/aapcs32/aapcs32.rst>
- License: `CC-BY-SA-4.0 AND LicenseRef-Arm-Patent-License`
- Version: embedded release `2025Q4`, issued 23 January 2026

Informed independently expressed ABI interpretation guidance, including argument allocation, the soft-float and VFP\
calling variants, and platform-dependent register roles. The source adds a patent grant with defensive termination. No\
prose, tables, or artwork were copied or adapted.

### Arm: Run-time ABI for the Arm Architecture

- Source: <https://github.com/ARM-software/abi-aa/blob/main/rtabi32/rtabi32.rst>
- License: `CC-BY-SA-4.0 AND LicenseRef-Arm-Patent-License`
- Version: embedded release `2025Q4`, issued 23 January 2026

Informed the independently expressed catalog of `__aeabi_*` compiler-runtime helpers and their register conventions.\
The source adds a patent grant with defensive termination. No prose, tables, or artwork were copied or adapted.

### Arm: Cortex-A Series Programmer's Guide

- Source: <https://developer.arm.com/documentation/den0013/d>
- License: `LicenseRef-Proprietary`
- Version: DEN0013D (ID012214), version 4.0, issue D, 22 January 2014

Formerly supplied a distilled programmer-model reference; the current package replaces that expression with\
independently written analysis procedures. Its Linux SVC example corroborates the system-call number register. The\
guide requires prior written permission for reproduction; no guide prose or tables are carried.

### Arm: ELF for the Arm Architecture

- Source: <https://github.com/ARM-software/abi-aa/blob/main/aaelf32/aaelf32.rst>
- License: `CC-BY-SA-4.0 AND LicenseRef-Arm-Patent-License`
- Version: embedded release `2025Q4`

Informed the independently expressed rule for reading the EABI version from the ELF header flags. No prose, tables, or\
artwork were copied or adapted.

### Linux kernel: ARM system-call entry

- Source: <https://github.com/torvalds/linux>, `arch/arm/kernel/entry-common.S`, `arch/arm/kernel/traps.c`, the ARM\
  `asm/unistd.h` header, and the arm64 compat system-call code
- License: `GPL-2.0-only AND GPL-2.0-only WITH Linux-syscall-note`
- Version: tags `v3.0`, `v3.18`, `v4.0`–`v4.4`, `v4.9`, `v4.14`–`v4.19`, `v5.4`, `v5.10`, `v5.15`, `v6.1`, and commit\
  `65ba8f34ec886ec72b2c07ddc8cf3d815c32869d`

Informed the independently expressed system-call convention: the EABI and OABI number encodings, argument and result\
registers, the ARM-private calls and the kernel versions that provide them, and the arm64 compat limits. The\
user-space `asm/unistd.h` header carries the syscall note. No code or prose is copied.

### Linux man-pages: syscall(2)

- Source: <https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/man/man2/syscall.2>
- License: `BSD-4-Clause-UC`
- Version: read 2026-10-28

Informed the even-register-pair rule for 64-bit system-call arguments under EABI. No prose is copied.

### National Security Agency: Ghidra

- Source: <https://github.com/NationalSecurityAgency/ghidra>, the ARM and Thumb SLEIGH instruction definitions and\
  `ResolveX86orX64LinuxSyscallsScript.java`; the GhidraClass advanced course on improving decompilation
- License: `Apache-2.0`
- Version: `Ghidra_12.2_build` for the source files, Ghidra 12.1.4 for the course

Informed the description of how Ghidra renders `svc` and its documented repair for system-call sites. No code or prose\
is copied.

## Third-party Sources

### mohitmishra786: low-level-dev-skills

- Source: <https://github.com/mohitmishra786/low-level-dev-skills/tree/bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608>,\
  `skills/low-level-programming/assembly-arm/SKILL.md`
- License: `MIT`
- Version: commit `bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608`

Supplied the original workflow structure linking disassembly, register interpretation, calling conventions, and frame\
recovery. Its concrete examples concern AArch64; this package's AArch32 guidance is independently written. The upstream\
notice accompanies the package in `LICENSE.upstream`.

### University of Washington CSE469 materials: ARMv7 Quick Reference

- Source: <https://courses.cs.washington.edu/courses/cse469/20wi/armv7.pdf>
- License: `LicenseRef-Unspecified`
- Version: embedded ARMv7 version 8

Formerly supplied a distilled instruction reference; the current package replaces that expression with independently\
written interpretation guidance. The publication supplies no verified redistribution grant, so its prose and tables are\
not copied.
