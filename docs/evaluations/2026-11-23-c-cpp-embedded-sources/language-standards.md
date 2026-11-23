# Language standards for embedded C and C++: evidence and proposed defaults

Read date: 2026-11-23. Every GitHub fact was read through `gh api repos/OWNER/REPO/contents/PATH?ref=REF` at the pinned
ref. "Source states" marks text or code read at the pin. "Inference" marks my reading of it.

Pins use the first 12 characters of the commit SHA. A tag name alone is not a pin.

## Summary

1. The draft default for embedded Linux C (`gnu17`) matches the evidence. The draft default for C++ (C++20) is ahead of
   what most projects declare: the common floor is C++17.
2. The user's experience holds for libraries, legacy SDKs and MISRA work, but current firmware SDKs have moved. Zephyr
   4.5 requires C17 or higher. ESP-IDF 6.x defaults to `gnu23` and `gnu++26`. Mbed OS (gnu11, gnu++14) is end of life.
   FreeRTOS and CMSIS headers still aim at C90/C99 and C++03.
3. Every toolchain currently supported by Yocto, Buildroot LTS and OpenWrt ships GCC 13 or newer, so C17 and most of
   C++20 are available there.

## Q1. Toolchains in embedded Linux

### Q1a. GCC per build system

| Build system and release                | GCC (source states)                                                                       | Pin and file                                                                                                                                             | Release status (source states)                                                                                                                     |
| --------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Yocto 5.0 scarthgap                     | `GCCVERSION ?= "13.%"`, recipe `gcc_13.5.bb`; binutils 2.42, glibc 2.39                   | openembedded-core tag `yocto-5.0.21` = `b4f06303e55c`, `meta/conf/distro/include/tcmode-default.inc`; same value on branch `scarthgap` at `fc4316861bec` | LTS until April 2028 (wiki.yoctoproject.org/wiki/Releases, read 2026-11-23)                                                                        |
| Yocto 6.0 wrynose                       | `GCCVERSION ?= "15.%"`, recipe `gcc_15.3.bb`; glibc 2.43                                  | tag `yocto-6.0.4` = `0f03c732a0a2`; branch `wrynose` at `16a03ed6c2db`                                                                                   | LTS until April 2030 (same wiki page)                                                                                                              |
| Yocto 6.1 blacksail                     | `GCCVERSION ?= "16.%"`, recipe `gcc_16.2.bb`; glibc 2.44                                  | tag `yocto-6.1` = `419c1b0f1ed0`; branch `blacksail` at `5b458838c126`                                                                                   | Support until April 2027 (same wiki page)                                                                                                          |
| Yocto 4.0 kirkstone, for context        | `GCCVERSION ?= "11.%"`, recipe `gcc_11.5.bb`                                              | tag `yocto-4.0.31`, same file                                                                                                                            | Listed as EOL (4.0.33 released February 2026)                                                                                                      |
| Buildroot LTS 2025.02.x                 | Choices 12.5.0, 13.4.0, 14.4.0. Default `BR2_GCC_VERSION_13_X` (13.4.0)                   | tag `2025.02.20` = `2f9129e7909b`, `package/gcc/Config.in.host`                                                                                          | The LTS is 2025.02, supported three years; the next LTS is 2027.02 (`docs/manual/release-engineering.adoc` at `2026.08.2`; buildroot.org/lts.html) |
| Buildroot 2026.02.3 (not LTS)           | Choices 13.4.0, 14.3.0, 15.2.0. Default 14.x (14.3.0)                                     | tag `2026.02.3` = `679b9ead7620`, same file                                                                                                              | Non-LTS                                                                                                                                            |
| Buildroot 2026.08.2 (latest stable)     | Choices 14.4.0, 15.3.0, 16.2.0. Default 15.x (15.3.0)                                     | tag `2026.08.2` = `cd8011d7c996`, same file                                                                                                              | Non-LTS                                                                                                                                            |
| OpenWrt 25.12.6 (current release)       | Default `GCC_VERSION` "14.3.0"; selectable 12.3.0, 13.4.0, 15.2.0 (needs `TOOLCHAINOPTS`) | tag `v25.12.6` = `64900e756efa`, `toolchain/gcc/Config.in` and `Config.version`                                                                          | Current stable branch `openwrt-25.12`                                                                                                              |
| OpenWrt 24.10.8 (previous), for context | Default 13.3.0; selectable 11.3.0, 12.3.0, 14.2.0                                         | tag `v24.10.8` = `0b795ce79e23`                                                                                                                          | Previous stable branch                                                                                                                             |

