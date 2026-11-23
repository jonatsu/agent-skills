# C and C++ testing: primary-source notes

Read date for every page without a pin: 2026-11-23. "Source states" marks a fact read in the cited source;
"inference" marks my conclusion; "background" marks knowledge I did not verify in this session.
Short SHAs are the first 12 characters. GitHub "release date" is the Atom feed `updated` value of the release
entry, which can differ by hours from the tag date.

Route notes: `gh` is not available in this lane (Bash is read-only), so GitHub files were read through
`raw.githubusercontent.com` and `github.com/<owner>/<repo>/blob/<sha>/...` pages, and release dates through
`releases.atom`. Plain-text files without a `.md` or `.rst` extension (LICENSE, COPYING) come back empty from the
raw route; the blob page worked for them.

## 1. Unit test frameworks

### 1.1 Name disambiguation: three things called "cpptest"

| Name               | What it is                                                                                                                            | Language                          | Licence                                                                                                                          | Status                                                                                                                                                                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CppUTest           | Unit test and mocking framework (Feathers, Grenning, Vodde). Repo `cpputest/cpputest`.                                                | C and C++ tests, framework is C++ | BSD 3-clause (COPYING at `42feb8740bea`: "Copyright (c) 2007, Michael Feathers, James Grenning and Bas Vodde", three conditions) | Active. HEAD `42feb8740bea` dated 2026-11-03.                                                                                                                                                                                                             |
| cpptest (library)  | "CppTest", a portable C++ unit test library by Niklas Lundell and later maintainers. Sourceforge `cpptest`, GitHub `cpptest/cpptest`. | C++                               | LGPL 2.1 (COPYING on master `bc01feae2084`: "GNU LESSER GENERAL PUBLIC LICENSE Version 2.1"; the Sourceforge page says "LGPLv2") | Dead. NEWS on `bc01feae2084` states: "Release 2.0.1 was the last release of this project, and the project is now unmaintained and closing down... please migrate to one of the alternatives." GitHub repo archived 2026-09-27, the date of release 2.0.1. |
| Parasoft C/C++test | Commercial static analysis, unit test, coverage and runtime analysis product. Not a library.                                          | C and C++                         | Proprietary                                                                                                                      | Active vendor product. See 7.4.                                                                                                                                                                                                                           |

Source states for the Parasoft row: parasoft.com product page, read 2026-11-23. Source states for cpptest:
`https://github.com/cpptest/cpptest/blob/bc01feae2084/NEWS`, the Sourceforge project page (summary text and LGPLv2),
and the GitHub repo page ("archived by the owner on Sep 27, 2026"). The Sourceforge home page
(`cpptest.sourceforge.io`) says "Latest version: 2.0.0" and lists output formats "simple text, compiler-like,
and HTML"; it is stale against the 2.0.1 release.

Inference for a skill: when a user writes "cpptest", ask or infer from context. In a C or C++ project that
mocks and checks heap leaks, CppUTest is the likely meaning. In a safety-certified automotive or avionics
project, Parasoft C/C++test is the likely meaning. The Sourceforge library should not be recommended for new work.

### 1.2 Comparison table

Pins: repo HEAD short SHA (default branch) read via `commits.atom`, release from `releases.atom`.

| Framework                 | Targets                                              | Runs on MCU target?                                                                                                                                                                                                                                                                                                                | Heap, exceptions, RTTI                                                                                                                                                                                  | Mocking                                                                                                                                                                                                                                                                                              | Licence (file read)                                                                                                                     | Latest release                                                                                                                              | Maintained                                                                                                                                                                                |
| ------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CppUTest                  | C and C++ code, tests in C++ (C tests via wrappers). | Source states build options `CPPUTEST_STD_C_LIB_DISABLED`, `CPPUTEST_STD_CPP_LIB_DISABLED`, `CPPUTEST_MEM_LEAK_DETECTION_DISABLED` exist (`CMakeLists.txt` at `42feb8740bea`), so it is designed to be buildable without a hosted libc or STL. Inference: runs on a target when those are set; Grenning's paper uses it on a host. | Leak detector replaces `new`, `delete`, and (with macro header) `malloc`; README: "For GCC a simple new/delete count is used in overridden operators". Exceptions and RTTI: not stated in sources read. | Source states README title "unit testing and mocking framework"; mocking is the CppUMock part of `CppUTestExt` (option `CPPUTEST_EXTENSIONS`). Memfault compares CppUMock, fff, CMock.                                                                                                               | BSD-3-Clause, `COPYING`                                                                                                                 | v4.0 (2020-05-27); rolling tag `latest-passing-build` 2026-07-30                                                                            | Yes: HEAD 2026-11-03. Slow release cadence: v4.0 is 6 years old; consumers track the rolling tag or a commit.                                                                             |
| Unity                     | C only.                                              | Yes. Source states (`docs/UnityConfigurationGuide.md` at `54f864cf6027`): output goes through `UNITY_OUTPUT_CHAR(a)` for targets without stdout; `UNITY_EXCLUDE_SETJMP` for targets without setjmp (cost: no custom helper functions, no CMock); Ruby scripts are "purely optional".                                               | No heap use stated; no C++ needed.                                                                                                                                                                      | Via CMock (separate project).                                                                                                                                                                                                                                                                        | MIT, `LICENSE.txt` ("Copyright (c) 2007-26 Mike Karlesky, Mark VanderVoord, & Greg Williams")                                           | v2.7.0 (2026-07-16)                                                                                                                         | Yes: HEAD `54f864cf6027` 2026-10-31                                                                                                                                                       |
| CMock                     | C mock generator and runtime for Unity.              | Mocks run on target or host; generator needs Ruby on the development host. Source states README: "mock and stub generator and runtime for unit testing C ... parses your C headers"; self-tests need `bundle install` and `rake`. Ceedling is the build manager that bundles it.                                                   | Mock runtime is C.                                                                                                                                                                                      | Yes, header-driven generation.                                                                                                                                                                                                                                                                       | MIT, `LICENSE.txt`                                                                                                                      | v2.7.0 (2026-07-16)                                                                                                                         | Yes: HEAD `34c26e540301` 2026-10-17                                                                                                                                                       |
| GoogleTest and GoogleMock | C++ (C code is tested from C++ tests).               | Host only in practice. Inference: needs C++17 (source states README: "requires at least C++17"), STL, and a hosted environment; Google's platforms page lists supported OS and compilers, no MCU.                                                                                                                                  | `GTEST_HAS_EXCEPTIONS` and `GTEST_HAS_RTTI` are 1 or 0 and autodetected (`gtest-port.h` at `a46a6012a133`). FAQ: portable tests should work with or without exceptions.                                 | GoogleMock mocks virtual methods; source states (`docs/gmock_for_dummies.md`): "while it's possible to mock non-virtual methods using templates, it's much more involved". Mocking a C free function therefore needs a seam (wrapper interface or link substitution); gmock gives no direct support. | BSD-3-Clause, `LICENSE` ("Copyright 2008, Google Inc.")                                                                                 | v1.18.0 (2026-08-10)                                                                                                                        | Yes: HEAD `a46a6012a133` 2026-11-17                                                                                                                                                       |
| Catch2                    | C++ only (v3 is compiled, not header-only).          | Host. Inference. Source states exceptions are used by default to abort tests and "experimental support for disabling exceptions" exists (`CATCH_CONFIG_DISABLE_EXCEPTIONS`, `docs/configuration.md` at `36c1bc3ef209`).                                                                                                            | C++14 minimum (source states, `docs/migrate-v2-to-v3.md`).                                                                                                                                              | No built-in mocking (inference: none found in docs read; Catch2 has no mock API).                                                                                                                                                                                                                    | BSL-1.0, `LICENSE.txt` ("Boost Software License - Version 1.0")                                                                         | v3.16.1 (2026-10-08)                                                                                                                        | Yes: HEAD `36c1bc3ef209` 2026-11-15                                                                                                                                                       |
| doctest                   | C++ only; tests may sit in production source files.  | Host. Inference. Source states `DOCTEST_CONFIG_NO_EXCEPTIONS` and `..._BUT_WITH_ALL_ASSERTS` exist (`doc/markdown/configuration.md` at `d44d4f6e6623`).                                                                                                                                                                            | C++11 (source states README: "Portable C++11 (use tag 1.2.9 for C++98)").                                                                                                                               | None.                                                                                                                                                                                                                                                                                                | MIT, `LICENSE.txt` ("Copyright (c) 2016-2023 Viktor Kirilov")                                                                           | v2.5.3 (2026-07-06)                                                                                                                         | Releases yes; master HEAD `d44d4f6e6623` is dated 2026-03-27, so the latest release tag is newer than master HEAD (releases come from another branch or tag); treat activity as moderate. |
| cmocka                    | C only.                                              | Source states (cmocka.org): "only requires the standard C library... works on a range of computing platforms (including embedded)", "No fork()", C99 required from 2.0.0, TAP 14, Subunit, xUnit XML output, signal exception handling.                                                                                            | No heap or C++ needs stated.                                                                                                                                                                            | Yes: built-in mock objects (`will_return`, `expect_*`, `mock()`) and type-safe assertions (source states "Support for Mock Objects").                                                                                                                                                                | Apache-2.0 (source states: cmocka.org "License: Apache License 2.0"; the `COPYING` in the stale GitHub mirror is the 11 KB Apache text) | 2.0.2 (tag dated 2026-01-12 on `gitlab.com/cmocka/cmocka`). The GitHub mirror `clibs/cmocka` stopped at 1.1.5 (2022-09-05): do not cite it. | Yes (upstream on GitLab and `git.cryptomilk.org`).                                                                                                                                        |
| Check                     | C only.                                              | Host only. Source states README: "Tests are run in a separate address space" (fork), POSIX build requirements.                                                                                                                                                                                                                     | No heap or C++ stated.                                                                                                                                                                                  | None.                                                                                                                                                                                                                                                                                                | LGPL-2.1 (`COPYING.LESSER`, "Version 2.1, February 1999")                                                                               | 0.15.2 (2020-08-07, NEWS)                                                                                                                   | Low: HEAD `35d9cc011faa` is 2026-07-13, but last release is 6 years old.                                                                                                                  |
| Criterion                 | C and C++ (C99, C++11).                              | Host only. Source states README: "Runs on Linux, FreeBSD, macOS, and Windows".                                                                                                                                                                                                                                                     | Not stated in README.                                                                                                                                                                                   | No mocking stated in README (inference: none).                                                                                                                                                                                                                                                       | MIT, `LICENSE` ("Copyright (c) 2015-2017 Franklin "Snaipe" Mathieu")                                                                    | v2.5.0 (2026-10-03)                                                                                                                         | Yes: HEAD `a4b2a6073404` 2026-11-14 after a long gap before the 2.5.0 release.                                                                                                            |
| cpptest (library)         | C++                                                  | Host                                                                                                                                                                                                                                                                                                                               | n/a                                                                                                                                                                                                     | None                                                                                                                                                                                                                                                                                                 | LGPL-2.1                                                                                                                                | 2.0.1 (2026-09-27)                                                                                                                          | No: archived, "closing down"                                                                                                                                                              |

