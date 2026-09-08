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
- [Packaging: `PACKAGES` and `FILES`](#packaging-packages-and-files)
- [Optional Features: `PACKAGECONFIG`](#optional-features-packageconfig)
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

**The output directory is not always `tmp/`.** `TMPDIR` defaults to `${TOPDIR}/tmp`, but OE-Core's
`defaultsetup.conf` then appends `TCLIBCAPPEND`, itself defaulting to `-${TCLIBC}` — so an ordinary distro builds into
`tmp-glibc/`. Poky sets `TCLIBCAPPEND = ""`, which is the only reason Poky builds show a plain `tmp/`. Deployed
artifacts land in `DEPLOY_DIR_IMAGE` (`${DEPLOY_DIR}/images/${MACHINE}` by default), and `DEPLOY_DIR` is commonly moved
outside `TMPDIR` altogether. Resolve both instead of assuming them, especially before reporting an artifact missing:

```bash
bitbake-getvar TMPDIR
bitbake-getvar -r <image-recipe> DEPLOY_DIR_IMAGE
```

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

`:append`, `:prepend`, and `:remove` (the `_append`/`_prepend`/`_remove` forms before Honister) are applied at
variable-expansion time, after parsing. You control all spacing yourself. Application order is `:append`, then
`:prepend`, then `:remove`.

**What "order-independent" does and does not mean.** Because they are deferred to expansion, an `:append` cannot be
wiped by a plain `=` parsed later in another file — that is the property worth having. It does **not** mean the appends
are unordered among themselves: two `:append` operations on the same variable concatenate in the order BitBake parsed
them, so a conditional override and an unconditional one still compose in a definite sequence. Inspect the result with
`bitbake-getvar -r <recipe> VAR`, which prints every assignment site alongside the final value, rather than reasoning
it out.

**Global config files.** Parse order there is defined, not arbitrary: `bitbake.conf` includes `site.conf`, `auto.conf`
and `local.conf`, and only then the multiconfig, machine and distro configs. That ordering is the real hazard — a
`VAR = "…"` in a machine or distro conf silently overwrites a `VAR += "…"` written earlier in `local.conf`, while an
`:append` survives it. Prefer the override forms for any variable a machine or distro conf also assigns. `+=` remains
correct and idiomatic for variables nothing downstream reassigns (`BBLAYERS`, `EXTRA_IMAGE_FEATURES`, `INHERIT`), and
OE's own examples use it; do not rewrite working `+=` lines without a reassignment to point at.

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

**Forgetting `RDEPENDS` is usually *not* how you get a missing library at runtime.** `do_package` scans the built ELF
objects, reads their `NEEDED` entries, and `read_shlibdeps` merges the resolved providers into each package's
`RDEPENDS` automatically. A normally-linked shared library therefore ends up in the runtime dependency set whether or
not the recipe names it, and if no recipe provides it, packaging QA reports the unresolved dependency at build time
rather than deferring it to the board.

Three different mechanisms, worth separating before editing a recipe:

| Need                                      | Mechanism                   | Declared by                                            |
| ----------------------------------------- | --------------------------- | ------------------------------------------------------ |
| A library/header to *build* against       | `DEPENDS`                   | you, explicitly                                        |
| A shared library the binary links against | generated from ELF `NEEDED` | the build, automatically — usually needs no `RDEPENDS` |
| Anything with no link-time trace          | `RDEPENDS:${PN}`            | you, explicitly — nothing can infer it                 |

The third row is where an explicit `RDEPENDS` genuinely earns its place: an interpreter for a shipped script
(`#!/usr/bin/env python3`), a `dlopen`'d plugin, a command the program shells out to, or a data/config package. None of
those appear in `NEEDED`, so nothing detects them and the failure really does land at runtime.

When a library *is* missing on target despite linking, suspect the package split (it landed in `-dev` or a separate
subpackage) or an `RDEPENDS` you removed by hand, and check the generated metadata with
`oe-pkgdata-util read-value RDEPENDS <pkg>` before adding names speculatively.

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

DEPENDS        = "openssl"        # build-time: headers/libs to link against
RDEPENDS:${PN} = "bash"           # runtime deps NOTHING can infer (here: a shipped script's
                                  # interpreter). The libssl link is detected automatically —
                                  # see "Task Dependency Varflags".

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

## Packaging: `PACKAGES` and `FILES`

`do_install` fills `${D}`; `do_package` then splits that tree into binary packages. Each path is matched against
`FILES:<pkg>` for every package in `PACKAGES` **in order, and the first match claims it** — a file already taken is
skipped for every later package. The default list puts `${PN}` last:

```bitbake
PACKAGES = "${PN}-src ${PN}-dbg ${PN}-staticdev ${PN}-dev ${PN}-doc ${PN}-locale ${PACKAGE_BEFORE_PN} ${PN}"
```

So the main package receives only what the `-src`/`-dbg`/`-staticdev`/`-dev`/`-doc`/`-locale` globs left behind. That is
why a shared library splits without anyone asking for it: `FILES:${PN}` claims `${libdir}/lib*${SOLIBS}` (`.so.*`, the
versioned runtime object) while `FILES:${PN}-dev` claims `${FILES_SOLIBSDEV}` (`.so`, the development symlink). A
library that looks "missing" on target is usually this split rather than a missing dependency — check with
`oe-pkgdata-util list-pkg-files`.

To add a package that must claim files **before** `${PN}` takes them, put it in `PACKAGE_BEFORE_PN`; appending to
`PACKAGES` places it after `${PN}`, where it gets nothing. `ALLOW_EMPTY:<pkg> = "1"` keeps a package that ends up with
no files at all (the default for `-dev` and `-dbg`).

### `installed but not shipped`

Whatever is left in `${D}` that no package's `FILES` claimed is reported by path, and this is an **error, not a
warning** — `installed-vs-shipped` is in the default `ERROR_QA`. Read the listed paths: each one says either "extend
`FILES`" or "`do_install` should not have installed this".

```bitbake
FILES:${PN} += "${datadir}/myapp"            # ship them, or
INSANE_SKIP:${PN} += "installed-vs-shipped"  # silence the check — read the caveat first
```

`INSANE_SKIP` silences the report; it packages nothing. Those files then belong to no package and are absent from the
image, so the skip is only right when they genuinely should not ship — and deleting them at the end of `do_install` is
usually the clearer way to say that. Note the key: this check reads `INSANE_SKIP:<recipe>` (`PN`), whereas most other
QA checks are keyed by *package* name, so the two forms coincide only for the main package.

## Optional Features: `PACKAGECONFIG`

`PACKAGECONFIG` is OE's idiom for a recipe's optional features, and the alternative to hand-editing `EXTRA_OECONF` and
`DEPENDS` in a `.bbappend`. Each feature is one varflag holding up to six comma-separated fields:

```bitbake
PACKAGECONFIG ??= "ssl"
PACKAGECONFIG[ssl] = "--enable-ssl,--disable-ssl,openssl"
PACKAGECONFIG[gtk] = "--with-gtk,--without-gtk,gtk+3"
#                     enable-arg,disable-arg,DEPENDS,RDEPENDS,RRECOMMENDS,conflicts
```

Fields 3–5 are added to the recipe's dependencies only when the feature is enabled. Critically, **every declared
feature that is not listed contributes its disable argument**: the variable declares the whole enabled set, it is not
an additive list.

```bitbake
PACKAGECONFIG:append = " gtk"   # correct — adds gtk, keeps the recipe's defaults (note the leading space)
PACKAGECONFIG = "gtk"           # in a .bbappend this silently DISABLES every other default feature
```

A feature name with no matching varflag is only a warning (`invalid-packageconfig` sits in `WARN_QA`), so a typo
disables the feature you meant to turn on and the build still succeeds. Confirm the outcome rather than the intent:

```bash
bitbake-getvar -r <recipe> PACKAGECONFIG
bitbake-getvar -r <recipe> PACKAGECONFIG_CONFARGS   # the arguments actually passed to configure
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

sstate (shared state) caches the output of the tasks a class opted in via `SSTATETASKS` — `do_populate_sysroot`,
`do_package_write_*` and friends, not literally every task — as a tarball keyed by a hash of that task's inputs. On
rebuild BitBake reuses the cached result when the input hash is unchanged. That is the core of Yocto's incremental
speed. (Sharing sstate across machines and pruning it: `yocto-best-practices.md`.)

### Three things that are easy to conflate

| Thing              | What it is                                                    | Where it lives           |
| ------------------ | ------------------------------------------------------------- | ------------------------ |
| **Stamp**          | a marker that this task already ran *in this build directory* | `tmp/stamps/`            |
| **Task hash**      | a checksum over the task's inputs; the sstate lookup key      | in the signature/stamp   |
| **sstate archive** | the reusable output tarball itself                            | `${SSTATE_DIR}`, mirrors |

A task hash is an **integrity/lookup key, not a publisher signature.** It answers "were the inputs the same?", never
"who produced this and do I trust them?"

Cryptographic signing is a separate, opt-in layer and is **off by default**: `SSTATE_SIG_KEY` defaults to empty (so
nothing is signed) and `SSTATE_VERIFY_SIG` defaults to `"0"` (so nothing is verified on extraction). Consequently
**a shared or mirrored sstate cache is unauthenticated unless you configured it otherwise**, and anything that can
write to that directory or mirror can hand your build a binary artifact. Decide the trust policy explicitly: either
treat the cache as a trusted-boundary asset (access-controlled directory, mirror you host), or turn on signing with
`SSTATE_SIG_KEY`, `SSTATE_VERIFY_SIG = "1"` and `SSTATE_VALID_SIGS`, and then test that an unsigned or wrong-key
archive is actually rejected.

### Diagnose before you delete

Ordinary `MACHINE` switches, recipe patches and layer bumps **are** hashed inputs — they normally invalidate the
affected tasks correctly. So "stale sstate" is a conclusion to reach *after* evidence, not the first guess; reaching
for `cleansstate` on suspicion throws away hours of reusable work and usually leaves the real cause in place.

Compare the signatures and let them name the changed input:

```bash
bitbake-dumpsig <sigfile>                  # inspect one task's signature inputs
bitbake-diffsigs <sig-a> <sig-b>           # exactly which input differs between two runs
bitbake -S printdiff <recipe>              # why this task will not reuse the cached result
```

Genuine causes look like an input BitBake could not see: a file changed in place that nothing checksums, a dependency
excluded via `vardepsexclude`, a host tool leaking into a task, or an sstate mirror serving artifacts built elsewhere.

When cleanup really is warranted, pick the narrowest tool and know its blast radius:

```bash
bitbake -c <task> -f <recipe>              # force ONE task to rerun; keeps everything else
bitbake -c clean <recipe>                  # remove this recipe's WORKDIR + stamps (sstate kept)
bitbake -c cleansstate <recipe>            # also drop its LOCAL sstate → full rebuild of it
bitbake -c cleanall <recipe>               # also delete its downloads → refetch from network
```

Three limits to state before running any of them:

- **`cleansstate` only clears the local `${SSTATE_DIR}`.** It cannot remove objects from a remote `SSTATE_MIRRORS`, so
  the next build may fetch the very artifact you thought you deleted. Rebuild against the mirror disabled if you need
  to prove a local rebuild.
- **`cleanall` is discouraged as routine practice** — it forces a refetch from upstream and defeats the source capture
  an offline or release build depends on.
- **On a shared cache, cleanup affects other people's builds**, and concurrent downloads into a shared `DL_DIR` are a
  known hazard. Never prune a shared directory as a personal debugging step.

All of these are gated — see SKILL.md *Confirmation gates* — and scoping to one recipe beats a global wipe.

## devtool Workflow

**Local, no target involved.** These stay inside the build directory and need no special authorization:

```bash
devtool add myapp https://github.com/org/myapp.git   # new recipe from source
devtool modify linux-yocto                            # bring a recipe into the workspace
devtool build myapp
devtool finish myapp meta-mylayer                     # write changes back as patches
devtool upgrade myapp                                 # bump to a new upstream version
```

Editable source lives at `workspace/sources/<recipe>/` and survives rebuilds.

**Crossing to a live board.** `deploy-target` is a different kind of operation and belongs behind SKILL.md
*Confirmation gates*: it opens SSH to a running machine and installs the recipe's `do_install` output onto it.

```bash
devtool deploy-target -n myapp root@<target>    # DRY RUN: list what would be written
devtool deploy-target myapp root@<target>       # the actual write, once authorized
devtool undeploy-target myapp root@<target>     # restore what it replaced
```

Four properties that decide whether this will do what you expect:

- **It deploys the recipe only, never its runtime dependencies.** The command assumes the target already has them
  installed. A binary that deploys "successfully" and then fails to start for a missing library is the normal
  presentation of this, not a build defect.
- **Existing files are preserved by default** and restored by `undeploy-target`; `--no-preserve` discards that safety
  net. Undeploy recovers files this tool replaced — it is not a general rollback of the board.
- **Resolve the target identity before connecting**, and reuse an authorization the user already gave for that board
  rather than asking again per invocation. `-n/--dry-run` answers "what would change?" without touching it.
- **The board keeps whatever you left on it.** Deployed output persists across your build directory being cleaned, so
  a stale deploy can mask a later change; undeploy when finishing rather than assuming a rebuild supersedes it.

Runtime debugging on the board once the code is there routes to **embedded-linux-bringup**.

## SDK Generation

```bash
bitbake core-image-minimal -c populate_sdk       # standard SDK (cross toolchain + sysroot)
bitbake core-image-minimal -c populate_sdk_ext   # extensible SDK (bundles devtool)
./tmp/deploy/sdk/poky-glibc-x86_64-*-toolchain-*.sh   # installer (name and path are distro-specific)
source /opt/poky/<ver>/environment-setup-aarch64-poky-linux
```

**Those last two paths are Poky's, not universal.** The installer filename comes from `SDK_NAME` and the default
install prefix from `SDKPATHINSTALL`, both set by the distro conf, so a custom distro produces different strings —
and the deploy directory follows `TMPDIR`, which is `tmp-glibc/` outside Poky. Resolve them rather than pattern-match:

```bash
bitbake-getvar -r <image-recipe> SDK_NAME          # one variable per call
bitbake-getvar -r <image-recipe> SDKPATHINSTALL
ls "$(bitbake-getvar --value --quiet DEPLOY_DIR)/sdk"
```

`bitbake-getvar` takes a single variable name. By default it prints the assignment history *and* the value; add
`--value` for the bare value alone, which is what a command substitution needs, and `--quiet` to keep server logging
out of it.

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

**Resolve the directory, do not guess it by timestamp.** The image path is deterministic:

```bitbake
BUILDHISTORY_DIR       ?= "${TOPDIR}/buildhistory"
BUILDHISTORY_DIR_IMAGE  = "${BUILDHISTORY_DIR}/images/${MACHINE_ARCH}/${TCLIBC}/${IMAGE_BASENAME}"
```

```bash
bitbake-getvar -r <image-recipe> BUILDHISTORY_DIR_IMAGE   # the exact directory for THIS image
cat <that-dir>/build-id.txt                                # MACHINE, image, DISTRO, DISTRO_VERSION
```

Picking "the newest directory by mtime" is unreliable and silently compares the wrong things: buildhistory retains
directories for every image and machine ever built in that build directory, so the newest may belong to a different
image entirely, and copying, restoring or merely touching a tree rewrites mtimes without changing what is inside.
Resolve `BUILDHISTORY_DIR_IMAGE` for the image you mean, then confirm identity from `build-id.txt` before trusting a
diff. Note also that the path keys on `MACHINE_ARCH` while deployed artifacts are named with `MACHINE`; the two differ
where a machine name contains a hyphen, so do not derive one from the other by hand.

## Offline / Air-Gapped Builds

Mechanics only — the *release discipline* around these (pinning, tagging, verifying) is the checklist in
`yocto-best-practices.md`.

**These are BitBake configuration variables, not shell prefixes.** Set them in `local.conf` or `site.conf`:

```bitbake
BB_GENERATE_MIRROR_TARBALLS = "1"    # turn VCS checkouts into archives in DL_DIR
BB_NO_NETWORK = "1"                  # deny ALL network access; any fetch that needs it fails
BB_FETCH_PREMIRRORONLY = "1"         # restrict fetching to PREMIRRORS entries
```

Writing `BB_NO_NETWORK = "1" bitbake <image>` on a shell command line does not do what it looks like: with spaces
around the `=` the shell reads `BB_NO_NETWORK` as the *command name* and exits **127** before BitBake ever starts. The
spaceless form `BB_NO_NETWORK=1 bitbake <image>` is at least valid shell, but BitBake filters its environment into the
datastore — only variables passed through `BB_ENV_PASSTHROUGH_ADDITIONS` arrive — so an exported variable is not
reliably in effect either. Put the policy in configuration and **verify the value BitBake actually holds**:

```bash
bitbake-getvar BB_NO_NETWORK
bitbake-getvar BB_FETCH_PREMIRRORONLY
```

**The two settings prove different things.** `BB_FETCH_PREMIRRORONLY` restricts *where* fetches may come from; a
premirror can itself be an `http://` host, so a build that passes with it is not thereby proved offline.
`BB_NO_NETWORK` is the one that denies network access outright. Use premirror-only to prove "every source is in our
mirror", and no-network to prove "this builds with the cable pulled" — do not report one as evidence for the other.

Capture the sources, then verify:

```bash
bitbake --runall=fetch <image>     # fetch everything without building
                                   # (prefer this: the old `-c fetchall` task no longer exists)
tar -czf dl-mirror.tar.gz -C "${DL_DIR}" .
```

The archive is a flat directory of source archives and mirror tarballs plus `.done` stamps — extract it *as*
`DL_DIR`, or publish the extracted directory and point at it with a `file://` premirror. It is not a nested tree to
copy on top of a build directory:

```bitbake
SOURCE_MIRROR_URL = "file:///mnt/mirror/downloads"
INHERIT += "own-mirrors"
BB_FETCH_PREMIRRORONLY = "1"
```

**Verify in a build directory with cold caches.** An existing `DL_DIR` or sstate cache satisfies a fetch that the
mirror is actually missing, so an offline build that reuses your working caches proves nothing about the capture.
Point `DL_DIR` at the extracted mirror only, use a fresh `TMPDIR`, and confirm the negative case as well: a
deliberately removed source must make the build fail, or the test cannot distinguish a complete capture from an
unused one.

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
- `oe-pkgdata-util read-value RDEPENDS <pkg>` — a package's *generated* metadata, including the shared-library
  dependencies the build detected automatically. Read this before adding an `RDEPENDS` by hand.
