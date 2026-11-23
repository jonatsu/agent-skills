# Kernel Debug Tools

Static analysis, compiler warning levels, runtime debug options, fuzzing, and product hardening configuration for
kernel code. The skill body says which check applies to which change. This file explains what each tool reports and
what it costs.

## Contents

- Sparse
- Coccinelle
- Warning Levels
- Runtime Debug Options
- Syzkaller
- Hardening Configuration

## Sparse

Sparse is a semantic checker that the kernel build drives. `C=1` checks the files that are rebuilt. `C=2` checks
every file, rebuilt or not.

- The `CF` make variable passes extra arguments to sparse. The build already passes `-Wbitwise`.
- The make help names sparse as the default value of `CHECK`, so `make CHECK=<tool> C=1` runs another checker.

Sparse reads annotations that GCC ignores. The tree defines most of them in `include/linux/compiler_types.h`, and
`__bitwise` in `include/uapi/linux/types.h`, under the `__CHECKER__` symbol that sparse sets:

- `__bitwise` marks an integer type that must not mix with plain integers or other bitwise types. Typical cases are
  little-endian, big-endian, and CPU-endian values. Declare it as `typedef int __bitwise name_t;`. Only the constant
  `0` converts silently.
- `__force` marks a cast that deliberately crosses a bitwise or address-space boundary. Add it after you confirm the
  conversion is intended, because it hides the report instead of fixing it.
- `__user` marks a pointer into userspace. `__iomem`, `__percpu`, and `__rcu` do the same for their address spaces.
- All four address-space annotations are `noderef`, so sparse reports a direct dereference. Reach user memory and I/O
  memory through the tree's accessors, and find them with `git grep`.

A sparse report on a pointer or endian annotation usually points at a missing or wrong annotation in your new code.
Fix the type first, and use `__force` last.

## Coccinelle

`make coccicheck` applies the semantic patches under `scripts/coccinelle`. It needs Coccinelle 1.0.0-rc11 or later.
Choose the output with `MODE=`:

- `report` prints `file:line:column-column: message`, and is the default.
- `patch` proposes a fix with a commit message, where the semantic patch supports it.
- `context` shows the lines of interest in a diff-like style, and `org` writes an Emacs Org report.
- `chain` tries the modes in order. `rep+ctxt` runs report and then context.

Not every semantic patch implements every mode. Narrow and tune a run with these variables:

- `M=<directory>` limits the run to one directory, such as your driver. It also works for an out-of-tree module.
- `COCCI=<file>.cocci` runs one semantic patch.
- `V=1` prints verbose output. `DEBUG_FILE=<log>` keeps stderr in a file, which the tool never overwrites.
- `J=<n>` sets the parallelism. `SPFLAGS` passes extra flags to `spatch`.

The documentation states that Coccinelle produces false positives, so treat every report as a lead. Read each
proposed patch before you apply it. Apply it only when it fixes a real defect in code you are changing.

## Warning Levels

`W=` raises the compiler warning level, and the digits combine, as in `W=12` or `W=123`. `scripts/Makefile.warn`
defines each group. Read it in the target tree for the exact flags of your compiler and release. A directory target
limits the build, as in `make W=1 drivers/foo/`.

- `W=1` is described as warnings that may be relevant and do not occur often. It adds `-Wmissing-format-attribute`,
  `-Wmissing-include-dirs`, `-Wunused-const-variable`, and `-Wundef`. It also stops hiding diagnostics that the
  default build suppresses, such as unused-but-set variables.
- `W=2` covers warnings that occur quite often but may still be relevant. It adds `-Wshadow`, `-Wunused-macros`,
  `-Wdisabled-optimization`, and `-Wlogical-op`. It also re-enables the `-Wextra` diagnostics for missing field
  initializers and negative shifts.
- `W=3` is described as more obscure warnings that can most likely be ignored. It adds `-Wconversion`,
  `-Wcast-align`, `-Wcast-qual`, `-Wpadded`, `-Wpacked`, `-Wsign-compare`, `-Wswitch-default`, and similar flags. It
  also re-enables the unused-parameter warning.
- `W=e` turns warnings into errors, as `CONFIG_WERROR` does. `W=c` adds extra checks at the configuration stage.

Fix every `W=1` report that your change introduces. Read `W=2` and `W=3` output for your own files, and fix what
points at a real defect. `4.Coding.rst` asks that submitted code produce no compiler warnings. It also asks you to
fix the cause of a warning rather than hide it.

Inference: leave warnings in code you did not change alone. A patch whose only purpose is to silence a tool is hard
to justify upstream.

## Runtime Debug Options

Runtime options need a bootable kernel. Build a separate debug configuration, because some options exclude each other
and others slow the target too much for product use. Each entry gives what the option finds and the cost its source
states. Where the source states no cost, the entry says so.

- KASAN finds out-of-bounds accesses and use-after-free in slab, page, vmalloc, stack, and global memory. Enable
  `CONFIG_KASAN` plus one mode.
  - `CONFIG_KASAN_GENERIC` is the debugging mode. It runs on x86_64, arm, arm64, powerpc, riscv, s390, xtensa, and
    loongarch, with significant performance and memory overhead.
  - `CONFIG_KASAN_SW_TAGS` is arm64 only, with moderate memory overhead. It suits real workloads on memory-limited
    devices.
  - `CONFIG_KASAN_HW_TAGS` needs arm64 with MTE and has low overhead. It can run in production.
  - The software modes also choose `CONFIG_KASAN_INLINE`, up to 2 times faster, or `CONFIG_KASAN_OUTLINE`, a smaller
    binary.
  - Software KASAN conflicts with `VMAP_STACK` unless `CONFIG_KASAN_VMALLOC` is on, which costs more memory. Modules
    get shadow memory from the module allocator.
  - KASAN reports only the first invalid access by default. `CONFIG_STACKTRACE` adds allocation and free traces.
  - `KASAN_SANITIZE_<file>.o := n` in a `Makefile` switches off instrumentation for one file.
