# Design: C, C++, and Embedded Coding Skills

Status: draft for review. The evidence behind this design is in
[the C, C++, and embedded sources](../evaluations/2026-11-23-c-cpp-embedded-sources/README.md).

## Purpose

An agent that writes C or C++ for an embedded product works in one of three places: the Linux kernel, U-Boot, or
Linux userspace on the device. MCU firmware is a fourth place with its own SDKs. Each place has its own conventions,
and the agent must match them first, then add improvements that the place's own rules allow.

The skills in this design give the agent four things it lacks today:

- a default language standard, style, and warning set for new code, and a rule that an existing tree's choices win;
- compiler hardening that works with the build system instead of around it;
- a way to test C and C++ code in each place, including MCU firmware, where most projects have no tests at all;
- working symbol navigation through clangd in cross-compiled trees.

The work is done when the skills below exist, pass `just check`, and the agent-setup session has the pointer rules
that route C and C++ work to them.

## Principles

These hold across every skill in the design.

- **The tree decides.** A tree's `.clang-format`, coding-style document, `-std`, warning set, test framework, and
  agent instruction files outrank every default here. The defaults apply to new code with no established convention.
- **Read version-specific rules from the tree.** Projects pin old releases for years. When a rule changed between
  releases, the skill names the document to read in the tree (such as the kernel's `coding-assistants.rst` or a
  project's `AGENTS.md`), never one release's answer.
- **Say nothing about AI attribution.** Whether to add an attribution or sign-off trailer belongs to the user's commit
  rules and the repository's own instructions. Some projects forbid every attribution.
- **Run formatters only with the tree's own configuration.** In kernel and U-Boot trees, format only changed lines,
  and treat `checkpatch.pl` as the gate, because no formatter reproduces kernel style exactly. A personal default
  configuration, such as an astyle profile read through `ARTISTIC_STYLE_OPTIONS`, rewrites most of a kernel file.
- **Work with the build system's flags.** A Makefile or recipe honours `CC`, `CXX`, `CPPFLAGS`, `CFLAGS`, `CXXFLAGS`,
  and `LDFLAGS`, and adds only what the build system does not already set.

## Decisions

| Subject                           | Decision                                                                                                                                                                                                                                                                                                                                                    |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C standard                        | `-std=gnu17` for new Linux userspace and MCU code, set explicitly because GCC 15 defaults to C23. C99 for portable library code and MISRA C:2012 work. Kernel and U-Boot code keep `gnu11`.                                                                                                                                                                 |
| C++ standard                      | `-std=gnu++17`, the floor most dependencies accept (Qt 6, MISRA C++:2023). C++20 when every supported toolchain is GCC 13 or newer and the code needs it. Firmware SDKs that default lower (Zephyr and the Pico SDK use C++11) are raised explicitly.                                                                                                       |
| C++ exceptions and RTTI           | Off in MCU firmware, where no runtime supports them (`-fno-exceptions -fno-rtti`).                                                                                                                                                                                                                                                                          |
| C++ errors in Linux userspace     | Default: errors as values with standard types, `std::error_code` or a status enum on C++17, and `std::expected` from C++23. A project may instead allow exceptions caught at the top of `main`. In both, an exception never crosses a C callback or a C library interface. An existing project's policy wins.                                               |
| Braces on single statements       | Follow the layout style in force: required where that style requires them, and in new userspace and firmware code with no style set, following CERT and MISRA. A `.clang-format` counts as a style, so a repository using `BreakBeforeBraces: Linux` without `InsertBraces` gets no added braces. Never in kernel or U-Boot code, whose styles forbid them. |
| `_FORTIFY_SOURCE`                 | Leave the level the build system sets (Yocto sets 2 and drops it at `-O0`, Buildroot offers a choice). In a standalone build, use 3 when the toolchain has GCC 12 or newer and glibc 2.34 or newer, and 2 otherwise. A build at `-O0` gets no fortification, so a debug-build test does not exercise it.                                                    |
| Other hardening flags             | The OpenSSF Compiler Options Hardening Guide is the basis: PIE, full RELRO, `-fstack-protector-strong`, `-fstack-clash-protection`, a non-executable stack, control-flow protection per architecture, and `-D_GLIBCXX_ASSERTIONS`. Check the finished binary with `readelf` or `checksec`.                                                                  |
| Runtime ASLR and kernel hardening | Stay in `yocto-security-hardening`, which already covers `randomize_va_space` and KASLR. The C skills point there.                                                                                                                                                                                                                                          |
| Firmware C                        | A reference inside `c-style` now. A separate firmware skill comes later, through `TODO.md`, only if the reference outgrows the skill.                                                                                                                                                                                                                       |
| Placement                         | `c-style`, `cpp-style`, and `c-cpp-testing` in a new `development/c-cpp/` group, following `development/python/` and `development/rust/`. `linux-kernel-development` in the existing `embedded-linux/` group. The new group needs an installer entry.                                                                                                       |

## The Skills

### `c-style` (new)

Writes, reviews, and refactors C for Linux userspace, MCU firmware, and code that lives beside the kernel or U-Boot.
Its body covers the decisions that apply to every place: checking the tree's conventions first, the standard and
warning set, error handling and resource cleanup, integer conversions, and the rules from the work session (an
explicit `-std` in the shared flag variable, a comment naming the bound beside any cast that silences `-Wconversion`,
and test-only macros that replace inputs but never checks). The shared flag variable has a concrete pattern for
Yocto: one `.inc` file holds `-std` and the warning set, every recipe requires it, and the host test script reads the
same file, so host checks and target builds use the same flags.

References, each loaded only when its branch applies:

- `userspace.md`: Linux userspace patterns with their man-page sources, such as atomic file replacement with `fsync`,
  `O_CLOEXEC`, `posix_spawn`, signal safety, `signalfd`, and `explicit_bzero`, plus systemd's coding style as the
  default written userspace style.
- `firmware.md`: the standard per SDK (Zephyr, ESP-IDF, the Pico SDK, STM32Cube, Arduino), MISRA editions and the
  standard each targets, freestanding constraints, and C99-clean headers for code shared across SDKs.
- `hardening.md`: the OpenSSF flag set with each flag's cost, how Yocto and Buildroot inject their own flags, the
  `_FORTIFY_SOURCE` rule above, which flags still apply on an MCU without a memory management unit, and how to verify
  a binary. To confirm that flags reached a Yocto compile, read `temp/run.do_compile`, because `log.do_compile` does
  not show the compiler command.
- `tooling.md`: clang-format with the tree's configuration and `git clang-format` for changed lines, and the
  kernel-style clang-format settings that keep pure tabs, kept together with `BreakStringLiterals: false` so
  user-visible messages stay searchable. It restricts the pre-commit clang-format hook to C and C++, and excludes
  `.clang-format` and `.clang-tidy` from `check-metaschema`, which parses them as JSON. It lists the clang-tidy and
  cppcheck checks to turn off, each with its reason written out, such as cppcheck's `variableScope` against
  declarations at the top of a block and `constParameter` on `main`'s `argv`, and it runs cppcheck once per `-D`/`-U`
  configuration. Tool versions are pinned, because clang-format, clang-tidy, and cppcheck change their output between
  releases: the pre-commit clang-format mirror's revision, clang-tidy through `uvx --from clang-tidy==<version>`, and
  cppcheck from the distribution or a container, since the PyPI `cppcheck` package is a third-party wheel. The
  reference also carries the clangd recipes: how each kind of tree produces `compile_commands.json`, the
  `--query-driver` limit for cross compilers, and the `.clangd` settings for a GCC-built kernel.

### `cpp-style` (new)

Writes, reviews, and refactors C++ for the same places. It covers the standard choice, the exception, RTTI, and
error-handling policy from the decisions above,
resource ownership (RAII, no raw owning pointers), `constexpr` and compile-time tables, avoiding the heap and
`iostream` on small targets, and headers that C code includes through `extern "C"`. It points to `c-style` for
hardening, tooling, and clangd, and carries its own short version of the tree-decides rule, because an agent may load
only one of the two.

### `c-cpp-testing` (new)

Tests C and C++ code in each place. Its body chooses the tool set by place:

| Place                    | Unit framework                                                                                                        | Memory checking                                                                       | Coverage                                 |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------- |
| Embedded Linux userspace | cmocka for C, GoogleTest with GoogleMock for C++                                                                      | Sanitizers on host builds, Valgrind's memcheck on the target for binaries not rebuilt | gcov with gcovr, collected on the target |
| MCU firmware             | Unity with CMock through Ceedling, or CppUTest, on host builds of the same sources; ztest in Zephyr; Unity in ESP-IDF | Sanitizers on the host build                                                          | gcov with gcovr on the host build        |
| Kernel and U-Boot        | KUnit and kselftest; U-Boot's sandbox `ut` tests and `test/py`                                                        | The kernel's own sanitizers                                                           | The kernel's gcov support                |

The body also carries the work session's sanitizer rule: set distinct exit codes in `ASAN_OPTIONS` and
`UBSAN_OPTIONS`, so that a test expected to fail cannot pass on a memory error.

References:

- `embedded-linux.md`: Yocto ptest and testimage, Buildroot's runtime tests, QEMU user mode for one cross-built
  binary, Valgrind on the target, and coverage collection with `GCOV_PREFIX`. It also carries the userspace seams. A
  vendor or firmware library is replaced by a stub shared library, built from a header that declares only the
  functions used, whose behaviour an environment variable selects. For an action that cannot be undone, such as a one-time-programmable
  memory write, a fuse, or an erase, the stub counts each call, and every refusal test asserts that count as well as the
  exit status, because an exit status alone passes when the tool fails for an earlier, wrong reason. A tool that reads
  sysfs, procfs, or device-tree files gets an alternate root path as a test-only compile-time macro. A test that uses
  `O_DIRECT` needs a temporary directory on a disk file system, or on tmpfs from Linux 6.6.
- `firmware.md`: the firmware testing practice, the largest gap in existing guidance. It covers what to test on the
  host, in emulation, and on hardware; the seams that let a test replace hardware (a hardware abstraction layer,
  link-time substitution, function-pointer interfaces, and register-level fakes); how to add tests to a codebase that
  has none, starting from pure logic; fake clocks and directly called callbacks; emulation with Renode and QEMU and
  its limits; and low-budget hardware in the loop. It ends with the ordered practices for an untested project. Each
  piece cites its source, and the interrupt advice is marked as an inference until better sources exist (tracked in
  `TODO.md`).
- `kernel-and-u-boot.md`: how to run KUnit, kselftest, and U-Boot's tests, and what a patch submitter is expected to
  run.

The name "cpptest" is explained once: CppUTest is the framework to use, the old cpptest library is dead, and Parasoft
C/C++test is a commercial product.

### `linux-kernel-development` (new, in `embedded-linux/`)

Writes and reviews kernel code and patches: out-of-tree and in-tree drivers, device-tree bindings, and patches for
upstream or a vendor tree. It covers reading the tree's coding style and process documents for the version in hand,
`checkpatch.pl` as the gate, `W=1`, sparse and Coccinelle, the kernel's sanitizers and KUnit, and building the
compilation database. Kernel-adjacent C, such as a userspace tool shipped in a BSP, belongs to `c-style`.

It is inspired by `UtsavBalar1231/kernel-development-skills` (MIT). Its material is rewritten, not copied, and the
upstream skill's stale `Assisted-by:` rule is not carried, in line with the attribution principle.

### `u-boot-development` (extended)

Adds a reference, `uboot-coding.md`: U-Boot's coding-style deviations from the kernel, its own `.clang-format`, the
`gen_compile_commands.py` script (from v2024.01), and testing on the sandbox with `ut` and `test/py`, including the
sandbox's ASan and libFuzzer support. The skill's routing table gains a row for it.

### `buildroot-development` (extended)

Adds a hardening section to an existing reference: the `BR2_SSP_*`, `BR2_RELRO_*`, `BR2_FORTIFY_SOURCE_*`, and
`BR2_PIC_PIE` options, the fact that the toolchain wrapper adds them rather than `CFLAGS`, and how a package honours
`TARGET_CFLAGS` and `TARGET_LDFLAGS`. Buildroot documents no way to produce a compilation database, so the clangd
recipe in `c-style` marks its Buildroot method as untested.

### Skills left unchanged

`yocto-openembedded-development` and the Yocto security skills already cover flag injection, the `ldflags` QA check,
`-Werror` handling, and the CVE tool, so they need no change. `c-style` points to `yocto-security-hardening` for
Yocto's flags. `embedded-linux-bringup` stays as it is.

## Provenance

- The first-party sources are the documents each skill cites: kernel, U-Boot, and systemd style documents, the Linux
  man-pages, the OpenSSF guide (CC BY 4.0), SEI CERT (CC BY 4.0), and project documentation.
- MISRA, BARR-C, and the C++ Core Guidelines are cited for ideas only, because their licences restrict reuse.
- Third-party skills are rewritten and credited as "inspired by" or "modified from" in `ATTRIBUTIONS.md`.
  `mohitmishra786/low-level-dev-skills` (MIT) is a candidate for `c-cpp-testing` and `tooling.md`. Its character-driver
  example leaks uninitialised stack and is not used.
- Skills with no licence, such as `haonguy3n/embedded-skills`, supply ideas only.

## Build Order

Each step lands as its own commit and passes `just check`.

1. `c-style` with its four references, since the other skills point to it.
2. `cpp-style`.
3. `c-cpp-testing` with its three references.
4. `linux-kernel-development`.
5. The `u-boot-development` and `buildroot-development` extensions.
6. A behavioural evaluation for each new skill, with cases drawn from the sources' known traps: an implicit C23
   build, a kernel file run through a personal formatter, a hard-coded `CFLAGS`, and a must-fail test that passes on
   a memory error.
7. Hand-off to agent-setup: the `development/c-cpp/` installer entry and the pointer rules that route C and C++ work
   to these skills.

## Open Questions

- The firmware interrupt and timing advice rests on thin sources. The skill marks it as inference until the `TODO.md`
  entry for better sources is done.
- The Buildroot compilation database method is untested inference.
- Several clangd defaults (`--background-index`, `--enable-config`, `--fallback-style`) are unconfirmed and stay out
  of the skills until checked against the installed clangd.
