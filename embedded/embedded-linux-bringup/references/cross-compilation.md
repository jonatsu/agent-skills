# Cross-compilation and Target ABI

Use a development sysroot and toolchain that correspond to the target image and configuration.
A runtime rootfs may lack headers, linker files, and development libraries needed for compilation.
For package integration or SDK generation, use **buildroot-development** or **yocto-openembedded-development**.

## Identify the Toolchain Before Building

Record architecture, CPU/ISA tuning, ABI, libc, dynamic loader, and library versions.
A tuple is a useful hint, not proof of all these properties: `arm-none-eabi` commonly targets bare metal,
`arm-linux-gnueabi` and `arm-linux-gnueabihf` select different ARM calling conventions, and
`aarch64-linux-gnu` identifies a different architecture/ABI.
Do not infer the complete supported CPU feature set from the tuple alone.

For an SDK, use its supplied setup script in a dedicated shell and inspect its compiler command, flags, and sysroot.
Do not install or source an untrusted SDK merely to inspect its documentation.
Yocto 4.3's environment exports `SDKTARGETSYSROOT` and `OECORE_TARGET_SYSROOT`; `$SYSROOT` is not its generic contract.
Compiler variables may contain multiple flags, so quoting the entire `CC` string as one executable is also wrong.
Use the SDK's build integration and preserve its intentional argument expansion.

An SDK generated for another image, tune, libc, or set of libraries is not an ABI guarantee.
See [Yocto's SDK workflow](https://docs.yoctoproject.org/4.3/sdk-manual/working-projects.html) and inspect the actual
setup script rather than copying a dated `/opt/poky/VERSION` path.

## Autotools: Select the Execution Platform Explicitly

For an application, `--build` names the compilation machine and `--host` names the machine running the result.
`--target` applies to tools that themselves generate target code, such as a compiler.
Keep host selection even when explicitly selecting a differently named compiler:

```bash
# Standalone toolchain example; replace tuples and provide the intended sysroot/flags.
./configure --build=x86_64-pc-linux-gnu --host=aarch64-linux-gnu CC=aarch64-linux-gnu-gcc
```

With a Yocto SDK, preserve its supplied `CONFIGURE_FLAGS` and compiler flags instead of overwriting them with this
standalone example. Check `config.log` for the actual compiler, execution tests, and cross-compiling decision.
Do not replace `--host` with `CC=...` alone or fabricate cache answers to suppress a failed target execution test.
See [Autoconf's cross-compilation contract](https://www.gnu.org/software/autoconf/manual/autoconf-2.70/html_node/Hosts-and-Cross_002dCompilation.html).

`--prefix=/usr` describes the runtime installation prefix; `DESTDIR` stages installation elsewhere on the build host.

```bash
# After configuring with the correct cross environment and runtime prefix:
make
make DESTDIR="$PWD/stage-rootfs" install
```

Use a fresh build directory when changing toolchains or cached assumptions.
If generated Autotools files are absent, follow the project's bootstrap procedure.
`autoreconf -i` installs missing auxiliary files; it is not a universal promise to replace existing stale helper files.
Inspect the specific `config.sub`/`config.guess` failure and the project's supported regeneration procedure.

## CMake, Meson, and pkg-config

Prefer the SDK's supplied CMake toolchain integration when present. Find it through the SDK environment/documentation;
do not reconstruct the SDK from an assumed installation path and a bare compiler name.
For a standalone compiler, a minimal toolchain file can establish target lookup rules:

```cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)
set(CMAKE_SYSROOT /absolute/path/to/development-sysroot)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
```

Add the actual CPU/ABI flags and other project requirements. Configure into a separate build directory:

```bash
cmake -S . -B build-target -DCMAKE_TOOLCHAIN_FILE=target.cmake -DCMAKE_INSTALL_PREFIX=/usr
cmake --build build-target
```

For Meson, use a verified cross file with the intended compiler, host machine, and sysroot/pkg-config settings.
Use a generated SDK cross file when supplied; do not assume every SDK includes one.
See the native [CMake](https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html)
and [Meson](https://mesonbuild.com/Cross-compilation.html) references.

When target dependencies unexpectedly resolve to host libraries, inspect pkg-config's environment and selected `.pc`
files. `PKG_CONFIG_LIBDIR` replaces its default metadata directories; include the target's applicable lib, share,
and multiarch paths. `PKG_CONFIG_SYSROOT_DIR` adjusts emitted include/library paths.
Remove unintended host entries in `PKG_CONFIG_PATH`, which can override the desired lookup.
Do not assume arbitrary `.pc` variables receive the same sysroot rewriting.

## Inspect the Binary and Its Dependencies

Use host ELF inspection before attempting to run an unknown or incompatible binary:

```bash
file ./myapp
readelf -h ./myapp
readelf -l ./myapp
readelf -d ./myapp
readelf --version-info ./myapp
```

Check machine/class, target-specific ABI attributes when applicable, requested interpreter, NEEDED entries, RPATH/RUNPATH,
and required symbol versions. Inspect the target's actual libraries and loader against these requirements.
A newer build-host glibc does not invariably make a binary incompatible; the relevant question is what versions its
linked objects require and what the target supplies. Indirect dependencies also matter.

If execution says `not found` while the file exists, inspect its ELF interpreter or script shebang.
If a trusted target executable reports a missing library, use the target loader's diagnostic facilities or `ldd`
where appropriate. Do not use `ldd` on an untrusted executable as a supposedly passive host inspection.
Keep deployment path and checksum verification consistent; see [deploy-and-iterate.md](deploy-and-iterate.md).

## The Board Pings but SSH Stalls

Two host interfaces on the board's subnet are one possible cause, not a diagnosis from successful ping alone.
Check the route, source address, neighbor state, and a bounded TCP/SSH diagnostic first.
For an established source-address problem, an SSH alias can bind the intended local address:

```sshconfig
Host board
  HostName 192.0.2.10
  User developer
  BindAddress 192.0.2.1
  StrictHostKeyChecking accept-new
```

Substitute real lab addresses and follow the user's host-key policy.
`BindAddress` selects a source address; it does not repair every routing, firewall, or reverse-path-filter problem.
Keep persistent host network changes with the network configuration owner.

## Static Linking and Iteration

Static linking can isolate a dynamic-loader problem for a small utility when the toolchain and required libraries
support it. Confirm the result with ELF inspection, then test the behavior that matters on the target.
It does not solve wrong architecture, unsupported instructions, missing kernel interfaces, or all runtime dependencies.

musl's license avoids an LGPL relinking requirement for musl itself; it does not make the complete executable free of
distribution obligations. Review all linked libraries and required notices against their actual licenses.
See [musl's copyright and license record](https://git.musl-libc.org/cgit/musl/tree/COPYRIGHT?h=v1.2.5).
Do not change libc merely to hide an unexplained ABI failure.

For repeated builds, use the build system's supported ccache configuration and verify that it still selects the
intended compiler and flags. Keep kernel `ARCH`/`CROSS_COMPILE` work in its configured build context, and route
Buildroot/Yocto persistence and package rebuilding to their owning skills.
