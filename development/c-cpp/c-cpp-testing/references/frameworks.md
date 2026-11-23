# Test Frameworks for C and C++

Licence, target support, heap and C++ needs, mocking, and maintenance for each framework the skill names. The skill
body picks a default by place and explains the name "cpptest". This file adds the detail for a choice or a check.

The data is as of 2026-11-23, from each project's repository, licence file, and release feed. "Release" is the latest
release entry. "HEAD" is the default branch on the date given. "Inference" marks a conclusion that no documentation
states.

## Contents

- Comparison
- Notes per Framework
- Real Projects and Their Frameworks
- The cpptest Library
- Parasoft C/C++test

## Comparison

| Framework                 | Licence      | Runs on an MCU target                               | Heap, exceptions, RTTI, language level                             | Mocking                                       | Release and maintenance                                        |
| ------------------------- | ------------ | --------------------------------------------------- | ------------------------------------------------------------------ | --------------------------------------------- | -------------------------------------------------------------- |
| CppUTest                  | BSD-3-Clause | Yes when built with its library-disable options     | Leak detector replaces `new`, `delete`, and `malloc` with a header | CppUMock, in `CppUTestExt`                    | v4.0 (2020-05-27); HEAD 2026-11-03; slow release cadence       |
| Unity                     | MIT          | Yes                                                 | No heap use stated; C only                                         | Through CMock                                 | v2.7.0 (2026-07-16); HEAD 2026-10-31                           |
| CMock                     | MIT          | Mocks run on target or host; generator needs Ruby   | Mock runtime is C                                                  | Header-driven generation for Unity            | v2.7.0 (2026-07-16); HEAD 2026-10-17                           |
| GoogleTest and GoogleMock | BSD-3-Clause | Host only in practice (inference)                   | C++17 minimum; exceptions and RTTI autodetected                    | Virtual methods only                          | v1.18.0 (2026-08-10); HEAD 2026-11-17                          |
| Catch2                    | BSL-1.0      | Host (inference)                                    | C++14 minimum; exceptions on by default, experimental off switch   | None                                          | v3.16.1 (2026-10-08); HEAD 2026-11-15                          |
| doctest                   | MIT          | Host (inference)                                    | C++11; exceptions can be disabled by a macro                       | None                                          | v2.5.3 (2026-07-06); master HEAD 2026-03-27; moderate activity |
| cmocka                    | Apache-2.0   | Yes: needs only the standard C library, no `fork()` | C99; no heap or C++ need stated                                    | Built in: `will_return`, `expect_*`, `mock()` | 2.0.2 (2026-01-12) on GitLab; maintained                       |
| Check                     | LGPL-2.1     | No: host only, tests run in a forked process        | C only                                                             | None                                          | 0.15.2 (2020-08-07); HEAD 2026-07-13; low activity             |
| Criterion                 | MIT          | No: host only                                       | C99 and C++11                                                      | None stated (inference: none)                 | v2.5.0 (2026-10-03); HEAD 2026-11-14                           |
| Zephyr ztest with FFF     | Unverified   | Yes, inside Zephyr, on boards and simulators        | C; part of the Zephyr tree                                         | FFF: `DEFINE_FAKE_VOID_FUN`, `RESET_FAKE`     | Ships with Zephyr 4.5.0 (2026-10-28)                           |
| systemd test macros       | Unverified   | Not applicable: host tests of systemd itself        | C                                                                  | None                                          | In `src/shared/tests.h` at v260.7                              |

## Notes per Framework

### CppUTest

Source: `COPYING` and `CMakeLists.txt` at commit `42feb8740bea`. The build options `CPPUTEST_STD_C_LIB_DISABLED`,
`CPPUTEST_STD_CPP_LIB_DISABLED`, and `CPPUTEST_MEM_LEAK_DETECTION_DISABLED` exist, so the framework can be built without
a hosted C library or STL. That a target build works with those set is an inference, and Grenning's paper uses it on
a host. The README says that GCC builds use a simple `new` and `delete` count in the overridden operators. The sources
do not state its exception and RTTI needs. The tests are C++, and C code is tested through wrappers. Consumers track the
rolling tag `latest-passing-build` (2026-07-30) or a commit, because the last numbered release is six years old.

### Unity, CMock, and Ceedling

