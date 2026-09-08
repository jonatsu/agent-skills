# Yocto / OpenEmbedded Best Practices

Judgment reference: where a setting belongs, how to keep layers clean, how to prepare a reproducible release, and how to
share and prune sstate. For the raw mechanics of any command named here, see `yocto-workflow.md`; for licensing and
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

- **Keep core layers pristine.** BitBake, OE-Core (`meta`), and `meta-poky` stay untouched; an upgrade overwrites local
  edits and the conflict is silent. Every customization goes in your own layer through a `.bbappend`.
- **One concern per layer** — BSP (machine/kernel/bootloader), distro (init, libc, ABI, global policy), middleware
  (third-party libraries), and application (product code) each get their own layer. Do not fold product code into a fork
  of OE-Core.
- **Start small.** Add a layer only when it earns its keep; layer count is compounding complexity.
- **Reuse before authoring.** Check the Yocto Compatible Layer Index — a `meta-<vendor>` layer for your SoC usually
  already exists.
- **Declare compatibility.** Every `layer.conf` sets `LAYERSERIES_COMPAT` (which releases the layer targets) and
  `LAYERDEPENDS` (which layers it needs). These are also your first evidence when debugging a release mismatch.
  `LAYERDEPENDS` names **collections, not directories** — BitBake resolves each entry against `BBFILE_COLLECTIONS`, so
  a layer living in `meta-foo/` but declaring the collection `foo` must be depended on as `foo`. Name the directory
  instead and the parse fails with `depends on layer 'y', but this layer is not enabled`, which reads like a missing
  layer even though it is sitting right there in `bblayers.conf`.

```bash
bitbake-layers show-layers
bitbake-layers show-recipes | grep <recipe>
bitbake-layers show-appends | grep <recipe>
```

## Where Does a Setting Belong?

The recurring mistake is treating a hand-edited `local.conf` as the project's configuration file. A change there
reparses every recipe, and when the file is developer-local and uncommitted it does not travel to teammates or CI, so
the build is not reproducible. Hand-maintained `local.conf` is for genuinely local, disposable settings you would never
ship; `site.conf` carries host-wide settings (proxy, mirrors, shared-cache paths) with the same limitation.

**The defect is "unversioned and hand-edited", not the file itself.** A `local.conf` that is *generated* from a
committed source — a kas config's `local_conf_header`, a CI template, a checked-in fragment — travels, reproduces, and
reviews perfectly well, and that is a legitimate and common design. When you find one, read the generator as the source
of truth and edit *it*; do not "fix" a generated `local.conf` by hand (the next `kas build` overwrites it) and do not
recommend migrating settings out of a versioned generator that already solves the reproducibility problem. kas
orchestration itself routes to **kas-build-orchestration**.

The placement table below still applies to the *content*: it says which scope owns a setting, whoever writes the file.

**Let the parse order decide, because it already decides for you.** `bitbake.conf` pulls the configuration files in a
fixed sequence, and a plain `=` in a later file silently beats anything an earlier one set:

```bitbake
include conf/site.conf                          # 1. host / site
include conf/auto.conf                          # 2. written by tooling, not by hand
include conf/local.conf                         # 3. this build directory
require conf/multiconfig/${BB_CURRENT_MC}.conf  # 4. multiconfig
include conf/machine/${MACHINE}.conf            # 5. board
include conf/distro/${DISTRO}.conf              # 6. distribution policy
```

Read that list downward and it answers both questions at once: which file owns a setting, and which file can overrule
which. Anything a machine or distro conf assigns is beyond `local.conf`'s reach with `=` or `+=`, so a setting you want
to survive belongs at or below the level that owns it — or must use `:append`, applied after every file is parsed.

