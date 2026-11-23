# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### Free Software Foundation: GCC manual and release notes

- Source: <https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html>,
  <https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html>, <https://gcc.gnu.org/gcc-15/changes.html>,
  <https://gcc.gnu.org/gcc-16/changes.html>
- License: `GFDL-1.3-or-later`
- Version: read 2026-11-23

The warning options, `-fanalyzer`'s scope, `-fhardened`, and the default language standards per GCC release come
from this documentation. No prose was copied.

### The Linux kernel: coding style and deprecated interfaces

- Source: <https://github.com/torvalds/linux>, `Documentation/process/coding-style.rst` and
  `Documentation/process/deprecated.rst`
- License: `GPL-2.0-only`
- Version: `b6a9fa34ce41`

The kernel's layout, brace, and declaration rules, and its list of deprecated string functions, shape the routing
and hygiene rules. No prose was copied.

### systemd: coding style

- Source: <https://github.com/systemd/systemd>, `docs/CODING_STYLE.md`
- License: `LGPL-2.1-or-later`
- Version: `e691c3d7c145`

It is the default written style for Linux userspace and supplied the `gnu17` choice and cleanup idioms. No prose
was copied.

### The Linux man-pages project

- Source: <https://man7.org/linux/man-pages/>
- License: `LicenseRef-Linux-man-pages`
- Version: 6.17

The userspace patterns for file replacement, descriptors, process spawning, signals, and wiping secrets come from
these pages. Each page carries its own permissive licence. No prose was copied.

### LLVM Project: clangd, clang-format, and clang-tidy documentation

- Source: <https://github.com/llvm/llvm-project>, `clang-tools-extra/docs/` and <https://clangd.llvm.org/>
- License: `Apache-2.0 WITH LLVM-exception`
- Version: read 2026-11-23

The clangd configuration, compilation database lookup, `--query-driver` behaviour, and the clang-format and
clang-tidy options in the tooling and clangd references come from this documentation. No prose was copied.

### Yocto Project and OpenEmbedded-Core: manuals and security flags

- Source: <https://docs.yoctoproject.org/>, and <https://git.openembedded.org/openembedded-core>,
  `meta/conf/distro/include/security_flags.inc`
- License: `CC-BY-SA-2.0-UK AND MIT`
- Version: Yocto Project 6.1 documentation

The flag injection, the `_FORTIFY_SOURCE` level, and the task logs used to confirm compiler flags come from these
sources. No prose was copied.

### Buildroot: user manual

- Source: <https://buildroot.org/downloads/manual/manual.html>
- License: `GPL-2.0-only`
- Version: 2026.08

The hardening options and the toolchain wrapper that injects them come from the manual. No prose was copied.

### Zephyr Project and Espressif: SDK documentation

- Source: <https://github.com/zephyrproject-rtos/zephyr> and <https://github.com/espressif/esp-idf>
- License: `Apache-2.0`
- Version: Zephyr `v4.5.0`, ESP-IDF `v6.1.1`

The language standard each SDK sets, and how to override it, come from these trees. No prose was copied.

### MCU SDKs and libraries: Pico SDK, Apache NuttX, FreeRTOS, CMSIS 6, and the Arduino cores

- Source: <https://github.com/raspberrypi/pico-sdk>, <https://github.com/apache/nuttx>,
  <https://github.com/FreeRTOS/FreeRTOS-Kernel>, <https://github.com/ARM-software/CMSIS_6>,
  <https://github.com/arduino/ArduinoCore-avr>
- License: `BSD-3-Clause AND Apache-2.0 AND MIT`
- Version: Pico SDK 2.3.1, NuttX 13.1.0, FreeRTOS V11.3.3, CMSIS 6.4.0, Arduino AVR core 1.8.8

The language standards these SDKs set and the C99 and C++03 baseline of shared headers come from their build files
and documentation. The Arduino AVR core states no top-level licence. No prose or code was copied.