### 1.3 Real projects and what they use

| Project                                                             | Framework                                                                                                                                                                                                                                 | Source                                                                                  |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Zephyr                                                              | Its own Ztest (C). Mocking with the Fake Function Framework (`zephyr/fff.h`, `DEFINE_FAKE_VOID_FUN`, `RESET_FAKE` in a `ZTEST_RULE`). Source states (`doc/develop/test/ztest.rst` at `v4.5.0`). Zephyr latest release 4.5.0 (2026-10-28). | `raw.githubusercontent.com/zephyrproject-rtos/zephyr/v4.5.0/doc/develop/test/ztest.rst` |
| ESP-IDF                                                             | Unity for target-based tests ("use the Unity unit test framework"), pytest-embedded to run them, CMock for mocks on the Linux host, with Ruby required on the host. ESP-IDF v6.1.1 (2026-11-16).                                          | `docs/en/api-guides/unit-tests.rst` at `v6.1.1`                                         |
| systemd                                                             | Own macros, no external framework: `TEST(name)`, `TEST_RET`, `DEFINE_TEST_MAIN(log_level)`, `ASSERT_*` and `assert_se` in `src/shared/tests.h` at `v260.7`.                                                                               | `raw.githubusercontent.com/systemd/systemd/v260.7/src/shared/tests.h`                   |
| U-Boot                                                              | Own C `ut` suites and a pytest harness (section 5).                                                                                                                                                                                       | docs.u-boot.org                                                                         |
| Linux kernel                                                        | KUnit (in-kernel C) and kselftest (userspace) (section 5).                                                                                                                                                                                | docs.kernel.org                                                                         |
| CppUTest users (gh_grep `find_package(CppUTest`)                    | snort3, weechat, Apache Celix.                                                                                                                                                                                                            | gh_grep search hits, not read in depth                                                  |
| cmocka users (gh_grep `#include <cmocka.h>`, `find_package(cmocka`) | edk2 (tianocore), glusterfs, OpenVPN, AFL++.                                                                                                                                                                                              | gh_grep search hits, not read in depth                                                  |
| Check users (gh_grep)                                               | xrdp, Slurm, vnstat, libnl, open62541.                                                                                                                                                                                                    | gh_grep search hits                                                                     |
| Criterion users (gh_grep)                                           | syslog-ng.                                                                                                                                                                                                                                | gh_grep search hit                                                                      |
| Unity users (gh_grep)                                               | ESP-IDF, cJSON.                                                                                                                                                                                                                           | gh_grep search hits                                                                     |

The gh_grep results show that a repo contains the include or CMake line; they do not prove the repo's whole
suite uses it. Treat them as "uses somewhere".

## 2. Memory and runtime checking

Pins: Valgrind 3.28.0, released 2026-10-23 (valgrind.org downloads page). LLVM docs read 2026-11-23 from
`clang.llvm.org/docs/` (latest tree, unpinned).

### 2.1 Valgrind tools