Unity's configuration guide (`docs/UnityConfigurationGuide.md` at `54f864cf6027`) covers target use. Output goes through
`UNITY_OUTPUT_CHAR(a)` for a target without stdout. `UNITY_EXCLUDE_SETJMP` serves a target without setjmp, at the cost
of custom helper functions and CMock. The Ruby scripts are optional. CMock parses C headers and generates mocks. Its
generator needs Ruby on the development host, and its self-tests need `bundle install` and `rake`. Ceedling is the build
manager that bundles Unity and CMock. Unverified: check Ceedling's licence and release before relying on them. ESP-IDF
requires Ruby on the host for the same reason.

### GoogleTest and GoogleMock

The README requires at least C++17. The documentation lists supported operating systems and compilers, and no MCU, and
it does not state that an MCU is unsupported. GoogleMock mocks virtual methods. Its guide says mocking non-virtual
methods with templates is "much more involved". Mocking a C free function therefore needs a seam: a wrapper interface
or link-time substitution.

### Catch2 and doctest

Catch2 version 3 is compiled, not header-only. Its documentation names `CATCH_CONFIG_DISABLE_EXCEPTIONS` as an
experimental switch. doctest has `DOCTEST_CONFIG_NO_EXCEPTIONS` and a variant that keeps all assertions. It also
allows tests inside production source files. Its latest release tag is newer than its master HEAD, so releases come
from another branch or tag.

### cmocka

Take the upstream from GitLab (`gitlab.com/cmocka/cmocka`) or `git.cryptomilk.org`. The GitHub mirror `clibs/cmocka`
stopped at 1.1.5 (2022-09-05), so a package that pins the mirror is old. Version 2.0.0 requires C99. The project lists
TAP 14, Subunit, and xUnit XML output, and signal exception handling.

### Check and Criterion

Both fit host-only C tests that need a separate process per test. Check states that tests run in a separate address
space and has POSIX build requirements. Criterion's README lists Linux, FreeBSD, macOS, and Windows. Its HEAD is active
after a long gap before the 2.5.0 release.

### Zephyr ztest and FFF

Zephyr documents ztest at `doc/develop/test/ztest.rst` (v4.5.0). Mocking uses the Fake Function Framework through
`zephyr/fff.h`, with `RESET_FAKE` in a `ZTEST_RULE`. The twister runner is described in the firmware reference.

### systemd Test Macros

systemd has no external framework. It uses `TEST(name)`, `TEST_RET`, `DEFINE_TEST_MAIN(log_level)`, and `ASSERT_*` and
`assert_se` macros from `src/shared/tests.h`. Follow these when you add a test to systemd, as the skill body says to
use the tree's own setup.

## Real Projects and Their Frameworks

These show where each framework appears. Search hits prove an include or CMake line, not that the whole suite uses it.

- CppUTest: snort3, weechat, Apache Celix.
- cmocka: edk2, glusterfs, OpenVPN, AFL++.
- Check: xrdp, Slurm, vnstat, libnl, open62541.
- Criterion: syslog-ng.
- Unity: ESP-IDF, cJSON.

## The cpptest Library

The skill body says the library is unmaintained and archived. The detail: it is "CppTest", a portable C++ unit test
library on Sourceforge and `github.com/cpptest/cpptest`, licensed LGPL 2.1. Its NEWS file at commit `bc01feae2084` says
that release 2.0.1 was the last release and the project is closing down. It asks users to migrate to an alternative.
The GitHub repository was archived on 2026-09-27, the date of release 2.0.1. The Sourceforge home page still says
"Latest version: 2.0.0", so it is stale. Output formats are simple text, compiler-like, and HTML.

## Parasoft C/C++test

The skill body names it as a commercial product. The claims below are the vendor's own marketing text as of
2026-11-23, with no version or price. Unverified: check each claim with the vendor before relying on it.

- Static analysis against MISRA C:2025, MISRA C++:2023, AUTOSAR C++14, CERT, CWE, and OWASP.
- Unit testing with a proprietary framework (stubbing, generated tests, on the host, virtual targets, and targets),
  and integration with GoogleTest, Boost.Test, and CppUnit.
- Coverage that includes MC/DC on host and target, and runtime analysis for leaks, corruption, and overflows on
  embedded targets.
- Certification by TÜV SÜD for ISO 26262, IEC 61508, DO-178C, IEC 62304, and EN 50128.
- A "C/C++test CT" edition that adds coverage and requirements traceability to open-source frameworks.
