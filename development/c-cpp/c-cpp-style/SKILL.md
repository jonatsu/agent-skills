---
name: c-cpp-style
description: Write, review, or refactor C and C++ for embedded Linux userspace, MCU firmware, and tools beside the kernel or U-Boot. Covers standards, warnings, memory safety, error handling, hardening flags, formatting, linting, and clangd. Use when writing or changing .c, .h, .cpp, or .hpp files, choosing -std or compiler flags, or setting up clang-format, clang-tidy, cppcheck, or compile_commands.json. Kernel code goes to linux-kernel-development, U-Boot code to u-boot-development, and tests to c-cpp-testing.
license: MIT
compatibility: A GCC or Clang toolchain. clang-format, clang-tidy, cppcheck, and clangd are optional and checked when used.
metadata:
  author: Joonas Onatsu
---

# C and C++ Style

C and C++ for embedded products: Linux userspace on the device, MCU firmware, and tools that sit beside the kernel
or U-Boot. One skill covers both languages, because they share the trees, build systems, flags, and tools; the
language rules are two sections of this body.

The tree decides. Every default here applies to new code with no established convention, and a tree's own
configuration, style document, or instruction file outranks it.

## Read the Tree First

Before writing code, read what the tree already decides:

- `.clang-format`, `.editorconfig`, and any `.astylerc` or `.uncrustify.cfg`;
- a coding-style document, such as `CODING_STYLE.md` or `Documentation/process/coding-style.rst`;
- `AGENTS.md`, `CLAUDE.md`, or `CONTRIBUTING.md`;
- the `-std` and warning flags in the build files (`Makefile`, `CMakeLists.txt`, `meson.build`, a recipe or `.inc`);
- the test framework the tree already uses.

This step is done when each default below is either confirmed or replaced by what the tree says. Take a rule that
changed between releases, such as a formatting option, from the tree in hand, never from another release.

## Route by Place

| Code                                         | Where the rules live                                              |
| -------------------------------------------- | ----------------------------------------------------------------- |
| Linux kernel, in-tree or out-of-tree modules | `linux-kernel-development`                                        |
| U-Boot                                       | `u-boot-development`                                              |
| Linux userspace on the device                | This skill and [references/userspace.md](references/userspace.md) |
| MCU firmware                                 | This skill and [references/firmware.md](references/firmware.md)   |
| Tests in any of these places                 | `c-cpp-testing`                                                   |

Kernel and U-Boot code follow their own style, allocators, and cleanup idioms, which outrank the hygiene rules
below. A userspace tool shipped in a board support package is userspace code, even when it lives in a kernel-style
repository.

The userspace reference covers atomic file replacement, descriptor hygiene, process spawning, signal handling, and
wiping secrets. The firmware reference covers standards per SDK, MISRA editions, freestanding constraints, and
headers shared across SDKs.

## Language Standard

Set the standard explicitly in every build. GCC 15 changed the C default to `gnu23`, and GCC 16 changed the C++
default to `gnu++20`. A build that relies on the default therefore changes language when the toolchain updates.

| Code                                 | Default                 | Move when                                                                                                     |
| ------------------------------------ | ----------------------- | ------------------------------------------------------------------------------------------------------------- |
| New Linux userspace C                | `-std=gnu17`            | C99 for a library other projects build on old compilers; `gnu23` only when every toolchain is GCC 15 or newer |
| New C++                              | `-std=gnu++17`          | C++20 when every supported toolchain is GCC 13 or newer and the code needs a C++20 feature                    |
| MCU firmware C                       | `-std=gnu17`            | The SDK's level when it requires one; strict `-std=c99` for MISRA C:2012                                      |
| MCU firmware C++                     | `-std=gnu++17`          | Raise SDK defaults explicitly: Zephyr and the Pico SDK default to C++11                                       |
| Code shared across SDKs or compilers | C99, C++11-safe headers | Never higher than the oldest consumer                                                                         |
| Kernel and U-Boot                    | `gnu11`                 | Never; the tree sets it                                                                                       |

C17 adds no language features over C11; it fixes defects. Choosing `gnu17` over `gnu11` costs nothing and matches
systemd. No MISRA C edition covers C23, and MISRA C++:2023 targets C++17.

## Warnings and Build Flags

Keep `-std` and the warning set in one shared flag variable. Host builds, test builds, and target builds then
compile with the same language and warnings. In a Yocto layer, put them in one `.inc` file that every recipe
requires and that the host test script also reads.

Start new code from this set, which follows the OpenSSF Compiler Options Hardening Guide and the GCC manual:

