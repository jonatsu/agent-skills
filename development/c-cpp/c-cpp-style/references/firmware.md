# MCU Firmware Standards

Use this file for code that runs on a microcontroller under an SDK or RTOS, not under Linux. It answers four
questions. Which standard does each SDK build with, and how is it set? Which language does each MISRA edition target?
What does a freestanding target lack? Which hardening flags apply without an MMU? Facts come from each project's
files at the pins named below. A note marked "inference" is a reading of those files, not a statement in them.

## Contents

- Standard per SDK
- Setting the Standard Explicitly
- MISRA Editions
- Freestanding Constraints
- Headers Shared Across SDKs
- Hardening Without an MMU

## Standard per SDK

An SDK's default is a build-file value, not a requirement, unless the details below say required. Read the tree's
build file before trusting a row.

| SDK or RTOS           | Pin                               | C                                   | C++                                   |
| --------------------- | --------------------------------- | ----------------------------------- | ------------------------------------- |
| Zephyr                | `v4.5.0` (`41d10b597304`)         | `c17` default, `c23` optional       | `c++11` default, 98 to 26 selectable  |
| ESP-IDF 6.x           | `v6.0` (`662a3be35475`), `v6.1.1` | `gnu23`                             | `gnu++26`, exceptions off by default  |
| ESP-IDF 5.x           | `v5.5.4` (`735507283d5b`)         | `gnu17`                             | `gnu++2b`                             |
| Raspberry Pi Pico SDK | `2.3.1` (`079c6f390236`)          | `CMAKE_C_STANDARD 11`               | `CMAKE_CXX_STANDARD 11`               |
| STM32Cube             | no ST repository states one       | CubeMX-generated CMake wants C11+   | not stated                            |
| Arduino AVR core      | `1.8.8` (`86df345b3cf4`)          | `gnu11`                             | `gnu++11 -fno-exceptions`             |
| Arduino Renesas core  | `1.6.0` (`424e86eff92d`)          | `gnu11`                             | `gnu++17 -fno-rtti -fno-exceptions`   |
| Apache NuttX          | `nuttx-13.1.0` (`2b5c0de5e933`)   | no `-std` found (compiler default)  | `gnu++17`, or `gnu++20` with `LIBCXX` |
| FreeRTOS Kernel       | `V11.3.3` (`89592801dd8b`)        | core is C90-clean, needs `stdint.h` | not stated                            |
| Arm CMSIS 6           | `v6.4.0` (`af1b110e46a1`)         | C99 headers                         | C++03 headers                         |

Details behind the rows:

- Zephyr 4.5 requires C17 or higher and removed the C99 and C11 options. Its build uses strict `c17`. It switches to
  `gnu17` only when `CONFIG_GNU_C_EXTENSIONS` is set. Its bundled SDK toolchain (sdk-ng `v1.0.1`) is GCC 14.3.0.
- ESP-IDF 6.x builds chip targets with `gnu23` and `gnu++26`. Its Linux host target picks the newest C standard the
  host compiler supports. ESP-IDF 5.x used `gnu17` and `gnu++2b`.
- The Pico SDK sets both standards in its top-level `CMakeLists.txt`. Inference: a user project can override them.
- STM32Cube: the only evidence is a third-party quote of CubeMX 6.12.1 output, which fails configuration when
  `CMAKE_C_STANDARD` is below 11. Treat C11 as the floor, and read the generated files in the project.
- NuttX: the missing C `-std` is an inference from reading `arch/arm/src/common/Toolchain.defs`. Confirm the real flag
  in the build log.
- FreeRTOS: the kernel imposes no standard beyond C90 plus `stdint.h`. The RP2040 port sets C11 and C++17.
- CMSIS 6 claims conformance to MISRA C:2012 without claiming compliance. Its checks are against C:2012.
- Mbed OS 6.17 built `gnu11` and `gnu++14 -fno-rtti`, and it is end of life.

Reading (inference): vendor SDKs that bundle a modern toolchain have moved to C17 and beyond. SDKs that accept many
third-party compilers, and portable library code, stay at C99 or lower. C++ defaults sit lower than C defaults.

## Setting the Standard Explicitly

State the standard in the project's own build files, so a toolchain or SDK update cannot change the language. The
default for new firmware comes from the `SKILL.md` section "Language Standard". Move it only as the list below says.

- Zephyr: select the standard through Kconfig. Set `CONFIG_STD_CPP17` for C++17, because the default is C++11, and
  `CONFIG_STD_C23` for C23. The C default already satisfies C17.
- ESP-IDF 6.x: the SDK builds `gnu23`. To keep a component at `gnu17`, add `-std=gnu17` in that component's
  `CMakeLists.txt`, as the ESP-IDF C guide shows. Pin C++ lower if the code must stay portable.
- Pico SDK: set `CMAKE_C_STANDARD` and `CMAKE_CXX_STANDARD` in the project's `CMakeLists.txt`, since the SDK defaults
  both to 11.
- STM32Cube: the generated top-level `CMakeLists.txt` is tool-owned and marked "do not modify". Put the standard in
  the user-editable toolchain file or in the project's own CMake (inference).
- Arduino: the standard lives in each core's `platform.txt`. Unverified: how a sketch overrides it; read the Arduino
  build documentation before editing.
- NuttX: set `CONFIG_CXX_STANDARD` for C++. For C, pass `-std` through the toolchain flags and check the compiler
  command line (inference).
- FreeRTOS and CMSIS: no setting exists, because the application chooses.

Confirm every change by reading the compile command in the build output or `compile_commands.json`. An unset
standard compiles at the compiler's default, which differs between GCC releases.

