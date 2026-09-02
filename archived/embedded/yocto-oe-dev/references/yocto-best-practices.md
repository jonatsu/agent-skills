# Yocto / OpenEmbedded Best Practices

Judgment reference: where a setting belongs, how to keep layers clean, how to
prepare a reproducible release, and how to share and prune sstate. For the raw
mechanics of any command named here, see `yocto-workflow.md`; for licensing and
SBOM, `compliance-and-sbom.md`.

## Contents

- [Layer Hygiene](#layer-hygiene)
- [Where Does a Setting Belong?](#where-does-a-setting-belong)
- [Poky Is a Reference, Not a Product Base](#poky-is-a-reference-not-a-product-base)
- [Release Preparation Checklist](#release-preparation-checklist)
- [Sharing sstate Across Machines](#sharing-sstate-across-machines)
- [Pruning sstate](#pruning-sstate)
- [CI Patterns](#ci-patterns)
- [wic Images and Flashing](#wic-images-and-flashing)
- [Common Traps](#common-traps)

## Layer Hygiene

- **Keep core layers pristine.** BitBake, OE-Core (`meta`), and `meta-poky` stay
  untouched; an upgrade overwrites local edits and the conflict is silent. Every
  customization goes in your own layer through a `.bbappend`.
- **One concern per layer** — BSP (machine/kernel/bootloader), distro (init, libc,
  ABI, global policy), middleware (third-party libraries), and application
  (product code) each get their own layer. Do not fold product code into a fork of
  OE-Core.
- **Start small.** Add a layer only when it earns its keep; layer count is
  compounding complexity.
- **Reuse before authoring.** Check the Yocto Compatible Layer Index — a
  `meta-<vendor>` layer for your SoC usually already exists.
- **Declare compatibility.** Every `layer.conf` sets `LAYERSERIES_COMPAT` (which
  releases the layer targets) and `LAYERDEPENDS` (which layers it needs). These are
  also your first evidence when debugging a release mismatch.

```bash
bitbake-layers show-layers
bitbake-layers show-recipes | grep <recipe>
bitbake-layers show-appends | grep <recipe>
```

## Where Does a Setting Belong?

The recurring mistake is treating `local.conf` as the project's configuration file.
It is not: a change there reparses every recipe and — because it is developer-local
and usually uncommitted — does not travel to teammates or CI, so the build is not
reproducible. `local.conf` is for genuinely local, disposable settings you would
never ship. `site.conf` carries host-wide settings (proxy, mirrors, shared-cache
paths) and has the same "does not travel" limitation.

Decide placement by asking *who and what a setting is about*, then put it in the
narrowest file that owns that scope:

| A setting about… | Goes in… | Examples |
|---|---|---|
| this developer's box | `local.conf` (never shipped) | `BB_NUMBER_THREADS`, `PARALLEL_MAKE`, `DL_DIR`, debug tweaks |
| this build host / site | `site.conf` | proxy, `SSTATE_MIRRORS`, shared-cache paths |
| distribution policy | `conf/distro/<name>.conf` | init system, libc, `DISTRO_FEATURES`, `PREFERRED_PROVIDER_*`, `PACKAGE_CLASSES`, license policy |
| a specific board | `conf/machine/<name>.conf` | kernel/bootloader provider, `IMAGE_FSTYPES`, serial console, kernel-into-rootfs `IMAGE_INSTALL` |
| image contents | an image recipe (`.bb`) | package set, `IMAGE_FEATURES` |

Two rules of thumb fall out of the table:

- **Do not grow `IMAGE_INSTALL:append` in `local.conf`.** The moment the
  `core-image-*` recipes stop being enough, write your own image recipe — it is
  versioned, shareable, and parse-order-safe.

  ```bitbake
  # my-app-image.bb
  require recipes-core/images/core-image-minimal.bb
  IMAGE_INSTALL:append   = " myapp libfoo"
  IMAGE_FEATURES:append  = " ssh-server-openssh"
  ```

- **Promote anything durable out of `local.conf`/`site.conf`** into the distro,
  machine, or image layer as soon as more than one person or machine depends on it.

## Poky Is a Reference, Not a Product Base

Poky is the Yocto Project's *reference* distribution: a demonstration configuration
(OE-Core + BitBake + the small `meta-poky` and `meta-yocto-bsp` layers) meant to
prove the system works, not to ship on a product. Its feature set is chosen for
breadth over stability and can shift between releases. Two consequences for a real
product:

- **Build your own distro** (`conf/distro/<name>.conf`) so *you* own the init
  system, C library, ABI, and default image policy, instead of tracking whatever
  Poky's reference defaults happen to be.
- **Watch Poky's default mirrors.** Poky ships `PREMIRRORS` that resolve fetches
  against a public Yocto mirror. For version-control fetches that means the *names*
  of the components you build travel to an external host — a confidentiality
  concern for a closed product. Set your own `PREMIRRORS`/`SOURCE_MIRROR_URL` (or
  `INHERIT += "own-mirrors"`) pointing at an internal mirror.

## Release Preparation Checklist

A reproducible, offline-capable release is three phases. Work them in order.

**1 — Pin and tag (make the inputs immutable).**

- [ ] No `SRCREV = "${AUTOREV}"` anywhere — every Git fetch pinned to a commit SHA.
      A floating branch is unreproducible and breaks air-gapped rebuilds.
- [ ] Every layer pinned to a tag or SHA (via a kas lockfile, a `repo` manifest, or
      submodule commits) and that manifest itself committed and tagged.
- [ ] `DISTRO_VERSION` set to the release identity.

**2 — Capture the sources (so the build needs no upstream later).**

```bash
BB_GENERATE_MIRROR_TARBALLS = "1"     # turn VCS checkouts into archives in DL_DIR
bitbake -c fetchall <image>           # or: bitbake --runall=fetch <image>
tar -czf dl-$(date +%Y%m%d).tar.gz "${DL_DIR}"   # archive DL_DIR as the source mirror
```

Publish the archive to your internal mirror and point BitBake at it with
`PREMIRRORS`/`SOURCE_MIRROR_URL` or `INHERIT += "own-mirrors"`.

**3 — Verify air-gapped (prove the capture is complete).**

```bash
BB_NO_NETWORK = "1" bitbake <image>       # fails loudly on any missed source / stray AUTOREV
BB_FETCH_PREMIRRORONLY = "1"              # or: restrict fetches to the internal mirror
```

**4 — Attach compliance artifacts.** Generate the SBOM, CVE report, and license /
source archives as part of the release — see `compliance-and-sbom.md`. Enable
`buildhistory` (committed) and diff it against the previous release to catch
unintended package-size, dependency, or version changes.

## Sharing sstate Across Machines

sstate reuse is keyed on a hash of each task's *inputs*, and those inputs include
aspects of the build host. So a shared cache pays off only when the machines that
produce and consume it are alike; a divergent host (different OS, tool versions)
computes different hashes and simply misses the cache instead of reusing it. Design
the share around that fact:

```bash
# site.conf, shared by all developers and CI
SSTATE_DIR     = "/mnt/shared/sstate"                          # local cache
SSTATE_MIRRORS = "file://.* http://internal-mirror/sstate/PATH"  # read-through mirror
DL_DIR         = "/mnt/shared/downloads"                       # shared source cache
```

- Serve the cache over **NFS or HTTP**; populate `PREMIRRORS` from a shared `DL_DIR`
  so sources are shared too.
- **Warm the cache from CI.** A nightly full build fills sstate before developers
  pull from it, so their first build of the day is fast.
- **Standardize the host to keep hashes stable.** A build container (for example
  `kas-container`, via **kas-dev**) pins the host environment, which is what makes
  the shared hashes actually match across machines.

## Pruning sstate

The cache grows without bound. Prune it deliberately — this is destructive, so gate
it (SKILL.md *Confirmation gates*) and echo the expanded `${SSTATE_DIR}` first.

```bash
./scripts/sstate-cache-management.sh --remove-duplicated -d --cache-dir="${SSTATE_DIR}"
# Age-based prune (irreversible — verify the path is not empty or '/')
find "${SSTATE_DIR}" -type f -atime +30 -delete
```

## CI Patterns

- **Pin the environment, not just the layers.** A container (kas-container, via
  **kas-dev**) fixes the host so sstate stays valid across runners.
- **Nightly full build** to keep sstate and `DL_DIR` warm; **incremental PR builds**
  against that warm cache for fast feedback.
- **Commit `buildhistory`** and diff each branch against main to surface regressions
  in package size, dependencies, or versions.
- **Lint appends after every layer bump** — a stale version glob or
  `LAYERSERIES_COMPAT` is a silent breakage:

  ```bash
  bitbake-layers show-appends
  ```

- **Release builds run offline** with `BB_FETCH_PREMIRRORONLY = "1"` (or
  `BB_NO_NETWORK = "1"`) to prove source capture.

## wic Images and Flashing

`wic` builds a partitioned, flashable image from build artifacts.

```bitbake
WKS_FILE      = "my-board.wks.in"       # in the image recipe or local.conf
IMAGE_FSTYPES = "wic wic.bmap"
```

```
# my-board.wks.in (worked example)
part u-boot --source rawcopy --sourceparams="file=u-boot.imx" --no-table --align 2
part /boot  --source bootimg-partition --use-uuid --fstype=vfat --label boot \
            --active --align 8192 --size 64
part /      --source rootfs --use-uuid --fstype=ext4 --label root --align 8192
```

Writing the image destroys the target device — this passes SKILL.md *Confirmation
gates*, and you MUST confirm the `/dev/sdX` path with `lsblk` immediately before:

```bash
bmaptool copy my-image.wic /dev/sdX     # faster: skips unwritten blocks (needs the .bmap)
dd if=my-image.wic of=/dev/sdX bs=4M conv=fsync status=progress   # fallback
```

## Common Traps

| Trap | Fix |
|------|-----|
| `_append` on Kirkstone+ silently no-ops | use `:append` (confirm release first) |
| `+=` in `local.conf` override | use `:append` / `:prepend` |
| `SRCREV = "${AUTOREV}"` in a release | pin to a commit SHA |
| Poky distro / default PREMIRRORS in production | own distro + own mirror |
| `IMAGE_INSTALL +=` growing in `local.conf` | write a custom image recipe |
| `.bbappend` version glob mismatch | use the `%` wildcard |
| `FILESEXTRAPATHS:prepend` missing in a `.bbappend` | add `:prepend := "${THISDIR}/files:"` |
| stale sstate after a `MACHINE` change | `bitbake -c cleansstate <recipe>` (gated) |
| `DEPENDS` used for a runtime dep | use `RDEPENDS:${PN}` |
| missing `LIC_FILES_CHKSUM` | add it (or `LICENSE = "CLOSED"`) — see compliance ref |
| `def` block in a `.conf` fails to parse | move it to a `.inc`; only BBHandler (`.bb`/`.bbclass`/`.inc`) accepts `def`, ConfHandler owns `.conf` |
| `#CONFIG_X is not set` in a kernel `.cfg` is ignored | needs the space — `# CONFIG_X is not set`; without it Kconfig reads a comment and the option keeps its defconfig value |
| distro identity set before `require conf/distro/poky.conf` is lost | poky assigns `DISTRO`/`DISTRO_NAME`/`DISTRO_VERSION` with hard `=`; set yours after the require |
| `kernel-module-*` in `IMAGE_INSTALL` breaks when the symbol turns `=y` | built-in emits no module, so the package stops existing; drop it in the same change |
| dlopen'd plugin absent at runtime though its provider is installed | plugins create no shared-library dependency, so nothing pulls them in; name the package explicitly |
| `buildhistory` gives stale or mismatched answers | it keys on `MACHINE_ARCH` while deploy uses `MACHINE` (differ on hyphens), and keeps dirs for previously-named images — select the newest by mtime |
| `UNPACKDIR` undefined on Scarthgap and older | use `${WORKDIR}` for `file://` sources |
