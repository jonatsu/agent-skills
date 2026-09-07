# Cross-Compilation for Embedded Linux

## Contents

- [Toolchain Types](#toolchain-types)
- [Using a Yocto SDK Toolchain](#using-a-yocto-sdk-toolchain)
- [Autotools Cross-Compilation Patterns](#autotools-cross-compilation-patterns)
- [Manual Toolchain (without SDK)](#manual-toolchain-without-sdk)
- [Diagnosing ABI / Library Mismatch on Target](#diagnosing-abi--library-mismatch-on-target)
- [CMake Cross-Compilation](#cmake-cross-compilation)
- [Deploying Binaries to Target](#deploying-binaries-to-target)
- [pkg-config Sysroot](#pkg-config-sysroot)
- [ccache with Cross-Compilers](#ccache-with-cross-compilers)
- [Static Linking and libc Licensing](#static-linking-and-libc-licensing)

For Buildroot's own toolchain, SDK, and package build commands, see **buildroot-development**.

## Toolchain Types

| Type                     | Format                    | Use case                  |
| ------------------------ | ------------------------- | ------------------------- |
| Bare-metal               | `arm-none-eabi-gcc`       | MCU firmware, no OS       |
| Linux uClibc             | `arm-linux-uclibc-gcc`    | Minimal embedded rootfs   |
| Linux glibc (soft-float) | `arm-linux-gnueabi-gcc`   | ARMv5/v6, no FPU          |
| Linux glibc (hard-float) | `arm-linux-gnueabihf-gcc` | ARMv7 with FPU            |
| Linux glibc 64-bit ARM   | `aarch64-linux-gnu-gcc`   | ARM Cortex-A53/A72/A76    |
| Yocto SDK                | `aarch64-poky-linux-gcc`  | Yocto-built target rootfs |

**Always match the toolchain to the target C library version.** A binary built with a newer glibc fails on the target
with `version GLIBC_2.XX not found` if the target runs an older glibc. The Yocto SDK toolchain guarantees ABI
compatibility.

## Using a Yocto SDK Toolchain

```bash
# Install the SDK (run the self-extracting installer)
./poky-glibc-x86_64-core-image-minimal-aarch64-toolchain-4.3.sh
# Default install path: /opt/poky/4.3/

# Source the environment (do this in every new shell)
source /opt/poky/4.3/environment-setup-cortexa53-poky-linux

# Verify the toolchain
echo $CC                          # should print the full aarch64 cross-compiler path
${CC} --version

# Build a project using the SDK environment
./configure --host=aarch64-poky-linux
make
```

Variables set by the SDK environment script:

| Variable                  | Purpose                               |
| ------------------------- | ------------------------------------- |
| `$CC`                     | Cross C compiler with target flags    |
| `$CXX`                    | Cross C++ compiler                    |
| `$CFLAGS`                 | Target-specific compiler flags        |
| `$LDFLAGS`                | Linker flags pointing to sysroot libs |
| `$PKG_CONFIG_SYSROOT_DIR` | sysroot for pkg-config                |
| `$SYSROOT`                | Path to target headers and libraries  |

## Autotools Cross-Compilation Patterns

Autotools distinguishes three system tuples:

- `--build` — the machine doing the compiling. Rarely needs changing; autotools detects it as the current machine.
- `--host` — the machine the built program will run on. Override this to cross-compile.
- `--target` — only relevant when the thing you are building is itself a compiler, where it names the machine that
  compiler will emit code for.

Set `--host` to the target tuple:

```bash
./configure --host=arm-linux-gnueabihf
```

`configure` then looks for cross tools whose names use that tuple as a prefix (for example `arm-linux-gnueabihf-gcc`).
When the tools are not named that way, point at them explicitly:

```bash
./configure CC=arm-linux-gcc
```

### `--prefix` vs `DESTDIR`

`--prefix` is where the program expects to find itself at runtime on the target. `DESTDIR` temporarily diverts the
*installation* into a staging directory without changing that runtime prefix.

```bash
# Runtime prefix is /usr (where the binary looks for its files on the target),
# but redirect `install` into a staging tree you later sync onto the rootfs.
./configure --prefix=/usr
make
make DESTDIR="$PWD/stage-rootfs" install    # files land under stage-rootfs/usr/...
```

### `config.log` and cache variables

`configure` records every test it runs in `config.log`. The end of the compiler tests section is usually where a
cross-build failure shows up, and the top of the file repeats the exact `./configure` line with all options and
environment variables. Cached test results appear there too, which matters when a stale cache hides a fixed problem —
delete `config.cache` if results look wrong.

### `autoreconf -i`, `config.guess`, and `config.sub`

Regenerate the autotools scaffolding and pull in missing helper scripts with:

```bash
autoreconf -i
```

Helper files such as `compile`, `config.guess`, `config.sub`, and `depcomp` land in the source tree's top directory by
default. Move them out of the way with `AC_CONFIG_AUX_DIR([build-aux])`. An out-of-date `config.sub`/`config.guess` is a
frequent cause of "cannot guess host type" on a new target tuple — `autoreconf -i` refreshes them.

## Manual Toolchain (without SDK)

```bash
export CROSS_COMPILE=aarch64-linux-gnu-
export ARCH=arm64

# Build the kernel
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- defconfig
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)

# Build a standalone binary
aarch64-linux-gnu-gcc -o myapp myapp.c

# Specify a sysroot for libraries from a rootfs
aarch64-linux-gnu-gcc --sysroot=/path/to/rootfs -o myapp myapp.c -lssl
```

## Diagnosing ABI / Library Mismatch on Target

**Before copying any binary to the target, check it:**

```bash
# Architecture and linkage
file mybinary
# Output examples:
# ELF 64-bit LSB executable, ARM aarch64  — correct for Cortex-A
# ELF 32-bit LSB executable, ARM, EABI5   — correct for 32-bit ARM
# ELF 64-bit LSB executable, x86-64       — wrong: host binary accidentally compiled

# Dynamic library dependencies
readelf -d mybinary | grep NEEDED
# Or:
aarch64-linux-gnu-readelf -d mybinary | grep NEEDED

# Verify the binary uses the expected interpreter (dynamic linker)
readelf -l mybinary | grep interpreter
# Should be: /lib/ld-linux-aarch64.so.1 (not /lib64/ld-linux-x86-64.so.2)
```

**On the target, if you get `not found` errors:**

```bash
# Which libraries are missing?
ldd mybinary 2>&1 | grep "not found"

# Where is the library the target has?
find /lib /usr/lib -name "libssl.so*" 2>/dev/null

# Is the RPATH pointing somewhere wrong?
readelf -d mybinary | grep RPATH
```

## CMake Cross-Compilation

Use a CMake toolchain file:

```cmake
# aarch64-poky-linux.cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

set(CMAKE_C_COMPILER   aarch64-poky-linux-gcc)
set(CMAKE_CXX_COMPILER aarch64-poky-linux-g++)

set(CMAKE_SYSROOT /opt/poky/4.3/sysroots/cortexa53-poky-linux)
set(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```

```bash
cmake -DCMAKE_TOOLCHAIN_FILE=aarch64-poky-linux.cmake \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -B build_aarch64 -S .
cmake --build build_aarch64
```

For Meson, use a cross file (`meson setup --cross-file <file> …`); a Yocto SDK and Buildroot both generate one for you
(Buildroot specifics live in **buildroot-development**).

## Deploying Binaries to Target

```bash
# SCP (most common)
scp mybinary root@192.168.1.100:/usr/local/bin/

# SSH + stdin (when SCP is unavailable)
cat mybinary | ssh root@192.168.1.100 "cat > /tmp/mybinary && chmod +x /tmp/mybinary"

# Via devtool (Yocto workflow — see yocto-openembedded-development)
devtool deploy-target myapp root@192.168.1.100

# Verify SHA-256 after copy
sha256sum mybinary
ssh root@192.168.1.100 sha256sum /tmp/mybinary
# Both should match
```

### The board pings but SSH stalls: two host NICs on one subnet

A lab host usually has the site LAN on one interface and a direct link to the board on another. When both land in the
same subnet the host can send from the wrong source interface, and the failure misleads: `ping <board>` succeeds while
`ssh` and every other TCP connection stall, the board cannot reach the host, and `arp -a` shows the board's address
against two interfaces or with a MAC that changes.

Pin the interface in the SSH config rather than chasing it per command:

```sshconfig
Host board
  HostName 192.168.1.100
  User root
  BindAddress 192.168.1.10        # host IP on the board-facing NIC
  StrictHostKeyChecking accept-new
```

Deploy through the alias afterwards (`scp mybinary board:/usr/local/bin/`). The successful `ping` is what makes this
expensive: it reads as proof the link is healthy, so the investigation starts one layer too high.

## pkg-config Sysroot

When cross-compiling, `pkg-config` defaults to host paths and emits `-L/usr/lib` pointing at the wrong sysroot.

```bash
# Fix: redirect pkg-config to the target sysroot
export PKG_CONFIG_LIBDIR=/path/to/sysroot/usr/lib/pkgconfig
export PKG_CONFIG_SYSROOT_DIR=/path/to/sysroot
pkg-config --cflags --libs openssl

# With a Yocto SDK (already set by the environment-setup script)
source /opt/poky/4.3/environment-setup-cortexa53-poky-linux
pkg-config --cflags --libs openssl   # uses $PKG_CONFIG_SYSROOT_DIR automatically
```

`PKG_CONFIG_LIBDIR` redirects the search path. `PKG_CONFIG_SYSROOT_DIR` rewrites the paths in the output
(`-L${sysroot}/usr/lib` instead of `-L/usr/lib`). Both must be set for a correct cross-compile.

## ccache with Cross-Compilers

Speed up repeated cross builds:

```bash
export CROSS_COMPILE="ccache aarch64-linux-gnu-"
make -j$(nproc)
```

Or enable it via the build system (`BR2_CCACHE=y` in Buildroot, `INHERIT += "ccache"` in Yocto).

## Static Linking and libc Licensing

When library ABI mismatches are blocking you and you need a fast path:

```bash
# Link everything statically (larger binary, no runtime deps)
aarch64-linux-gnu-gcc -static -o myapp myapp.c

# Verify no dynamic deps
ldd myapp
# Expected: "not a dynamic executable"
```

Use static linking as a diagnostic step or for simple utilities.

**LGPL licensing caveat:** glibc and uClibc are LGPL, which requires that end users be able to relink against a modified
library. A fully static binary built against glibc or uClibc creates a distribution obligation to provide the object
files (or a relink mechanism). Use **musl libc** for clean, obligation-free static binaries in production — musl's
static linking carries no LGPL relink requirement (select the musl toolchain in your build system).
