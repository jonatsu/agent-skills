# Testing the Linux Kernel and U-Boot

How to run the kernel's KUnit and kselftest suites and U-Boot's sandbox and `test/py` tests, and what a patch
submitter is expected to run. Both projects publish their own test documents, and the tree's documents override this
file when they differ. Read the version in the tree you work in, because commands and options change between releases.

## Contents

- Choosing KUnit or kselftest
- Running KUnit
- Running kselftest
- U-Boot Sandbox Tests
- U-Boot test/py
- What a Submitter Runs
- Unverified Points

## Choosing KUnit or kselftest

The kernel's documentation says that the bulk of kernel tests use either kselftest or KUnit.

- KUnit is entirely in-kernel and white-box. Its test code is part of the kernel, so it suits small, self-contained
  parts that need to call kernel functions directly.
- kselftest is mostly userspace. It tests a feature through a system call, a device, or a file system, and it cannot
  call kernel functions directly. The tests are meant to run after you build, install, and boot a kernel.

## Running KUnit

Run the wrapper from the kernel tree root.

```sh
./tools/testing/kunit/kunit.py run
```

1. By default it builds for UML (`ARCH=um`) in a `.kunit` build directory.
2. A `.kunitconfig` file selects the Kconfig options. Point at a subsystem's file with
   `--kunitconfig=fs/ext4/.kunitconfig`.
3. Filter tests with globs. Add `--raw_output` to see the TAP output.
4. To parse a saved kernel log, run `kunit.py parse`.
5. To run under QEMU instead of UML, pass `--arch=<arch>`. For an architecture without a built-in configuration, pass
   `--qemu_config`.
6. `CONFIG_KUNIT_ALL_TESTS` is a broad switch. Prefer the subsystem's `.kunitconfig` when you test one area.

## Running kselftest

Build the headers first, then run through either entry point.

```sh
make headers
make -C tools/testing/selftests run_tests
make kselftest
```

Control the run with these variables:

- `TARGETS="size timers"` selects the test directories. `SKIP_TARGETS` excludes some.
- `O=/tmp/kselftest` writes the output to a separate directory.
- `summary=1` prints a summary.
- `FORCE_TARGETS=1` makes every target build or fail. Without it, the build succeeds when one target builds, so a
  broken target can pass unnoticed.

## U-Boot Sandbox Tests

The sandbox build runs U-Boot as a user-space program, so the tests need no target hardware. All the tests share a
small number of executables. U-Boot has two kinds of tests: C tests in `test/`, run by the `ut` command, and Python
tests in `test/py/tests`.

Build the sandbox first, then run one suite or one test through the `ut` command.

```sh
make sandbox_defconfig
make
./u-boot -T -c "ut dm gpio"
```

`-T` selects the test device tree, `test.dts`. Without it, tests fail on missing devices.

The sandbox is a hosted program, so AddressSanitizer applies. U-Boot's `arch/sandbox/config.mk` adds
`-fsanitize=address` when `CONFIG_ASAN` is set, and `-fsanitize=fuzzer` when `CONFIG_FUZZ` is set. Set the option in
the sandbox configuration before the build.

## U-Boot test/py

The U-Boot documentation describes `make check` as running most tests on the sandbox, and also says that only the
pytest suite runs under this command. Unverified: check whether `make check` runs the C `ut` suites in the tree before
relying on it. Run them with the `ut` command above to be sure. `make qcheck` skips tests marked
`@pytest.mark.slow`.

To run the pytest harness directly:

```sh
./test/py/test.py --bd sandbox --build
```

- Add `-k <name>` to select tests.
- Read the HTML log in `build-sandbox/test-log.html`.
- Install the requirements first, with `pip install -r test/py/requirements.txt`. The harness needs Python 3.
- The same harness runs on real hardware. It talks to the console through hook scripts. Use hardware when a bug is
  specific to one board.

## What a Submitter Runs

### U-Boot

A patch series that changes or enhances a U-Boot subsystem should carry a new or expanded test, as the U-Boot
documentation states. Check the patches with `b4 prep --check`, which wraps
`scripts/checkpatch.pl`, and send them with `b4 send`. U-Boot treats `checkpatch.pl` warnings as advice, because the
tool "can help you find some style problems, but is imperfect".

### Linux Kernel

The kernel's submit checklist asks for these checks. It does not require KUnit or kselftest.

- Run `scripts/checkpatch.pl`, and keep `sparse` clean.
- Test with the debug options enabled together, among them `CONFIG_PREEMPT`, `CONFIG_DEBUG_PREEMPT`,
  `CONFIG_SLUB_DEBUG`, `CONFIG_DEBUG_PAGEALLOC`, `CONFIG_DEBUG_MUTEXES`, `CONFIG_DEBUG_SPINLOCK`,
  `CONFIG_DEBUG_ATOMIC_SLEEP`, and `CONFIG_PROVE_RCU`.
- Build with and without `CONFIG_SMP` and `CONFIG_PREEMPT`.
- Exercise all code paths with lockdep.
- Test against the latest `linux-next` tag.
- Build on 32-bit and 64-bit and on both endiannesses.

## Unverified Points

Unverified: check each point in the tree before relying on it.

- Usage of KASAN, KCSAN, and KMSAN. The kernel testing overview names them.
- Kernel gcov setup, including whether `CONFIG_GCOV_CONDITION_COVERAGE` exists.
- U-Boot coverage.
- Whether U-Boot's GitLab CI must pass before a patch merges.
- Whether Valgrind applies to the U-Boot sandbox. It is a user-space program, so it may.
- The kernel CI systems, KernelCI and 0-day.