## MISRA Editions

MISRA text is paywalled, and this skill carries none. Do not quote or reconstruct rule text. Ask for the project's
rule list or checker configuration, and use this table only to pick `-std`.

| Edition        | Language it targets                  | Source                                    |
| -------------- | ------------------------------------ | ----------------------------------------- |
| MISRA C:2012   | C99, with guidelines kept for C90    | misra.org.uk, published 18 March 2013     |
| MISRA C:2023   | C90, C99, C11, and C18               | misra.org.uk, published April 2023        |
| MISRA C:2025   | C11 and C18, and earlier             | misra.org.uk, published March 2025        |
| MISRA C++:2023 | C++17 (ISO/IEC 14882:2017)           | misra.org.uk, published October 2023      |
| MISRA C++:2008 | C++03 (inference from the 2008 date) | superseded by C++:2023                    |
| AUTOSAR C++14  | C++14                                | obsolete; MISRA C++:2023 is the successor |

- Under MISRA C:2012, build with strict `-std=c99`. Under C:2023 or C:2025, use strict `-std=c11` or `-std=c17`.
  Strict means no GNU extensions, so write `c`, not `gnu`.
- No MISRA C edition covers C23. A MISRA forum answer says C:2025 did not extend to the newer standard and that work
  on C23 had started. Keep MISRA code off `gnu23`.
- Under MISRA C++:2023, stay at C++17.
- Zephyr publishes a free subset of MISRA C:2012 rules with CERT C cross references. Use it as the model for adopting
  a subset. The Power of Ten is a short readable rule set, and `SKILL.md` already uses it.

## Freestanding Constraints

A freestanding target has no hosted library to rely on. U-Boot builds with `-ffreestanding -fno-builtin` and brings
its own `printf` and string helpers.

- Check that each header and function exists in the SDK's libc before using it.

- C11 makes three features optional, and a bare-metal toolchain may lack them. Test the macro before use:

  | Feature                 | Macro defined when it is absent |
  | ----------------------- | ------------------------------- |
  | Atomics (`_Atomic`)     | `__STDC_NO_ATOMICS__`           |
  | Threads (`<threads.h>`) | `__STDC_NO_THREADS__`           |
  | Variable-length arrays  | `__STDC_NO_VLA__`               |

  Avoid all three unless the target documents support. The `SKILL.md` warning set already flags VLAs.

- Gate C23 features on `__STDC_VERSION__`. Avoid `#embed` and `_BitInt` where portability matters, and every C23
  feature on a toolchain that supports only C11 or C17.

- In C++, avoid coroutines (they allocate frames), `std::regex`, and library headers that assume a hosted libstdc++.
  The cppreference page `w/cpp/freestanding` lists what a freestanding implementation must provide. Unverified: read
  it before choosing a library facility.

- Take the exceptions and RTTI default from the `SKILL.md` section "Errors in C++". A project that enables them in its
  SDK configuration keeps them.

## Headers Shared Across SDKs

A header that several SDKs or compilers include must stay at the oldest consumer's language. CMSIS headers are C99 and
C++03-safe, and the FreeRTOS kernel is C90-clean.

- Write headers in C99 with C++ guards. Avoid `_Atomic`, C11 threads, and variable-length arrays.
- Write every prototype with `(void)` for no parameters. C23 makes `int f()` mean `int f(void)`, and older standards
  read it as unspecified.
- Include `<stdbool.h>` and `<stdint.h>`, and never define `bool`, `true`, or `false` yourself. GCC 15's C23 default
  makes `bool`, `true`, `false`, `nullptr`, and `thread_local` keywords, so `typedef int bool;` is an error there.
- Reserve C++ types for C++-only headers. A C-visible header keeps the `extern "C"` rule from `SKILL.md`.

## Hardening Without an MMU

The OpenSSF guide says its tables are "primarily applicable to compiling user space code in GNU/Linux". It says kernel
and firmware have their own flag sets, and for firmware it notes only a size cost, for `-ftrivial-auto-var-init`.
The sorting below is inference from what each flag acts on. Confirm it against the toolchain documentation.
`references/hardening.md` explains each flag.

Flags that act on generated code and still apply:

- The warning set and the `-Werror=<warning>` forms from `SKILL.md`.
- `-fstack-protector-strong`. U-Boot, a freestanding program, enables it per board. The runtime must supply the canary
  value and the failure handler (inference), so a bare-metal link can fail without them. Check the RAM and flash cost.
- `-fno-delete-null-pointer-checks`, `-fno-strict-overflow`, and `-fno-strict-aliasing`.
- `-ftrivial-auto-var-init=zero`, at a size cost the OpenSSF guide notes for embedded targets.

Flags to treat as unproven on an MCU:

- `-fstack-clash-protection`. It targets guard-page schemes, which a device without an MMU may not have. Verify first.
- `-fcf-protection=full` and `-mbranch-protection=standard`. The guide names them for x86_64 and aarch64 only, and no
  source names an MCU equivalent.

Flags that do not apply to a bare-metal image, because they act on the dynamic loader or the C library:

- Position-independent executables, `-z relro`, `-z now`, `-z noexecstack`, `-z nodlopen`, and `--as-needed`.
- `_FORTIFY_SOURCE`, which needs glibc. Do not expect it to work on newlib or musl.
- `-D_GLIBCXX_ASSERTIONS`, which needs libstdc++. libc++ has its own hardening mode.
- Runtime ASLR and kernel hardening, which belong to a running Linux.

Sanitizers do not run on the MCU. Run them on the host build through `c-cpp-testing`.
