# clangd and compile_commands.json

How clangd finds a compilation database, how to produce one in each kind of tree, and how to repair a database that
GCC built. Recipes marked as inference were not run; confirm each with `clangd --check=<file>`.

## Contents

- How clangd Finds the Database
- Verify a Setup
- The Query Driver
- Repairing a GCC Database
- Indexing
- Recipe per Tree
- clang-tidy and the Analyzer
- Formatting Through clangd

## How clangd Finds the Database

clangd looks for `compile_commands.json` in the parent directories of each edited file, and in a `build/` subdirectory
of each. For `$SRC/gui/window.cpp` it searches `$SRC/gui/`, `$SRC/gui/build/`, `$SRC/`, `$SRC/build/`, and so on up.
A database anywhere else needs one of these:

- a symlink or copy of the file in `$SRC`;
- `CompileFlags: CompilationDatabase: <dir>` in `.clangd`, with an absolute path or one relative to the fragment;
- the command-line flag `--compile-commands-dir=<dir>`, which also serves headers outside the project directory.

A header gets the command of a file that includes it, when clangd has opened one. Otherwise clangd picks the database
entry with the closest file name, which can be wrong. clangd supports only self-contained headers, and
`compdb -p build/ list` adds header entries.

`compile_flags.txt`, one flag per line in the source root, is the hand-written alternative. Background indexing does
not work with it, and clangd ignores it when `compile_commands.json` exists.

## Verify a Setup

Run `clangd --check=<file>` on one source file. The output must say "Compile command from CDB is", and a line "Generic
fallback command is" means clangd did not find the database. Restart clangd after the database changes. Then read the
`drv_unknown_argument` diagnostics and add each rejected flag to `CompileFlags: Remove`.

## The Query Driver

For a cross compiler, clangd runs the driver named in the database command as `<driver> -E -v` and reads its target
and system include list, then adds `--target=<triple>` and `-isystem <dirs>` to the command. Without that, clang
cannot find the C library headers of a custom toolchain, and the editor reports missing headers or wrong type sizes
(inference).

clangd runs a binary named by the database only when it matches the allowlist given by `--query-driver`. That flag is
command-line only: no `.clangd` key carries the allowlist. A `.clangd` file can pick the compiler through
`CompileFlags: Compiler`, which replaces argv[0] and controls target inference, but clangd queries that compiler
only when its name matches the pattern passed on the command line. A cross GCC outside the allowed pattern therefore
needs the pattern widened on the command line. Tell the user to set the flag in the editor or in the agent's LSP
launcher, because writing `.clangd` alone does not do it.

```sh
clangd --compile-commands-dir=build --query-driver='/opt/toolchain/bin/arm-none-eabi-*'
```

The flag takes comma-separated globs. Follow these rules:

- Match the glob to argv[0] as written in the database. Use an absolute driver path in the database, or put the driver
  directory on `$PATH`, because a relative name defeats clang's heuristics.
- The docs do not say whether the glob is matched before or after clangd makes a bare compiler name absolute, so test
  with `--check`.
- Allow the `g++` driver as well as `gcc` when the project has C++ files.
- Use `--query-driver=**` only in a trusted checkout. It allows any compiler that the database names, so a hostile
  database can run an arbitrary binary (inference).
- Setting `BuiltinHeaders: QueryDriver` makes clangd use the queried compiler's own builtin headers. With a GCC driver
  this can cause false positive diagnostics, because clang parses another compiler's headers.

An editor passes the flag through its own setting: `clangd.arguments` in VS Code and coc, the `cmd` table in Neovim,
and the program list in Emacs eglot.

## Repairing a GCC Database

A database from a GCC build holds flags that clang rejects, with the diagnostic `drv_unknown_argument`, or
`-Wunknown-warning-option` for warnings. An unknown argument can be fatal for indexing, not only noise, and then find
references and call hierarchy fail silently (inference from a reported case: an arm64 kernel needed
`Remove: -mabi=lp64`).