Notes on the Buildroot row. The Buildroot manual says "Starting with 2025.02, the first release of every odd-numbered
year is a long-term support (LTS) release supported for three years", and lists LTS releases as 2025.02, 2027.02. A
LinkedIn post found by search says "2025.02 & 2026.02 LTS". I followed the manual in the repository, so 2026.02 is not
an LTS. Treat the LinkedIn text as a stale or loose claim.

### Q1b. Default language standard per GCC version

| GCC        | Default C         | Default C++ | Source and pin (all read 2026-11-23)                                                                                                            |
| ---------- | ----------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 5          | gnu11 (was gnu89) | gnu++98     | gcc.gnu.org/gcc-5/changes.html                                                                                                                  |
| 6          | gnu11             | gnu++14     | gcc.gnu.org/gcc-6/changes.html                                                                                                                  |
| 8          | gnu17             | gnu++14     | gcc.gnu.org/gcc-8/changes.html ("The default mode for C is now -std=gnu17 instead of -std=gnu11")                                               |
| 11         | gnu17             | gnu++17     | gcc.gnu.org/gcc-11/changes.html ("The default mode for C++ is now -std=gnu++17 instead of -std=gnu++14")                                        |
| 12, 13, 14 | gnu17             | gnu++17     | Inference: the change pages for 12 to 14 announce no new default. GCC 14 added the `-std=c23` and `-std=gnu23` spellings (gcc-14/changes.html). |
| 15         | gnu23             | gnu++17     | gcc.gnu.org/gcc-15/changes.html ("changes the default language version for C compilation from -std=gnu17 to -std=gnu23")                        |
| 16         | gnu23             | gnu++20     | gcc.gnu.org/gcc-16/changes.html (C++ default changes from `-std=gnu++17` to `-std=gnu++20`)                                                     |

Reading across Q1a and Q1b (inference). Scarthgap (GCC 13.5) and Buildroot LTS (13.4 default) compile with `gnu17` and
`gnu++17` unless told otherwise. Wrynose and Buildroot 2026.08 (GCC 15) silently switch C code to `gnu23` unless the
build sets `-std`. GCC 15 porting notes (gcc.gnu.org/gcc-15/porting_to.html) list the breaks: `int f()` now means
`int f(void)`, and `typedef int bool;` is an error because `bool`, `true`, `false`, `nullptr` and `thread_local` are
keywords. Pin `-std` explicitly in every build.

Kernel for context: `Documentation/process/programming-language.rst` at `v7.3` (`c03c1a14507d`) says the kernel is
"typically compiled with gcc under -std=gnu11". Kernel code is not userspace, but it is the C dialect of the whole
stack.

## Q2. Standards declared by embedded Linux userspace projects

Rows read from build files at the pinned ref. "Not set" means the file was read and has no `-std`, `c_std` or
`CMAKE_*_STANDARD` entry.