```text
-Wall -Wextra -Wformat=2 -Wconversion -Wimplicit-fallthrough -Wshadow -Wvla -Wundef
-Wnull-dereference -Wcast-align -Werror=format-security
```

Add these to the C flags only. `g++` warns that each is not valid for C++, and `-Werror` turns that into a build
failure:

```text
-Wstrict-prototypes -Wmissing-prototypes
-Werror=implicit -Werror=incompatible-pointer-types -Werror=int-conversion
```

Under `gnu17`, `int f()` still declares a function without a prototype, which `-Wstrict-prototypes` reports.
`-Wmissing-prototypes` reports an external function with no prior declaration, which is usually one that should be
`static`.

In C, `-Wconversion` also enables `-Wsign-conversion`. In C++, add `-Wsign-conversion` separately.
`-Wnull-dereference` works only while the compiler deletes null-pointer checks. The production flag
`-fno-delete-null-pointer-checks` from the hardening reference turns the warning off, so rely on it in development
builds.

Use `-Werror` in development and CI builds only. In shipped source and recipes, use selective `-Werror=<warning>`,
because a blanket `-Werror` breaks the build when a newer compiler adds a warning. A build layer that pins its
toolchain may use a blanket `-Werror` on purpose, so that a toolchain update shows every new warning at once; keep
that choice where the tree makes it.

Honour the build system's flag variables: `CC`, `CXX`, `CPPFLAGS`, `CFLAGS`, `CXXFLAGS`, and `LDFLAGS`. Yocto passes
them in the environment, and Buildroot passes them on the `make` command line. Both carry hardening and sysroot
flags, so a project's own flags must add to them without replacing them:

- `CFLAGS = ...` in a Makefile drops Yocto's environment flags.
- `CFLAGS += ...` is ignored when `CFLAGS` comes from the `make` command line, as in Buildroot.
- Keep the project's flags in their own variable, such as `PROJECT_CFLAGS`, placed after `$(CFLAGS)` on the compile
  line. `override CFLAGS += ...` also works.

For hardening flags, the `_FORTIFY_SOURCE` level, and checking that flags reached the binary, read
[references/hardening.md](references/hardening.md).

## Layout

Run a formatter only with the tree's own configuration. A personal default, such as an astyle profile from
`ARTISTIC_STYLE_OPTIONS` or `~/.astylerc`, reformats most of a file in another style. In kernel and U-Boot trees,
format only the lines you changed, with `git clang-format`, and treat `checkpatch.pl` as the gate.

Braces follow the layout style in force. A `.clang-format` counts as a style: one with `BreakBeforeBraces: Linux`
and no `InsertBraces` means no added braces. Kernel and U-Boot style forbid braces on single statements.

Where the tree sets no style, match the indentation of the surrounding code, and brace every `if`, `else`, `for`,
`while`, and `do` body. CERT and MISRA require braces because a statement added later runs unconditionally without
them.

For formatter, linter, and pre-commit configuration, read [references/tooling.md](references/tooling.md). For
symbol navigation and `compile_commands.json`, read [references/clangd.md](references/clangd.md).

## C: Memory and Code Hygiene

These rules name the mistakes C code makes most often and the tool that catches each one. Rule identifiers refer to
the SEI CERT C Coding Standard and Holzmann's "The Power of Ten".

- Initialise each variable at its declaration, or before every path reads it (CERT EXP33-C). Where kernel style
  puts declarations at the top of a block, initialise them there. `-ftrivial-auto-var-init=zero` is a safety net,
  not a fix: it hides the bug from `-Wmaybe-uninitialized` and the sanitizers.
- Give each allocation one owner. Comment who frees a pointer that a function returns or stores.
- Release resources on every exit path through one `goto` cleanup ladder, in reverse order of acquisition.
- Never use memory after freeing it or free it twice (MEM30-C, MEM31-C). Set a pointer that outlives the call to
  `NULL` after freeing it. This protects that one copy only, so keep ownership single rather than copying owning
  pointers.
- Never let a pointer to a local escape its function: not by return, not through a stored callback, and not as a
  struct member.
- Check every allocation and every non-void return (ERR33-C, Power of Ten rule 7). Mark a deliberate ignore with a
  `(void)` cast.
- Use `size_t` for sizes and counts. Check a multiplication that sizes an allocation with `__builtin_mul_overflow`,
  or `ckd_mul` on C23 (INT30-C, INT32-C). Signed overflow is undefined behaviour, so never rely on it wrapping.