Start a `.clangd` file for a GCC-built kernel from this, then extend it from `clangd --check` output:

```yaml
CompileFlags:
  Add: [-Wno-unknown-warning-option]
  Remove: [-mno-fp-ret-in-387, -mpreferred-stack-boundary=*, -mskip-rax-setup, -mindirect-branch=*, -mindirect-branch-register, -fconserve-stack, -fno-var-tracking-assignments, -mabi=lp64]
Diagnostics:
  Suppress: [drv_unknown_argument]
```

The flags come from the x86 and arm64 reports in clangd issues 662 and 1200. How `Remove` matches:

- A recognised clang flag, such as `-I`, goes with its arguments.
- A value ending in `*` removes every argument with that prefix.
- Any other value must match exactly, so write a GCC-only flag out in full or use the `*` form.
- Flags added by the same `CompileFlags` entry stay.

The broad form `Remove: [-m*, -f*]` works, and ESP-IDF ships it, but it also drops flags that change how the code parses.
`-funsigned-char`, `-fshort-wchar`, and `-ffreestanding` are examples (inference), so prefer a targeted list when the tree
relies on them. Add `-Werror` to `Remove` so warnings do not become errors in the editor.

A clang build gives the cleanest database. In the kernel, `make LLVM=1` still left `-fconserve-stack` and
`-mrecord-mcount` errors on one 6.8 tree, so keep the `Remove` list. After a switch of compilers, regenerate the
database, because an old database can mix GCC and clang commands (inference).

## Indexing

The background index parses every translation unit in the database on a thread pool and caches the result in
`.cache/clangd/index/` next to `compile_commands.json`. Find references and call hierarchy need it for files that the
session has not opened. A very large tree can take hours and gigabytes of memory.

Turn it off for a tree with this `.clangd` fragment, optionally under `If: PathMatch:` to limit the paths:

```yaml
Index:
  Background: Skip
```

`--background-index=0` on the command line does the same. The cost: with `Skip`, find references and call hierarchy
see only the files that the session opened, plus any static index loaded with `Index: External` (inference). An agent
that needs tree-wide references keeps the default `Build`, or loads a prebuilt index made by `clangd-indexer`.

clangd returns at most 1000 references; `--limit-references=0` removes the cap.

## Recipe per Tree

Every recipe ends the same way: confirm the database with `clangd --check`, give clangd the query driver for a cross
compiler, and regenerate the database after a rebuild. Regenerate also when the compiler changes.

### Linux Kernel

`make compile_commands.json` exists from v5.10, together with the move of the script to
`scripts/clang-tools/gen_compile_commands.py`. The script reads the `.cmd` file that kbuild writes beside each object, so
it lists only files that this build compiled. Build first, then generate:

```sh
make LLVM=1 ARCH=arm64 O=build defconfig
make LLVM=1 ARCH=arm64 O=build -j"$(nproc)"
make LLVM=1 ARCH=arm64 O=build compile_commands.json

# GCC build: the same targets with CROSS_COMPILE and no LLVM=1
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- O=build compile_commands.json
```

With `O=build` the file is expected in `build/`, where clangd finds it from the source root (inference). For an
out-of-tree module, run `make -C <kernel-build> M=$PWD compile_commands.json`. Before v5.10, the script sits at
`scripts/gen_compile_commands.py` (present at v5.4); run it by hand with `-d <objdir>`.

For a GCC build, apply "Repairing a GCC Database".

### U-Boot

U-Boot ships `scripts/gen_compile_commands.py` from v2024.01, ported from the kernel's script. There is no make target.
Build a board first, then run the script from the repository root:

```sh
make CROSS_COMPILE=aarch64-linux-gnu- <board>_defconfig
make CROSS_COMPILE=aarch64-linux-gnu- -j"$(nproc)"
./scripts/gen_compile_commands.py
```

