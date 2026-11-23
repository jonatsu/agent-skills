# clangd in embedded C and C++ trees: research notes

Read date for all pages without a pin: 2026-11-23. Tags used: "source states" (a page or file says it) and "inference"
(my reading of what follows). Anything from memory is marked "background knowledge".

Fetch route used: `crawl4ai md` for clangd.llvm.org pages (renders cleanly), `docs-mcp:fetch_url` inside
`code_execution` for batches, raw GitHub files and `commits/*.atom` feeds for pins. `gh` is not runnable in this lane
(Bash is read-only), so GitHub API calls went through `docs-mcp:fetch_url`.

## Pins for clangd documentation (clangd.llvm.org is built from the `llvm/clangd-www` repository)

Pages carry no date. The pin is the last commit that touched the page source, from
`github.com/llvm/clangd-www/commits/main/<page>.md.atom` read 2026-11-23.

| Page                                                 | Last commit touching it     | Date       |
| ---------------------------------------------------- | --------------------------- | ---------- |
| `config`                                             | `ae5866d4552e`              | 2026-09-18 |
| `installation`                                       | `4375510e9474`              | 2026-07-06 |
| `faq`                                                | `5cc0132bc7a3`              | 2025-11-30 |
| `troubleshooting`                                    | `07116b2c21d3`              | 2024-12-12 |
| `guides/system-headers`                              | `993722d2be98`              | 2022-09-28 |
| `design/compile-commands`                            | `e84f0d9d8d83`              | 2023-12-27 |
| `design/indexing`, `features`, `guides/remote-index` | not pinned; read 2026-11-23 |            |

clangd releases: the `clangd/clangd` releases feed lists stable `23.1.0` and `22.1.6` plus weekly snapshots
(newest `snapshot_20260913`, feed updated 2026-09-14). Licence of clangd: it is part of `llvm/llvm-project`
(`clang-tools-extra/LICENSE.TXT`, read at `main` 2026-11-23): Apache License v2.0 with LLVM Exceptions.

## Q1. clangd configuration

### Finding the compilation database

- Source states (installation, "Project setup"): clangd looks in the parent directories of each edited file for
  `compile_commands.json`, and also in subdirectories named `build/`. For `$SRC/gui/window.cpp` it searches
  `$SRC/gui/`, `$SRC/gui/build/`, `$SRC/`, `$SRC/build/`, and so on up.
- Source states (installation): for CMake, if the build directory is not `$SRC` or `$SRC/build`, symlink or copy
  `compile_commands.json` to `$SRC`.
- Source states (config, `CompileFlags.CompilationDatabase`): a `.clangd` fragment can set the directory to search.
  Values: one directory path (absolute, or relative to the fragment), `Ancestors` (search all parents, the default),
  or `None` (no database, default flags only).
- Source states (faq): the command-line flag `--compile-commands-dir=<path>` makes clangd use that database for all
  files, including headers outside the project directory.
- Source states (troubleshooting): after the database changes, restart clangd. The log shows whether the database was
  found and which command was used. (`clangd --check=<file>` prints "Compile command from CDB is: ..." and the
  internal cc1 args; `--check` exists from clangd 12; system-headers guide.) A log line "Generic fallback command
  is" means the database was not picked up.
- Source states (installation): `compile_flags.txt` (one flag per line in the source root) is the hand-written
  alternative. Background indexing does not work with it, and it is ignored when `compile_commands.json` exists.
- Source states (design/compile-commands): a header gets the command of a file that transitively includes it, if one
  was opened; otherwise clangd picks the database entry whose file name is closest (filename heuristic, can be
  wrong). FAQ points to `compdb` (Sarcasm/compdb) to add header entries. Clangd only supports self-contained headers.
