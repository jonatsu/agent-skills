# Buildroot — Advanced Topics

`BR2_EXTERNAL` trees, external toolchains and the wrapper, out-of-tree CMake and Meson against the staging sysroot,
`pkg-config` sysroot, SDK generation and `environment-setup`, `make legal-info`, reproducible builds, dependency graphs,
out-of-tree `O=` builds, and ccache.

For package `.mk`/`Config.in` authoring, see `buildroot-packages.md`. For board files, overlays, and `genimage`, see
`buildroot-board-support.md`.

## Contents

- [BR2_EXTERNAL](#br2_external)
- [External Toolchain](#external-toolchain)
- [CMake and Meson Against the Staging Sysroot](#cmake-and-meson-against-the-staging-sysroot)
- [SDK Generation](#sdk-generation)
- [Legal-Info (License Compliance)](#legal-info-license-compliance)
- [Reproducible Builds](#reproducible-builds)
- [Dependency Graphs](#dependency-graphs)
- [Out-of-Tree Builds](#out-of-tree-builds)
- [ccache Integration](#ccache-integration)

## BR2_EXTERNAL

`BR2_EXTERNAL` keeps board- and project-specific files out of the Buildroot tree. You can compose several external trees
at once.

### Required directory structure

```
my-br2-external/
├── external.desc           # mandatory: name and description
├── Config.in               # mandatory: top-level Kconfig (sources package Config.in files)
├── external.mk             # mandatory: includes package .mk files
├── configs/                # board defconfigs (appear in make list-defconfigs)
├── package/                # custom packages
│   └── mypkg/
│       ├── Config.in
│       └── mypkg.mk
├── board/                  # board files (overlays, scripts, genimage configs)
│   └── mycompany/myboard/
└── provides/               # optional: extend selectable providers
```

### `external.desc`

```
name: MYPROJECT
desc: My Project BSP and Application Packages
```

- `name` is mandatory and may contain only `[A-Za-z0-9_]`.
- Buildroot exposes `BR2_EXTERNAL_MYPROJECT_PATH` and `BR2_EXTERNAL_MYPROJECT_DESC`.

### `Config.in`

```kconfig
# my-br2-external/Config.in
source "$BR2_EXTERNAL_MYPROJECT_PATH/package/mypkg/Config.in"
source "$BR2_EXTERNAL_MYPROJECT_PATH/package/anotherpkg/Config.in"
```

### `external.mk`

```makefile
# my-br2-external/external.mk
include $(sort $(wildcard $(BR2_EXTERNAL_MYPROJECT_PATH)/package/*/*.mk))
```

### Using BR2_EXTERNAL

```bash
# Single external tree
make BR2_EXTERNAL=/absolute/path/to/my-br2-external menuconfig

# Multiple trees (space-separated, always absolute paths)
make BR2_EXTERNAL="/path/to/bsp-tree /path/to/app-tree" menuconfig
```

Buildroot records `BR2_EXTERNAL` in `output/.br2-external.mk`, so later `make` calls in the same output directory do not
need to repeat it. That file is generated — you MUST NOT hand-edit it.

### `provides/` (optional)

Lets the external tree add selectable providers for `toolchain`, `jpeg`, `openssl`, `skeleton`, and `init`.

## External Toolchain

### Why use one

- Skips rebuilding the toolchain on every `make distclean`.
- Lets you use a pre-validated toolchain from Bootlin, Linaro, or your own crosstool-NG build.

A Yocto or OpenEmbedded SDK does NOT work as a Buildroot external toolchain. Buildroot expects a bare cross toolchain —
compiler, binutils, C/C++ runtime, and a sysroot that Buildroot itself fills as it builds packages. An OE/Yocto SDK
instead ships a sysroot already loaded with hundreds of prebuilt libraries, so Buildroot cannot adopt it without
colliding with the very packages it is supposed to build. The host distribution's own gcc/binutils are unusable for the
same reason. Generate a toolchain with crosstool-NG or Buildroot instead.

### Configuring in menuconfig

```
Toolchain → Toolchain type → External toolchain
Toolchain → Toolchain → Custom toolchain
Toolchain → Toolchain path → /path/to/toolchain
Toolchain → External toolchain prefix → arm-linux-gnueabihf
Toolchain → External toolchain C library → glibc
```

Buildroot checks the features you declare (threads, C++, RPC, wide-char, and so on) against what the toolchain binary
actually provides, and errors at configure time on a mismatch. In particular the declared libc MUST match the
toolchain's: a glibc external toolchain cannot back a musl or uClibc target.

### Toolchain wrapper debugging

Buildroot fronts the external toolchain with a small wrapper that injects the sysroot and target flags. To see what it
forwards, set `BR2_DEBUG_WRAPPER` before the build: `1` prints the whole invocation on one line, `2` breaks each
argument onto its own line, and `0` (or leaving it unset) prints nothing.

```bash
export BR2_DEBUG_WRAPPER=2
make <pkg>-rebuild
```

### Pre-built toolchain sources

| Source             | URL                                   |
| ------------------ | ------------------------------------- |
| Bootlin toolchains | <https://toolchains.bootlin.com/>     |
| Arm GNU toolchains | <https://developer.arm.com/downloads> |
| crosstool-NG       | <https://crosstool-ng.github.io/>     |

## CMake and Meson Against the Staging Sysroot

Build an out-of-tree project against Buildroot's staging sysroot using the toolchain files Buildroot generates. Those
files are generated — do NOT edit them; your changes are overwritten on the next build.

### CMake (toolchain file)

```bash
cmake \
    -DCMAKE_TOOLCHAIN_FILE=/path/to/buildroot/output/host/share/buildroot/toolchainfile.cmake \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -B build_br -S .
cmake --build build_br
make DESTDIR=/path/to/buildroot/output/staging install -C build_br
```

### Meson (cross file)

```bash
meson setup \
    --cross-file /path/to/buildroot/output/host/etc/meson/cross-compilation.conf \
    --prefix /usr \
    build_br .
ninja -C build_br
DESTDIR=/path/to/buildroot/output/staging ninja -C build_br install
```

### pkg-config sysroot

Calling `pkg-config` outside Buildroot needs the sysroot set explicitly:

```bash
export PKG_CONFIG_LIBDIR=/path/to/buildroot/output/staging/usr/lib/pkgconfig
export PKG_CONFIG_SYSROOT_DIR=/path/to/buildroot/output/staging
pkg-config --cflags --libs openssl
```

Without `PKG_CONFIG_SYSROOT_DIR`, the flags carry host paths (`-L/usr/lib`) that point at the wrong sysroot.

## SDK Generation

### Export the host toolchain as an SDK tarball

```bash
make sdk
# Output: output/images/<tuple>_sdk-buildroot.tar.gz
```

After extracting the tarball on another machine, the recipient MUST run the `relocate-sdk.sh` script at the SDK's top
directory so paths point at the new location.

### Prepare the SDK layout without a tarball

```bash
make prepare-sdk
# output/host/ now holds the complete SDK
```

### `environment-setup` script

Enable `BR2_PACKAGE_HOST_ENVIRONMENT_SETUP` to install an `output/host/environment-setup` script into the SDK:

```
Host utilities → host-environment-setup
# or in defconfig: BR2_PACKAGE_HOST_ENVIRONMENT_SETUP=y
```

Source it to point a shell at the Buildroot toolchain:

```bash
source output/host/environment-setup
```

It puts the SDK binaries on `PATH`, defines the standard autotools variables (`CC`, `CXX`, `CFLAGS`, `LDFLAGS`,
`PKG_CONFIG_*`, ...), and sets `CONFIGURE_FLAGS` for cross-configuring autotools projects. Note the trade-off: once
sourced, the shell is wired for cross-compilation ONLY — native builds in that same shell will break, so open a fresh
shell when you need to compile for the host again.

## Legal-Info (License Compliance)

```bash
make legal-info
```

Output under `output/legal-info/`:

```
legal-info/
├── README                  # warnings and gaps in the manifest
├── buildroot.config        # the .config used for this build
├── host-licenses/          # host tool license texts
├── licenses/               # target package license texts
├── host-manifest.csv       # host package name + version + license
└── target-manifest.csv     # target package name + version + license
```

Limits you MUST account for before treating this as a compliance deliverable:

- The manifest is only as complete as the `.mk` metadata behind it. A package missing `<PKG>_LICENSE` or
  `<PKG>_LICENSE_FILES` produces gaps, flagged in the `README`.
- Some material is not collected automatically — notably an external toolchain's source and Buildroot itself — so the
  output is a starting point, not the whole obligation.
- Review it by hand against each package's actual license terms before shipping.

## Reproducible Builds

```bash
# Build options → Enable reproducible builds
BR2_REPRODUCIBLE=y
```

The goal is a byte-for-byte identical image across rebuilds of the same configuration, even after a `make clean`. One
practical constraint to plan around: the absolute output path MUST keep the same character length between the builds you
compare. Build paths can leak into artifacts, and a path of a different length shifts those bytes and defeats the
comparison — so build the runs you intend to match under equal-length directories.

## Dependency Graphs

```bash
# Full dependency graph (needs host graphviz; matplotlib for build-time graphs)
make graph-depends

# Per-package graph
make <pkg>-graph-depends

# Output format (default: pdf)
BR2_GRAPH_OUT=svg make graph-depends

# Trim depth and drop transitive edges for a readable graph
BR2_GRAPH_DEPS_OPTS='-d 3 --no-transitive' make graph-depends
```

Graphs land in `output/graphs/graph-depends.<format>`.

## Out-of-Tree Builds

Build into a separate directory to keep the source clean and drive several configurations from one source tree:

```bash
# First run from the Buildroot source directory
make O=../my-board-output menuconfig

# Buildroot writes a wrapper Makefile into O=, so afterwards:
cd ../my-board-output
make menuconfig
make
```

Multiple boards from one source tree:

```bash
make O=../output-board-a BR2_EXTERNAL=/path/to/ext board_a_defconfig && make -C ../output-board-a
make O=../output-board-b BR2_EXTERNAL=/path/to/ext board_b_defconfig && make -C ../output-board-b
```

## ccache Integration

```bash
# Build options → Enable compiler cache → ccache
BR2_CCACHE=y
BR2_CCACHE_DIR="/mnt/shared/br-ccache"   # optional: share across machines
```

Alternatively wrap the compiler with ccache from outside Buildroot:

```bash
export CROSS_COMPILE="ccache arm-linux-gnueabihf-"
```