The script writes `compile_commands.json` in the current directory, and the repository's `.gitignore` already ignores it.
It takes the kernel script's `-d`, `-o`, and `-a` options; for an `O=` build pass `-d <builddir>` (inference). Before
v2024.01, copy the kernel's script (inference). A normal U-Boot build uses GCC, so apply "Repairing a GCC Database" and
list the failing flags with `--check`. A clang-built sandbox (`HOSTCC=clang CC=clang`) gives the cleanest database
(inference); almost all architectures keep `gd` in a global register, which clang does not support, so a board needs
GCC.

### Yocto

| Recipe type                     | Database                                                                                            |
| ------------------------------- | --------------------------------------------------------------------------------------------------- |
| Inherits `cmake`                | The class always passes `-DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=ON`; the file lands in `B`.           |
| Inherits `meson`                | Meson writes it by default.                                                                         |
| Kernel, `cml1`, or `u-boot.inc` | No support in OE-core. Run the in-tree make target or script against `B` after a build (inference). |

Find `B` with `bitbake-getvar -r <recipe> B` or `bitbake -e <recipe>` (standard BitBake commands, not checked against
the sources here). Point clangd at it:

```yaml
# <workspace>/sources/<recipe>/.clangd
CompileFlags:
  CompilationDatabase: /abs/path/to/B
```

Whether `B` equals `WORKDIR/build` under `devtool modify` is not established, so read it from the recipe. The cross
compiler sits under the recipe's `recipe-sysroot-native`; read argv[0] from the database and match it exactly in
`--query-driver` (inference).

`devtool ide-sdk` (Yocto 5.0 and later) generates IDE configuration for a recipe, and `IDE_SDK_INTELLISENSE = "clangd"`
opts a recipe in to clangd. The clangd text was read only in the newest documentation, so older releases may differ.
With a `.clang-format` in the source, it sets VS Code to format C and C++ on save, so check `.vscode/settings.json`.

With the standard SDK, source `/opt/poky/<version>/environment-setup-<arch>-poky-linux`, which defines `CC` with
`--sysroot`, and then use the project's CMake or Meson export or `bear -- make`. OE-core has no Bear recipe, so Bear
comes from the host.

### Buildroot

The Buildroot manual documents no clangd or compilation database method. Treat every step here as untested inference.
The `<pkg>-rebuild` and `<pkg>-reconfigure` targets make sense only with `<pkg>_OVERRIDE_SRCDIR` set in `local.mk` or
with an edited build directory.

- CMake package: add `<PKG>_CONF_OPTS += -DCMAKE_EXPORT_COMPILE_COMMANDS=ON` in a br2-external `.mk` file or in
  `local.mk`, then run `make <pkg>-reconfigure`. The file should appear in `output/build/<pkg>-<ver>/buildroot-build/`.
- Package built by plain make: run `bear -- make <pkg>-rebuild` from the Buildroot top directory.
- Kernel: run `make -C output/build/linux-<ver> ARCH=<arch> CROSS_COMPILE=<output/host/bin/tuple-> compile_commands.json`.
- Query driver: `<buildroot>/output/host/bin/*-gcc`, plus `*-g++` for C++.

### CMake, Meson, and Plain Make

```sh
cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON [-DCMAKE_TOOLCHAIN_FILE=<file>]
meson setup build [--cross-file <file>]
bear -- make
```

CMake writes the file only with the Makefile and Ninja generators, and it does not work well with unity builds. Meson
writes it into the build directory at `meson setup`, so no option is needed. Bear records real compiler calls, so run
it on a clean or forced build (`make clean; bear -- make`). Bear 3 and later use `bear -- make`; older versions use
`bear make`. Prefer the native export of CMake or Meson where one exists. `make -n | bear parse-sh` handles a build that
cannot run.

A Meson database from a GCC build can be unusable for clangd. Build a second directory with
`CC=clang CXX=clang++ meson setup build-clang`, run `ninja -C build-clang`, and set
`CompileFlags: CompilationDatabase: build-clang` in `.clangd`. That directory drifts from the main build after a checkout,
so rebuild it then.