| Tool      | What it catches (source states)                                                                                                                                                                                                           | Slowdown (source states)                                                                                                                                       |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| memcheck  | Illegal heap, stack accesses; use of uninitialised values (`--track-origins=yes` finds the origin); double free and mismatched `malloc`/`new`/`new[]` against `free`/`delete`; overlapping `memcpy`, `strcpy`, `strcat` arguments; leaks. | "10-50 times slower than natively" (manual-core); quick start says "20 to 30 times" and "a lot more memory". `--track-origins` and `--read-var-info` add more. |
| helgrind  | POSIX pthreads API misuse, lock-order (potential deadlock) problems, data races, in C, C++, Fortran.                                                                                                                                      | Not stated in the pages read.                                                                                                                                  |
| drd       | Thread errors, data races; "similar to Helgrind but uses different analysis techniques".                                                                                                                                                  | Not stated in the pages read.                                                                                                                                  |
| massif    | Heap profiler: block lifetimes, utilisation, layout; optional stack measurement.                                                                                                                                                          | Not stated in the pages read.                                                                                                                                  |
| callgrind | Call-graph cache profiler (overlaps cachegrind).                                                                                                                                                                                          | Doc says extra options slow it "by approximately a factor of 2"; baseline not stated in the pages read.                                                        |

Build guidance from the Valgrind quick start: compile with `-g`; `-O0` is good, `-O1` is fine and much
faster, "Use of -O2 and above is not recommended as Memcheck occasionally reports uninitialised-value errors
which don't really exist."

### 2.2 Architectures

Source states (valgrind.org/info/platforms.html, current release 3.28.0): "ARM/Linux: supported since ARMv7",
"ARM64/Linux: supported for ARMv8", AMD64/Linux (primary target, up to AVX2), X86/Linux (maintenance mode, no
SSE4 or AVX), PPC32/PPC64/PPC64LE, S390X, MIPS32/MIPS64, RISCV64/Linux. Requires Linux kernel 3.0 or later and
glibc 2.5 or later. Inference: a musl-based Buildroot or Alpine target is not covered by the stated glibc
requirement; I did not find a statement on musl in the pages read, so verify per target.

### 2.3 Sanitizers

| Sanitizer        | Catches (source states, clang docs)                                                                                       | Cost (source states)                                                                                                                                            | Notes                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| AddressSanitizer | Out-of-bounds on heap, stack, globals; use-after-free; use-after-return; use-after-scope; double and invalid free; leaks. | "Typical slowdown 2x"; exits on first error; "does not produce false alarms".                                                                                   | Needs a rebuild. Integrates LeakSanitizer by default on supported platforms.            |
| LeakSanitizer    | Memory leaks.                                                                                                             | "Almost no performance overhead until the very end of the process."                                                                                             | Standalone or inside ASan. Suppression files support wildcards.                         |
| UBSan            | Out-of-bounds shifts and arrays, misaligned or null dereference, signed overflow, etc.                                    | "Small runtime cost, no impact on address space layout or ABI."                                                                                                 | `-fsanitize=undefined`; trap mode needs no runtime library.                             |
| ThreadSanitizer  | Data races.                                                                                                               | "5x-15x" slowdown, "5x-10x" memory. Supported: Linux aarch64, x86_64, powerpc64, powerpc64le; "Support for 32-bit platforms is problematic and is not planned." | So TSan is not usable on 32-bit ARM targets.                                            |
| MemorySanitizer  | Reads of uninitialised memory.                                                                                            | "Typical slowdown 3x".                                                                                                                                          | All code must be instrumented; libc calls that receive uninitialised data are reported. |

### 2.3b Valgrind versus sanitizer: choosing and interaction

Inference from the sources above (no source read states the interaction):

- Pick a sanitizer when you can rebuild: it is 2x for ASan against 10-50x for memcheck, and it catches stack and global
  overflows that memcheck cannot see because memcheck only knows heap block bounds. The "stack and globals" claim for
  ASan is source stated; the "memcheck does not see them" half is background knowledge.
- Pick Valgrind when you cannot rebuild (a cross-built vendor binary, a third-party library), when the target has 32-bit
  ARM (TSan unsupported) or when you need uninitialised-value tracking without rebuilding every dependency (MSan needs
  full instrumentation).
- Do not run a sanitizer-instrumented binary under Valgrind. Background knowledge; the Valgrind FAQ and manual pages
  read this session do not state it, so the skill should present it as common guidance and not as a quoted rule.

### 2.4 CI practice: exit codes and suppressions

Source states (valgrind.org manual-core, `--error-exitcode`): default 0; "Specifies an alternative exit code to
return if Valgrind reported any errors in the run", so a CI job needs `--error-exitcode=1` or similar to fail.
Suppressions: `--suppressions=/path/to/file.supp` (repeatable) and `--gen-suppressions=yes` to print a ready-made
suppression block ("by far the easiest way to add suppressions"). `--leak-check=full` is needed for per-leak
detail (background). `--trace-children=yes` is off by default; "confusion is still likely" (manual-core).

Mark as a gap: I did not read real CI configs that combine these flags.

## 3. Coverage

### 3.1 Tools

| Tool     | Role                                                                                                                                                                                                                                     | Source                                                                          |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| gcov     | GCC's coverage reader. Compile with `--coverage` (or `-fprofile-arcs -ftest-coverage`), run, then read `.gcda`/`.gcno`.                                                                                                                  | GCC docs Invoking Gcov                                                          |
| lcov     | Front end that captures gcov data and makes HTML.                                                                                                                                                                                        | `linux-test-project/lcov`; README at HEAD is short; I did not read its man page |
| gcovr    | Python tool that drives gcov and emits text, HTML, Cobertura, JSON. Docs: compile with `-fprofile-arcs -ftest-coverage -fPIC -O0`; "optimizations may merge lines of code"; `-fprofile-abs-path` (GCC 8 and later) avoids path problems. | gcovr.com guide `compiling.html`                                                |
| llvm-cov | LLVM equivalent. `clang++ -fprofile-instr-generate -fcoverage-mapping`, run (`LLVM_PROFILE_FILE=foo.profraw`), `llvm-profdata merge`, `llvm-cov show/report`.                                                                            | clang docs SourceBasedCodeCoverage                                              |

Release and licence pins (releases.atom, licence files read through WebFetch on the raw URL at the tag):

| Tool         | Latest release                       | Licence                                                                            |
| ------------ | ------------------------------------ | ---------------------------------------------------------------------------------- |
| lcov         | v2.6 (2026-10-03)                    | GPL-2.0 (`COPYING` at `v2.6`: "GNU General Public License, Version 2 (June 1991)") |
| gcovr        | 8.8 (2026-10-27)                     | BSD-3-Clause (`LICENSE.txt` at `8.8`: "Copyright (c) 2013-2026 the gcovr authors") |
| gcov, GCC 14 | part of GCC 14 (docs read at 14.2.0) | GPL                                                                                |
| llvm-cov     | part of LLVM                         | Apache-2.0 with LLVM exceptions (background)                                       |

gcovr's manual (gcovr.com stable, read 2026-11-23) lists `--gcov-executable` (use a particular gcov; for Clang
use `llvm-cov gcov`) and `--decisions` (decision coverage). I could not read the lcov man page (the
`man/lcov.1` path returned 404 at `v2.6`), so lcov's cross-compile options (`--gcov-tool`, `--base-directory`)
and whether lcov 2.x reports MC/DC are not verified.

### 3.2 Collecting on a cross target

