# Buildroot — Advanced Topics

`BR2_EXTERNAL` trees, external toolchains and the wrapper, out-of-tree CMake and Meson against the staging sysroot,
`pkg-config` sysroot, SDK generation and `environment-setup`, `make legal-info`, reproducible builds, dependency graphs,
out-of-tree `O=` builds, and ccache.

For package `.mk`/`Config.in` authoring, see `buildroot-packages.md`. For board files, overlays, and `genimage`, see
`buildroot-board-support.md`.

Paths shown as `output/...` illustrate the default layout relative to the Buildroot source. For a custom `O=` build,
use the resolved `BASE_DIR`, `HOST_DIR`, `STAGING_DIR`, and `BINARIES_DIR`; do not append another `output` directory
inside the selected output. Run configuration/build commands in the established build context.

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
├── external.desc           # mandatory file: name required, description optional
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

# Multiple trees (space-separated; explicit absolute paths avoid cwd ambiguity)
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

Check the candidate against the release's external-toolchain requirements before configuring it. A general application
SDK or the host distribution's toolchain is not interchangeable with the external toolchain Buildroot expects.
Use a supported profile or a suitable purpose-built toolchain. The
[first-party toolchain documentation](https://github.com/buildroot/buildroot/blob/2026.08/docs/manual/configure.adoc)
explains the supported inputs, including the OE/Yocto SDK exclusion; verify a real candidate's libc and features.

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

When external compiler arguments are wrong, inspect the wrapper's actual invocation using `BR2_DEBUG_WRAPPER=2`.
In 2026.08, level 2 separates arguments by line, level 1 prints one line, and 0/unset disables the trace. Verify these
values in the release's toolchain-wrapper documentation when they differ from observed output.

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
DESTDIR=/path/to/buildroot/output/staging cmake --install build_br
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

For the exported SDK, follow its relocation instructions before compiling from a new installation path.
The generated `relocate-sdk.sh` at the extracted SDK root performs the path update.

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

Use a dedicated shell for the SDK environment. Inspect the script's exported compiler, flags, search paths, and
`CONFIGURE_FLAGS` rather than mixing them with a native build environment. Validate the resulting executable's target
architecture and library requirements. See the release's
[generated-toolchain guidance](https://github.com/buildroot/buildroot/blob/2026.08/docs/manual/using-buildroot-toolchain.adoc)
for SDK layout, relocation, and environment setup.

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
└── manifest.csv            # target package name + version + license
```

This is a partial layout; inspect the complete generated directory, including source archives and warnings.
Validate the evidence against the actual package inputs and metadata. Resolve missing notices or sources before using
it for a release, including inputs outside the normal package collection. The
[first-party legal-info documentation](https://github.com/buildroot/buildroot/blob/2026.08/docs/manual/legal-notice.adoc)
describes collection limits; a successful command is not a license-compliance verdict.

## Reproducible Builds

```bash
# Build options → Enable reproducible builds
BR2_REPRODUCIBLE=y
```

Treat reproducibility as a measured property of the selected inputs and outputs. Buildroot 2026.08 labels this option
experimental and documents a same-output-directory constraint in `Config.in`; equal-length paths alone are not the
documented guarantee. Keep source revisions, configuration, environment, and `SOURCE_DATE_EPOCH` fixed, then compare
the intended artifacts from independent clean builds. Report mismatches and investigate their source.
Do not put wall-clock timestamps in an in-image provenance file; keep volatile run metadata outside the image.

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

For builds outside Buildroot, use the project's supported compiler-launcher mechanism. Do not assume assigning a
command containing spaces to `CROSS_COMPILE` is supported by its build system.
