# Design: C, C++, and Embedded Coding Skills

Status: accepted. The evidence behind this design is in
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
| `_FORTIFY_SOURCE`                 | Leave the level the build system sets (Yocto sets 2 and drops it at `-O0`, Buildroot offers a choice). In a standalone build, use 3 when the toolchain has GCC 12 or newer and glibc 2.35 or newer, and 2 otherwise. A build at `-O0` gets no fortification, so a debug-build test does not exercise it.                                                    |
| Other hardening flags             | The OpenSSF Compiler Options Hardening Guide is the basis: PIE, full RELRO, `-fstack-protector-strong`, `-fstack-clash-protection`, a non-executable stack, control-flow protection per architecture, and `-D_GLIBCXX_ASSERTIONS`. Check the finished binary with `readelf` or `checksec`.                                                                  |
| Runtime ASLR and kernel hardening | Stay in `yocto-security-hardening`, which already covers `randomize_va_space` and KASLR. The C skills point there.                                                                                                                                                                                                                                          |
| Firmware C                        | A reference inside `c-cpp-style` now. A separate firmware skill comes later, through `TODO.md`, only if the reference outgrows the skill.                                                                                                                                                                                                                   |
| Placement                         | `c-cpp-style` and `c-cpp-testing` in a new `development/c-cpp/` group, following `development/python/` and `development/rust/`. `linux-kernel-development` in the existing `embedded-linux/` group. The new group needs an installer entry.                                                                                                                 |

## The Skills

### `c-cpp-style` (new)

One skill covers both languages, because C and C++ share the trees, build systems, flags, tools, and clangd setup in
embedded work, and this repository requires each skill to be complete for its own job. Two skills would duplicate
half their content; the merged skill keeps the language rules as two sections of its body.

Draft description:

> Write, review, or refactor C and C++ for embedded Linux userspace, MCU firmware, and tools beside the kernel or
> U-Boot: language standard, warnings, error handling, hardening flags, formatting, linting, and clangd. Use when
> writing or changing .c, .h, .cpp, or .hpp files, choosing -std or compiler flags, or setting up clang-format,
> clang-tidy, cppcheck, or compile_commands.json. Kernel code goes to linux-kernel-development, U-Boot code to
> u-boot-development, and tests to c-cpp-testing.

Body sections, about 300 lines:

1. Read the tree first: `.clang-format`, `.editorconfig`, coding-style documents, `AGENTS.md`, the `-std` and warnings
   in the build files, and the test framework. Done when every default below is confirmed or overridden by the tree.
2. Route by place: kernel code to `linux-kernel-development`, U-Boot code to `u-boot-development`, userspace and
   firmware to this skill's references.
3. Language standard: the C and C++ defaults and the conditions that change them.
4. Warnings: the OpenSSF baseline (`-Wall -Wextra -Wformat=2 -Wconversion -Wsign-conversion -Wshadow` and others),
   `-Werror` in development and CI, and the standard and warnings in one shared flag variable. For Yocto, one `.inc`
   file holds `-std` and the warning set, every recipe requires it, and the host test script reads the same file, so
   host checks and target builds use the same flags.
5. Layout: the brace rule and formatters with the tree's own configuration only.
6. C memory and code hygiene, as concrete practices with the tool that catches each mistake:
   - initialise at declaration, and never read a variable before every path sets it (CERT EXP33-C);
     `-ftrivial-auto-var-init=zero` is a safety net that hides the bug from warnings and sanitizers, not a fix;
   - one owner per allocation, with a comment naming who frees a returned or stored pointer, and release on every
     exit path through one `goto` cleanup ladder in reverse order of acquisition;
   - no use after free and no double free (MEM30-C, MEM31-C): set a pointer that outlives the call to `NULL` after
     freeing it, and keep ownership single, because clearing one copy leaves the others dangling;
   - no pointer to a local escapes its function, by return, stored callback, or struct member;
   - every allocation and every non-void return is checked (ERR33-C, Power of Ten rule 7), with `(void)` marking a
     deliberate ignore;
   - `size_t` for sizes, allocation sizes checked with `__builtin_mul_overflow` or C23 `ckd_mul` (INT30-C, INT32-C),
     and no reliance on signed overflow;
   - a length with every buffer, `snprintf` checked for truncation, and no `strcpy`, `sprintf`, `gets`, or `strncpy`
     as a safe copy (STR31-C, ARR30-C);
   - no variable-length arrays (`-Wvla`) and no `alloca` in new code;
   - `static` for file-local symbols and `const` on pointer parameters the function does not write through;
   - in firmware, no heap after initialisation, a fixed bound on every loop, and no recursion (Power of Ten);
   - the catching tools: the warning set, `-fanalyzer` for use after free, double free, and leaks, clang-tidy
     `bugprone-*`, and ASan and UBSan in host tests.
     The work session's rules sit here too: a comment naming the bound beside any cast that silences `-Wconversion`,
     and test-only macros that replace inputs but never checks.