| Project                         | Pin                                                                                    | Declared C                                         | Declared C++                                                                                | File and evidence                                                                                                                                             |
| ------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| systemd                         | `v262.2` = `63511d7283d7`                                                              | `gnu17`                                            | none (C only)                                                                               | `meson.build` `c_std=gnu17`. `docs/CODING_STYLE.md`: "we intend to use ISO C17 with GNU extensions (aka gnu17)". `README`: `gcc >= 8.4`.                      |
| BusyBox                         | `1_38_0` = `fc71374dfccd` (git.busybox.net, cloned; the GitHub mirror stops at 1_36_1) | `-std=gnu99` via `cc-option`                       | none                                                                                        | `Makefile.flags` line 10, comment "-std=gnu99 needed for [U]LLONG_MAX on some systems". Source states.                                                        |
| RAUC                            | `v1.15.2` = `4fb7c798d6ae`                                                             | `gnu11`                                            | none                                                                                        | `meson.build` `c_std=gnu11`                                                                                                                                   |
| SWUpdate                        | `2026.05.2` = `6afadb8c03c9`                                                           | `-std=gnu99` via `cc-option`                       | none                                                                                        | `Makefile.flags`, "-std=gnu99 needed for [U]LLONG_MAX on some systems"                                                                                        |
| Mender client (C++)             | `5.2.0` = `0f4eb08e9d71`                                                               | none                                               | Release builds `-std=c++17`. Debug builds `-std=c++11` "so that we catch C++11 violations". | `cmake/build_mode.cmake`; `MENDER_CXX_STANDARD` is 17 or 11. Source states. Inference: the client's code is written to the C++11 subset and shipped as C++17. |
| mosquitto                       | `v2.1.4` = `d69b6b757d05`                                                              | `CMAKE_C_STANDARD 99`; Makefile build `-std=gnu99` | `CMAKE_CXX_STANDARD 17`                                                                     | `CMakeLists.txt` lines 16 to 20; `config.mk` line 192                                                                                                         |
| GStreamer                       | `1.28.9` = `3ced45da0960`                                                              | `c_std=gnu11,c11`                                  | `cpp_std=c++14` only in the top-level monorepo file, commented as a Meson workaround        | `subprojects/gstreamer/meson.build`, `subprojects/gst-plugins-base/meson.build`, top `meson.build`                                                            |
| libcamera                       | `v0.8.0` = `df8e348d64b4`                                                              | not set                                            | `cpp_std=c++20`                                                                             | `meson.build`                                                                                                                                                 |
| Qt 6 (qtbase)                   | `v6.12.1` = `5af1a37e31a8`                                                             | `CMAKE_C_STANDARD 11`                              | Newest the compiler supports, from 17 up to 26. Qt headers require C++17.                   | `cmake/QtFlagHandlingHelpers.cmake` `qt_set_language_standards`; `src/corelib/global/qcompilerdetection.h`: "Qt requires a C++17 compiler"                    |
| PipeWire                        | `1.6.11` = `4287f3151077`                                                              | `gnu11`                                            | `c++20`                                                                                     | `meson.build`                                                                                                                                                 |
| NetworkManager                  | `1.58.1` = `7406dfbcc35b`                                                              | `gnu11`                                            | none                                                                                        | `meson.build`                                                                                                                                                 |
| ConnMan                         | `2.0` = `c51dc2177cdb` (git.kernel.org, dated 2026-02-09)                              | Not set (autoconf `AC_PROG_CC` only)               | none                                                                                        | `configure.ac`. Inference: it uses the compiler default (gnu17 on GCC 8 to 14, gnu23 on GCC 15).                                                              |
| dbus-broker                     | `v37` = `e5b413f573b2`                                                                 | `c11` (strict)                                     | none                                                                                        | `meson.build`                                                                                                                                                 |
| AGL agl-compositor              | `21.0.4` = `cea35f44d1` (git.automotivelinux.org)                                      | `c_std=gnu99`                                      | none                                                                                        | `meson.build`                                                                                                                                                 |
| AGL app-framework-binder        | `17.1.12` = `5d65053777`                                                               | none seen                                          | `CMAKE_CXX_STANDARD 14`                                                                     | `CMakeLists.txt`                                                                                                                                              |
| AGL meta-agl layer              | `master` = `8611917335f6`                                                              | n/a                                                | n/a                                                                                         | `meta-agl-core/conf/layer.conf`: `LAYERSERIES_COMPAT_aglcore = "scarthgap"`, so AGL builds with the Yocto 5.0 toolchain (GCC 13).                             |
| Mbed TLS (library, for context) | `v4.3.0` = `eafb4a72592a`                                                              | `CMAKE_C_STANDARD 99` (tests 11)                   | none                                                                                        | `CMakeLists.txt` lines 329 and 584                                                                                                                            |

Reading (inference). Among the 11 C projects that declare a level (ConnMan sets none), it is gnu99 or C99 (BusyBox,
SWUpdate, mosquitto, agl-compositor), gnu11 or c11 (RAUC, GStreamer, NetworkManager, dbus-broker, PipeWire, Qt), or
gnu17 (systemd). None declares C23. For C++, Mender, mosquitto and Qt's minimum say C++17, libcamera and PipeWire say
C++20, and the AGL binder says C++14. The older C99 declarations come from small-footprint or long-lived code, not from
toolchain limits: every Yocto, Buildroot and OpenWrt compiler since 2018 defaults to gnu17.

Limits. AGL coverage is thin: git.automotivelinux.org lists few repos and several `agl-service-*` names I tried returned
nothing. A GitHub code-search rate limit stopped further sampling (weston, libinput, BlueZ not read).

## Q3. MCU and RTOS firmware

### Q3a. SDKs and RTOS projects