Source states (GCC docs, "Data File Relocation to Support Cross-Profiling"): by default the program writes
`.gcda` files to the absolute build path, which "implicitly requires running the program on the same system as
it was built or having the same absolute directory structure". To relocate, set on the target `GCOV_PREFIX`
(prefix added to absolute paths) and optionally `GCOV_PREFIX_STRIP` (strip leading path components); the doc's
example `GCOV_PREFIX=/target/run GCOV_PREFIX_STRIP=1` writes `/target/run/build/foo.gcda`. Workflow
(inference from that doc): build on the host with `--coverage`, run the test binary on the target with
`GCOV_PREFIX` pointing at a writable directory, copy the `.gcda` tree back, and run gcov, gcovr or lcov on the
host against the build tree, with the cross toolchain's `gcov` binary (gcovr has `--gcov-executable`; background
knowledge, not read this session). The `.gcno` files stay in the build tree.

Bare-metal: GCC's "Profiling and Test Coverage in Freestanding Environments" page documents
`-fprofile-info-section` (default section name `.gcov_info`) so the data can be dumped without a filesystem
(source states: `__gcov_exit()` writes the files in a hosted environment).

Zephyr's coverage page (`doc/develop/test/coverage.rst` at `v4.5.0`) states two routes: gcov on "a real embedded
target or QEMU", or on the host by compiling for the POSIX architecture. It also states: "Support for gcov
collection and reporting is limited by available RAM size and so is currently enabled only for QEMU emulation of
embedded targets." The flow is `CONFIG_COVERAGE=y` plus `CONFIG_COVERAGE_DUMP=y`, the emulator prints a coverage
dump to the console, the log is saved, and `scripts/gen_gcov_files.py -i log.log` rebuilds the `.gcda` and
`.gcno` files. Inference: on an MCU, host (dual-target) coverage is the practical route; target coverage works
only for QEMU-sized setups or where a console dump fits.

### 3.3 MC/DC

