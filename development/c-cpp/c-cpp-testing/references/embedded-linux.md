# Testing on Embedded Linux

Runners, Valgrind and coverage detail, and the userspace seams for C and C++ tools that run on an embedded Linux
device. Read it after "Use the Tree's Test Setup First" in the skill body. By then you know whether the tree builds
with Yocto, Buildroot, or a plain cross toolchain.

## Contents

- Yocto ptest
- Yocto testimage
- Buildroot Runtime Tests
- QEMU User Mode
- Valgrind on the Target
- Coverage on the Target
- Userspace Seams

## Yocto ptest

A ptest suite is the package's own tests plus a `run-ptest` script. The script prints one line per case, in the
Automake format: `PASS: name`, `FAIL: name`, or `SKIP: name`.

1. Enable the feature with `DISTRO_FEATURES:append = " ptest"`. This builds and packages every ptest package, and adds
   none of them to the image.
2. Add the suites to the image with `EXTRA_IMAGE_FEATURES += "ptest-pkgs"`, or name them, as in
   `IMAGE_INSTALL:append = " e2fsprogs-ptest zlib-ptest"`.
3. Add `ptest-runner` to the image. It loops over the suites, counts the failures, and returns 1 when any `run-ptest`
   fails, so a CI job can use its exit status.
4. List the available suites with `oe-pkgdata-util list-pkgs "*-ptest"`.
5. On the device, the files sit under `/usr/lib/<package>/ptest`.

The Yocto test manual does not say how a recipe sets `PTEST_ENABLED`. Read the recipe class in the tree before you
write a recipe-level ptest.

## Yocto testimage

`testimage` boots the image and runs Python `unittest` modules against it, mostly as commands over SSH. It runs on
QEMU or on real hardware.

1. Add `IMAGE_CLASSES += "testimage"` and run `bitbake -c testimage <image>`.
2. Find the stock cases in `meta/lib/oeqa/runtime/cases`. Choose the cases with `TEST_SUITES`.
3. `TEST_TARGET` defaults to `qemu`. For real hardware, the manual names `simpleremote` (a board that already runs)
   and `SystemdbootTarget`, with power control hooks.
4. Give QEMU a network. Create tap devices with `scripts/runqemu-gen-tapdevs` after `bitbake qemu-helper-native`, or
   allow `NOPASSWD` sudo for the runner.
5. When a boot hangs, read `${WORKDIR}/testimage/qemu_boot_log` and `ssh_target_log`, and raise
   `TEST_QEMUBOOT_TIMEOUT` when the image only boots slowly.

Use ptest for a package's own suite and `testimage` for behaviour of the whole image.

## Buildroot Runtime Tests

Buildroot's runtime test framework is Python plus QEMU. A test builds a defined configuration, optionally checks the
build output, and optionally boots the result under QEMU to check a feature. The manual section is "Using the runtime
tests framework".

- Run `support/testing/run-tests` from the Buildroot tree.
- List the tests with `-l`.
- Run one test or a group of tests, as the manual describes. Read the manual of the release in the tree for the syntax.

## QEMU User Mode

Use user mode to run one cross-built, dynamically linked test binary on the host, without booting an image. QEMU
translates the system calls and signals, and runs `clone` threads as host threads.

```sh
qemu-aarch64 -L <sysroot> ./test_bin
```

`-L` sets the interpreter prefix, so the binary loads the target sysroot's libc. `-g <endpoint>` opens a GDB endpoint
and `-cpu <model>` picks a core. Replace `aarch64` with the architecture of the binary.

User mode has only the translated system calls. Tests that need real devices, netlink details, or kernel modules
belong on a booted image (inference from the QEMU user documentation). Unverified: check whether Valgrind runs under
user mode before relying on it. Valgrind probably needs a native or full-system run (inference).

## Valgrind on the Target

The skill body gives the flags that make Valgrind fail a CI job. Add these details when you run it on a device.

- Pass `--track-origins=yes` to find where an uninitialised value came from. It slows the run further.
- Pass `--leak-check=full` for per-leak detail. Unverified: check this flag in the Valgrind manual before relying on it.
- Pass `--trace-children=yes` to follow child processes. It is off by default. The manual warns that confusion is still
  likely, so use it only for a test that must start helper programs.
- Use Helgrind or DRD for lock-order problems and races in a pthreads program when ThreadSanitizer is unavailable, as
  on 32-bit ARM. Both target POSIX threads and cannot see interrupt handlers or RTOS tasks.
- Use Massif for a heap profile and Callgrind for a call-graph profile. Neither is a test oracle.
- Expect a device with little RAM to run out of memory first. The Valgrind quick start says memcheck needs "a lot more
  memory" than the program alone.

## Coverage on the Target

The program writes `.gcda` files to the absolute path of the build tree. Relocate them with the GCC cross-profiling
variables. The GCC manual's example runs with `GCOV_PREFIX=/target/run` and `GCOV_PREFIX_STRIP=1`, and the program
then writes `/target/run/build/foo.gcda`.

1. Build on the host with `--coverage`, and keep the `.gcno` files in the build tree. They are not copied.
2. Run the test binary on the target with `GCOV_PREFIX` set to a writable directory.
3. Copy the `.gcda` tree to the host, and place it where the build tree's object paths point.
4. Run gcovr with `--gcov-executable` set to the cross toolchain's `gcov`. With Clang, the gcovr manual says to use
   `llvm-cov gcov`.

The gcovr documentation advises `-O0` and `-fPIC` with `-fprofile-arcs -ftest-coverage`, because optimisation can
merge lines. It also names `-fprofile-abs-path` (GCC 8 and later) for path problems. Pass `--decisions` to gcovr for
decision coverage.

The `.gcda` workflow above is an inference from the GCC manual and gcovr documentation; no source covers a full cross
run. Unverified: check each of these in the tool's documentation before relying on it.

- lcov's cross options, `--gcov-tool` and `--base-directory`.
- Whether lcov 2.x reports MC/DC.
- The LLVM source-based flow on a cross target: `-fprofile-instr-generate`, `-fcoverage-mapping`, `LLVM_PROFILE_FILE`,
  `llvm-profdata merge`, and `llvm-cov`.

## Userspace Seams

The skill body defines a seam and names the test-only alternate root. This section adds the construction detail.

### Stub Shared Library

Replace a vendor or firmware library the tool calls with a stub shared library.

1. Write a header that declares only the functions the tool uses, not the vendor's whole API.
2. Copy the status and error values from the vendor header, so the tool under test sees the constants it sees in
   production.
3. Implement each function so an environment variable selects its behaviour, such as success, a named error, or a
   short read. One built stub then serves every test, and each test sets the variable before it starts the tool.
4. Link the tool against the stub for the test run. The tool's own code stays unchanged.

### Call Counting

For an action that cannot be undone, have the stub count each call to the irreversible function. The counter must
survive until the test reads it, so write it to a file in the test's temporary directory, or print it on exit. The
test then asserts the count next to the exit status, as the skill body requires.

### Alternate Root

When a tool reads sysfs, procfs, or device-tree files, point every such path at one prefix macro that the production
build never sets. The test creates the fake tree under a temporary directory, with the file contents the case needs.
Make the macro replace the input path only. A check that the tool runs in production must run in the test.

### O_DIRECT

A test that opens a file with `O_DIRECT` needs its temporary directory on a disk file system. From Linux 6.6, tmpfs
also works. On an older kernel, point the test at a real disk path. A `/tmp` on tmpfs makes the open fail for a
reason unrelated to the code under test.