| Project               | Pin                                                                         | Declared or required (source states)                                                                                                                                          | File and evidence                                                                                                                                                                                                                                                                                                                                            |
| --------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Zephyr                | `v4.5.0` = `41d10b597304` (2026-10-28)                                      | C: `STD_C17` default, `STD_C23` optional. C11, C99 and C90 options removed. C++: choice `STD_CPP`, default `STD_CPP11`, options 98 to 26.                                     | `Kconfig.zephyr` ("default STD_C17"); `CMakeLists.txt` builds `-std=c17` or `c2x`, and replaces `c` with `gnu` only when `CONFIG_GNU_C_EXTENSIONS` is set (no default in Kconfig); `lib/cpp/Kconfig`; `doc/releases/migration-guide-4.5.rst`: "Support for C standard versions older than C17 has been removed ... Use C17 or higher when compiling Zephyr." |
| Zephyr SDK toolchain  | sdk-ng `v1.0.1` = `cb61ae18a0de`                                            | GCC 14.3.0, binutils 2.43.1                                                                                                                                                   | Release notes of `v1.0.1`; `SDK_VERSION` in Zephyr `v4.5.0` is 1.0.1                                                                                                                                                                                                                                                                                         |
| FreeRTOS Kernel       | `V11.3.3` = `89592801dd8b`                                                  | Kernel core is C90-clean. `include/FreeRTOS.h`: "FreeRTOS does not require C99 in any other way" than `stdint.h`.                                                             | `examples/cmake_example/CMakeLists.txt`: `set_property(TARGET freertos_kernel PROPERTY C_STANDARD 90)`. The RP2040 port sets `CMAKE_C_STANDARD 11` and `CMAKE_CXX_STANDARD 17` (`portable/ThirdParty/GCC/RP2040/CMakeLists.txt`).                                                                                                                            |
| ESP-IDF               | `v6.1.1` = `051e4c4eb203`; `v6.0` = `662a3be35475`; `v6.1` = `fff9895c82d7` | Chip targets: `-std=gnu23` and `-std=gnu++26`. Linux target picks the newest the host compiler supports (C: gnu23, gnu17, gnu11, gnu99).                                      | `tools/cmake/build.cmake`; `docs/en/api-guides/c.rst` ("GNU dialect of ISO C23 ... is the current default"); `docs/en/api-guides/cplusplus.rst` (C++ exceptions "disabled by default").                                                                                                                                                                      |
| ESP-IDF 5.x           | `v5.5.4` = `735507283d5b`; `v5.4.4` = `296b6eab9445`                        | `-std=gnu17` and `-std=gnu++2b`                                                                                                                                               | `tools/cmake/build.cmake` (`v5.3.4` is the same)                                                                                                                                                                                                                                                                                                             |
| Raspberry Pi Pico SDK | `2.3.1` = `079c6f390236`                                                    | `CMAKE_C_STANDARD 11` and `CMAKE_CXX_STANDARD 11`, set in `pico_sdk_init` logic                                                                                               | `CMakeLists.txt` lines 35 and 36. Inference: user projects can override these, so they are defaults, not requirements.                                                                                                                                                                                                                                       |
| Mbed OS               | `mbed-os-6.17.0` = `17dc3dc2e6e2`                                           | C `-std=gnu11`, C++ `-std=gnu++14 -fno-rtti`                                                                                                                                  | `tools/profiles/release.json`. The README on `master` (`d723bf9e5541`, last push 2024-10-08) says Arm announced end of life; os.mbed.com says "Mbed was sunsetted in July 2026".                                                                                                                                                                             |
| Apache NuttX          | `nuttx-13.1.0` = `2b5c0de5e933`                                             | C: no `-std` flag found in `arch/arm/src/common/Toolchain.defs`; inference: compiler default. C++: `CONFIG_CXX_STANDARD` default `gnu++17`, or `gnu++20` when `LIBCXX` is on. | `libs/libxx/Kconfig` lines 109 to 113                                                                                                                                                                                                                                                                                                                        |
| Arm CMSIS 6           | `v6.4.0` = `af1b110e46a1`                                                   | "Compliant with ANSI C (C99) and C++ (C++03)". Also "Conforms to MISRA 2012 (but does not claim MISRA compliance)".                                                           | `CMSIS/Documentation/Doxygen/General/src/mainpage.md`, "Coding Rules". The same page says CMSIS is checked against MISRA C:2012, not MISRA C++:2008.                                                                                                                                                                                                         |
| STM32Cube             | no ST repository states one (see limits)                                    | Third-party report of STM32CubeMX 6.12.1 generated `cmake/stm32cubemx/CMakeLists.txt`: "if(CMAKE_C_STANDARD LESS 11) message(ERROR "Generated code requires C11 or higher")". | community.st.com thread "Bug: STM32MX useless CMake C standards check", posted 2024-11-06. Second-hand quote of generated code. Third-party CubeMX templates set `CMAKE_C_STANDARD 11`. ST's `gnu-tools-for-stm32` tag `15.3.rel2.20261015-0600` suggests GCC 15.3 (inference from the tag name).                                                            |
| RIOT                  | `2026.10` = `78acd33c53c0`                                                  | Adds `-std=c11` when the compiler accepts it and no `-std` is set                                                                                                             | `Makefile.include`                                                                                                                                                                                                                                                                                                                                           |
| Arduino AVR core      | `1.8.8` = `86df345b3cf4`                                                    | `-std=gnu11`; C++ `-std=gnu++11 -fno-exceptions -fno-threadsafe-statics`                                                                                                      | `platform.txt`                                                                                                                                                                                                                                                                                                                                               |
| Arduino Renesas core  | `1.6.0` = `424e86eff92d`                                                    | `-std=gnu11`; C++ `-std=gnu++17 -fno-rtti -fno-exceptions`                                                                                                                    | `platform.txt`                                                                                                                                                                                                                                                                                                                                               |