- Source states (design/compile-commands): clangd always makes a bare compiler name absolute (via `$PATH`), adds
  `-fsyntax-only`, adds `-resource-dir=` (clangd's own builtin headers such as `<stddef.h>`), and drops some
  unsupported flags such as `-plugin`.

### What a `.clangd` file can set

- Source states (config): project config is a file named `.clangd` found in the source tree and its parents; user
  config is `~/.config/clangd/config.yaml` (Linux, `$XDG_CONFIG_HOME/clangd/config.yaml`). Precedence: user config,
  then inner project, then outer project. Fragments are separated by `---`. Changes apply as you edit.
- `If`: `PathMatch` and `PathExclude` are regular expressions that must match the whole path; in a project file the
  path is relative to the file, in a user file it is absolute. Conditions are ANDed, multiple values within one are
  ORed.
- `CompileFlags`: `Add` (appended to the command), `Remove`, `Compiler` (replaces argv[0]; the name controls flag
  parsing and target inference such as `gcc-arm-noneabi`; if it matches a `--query-driver` glob it is queried for
  include paths), `CompilationDatabase`, `BuiltinHeaders` (`Clangd` default, or `QueryDriver`).
- `Index`: `Background: Build|Skip` (checked for translation units only, not headers), `External` (`File:` for a
  `clangd-indexer` index or `Server:`, with `MountPoint`; declaring it disables background indexing under the mount
  point), `StandardLibrary: true|false`.
- `Diagnostics`: `Suppress` (list of codes, `'*'` for all, clang codes such as `-Wunused-result` or
  `err_unknown_type`, warning categories, and clang-tidy check names), `ClangTidy` (`Add`, `Remove`, `CheckOptions`,
  `FastCheckFilter`, `ExperimentalCustomChecks`), `UnusedIncludes: None|Strict` (Strict since clangd 17),
  `MissingIncludes: None|Strict` (None is default), `Includes.IgnoreHeader`, `Includes.AnalyzeAngledIncludes`.
- Others on the page: `Style` (`QuotedHeaders`, `AngledHeaders`, `FullyQualifiedNamespaces`), `Completion`,
  `InlayHints`, `Hover`, `SemanticTokens`, `Documentation`.
- Source states (config): the configuration mechanism is new in clangd 11.
- Source states (config, `ClangTidy`): clangd settings merge with `.clang-tidy` files and win on conflict.
  `Remove` beats `Add`. `CheckOptions` use `<key>: <value>` form, not the `key:/value:` pairs of `.clang-tidy`.
  `FastCheckFilter` default is `Strict`: only checks measured as fast run (this excludes recently added unmeasured
  checks). `Loose` runs all checks not known to be slow; `None` runs all.

### `CompileFlags: Remove` semantics (for dropping GCC-only flags)

Source states (config): a value that is a recognised clang flag (such as `-I`) is removed together with its
arguments, and synonyms such as `--include-directory=` also go. Otherwise a value ending in `*` removes every
argument with that prefix. Otherwise only an exact match goes. `-Xclang` is removed where needed. Flags added by the
same `CompileFlags` entry are not removed. The FAQ example uses `Remove: -mabi` (single value allowed; `-mabi` is
ARM and RISC-V ABI selection, so this is the doc's own embedded-flavoured example).

Inference: a GCC-only flag that clang does not recognise matches only by exact text or by the `*` prefix form, so
write `-fno-allow-store-data-races`, `-mno-fdpic` or `-fconserve-stack` literally, or use a prefix like `-mpreferred-stack-boundary=*`.
The `-W*` example on the config page strips all warning flags.

### `--query-driver`

- Source states (design/compile-commands, system-headers): clangd runs the compiler named in argv[0] of the compile
  command as `<driver> -E -v -x c++ /dev/null` (the guide shows `-xc++`; for C files the language flag follows the
  file) and parses `Target:` and the `#include <...> search starts here:` list, then adds
  `--target=<triple>` and `-isystem <dirs>` to the command. It needs a gcc-compatible `-v` output.
- Source states (system-headers): clangd does not do this by default because it executes binaries named by the
  build database. `--query-driver` is an allowlist of comma-separated globs; the driver that runs still comes from the
  compile command and must match one glob. Example:
  `--query-driver="/path/to/my/project/arm-g*,/path/to/other/project/gcc"`.
- Source states (troubleshooting): for an unusual compiler (cross-compiler, MinGW) pass
  `--query-driver=/path/to/mygcc[,/path/to/myg++]`. This is recommended over writing system include paths by hand,
  because include order matters. The glob "should match the command emitted by your build system in
  `compile_commands.json`, such as `/usr/bin/c++`".
- Without it (source states, system-headers): "most of clang's heuristics rely on the location of the driver and the
  target triple". A relative driver name breaks them; use an absolute path in the database or put the driver
  directory on `$PATH`. For custom embedded toolchains ("the worst scenario ... common for custom toolchains
  targeting embedded devices") the guide lists four options: give an explicit `--target` triple, add each system
  path with `-isystem` (and `-nostdlibinc`), use `--query-driver`, or patch clang.
- Source states (config `BuiltinHeaders`): with `QueryDriver`, clangd uses the compiler's own builtin headers. The
  page warns that when the driver is not clang this can cause "false positive diagnostics", because the embedded
  clang parses another compiler's builtin headers.
- Source states (system-headers): clangd ships only its own builtin headers; the C library headers come from the
  system or toolchain.

Inference: with a cross GCC that sits at `/opt/x/bin/arm-none-eabi-gcc`, the allowlist glob must match that exact
argv[0] string as written in the database (a bare `arm-none-eabi-gcc` is first made absolute via `$PATH`, per the
"tweaks" list; the docs do not say whether the glob is matched before or after that step, so give an absolute path in
the database or test with `--check`).

### Coordinator check: is `--query-driver` command-line only? (confirmed, with one precision)

Re-read `config` (pin `ae5866d4552e`) on 2026-11-23 and searched it for every mention of "query driver".

- Source states: there is no `.clangd` key that sets the query-driver allowlist. The page mentions `--query-driver`
  only as a command-line flag in two places: under `CompileFlags.Compiler` ("If the option matches a glob mentioned
  in `--query-driver`, then it will be invoked for extraction of include paths") and under
  `CompileFlags.BuiltinHeaders` (value `QueryDriver` uses "the headers extracted from the compiler via the
  `--query-driver` command line argument"). The system-headers guide and troubleshooting page also describe it only as
  a clangd flag. So a `.clangd` file can pick the compiler name (`Compiler`) but cannot allow it.
- Source states: the allowlist is mandatory for the query to happen, because clangd will not run a binary named in
  a database unless the glob allows it (system-headers guide).
- Precision on the fallback: the "falls back to clangd's builtin headers" sentence is documented for
  `BuiltinHeaders: QueryDriver` ("If a query driver is not supplied or does not match the compiler, then the Clangd
  builtin headers will be the fallback"). For the plain case (no `--query-driver` match) the docs say clangd uses
  clang's own heuristics, which rest on the driver directory and the target triple (system-headers guide). For a
  cross GCC whose layout clang does not know, that means missing or wrong C library headers. Inference: the user
  sees "file not found" for libc headers or wrong sizes for `long`, not a clangd error.
- What the user or editor must pass: the flag on the clangd command line, for example
  `clangd --query-driver=/opt/toolchain/bin/arm-none-eabi-*` (VS Code: `clangd.arguments`; Neovim: the `cmd` table;
  Emacs eglot: the program list; coc: `clangd.arguments`; from installation page, "Editor plugins"). The glob must
  match argv[0] of the command in the database. A `.clangd` file cannot carry it, so a skill that sets up a tree must
  tell the user to configure the editor or the agent's LSP launcher, not just write `.clangd`.
- Wrapper option (inference, background knowledge): a wrapper script on `$PATH` named `clangd` that execs the real
  clangd with `--query-driver=...` makes the setting travel with the tree. The docs do not describe this.

### Per-tree way to turn background indexing off (confirmed)

Source states (config `Index.Background`, faq "How do I stop clangd from indexing certain folders"): a `.clangd`
fragment with `Index:` / `Background: Skip` disables background indexing; `If: PathMatch:` limits it to some paths.
"Legal values are `Build` (the default) or `Skip`." It is checked for translation units only, not for the headers they
include. A `.clangd` file in the tree root applies to the whole tree (project config applies to `proj/**`), so it
is a per-tree switch. The command-line alternative is `--background-index=0` (troubleshooting). Caveat (inference
from design/indexing): with `Skip`, find-references and call hierarchy only see symbols from files the session has
opened plus whatever a static `Index.External` index supplies, so a coding agent that needs tree-wide references
should keep `Build` or load a prebuilt index.

### Background indexing on big trees

- Source states (design/indexing): the background index parses every translation unit in the database on a thread
  pool, caches results as `*.idx` files in `.cache/clangd/index/` next to `compile_commands.json`, and does not
  reindex unchanged files on restart. It gives full-project references, including those inside template
  instantiations. It is needed for "find references" beyond the files you opened.
- Source states (indexing, remote-index): for very large codebases (LLVM, Chromium) an index can take hours and
  gigabytes of memory; options are a prebuilt static index from `clangd-indexer` loaded with the `-index-file`
  option, or the remote index service.
- Source states (config, faq): `Index: Background: Skip` under an `If: PathMatch:` stops indexing of those paths
  (the FAQ example for "how do I stop clangd from indexing certain folders"). Declaring `Index.External` disables
  background indexing for its mount point.
- Source states (faq): clangd returns at most 1000 references by default; `--limit-references=0` removes the cap.
  A missing reference can also mean a file was not in the database.
- Source states (troubleshooting): a crash in background indexing can crash the whole process and repeat at start;
  `--background-index=0` avoids it, and `-j=1 --log=verbose` logs one file at a time to find the culprit.
- Source states (installation, coc and neovim examples): flags `--background-index` and `--clang-tidy` are passed on
  the clangd command line; `--clang-tidy=0` disables tidy (troubleshooting).
- Source states (faq "false or missing diagnostics"): clangd skips function bodies in included headers, which can
  give false unused-declaration diagnostics and miss diagnostics in headers.
- The clangd command-line help (`--help`) is the authoritative list of flags; no documentation page lists them, and
  clangd is not installed here, so flag defaults other than those above are unverified.

## Q2. Generating the database per tree

### Linux kernel

Pins: kernel `master` was `7.4-rc4` on 2026-11-23 (Makefile header); newest tag in the feed `v7.4-rc4`, last release
`v7.3`. `scripts/clang-tools/gen_compile_commands.py` last touched by commit `51fa14ab9705` (read on `master`).
Licence: `COPYING` states "GPL-2.0 WITH Linux-syscall-note"; the script carries `SPDX-License-Identifier: GPL-2.0`.

- Source states (script at `master`): the script ("Creates a compile_commands.json database from kernel .cmd
  files") parses the `.cmd` files that kbuild writes next to each built object (`.foo.o.cmd`). So it only sees files
  that were compiled in this build tree. Options: `-d/--directory` (build output dir, default `.`), `-o/--output`
  (default `compile_commands.json`), `-a/--ar` (default `llvm-ar`, used to list members of `.a` archives),
  `--log_level`, and positional paths (directories, `*.a`, or `modules.order`; default is the current directory).
  It skips `.git`, `Documentation`, `include` and `tools`. Entries use the compile command exactly as kbuild ran it
  (`command` = the saved prefix plus the source path), `directory` is the build directory.
- Source states (Makefile at `master`, "Clang Tooling" section): `make compile_commands.json` runs the script with
  `-a $(AR)`; prerequisites are `vmlinux.a $(KBUILD_VMLINUX_LIBS)` and, when `CONFIG_MODULES`, `modules.order`.
  For an external module build (`KBUILD_EXTMOD`) the prerequisites are the module's own. `clang-tidy` and
  `clang-analyzer` targets depend on it and print "requires CC=clang" otherwise (so the kernel's own
  `make clang-tidy` works only with a clang build). Inference: because the prerequisites are build targets, the
  target builds (or finds built) `vmlinux.a` and `modules.order`; a configured tree is required, and an unbuilt
  tree is a long build.
- Version facts, read from raw files at tags (2026-11-23):

| Question                                                     | Result                                                                                              |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| Script exists at `v5.4` as `scripts/gen_compile_commands.py` | yes (file present)                                                                                  |
| `compile_commands` in top `Makefile` at `v5.4` to `v5.9`     | no hits in any of the six tags                                                                      |
| `make compile_commands.json` target in `Makefile` at `v5.10` | yes (rule `$(extmod-prefix)compile_commands.json: scripts/clang-tools/gen_compile_commands.py ...`) |
| Script path `scripts/clang-tools/` at `v5.8`, `v5.9`         | file absent                                                                                         |
| Script path `scripts/clang-tools/` at `v5.10` and later      | present                                                                                             |

So the make target arrived in `v5.10` together with the move to `scripts/clang-tools/` (inference: the first
tag where both exist; I did not read the commit message). Before `v5.10`, run the script by hand from the
build directory. `v6.0` to `v6.2` Makefiles carry the same target.

- Source states (`Documentation/kbuild/llvm.rst` at `master`): `make LLVM=1` builds with clang for the host,
  `make LLVM=1 ARCH=arm64` cross-compiles, and `CROSS_COMPILE` is not used to prefix the clang binary when `LLVM=1`
  is set. The page does not mention `compile_commands.json` or clangd.
- Inference (this is the kernel's own recommended path for clangd): build with `LLVM=1` so the database holds clang
  flags. A GCC build produces a database with GCC-only flags (see pitfalls). Where the architecture cannot be built
  with clang, use the `.clangd` `Remove` list below.
- Source states (kernel `.clang-format`): present at tree root (header "Intended for clang-format >= 11"). The
  tree has no `.clangd` file at `master` (raw fetch returned empty).

### U-Boot

Pins: tags feed shows `v2027.01-rc2` newest, last release `v2026.10`. Licence: `Licenses/README` states
GPL-2.0 for U-Boot (with the standalone-application note); the doc page carries `SPDX GPL-2.0-only`.

- Source states (`scripts/gen_compile_commands.py`, header): "Ported and modified for U-Boot by Joao Marcos Costa",
  original author Tom Roeder; "Briefly documented at doc/build/gen_compile_commands.rst". Commit history
  of the script: `97fbb2eb016b` (2023-10-11, "scripts: Port Linux's gen_compile_commands.py to U-Boot"),
  `311df90b3eab` (docs, 2023-10-11), `830d83ec385d` (2024-05-13, "update to Linux v6.7").
- Release: the script is absent at tag `v2023.10` and `v2023.07`, present at `v2024.01` (raw files read). So the
  first release with it is `v2024.01`.
- Source states (`doc/build/gen_compile_commands.rst`): parses the `.cmd` file of each translation unit; "one needs
  to have a target (e.g. configs/xxx_defconfig) built before running the script":
  `make sandbox_defconfig && make && ./scripts/gen_compile_commands.py`. Output goes to the repository root as
  `compile_commands.json` and "no further modifications are needed" for the LSP. Re-run after rebuilding.
  For options: `./scripts/gen_compile_commands.py --help`; the script has the same `-d`, `-o`, `-a` (default
  `llvm-ar`) and `--log_level` options as the kernel's. It excludes `.git`, `Documentation`, `include`, `tools`.
- No make target: the top-level `Makefile` at `master` has no `compile_commands` string (read 2026-11-23). U-Boot
  `.gitignore` lists `/compile_commands.json`.
- Source states (`doc/build/clang.rst`): U-Boot can be built with clang (`make CROSS_COMPILE=... CC=clang`), but
  "almost all archs rely on storing gd in a global register" and clang does not support global register variables;
  the ARM backend is told not to use `r9` and `x18` with `-ffixed-r9` and `-ffixed-x18`, and inline assembly gets
  and sets the register. The page also says `CROSS_COMPILE` is used to derive the `--target` passed to clang, and
  that the sandbox build works with `HOSTCC=clang CC=clang`.
  Inference: a U-Boot database from a normal GCC build has GCC command lines, so the same unknown-flag handling as
  for a GCC-built kernel applies; which exact flags fail for a given board is not documented, so list them with
  `clangd --check` and remove them one by one. A clang-built sandbox tree is the cleanest case.
- Source states (`doc/develop/codingstyle.rst`): U-Boot has a `.clang-format` "copied directly from the Linux
  kernel". No `.clangd` file at `master`.

### CMake, Meson, plain Make and autotools

| Build system                      | Method                                                                                                                                                    | Source and pin                                                                                                                                                                                                 | Licence of the tool (as read)                                         |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| CMake                             | `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` writes `compile_commands.json` into the build directory                                                              | CMake docs "latest" page for the variable (read 2026-11-23; CMake tag feed newest `v4.5.1`)                                                                                                                    | CMake `LICENSE.rst`: 3-clause BSD text, "Copyright 2000-2026 Kitware" |
| Meson                             | writes it into the build directory at `meson setup`, no option needed                                                                                     | libvirt `clangd.html` ("Meson creates a compile_commands.json in the build directory"); Meson issue 6400 comment says it is generated but "not obvious from the docs"; Meson docs pages I read do not state it | Meson `COPYING`: Apache-2.0                                           |
| Make, autotools, scripts          | `bear -- make` (Bear 3 and later); older `bear make`; `make -n \| bear parse-sh` when the build cannot run                                                | clangd `installation` page (pin `4375510e9474`); Bear `README.md` at `master`; Bear releases feed newest `4.2.4` (2026-11-02)                                                                                  | Bear `COPYING`: GPL-3.0                                               |
| GNU Make without a clean build    | `compiledb make` wraps make; `compiledb -n make` skips the build; `make -Bnwk \| compiledb -o-` parses a dry run; "command" style needs `--command-style` | compiledb `README.md` at `master`; releases feed newest `0.10.7` (2025-03-23)                                                                                                                                  | compiledb `LICENSE`: GPL-3.0                                          |
| Headers missing from the database | `compdb -p build/ list > compile_commands.json` adds header entries                                                                                       | clangd `faq` (pin `5cc0132bc7a3`); compdb `README.rst`; releases newest `0.2.0` (2018-03-26)                                                                                                                   | compdb `LICENSE.txt`: MIT                                             |

- Source states (CMake page): the variable is "implemented only by Makefile Generators and Ninja Generators"
  and ignored by others; it "does not work well" with unity builds. The `command` entries hold the exact compiler
  call. It was added in CMake 3.5.
- Source states (Bear README): Bear "gives you working code navigation ... on any C/C++ project", names embedded
  toolchains (ARM, TI, Microchip), cross-compilers and compiler launchers (ccache, distcc) as use cases, and says
  to prefer the native export of CMake, Meson or Bazel when one exists. Output goes to the current directory.
  Inference: the build has to run (or be dry-run) because Bear records actual compiler invocations, so an
  up-to-date tree needs a clean or forced rebuild, as the clangd page says ("make clean; bear -- make").
- Source states (compiledb README): it avoids needing a clean build by using `make -n` and `-k`, and calls
  itself "more cross-compiling friendly". Python 3.3 or later.
- Source states (Meson `Code-formatting.md`, since 0.50.0): with `clang-format` installed and a `.clang-format` at
  the project root, Meson adds a `clang-format` ninja target that reformats all C and C++ files. This is a way to
  reformat the whole tree by accident; do not run `ninja clang-format` in a tree whose files are not already clean.
- Source states (libvirt `clangd.html`): when the default compiler is GCC, the Meson database "cannot be used with
  clangd due to differences in compiler invocation flags"; they build a second directory with
  `CC=clang CXX=clang++ meson setup build-clang`, run `ninja -C build-clang` for generated sources, and put
  `CompileFlags: CompilationDatabase: "build-clang"` in `.clangd`. They warn that the extra directory drifts out of
  sync after a checkout update and needs a fresh build. Counter-view (inference, WebSearch lead not verified at
  its source): some report clangd copes with GCC flags for simple userspace code.

### Yocto

Pins: `docs.yoctoproject.org` pages read 2026-11-23 are the "6.1-tip" documentation (the SDK page shows
`/opt/poky/6.1/`); the 5.0.7 SDK page was also read. OE-core `meta/classes-recipe/cmake.bbclass` last commit
`9949e7d68fd7` (2026-07-30); `meson.bbclass` last commit `77c5ed98db82` (2026-07-06). Licence of OE-core and the
docs was not read (the raw `COPYING.MIT` fetch came back empty); background knowledge: MIT and CC-BY-SA.

| Situation                                                    | What the documentation says                                                                                                                                                                                                                                                                                                                                                             | Evidence                                                         |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Recipe inherits `cmake`                                      | the class always passes `-DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=ON`, so `compile_commands.json` appears in the recipe build directory `B`                                                                                                                                                                                                                                                 | raw `cmake.bbclass` at `master` (OE-core `meta/classes-recipe/`) |
| Recipe inherits `meson`                                      | Meson writes it by default; no `compile_commands` string in `meson.bbclass`                                                                                                                                                                                                                                                                                                             | raw file at `master`; mailing list statement below               |
| Recipe uses `kernel.bbclass`, `cml1.bbclass` or `u-boot.inc` | no support: no `compile_commands` or `gen_compile` string in those three files at `master`                                                                                                                                                                                                                                                                                              | raw files read 2026-11-23                                        |
| Any recipe, via `devtool ide-sdk`                            | generates IDE config; for C and C++ it picks clangd or cpptools "matched to the recipe's real cross-compiler via the generated `compile_commands.json`"; clangd is automatic for LLVM/clang-built recipes, and a recipe can opt in with `IDE_SDK_INTELLISENSE = "clangd"`; with clangd and a `.clang-format` in the source tree it sets VS Code to format C and C++ on save with clangd | "6.1-tip" `dev-manual/devtool.html`, sections 20.3 and 20.3.1.6  |
| `devtool ide-sdk` release                                    | "Introduce a new `ide-sdk` plugin" is in the 5.0 release notes; the 4.3 and 4.2 notes have no match                                                                                                                                                                                                                                                                                     | `migration-guides/release-notes-5.0.html`                        |
| clangd wording in older docs                                 | the 5.0.7 SDK page has no clangd mention (zero hits); the clangd text was read only in the tip docs, so the release that added it is not established                                                                                                                                                                                                                                    | `5.0.7/sdk-manual/extensible.html`                               |
| Recipe type not supported by `ide-sdk`                       | an IDE configuration based on the `devtool build` workflow is generated "as a fallback"                                                                                                                                                                                                                                                                                                 | tip `devtool.html`, section 20.3                                 |
| Standard SDK                                                 | `. /opt/poky/<version>/environment-setup-<arch>-poky-linux`; this defines `CC` and friends; example `echo ${CC}` prints `i586-poky-linux-gcc -m32 -march=i586 --sysroot=/opt/poky/<version>/sysroots/i586-poky-linux`; a Makefile using `${CC}` then runs that command                                                                                                                  | tip `sdk-manual/working-projects.html`                           |
| Extensible SDK                                               | same `environment-setup-*` script, plus `devtool`                                                                                                                                                                                                                                                                                                                                       | tip and 5.0.7 `sdk-manual/extensible.html`                       |

- Source states (Yocto mailing list, Adrian Freihofer, 2024-11-03 and 2024-11-05): cmake and meson have built-in
  generators ("with meson it's enabled by default, with cmake we enable this feature" in `cmake.bbclass`); Bear is
  not in OE-core (no `bear-native` recipe); for the kernel and U-Boot the in-tree scripts "are available as make
  targets"; he was unsure the kernel script works when the kernel is built with GCC and noted Yocto did not yet
  build the kernel with clang; he proposed adding `oe_runmake compile_commands.json` to `cml1.bbclass`, which the
  files above show is not there. This is a maintainer's email, so it is background for the "no support" row, not
  documentation.
- Inference, kernel build target: the top-level `Makefile` defines `compile_commands.json` outside the
  `CONFIG_CC_IS_CLANG` block (only `clang-tidy` and `clang-analyzer` sit inside it), so the target itself works for
  a GCC build. What clangd does with the GCC flags is the separate problem in Q5.
- Inference, `devtool modify` flow for a CMake recipe: `devtool modify <recipe>` puts the source in the workspace;
  `bitbake <recipe>` (or `devtool build`) configures it and writes `compile_commands.json` into `B`; find `B` with
  `bitbake-getvar -r <recipe> B` or `bitbake -e <recipe> | grep ^B=` (background knowledge: standard BitBake
  commands; not read in these sources), then point clangd at it with `CompileFlags: CompilationDatabase: <B>` or a
  symlink into the workspace source directory. The `externalsrc` class page says `B` defaults to
  `${WORKDIR}/${BPN}-{PV}/`, separate from `S`; `cmake.bbclass` says its default is `B=WORKDIR/build`. Which one
  applies under `devtool modify` was not established.

### Buildroot

Pins: Buildroot manual "2026.08 manual generated on 2026-09-04 from git revision d5180309b1"
(`buildroot.org/downloads/manual/manual.html`); tags feed newest `2026.11-rc2`. `package/pkg-cmake.mk` last commit
`ef9f0a07ed40` (2026-02-04). Licence: `COPYING` states GPL version 2 or later with exceptions.

- Source states: the manual has no mention of `compile_commands`, `clangd`, "compilation database" or `Bear`
  (a case-insensitive search of the 388 kB page, positive control: `OVERRIDE_SRCDIR` and `make sdk` both matched).
  So there is no documented method.
- Source states (manual 8.14.6): `<pkg>_OVERRIDE_SRCDIR` in `local.mk` makes Buildroot rsync your source tree to
  `output/build/<package>-custom/`, and `make <pkg>-rebuild` and `make <pkg>-reconfigure` rerun compile or configure
  (these only make sense with the override or edited build directory files).
- Source states (manual): `make sdk` packs `output/host/` into `<tuple>_sdk-buildroot.tar.gz` in `output/images/`;
  after extraction run `relocate-sdk.sh`. For an external toolchain, Buildroot generates a wrapper program that
  adds the configured options.
- Source states (`pkg-cmake.mk`): configure runs `cmake` with
  `-DCMAKE_TOOLCHAIN_FILE=$(HOST_DIR)/share/buildroot/toolchainfile.cmake`, plus fixed flags (`-DBUILD_TESTING=OFF` and
  others); no `CMAKE_EXPORT_COMPILE_COMMANDS` string in the file. The build directory is `$(SRCDIR)/buildroot-build`
  unless the package supports in-source builds.
- Source states (`linux/linux.mk`): the kernel is built with `make -C $(LINUX_DIR)` and `LINUX_MAKE_FLAGS`
  (`ARCH`, `CROSS_COMPILE="$(TARGET_CROSS)"`, `KCFLAGS`, ...); no `O=` in the flags I saw.
- Inference (no documentation exists; test it): for a CMake package, add
  `<PKG>_CONF_OPTS += -DCMAKE_EXPORT_COMPILE_COMMANDS=ON` (in a br2-external `.mk` or `local.mk`) and run
  `make <pkg>-reconfigure`; the file lands in `output/build/<pkg>-<ver>/buildroot-build/`. For a package built by plain
  make, run `bear -- make <pkg>-rebuild` from the Buildroot top directory (Bear follows child processes; not tested).
  For the kernel, run
  `make -C output/build/linux-<ver> ARCH=<arch> CROSS_COMPILE=<output/host/bin/tuple-> compile_commands.json`. The cross
  compiler is `output/host/bin/<tuple>-gcc`.
- gh_grep on `buildroot/buildroot` found `compile_commands` only in one package patch (mbpoll); a zero from
  gh_grep is not proof of absence, so the manual search above is the evidence.

### MCU SDKs

| SDK                   | How the database appears                                                                                                                                                                                                                                                                                                                                   | Source and pin                                                                                                                                                                                                                   | Licence (as read)                                                         |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Zephyr (`west build`) | always written: `cmake/modules/kernel.cmake` sets `CMAKE_EXPORT_COMPILE_COMMANDS TRUE CACHE BOOL ... FORCE` "unconditionally, as this is also useful for several IDEs"; output `build/compile_commands.json`                                                                                                                                               | `kernel.cmake` at `main`, last commit `34525bd9fa02` (2026-11-06); Zephyr tags feed newest `Zephyr 4.5.0`; `doc/develop/tools/vscode.rst` says to compile once, then point the extension at `zephyr/build/compile_commands.json` | Apache-2.0 (`LICENSE`)                                                    |
| Zephyr, west config   | `west config build.cmake-args -- -DCMAKE_EXPORT_COMPILE_COMMANDS=ON` is the documented example for a default extra CMake argument; it takes effect after a pristine build                                                                                                                                                                                  | `doc/develop/west/build-flash-debug.rst` at `main`                                                                                                                                                                               |                                                                           |
| ESP-IDF               | CMake writes `<project>/build/compile_commands.json`, "the default location for clangd"; the guide gives the settings below; `IDF_TOOLCHAIN=gcc` is the default                                                                                                                                                                                            | ESP-IDF "Using Clangd with IDF Applications" (`api-guides/tools/esp-clangd.html`, "latest", read 2026-11-23); ESP-IDF tags feed newest `v6.1.1`; `tools/clangd-config.yaml` at `master`                                          | Apache-2.0 (`LICENSE`)                                                    |
| Pico SDK              | no SDK documentation for clangd found; projects made by the Pico VS Code extension "should contain a `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)` line near the top" of `CMakeLists.txt` (maintainer reply in `raspberrypi/pico-vscode` issue 135, 2024-12-13); the file is written into `build/` at configure; "Clean CMake" deletes `build/` and reconfigures | issue 135; `pico-sdk` tags feed newest `2.3.1`; `pico-vscode` newest `v0.23.1`                                                                                                                                                   | pico-sdk `LICENSE.TXT`: BSD-3-Clause text; pico-vscode `LICENSE`: MPL-2.0 |
| STM32CubeMX CMake     | CubeMX generates `CMakeLists.txt` (tool-owned, "do not modify"), `gcc-arm-none-eabi.cmake` (toolchain file, user-editable), `CMakePresets.json` (user-editable); the VS Code extension configures with `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` (seen in an ST community log, not in ST's docs)                                                                | ST `stm32cubeide-vscode/latest` CMake page (read 2026-11-23)                                                                                                                                                                     | not read                                                                  |

- Source states (ESP-IDF guide, "Important" blocks, and `tools/clangd-config.yaml` at `master`): ESP-IDF ships a
  patched clangd ("ESP-Clangd") that adds `--custom-config-file=<yaml>`; the recommended file is exactly
  `CompileFlags:` with `BuiltinHeaders: QueryDriver` and `Remove: [-m*, -f*]`; the clangd argument is
  `--query-driver=**`; no filtering is needed when `IDF_TOOLCHAIN=clang`; for ULP coprocessor code a project
  `.clangd` fragment with `If: PathMatch: main/ulp/.*` sets a second `CompilationDatabase`
  (`build/esp-idf/main/ulp_main`). The guide's reason for `-m*, -f*`: "remove all code generation options that do
  not affect the AST". Inference: that reasoning is too broad for some flags (`-funsigned-char`, `-fshort-wchar`
  and `-ffreestanding` change the AST); prefer targeted removal when the tree relies on them.
- Source states (ESP-IDF guide): `--query-driver=**` allows any compiler named in the database to run. Inference:
  that is acceptable for a trusted checkout and a risk for an untrusted one, because clangd then runs whatever
  binary the database names.
- Source states (Zephyr, third-party): a Nordic engineer's `.clangd` gist (Zephyr SDK 0.15.0) sets
  `Compiler: <sdk>/arm-zephyr-eabi/bin/arm-zephyr-eabi-gcc` and removes `-fno-printf-return-value`,
  `-mfp16-format=*` and `-fno-reorder-functions`; a vendor blog (GoodByte, nRF Connect SDK 2.6.1, clangd 1.8.3 of
  the VS Code extension) passes `--compile-commands-dir=${workspaceFolder}/build` and
  `--query-driver=${env:ZEPHYR_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-*`, adds
  `-Wno-unknown-warning-option`, removes `-mfp16-format=ieee` and `-fno-reorder-functions`, and suppresses
  `drv_unknown_argument`. Both are community configurations, not Zephyr documentation.
- Source states (Zephyr docs): the clang static analysis page says the analyser needs a build with an LLVM
  toolchain and a `compile_commands.json`; Zephyr's docs describe clangd only through the VS Code pages.
  Building with the LLVM toolchain variant would give a clang-flavoured database (`ZEPHYR_TOOLCHAIN_VARIANT=llvm`
  is background knowledge; the LLVM toolchain page did not load, so it is unverified here).
- Source states (ST community, 2025): in the STM32Cube clangd extension, the generated `--query-driver` named only
  `arm-none-eabi-gcc`; for C++ files users needed both `arm-none-eabi-gcc` and `arm-none-eabi-g++`; another user
  saw `-mcpu=`, `-mfpu=`, `-mfloat-abi=` rejected "for target 'x86_64-pc-windows-msvc'" and fixed it by adding an
  explicit `--target` in `.clangd` (the text is cut; value not read). An ST employee said a fix was planned.
  These are forum posts (lower trust).

## Q3. Formatting through clangd

- Source states (clangd `features`): clangd "embeds clang-format" and "respects your project's `.clang-format` file";
  "Format-as-you-type is experimental and doesn't work well yet." Formatting only happens when the client asks
  (LSP document, range or on-type formatting; the initialize reply in issue 1200 lists
  `documentFormattingProvider`, `documentRangeFormattingProvider` and `documentOnTypeFormattingProvider`).
- Source states (clangd man page, `clangd-22`, Debian experimental): `--fallback-style=<string>`: "clang-format
  style to apply by default when no .clang-format file is found". There is no `.clangd` key for formatting; the
  `Style` block in `.clangd` covers include style, namespaces and header quoting only (config page).
- Source states (clang-format docs, `ClangFormat.html` read 2026-11-23): `--style=file` is the default and
  searches for `.clang-format` (or `_clang-format`) in the file's parent directories; with none found it uses
  `--fallback-style`, which "defaults to 'LLVM'"; `--fallback-style=none` skips formatting; `--style=file:<path>`
  names a file explicitly. Inference: clangd's own default for `--fallback-style` is not stated in the man page;
  background knowledge says it is `LLVM`. So a tree with no `.clang-format` gets LLVM style (2-space indent, 80
  columns) from clangd unless the client passes `--fallback-style=none`, which is the safe choice for an agent.
  Whether clangd accepts `none` is not documented (the clang-format flag does).
- Source states (clang-format style options): `DisableFormat: true` "disables formatting completely" and is
  honoured per `Language:` section in a `.clang-format`; `// clang-format off` and `// clang-format on` fence a
  region; `InheritParentConfig` lets a subdirectory file build on the parent's.
- Kernel: the tree has `.clang-format` ("Intended for clang-format >= 11"). Source states
  (`Documentation/dev-tools/clang-format.rst` at `master`): the file is the approximate kernel style, "since not
  all the kernel follows the same style" a subsystem may add its own `.clang-format` in a subfolder; use the tool
  to reformat blocks or review patches ("Make sure your working directory is clean!" before `clang-format -i`);
  and "you should probably refrain yourself from using" `// clang-format off` in kernel sources because other
  people may run other clang-format versions. Documented gaps: the page has a "Missing support" section for
  constructs common in kernel code. Inference: so reformatting a whole kernel file against `.clang-format` creates
  unrelated hunks; never format a whole file there.
- U-Boot: source states (`doc/develop/codingstyle.rst`, last commit `08183ba1af19`): the `.clang-format` was "copied
  directly from the Linux kernel"; usage: `clang-format -style=file -i <file>`; `git clang-format` "format only
  staged changes"; best practice "format only the blocks of code that have been modified rather than entire files";
  "If you need to format entire files, create a separate commit containing only formatting changes"; fence
  hand-aligned tables with `// clang-format off` and `// clang-format on`.
- `git clang-format`: source states (script header and docs; `git-clang-format` at `llvm-project` `main`,
  licence line "Apache-2.0 WITH LLVM-exception", needs Python 3.8 or later): with zero or one commit it runs
  clang-format "on all lines that differ between the working directory and `<commit>`, which defaults to HEAD";
  "Changes are only applied to the working directory, or in the stage/index"; examples: `git clang-format`
  (staged changes), `git clang-format HEAD~1` (last commit too), `git clang-format main` (whole branch);
  `--diff` prints a diff instead of applying (the script says `--diff` is required with two commits; the
  preview-only behaviour for one commit is background knowledge, confirm with `git clang-format -h`);
  git-config keys `clangFormat.binary`, `clangFormat.commit`, `clangFormat.extensions`, `clangFormat.style`; it
  formats only files with its default extension list (`c`, `h`, `cc`, `cpp`, `hpp`, ..., plus proto, java, js).
- Keeping format-on-save off. No clangd or kernel document states this; it is a client setting. Inference: clangd
  never reformats unless the client sends a formatting request, so for an agent that only uses navigation and
  diagnostics there is nothing to turn off; for a human's editor set the client's format-on-save and
  format-on-type options to off for the tree (VS Code: `editor.formatOnSave`, `editor.formatOnType`, scoped to the
  workspace; background knowledge, not read here). Yocto's `devtool ide-sdk` is a counter-example: it deliberately
  turns format-on-save on when the source has a `.clang-format`, so check the generated `.vscode/settings.json`
  in a Yocto workspace.
- Meson trap: `ninja -C builddir clang-format` reformats every C and C++ file when a `.clang-format` exists at the
  root (Meson `Code-formatting.md`, since 0.50.0).

## Q4. clang-tidy through clangd versus `clang-tidy -p build/`

| Aspect                               | Through clangd                                                                                                                                                                                   | Direct `clang-tidy -p build/`                                                                                                                                                                      |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Enable                               | `--clang-tidy` flag on clangd (the man page lists `--clang-tidy`; `--clang-tidy=0` disables it, troubleshooting page)                                                                            | run the tool; `-p <build-path>` reads the database; without `-p` it searches parent directories of the first input file (clang-tidy docs)                                                          |
| Checks and options                   | `.clang-tidy` files merged with `.clangd` `Diagnostics.ClangTidy` (`Add`, `Remove`, `CheckOptions`); clangd settings win; `Remove` beats `Add` (config page)                                     | `.clang-tidy` found per source file in its parent directories when `--config` is empty; `--checks=`, `--config-file=`, `--header-filter=`, `--extra-arg=`, `--extra-arg-before=` (clang-tidy docs) |
| Speed filter                         | `FastCheckFilter` defaults to `Strict`: only checks measured fast run; `Loose` and `None` widen it (config page)                                                                                 | all enabled checks run                                                                                                                                                                             |
| Static analyzer (`clang-analyzer-*`) | not supported: maintainer says clangd supports only "pure (matcher-based) clang-tidy checks, not those based on the clang static analyzer" (issue 1727, 2023-08-13; tracking issue 905, open)    | supported (`-checks=clang-analyzer-*` in the docs)                                                                                                                                                 |
| Some other checks                    | features page: "Not all checks work within clangd"; issue 1727 shows `misc-const-correctness` working on the command line and not in clangd (cause not stated by the maintainers in what I read) | full set                                                                                                                                                                                           |
| Scope                                | the file being edited, parsed with function bodies of included headers skipped (faq)                                                                                                             | every translation unit in the database; `run-clang-tidy.py -p=build/` runs them in parallel; `clang-tidy-diff.py` limits it to a diff                                                              |
| Output                               | LSP diagnostics with fix-its in the editor                                                                                                                                                       | text on stderr; `--export-fixes`, `--fix` apply changes                                                                                                                                            |
| Compile flags                        | the same `Add` and `Remove` and query-driver handling as clangd                                                                                                                                  | no query-driver; uses the database command as is, so GCC-only flags and cross-compiler include paths need `--extra-arg` or `--extra-arg-before`                                                    |

- Source states (clang-tidy docs): "it's easier to work with if you set up a compile command database";
  `-p <build-path>` "is used to read a compile command database ... (use `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`)";
  `run-clang-tidy.py -p=build/` and `clang-tidy-diff.py` exist; Bear is named as a database source.
- Source states (kernel `Makefile`): `make clang-tidy` and `make clang-analyzer` run
  `scripts/clang-tools/run-clang-tools.py` over `compile_commands.json` and print "requires CC=clang" when the
  kernel is not built with clang. So the kernel's own tidy path needs a clang build.
- Source states (clangd config): `ExperimentalCustomChecks` (query-based custom checks) run only with
  `FastCheckFilter` `Loose` or `None`.
- Inference: for an agent that needs the full check set or the analyzer, run `clang-tidy -p build/` or
  `run-clang-tidy.py -p=build/` from the shell, and use clangd only for what it supports. The two paths read the
  same `.clang-tidy`, so one file serves both.

## Q5. Known pitfalls in cross builds

| Pitfall                                                                                                                                         | Evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Database holds GCC-only flags that clang rejects (`Unknown argument` with code `drv_unknown_argument`; for warnings `-Wunknown-warning-option`) | clangd issue 662 (opened 2021-01-22, still open): a kernel module database made with Bear shows `-mno-fp-ret-in-387`, `-mpreferred-stack-boundary=3`, `-mskip-rax-setup`, `-mindirect-branch=thunk-extern`, `-fconserve-stack`; the posted fix is `CompileFlags: Add: -Wno-unknown-warning-option` with `Remove: [-m*, -f*]`; a maintainer replied to a first report that the config `Remove` and `Add` options are the intended remedy                                                                                             |
| That broad fix has a cost                                                                                                                       | same issue, a commenter (2024-04-06): it "ignores compiler flags which can change the semantics of the code", so the LSP can misread the code; their alternative is to build the kernel with clang, and another user found `make LLVM=1` still gave `-fconserve-stack` and `-mrecord-mcount` errors on a 6.8 kernel                                                                                                                                                                                                                 |
| A cross GCC kernel fails to index at all                                                                                                        | clangd issue 1200 (2022-07-03, closed): aarch64 GCC kernel, `--query-driver=/usr/bin/aarch64-linux-gnu-gcc` set; log shows "Ignored diagnostic. unknown target ABI 'lp64'" then "Indexing ... failed: Couldn't build compiler instance"; a maintainer read the first as fatal; the reporter's fix was `.clangd` with `CompileFlags: Remove: -mabi=lp64`. Lesson (inference): an unknown-argument error can be fatal for indexing, not only noise, so features that rely on the index (find references, call hierarchy) die silently |
| Wrong target guessed                                                                                                                            | ST community post (2025): `-mcpu=`, `-mfpu=`, `-mfloat-abi=` rejected "for target 'x86_64-pc-windows-msvc'"; workaround was an explicit `--target` in `.clangd` `Add`                                                                                                                                                                                                                                                                                                                                                               |
| System headers not found with a custom toolchain                                                                                                | clangd system-headers guide: "worst scenario ... common for custom toolchains targeting embedded devices"; options: explicit `--target`, `-isystem` plus `-nostdlibinc`, `--query-driver`; check with `clangd --check=<file>`                                                                                                                                                                                                                                                                                                       |
| Relative driver name                                                                                                                            | system-headers guide: use an absolute driver path in the database or put the driver directory on `$PATH`                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `--query-driver` glob does not match                                                                                                            | the flag is an allowlist matched against argv[0] of the database command; the guide says it should match the command emitted by the build system (troubleshooting)                                                                                                                                                                                                                                                                                                                                                                  |
| C++ missing when only the C driver is allowed                                                                                                   | ST community: both `arm-none-eabi-gcc` and `arm-none-eabi-g++` needed; GoodByte uses `arm-zephyr-eabi-*` for both                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Stdlib headers changed under clangd                                                                                                             | GoodByte blog: a new clangd version dropped `arm-zephyr-eabi/12.2.0/include/` from the list for an nRF SDK 2.6.1 project (one report; a regression claim I could not confirm elsewhere)                                                                                                                                                                                                                                                                                                                                             |
| `BuiltinHeaders: QueryDriver` with GCC                                                                                                          | config page: processing another compiler's builtin headers "could lead to ... false positive diagnostics"; ESP-IDF nevertheless recommends it for its Xtensa GCC toolchain                                                                                                                                                                                                                                                                                                                                                          |
| Mixed GCC and clang commands in one database                                                                                                    | LKML patch discussion for the kernel `clang-tidy` target (WebSearch summary only; not read at the source): rebuilding with GCC then clang without `make clean` leaves a mixed database. Inference: regenerate after changing compilers                                                                                                                                                                                                                                                                                              |
| Stale or partial kernel database                                                                                                                | script reads only `.cmd` files, so unbuilt files are missing (script source); clangd then guesses a command for them from a similar file (design/compile-commands)                                                                                                                                                                                                                                                                                                                                                                  |
| Database path not found                                                                                                                         | clangd searches only parents and `build/` subdirectories; any other directory needs `CompilationDatabase` or a symlink                                                                                                                                                                                                                                                                                                                                                                                                              |
| Headers outside the project directory                                                                                                           | faq: use `--compile-commands-dir`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Wrong source file chosen for a header                                                                                                           | faq and design/compile-commands: filename heuristic; `compdb` adds header entries                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Background index crash                                                                                                                          | troubleshooting: `--background-index=0`, or `-j=1 --log=verbose` to find the file                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `-Werror` in the database                                                                                                                       | the compile-commands design page shows `Remove: '-Werror'` as the example, so warnings do not become errors in the editor                                                                                                                                                                                                                                                                                                                                                                                                           |

## Recipe per tree

Common to every recipe. Use clangd 17 or later where possible (some config keys need newer clangd: the `Includes`
and `UnusedIncludes` keys are described as since clangd 17 on the config page). Pass these on the clangd command
line, because the allowlist and a few others have no `.clangd` key: `--query-driver=<glob>`,
`--compile-commands-dir=<dir>` when the database is not under `build/`, `--background-index` (explicit; default
not stated in the man page), and `--clang-tidy` only when wanted. Verify any setup with
`clangd --check=<file>`: the log must say "Compile command from CDB" and not "Generic fallback command".
Then fix `drv_unknown_argument` diagnostics by adding the flags to `CompileFlags: Remove`.

### Linux kernel

```text
# clang build (cleanest database), cross example
make LLVM=1 ARCH=arm64 O=build defconfig
make LLVM=1 ARCH=arm64 O=build -j"$(nproc)"
make LLVM=1 ARCH=arm64 O=build compile_commands.json   # target exists since v5.10

# GCC build
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- O=build defconfig
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- O=build -j"$(nproc)"
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- O=build compile_commands.json
```

The database lands in the output directory (inference: the make rule writes `$@` in the object tree), so with
`O=build` clangd finds `build/compile_commands.json` from the source root. Before v5.10 run
`scripts/gen_compile_commands.py -d <objdir>` by hand. For an external module:
`make -C <kernel-build> M=$PWD compile_commands.json` (the Makefile defines the target for `KBUILD_EXTMOD`).

`.clangd` for a GCC-built kernel (start here, then extend from `clangd --check` output):

```yaml
CompileFlags:
  Add: [-Wno-unknown-warning-option]
  Remove: [-mno-fp-ret-in-387, -mpreferred-stack-boundary=*, -mskip-rax-setup, -mindirect-branch=*, -mindirect-branch-register, -fconserve-stack, -fno-var-tracking-assignments, -mabi=lp64]
Diagnostics:
  Suppress: [drv_unknown_argument]
```

Flags are the ones named in clangd issues 662 and 1200 (x86 and arm64). The broad `[-m*, -f*]` form works but
removes semantic flags. Do not format the tree: no `.clang-format` change, no `--fallback-style` needed because the
kernel has a `.clang-format`; never run whole-file format. Command line:
`clangd --background-index --compile-commands-dir=build --query-driver=/usr/bin/aarch64-linux-gnu-*`.

### U-Boot

```text
make CROSS_COMPILE=aarch64-linux-gnu- <board>_defconfig
make CROSS_COMPILE=aarch64-linux-gnu- -j"$(nproc)"
./scripts/gen_compile_commands.py            # needs a release from v2024.01; no make target
```

The script writes `compile_commands.json` in the current directory (the repository root), which clangd finds as a
parent directory; the root `.gitignore` already ignores it. For an `O=` build pass `-d <builddir>` (inference, from
the script options; the doc shows only the in-tree case). Before v2024.01 copy the kernel's script (inference).
Use the same `.clangd` approach as the kernel for GCC flags. Formatting: the tree has the kernel's `.clang-format`;
format only changed lines with `git clang-format`.

### Yocto recipe (CMake or Meson)

```text
devtool modify <recipe>
devtool build <recipe>                       # CMake recipes write compile_commands.json into B
# 5.0 or later, VS Code users: devtool ide-sdk <recipe> <image>
bitbake -e <recipe> | grep '^B='             # background knowledge: find B
```

```yaml
# <workspace>/sources/<recipe>/.clangd
CompileFlags:
  CompilationDatabase: /abs/path/to/B
```

Clangd flag: `--query-driver=<TMPDIR>/work/**/recipe-sysroot-native/usr/bin/**` (inference: the cross compiler sits
under `recipe-sysroot-native` per the tip docs; read argv[0] from the database and match it exactly). Kernel and
U-Boot recipes have no database support in OE-core: after a successful `bitbake`, run the in-tree
script or make target against `B` (inference), or use the Yocto-recommended path only for CMake and Meson recipes.
Standard SDK: `. /opt/poky/<ver>/environment-setup-<arch>-poky-linux`, then `bear -- make` or the recipe's own
CMake or Meson export; `CC` carries `--sysroot`, which clang accepts.

### Buildroot package

No documented method. Test-before-use sequence (inference): add `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` through
`<PKG>_CONF_OPTS` for a CMake package and run `make <pkg>-reconfigure`; the file appears in
`output/build/<pkg>-<ver>/buildroot-build/`. Otherwise run `bear -- make <pkg>-rebuild`. Clangd flag:
`--query-driver=<buildroot>/output/host/bin/*-gcc` (and `*-g++` for C++).

### CMake or Meson userspace project

```text
cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON [-DCMAKE_TOOLCHAIN_FILE=...]
meson setup build [--cross-file ...]
```

`build/` is on clangd's search path, so no `.clangd` is needed for a host build. For a cross GCC add
`--query-driver=/opt/toolchain/bin/*-g*`, and for a GCC database add the unknown-flag removals; Meson projects that
reject GCC flags can use a second clang build directory as libvirt does
(`CC=clang CXX=clang++ meson setup build-clang`, then `CompilationDatabase: build-clang`).

### MCU SDK project

```text
# Zephyr
west build -p auto -b <board> <app>          # always writes build/compile_commands.json
# ESP-IDF
idf.py set-target <chip> && idf.py reconfigure   # writes build/compile_commands.json
# Pico SDK and STM32CubeMX CMake
cmake -S . -B build -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_TOOLCHAIN_FILE=<toolchain file>
```

Clangd flags: `--compile-commands-dir=build --query-driver=<toolchain>/bin/arm-none-eabi-*` (Zephyr SDK:
`$ZEPHYR_SDK_INSTALL_DIR/arm-zephyr-eabi/bin/arm-zephyr-eabi-*`; ESP-IDF: `--query-driver=**` as its guide states).
`.clangd`: ESP-IDF's file as shipped (`BuiltinHeaders: QueryDriver`, `Remove: [-m*, -f*]`); for Zephyr start from
`Add: -Wno-unknown-warning-option`, `Remove: [-mfp16-format=*, -fno-reorder-functions, -fno-printf-return-value]`,
`Diagnostics: Suppress: [drv_unknown_argument]`. Allow both the `gcc` and the `g++` driver when the project has C++
files. ESP-IDF has a patched clangd (`esp-clangd`) for Xtensa targets (the guide calls it "lightly patched"); stock
clangd has no Xtensa backend (background knowledge, not read).

## What I could not verify

- clangd flag defaults not printed in the man page: `--background-index` and `--enable-config` defaults, the
  default of `--fallback-style` (assumed `LLVM`), and whether `--fallback-style=none` is accepted by clangd.
- Whether `--query-driver` globs are matched against argv[0] before or after clangd makes a bare compiler name
  absolute through `$PATH`; the design page lists both behaviours but not their order.
- Which Yocto release added the clangd integration in `devtool ide-sdk` (read only in the "6.1-tip" docs; the
  5.0.7 SDK page has no clangd text) and whether `B` equals `${WORKDIR}/build` under `devtool modify`.
- Any Buildroot documentation for clangd: none found in the 2026.08 manual; the Buildroot recipe is untested
  inference.
- The Meson database default from Meson's own manual: I only found it in the libvirt page and a Meson issue.
- The Zephyr LLVM toolchain page, the Pico SDK's own guidance, and any ST document that names clangd flags:
  not reachable or not found; Pico and STM32 rely on a maintainer reply and forum posts.
- Why `make compile_commands.json` should have a kernel-doc entry: `Documentation/kbuild/llvm.rst` does not
  mention it, and gh_grep found no `compile_commands.json` text under `Documentation/`; a zero from gh_grep is not
  proof, but I did not read other kernel docs (for example `kbuild.rst`) in full.
- The LKML claim about mixed GCC and clang databases, and the GoodByte clangd 1.8.3 regression: read only through
  a search summary or one blog.
- Licence of OE-core, the Yocto docs, CubeMX and ST docs, and the Zephyr LLVM page: not read. Licences read from
  files: kernel `COPYING` (GPL-2.0 WITH Linux-syscall-note), U-Boot `Licenses/README` (GPL-2.0), LLVM `LICENSE.TXT`
  (Apache-2.0 with LLVM Exceptions), Bear and compiledb (GPL-3.0), compdb (MIT), CMake (BSD text), Meson,
  Zephyr and ESP-IDF (Apache-2.0), Buildroot (GPL-2.0 or later), pico-sdk (BSD-3-Clause text), pico-vscode
  (MPL-2.0).
- clangd, `.clangd` and every command in the recipes were not run: clangd is not installed here and the lane
  forbids installing it.