| Level in the parse order     | Owns                             | Observable examples                                                                                     |
| ---------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 1 `site.conf`                | this build host                  | proxy settings, `SSTATE_MIRRORS`, shared `DL_DIR`/`SSTATE_DIR` paths                                    |
| 2 `auto.conf`                | whatever your tooling generates  | CI-injected values; hand-editing it loses the next time the generator runs                              |
| 3 `local.conf`               | this build directory, disposably | `BB_NUMBER_THREADS`, `PARALLEL_MAKE`, `EXTRA_IMAGE_FEATURES` debug tweaks                               |
| 5 `conf/machine/<name>.conf` | one board                        | `KERNEL_IMAGETYPE`, `PREFERRED_PROVIDER_virtual/bootloader`, `SERIAL_CONSOLES`, `IMAGE_FSTYPES`         |
| 6 `conf/distro/<name>.conf`  | policy across every board        | `DISTRO_FEATURES`, `INIT_MANAGER`, `PACKAGE_CLASSES`, `PREFERRED_VERSION_*`, `TCLIBCAPPEND`, SDK naming |
| — an image recipe (`.bb`)    | what lands in one image          | `IMAGE_INSTALL`, `IMAGE_FEATURES`                                                                       |

The distro row is not a guess: read `meta-poky/conf/distro/poky.conf` in your own checkout, which sets exactly those —
identity (`DISTRO`, `DISTRO_VERSION`, `DISTRO_CODENAME`), `DISTRO_FEATURES`, `INIT_MANAGER`, `PACKAGE_CLASSES`,
`PREFERRED_VERSION_linux-yocto`, `TCLIBCAPPEND`, `SDK_NAME`/`SDKPATHINSTALL`, a signature handler, and a set of
`INHERIT` and `require` lines for security flags, `uninative` and `create-spdx`. It is the worked example of the file
you are being told to write.

Two rules of thumb fall out of the table:

- **Do not grow `IMAGE_INSTALL:append` in `local.conf`.** The moment the `core-image-*` recipes stop being enough, write
  your own image recipe — it is versioned, shareable, and parse-order-safe.

  ```bitbake
  # my-app-image.bb
  require recipes-core/images/core-image-minimal.bb
  IMAGE_INSTALL:append   = " myapp libfoo"
  IMAGE_FEATURES:append  = " ssh-server-openssh"
  ```

- **Promote anything durable out of a hand-edited `local.conf`/`site.conf`** into the distro, machine, or image layer as
  soon as more than one person or machine depends on it. Reusable policy belongs in a layer even when a generator is
  emitting the config correctly — a generated `local.conf` solves reproducibility, not reuse across products.

## Poky Is a Reference, Not a Product Base

Poky is the Yocto Project's *reference* distribution: a demonstration configuration (OE-Core + BitBake + the small
`meta-poky` and `meta-yocto-bsp` layers) meant to prove the system works, not to ship on a product. Its feature set is
chosen for breadth over stability and can shift between releases. Two consequences for a real product:

- **Build your own distro** (`conf/distro/<name>.conf`) so *you* own the init system, C library, ABI, and default image
  policy, instead of tracking whatever Poky's reference defaults happen to be.
- **Watch Poky's default mirrors.** Poky ships `PREMIRRORS` that resolve fetches against a public Yocto mirror. For
  version-control fetches that means the *names* of the components you build travel to an external host — a
  confidentiality concern for a closed product. Set your own `PREMIRRORS`/`SOURCE_MIRROR_URL` (or
  `INHERIT += "own-mirrors"`) pointing at an internal mirror.

## Release Preparation Checklist

A reproducible, offline-capable release is three phases. Work them in order.

**1 — Pin and tag (make the inputs immutable).**

- [ ] No `SRCREV = "${AUTOREV}"` anywhere — every Git fetch pinned to a commit SHA. A floating branch is unreproducible
  and breaks air-gapped rebuilds.
- [ ] Every layer pinned to a tag or SHA (via a kas lockfile, a `repo` manifest, or submodule commits) and that manifest
  itself committed and tagged.
- [ ] `DISTRO_VERSION` set to the release identity.

**2 — Capture the sources (so the build needs no upstream later).**

Set in `local.conf`/`site.conf`, then fetch:

```bitbake
BB_GENERATE_MIRROR_TARBALLS = "1"     # turn VCS checkouts into archives in DL_DIR
```

```bash
bitbake --runall=fetch <image>                       # fetch everything, build nothing
tar -czf dl-mirror.tar.gz -C "${DL_DIR}" .           # DL_DIR's CONTENTS are the mirror
```

Publish the extracted archive to your internal mirror and point BitBake at it with `SOURCE_MIRROR_URL` +
`INHERIT += "own-mirrors"`, or an explicit `PREMIRRORS`. Extract it *as* a `DL_DIR`-shaped directory — it is a flat set
of archives and `.done` stamps, not a tree to overlay onto a build directory.

**3 — Verify air-gapped (prove the capture is complete).**

These are **configuration variables, not shell prefixes**. `BB_NO_NETWORK = "1" bitbake <image>` typed at a prompt
exits 127 running a command named `BB_NO_NETWORK`; the build never starts, and a green terminal proves nothing. Put
them in configuration and confirm the effective values:

```bitbake
BB_NO_NETWORK = "1"                   # denies ALL network access
# or, to prove only that the mirror is complete:
BB_FETCH_PREMIRRORONLY = "1"          # restricts fetching to PREMIRRORS
```

```bash
bitbake-getvar BB_NO_NETWORK          # verify BitBake actually holds it
bitbake --runall=fetch <image>        # fails loudly on a missed source or stray AUTOREV
```

Two conditions decide whether this test means anything:

- **Choose the variable that matches the claim.** A premirror may be an `http://` host, so passing with
  `BB_FETCH_PREMIRRORONLY` shows the mirror is complete, *not* that the build runs without a network.
  `BB_NO_NETWORK` is the air-gap claim.
- **Start from cold caches.** A populated `DL_DIR` or sstate cache silently satisfies sources the mirror is missing.
  Verify with `DL_DIR` pointing at the extracted mirror alone and a fresh `TMPDIR`, and confirm the negative case: with
  one source removed from the mirror, the build must fail.

**4 — Attach compliance artifacts.** Generate the SBOM, CVE report, and license / source archives as part of the release
— see `compliance-and-sbom.md`. Enable `buildhistory` (committed) and diff it against the previous release to catch
unintended package-size, dependency, or version changes.

## Sharing sstate Across Machines

sstate reuse is keyed on a hash of each task's *inputs*. A mismatch is a cache **miss**, never a wrong result — the
build falls back to compiling, which is slow but correct.

How much the host matters depends on what is being built. Target recipes are cross-compiled and largely insulated from
the host, and `uninative` exists precisely to keep `-native` output portable across distributions by pinning a common
loader and libc. So a shared cache does *not* require identical machines. Host divergence still costs hit rate, mostly
through `-native` and SDK tasks and through the tool versions that leak into a task's signature, and
`NATIVELSBSTRING` partitions some native artifacts by distribution. Standardising the host is a hit-rate optimisation,
not a correctness precondition.

When hit rates disappoint, measure rather than assume: `bitbake -S printdiff <recipe>` names the input that differed.
Design the share around that:

```bash
# site.conf, shared by all developers and CI
SSTATE_DIR     = "/mnt/shared/sstate"                          # local cache
SSTATE_MIRRORS = "file://.* http://internal-mirror/sstate/PATH"  # read-through mirror
DL_DIR         = "/mnt/shared/downloads"                       # shared source cache
```

**Settle these before anyone shares a cache**, because they decide whether the share is safe and functional at all:

- **Treat the cache as a trust boundary.** sstate archives are unsigned and unverified by default (`SSTATE_SIG_KEY`
  empty, `SSTATE_VERIFY_SIG = "0"`), so write access to a shared directory or mirror is the ability to inject binaries
  into everyone's build. Restrict who can write it, or enable signing and verification and test that a bad archive is
  actually rejected. See the sstate section of `yocto-workflow.md`.