Reading (inference). The firmware world splits in two. Vendor-controlled SDKs with a bundled modern toolchain (Zephyr
SDK GCC 14, ESP-IDF toolchain) have moved to C17 and beyond. SDKs that support many third-party compilers, and portable
library code (CMSIS, FreeRTOS), stay at C99 or lower. C++ defaults are lower than C defaults: Zephyr C++11, Pico SDK
C++11, Arduino AVR C++11, Mbed C++14. ESP-IDF is the outlier at C++26. Every C++ configuration surveyed that sets
exceptions turns them off (ESP-IDF, Arduino cores) and Mbed turns off RTTI.

### Q3b. Coding standards

| Standard       | Language target                   | Source (read 2026-11-23)                                                                                                                                                                                                                                           | Note                                                                                                                                                                                           |
| -------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MISRA C:2012   | C99, with guidelines kept for C90 | misra.org.uk/misra-c/: "extends support to the C99 version of the language whilst maintaining guidelines for C90"                                                                                                                                                  | Published 18 March 2013 per the same page. The text is paywalled; I used MISRA's public page.                                                                                                  |
| MISRA C:2023   | C90, C99, C11 and C18             | misra.org.uk/misra-c2023-released/: incorporates Amendments 2 to 4 and TC2, "incorporates support for C11 and C18 language features"                                                                                                                               | Published April 2023                                                                                                                                                                           |
| MISRA C:2025   | C11 and C18, and earlier          | misra.org.uk/misra-c/: "published in March 2025 ... maintaining support to the C11 and C18 (and earlier)"                                                                                                                                                          | MISRA forum thread tid=1728: C:2025 "did not extend the scope to the newer C Standard"; "work has commenced" on C23 after ISO/IEC 9899:2024. So no MISRA C edition covers C23 as of this read. |
| MISRA C++:2023 | C++17 (ISO/IEC 14882:2017)        | misra.org.uk/misra-cpp2023-released-including-hardcopy/: "Guidelines for the use C++:17 in critical systems", published October 2023                                                                                                                               | Merges MISRA C++:2008 and AUTOSAR C++14 (MISRA page and vendor summaries)                                                                                                                      |
| MISRA C++:2008 | C++03                             | misra.org.uk/misra-c-plus-plus/ (published 5 June 2008). The C++03 target is inference from the 2008 date and from CMSIS naming it as the C++ MISRA version.                                                                                                       | Superseded                                                                                                                                                                                     |
| AUTOSAR C++14  | C++14                             | AUTOSAR document 839 "Guidelines for the use of the C++14 language in critical and safety-related systems", file `AUTOSAR_RS_CPP14Guidelines.pdf` (sha256 prefix `03d6e4baed98`), release AP 19-03; the change history says "Marked the specification as obsolete" | Obsolete; MISRA C++:2023 is its successor                                                                                                                                                      |

## Q4. What changed between the standards

