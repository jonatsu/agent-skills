---
name: c-cpp-testing
description: Test C and C++ code on embedded Linux, MCU firmware, the Linux kernel, and U-Boot. Covers unit test frameworks and mocks, sanitizers and Valgrind, coverage, on-target and emulated runs, and making hardware-facing code testable, including firmware with no tests yet. Use when writing or running C or C++ tests, choosing a framework such as CppUTest, Unity, cmocka, or GoogleTest, or adding tests to an untested codebase. Writing the production code belongs to c-cpp-style.
license: MIT
compatibility: A GCC or Clang toolchain. Valgrind, gcovr, QEMU, and each test framework are optional and checked when used.
metadata:
  author: Joonas Onatsu
---

# C and C++ Testing

Tests for C and C++ in four places: Linux userspace on an embedded device, MCU firmware, the Linux kernel, and
U-Boot. Hardware is the hard part in each, so most of this skill is about where a test can stand in for it.

## Use the Tree's Test Setup First

Read how the tree already tests before adding anything. Check its test directory, the framework its build files
link, its CI configuration, and any `ptest`, `kselftest`, or `test/py` setup. Keep a tree's existing framework,
because two frameworks in one tree split every helper and fixture.

## Choose the Tools by Place

| Place                    | Unit framework                                                                      | Memory checking                                                                       | Coverage                              |
| ------------------------ | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------- |
| Embedded Linux userspace | cmocka for C; GoogleTest with GoogleMock for C++                                    | Sanitizers on host builds; Valgrind's memcheck on the target for binaries not rebuilt | gcov with gcovr, collected on target  |
| MCU firmware             | Unity with CMock through Ceedling, or CppUTest, on a host build of the same sources | Sanitizers on the host build                                                          | gcov with gcovr on the host build     |
| Zephyr                   | ztest with twister, mocks with the Fake Function Framework                          | Check the tree's documentation                                                        | `CONFIG_COVERAGE` on QEMU or the host |
| ESP-IDF                  | Unity run by pytest-embedded, CMock for host mocks                                  | Check the tree's documentation                                                        | Check the tree's documentation        |
| Linux kernel             | KUnit, and kselftest for userspace-facing behaviour                                 | KASAN, UBSAN, and KCSAN in a debug configuration (`linux-kernel-development`)         | Check the tree's documentation        |
| U-Boot                   | The sandbox `ut` tests and `test/py`                                                | The sandbox built with `CONFIG_ASAN`                                                  | Check the tree's documentation        |

Move off the default when the tree already uses another framework, or for these reasons:

- Use CppUTest where its built-in leak detection helps, or for C++ firmware code.
- Use Check or Criterion only for host-only C tests that need each test in its own process.
- Use Catch2 or doctest only for host-only C++ tests with exceptions available.

"cpptest" can mean three things. CppUTest is the active framework above. The cpptest library is unmaintained and
archived, so never add it to new work. Parasoft C/C++test is a commercial analysis and test product. When a user
names "cpptest", infer which from the project, and ask when the project does not settle it.

For each framework's licence, target support, mocking, and C++ needs, read
[references/frameworks.md](references/frameworks.md).

## Design Each Test to Fail for Its Reason

A test that expects failure passes whenever the code fails, including for the wrong reason. Write each one so only
the named failure satisfies it:

- Give each memory checker its own exit code, distinct from every exit code the program uses:
  `ASAN_OPTIONS=exitcode=99`, `UBSAN_OPTIONS=halt_on_error=1:exitcode=98`, and Valgrind's `--error-exitcode=97`.
  A memory error then cannot pass as an expected refusal. Without `halt_on_error=1`, UBSan reports and exits 0.
- For an action that cannot be undone, such as writing one-time-programmable memory, blowing a fuse, or erasing
  flash, have the stub count each call. Assert that count, 0 or 1, as well as the exit status, because an
  exit status alone passes when the tool fails early for another reason.
- Assert the specific error or message, not only that something failed.
- Check that every new test can fail: break the code under test once and watch the test go red.

## Make Hardware-Facing Code Testable

