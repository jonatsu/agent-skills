# Buildroot Package Infrastructure

Package macros, `Config.in` wiring, the `.mk` variables that matter, fetch methods, staging vs target install, rebuild
commands, and package-failure triage.

For `BR2_EXTERNAL` layout and where custom packages live, see `buildroot-advanced.md`. For a symbol that will not appear
or a `select` that warns, see `kconfig-troubleshooting.md`.

## Contents

- [Package Infrastructure Types](#package-infrastructure-types)
- [`Config.in` Structure](#configin-structure)
- [Key Package Variables](#key-package-variables)
- [Fetch Methods](#fetch-methods)
- [Package Rebuild Commands](#package-rebuild-commands)
- [Host Package Dependencies](#host-package-dependencies)
- [Build Order vs Runtime Presence (there is no RDEPENDS)](#build-order-vs-runtime-presence-there-is-no-rdepends)
- [Debugging Package Failures](#debugging-package-failures)

## Package Infrastructure Types

Each package picks one macro. The macro decides how the configure, build, and install steps run; you MUST match it to
the upstream build system.

### `generic-package` / `host-generic-package`

Fully manual — you write every step. Use it only when no higher-level macro fits.

```makefile
# package/mypkg/mypkg.mk
MYPKG_VERSION = 1.2.3
MYPKG_SOURCE = mypkg-$(MYPKG_VERSION).tar.gz
MYPKG_SITE = https://example.com/releases
MYPKG_LICENSE = MIT
MYPKG_LICENSE_FILES = LICENSE

MYPKG_DEPENDENCIES = libfoo libbar

define MYPKG_BUILD_CMDS
    $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D)
endef

define MYPKG_INSTALL_TARGET_CMDS
    $(INSTALL) -D -m 0755 $(@D)/mypkg $(TARGET_DIR)/usr/bin/mypkg
endef

$(eval $(generic-package))
```

Do NOT set `MYPKG_SITE_METHOD` here: an `https://` site auto-selects the `wget` backend. Set the method explicitly only
to override that inference (see *Fetch Methods*).

### `autotools-package`

For packages driven by `./configure && make && make install`.

```makefile
MYPKG_VERSION = 1.0
MYPKG_SOURCE = mypkg-$(MYPKG_VERSION).tar.gz
MYPKG_SITE = https://example.com/releases
MYPKG_LICENSE = GPL-2.0+
MYPKG_LICENSE_FILES = COPYING

MYPKG_CONF_OPTS = --disable-tests --with-feature=yes

$(eval $(autotools-package))
```

The macro runs `autoreconf` when needed and sets `--host`, `--build`, `--prefix`, and `DESTDIR` for you.

### `cmake-package`

For CMake projects.

```makefile
MYPKG_VERSION = 2.0.0
MYPKG_SOURCE = mypkg-$(MYPKG_VERSION).tar.gz
MYPKG_SITE = https://github.com/org/mypkg/releases/download/v$(MYPKG_VERSION)
MYPKG_LICENSE = Apache-2.0
MYPKG_LICENSE_FILES = LICENSE

MYPKG_CONF_OPTS = -DENABLE_TESTS=OFF -DBUILD_SHARED_LIBS=ON

$(eval $(cmake-package))
```

Buildroot injects `-DCMAKE_TOOLCHAIN_FILE=...` itself. You MUST NOT set it by hand.

### `meson-package`

For Meson projects.

```makefile
MYPKG_VERSION = 0.5.0
MYPKG_SOURCE = mypkg-$(MYPKG_VERSION).tar.gz
MYPKG_SITE = https://example.com/releases
MYPKG_LICENSE = LGPL-2.1+
MYPKG_LICENSE_FILES = COPYING.LESSER

MYPKG_CONF_OPTS = -Dtests=disabled

$(eval $(meson-package))
```

Buildroot supplies the Meson cross file automatically.

### `python-package`

For Python packages. Declare the build backend with `SETUP_TYPE`.

```makefile
MYPKG_VERSION = 1.0.0
MYPKG_SOURCE = mypkg-$(MYPKG_VERSION).tar.gz
MYPKG_SITE = https://pypi.org/packages/source/m/mypkg
MYPKG_LICENSE = MIT
MYPKG_LICENSE_FILES = LICENSE
MYPKG_SETUP_TYPE = setuptools  # or: pep517, flit, poetry, hatchling

$(eval $(python-package))
```

The accepted `SETUP_TYPE` values grow across releases — confirm the one you want exists in your Buildroot version before
relying on it.

### `kernel-module`

For out-of-tree kernel modules. Combine it with a base package macro.

```makefile
MYMOD_VERSION = 1.0
MYMOD_SOURCE = mymod-$(MYMOD_VERSION).tar.gz
MYMOD_SITE = https://example.com
MYMOD_LICENSE = GPL-2.0

$(eval $(kernel-module))
$(eval $(generic-package))
```

`kernel-module` adds a `make` invocation with `KERNELDIR` pointed at the kernel source Buildroot built.

### `host-*` variants

Every macro has a `host-*` sibling (`host-generic-package`, `host-cmake-package`, ...) for tools that must run on the
build machine:

```makefile
$(eval $(host-autotools-package))
```

## `Config.in` Structure

Every package needs a `Config.in` beside its `.mk`:

```kconfig
# package/mypkg/Config.in
config BR2_PACKAGE_MYPKG
    bool "mypkg"
    depends on BR2_TOOLCHAIN_HAS_THREADS
    depends on BR2_PACKAGE_LIBFOO
    select BR2_PACKAGE_LIBBAR
    help
      Short description of what mypkg does.

      https://example.com/mypkg
```

- `depends on` — hides the option until the dependency is enabled.
- `select` — force-enables the named symbol, but does NOT check that symbol's own `depends on`. An unguarded `select` is
  the usual source of "unmet direct dependencies" warnings; see `kconfig-troubleshooting.md`.
- `BR2_TOOLCHAIN_HAS_THREADS` — the standard guard for anything needing POSIX threads.

Register the package in a parent `Config.in` (e.g. `package/Config.in`):

```kconfig
menu "My packages"
    source "package/mypkg/Config.in"
endmenu
```

Or source it from your `BR2_EXTERNAL` tree's `Config.in` (see `buildroot-advanced.md`).

## Key Package Variables

| Variable                    | Purpose                                                     |
| --------------------------- | ----------------------------------------------------------- |
| `<PKG>_VERSION`             | Version string (feeds the source filename)                  |
| `<PKG>_SOURCE`              | Source archive filename (set `= ""` for VCS fetches)        |
| `<PKG>_SITE`                | Base URL or VCS URL                                         |
| `<PKG>_SITE_METHOD`         | Override only — auto-detected from `<PKG>_SITE` (see below) |
| `<PKG>_GIT_SUBMODULES`      | `YES` to init submodules after clone                        |
| `<PKG>_LICENSE`             | SPDX identifier(s)                                          |
| `<PKG>_LICENSE_FILES`       | Path(s) to license text within the source                   |
| `<PKG>_DEPENDENCIES`        | Packages that MUST build first (build order)                |
| `<PKG>_CONF_OPTS`           | Extra options for configure/cmake/meson                     |
| `<PKG>_MAKE_OPTS`           | Extra options passed to `make` at build                     |
| `<PKG>_INSTALL_TARGET`      | `YES` (default) — install into `$(TARGET_DIR)`              |
| `<PKG>_INSTALL_STAGING`     | `YES` — install headers + `.so` into `$(STAGING_DIR)`       |
| `<PKG>_INSTALL_TARGET_CMDS` | Custom install recipe (`generic-package` only)              |

A library that other packages link against MUST set `<PKG>_INSTALL_STAGING = YES`, or its headers and shared objects
never reach `$(STAGING_DIR)` and downstream links fail.

## Fetch Methods

Buildroot infers the download backend from the site URL, so you rarely set `<PKG>_SITE_METHOD` at all. There is no
`https` method — an `http(s)://` or `ftp://` site uses the `wget` backend; a `git://` URL or one ending `.git` uses
`git`; a `file://` path uses `file`. Set the variable explicitly only to force a backend the URL does not imply, and
only to a real value: `wget`, `git`, `svn`, `hg`, `bzr`, `cvs`, `scp`, `file`, or `local`.

```makefile
# HTTPS tarball — method inferred as wget, do not set it
MYPKG_SITE = https://example.com/releases
MYPKG_SOURCE = mypkg-$(MYPKG_VERSION).tar.gz

# Git repository — method inferred from the URL, but pin an exact revision
MYPKG_SITE = https://github.com/org/mypkg.git
MYPKG_SITE_METHOD = git
MYPKG_VERSION = abc1234def567    # full commit SHA for reproducibility

# Local directory — must be forced; useful for in-development packages
MYPKG_SITE = $(TOPDIR)/../mypkg
MYPKG_SITE_METHOD = local
```

## Package Rebuild Commands

Buildroot stamps each build step, so a bare `make` skips a package that already built even after you edit its source or
`.mk`. You MUST force the step you changed.

```bash
# Re-run configure + build + install for one package
make <pkg>-rebuild

# Re-run install only (skip configure and build)
make <pkg>-reinstall

# Remove the package's build dir and stamps (next make re-fetches all steps)
make <pkg>-dirclean

# Rebuild the package, then regenerate the rootfs image
make <pkg>-rebuild all

# List every target a package exposes
make <pkg>-list-targets
```

A `-rebuild`/`-reinstall` updates `$(TARGET_DIR)` but not the packed image — follow it with `make` (or append `all`) to
regenerate the filesystem image.

## Host Package Dependencies

When a target package needs a host tool at build time, depend on its `host-` package so the host build runs first:

```makefile
MYPKG_DEPENDENCIES = host-mypkg-tool
```

Host packages install into `$(HOST_DIR)/bin/`, which is already on `PATH` during the build.

## Build Order vs Runtime Presence (there is no RDEPENDS)

Buildroot has NO runtime-dependency declaration. Unlike Yocto/OE (`RDEPENDS`) or Debian (`Depends`), there is no
variable that says "this package needs that one present at run time." Do NOT go looking for one.

`<PKG>_DEPENDENCIES` is a build-ORDER list and nothing more: it guarantees the listed packages finish building before
this package configures. It has no separate runtime meaning.

A library ends up on the target for one reason only: it is an enabled target package, and target packages install into
`$(TARGET_DIR)` by default. So the way to guarantee something is present at run time is to make sure it is enabled in
the configuration:

- Express the need in `Config.in` with `select BR2_PACKAGE_X` (or a matching `depends on`). Enabling your package then
  forces `X` on, and `X` installs itself to the target.
- Listing a runtime-only library in `<PKG>_DEPENDENCIES` also pulls it in, but only as a build-ordering side effect — it
  does not create a tracked runtime relationship, and it silently does nothing if the library is not also enabled in the
  config.

The reliable lever is always the configuration (`Config.in` `select`/`depends on`), never a runtime-deps variable.

## Debugging Package Failures

```bash
# Where the build ran and what it left behind
ls output/build/<pkg>-<ver>/           # look for config.log, CMakeFiles/
cat output/build/<pkg>-<ver>/config.log | tail -60   # autotools failures

# Reproduce the failure inside the exact build environment
make <pkg>-shell

# Package metadata (deps, version, license) as JSON
make <pkg>-show-info

# Resolve a variable's effective value (wildcards allowed)
make -s printvars VARS=MYPKG_SITE
make -s printvars VARS='MYPKG_*'
```