Sources: cppreference pages for C11, C17 and C23 (en.cppreference.com/w/c/11, /17, /23, read 2026-11-23); the GCC 13, 14
and 15 change pages; gcc.gnu.org/projects/cxx-status.html and the libstdc++ status table
(gcc.gnu.org/onlinedocs/libstdc++/manual/status.html), both read 2026-11-23. Where I add detail beyond them, I mark it
"background". I did not read the ISO texts, which are paywalled.

### C

| Step                    | What it gives or removes for embedded code                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Basis                                                                                                                                                                                                                                         |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C99                     | `//` comments, declarations after statements, `for` loop declarations, `stdint.h`, `stdbool.h`, `inline`, `restrict`, designated initializers, compound literals, variable length arrays (VLAs)                                                                                                                                                                                                                                                                                                                | Background; CMSIS names C99 as its baseline and FreeRTOS needs only `stdint.h` from it                                                                                                                                                        |
| C11                     | `_Static_assert`, `_Generic`, `_Atomic`, `_Thread_local`, `alignas`/`alignof`, anonymous structs and unions, `_Noreturn`. Optional in C11: atomics, threads, VLAs (feature macros `__STDC_NO_ATOMICS__`, `__STDC_NO_THREADS__`, `__STDC_NO_VLA__`). Removes `gets()`.                                                                                                                                                                                                                                          | cppreference c/11                                                                                                                                                                                                                             |
| C17 (ISO/IEC 9899:2018) | No new language features. cppreference: "same as C11, except that it bumps `__STDC_VERSION__` to 201710L, contains several defect reports, and deprecates some features". It fixes 54 defects.                                                                                                                                                                                                                                                                                                                 | cppreference c/17. So choosing `gnu11` or `gnu17` changes almost nothing but the macro.                                                                                                                                                       |
| C23 (ISO/IEC 9899:2024) | `nullptr`, `bool`/`true`/`false`/`static_assert`/`thread_local` as keywords, `constexpr` objects, `auto` type inference, `typeof`, enums with a fixed underlying type, `[[attributes]]`, binary literals (`0b`), digit separators, `{}` empty initializer, `#embed`, `#elifdef`, `#warning`, `_BitInt`, `<stdckdint.h>` (checked arithmetic), `<stdbit.h>`, `memset_explicit`. Removes old-style (K&R) function definitions, non-two's-complement integers, trigraphs. Unprototyped `f()` now means `f(void)`. | cppreference c/23 and GCC 13, 14 and 15 change pages. GCC 13 implemented `nullptr`, `auto`, `constexpr`, `typeof`, keywords and fixed enums. GCC 14 added `_BitInt` (IA-32, x86-64, AArch64 only) and `<stdckdint.h>`. GCC 15 added `#embed`. |

What matters for the C choice (inference). C11 adds `_Static_assert` and `_Generic`, which firmware uses heavily. C11
also adds optional parts (`_Atomic`, threads, VLAs) that bare-metal toolchains may lack, so check the feature macros.
C17 is a free upgrade over C11. C23 brings useful items (`constexpr`, `nullptr`, `typeof`, `#embed` for firmware images,
`stdckdint.h`) but needs GCC 13 or newer for most of them, GCC 14 or newer for `_BitInt` and `stdckdint.h`, and GCC 15
for `#embed` and as the default. No MISRA C edition covers C23.

### C++

