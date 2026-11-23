# Hardening Flags

Use this file to choose hardening flags for Linux userspace C and C++ and to set the `_FORTIFY_SOURCE` level. It also
shows how Yocto and Buildroot inject flags and how to check a binary. The basis is the OpenSSF Compiler Options
Hardening Guide for C and C++ (dated 2026-08-20, repository commit `816cacb72970`, CC BY 4.0). Its tables apply to
userspace on GNU/Linux. For MCU firmware, read `references/firmware.md`, section "Hardening Without an MMU". A note
marked "inference" is a reading of the sources, not a statement in them.

## Contents

- Rules Before the Flags
- The OpenSSF Flag Set
- GCC `-fhardened`
- The `_FORTIFY_SOURCE` Rule
- How Yocto and Buildroot Inject Flags
- Verifying a Binary
- Runtime Hardening

## Rules Before the Flags

- Name the flags you want in the build files, because defaults differ between distributions (OpenSSF).
- Add only the flags the build system does not already set. A repeated flag can fight the BSP's setting (inference).
- Treat a program that cannot build with these options as a bug. Test with production flags and with an instrumented
  build.
- Decide explicitly before omitting a flag for speed. The guide allows it only for a program that processes trusted
  data alone.

The `SKILL.md` section "Warnings and Build Flags" holds the warning set and the `-Werror` policy. It also says how a
project's flags sit beside the build system's flag variables. This file covers the flags that change generated code
and the link.

## The OpenSSF Flag Set

Compiler baseline, for every build:

```text
-O2 -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=3 -D_GLIBCXX_ASSERTIONS
-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST -fstrict-flex-arrays=3
-fstack-clash-protection -fstack-protector-strong
```

Linker baseline:

```text
-Wl,-z,nodlopen -Wl,-z,noexecstack -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -Wl,--no-copy-dt-needed-entries
```

Per target, and for production:

```text
-fPIE -pie                                  (executables)
-fPIC -shared                               (shared libraries)
-fcf-protection=full                        (x86_64)
-mbranch-protection=standard                (aarch64)
-fzero-call-used-regs=used-gpr              (x86_64 and aarch64)
-Wtrampolines -fzero-init-padding-bits=all  (GCC only)
-fno-delete-null-pointer-checks -fno-strict-overflow -fno-strict-aliasing -ftrivial-auto-var-init=zero
-fexceptions                                (multi-threaded C on glibc pthreads)
```

Three of these flags need a recent GCC (GCC 13, 14, and 15 changes pages):

- `-fstrict-flex-arrays=3` needs GCC 13.
- `-fhardened` needs GCC 14.
- `-fzero-init-padding-bits=all` needs GCC 15.

Yocto scarthgap ships GCC 13.5 and Buildroot LTS defaults to 13.4, so both lack the last two. Unverified: the minimum
version of every other flag. Probe each flag before adding it, and drop it for a toolchain that rejects it:

```sh
"$CC" -Werror -fstrict-flex-arrays=3 -x c -c /dev/null -o /dev/null
```

What each flag protects and costs, where the sources state it:

| Flag                                                   | Effect                                                                                                                             | Cost or limit                                                              |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `-fstack-protector-strong`                             | Guards a function's stack against overwrite; `-fstack-protector` guards only functions with `alloca` or buffers of 8 bytes or more | `-fstack-protector-all` has a noted performance cost (Buildroot help text) |
| `-fstack-clash-protection`                             | Stack clash defence                                                                                                                | No cost verified                                                           |
| `-fPIE -pie`                                           | Position-independent executable                                                                                                    | Needs shared libraries and a PIE-capable toolchain                         |
| `-z relro -z now`                                      | Full RELRO: the GOT becomes read-only                                                                                              | Start-up time; full RELRO selects PIE                                      |
| `-z noexecstack`                                       | Non-executable stack                                                                                                               | No cost verified                                                           |
| `-z nodlopen`                                          | Object cannot be loaded with `dlopen`                                                                                              | No cost verified                                                           |
| `-fstrict-flex-arrays=3`                               | Treats only true flexible array members as flexible                                                                                | Breaks code that uses trailing arrays as flexible (inference)              |
| `-D_GLIBCXX_ASSERTIONS`                                | libstdc++ run-time assertions                                                                                                      | libstdc++ only                                                             |
| libc++ fast hardening mode                             | libc++ run-time checks                                                                                                             | The libc++ docs say it has no ABI impact and recommend it for production   |
| `-fno-strict-overflow`                                 | Signed overflow is not optimised away                                                                                              | Does not replace explicit overflow checks                                  |
| `-fno-delete-null-pointer-checks`                      | Keeps null checks the optimiser would remove                                                                                       | Disables `-Wnull-dereference`, so keep that warning in development builds  |
| `-ftrivial-auto-var-init=zero`                         | Zeroes uninitialised locals                                                                                                        | Size cost on embedded targets; hides bugs from warnings and sanitizers     |
| `-fcf-protection=full`, `-mbranch-protection=standard` | Control-flow protection, per architecture                                                                                          | Architecture-specific                                                      |

More OpenSSF positions:

- Avoid a hard-coded `-Wl,-rpath` in release binaries. An attacker who controls the target directory can substitute
  libraries, and set-user-ID programs are exposed. It is the guide's only discouraged option.
- Keep sanitizers in test builds. Production and set-user-ID binaries get none, except UBSan with
  `-fsanitize-minimal-runtime` (Clang) or `-fsanitize-trap=undefined` (GCC).
- Ship stripped binaries and keep debug files apart: `objcopy --only-keep-debug`, `objcopy --strip-unneeded`, then
  `objcopy --add-gnu-debuglink`. Security must not depend on hidden symbols.

## GCC `-fhardened`

`-fhardened` is one GCC option, available from GCC 14. It enables `-D_FORTIFY_SOURCE=3`, `-D_GLIBCXX_ASSERTIONS`,
`-ftrivial-auto-var-init=zero`, PIE with `-z relro -z now`, `-fstack-protector-strong`, `-fstack-clash-protection`, and
`-fcf-protection=full` on x86 GNU/Linux. It sets only an option the command line has not already set, so an explicit
flag wins. The list can change between major releases.

Inference: a Yocto or Buildroot build's own flags win over it, and the two can disagree on the `_FORTIFY_SOURCE`
level. Use one source of flags.

## The `_FORTIFY_SOURCE` Rule

- Leave the level the build system sets. Yocto sets 2 and drops it at `-O0`. Buildroot offers 1, 2, or 3 through
  `BR2_FORTIFY_SOURCE_*`.
- In a standalone build, use 3 with GCC 12 or newer and glibc 2.35 or newer. Otherwise use 2. The glibc 2.35 NEWS
  says level 3 is available with glibc and GCC 12 and later, and GCC with glibc 2.34 gets level 2.
- A `-O0` build gets no fortification, so a debug-build test does not exercise it. Level 3 needs `-O1` or higher and a
  compiler that can derive the destination size.
- Disable it in sanitizer builds, because `_FORTIFY_SOURCE` is incompatible with AddressSanitizer.
- Add it only for glibc. Do not add it for musl or newlib (inference).
- Level 3 can break code that uses flexible array extensions or `malloc_usable_size`. Buildroot's level 2 help text
  warns that some conforming programs might fail, and level 3 adds run-time overhead.

## How Yocto and Buildroot Inject Flags

The two systems deliver flags differently. The `SKILL.md` section "Warnings and Build Flags" gives the rule that
serves both.

Yocto (`meta/conf/distro/include/security_flags.inc` in openembedded-core, blob `824ba2c0e3f1`, branch `blacksail`):

- It sets `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2` when optimisation is not `-O0`,
  `-Wformat -Wformat-security -Werror=format-security`, and linker `-Wl,-z,relro,-z,now`. PIE comes from GCC's
  `--enable-default-pie`.