- **Decide how it is served and who writes it.** NFS gives a shared `SSTATE_DIR`; HTTP gives a read-only
  `SSTATE_MIRRORS` that developers cannot poison, which is usually the better default. Share sources the same way, with
  `PREMIRRORS` pointing at a common `DL_DIR`.

**Then raise the hit rate.** These are optimisations, and a miss only costs time:

- **Warm the cache from CI.** A nightly full build populates sstate before developers pull from it, so their first build
  of the day is fast.
- **Pin the host environment.** A build container (for example `kas-container`, via **kas-build-orchestration**) keeps
  native and SDK signatures matching across machines. Keep `INHERIT += "uninative"` in play too — it is what makes
  native artifacts portable between distributions in the first place.

## Pruning sstate

The cache grows without bound. Prune it deliberately — this is destructive, so gate it (SKILL.md *Confirmation gates*)
and expand `${SSTATE_DIR}` and read it back first.

```bash
echo "${SSTATE_DIR}"   # necessary, NOT sufficient — see below
./scripts/sstate-cache-management.py -d --cache-dir="${SSTATE_DIR}"   # drop all but the newest per package
# Age-based prune (irreversible)
find "${SSTATE_DIR}" -type f -atime +30 -delete
```

**Confirm the script's name for your release before quoting it.** OE-Core rewrote this tool in Python: it is
`sstate-cache-management.sh` up to and including Kirkstone (4.0) and `sstate-cache-management.py` by Scarthgap (5.0),
where the shell version no longer exists. The `-d`/`--remove-duplicated` and `--cache-dir` options survived the
rewrite, so only the filename changes. The Python version also takes `--stamps-dir` to keep exactly what the named
build directories still use, and prompts before deleting unless you pass `-y`/`--yes`.

Printing the path catches the catastrophic case — an empty expansion turning the `find` into a walk of `/` — but a
plausible-looking path is not a safe one. Two further checks before deleting:

- **Whose cache is it?** A path under `/mnt/shared` or an NFS mount is very likely someone else's working set and CI's
  warm cache as well. Pruning a shared cache is a team-wide action, not a personal cleanup; take it to whoever owns it.
- **Will it come back anyway?** `SSTATE_MIRRORS` entries are untouched by any local prune, so deleting locally may
  simply force a re-download rather than the rebuild you intended.

Age-based pruning uses access times, so a filesystem mounted `noatime` or `relatime` can report far older access than
reality and delete entries still in daily use. Check the mount options before trusting `-atime`.

## CI Patterns

- **Pin the environment, not just the layers.** A container (kas-container, via **kas-build-orchestration**) fixes the
  host so sstate stays valid across runners.

- **Nightly full build** to keep sstate and `DL_DIR` warm; **incremental PR builds** against that warm cache for fast
  feedback.

- **Commit `buildhistory`** and diff each branch against main to surface regressions in package size, dependencies, or
  versions.

- **Lint appends after every layer bump** — a stale version glob or `LAYERSERIES_COMPAT` is a silent breakage:

  ```bash
  bitbake-layers show-appends
  ```

- **Release builds run offline** with `BB_FETCH_PREMIRRORONLY = "1"` to prove the mirror is complete, or
  `BB_NO_NETWORK = "1"` to prove the build needs no network at all. Set them in configuration, not as shell prefixes,
  and run the job from cold caches — a warm `DL_DIR` makes either check pass vacuously.

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

Writing the image destroys the target device — this passes SKILL.md *Confirmation gates*, and you MUST confirm the
`/dev/sdX` path with `lsblk` immediately before:

```bash
bmaptool copy my-image.wic /dev/sdX     # faster: skips unwritten blocks (needs the .bmap)
dd if=my-image.wic of=/dev/sdX bs=4M conv=fsync status=progress   # fallback
```

## Common Traps

