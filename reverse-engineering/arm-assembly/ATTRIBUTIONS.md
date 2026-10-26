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
independently written analysis procedures. The guide requires prior written permission for reproduction; no guide prose\
or tables are carried.

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