- UBSAN reports undefined behavior, such as an oversized shift. Enable `CONFIG_UBSAN`. Exclude a file with
  `UBSAN_SANITIZE_<file>.o := n`. `CONFIG_UBSAN_ALIGNMENT` is off by default where unaligned access is efficient,
  and it produces many reports when on. The documentation states no cost.
- KCSAN finds data races with watchpoints. It needs GCC 11 or Clang 11 or later. Enable `CONFIG_KCSAN`.
  - The documentation states a 5.0 times slower boot on 8 CPUs with the default configuration, and a few MiB of
    memory.
  - `lib/Kconfig.kcsan` makes it depend on architecture support and on KASAN being off, so give it its own build.
  - Mark an intended race with `data_race()`, `__data_racy`, or `__no_kcsan`.
  - A race at unknown origin often comes from DMA or uninstrumented code, which matters for drivers.
- KFENCE finds heap out-of-bounds access, use-after-free, and invalid free by sampling. Enable `CONFIG_KFENCE`. Set
  `kfence.sample_interval` in milliseconds on the command line, where `0` disables it.
  - It has near zero overhead and suits production, but a short test may never sample the faulty allocation.
  - The default pool takes 2 MiB with 4 KiB pages, which matters on a small board.
- lockdep tracks lock acquisition order and interrupt context. It finds lock orders that could deadlock before they
  do. Enable `CONFIG_LOCKDEP` and `CONFIG_PROVE_LOCKING`.
  - `4.Coding.rst` calls it one of the heavier tools and asks that non-trivial locking run under it before
    submission.
  - `CONFIG_DEBUG_ATOMIC_SLEEP`, `CONFIG_DEBUG_SPINLOCK`, and `CONFIG_DEBUG_MUTEXES` add further locking checks.
- kmemleak finds unreferenced allocations. Enable `CONFIG_DEBUG_KMEMLEAK`, mount debugfs, and read
  `/sys/kernel/debug/kmemleak`.
  - A scan thread runs every 10 minutes. `echo scan > /sys/kernel/debug/kmemleak` forces a scan.
  - The first reported object can make later ones look orphaned. The documentation states no cost.
- KCOV exports the coverage of a task to userspace for coverage-guided fuzzing, and finds no bugs itself. Enable
  `CONFIG_KCOV` and mount debugfs. `CONFIG_KCOV_ENABLE_COMPARISONS` adds comparison operands. The documentation
  states no cost.
- Fault injection fails allocations on purpose so that error paths run. `4.Coding.rst` recommends it, because
  untested recovery code tends to be broken.

KASAN has KUnit tests under `CONFIG_KASAN_KUNIT_TEST`, which confirm that the detector works on your build. Treat a
sanitizer report as a defect in your code until you show otherwise.

## Syzkaller

Syzkaller fuzzes system calls and needs coverage from `CONFIG_KCOV=y`. The syzkaller kernel-configuration page lists
`CONFIG_KCOV_INSTRUMENT_ALL=y`, `CONFIG_KCOV_ENABLE_COMPARISONS=y`, and `CONFIG_DEBUG_FS=y` with it. The same page
names these companions:

- KASAN with `CONFIG_KASAN_INLINE`, to catch use-after-free and out-of-bounds bugs.
- `CONFIG_DEBUG_KMEMLEAK` as an optional leak detector.
- The lockdep and debug options above, with the advice that more debugging options are better.
- Fault injection, which syzkaller picks up automatically when enabled.

Read that page in the syzkaller repository for the current list, because the symbols follow the kernel. Inference:
fuzz a driver only on a target the fuzzer can reach, such as a virtual machine or hardware the user provides.
Inference: reproduce a fuzzing finding before you propose a fix.

## Hardening Configuration

`kernel/configs/hardening.config` and the Kernel Self Protection Project (KSPP) recommended settings belong to the
product's kernel configuration. They are not driver patch content. Leave them out of driver patches, and route a
change to a product defconfig through the product's own review.

- `make hardening.config` merges the fragment into the current `.config`.
- The fragment calls itself basic hardening with low or no performance impact on most workloads. It includes
  `CONFIG_STRICT_KERNEL_RWX`, `CONFIG_VMAP_STACK`, `CONFIG_STACKPROTECTOR_STRONG`, `CONFIG_HARDENED_USERCOPY`,
  `CONFIG_FORTIFY_SOURCE`, `CONFIG_LIST_HARDENED`, `CONFIG_KFENCE`, and `CONFIG_INIT_STACK_ALL_ZERO`. It enables
  `CONFIG_UBSAN_BOUNDS` with `CONFIG_UBSAN_TRAP`, and it lists options to keep off, such as `CONFIG_COMPAT_BRK`.
- The KSPP page at `https://kspp.github.io/Recommended_Settings.html` describes a more paranoid set. It marks some
  symbols by the release that introduced them. Check each symbol against the target tree's Kconfig before you use it.
- Inference: `CONFIG_UBSAN_TRAP` turns a UBSAN finding into a trap instead of a report. Keep it out of the
  configuration you use to collect reports.

Hardening options can change behavior that a driver relies on, such as stack layout or uninitialized memory. Test the
driver on the product configuration as well as on the debug configuration.
