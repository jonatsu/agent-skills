# U-Boot Coding, Checks, and Tests

How to write U-Boot C that its maintainers accept, check it, and test it on the sandbox. U-Boot follows Linux kernel
style with its own deviations, so read the tree's `doc/develop/codingstyle.rst` for the release in hand; the rules
below come from it at commit `e578056c766d`.

## Contents

- [Style](#style)
- [Build Flags](#build-flags)
- [Check a Change](#check-a-change)
- [Test on the Sandbox](#test-on-the-sandbox)
- [Navigate With clangd](#navigate-with-clangd)
- [Send Patches](#send-patches)

## Style

All U-Boot code follows the Linux kernel coding style: tabs, 80 columns where the file keeps them, no braces around
single statements, and `scripts/checkpatch.pl` as the gate. U-Boot adds its own rules:

- Map an I/O register region with a C structure, and check its layout with `check_member()`.
- Prefer `IS_ENABLED(CONFIG_X)` in C over `#if`, and a header stub over `#if` in a `.c` file. Compile out whole
  functions rather than parts of them, and mark possibly unused definitions `__maybe_unused`.
- Use `CONFIG_IS_ENABLED(X)` where the code is built for U-Boot proper, SPL, and TPL, because it checks the option
  for the phase being built.
- Log with `log_*()` and the driver model's device helpers, not the kernel's `printk` or `dev_*()`.
- Put a blank line before a function's final `return`.
- The kernel's networking comment style exception does not apply in U-Boot.
- Treat data from removable media, the network, or an unsigned image as hostile. Read multi-byte fields with
  `get_unaligned_be32()` and its relatives, or `fdt32_to_cpu()` for a raw device-tree cell, never by casting a byte
  buffer to a struct or integer pointer. Check each length against the bytes remaining, so no sum can overflow, and
  validate the whole input before acting on it.

The tree ships its own `.clang-format`, which differs from the kernel's, including a U-Boot `ForEachMacros` block.
Format only the lines you changed, with `git clang-format`, so unrelated lines keep their history. A personal
formatter profile rewrites most of a file into another style, so never run one over U-Boot code.

U-Boot is freestanding: it links no C library, so use its own `printf`, string, and memory helpers. Stack and heap
are small early in boot, particularly in SPL, so avoid large stack buffers there.

## Build Flags

The top `Makefile` sets the language and core flags, among them `-std=gnu11`, `-ffreestanding`, `-fno-builtin`,
`-fno-common`, and errors for implicit declarations and missing prototypes. A board enables the stack protector
through Kconfig. Add no `-std`, `-Werror`, or hardening flags in a driver or board `Makefile`, because the tree owns
them.

## Check a Change

Run these before posting, and fix what they report or state why a report does not apply:

| Check                   | Command                                                     |
| ----------------------- | ----------------------------------------------------------- |
| Style                   | `scripts/checkpatch.pl` on the patch, or `b4 prep --check`  |
| Extra compiler warnings | `make W=1` for the affected board; `W=2` and `W=3` add more |
| Sparse                  | `make C=1` for the files rebuilt                            |
| Coccinelle              | `scripts/coccicheck`                                        |
| Many boards at once     | `tools/buildman` for the boards the change touches          |

## Test on the Sandbox

The sandbox board builds U-Boot as a Linux program, so it runs tests on the build host:

```sh
make sandbox_defconfig
make -j"$(nproc)"
./u-boot -T -c "ut dm gpio"
```

`-T` selects the test device tree, and `ut` runs a C unit-test suite by name. The pytest framework in `test/py`
drives the built binary through its console; run it as `testing.rst` in the tree describes, for example through
`make check` or `make qcheck`. A patch that changes behaviour is expected to add or extend a test.

The sandbox also supports AddressSanitizer and libFuzzer upstream: `arch/sandbox/config.mk` adds
`-fsanitize=address` when `CONFIG_ASAN` is set, and `-fsanitize=fuzzer` when `CONFIG_FUZZ` is set. Because the
sandbox build is a host program, host tools such as cppcheck and clang-tidy run on it too. Their results do not cover
code built only for a target.

## Navigate With clangd

From v2024.01, U-Boot ships `scripts/gen_compile_commands.py`. Build the configuration first, then run the script
from the source tree; pass `-d <dir>` when the build used `O=<dir>`. U-Boot has no make target for it. For older
releases, wrapping the build in Bear should produce one (inference; untested). Point clangd at the cross compiler with
`--query-driver`, because that option is accepted only on clangd's command line.

## Send Patches

`b4` is the tree's preferred tool for preparing and sending a series, and the tree ships a `.b4-config`. `patman`
now lives outside the U-Boot tree. Read `doc/develop/sending_patches.rst` for the release in hand before sending.

### Patches Carried in a Build Layer

A product's build layer often carries U-Boot patches against a pinned release instead of sending them upstream. Keep
each one as a `git format-patch` file with its author and `Signed-off-by:`, give it the header the build system's
patch policy requires, and run the tree's `scripts/checkpatch.pl` on it. When the pin moves, rebase the patches onto
the new release, drop those upstream now contains, and build after each one.