### MCU SDKs

| SDK         | Database                                                                                                       |
| ----------- | -------------------------------------------------------------------------------------------------------------- |
| Zephyr      | `west build -p auto -b <board> <app>` always writes `build/compile_commands.json`.                             |
| ESP-IDF     | `idf.py set-target <chip> && idf.py reconfigure` writes `build/compile_commands.json`.                         |
| Pico SDK    | Put `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)` near the top of `CMakeLists.txt`; configure writes it to `build/`. |
| STM32CubeMX | Configure with `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` and CubeMX's `gcc-arm-none-eabi.cmake` toolchain file.     |

The Pico entry rests on a maintainer reply in a VS Code extension issue, and the CubeMX entry on a forum log, not on
the vendors' documentation. CubeMX owns the generated `CMakeLists.txt`, so pass the option on the command line
rather than editing that file; `CMakePresets.json` is user-editable and can carry it (inference). Pass the toolchain
file with `-DCMAKE_TOOLCHAIN_FILE=`, as in the CMake command above.

Clangd flags: `--compile-commands-dir=build --query-driver=<toolchain>/bin/arm-none-eabi-*`. For Zephyr the driver
is `$ZEPHYR_SDK_INSTALL_DIR/arm-zephyr-eabi/bin/arm-zephyr-eabi-*`. This `.clangd` start for Zephyr comes from
community configurations, not from Zephyr's documentation:

```yaml
CompileFlags:
  Add: [-Wno-unknown-warning-option]
  Remove: [-mfp16-format=*, -fno-reorder-functions, -fno-printf-return-value]
Diagnostics:
  Suppress: [drv_unknown_argument]
```

ESP-IDF ships a patched clangd, `esp-clangd`, that adds `--custom-config-file=<yaml>`. It recommends
`--query-driver=**`, and a config file holding `BuiltinHeaders: QueryDriver` and `Remove: [-m*, -f*]`. A clang-built
project (`IDF_TOOLCHAIN=clang`) needs no filtering. In the STM32 extension, forum posts report a generated query driver
that named only `arm-none-eabi-gcc`, and `-mcpu=` flags rejected for a guessed host target until `.clangd` `Add` gave an
explicit `--target`.

## clang-tidy and the Analyzer

clangd runs only the matcher-based clang-tidy checks. It skips `clang-analyzer-*`, so run the analyzer from the shell:

```sh
clang-tidy -p build/ <file>
run-clang-tidy.py -p=build/
```

`-p` reads the database from that directory. The clang-tidy command has no query driver. It uses the database command
as written, so GCC-only flags and cross include paths need `--extra-arg` or `--extra-arg-before`. Both paths read the
same `.clang-tidy` file. Pin the tool version as described in [tooling.md](tooling.md).

clangd merges its own `Diagnostics: ClangTidy` settings (`Add`, `Remove`, `CheckOptions`) with `.clang-tidy` and wins on
conflict, and `Remove` beats `Add`. Its `CheckOptions` use the form `<key>: <value>`. `FastCheckFilter` defaults to
`Strict`, so checks not measured as fast do not run; `Loose` or `None` widens the set. `--clang-tidy=0` turns the clangd
integration off.

## Formatting Through clangd

clangd embeds clang-format and uses the nearest `.clang-format` for a file. `--fallback-style` applies only when no
`.clang-format` exists. No `.clangd` key controls formatting, because the `Style` block covers only include style,
namespaces, and header quoting. clangd formats only when the client sends a formatting request, so an agent that
uses navigation and diagnostics never reformats a file. For a human's editor, turn format-on-save and format-on-type
off for a kernel or U-Boot tree (client settings, such as `editor.formatOnSave` in VS Code).

A Meson project with a `.clang-format` at its root also has a `clang-format` ninja target that reformats every C and
C++ file. Do not run it in a tree whose files are not already clean.

For which lines to format, read [tooling.md](tooling.md).