7. C++ ownership and modern idioms:
   - RAII for every resource, including descriptors, locks, and hardware handles (Core Guidelines R.1); a raw pointer
     or reference never owns (R.3); no bare `new` or `delete` (R.11);
   - `std::unique_ptr` by default, made with `std::make_unique`, and with a custom deleter to wrap a C handle without
     the heap; `std::shared_ptr` only for genuinely shared ownership, and not in firmware;
   - the rule of zero, or all five special members defined or deleted for a class that manages a resource itself;
   - the lifetime traps the compiler misses: a `std::string_view` or `std::span` outliving its buffer, a lambda
     capturing by reference that runs after its scope ends, an iterator or reference used after a container
     reallocates (CERT C++ CTR rules), and use after move;
   - modern features with the standard that brings each: `std::array`, `enum class`, `nullptr`, `override`, `final`,
     `= delete`, `[[nodiscard]]` on error-returning functions, and `constexpr` tables (C++11 and C++14);
     `std::optional`, `std::variant`, `std::string_view`, structured bindings, and `if constexpr` (C++17); `std::span`,
     `consteval`, `constinit`, and designated initialisers (C++20), with a pointer and length in place of `std::span`
     on C++17;
   - brace initialisation to catch narrowing (ES.46), and every member initialised at its declaration (ES.20);
   - the error policy from the decisions above, and an `extern "C"` function that catches everything;
   - in firmware, no exceptions, RTTI, heap containers, `std::function`, or `iostream`, static or placement
     allocation, and `-fno-threadsafe-statics` only where nothing runs before the scheduler starts.
8. Build flags: honour the build system's flag variables and add only what it lacks.
9. Done when the code builds with the tree's flags at no new warnings, the formatter is clean on changed lines, the
   linters are clean or each suppression carries its reason, and the tests pass through `c-cpp-testing`.

The hygiene rules give way to the tree. The kernel and U-Boot have their own allocators, managed resources, and
cleanup idioms, carried by `linux-kernel-development` and U-Boot's coding reference. The Core Guidelines' advice to
compile C as C++ (CPL.2) is not adopted, because kernel and systemd style contradict it. Core Guidelines rules are
cited by number with the ideas restated, because their licence allows internal use only.

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
  cppcheck from the distribution or a container, since the PyPI `cppcheck` package is a third-party wheel.
- `clangd.md`: a recipe per tree for producing `compile_commands.json` (kernel, U-Boot, a Yocto recipe or SDK, a
  Buildroot package, CMake or Meson, and MCU SDKs), the `--query-driver` limit for cross compilers, the `.clangd` file
  for a GCC-built kernel, `Index: Background: Skip`, and `clang-tidy -p` for the analyzer checks clangd skips.

### `c-cpp-testing` (new)

Tests C and C++ code in each place.

Draft description:

> Test C and C++ code on embedded Linux, MCU firmware, the kernel, and U-Boot: unit frameworks and mocks, sanitizers
> and Valgrind, coverage, on-target and emulated runs, and adding tests to firmware that has none. Use when writing or
> running C or C++ tests, choosing a test framework such as CppUTest, Unity, cmocka, or GoogleTest, or making
> hardware-facing code testable.

Body sections, about 180 lines: read the tree's test setup first and use an existing framework; the tool set by
place; test design rules; memory checking (sanitizers on the host, Valgrind on the target, and when to pick each);
coverage, including MC/DC from GCC 14; and a done criterion: tests run in CI, each memory-checker run fails on an
injected defect, and each new seam has a test that uses it. The tool set by place:

| Place                    | Unit framework                                                                                                        | Memory checking                                                                       | Coverage                                 |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------- |
| Embedded Linux userspace | cmocka for C, GoogleTest with GoogleMock for C++                                                                      | Sanitizers on host builds, Valgrind's memcheck on the target for binaries not rebuilt | gcov with gcovr, collected on the target |
| MCU firmware             | Unity with CMock through Ceedling, or CppUTest, on host builds of the same sources; ztest in Zephyr; Unity in ESP-IDF | Sanitizers on the host build                                                          | gcov with gcovr on the host build        |
| Kernel and U-Boot        | KUnit and kselftest; U-Boot's sandbox `ut` tests and `test/py`                                                        | The kernel's own sanitizers                                                           | The kernel's gcov support                |

The test design rules include the work session's sanitizer rule: set distinct exit codes in `ASAN_OPTIONS` and
`UBSAN_OPTIONS`, so that a test expected to fail cannot pass on a memory error. Every test expected to fail must fail
for the reason it names.

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
- `frameworks.md`: the framework comparison, with licence, whether each runs on target, mocking support, and the C++
  features it needs. It explains the name "cpptest" once: CppUTest is the framework to use, the old cpptest library
  is dead, and Parasoft C/C++test is a commercial product.

### `linux-kernel-development` (new, in `embedded-linux/`)

Writes and reviews kernel code and patches: out-of-tree and in-tree drivers, device-tree bindings, and patches for
upstream or a vendor tree. Kernel-adjacent C, such as a userspace tool shipped in a BSP, belongs to `c-cpp-style`.

Draft description:

> Write, review, and prepare Linux kernel code and patches: drivers, device-tree bindings, and patches for mainline or
> a vendor tree, following that tree's own coding-style and submission documents. Use when changing kernel source or
> an out-of-tree module, running checkpatch, sparse, or Coccinelle, or preparing a patch series. Board bring-up goes
> to embedded-linux-bringup.

Body sections, about 180 lines:

1. Identify the tree and version (mainline or vendor), then read its `coding-style.rst`, `submitting-patches.rst`, and
   any `coding-assistants.rst` or `AGENTS.md`; version-specific rules come from these.
2. Style: `checkpatch.pl --strict` as the gate, and formatting of changed lines only with the tree's `.clang-format`.
3. Memory and cleanup: the kernel's allocators, `devm_*` managed resources, and its cleanup idioms, which replace the
   userspace hygiene rules.
4. Build checks: `W=1`, sparse (`C=1`), `coccicheck`, and every affected configuration.
5. Runtime checks: KASAN, UBSAN, KCSAN, and lockdep in debug configurations, and KUnit.
6. Out-of-tree modules: building with `M=` and the module's compilation database.
7. Done when checkpatch is clean, `W=1` adds no new warnings, and the relevant KUnit or kselftest suites pass.

References: `patch-workflow.md` (`format-patch`, `get_maintainer.pl`, cover letters, and revising a series),
`debug-tools.md` (sparse, Coccinelle, the sanitizers, and syzkaller), and `device-tree-bindings.md` (binding
schemas and `dt_binding_check`).

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
recipe in `c-cpp-style` marks its Buildroot method as untested.

### Skills left unchanged

`yocto-openembedded-development` and the Yocto security skills already cover flag injection, the `ldflags` QA check,
`-Werror` handling, and the CVE tool, so they need no change. `c-cpp-style` points to `yocto-security-hardening` for
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

1. `c-cpp-style` with its five references, since the other skills point to it.
2. `c-cpp-testing` with its four references.
3. `linux-kernel-development` with its three references.
4. The `u-boot-development` and `buildroot-development` extensions.
5. A behavioural evaluation for each new skill, with cases drawn from the sources' known traps: an implicit C23
   build, a kernel file run through a personal formatter, a hard-coded `CFLAGS`, and a must-fail test that passes on
   a memory error.
6. Hand-off to agent-setup: the `development/c-cpp/` installer entry and the pointer rules that route C and C++ work
   to these skills.
7. Review with the work session that supplied the original ruleset: both sides confirm that the finished skills
   serve its kernel, U-Boot, and userspace work, and any generic finding it returns is fixed before the work is
   called done.

## Open Questions

- The firmware interrupt and timing advice rests on thin sources. The skill marks it as inference until the `TODO.md`
  entry for better sources is done.
- The Buildroot compilation database method is untested inference.
- Several clangd defaults (`--background-index`, `--enable-config`, `--fallback-style`) are unconfirmed and stay out
  of the skills until checked against the installed clangd.
