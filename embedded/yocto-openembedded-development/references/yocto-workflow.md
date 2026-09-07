# Yocto / OpenEmbedded Workflow

Mechanics reference: the layer model, BitBake syntax and task lifecycle, recipe anatomy, `.bbappend` overrides, sstate
internals, and the build/inspect/debug commands. For where a setting *belongs* and release-engineering discipline, see
`yocto-best-practices.md`; for licensing and SBOM, `compliance-and-sbom.md`.

## Contents

- [Layer Model](#layer-model)
- [Build Environment Setup](#build-environment-setup)
- [`local.conf` Essentials](#localconf-essentials)
- [MACHINE and DISTRO Feature Variables](#machine-and-distro-feature-variables)
- [Package Groups](#package-groups)
- [BitBake Assignment Operators and Overrides](#bitbake-assignment-operators-and-overrides)
- [BitBake Task Lifecycle](#bitbake-task-lifecycle)
- [Task Dependency Varflags](#task-dependency-varflags)
- [Recipe Anatomy](#recipe-anatomy)
- [License, Fetch, and Version Fields](#license-fetch-and-version-fields)
- [Inline and Anonymous Python](#inline-and-anonymous-python)
- [`.bbappend` and `FILESEXTRAPATHS`](#bbappend-and-filesextrapaths)
- [sstate-cache Mechanics](#sstate-cache-mechanics)
- [devtool Workflow](#devtool-workflow)
- [SDK Generation](#sdk-generation)
- [Kernel Customization](#kernel-customization)
- [Build History](#build-history)
- [Offline / Air-Gapped Builds](#offline--air-gapped-builds)
- [Debugging a Task Failure](#debugging-a-task-failure)
- [Recipe Tooling: `recipetool`, `oe-pkgdata-util`](#recipe-tooling-recipetool-oe-pkgdata-util)

## Layer Model

A Yocto build is a stack of layers. Each layer is a directory:

```
meta-mylayer/
├── conf/
│   └── layer.conf           # required: BBFILES, BBFILE_COLLECTIONS,
│                            #           LAYERSERIES_COMPAT, LAYERDEPENDS
├── recipes-*/
│   └── <pkg>/
│       ├── <pkg>_<ver>.bb   # recipe
│       └── <pkg>_%.bbappend # override (% = version wildcard)
└── classes/                 # optional bbclass files
```

`bblayers.conf` lists the active layers:

```bash
# conf/bblayers.conf
BBLAYERS ?= " \
  /path/to/poky/meta \
  /path/to/poky/meta-poky \
  /path/to/meta-openembedded/meta-oe \
  /path/to/meta-mylayer \
"
```

Create and register a layer skeleton:

```bash
bitbake-layers create-layer meta-mylayer
bitbake-layers add-layer meta-mylayer
```

## Build Environment Setup

```bash
source oe-init-build-env build
```

This creates `build/conf/{local.conf,bblayers.conf}` and puts `bitbake` on the path. For a one-command "fetch layers,
configure, and build" wrapper driven by a single YAML config, use kas — that workflow lives in the
**kas-build-orchestration** skill. Plain `bitbake` after `oe-init-build-env` is fully sufficient; kas is optional.

## `local.conf` Essentials

```bash
MACHINE = "raspberrypi4-64"          # target hardware
DISTRO  = "poky"                     # distribution policy (see best-practices)
BB_NUMBER_THREADS = "8"              # BitBake task parallelism
PARALLEL_MAKE = "-j8"                # make parallelism inside a task
DL_DIR    = "/mnt/yocto-cache/downloads"      # shared download cache
SSTATE_DIR = "/mnt/yocto-cache/sstate-cache"  # shared state cache
IMAGE_INSTALL:append = " strace gdbserver"    # dev extras (release: use an image recipe)
EXTRA_IMAGE_FEATURES += "debug-tweaks tools-debug"
```

A change to `local.conf` reparses every recipe, so keep it to genuinely local, development-only settings. Everything
durable belongs in a distro, machine, or image recipe — see `yocto-best-practices.md`.

## MACHINE and DISTRO Feature Variables

```bash
MACHINE_FEATURES  = "usbgadget usbhost vfat"        # BSP/kernel feature flags
SERIAL_CONSOLES   = "115200;ttyAMA0"                # console port + baud
DISTRO_FEATURES   = "sysvinit ipv4 ipv6 wifi usbgadget"  # subsystems compiled in

# Machine-scoped override (worked example: BeagleBone)
IMAGE_INSTALL:beaglebone = "busybox mtd-utils i2c-tools"
IMAGE_INSTALL = "busybox mtd-utils"
# With MACHINE=beaglebone the i2c-tools line applies; otherwise it does not.
```

## Package Groups

| Package group                      | Contents                     |
| ---------------------------------- | ---------------------------- |
| `packagegroup-core-boot`           | minimal boot set             |
| `packagegroup-core-buildessential` | on-target build tools        |
| `packagegroup-core-tools-debug`    | `gdb`, `strace`, debug tools |
| `packagegroup-core-tools-profile`  | `perf`, profiling tools      |
| `packagegroup-core-nfs-client`     | NFS client                   |

## BitBake Assignment Operators and Overrides

| Operator    | Meaning                                                                      |
| ----------- | ---------------------------------------------------------------------------- |
| `=`         | lazy assignment (RHS expanded when used)                                     |
| `:=`        | immediate assignment (RHS expanded at parse time)                            |
| `?=`        | weak default — sets only if undefined; among several, the **first** wins     |
| `??=`       | weakest default — lower priority than `?=`; among several, the **last** wins |
| `+=` / `=+` | append / prepend with a space                                                |
| `.=` / `=.` | append / prepend without a space                                             |

`:append`, `:prepend`, and `:remove` (the `_append`/`_prepend`/`_remove` forms before Kirkstone) are applied at
variable-expansion time, after parsing — so their result is order-independent, unlike `+=`/`.=`. You control all spacing
yourself. Application order is `:append`, then `:prepend`, then `:remove`. In global config files (`local.conf`,
`site.conf`) prefer the override forms; `+=`/`.=` there depend on include order and are hard to reason about.

## BitBake Task Lifecycle

| Task           | Purpose                                  |
| -------------- | ---------------------------------------- |
| `do_fetch`     | download `SRC_URI`                       |
| `do_unpack`    | extract archives                         |
| `do_patch`     | apply `.patch` files from `SRC_URI`      |
| `do_configure` | autoconf / cmake / meson configure       |
| `do_compile`   | build                                    |
| `do_install`   | install into `${D}`                      |
| `do_package`   | split `${D}` into packages               |
| `do_rootfs`    | assemble the rootfs (image recipes only) |

```bash
bitbake -c compile -v <recipe>     # run one task, verbose
bitbake -c devshell <recipe>       # interactive shell in the recipe environment
cat ${WORKDIR}/temp/log.do_compile # task log (path printed on failure)
```

## Task Dependency Varflags

```bitbake
do_patch[depends]        = "quilt-native:do_populate_sysroot"
do_configure[deptask]    = "do_populate_sysroot"
do_package_qa[rdeptask]  = "do_packagedata"
do_rootfs[recrdeptask]  += "do_packagedata"
```

- `[depends]` — inter-task dependency on a specific target's task.
- `[deptask]` — task each `DEPENDS` item must finish first (`DEPENDS` = build-time).
- `[rdeptask]` — task each `RDEPENDS` item must finish first (`RDEPENDS` = runtime).
- `[recrdeptask]` — recursive form.

Forgetting `RDEPENDS` produces a clean build that fails at runtime with a missing library — there is no build-time
error.

## Recipe Anatomy

```bitbake
SUMMARY  = "My application"
HOMEPAGE = "https://github.com/org/myapp"
LICENSE  = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=abc123..."

SRC_URI = "git://github.com/org/myapp.git;protocol=https;branch=main"
SRCREV  = "abc123def456..."       # pin a commit; never floating HEAD in a release
S       = "${WORKDIR}/git"        # source dir after unpack (Git fetches)

inherit cmake                     # or autotools, meson, python3-poetry, ...

RDEPENDS:${PN} = "libssl"         # runtime deps
DEPENDS        = "openssl"        # build-time deps

do_install() {
    install -d ${D}${bindir}
    install -m 0755 myapp ${D}${bindir}/myapp
}
```

## License, Fetch, and Version Fields

- `LIC_FILES_CHKSUM` is mandatory unless `LICENSE = "CLOSED"`; it may reference a whole license file or a line range
  inside a source file. A mismatch fails `do_populate_lic`. (Compliance detail: `compliance-and-sbom.md`.)
- `SRC_URI[sha256sum]` guards a fetched archive against a tampered upstream server.
- `SRCREV` selects the commit for a Git fetch; set `S` to the unpacked directory.
- If the version cannot come from the filename, set `PV` (e.g. `PV = "3.8.0+git"`).

```bitbake
LIC_FILES_CHKSUM = "file://COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263 \
                    file://serpent.c;beginline=14;endline=36;md5=ca0d220bc413e18..."
SRC_URI = "http://downloads.example.org/${BP}.tar.xz"
SRC_URI[sha256sum] = "f2c1c76592a82ffff8413ba3c4a1299b6c7ab06c734dee03fd88630485c2b920"
```

## Inline and Anonymous Python

```bitbake
DATE = "${@time.strftime('%Y%m%d', time.gmtime())}"   # called at each expansion
FOO := "${@foo()}"                                     # called once at parse time
inherit ${@'featureclass' if condition else ''}

python () {                        # anonymous function: runs at end of parsing
    if d.getVar('SOMEVAR') == 'value':
        d.setVar('ANOTHERVAR', 'value2')
}
```

Inline `${@...}` runs when the variable expands (with `=`) or once at parse (`:=`). Anonymous Python runs after all
parsing; override operators like `:append` are applied *before* it runs.

## `.bbappend` and `FILESEXTRAPATHS`

Use a `.bbappend` to modify a recipe from another layer without forking it:

```bitbake
# meta-mylayer/recipes-kernel/linux/linux-yocto_%.bbappend
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI += "file://my-board-fix.patch \
            file://my-defconfig-fragment.cfg"
```

Two rules that cause silent failures when missed:

- **`FILESEXTRAPATHS:prepend` is required** to make BitBake search this layer's `files/` directory. Omit it and the
  added `file://` entries are not found — `do_fetch` fails with a "cannot find file" that points nowhere obvious.
- **The version glob must match.** `linux-yocto_6.6.bbappend` does not apply to `linux-yocto_6.10`. Use
  `linux-yocto_%.bbappend` to track any version.

## sstate-cache Mechanics

sstate (shared state) stores each completed task's output as a signed tarball, keyed by a hash of that task's inputs. On
rebuild BitBake reuses the cached result when the input hash is unchanged — the core of Yocto's incremental speed.
(Sharing sstate across machines and pruning it: `yocto-best-practices.md`.)

Stale sstate serving a wrong result usually traces to an input change BitBake could not see reflected in the hash of an
*already-cached* upper task:

- switched `MACHINE` without a clean;
- patched the kernel or a recipe but the depending task was already cached;
- pulled a new layer revision while old artifacts remain.

```bash
bitbake -c cleansstate <recipe>            # drop this recipe's sstate → forces rebuild
bitbake -c cleanall <recipe>               # cleansstate + remove its downloads
bitbake-dumpsig <sigfile>                  # inspect a task's signature inputs
bitbake-diffsigs <sig-a> <sig-b>           # why two signatures differ (what changed)
```

`cleansstate`/`cleanall` discard reusable work — gate them (see SKILL.md *Confirmation gates*) and prefer scoping to one
recipe.

## devtool Workflow

```bash
devtool add myapp https://github.com/org/myapp.git   # new recipe from source
devtool modify linux-yocto                            # bring a recipe into the workspace
devtool build myapp
devtool deploy-target myapp root@192.168.1.100        # push to a running target
devtool finish myapp meta-mylayer                     # write changes back as patches
devtool upgrade myapp                                 # bump to a new upstream version
```

Editable source lives at `workspace/sources/<recipe>/` and survives rebuilds.

## SDK Generation

```bash
bitbake core-image-minimal -c populate_sdk       # standard SDK (cross toolchain + sysroot)
bitbake core-image-minimal -c populate_sdk_ext   # extensible SDK (bundles devtool)
./tmp/deploy/sdk/poky-glibc-x86_64-*-toolchain-*.sh   # installer
source /opt/poky/<ver>/environment-setup-aarch64-poky-linux
```

After sourcing, `$CC`, `$CXX`, `$CFLAGS`, and the target `$SDKTARGETSYSROOT` point at the cross toolchain and sysroot.
Add packages with `TOOLCHAIN_TARGET_TASK:append` (target sysroot) and `TOOLCHAIN_HOST_TASK:append` (host `nativesdk-*`
tools). Cross-compilation *usage* is covered in **embedded-linux-bringup**.

## Kernel Customization

```bash
KERNEL_DEVICETREE = "ti/k3-am62-beagleplay.dtb"   # DTBs to build (worked example)
SRC_URI += "file://enable-cma.cfg"                 # config fragment
bitbake linux-yocto -c menuconfig                  # interactive; save as a fragment
SRC_URI += "file://fix-sensor-dma.patch"           # kernel patch
```

## Build History

```bash
INHERIT += "buildhistory"
BUILDHISTORY_COMMIT = "1"
buildhistory-diff        # compare the last two builds
```

Catches unintended package-size, dependency, or version changes after a layer bump.

## Offline / Air-Gapped Builds

Mechanics only — the *release discipline* around these (pinning, tagging, verifying) is the checklist in
`yocto-best-practices.md`.

```bash
BB_GENERATE_MIRROR_TARBALLS = "1"          # tar Git repos into DL_DIR
bitbake -c fetchall <target>               # or: bitbake --runall=fetch <image>
BB_NO_NETWORK = "1"                        # hard-fail on any network access
BB_FETCH_PREMIRRORONLY = "1"               # only use pre-populated mirrors
```

## Debugging a Task Failure

```bash
bitbake -c listtasks <recipe>                       # tasks available for a recipe
bitbake -g <recipe> && grep <recipe> pn-buildlist   # dependency tree
bitbake-layers show-recipes | grep <recipe>         # which layer provides it
bitbake-layers show-appends | grep <recipe>         # which appends fire
bitbake <recipe> -e | grep '^SRC_URI='              # variable value at build time
bitbake-getvar -r <recipe> SRC_URI                  # value + every assignment site
```

## Recipe Tooling: `recipetool`, `oe-pkgdata-util`

- `recipetool create <url>` — scaffold a recipe from a source URL or tarball, guessing `LICENSE`, `SRC_URI`, and
  checksums (verify the guess).
- `recipetool appendfile <layer> <target-path> <local-file>` — generate a `.bbappend` that installs or replaces a file,
  wiring `FILESEXTRAPATHS` for you.
- `recipetool setvar <recipe> VAR value` — edit a recipe variable programmatically.
- `oe-pkgdata-util find-path <path>` — which package ships a given file path.
- `oe-pkgdata-util list-pkg-files <pkg>` — the files a built package contains.
- `oe-pkgdata-util lookup-recipe <pkg>` — the recipe behind a runtime package name.