| Step  | What it gives or removes for embedded code                                                                                                                                                                                                                                                                                                                                                                             | Basis                                                                                                       |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| C++11 | `auto`, `constexpr`, `nullptr`, `enum class`, `static_assert`, lambdas, move semantics, `std::array`, `<atomic>`, `<cstdint>`, `override`/`final`, `= delete`, range `for`                                                                                                                                                                                                                                             | Background                                                                                                  |
| C++14 | Relaxed `constexpr`, generic lambdas, return type deduction, `std::make_unique`, binary literals, digit separators                                                                                                                                                                                                                                                                                                     | Background; binary literals GCC 4.9 per cxx-status                                                          |
| C++17 | `if constexpr`, structured bindings (GCC 7), inline variables (GCC 7), fold expressions, class template argument deduction, `std::optional`, `std::variant`, `std::string_view`, `[[nodiscard]]`, `[[maybe_unused]]`, `[[fallthrough]]`, guaranteed copy elision. Removes `register`, trigraphs, `std::auto_ptr`.                                                                                                      | cxx-status rows for structured bindings and inline variables; rest background                               |
| C++20 | Concepts (GCC 10), `consteval` (GCC 10, full in 11), `constinit` (GCC 10), designated initializers (GCC 8, with C++ ordering rules), `<=>`, coroutines (GCC 10; on with `-std=c++20` from GCC 11), modules (GCC 11, experimental, needs `-fmodules`), `std::span`, `<bit>`, `std::format` (libstdc++ 13.1), `<ranges>` (libstdc++ 10.1). It deprecates some compound `volatile` operations.                            | cxx-status and libstdc++ status. Note the cxx-status page says C++20 modules support is still experimental. |
| C++23 | `if consteval` (GCC 12), deducing this (GCC 14), `static operator()` (GCC 13), multidimensional `operator[]` (GCC 12), `std::expected` (libstdc++ 12.1), `std::unreachable` (12.1), `std::move_only_function` (12.1), `std::byteswap` (12.1), `std::to_underlying`, `std::print` (14.1), `std::flat_map` (15.1), `std::mdspan` (16.1). Compound `volatile` operations are de-deprecated (P2327R1, GCC 13 change page). | cxx-status, libstdc++ status, GCC 13 change page. GCC marks C++23 support "experimental".                   |
| C++26 | `static_assert` with a generated message (GCC 14), pack indexing, `= delete("reason")` (GCC 15), trivial infinite loops no longer undefined behaviour (GCC 14).                                                                                                                                                                                                                                                        | GCC 14 and 15 change pages                                                                                  |

What matters for the C++ choice (inference). `constexpr`, `consteval`, `constinit`, `enum class` and `std::array` give
embedded code compile-time tables and type safety without heap use, and all of them are in C++20 or earlier.
`std::expected` and `std::optional` give error handling without exceptions, which embedded builds turn off (Arduino
cores, ESP-IDF default). Things to avoid on small targets stay the same across versions: exceptions and RTTI,
`iostream`, heap containers, `std::function`, coroutines (they allocate frames), thread-safe static initialisation
(Arduino AVR passes `-fno-threadsafe-statics`), and any library header that assumes a hosted libstdc++. The cppreference
page `w/cpp/freestanding` covers what a freestanding implementation must provide; I did not read it closely enough to
cite specific items.

## Proposed defaults

Each default is a recommendation for a skill that tells an agent which standard to target when nothing else is known.
The conditions say when to move.

### Embedded Linux userspace, C: `-std=gnu17`

Reason. Source states that every Yocto, Buildroot and OpenWrt compiler listed in Q1 ships GCC 13 or newer and defaults
to `gnu17` up to GCC 14. The main projects declare gnu11 or gnu17 (systemd, RAUC, PipeWire, Qt, NetworkManager).
Inference: C17 has the same features as C11, so `gnu17` costs nothing and matches systemd. Setting it explicitly
protects against the GCC 15 switch to `gnu23` in Yocto wrynose and Buildroot 2026.08.

Conditions that change it.

- Go to `gnu11` (or `c11`) for a public library that other projects build, or when a compiler older than GCC 8 must
  work. Both give the same language; only the macro differs.
- Go to `gnu99` for a BusyBox or SWUpdate-style package that must build on any system, or when matching an existing codebase.
- Go to `gnu23` only when every supported toolchain is GCC 15 or newer (Yocto wrynose, Buildroot 2026.08 or later) and
  the project accepts that no MISRA C edition covers C23.
- A strict `-std=c11` (no GNU extensions) is right when the project must also build with other compilers or follows MISRA.
- Do not rely on the compiler default for any of these: it changes with the GCC version.

### Embedded Linux userspace, C++: `-std=gnu++17`

Reason. Source states Qt 6.12 requires C++17, Mender and mosquitto declare C++17, and GCC 11 to 15 default to `gnu++17`.
libcamera and PipeWire already use C++20, so C++17 is the floor most dependencies accept, not the ceiling. The draft's
C++20 is workable on current toolchains (GCC 13 in scarthgap, GCC 15 in wrynose), but few surveyed projects need it.

Conditions that change it.

- Go to C++20 for new code when the oldest toolchain you must support is GCC 13 or newer or a comparable Clang (I did
  not check Clang versions). Avoid C++20 modules (GCC marks them experimental) and `std::print` (needs libstdc++ 14).
- Go to C++14 when the target must build with a compiler of GCC 6 to 8 or an AGL-style legacy layer.
- Keep the Mender pattern when shipping a library to unknown consumers: compile as the lowest standard you document and
  test that subset in debug builds.