- Pass a length with every buffer. Check `snprintf`'s return value for truncation.
- Use none of `strcpy`, `strcat`, `sprintf`, or `gets`. Never treat `strncpy` as a safe copy, because it can leave the
  string unterminated (STR31-C, ARR30-C).
- Use no variable-length arrays (`-Wvla`) and no `alloca` in new code, because both make stack use unbounded.
- Make symbols used in one file `static`. Make a pointer parameter `const` when the function never writes through it.
- When an explicit cast silences `-Wconversion`, comment the bound that keeps the value in range. A reviewer can then
  check the cast instead of trusting it.
- A test-only compile-time macro may replace an input, such as a fixed key or an alternate root for
  `/proc/device-tree`. It never disables a check, so the host test build runs the device build's checks.
- In MCU firmware, allocate no heap memory after initialisation, and give every loop a fixed upper bound. Use no
  recursion (Power of Ten rules 1 to 3), because stack and heap exhaustion on a device has no recovery.

Power of Ten rule 1 also bans `goto`, which conflicts with the cleanup ladder. In firmware that follows the Power
of Ten or MISRA, the project's rule set decides the cleanup form.

The tools that catch these: the warning set above; `-fanalyzer`, which GCC documents for C code only and which
reports use after free, double free, and leaks; clang-tidy's `bugprone-*` checks; and AddressSanitizer and UBSan
in host tests, set up through `c-cpp-testing`.

## C++: Ownership and Modern Idioms

The rule numbers refer to the C++ Core Guidelines and the SEI CERT C++ Coding Standard.

- Wrap every resource in an object that releases it in its destructor (RAII, Core Guidelines R.1). That covers
  file descriptors, locks, mapped memory, and hardware handles, not only heap memory.
- A raw pointer or reference never owns what it points to (R.3). Write no bare `new` or `delete` (R.11).
- Use `std::unique_ptr` for single ownership, created with `std::make_unique`. To own a C handle, such as a `FILE*`
  or a vendor library handle, give `std::unique_ptr` a custom deleter; that needs no heap allocation.
- Use `std::shared_ptr` only when ownership is genuinely shared. It costs an atomic reference count and a heap
  control block, so keep it out of firmware.
- Follow the rule of zero: a class whose members manage their own resources declares no destructor, copy, or move
  operations. A class that manages a resource directly defines or deletes all five.
- Watch for the lifetime errors the compiler does not report:
  - a `std::string_view` or `std::span` that outlives the buffer it views;
  - a lambda that captures by reference and runs after its scope ends;
  - an iterator, pointer, or reference into a container used after the container reallocates (CERT C++ CTR rules);
  - an object used after it was moved from.
- Prefer these features where the standard in force has them:
  - C++11 and C++14: `std::array`, `enum class`, `nullptr`, `override`, `final`, `= delete`, and `constexpr` tables.
  - C++17: `std::optional`, `std::variant`, `std::string_view`, structured bindings, `if constexpr`, and
    `[[nodiscard]]` on every function that returns an error.
  - C++20: `std::span`, `consteval`, `constinit`, and designated initialisers. On C++17, pass a pointer and a length
    where `std::span` would go.
- Initialise every member at its declaration (ES.20). Use brace initialisation so narrowing conversions fail to
  compile (ES.46).

### Errors in C++

In MCU firmware, default to `-fno-exceptions -fno-rtti`. Unwinding tables cost flash, and many SDKs ship with
exceptions off. A project that enables them in its SDK configuration keeps them.

In new Linux userspace code, return errors as values with standard types: `std::error_code` or a status enum on
C++17, and `std::expected` from C++23. `std::optional` carries no error, so use it only where absence is the whole
answer. A project may instead allow exceptions, caught at the top of `main`; follow the project when it does.

In every place, an exception never crosses a C callback or a C library interface, because unwinding through C
frames is undefined. A function declared `extern "C"` catches everything and converts it to an error code.

### Firmware C++

Unless the project enables them, use no exceptions, RTTI, heap-backed containers, `std::function`, or `iostream`.
Allocate statically or with placement `new` into static storage. Use `-fno-threadsafe-statics` only when no
function-local static is first touched after the scheduler starts. Keep headers that C code includes free of C++
types, behind `extern "C"`.

## Done

The work is done when:

- the code builds with the tree's flags and adds no new warnings;
- the formatter, run with the tree's configuration, leaves the changed lines unchanged;
- the linters are clean, or each suppression states its reason;
- the tests pass, set up through `c-cpp-testing`.