Verified. Source states: the GCC 14.2.0 gcov manual documents `-g`/`--conditions` ("modified condition/decision
coverage ... requires you to compile the source with -fcondition-coverage") and the GCC 14.2.0 Instrumentation
Options document `-fcondition-coverage`; the GCC 13.3.0 gcov manual has no `--conditions` option (checked by
string search). The patch series is titled "Add condition coverage (MC/DC)" (gcc-patches, 2024-02). Clang:
source states `-fcoverage-mcdc` in addition to the profile flags ("MC/DC is an advanced form of code coverage
most applicable to the embedded space", clang SourceBasedCodeCoverage). Parasoft C/C++test CT reports MC/DC on
host and target (vendor page). Caveat from the GCC paper title: GCC's implementation is "masking MC/DC".
Inference: it is usable as evidence for DO-178C or ISO 26262 only if the toolchain is qualified; neither GCC nor
Clang docs claim qualification.

## 4. On-target and integration testing in embedded Linux

### 4.1 Yocto ptest and testimage

Source states (Yocto Project docs "test-manual", tip 6.1, read 2026-11-23):

- A ptest has the real test plus a `run-ptest` script. Output lines are `PASS: name`, `FAIL: name`, or `SKIP: name`
  (Automake format).
- Enable with `DISTRO_FEATURES:append = " ptest"` (builds and packages all ptest packages, adds none to the image). Add
  them with `EXTRA_IMAGE_FEATURES += "ptest-pkgs"` or `IMAGE_INSTALL:append = " e2fsprogs-ptest zlib-ptest"`.
- Files install under `/usr/lib/<package>/ptest`. Add `ptest-runner` to the image: it loops over suites, counts
  failures, and "If any of the `run-ptest` fails, `ptest-runner` returns '1'."
- `oe-pkgdata-util list-pkgs "*-ptest"` lists what is available.
- Runtime tests (`testimage`): `IMAGE_CLASSES += "testimage"` then `bitbake -c testimage <image>`. Tests are Python
  `unittest` modules in `meta/lib/oeqa/runtime/cases`, run mostly as commands over SSH; they run on QEMU or on real
  hardware. Selection via `TEST_SUITES`. `TEST_TARGET` defaults to `qemu`; hardware options include `simpleremote` and
  `SystemdbootTarget`. QEMU networking needs tap devices (`scripts/runqemu-gen-tapdevs`, `bitbake qemu-helper-native`)
  or `NOPASSWD` sudo; logs in `${WORKDIR}/testimage/qemu_boot_log` and `ssh_target_log`; `TEST_QEMUBOOT_TIMEOUT` raises
  the boot timeout.
- Not read: how `PTEST_ENABLED` is set per recipe (background: recipe-level variable set when the `ptest` distro feature
  is on); the task-brief mention of `PTEST_ENABLED` is not confirmed from the docs read.

### 4.2 Buildroot runtime tests

Source states (Buildroot manual 2026.11-rc2, section 22.7 "Using the runtime tests framework"): Python plus QEMU
framework with three goals (build a defined configuration, optionally check build output, optionally boot under
QEMU and check a feature). Entry point `support/testing/run-tests`; `-l` lists tests; tests can be run singly or
in groups. Buildroot 2026.11-rc2 appeared 2026-11-23 (releases.atom).

### 4.3 QEMU user mode

Source states (qemu.org user docs, master): "QEMU User space emulator", Linux user mode translates system calls and
signals and can create real host threads for `clone`; the command line is
`qemu-<arch> [-h] [-d] [-L path] [-s size] [-cpu model] [-g endpoint] ... program [arguments...]`, where `-L path` sets
the interpreter prefix and `-g` opens a GDB endpoint. Inference: `qemu-aarch64 -L <sysroot> ./test_bin` runs a
cross-built dynamically linked test against the target sysroot's libc. `QEMU_LD_PREFIX` is background knowledge, not
read. Limits (inference): no kernel features beyond the translated syscalls, so tests that need real devices, netlink
details, or kernel modules do not belong here; whether Valgrind works under qemu-user: I did not verify, and Valgrind
needs a native or full-system run.

## 5. Kernel and U-Boot

### 5.1 Linux kernel (docs.kernel.org, latest, read 2026-11-23)

| Item                  | Source states                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Division              | "The bulk of kernel tests are written using either the kselftest or KUnit frameworks." KUnit is "entirely in-kernel", white-box, for small self-contained parts (test code is part of the kernel). kselftest is mostly userspace and tests a feature through a syscall, device or filesystem; it cannot call kernel functions directly.                                                                                                                                                                                                                        |
| KUnit run             | `./tools/testing/kunit/kunit.py run` from the kernel tree. It defaults to UML (`ARCH=um`) and a `.kunit` build directory; `.kunitconfig` selects the Kconfig; `--kunitconfig=fs/ext4/.kunitconfig` runs a subsystem's file; `--raw_output` shows TAP; `kunit.py parse` parses a dmesg log; globs filter tests; `--arch=<arch>` runs under QEMU (`--qemu_config` for architectures without a built-in config). `CONFIG_KUNIT_ALL_TESTS` is a broad switch.                                                                                                      |
| kselftest run         | `make headers` then `make -C tools/testing/selftests run_tests`, or `make kselftest` at the tree root; `O=/tmp/kselftest` for a separate output directory; `TARGETS="size timers"` selects; `SKIP_TARGETS` excludes; `summary=1`; `FORCE_TARGETS=1` makes every target build or fail (without it the build succeeds if one target builds). Tests are "intended to be run after building, installing and booting a kernel".                                                                                                                                     |
| What a submitter runs | The kernel submit checklist asks for: `scripts/checkpatch.pl`; clean `sparse`; tests with the debug options (`CONFIG_PREEMPT`, `CONFIG_DEBUG_PREEMPT`, `CONFIG_SLUB_DEBUG`, `CONFIG_DEBUG_PAGEALLOC`, `CONFIG_DEBUG_MUTEXES`, `CONFIG_DEBUG_SPINLOCK`, `CONFIG_DEBUG_ATOMIC_SLEEP`, `CONFIG_PROVE_RCU` etc.) enabled together; builds with and without `CONFIG_SMP` and `CONFIG_PREEMPT`; lockdep coverage of all code paths; a test against the latest `linux-next` tag; builds on 32/64-bit and endianness variants. It does not mandate KUnit or kselftest. |

Not covered in these pages: KASAN, KCSAN and KMSAN usage detail (the testing overview mentions the
sanitizers; I did not read their pages), and the CI systems (KernelCI, 0-day).

### 5.2 U-Boot (docs.u-boot.org latest, read 2026-11-23; latest tag seen `v2027.01-rc2`, 2026-11-09)

| Item         | Source states                                                                                                                                                                                                                                                                                                                                     |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Entry        | `make check` runs "most tests on sandbox", and "only the pytest suite is run using this command". `make qcheck` skips tests marked `@pytest.mark.slow`.                                                                                                                                                                                           |
| Sandbox      | U-Boot built as a user-space program, so tests run "without needing target hardware"; "all the tests share a small number of executables".                                                                                                                                                                                                        |
| `ut` command | `./u-boot -T -c "ut dm gpio"` runs one suite or test; `-T` selects the test device tree (`test.dts`); without it tests fail on missing devices.                                                                                                                                                                                                   |
| pytest       | `test/py`; `./test/py/test.py --bd sandbox --build`, `-k <name>` selects; HTML log in `build-sandbox/test-log.html`; runs on sandbox or real hardware by talking to the console through hook scripts; requires Python 3 and `pip install -r test/py/requirements.txt`.                                                                            |
| Types        | Two kinds: Python tests in `test/py/tests` (talk through the command line, sandbox or hardware) and C tests in `test/` (`ut`).                                                                                                                                                                                                                    |
| Submitter    | "If you change or enhance any U-Boot subsystem, you should write or expand a test and include it with your patch series submission." Use `b4 prep --check` (wraps `scripts/checkpatch.pl`) and `b4 send`. U-Boot treats `checkpatch.pl` warnings as advice ("Checkpatch is a tool that can help you find some style problems, but is imperfect"). |

Gap: I did not read the GitLab CI configuration or a statement that patches must pass CI before merge.

## 6. MCU firmware testing

Evidence labels: **doc** is a project's or vendor's own documentation. **expert** is a named practitioner's
published opinion or worked example (useful, but one voice). **inference** is my conclusion from the sources.
No source I read gives numbers for how many tests belong at each level; the proportions below are inference
and the notes say so.

Sources and ages: Grenning, "Test-Driven Development for Embedded C", conference paper, copyright 2014, 23 pages
(`wingman-sw.com/papers/EmbeddedTdd-Grenning-v1r1.pages.pdf`, page numbers below are PDF pages; the book
(Pragmatic Bookshelf, 2011) is not free and was not read). Memfault Interrupt posts by Tyler Hoffman: unit-test
basics 2019-10-08 (CppUTest 3.8), mocking 2020-05-12, Renode 2020-07-07, intro to Renode (undated in the text I
read). VanderVoord (Unity and CMock co-author), "Unit Test How?" series, 2015, `vandervoord.net`. Embedded
Artistry (Phillip Johnston), 2020-08-03 and 2021-10-25.

### 6.1 Test strategy: what runs where

Grenning describes five stages with decreasing frequency (expert, paper pp. 19-20):

| Stage | Where it runs                          | Problems it is likely to find (his table)                                                            |
| ----- | -------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1     | TDD microcycle on the development host | Logic, design, modularity, interface, boundary conditions                                            |
| 2     | Compile for the target processor       | Compiler and library compatibility (language features, headers, prototypes)                          |
| 3     | Run tests on evaluation hardware       | Processor execution problems (compiler and library bugs), portability (word size, alignment, endian) |
| 4     | Run tests in the target hardware       | Stage 3 problems plus hardware integration and misunderstood hardware specifications                 |
| 5     | Acceptance tests                       | Stage 4 problems plus misunderstood feature specifications                                           |

He states that the cycle works when build and test takes "only a handful of seconds", so the microcycle moves
off the target. Stage 3 "sometimes ... makes up for very constrained memory in the target" and "is not always
needed". Stages 2 to 4 "should be executed automatically upon checkin or at least nightly". He calls building
the same code for host and target "dual-targeting" and says potential differences in execution environments
should not discourage it.

Projects that document the same split (doc):

- Zephyr: `unit_testing` pseudo-board builds only the module under test plus Ztest into a native host executable ("The
  Zephyr kernel and operating system are not built at all"); `native_sim` builds the whole OS for the host; QEMU and
  other simulators and real boards run through Twister (`ztest.rst` and Twister docs at `v4.5.0`; Twister docs read
  2026-11-23). Unit tests are Linux-only ("To run unit tests on Windows or macOS it is necessary to use containers or
  Virtual Machines").
- ESP-IDF: Unity tests on the chip, Linux-host tests with CMock mocks ("only a small fraction of IDF components support
  them"), and pytest-embedded runs on the target, on the Linux host, and in QEMU (`unit-tests.rst`,
  `esp-idf-tests-with-pytest.rst` at `v6.1.1`).

Inference on proportion: most tests on the host (fast, no hardware), a smaller layer of emulator boots for
integration paths that need the real startup and peripherals, and a thin hardware smoke layer for what only
silicon shows (timing, analog, DMA, clock trees, errata). Grenning's frequency axis supports "more host runs,
fewer hardware runs" but gives no ratio.

### 6.2 Seams for hardware-facing code

| Seam                                                                        | How it works                                                                                                                           | Source                                                                                                                                                                                                                                                                                                                                                                                                                                        | Trade-offs (inference unless marked)                                                                                                                                                                                                           |
| --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hardware abstraction layer (function-pointer table, vtable, abstract class) | Hardware-independent modules call an interface; hardware-dependent modules implement it; tests supply a fake implementation.           | Embedded Artistry "Virtual Devices" (expert): split into "hardware-dependent" modules that implement abstract interfaces and "hardware-independent" modules that use them; a follow-up says you can develop and test drivers on the PC first.                                                                                                                                                                                                 | Needs a production-code change and a design decision per interface; adds an indirection (small RAM and call cost); the best long-term shape. A badly shaped HAL leaks hardware details.                                                        |
| Link-time substitution                                                      | The test build links `mock_*.c` or `fake_*.c` instead of the real dependency object; no production change.                             | Memfault mocking post (expert): the unit-test Makefile lists the module under test plus `mocks/mock_littlefs.cpp` and `fakes/fake_mutex.c`; link errors name each missing symbol. CMock (doc, `CMock_Summary.md`): for each prototype in a header you get a generated function "that you can link to instead of your real" one.                                                                                                               | Cheapest way to start on legacy code; works for C because symbols are global; one fake per link set, so each test binary needs its own file list; weak for static functions and inlined code.                                                  |
| Preprocessor substitution                                                   | `#ifdef TEST` swaps a header or macro for a test version.                                                                              | VanderVoord (expert): register headers are rebuilt under `TEST` so registers become RAM variables.                                                                                                                                                                                                                                                                                                                                            | Works without touching call sites but makes the production header more complex and can drift from the real one.                                                                                                                                |
| Register-level fake                                                         | A struct, array or plain variables stand in for peripheral memory; the test writes the "hardware" state and reads what the code wrote. | VanderVoord (expert): "remap all those registers [to] regular variables"; address "isn't important"; simulators treat registers as a pool of RAM. Tedious ("Most modern microcontrollers have complex register sets"). For registers that change on read (status flags, FIFO data), a macro returns the next value from a queue the test sets up; he calls this too complex to use "regularly" ("We'll save this one for special occasions"). | Exercises real driver code including bit manipulation, so it catches register-level mistakes; it does not model hardware behaviour (read-to-clear, write-one-to-clear, timing), so tests encode your belief about the datasheet, not the chip. |
| Fake versus mock                                                            | Fake: working simplified implementation. Stub: canned values. Mock: records and verifies calls and returns scripted values.            | Memfault (expert): "Fakes are a working implementation", "Stubs are a trivial implementation that returns canned values"; use mocks when a stub is not enough but "modeling the subsystem behavior perfectly in a fake" is not worth it; his experience: reaching 100% branch coverage usually needs mocks because each `buffer == NULL` branch must be forced.                                                                               | Mocks pin down call sequences, so they break on refactors (inference); fakes survive refactors but cost effort to write correctly.                                                                                                             |

Mock tooling in the sources: CppUMock, the Fake Function Framework (`fff`, header-only, C, which Memfault says
generates mocks despite its name; Zephyr bundles it as `zephyr/fff.h`), and CMock (Ruby generator, doc).

### 6.3 Adding tests to an untested firmware codebase

- Grenning (expert, paper p. 21): "You've got legacy code? Try to get the legacy code into your test harness. Write
  tests for the current behavior. Test drive the new behavior. Changing legacy code is dangerous. It's best to go
  carefully." He cites Feathers, Working Effectively with Legacy Code (2004; I did not read the book; the seam names
  "link seam" and "preprocessing seam" are background knowledge, and the link and preprocessor rows above match them).
- Embedded Artistry (expert, 2021-10-25): "Going back and writing unit tests for all of your pre-existing code doesn't
  make economic sense." Bring old code under test "whenever you're going to change it". "It doesn't have to be fully
  tested ... 'big fat tests' that exercise existing code end-to-end", then "refactor the module to improve its
  testability later". The author notes that most of their own code was tested only on the device.
- Where to start: code with no hardware dependency. Grenning calls his circular buffer "one of the easier things to test
  because there are no external dependencies"; Memfault's worked example tests a protocol parser; Grenning's Zune
  example (paper pp. 4-5) is a pure date-conversion loop that hangs on the 366th day of a leap year, found by one test.
  Inference: parsers, state machines, checksums, ring buffers, fixed-point and unit conversion, scheduling logic and
  command dispatch are the usual first targets.
- Breaking hardware dependencies one at a time (Memfault, expert): compile the module with the test, read the linker's
  undefined symbols, and add one stub, fake or mock per symbol until it links. Each added double can be replaced with a
  better one later.

### 6.4 Timing, interrupts and concurrency

Documented facts are thin. What I found:

- Zephyr's Ztest includes a stress tool (`ZTRESS_EXECUTE`) that runs several contexts (timer, threads) with randomised
  sleeps and adjusts CPU load to raise the chance of preemption; it advises a much higher tick rate under QEMU
  (`ztest.rst`, doc). Inference: this runs inside the Zephyr kernel, so it needs `native_sim`, QEMU or hardware, not the
  bare `unit_testing` board.
- Valgrind's Helgrind and DRD target POSIX pthreads programs (doc, section 2). Inference: they and TSan check host code
  that uses pthreads; they cannot see interrupt handlers or RTOS tasks on a target.
- Fake time and interrupts, inference only (no primary source read): put the clock behind a function (`now_ms()`) or HAL
  interface and let the test advance it; call the interrupt service routine as an ordinary function from the test after
  setting the fake register state (VanderVoord's register fakes make the state settable); keep the ISR thin so the logic
  is in a pure function tested with controlled inputs. A secondary web article (HelpMeTest, "Testing RTOS Tasks and
  Interrupts in Embedded Firmware", seen only through a search summary, low authority) says the same and admits it will
  not catch every race.
- Limits of host tests (inference): no preemption or interrupt latency, no memory ordering of the real core, no
  peripheral timing, and word size, alignment and endianness differ unless the host build is `-m32` or equivalent
  (Grenning's stage 3 table lists those as target-found problems, doc/expert).

### 6.5 Emulation

| Tool                                                                                    | What it models and how it is used                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Honest limits                                                                                                                                                                                                                                                                                                           |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Renode (Antmicro; MIT licence, `LICENSE` at `b3664392f23a`; release 1.17.1, 2026-11-23) | Whole-machine emulator with a Robot Framework integration: `renode-test my_test.robot` starts Renode, runs the suite, and writes `robot_output.xml`, `log.html`, `report.html` (doc, `renode.readthedocs.io` testing page). Memfault (2020) says it emulates "many peripherals of the board, including the UART, SPI, I2C, RAM, ROM, and GPIO" and runs under GitHub Actions. Zephyr Twister supports `renode` as a simulation and takes `uart` and `resc` keys for the platform (doc). | Peripheral models are per chip. In Memfault's intro post the firmware wrote to unmapped memory ("WriteByte to non existing peripheral") because "the renode model does not implement" the CCM RAM, and the author had to extend the machine description. Tests that depend on timing accuracy are doubtful (inference). |
| QEMU system mode, Arm M-profile                                                         | Supports Cortex-M0, M4, M33 machines (doc, qemu.org Arm page). The STM32 machines list supported devices (ADC, EXTI, USART, SPI, SYSCFG, timer, RCC for "reset and enable only") and a "Missing devices" list.                                                                                                                                                                                                                                                                          | "Even with fifty boards QEMU does not cover more than a small fraction of the Arm hardware ecosystem" (doc). Machines are generic boards, so vendor peripherals usually are not present.                                                                                                                                |
| Zephyr's list of simulators                                                             | Twister supports `qemu`, `simics`, `xt-sim`, `renode`, `nsim`, `mdb-nsim`, `tsim`, `armfvp`, `native`, `custom` (doc). Twister notes that instruction-accurate simulation "does it slowly" and offers `--timeout-multiplier`.                                                                                                                                                                                                                                                           | Not every board has a simulator; tests marked `build_only` are not run.                                                                                                                                                                                                                                                 |
| Vendor simulators                                                                       | Not researched beyond the Zephyr list above.                                                                                                                                                                                                                                                                                                                                                                                                                                            | Gap.                                                                                                                                                                                                                                                                                                                    |

Inference on where emulation falls short: it validates startup, scheduling, protocol and driver logic against
a model, so it cannot find errata, analog behaviour, power, real bus electrical faults, or DMA and cache
subtleties; and it passes or fails against the model's author's reading of the datasheet.

### 6.6 Hardware in the loop on a small budget

- Zephyr Twister (doc): `west twister --device-testing --device-serial /dev/ttyACM0 -p <board> -T tests/...` runs on one
  board; `--generate-hardware-map` plus `--hardware-map map.yml` runs on several. Supported flash runners for the
  hardware map: pyocd, nrfjprog, jlink, openocd, dediprog. `--device-serial-pty` takes a script that relays messages for
  devices without a serial port. Fixtures describe special wiring; `run_with_fixture_only` reserves a board; a
  quarantine list skips tests that can wedge a board; the pytest harness supports multi-core and multi-device tests;
  reports include JUnit XML.
- probe-rs plus `embedded-test` (doc, docs.rs): the target runs a harness; `probe-rs run` reads the test list from the
  ELF, flashes all tests once, resets the device before each test, tells the device which test to run through
  semihosting `SYS_GET_CMDLINE`, and reads the verdict from semihosting `SYS_EXIT`. It targets Rust (riscv, arm,
  xtensa); the mechanism (semihosting for selection and verdict, debug probe for flashing) is language-neutral
  (inference).
- Unity: `UNITY_OUTPUT_CHAR(a)` redirects results to a UART or other channel on a target without stdout (doc,
  `UnityConfigurationGuide.md`). Inference: a serial-port reporter plus a host script that parses Unity's
  `file:line:test:PASS|FAIL` lines is the cheapest HIL runner for C.
- ESP-IDF (doc): `pytest-embedded` drives target tests, Linux-host tests (`target: linux`) and QEMU (`@pytest.mark.qemu`).
- Yocto `testimage` on real boards (doc): `TEST_TARGET` values `simpleremote` (a board already running) and
  `SystemdbootTarget`, with power control hooks; for Linux-class hardware rather than MCUs.
- Cost warning from Memfault (expert, 2020): automated testing on real hardware is "hard"; it needs "flashers and power
  supplies, and software to orchestrate the tests and capture results"; emulation with Renode is offered as the cheaper
  alternative.
- Continuous integration with a device on a desk (inference): a self-hosted runner attached to the board, a serial port
  and a debug probe; the CI job flashes, resets, reads results and fails on a non-zero verdict. I read no primary source
  that prescribes this layout; a DIY HIL guide (EmbeddedCI) appeared in search results but was not read.

### 6.7 Vendor and project guidance read

Zephyr (doc, above) and ESP-IDF (doc, above) are the two vendor-backed frameworks read in full. I did not read
guidance from ST, NXP, Nordic, TI or Microchip (a Nordic search failed on rate limits). ESP-IDF states the
limits plainly: host tests with mocks exist for few components and are "still under development".

### 6.8 Practices for an untested MCU project

01. Build a host test target next to the firmware build and make it run in CI before writing tests. Pick one framework:
    CppUTest or Unity with Ceedling for plain C, Zephyr's `unit_testing` board inside Zephyr, Unity with pytest-embedded
    inside ESP-IDF (doc: Zephyr, ESP-IDF; Memfault, Grenning stage 1).
02. Test pure logic first: parsers, state machines, ring buffers, fixed-point and conversion code. Needs no doubles
    (expert: Grenning, Memfault; Grenning's Zune example).
03. Test code when you change it, not all at once. Write a "big fat" characterization test of today's behaviour before
    the change, then drive the new behaviour (expert: Grenning p. 21, Embedded Artistry 2021).
04. Cut hardware dependencies one at a time: compile the module with its test, read the undefined symbols, add one stub,
    fake or mock per symbol; prefer link-time substitution first because it needs no production change (expert: Memfault;
    CMock doc).
05. For drivers that must stay register-based, remap registers to RAM variables under a `TEST` build and use a
    queue-of-values macro only for the few registers that change on read (expert: VanderVoord).
06. When you next change a driver, add a narrow interface (function-pointer table or abstract class) between
    hardware-independent and hardware-dependent code (expert: Embedded Artistry).
07. Keep a CI job that compiles the same sources for the target, so host and target builds do not drift (expert: Grenning
    stage 2). Run host tests under AddressSanitizer and UBSan, and collect gcov coverage on the host (sections 2 and 3;
    inference for MCU use).
08. Add one emulator smoke test: boot the real image in Renode or QEMU and assert on UART output with Robot Framework or
    a script. Expect to add missing peripheral models (doc: Renode testing page; expert: Memfault).
09. Add one hardware smoke job on a bench board: flash, reset, read the serial verdict, nightly at first (doc: Zephyr
    Twister hardware map or probe-rs; expert: Grenning "at least nightly").
10. Grow by defect: every field bug gets a regression test at the lowest level that can reproduce it (inference;
    consistent with Grenning's Zune example).

## 7. Static analysis as part of testing

| Tool               | What it is                                                                                       | Pins                                                                                                                      | Notes (source states unless marked)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cppcheck           | Static analyser for C and C++.                                                                   | 2.22.0 (2026-09-19); repo moved to `cppcheck-opensource/cppcheck`, HEAD `21459e9c4fb9` (2026-11-22); GPL-3.0 (`COPYING`). | README: "Despite the name, Cppcheck is designed for both C and C++"; "a hobby project with limited resources". Inference: needs no build; lower false-positive risk than a path-sensitive analyser, finds fewer defects. I did not read the manual or the MISRA addon notes.                                                                                                                                                                                                                                                                                                                                           |
| clang-tidy         | Clang-based linter and checker framework.                                                        | LLVM docs read 2026-11-23.                                                                                                | "has its own checks and can also run Clang Static Analyzer checks"; checks chosen with `-checks=` globs (positive add, negative remove). Needs a compile database (background).                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| GCC `-fanalyzer`   | Interprocedural path analysis in the compiler.                                                   | GCC docs, "Options That Control Static Analysis".                                                                         | "neither sound nor complete: it can have false positives and false negatives"; heuristics "can be defeated by sufficiently complicated code" (`-Wanalyzer-too-complex`). Warnings include double-free, deref-before-check, allocation-size, div-by-zero, leaks, uninitialised copies to output. Support for C++ is not stated in the page I read (gap).                                                                                                                                                                                                                                                                |
| Parasoft C/C++test | Commercial platform: static analysis, unit test, coverage, runtime analysis. Role is compliance. | Vendor page read 2026-11-23, no version.                                                                                  | Vendor states: static analysis against MISRA C:2025, MISRA C++:2023, AUTOSAR C++14, CERT, CWE, OWASP; unit testing with a proprietary framework (stubbing, auto-generated tests, host, virtual and target) and integration with GoogleTest, Boost.Test, CppUnit; coverage including MC/DC on host and target; runtime analysis for memory leaks, corruption and overflows on embedded targets; "TÜV SÜD-certified" for ISO 26262, IEC 61508, DO-178C, IEC 62304, EN 50128. A "C/C++test CT" edition adds coverage and requirements traceability to open-source frameworks. Marketing text, not independently verified. |

Inference for the skills: static analysers find different defects from tests, so they complement them; none of
them can verify behaviour. The kernel's sparse and Coccinelle, compiler hardening flags, and fuzzing are covered
elsewhere and not repeated here.

## Proposed tool set

### Embedded Linux userspace (Yocto or Buildroot, cross-built C and C++)

| Need           | Default                                                                                                                                                                                       | Conditions that change it                                                                                                                                                                                                                                                                                                         |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Unit framework | cmocka for C (mocking built in, no `fork()`, Apache-2.0, 2.0.2); GoogleTest with GoogleMock for C++ (needs C++17; gmock mocks virtual methods only).                                          | Use Check or Criterion only when tests need per-test `fork()` isolation and run on the host (both fork-based or host-only). Use CppUTest when you want leak detection in the framework or already use it. Use the project's own framework when the upstream already has one (systemd macros, `ptest` suites that upstream ships). |
| Memory checker | AddressSanitizer plus UBSan (and LeakSanitizer) on host-built tests; Valgrind memcheck on target (armv7 and aarch64 supported) for cross-built binaries that cannot be rebuilt.               | Check Valgrind's glibc 2.5+ requirement on musl systems. TSan is not available on 32-bit targets. Use Helgrind or DRD for pthreads races when TSan is unavailable. Do not combine a sanitizer build with Valgrind (background).                                                                                                   |
| Coverage       | gcov plus gcovr on the host; on target set `GCOV_PREFIX` (and `GCOV_PREFIX_STRIP`), copy the `.gcda` tree back, and report on the host with the cross toolchain's gcov (`--gcov-executable`). | MC/DC: GCC 14 `-fcondition-coverage` with `gcov --conditions`, or Clang `-fcoverage-mcdc`. Under Yocto run on-target suites with `ptest-runner` and the image's `testimage` on QEMU; under Buildroot use `support/testing/run-tests`; for a single cross binary use `qemu-<arch> -L <sysroot>`.                                   |

### MCU firmware

| Need           | Default                                                                                                                                                           | Conditions that change it                                                                                                                                                                                                                                                              |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Unit framework | Host tests of the same sources: Unity with CMock (via Ceedling) for C; CppUTest with CppUMock for C or C++ code that benefits from built-in leak detection.       | Zephyr: Ztest with Twister (`unit_testing` board for modules, `native_sim` for OS-level, then QEMU, Renode or hardware). ESP-IDF: Unity plus pytest-embedded. cmocka if you want Apache-2.0 and no fork. Catch2 or doctest only for C++ with exceptions available and a host-only run. |
| Memory checker | ASan plus UBSan on the host test build; CppUTest's leak counter for heap discipline.                                                                              | Valgrind on the host build where sanitizers are missing. On the target there is no equivalent; use fixed-size pools, canaries and the stack-size reports your RTOS provides (inference).                                                                                               |
| Coverage       | gcov plus gcovr on the host build.                                                                                                                                | Target coverage only where Zephyr-style console dump or `-fprofile-info-section` fits in RAM; MC/DC via GCC 14 `-fcondition-coverage` on host; certified projects use a qualified commercial tool (Parasoft or similar).                                                               |
| Beyond host    | Renode (Robot Framework) or QEMU smoke test of the real image, then a bench-board HIL job (Twister hardware map, `probe-rs` or a serial parser for Unity output). | Pick QEMU only when the board has a machine model; otherwise Renode.                                                                                                                                                                                                                   |

### Kernel and U-Boot

| Need           | Default                                                                                                                                                                                                                                                                                                                                                            | Conditions that change it                                                                                                                                                                                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Unit framework | Kernel: KUnit for in-kernel units (`tools/testing/kunit/kunit.py run`, UML by default, `--arch` for QEMU) and kselftest for user-visible behaviour (`make -C tools/testing/selftests TARGETS=... run_tests`). U-Boot: sandbox `ut` suites (`./u-boot -T -c "ut dm gpio"`) and `test/py` (`./test/py/test.py --bd sandbox --build`), `make check` or `make qcheck`. | Run `test/py` against real hardware with hook scripts when a bug is board-specific. A submitter writes or extends a test with a U-Boot patch, runs `b4 prep --check`, and for the kernel runs `checkpatch.pl`, `sparse`, and the debug-config builds from the submit checklist. |
| Memory checker | Kernel: the in-kernel sanitizers (KASAN, KCSAN, KMSAN, UBSAN are named in the kernel testing overview; I did not read their pages). U-Boot sandbox is a user-space program, so host tools could apply (inference; not stated in the docs read).                                                                                                                    | Valgrind and ASan are not meaningful for the kernel itself.                                                                                                                                                                                                                     |
| Coverage       | Kernel gcov with `CONFIG_GCOV_*` (a search snippet mentions `CONFIG_GCOV_CONDITION_COVERAGE`; not read). U-Boot: not verified.                                                                                                                                                                                                                                     | Verify before the skill states a command.                                                                                                                                                                                                                                       |

## What I could not verify

- Valgrind: slowdown figures for Helgrind, DRD and Massif; musl support; behaviour on a sanitizer-built binary (no
  source read states it); real CI configs that combine `--error-exitcode` and `--suppressions`; whether Valgrind runs
  under qemu-user.
- Sanitizers: MSan's supported architectures, and exact ASan platform lists (the clang pages gave slowdowns and bug
  classes only).
- Coverage: the lcov man page (404), lcov's cross options and MC/DC support, the gcovr cross-compile guide, and the
  Zephyr path for host coverage with `native_sim`. LLVM coverage flow on a cross target.
- QEMU user mode: `QEMU_LD_PREFIX` (background only) and limits on threads and `ioctl` coverage for real tests.
- Yocto: how `PTEST_ENABLED` is set per recipe (the brief named it; the docs read name `DISTRO_FEATURES` and `ptest-pkgs`).
- Kernel and U-Boot: the sanitizer pages, kernel gcov setup, U-Boot coverage, and whether U-Boot CI must pass before merge.
- Frameworks: exceptions and RTTI needs of CppUTest; whether Criterion and Catch2 have any mocking (I found none, but
  did not read their full docs); GoogleTest on an MCU (not supported per the docs read, but no explicit statement); the
  gh_grep usage hits were not opened.
- cpptest library: the original author and first-release date; the Sourceforge home page is Cloudflare-protected for the
  crawl tool, so it was read through WebFetch only.
- MCU practice: Feathers' book and Grenning's book (not free, not read; only Grenning's free paper, pages 1-8 and 19-23
  of 23, was read); Embedded Artistry's testable-systems course (paid); vendor guidance from ST, NXP, Nordic, TI and
  Microchip; vendor simulators; a primary source for fake clocks and interrupt testing; the EmbeddedCI DIY HIL guide.
- Parasoft: all claims are vendor marketing text; no version or pricing read.
- Memfault posts are 2019-2020; their tool versions (CppUTest 3.8, Renode 1.9) are old.
- Formatting: the notes use soft-wrapped prose; the repository's Markdown rule (trailing-backslash hard breaks) was not
  applied because the move into `docs/evaluations/` is yours.