### U-Boot: coding style

- Source: <https://github.com/u-boot/u-boot>, `doc/develop/codingstyle.rst`
- License: `GPL-2.0-or-later`
- Version: read 2026-11-23

U-Boot's deviations from kernel style and its own `.clang-format` come from this document. No prose was copied.

### Artistic Style and Cppcheck: manuals

- Source: <https://astyle.sourceforge.net/astyle.html>, <https://github.com/danmar/cppcheck>, `man/manual.md`
- License: `MIT AND GPL-3.0-only`
- Version: astyle 3.6, cppcheck `21459e9c4fb9`

The astyle option lookup order and the cppcheck configuration and suppression options come from these manuals. No
prose was copied.

### Free Software Foundation: GNU Coding Standards

- Source: <https://www.gnu.org/prep/standards/standards.html>
- License: `GFDL-1.3-or-later`
- Version: last updated 2026-04-27

It is the fallback written style for GNU-style projects and supplied the `sigaction` advice. No prose was copied.

## Third-party Sources

### LWN.net: ext4 and data durability articles

- Source: <https://lwn.net/Articles/322823/>, "ext4 and data loss" (2009), and "Ensuring data reaches disk" (2011)
- License: `LicenseRef-AllRightsReserved`
- Version: 2009-03-11 and 2011

They supplied the reasoning that durable file replacement is the application's job and needs `fsync` on the file
and its directory. The articles are copyright Eklektix, Inc., so nothing was copied.

### Research papers: LangSec, "A fork() in the road", and privilege separation

- Source: Sassaman, Patterson, Bratus, Locasto, "The Halting Problems of Network Stack Insecurity" (USENIX ;login:,
  2011); Baumann et al., "A fork() in the road" (HotOS 2019); Provos, Friedl, Honeyman, "Preventing Privilege
  Escalation" (USENIX Security 2003)
- License: `LicenseRef-NoLicenseStated`
- Version: 2011, 2019, and 2003

They supplied the advice to recognise input fully before acting on it, to prefer `posix_spawn` over `fork`, and to
split privileged work into a small separate process. The papers state no reuse licence, so nothing was copied.

### Open Source Security Foundation: Compiler Options Hardening Guide for C and C++

- Source: <https://github.com/ossf/wg-best-practices-os-developers>, `docs/Compiler-Hardening-Guides/`
- License: `CC-BY-4.0`
- Version: `816cacb72970`

It supplied the warning baseline, the hardening flag set with each flag's cost, and the `-Werror` policy. The
guidance is restated, not copied.

### Software Engineering Institute: SEI CERT C and C++ Coding Standards

- Source: <https://github.com/cmu-sei/secure-coding-standards>
- License: `CC-BY-4.0 AND MIT`
- Version: `73ee7a0dbe77`

The memory, integer, string, and error-checking rules are cited by their rule identifiers. No prose or code was
copied.

### Standard C++ Foundation: C++ Core Guidelines

- Source: <https://github.com/isocpp/CppCoreGuidelines>
- License: `LicenseRef-CppCoreGuidelines`
- Version: `5baf9fe252d0`

The resource, ownership, and initialisation rules are cited by number and restated in this skill's own words. The
licence permits personal and internal business use only, so no prose was copied.

### MISRA: MISRA C and MISRA C++ publication pages

- Source: <https://misra.org.uk/>
- License: `LicenseRef-Proprietary`
- Version: read 2026-11-23

The language version each MISRA edition targets comes from MISRA's public pages. The guidelines themselves are
sold under a proprietary licence and were not read, so nothing was copied.

### Gerard J. Holzmann: The Power of Ten

- Source: <https://spinroot.com/gerard/pdf/P10.pdf>
- License: `LicenseRef-NoLicenseStated`
- Version: read 2026-11-23

The firmware rules on heap use after initialisation, loop bounds, recursion, and checked return values come from
this paper. The paper states no licence, so no prose was copied.
