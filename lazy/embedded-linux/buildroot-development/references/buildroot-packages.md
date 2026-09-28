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
- [Local Source Iteration](#local-source-iteration)
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

The infrastructure supplies cross-build configuration and installation paths. Set `MYPKG_AUTORECONF = YES` when
the package needs its configure machinery regenerated; the default is `NO`, not automatic detection.

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
MYPKG_SETUP_TYPE = setuptools

$(eval $(python-package))
```

Check `package/pkg-python.mk` in the selected release for accepted `SETUP_TYPE` values. Buildroot 2026.08 names the
Hatch backend `hatch`, not `hatchling`; do not infer Buildroot's spelling from the Python module name.

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

`kernel-module` adds the kernel build dependency and module build/install hooks. For its module-directory and make-option
interfaces, consult `package/pkg-kernel-module.mk` and the release's kernel-module documentation.
Verify the resulting modules are paired with the kernel image actually selected at boot. Keep runtime module-load
diagnosis in `embedded-linux-bringup`.

### `host-*` variants

Use the infrastructure's supported `host-*` form for tools that run on the build machine, for example:

```makefile
$(eval $(host-autotools-package))
```

## `Config.in` Structure

A selectable target package needs a `Config.in` beside its `.mk`. Host-only build dependencies usually need no menu
entry; use the release's `Config.in.host` convention when exposing an optional host utility.

```kconfig
# package/mypkg/Config.in
config BR2_PACKAGE_MYPKG
    bool "mypkg"
    depends on BR2_TOOLCHAIN_HAS_THREADS
    select BR2_PACKAGE_LIBFOO
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

| Variable                    | Purpose                                                                      |
| --------------------------- | ---------------------------------------------------------------------------- |
| `<PKG>_VERSION`             | Version string (feeds the source filename)                                   |
| `<PKG>_SOURCE`              | Source archive filename; normally keep the generated default for VCS sources |
| `<PKG>_SITE`                | Base URL or VCS URL                                                          |
| `<PKG>_SITE_METHOD`         | Override only — auto-detected from `<PKG>_SITE` (see below)                  |
| `<PKG>_GIT_SUBMODULES`      | `YES` to init submodules after clone                                         |
| `<PKG>_LICENSE`             | SPDX identifier(s)                                                           |
| `<PKG>_LICENSE_FILES`       | Path(s) to license text within the source                                    |
| `<PKG>_DEPENDENCIES`        | Packages that MUST build first (build order)                                 |
| `<PKG>_CONF_OPTS`           | Extra options for configure/cmake/meson                                      |
| `<PKG>_MAKE_OPTS`           | Extra options passed to `make` at build                                      |
| `<PKG>_INSTALL_TARGET`      | `YES` (default) — install into `$(TARGET_DIR)`                               |
| `<PKG>_INSTALL_STAGING`     | `YES` — install headers + `.so` into `$(STAGING_DIR)`                        |
| `<PKG>_INSTALL_TARGET_CMDS` | Target install commands; infrastructure may provide a default                |

A library that other packages link against MUST set `<PKG>_INSTALL_STAGING = YES`, or its headers and shared objects
never reach `$(STAGING_DIR)` and downstream links fail.

## Fetch Methods

URL inference uses the scheme, not a `.git` suffix. For a Git repository accessed over HTTPS, explicitly set
`<PKG>_SITE_METHOD = git`. Keep the generated VCS source-archive name unless a verified need requires an override;
an empty or quoted-empty `_SOURCE` is not the way to request a VCS checkout.

Distinguish the effective method value from the download program: in 2026.08 an inferred `https` method is dispatched
to wget, while FTP is dispatched to curl. The manual's backend shorthand is not an exhaustive description of these
internal values. Check `package/pkg-download.mk`, `package/pkg-generic.mk`, and `support/download/dl-wrapper` when
diagnosing inference in the target release.

```makefile
# HTTPS tarball — infer the method from the URI; the wrapper chooses the backend
MYPKG_SITE = https://example.com/releases
MYPKG_SOURCE = mypkg-$(MYPKG_VERSION).tar.gz

# Git over HTTPS — select the method explicitly and pin the real full commit ID
MYPKG_SITE = https://github.com/org/mypkg.git
MYPKG_SITE_METHOD = git
MYPKG_VERSION = <full-commit-id>

# Local directory — must be forced; useful for in-development packages
MYPKG_SITE = /absolute/path/to/mypkg
MYPKG_SITE_METHOD = local
```

## Package Rebuild Commands

Buildroot stamps each build step, so a bare `make` skips a package that already built even after you edit its source or
`.mk`. You MUST force the step you changed.

| Change                                                                                        | Appropriate operation                                               |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Install commands only                                                                         | `<pkg>-reinstall`                                                   |
| Source edit in the active build tree or source override                                       | `<pkg>-rebuild`: compilation and installation                       |
| Configure options or configure inputs                                                         | `<pkg>-reconfigure`: configuration, compilation, and installation   |
| Extract/patch inputs or a need to recreate this package's build tree                          | Preserve local edits, then `<pkg>-dirclean` and rebuild the package |
| Package removed, architecture/toolchain changed, or affected dependents cannot be established | Fresh/full build; per-package uninstall is unsupported              |

`-dirclean` does not remove installed files or cached downloads. Recreating the build tree normally reuses cached source
archives; it does not necessarily download again. Rebuilding a dependency does not automatically rebuild every consumer.
Use the release's `make help` and package-target documentation for available operations.

A `-rebuild`/`-reinstall` updates `$(TARGET_DIR)` but not the packed image — follow it with `make` (or append `all`) to
regenerate the filesystem image.

## Local Source Iteration

For repeated development edits, keep sources in a developer-owned checkout. Set an override in the file selected by
`BR2_PACKAGE_OVERRIDE_FILE` (default: `local.mk` beside `BR2_CONFIG`):

```makefile
MYPKG_OVERRIDE_SRCDIR = /absolute/path/to/mypkg
```

Buildroot rsyncs the checkout into its temporary `<package>-custom` build tree. Normal download, extraction, and
patching are bypassed; do not assume patches configured for a release source were applied to the override.
Edit the checkout and use `make mypkg-rebuild all`, or `mypkg-reconfigure all` for configuration changes.
Before release, verify the pinned source and patch inputs without the development override. See the
[native development workflow](https://github.com/buildroot/buildroot/blob/2026.08/docs/manual/using-buildroot-development.adoc)
for rsync exclusions and version-specific details.

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

Target-package install steps normally populate `TARGET_DIR`; invoking a package as a Make dependency can run those
steps even without selecting its Kconfig symbol. This side effect is not a sound runtime dependency contract.
Keep configuration dependencies and build-order dependencies consistent:

- Select required libraries in `Config.in`, propagating their toolchain and other non-selectable constraints.
  `depends on` restricts availability; it does not enable the dependency.
- Add build dependencies to `<PKG>_DEPENDENCIES` as well. Their targets can run even without a matching selected Kconfig
  symbol, so this is not a substitute for correct configuration dependencies. Host tools and packages that disable target
  installation do not imply runtime presence.

The reliable lever is always the configuration (`Config.in` `select`/`depends on`), never a runtime-deps variable.

## Debugging Package Failures

```bash
# Resolve the actual build directory, including source-override and O= cases
make -s printvars VARS=MYPKG_DIR
# Substitute the returned path; config.log is an autotools example.
tail -n 60 -- /absolute/path/to/package-build/config.log

# Inspect the release's supported targets and actual build invocation
make help
make V=1 mypkg

# Package metadata (deps, version, license) as JSON
make mypkg-show-info

# Resolve a variable's effective value (wildcards allowed)
make -s printvars VARS=MYPKG_SITE
make -s printvars VARS='MYPKG_%'
```