- It appends the flags to `TARGET_CC_ARCH` and `TARGET_LDFLAGS` for the target class, so `${CC}` carries them even if
  a recipe ignores `CFLAGS`. Inference: a Makefile that hard-codes `gcc` or `cc` gets neither the flags nor the cross
  compiler.
- A recipe that links without `LDFLAGS` fails the `ldflags` QA check. The documented workaround is
  `TARGET_CC_ARCH += "${LDFLAGS}"`.
- The file keeps per-recipe opt-outs and says the aim is to shrink that list over time.

Buildroot (tag `2026.08.2`, `Config.in`, `package/Makefile.in`, `toolchain/toolchain-wrapper.mk`):

| Option                                        | Effect                                                                                |
| --------------------------------------------- | ------------------------------------------------------------------------------------- |
| `BR2_PIC_PIE`                                 | PIE, on by default where supported                                                    |
| `BR2_SSP_NONE`, `_REGULAR`, `_STRONG`, `_ALL` | `-fstack-protector`, `-fstack-protector-strong` (default when supported), or `-all`   |
| `BR2_RELRO_NONE`, `_PARTIAL`, `_FULL`         | Full is the default when PIE is supported; it selects PIE                             |
| `BR2_FORTIFY_SOURCE_1`, `_2`, `_3`            | Level 1 is the default; level 3 needs GCC 12 or newer; all need glibc and above `-O0` |

- Buildroot's toolchain wrapper adds the stack protector, PIE, and RELRO, so they reach every compile through the
  wrapper. `_FORTIFY_SOURCE` travels in `TARGET_CFLAGS` through `TARGET_HARDENED`. Inference: it reaches only builds
  that use `TARGET_CFLAGS` or `TARGET_CPPFLAGS`.
- `$(MAKE) $(TARGET_CONFIGURE_OPTS)` passes the flag variables to a hand-written Makefile on the `make` command line.
  That beats a plain `CFLAGS += ...` in the Makefile. Put the project's flags in `PROJECT_CFLAGS` after `$(CFLAGS)`,
  or write `override CFLAGS += ...`.

The OpenSSF set is broader than both build systems. At these pins, neither `security_flags.inc` nor Buildroot's
`Config.in`, `package/Makefile.in`, or `toolchain-wrapper.mk` sets `-fstack-clash-protection`,
`-fstrict-flex-arrays=3`, `-fcf-protection=full`, or `-ftrivial-auto-var-init=zero`. Add them in the project's flag
file only where the toolchain accepts them.

## Verifying a Binary

Check the finished binary, not the flag list. Run these on the target-architecture ELF, with the cross toolchain's
`readelf` when the host differs:

```sh
readelf -h  app | grep Type                    # DYN (Position-Independent Executable file) means PIE
readelf -lW app | grep -E 'GNU_RELRO|GNU_STACK' # GNU_RELRO present; GNU_STACK flags RW, never RWE
readelf -dW app | grep -E 'BIND_NOW|FLAGS'     # BIND_NOW or NOW for full RELRO
readelf -sW app | grep -E '__stack_chk_fail|_chk@'  # stack protector and fortified calls in use
checksec --file=app                            # one-line summary of the same properties, where installed
```

An absent `__stack_chk_fail` means the compiler found no function that needed a canary, or the flag did not reach the
compile. Absent `_chk` symbols at `-O2` mean the fortification did not reach the compile, or the code calls no
fortified function.

To confirm that flags reached a Yocto compile, read `temp/run.do_compile` in the recipe's work directory. The file
holds the compiler command. `log.do_compile` shows only the output, so it does not show the flags.

## Runtime Hardening

Runtime address-space randomisation (`randomize_va_space`), KASLR, and Yocto's complete flag tables belong to the
`yocto-security-hardening` skill. Load it for those; it holds the values, so this file carries none.
