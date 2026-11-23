# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### Test framework projects: CppUTest, Unity, CMock, GoogleTest, Catch2, doctest, cmocka, Check, and Criterion

- Source: <https://github.com/cpputest/cpputest>, <https://github.com/ThrowTheSwitch/Unity>,
  <https://github.com/ThrowTheSwitch/CMock>, <https://github.com/google/googletest>,
  <https://github.com/catchorg/Catch2>, <https://github.com/doctest/doctest>, <https://gitlab.com/cmocka/cmocka>,
  <https://github.com/libcheck/check>, <https://github.com/Snaipe/Criterion>
- License: `BSD-3-Clause AND MIT AND BSL-1.0 AND Apache-2.0 AND LGPL-2.1-only`
- Version: CppUTest `42feb8740bea`, Unity and CMock 2.7.0, GoogleTest 1.18.0, Catch2 3.16.1, doctest 2.5.3,
  cmocka 2.0.2, Check 0.15.2, Criterion 2.5.0

Each framework's target support, configuration options, mocking support, and maintenance state come from its own
repository. No prose or code was copied.

### Valgrind, sanitizers, and coverage tools

- Source: <https://valgrind.org/docs/manual/manual-core.html>, <https://clang.llvm.org/docs/>,
  <https://gcc.gnu.org/onlinedocs/gcc/Gcov.html>, <https://gcovr.com/>
- License: `GFDL-1.3-or-later AND Apache-2.0 WITH LLVM-exception AND BSD-3-Clause`
- Version: Valgrind 3.28.0, GCC 14.2.0 manual, gcovr 8.8

The memory checkers' coverage and costs, Valgrind's CI options, cross-target coverage collection, and MC/DC support
come from this documentation. No prose was copied.

### Yocto Project, Buildroot, and QEMU: test documentation

- Source: <https://docs.yoctoproject.org/test-manual/>, <https://buildroot.org/downloads/manual/manual.html>,
  <https://www.qemu.org/docs/master/user/main.html>
- License: `CC-BY-SA-2.0-UK AND GPL-2.0-only AND GPL-2.0-or-later`
- Version: Yocto Project 6.1 documentation, Buildroot 2026.11-rc2 manual, QEMU master read 2026-11-23

Running ptest, testimage, Buildroot's runtime tests, and QEMU user mode come from these manuals. No prose was copied.

### Linux kernel and U-Boot: testing documentation

- Source: <https://docs.kernel.org/dev-tools/kunit/>, <https://docs.kernel.org/dev-tools/kselftest.html>,
  <https://docs.u-boot.org/en/latest/develop/testing.html>
- License: `GPL-2.0-only`
- Version: read 2026-11-23; U-Boot `v2027.01-rc2`

KUnit, kselftest, U-Boot's sandbox tests, and `test/py` come from this documentation. No prose was copied.

### Zephyr Project, Espressif, and Renode: test and emulation documentation

- Source: <https://github.com/zephyrproject-rtos/zephyr>, `doc/develop/test/`; <https://github.com/espressif/esp-idf>,
  `docs/en/api-guides/unit-tests.rst`; <https://github.com/renode/renode>
- License: `Apache-2.0 AND MIT`
- Version: Zephyr `v4.5.0`, ESP-IDF `v6.1.1`, Renode 1.17.1

ztest, twister, the Fake Function Framework, Zephyr's coverage flow, ESP-IDF's Unity and pytest-embedded flow, and
Renode's test integration come from these trees. No prose was copied.

## Third-party Sources

### James W. Grenning: Test-Driven Development for Embedded C (conference paper)

- Source: <https://wingman-sw.com/papers/EmbeddedTdd-Grenning-v1r1.pages.pdf>
- License: `LicenseRef-NoLicenseStated`
- Version: 2014

It supplied the staged test strategy, the fake time service with a directly called callback, and the advice to
bring legacy code into a test harness. The paper states no licence beyond its copyright, so nothing was copied.

### Memfault, Embedded Artistry, and Mark VanderVoord: firmware testing articles

- Source: <https://interrupt.memfault.com/>, <https://embeddedartistry.com/>, <https://www.vandervoord.net/>
- License: `LicenseRef-NoLicenseStated`
- Version: articles dated 2015 to 2021

They supplied the comparison of mocking approaches, register-level fakes, starting tests from pure logic, and
emulation with Renode. The articles state no reuse licence, so nothing was copied.