A seam is a point where a test can replace a dependency without editing the code under test. Add seams one at a
time, starting at the dependency that blocks the most tests:

- A hardware abstraction layer: hardware access goes through a small interface, and tests link a fake.
- Link-time substitution: the test build links a fake source file in place of the driver or vendor library.
- Function pointers: the code calls through a table that a test can fill.
- Register-level fakes: a struct or array in RAM stands in for peripheral registers, so a test sets status bits and
  reads back what the code wrote.
- A test-only alternate root: a compile-time macro the production build never sets points hard-coded paths, such
  as `/proc/device-tree` or `/sys`, at a test directory. It replaces inputs only, never a check.

Time is a dependency too. Put the clock behind an interface, and give tests a fake clock. After setting the fake
time, call the timer or scheduler callback directly.

Interrupt handlers and concurrency are the weakest part of host testing. Keep a handler thin, so its logic sits in
a function a test can call. Host tests cannot show preemption, interrupt latency, or the target's memory ordering,
so those need emulation or hardware.

For the userspace seams in detail, read [references/embedded-linux.md](references/embedded-linux.md). For firmware,
read [references/firmware.md](references/firmware.md): it covers what to test where, interrupts and timing, the
hazards of a first host build, and starting from no tests at all.

## Check Memory Errors

Pick a sanitizer when you can rebuild the code, and Valgrind when you cannot:

- AddressSanitizer finds out-of-bounds access on the heap, stack, and globals, use after free, double free, and
  leaks, at about twice the run time. UBSan finds undefined behaviour such as signed overflow and bad shifts at
  small cost. Build test binaries with both.
- ThreadSanitizer finds data races, on 64-bit targets only.
- Valgrind's memcheck needs no rebuild and runs 10 to 50 times slower. Use it for a cross-built or vendor binary on
  the target. It supports 32-bit ARM from ARMv7 and 64-bit ARM. It requires glibc, so check musl targets separately.
- Never run a sanitizer-built binary under Valgrind. Valgrind then sees none of the program's allocations, because
  the AddressSanitizer runtime replaces the allocator, so it reports nothing.

For CI, make each tool fail the job. Valgrind's default exit code is 0 even when it reports errors, so always pass
`--error-exitcode` with the distinct code above. Record known false reports in a suppression file with `--suppressions`,
and generate entries with `--gen-suppressions=yes`. Build Valgrind runs with `-g` and `-O0` or `-O1`, because higher
optimisation produces false uninitialised-value reports.

Drop `_FORTIFY_SOURCE` in sanitizer builds, because the OpenSSF hardening guide lists it as incompatible with
AddressSanitizer.

## Measure Coverage

Compile with `--coverage`, run the tests, and report with gcovr. Coverage at `-O0` maps to source lines; higher
optimisation merges lines.

On a cross target, the program writes its `.gcda` files to the absolute build path. Set `GCOV_PREFIX` to a
writable directory on the target, and `GCOV_PREFIX_STRIP` to drop leading path components. Copy the files back to
the build tree on the host, and run gcovr with the cross toolchain's gcov through `--gcov-executable`.

Modified condition and decision coverage (MC/DC) is available from GCC 14 with `-fcondition-coverage` and
`gcov --conditions`, and in Clang with `-fcoverage-mcdc`. Neither compiler is a qualified tool, so treat the result
as evidence for safety standards only with a qualified toolchain.

## Place-Specific Runners

- [references/embedded-linux.md](references/embedded-linux.md): Yocto ptest and testimage, Buildroot runtime tests,
  QEMU user mode for one cross-built binary, Valgrind and coverage on the target, and the userspace seams.
- [references/firmware.md](references/firmware.md): host, emulator, and hardware testing for MCU code, and the
  ordered practices for a project with no tests.
- [references/kernel-and-u-boot.md](references/kernel-and-u-boot.md): KUnit, kselftest, U-Boot's tests, and what a
  patch submitter is expected to run.

## Done

The work is done when:

- the tests run in CI, or in the tree's documented test command;
- each memory checker, given one injected defect, fails the run with its own exit code;
- each new seam has at least one test that uses it;
- each test expected to fail asserts the reason for the failure, not only that it failed.