- Raise the floor when a dependency requires it, such as Qt (C++17) or libcamera (C++20).

### MCU firmware, C: `-std=gnu17`

Reason. Source states that Zephyr 4.5 requires C17 or higher and defaults to it, ESP-IDF 5.x used `gnu17`, Arduino and
Mbed use `gnu11`, and STM32CubeMX-generated CMake checks for C11 or higher. C17 equals C11 in features, so this default
also covers the C11 SDKs. Vendor toolchains today (Zephyr SDK GCC 14.3, ST GNU tools tag 15.3) accept it.

Conditions that change it.

- Zephyr 4.5 or later: C17 is required. Zephyr's own default is strict `c17` without GNU extensions; use `gnu17` only if
  you need them.
- ESP-IDF 6.x: the SDK builds with `gnu23`; your component can stay at `gnu17` by adding `-std=` in its
  `CMakeLists.txt`, as the ESP-IDF docs show.
- MISRA C:2012: target C99 (strict `-std=c99`). MISRA C:2023 or 2025: C11 or C18 is allowed; use strict `-std=c11` or
  `c17`. No MISRA edition covers C23.
- Reusable library or driver code meant for any SDK: write to C99 (CMSIS and FreeRTOS headers are C99 and C90-clean) and
  avoid VLAs, `_Atomic` and C11 threads unless the target supports them.
- Older or vendor-locked compilers (IAR, Keil, old `arm-none-eabi-gcc` older than GCC 8): use the highest standard the
  compiler documents, often C99 or C11.
- C23 is reasonable only with GCC 13 or newer and when the project is outside MISRA.

### MCU firmware, C++: `-std=gnu++17`

Reason. Source states MISRA C++:2023 targets C++17, NuttX defaults to `gnu++17`, Arduino Renesas uses `gnu++17`, and the
RP2040 FreeRTOS port uses C++17. C++17 gives `constexpr` (relaxed from C++14), `if constexpr`, `std::optional`,
`std::variant` and `std::string_view` without needing a newer toolchain. The values below C++17 (Zephyr C++11 default,
Pico SDK C++11, Arduino AVR C++11, Mbed C++14) are SDK defaults, not firm requirements. Inference: they stay low for
compatibility.

Conditions that change it.

- Zephyr: the default is C++11, so set `CONFIG_STD_CPP17` explicitly.
- Pico SDK: the default is C++11; override `CMAKE_CXX_STANDARD`.
- ESP-IDF: the default is already `gnu++26` on 6.x and `gnu++2b` on 5.x. Pin lower if you need portability.
- Go to C++14 for AUTOSAR C++14 projects (obsolete guideline) or toolchains older than GCC 7.
- Go to C++20 when the toolchain is GCC 11 or newer, you want `consteval`, `constinit` or concepts, and you avoid hosted
  library features. C++20 modules and coroutines are not recommended on small targets.
- MISRA C++:2023: stay at C++17.
- Disable exceptions and RTTI unless the product needs them (`-fno-exceptions -fno-rtti`), as Arduino cores, ESP-IDF and
  Mbed do. Write C++ headers for C consumers behind `extern "C"` and keep CMSIS-facing headers C99 and C++03 safe.

## What I could not verify

- The Arm GNU Toolchain's current GCC version: developer.arm.com returned an empty page. Zephyr SDK (GCC 14.3.0) and
  ST's tag name are the only MCU toolchain pins here.
- STM32Cube's own build files: no ST repository showed a language standard, and GitHub code search hit its rate limit.
  The C11 evidence is a user-posted quote of CubeMX 6.12.1 output.
- NuttX's C standard: I found no `-std` flag, so "compiler default" is an inference.
- Clang's default standards and minimum versions: not read.
- Breadth for AGL and for projects beyond the list (weston, BlueZ, libinput).
- ISO standard texts, MISRA texts and the AUTOSAR document's rule contents beyond front matter: paywalled or not read.
  MISRA language targets come from misra.org.uk pages and a MISRA forum answer.
- The C++11, C++14 and C++17 feature lists and the C99 list are background knowledge, not read from a source this session.
- Whether current Pico SDK projects commonly override the C++11 default.

## Retrieval commands

Re-read any pin with `gh api "repos/OWNER/REPO/contents/PATH?ref=REF" --jq .content | base64 -d`.