| Trap                                                                   | Fix                                                                                                                                                                                                  |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `_append` on Honister+ aborts the parse with a fatal error             | use `:append` (confirm the release first); the reverse — `:append` on a pre-Honister tree — is the silent one                                                                                        |
| `+=` in `local.conf` clobbered by a machine/distro conf                | `local.conf` parses first, so a later hard `=` wins; use `:append` for variables those files also assign                                                                                             |
| `SRCREV = "${AUTOREV}"` in a release                                   | pin to a commit SHA                                                                                                                                                                                  |
| Poky distro / default PREMIRRORS in production                         | own distro + own mirror                                                                                                                                                                              |
| `IMAGE_INSTALL +=` growing in `local.conf`                             | write a custom image recipe                                                                                                                                                                          |
| `.bbappend` version glob mismatch                                      | use the `%` wildcard                                                                                                                                                                                 |
| `FILESEXTRAPATHS:prepend` missing in a `.bbappend`                     | add `:prepend := "${THISDIR}/files:"`                                                                                                                                                                |
| suspected stale sstate after a `MACHINE`/patch/layer change            | those are hashed inputs and normally invalidate correctly — run `bitbake -S printdiff` / `bitbake-diffsigs` and fix the real input before cleaning                                                   |
| `DEPENDS` used for a runtime dep                                       | use `RDEPENDS:${PN}` — but a linked shared library needs neither, it is detected from ELF `NEEDED`                                                                                                   |
| build fails with `installed but not shipped`                           | `installed-vs-shipped` is in `ERROR_QA`, not `WARN_QA`: extend `FILES:<pkg>` or stop installing the paths it names; `INSANE_SKIP` hides the report and still ships the files nowhere                 |
| a linked library is "missing" on target                                | usually the package split, not a dependency — `PACKAGES` is matched in order with `${PN}` last, so `.so` goes to `-dev` and only `.so.*` to `${PN}`                                                  |
| `PACKAGECONFIG = "x"` in a `.bbappend`                                 | that declares the whole enabled set, silently disabling every other default feature; use `PACKAGECONFIG:append = " x"` with the leading space — and note a typo'd feature is only a `WARN_QA`        |
| `LAYERDEPENDS` naming a layer directory                                | it resolves against `BBFILE_COLLECTIONS`; use the collection name, or the layer reports as "not enabled" while sitting in `bblayers.conf`                                                            |
| artifacts "missing" because nothing is under `tmp/deploy`              | `TMPDIR` gains `-${TCLIBC}` outside Poky (`tmp-glibc/`) and `DEPLOY_DIR` is often moved out of it — resolve `bitbake-getvar TMPDIR` and `DEPLOY_DIR_IMAGE` before reporting an absence               |
| missing `LIC_FILES_CHKSUM`                                             | add it (or `LICENSE = "CLOSED"`) — see compliance ref                                                                                                                                                |
| `def` block in a `.conf` fails to parse                                | move it to a `.inc`; only BBHandler (`.bb`/`.bbclass`/`.inc`) accepts `def`, ConfHandler owns `.conf`                                                                                                |
| `#CONFIG_X is not set` in a kernel `.cfg` is ignored                   | needs the space — `# CONFIG_X is not set`; without it Kconfig reads a comment and the option keeps its defconfig value                                                                               |
| distro identity set before `require conf/distro/poky.conf` is lost     | poky assigns `DISTRO`/`DISTRO_NAME`/`DISTRO_VERSION` with hard `=`; set yours after the require                                                                                                      |
| `kernel-module-*` in `IMAGE_INSTALL` breaks when the symbol turns `=y` | built-in emits no module, so the package stops existing; drop it in the same change                                                                                                                  |
| dlopen'd plugin absent at runtime though its provider is installed     | plugins create no shared-library dependency, so nothing pulls them in; name the package explicitly                                                                                                   |
| `buildhistory` gives stale or mismatched answers                       | it keys on `MACHINE_ARCH` while deploy uses `MACHINE` (differ on hyphens) and keeps dirs for every image ever built — resolve `BUILDHISTORY_DIR_IMAGE` and check `build-id.txt`; never pick by mtime |
| `UNPACKDIR` undefined on Scarthgap and older                           | use `${WORKDIR}` for `file://` sources                                                                                                                                                               |
