---
name: buildroot-dev
description: "Buildroot build-system partner for embedded Linux — menuconfig/nconfig, defconfigs and `make savedefconfig`, `BR2_EXTERNAL` trees (`external.desc`/`Config.in`/`external.mk`), package authoring (generic-/cmake-/meson-/autotools-/python-package, kernel-module, host-* variants, `.mk` + `Config.in`), rootfs overlays, post-build/post-image scripts, genimage partition layout, internal vs external toolchains, `make sdk`, `make legal-info`, reproducible builds, and package build-failure triage. Use when a package will not build or rebuild, a `BR2_*` symbol is invisible or has unmet dependencies, a `.config` change vanished after `make clean`, an overlay file landed in the wrong path, an external toolchain is rejected, or you are standing up a board defconfig or SDK. For kernel/DTS/driver bring-up route to embedded-linux-dev, for U-Boot env/porting to uboot-dev, and for Yocto/OpenEmbedded/BitBake to yocto-oe-dev or kas-dev."
metadata:
  author: Joonas Onatsu
  license: MIT
  tags:
    - buildroot
    - embedded-linux
    - br2-external
    - menuconfig
    - defconfig
    - kconfig
    - cross-compilation
    - toolchain
    - genimage
    - rootfs
    - package-infrastructure
    - sdk
    - legal-info
    - reproducible-builds
---

# Buildroot Dev

**IRON LAW: Run `make savedefconfig` after EVERY `menuconfig`/`nconfig`/`xconfig` session, and `make linux-update-defconfig` (or `linux-update-config`) after every `make linux-menuconfig`. A raw `output/.config` is a build-tree scratchpad, NOT a persistable board config — it is discarded by `make clean`/`distclean` and cannot be committed as the board's source of truth. You MUST NOT hand back, commit, or call "done" a configuration that lives only in `.config`.**

The persistable artifact is the minimal defconfig (and the kernel/BusyBox/U-Boot config files it references), never the expanded `.config`. Save it, then diff it.

---

## Overview

Development partner for Buildroot configuration, package authoring, `BR2_EXTERNAL` trees, board support, toolchain selection, SDK generation, and release preparation. Keep this file for method, safety, and routing; pull worked commands and board examples from `references/` on demand — do NOT read every reference upfront.

Board-specific examples live ONLY in `references/`, as clearly-labeled worked cases. This file stays board-agnostic.

### Route sibling-domain work to another skill

| Task | Skill |
|------|-------|
| Kernel/DTS/driver bring-up, probe failures, `dmesg`, peripheral debug | **embedded-linux-dev** |
| U-Boot env, `extlinux`, FIT, boot scripts, porting, board defconfig | **uboot-dev** |
| Yocto/OpenEmbedded: recipes, layers, BitBake, sstate | **yocto-oe-dev** |
| kas build orchestration (`.kas.yml`, `kas build`) | **kas-dev** |

### Route the task to a reference

| Task | Reference |
|------|-----------|
| Package `.mk`/`Config.in`, infra type, fetch method, rebuild commands, deps | `references/buildroot-packages.md` |
| Board dir layout, defconfig, overlays, post-build/post-image, genimage, provenance | `references/buildroot-board-support.md` |
| `BR2_EXTERNAL`, external toolchain, CMake/Meson sysroot, SDK, legal-info, reproducibility | `references/buildroot-advanced.md` |
| Symbol invisible, "unmet dependencies", `select`/`imply` loop, Kconfig triage | `references/kconfig-troubleshooting.md` |

---

## Workflow

Tick each step per task. Steps marked ⛔ BLOCKING MUST complete before the next; ⚠️ REQUIRED MUST be done but MAY interleave.

- [ ] **⚠️ REQUIRED — Lock build context.** Record Buildroot version (`make --version` inside the tree, or `git describe`), `BR2_ARCH`, the active defconfig or `.config`, toolchain type (internal libc, or which external), the output directory (`O=`), and the exact symptom (failing package, error string, invisible symbol, wrong config value).
- [ ] **⛔ BLOCKING — Classify the lane.** Configuration, package authoring, `BR2_EXTERNAL`, board support, toolchain, out-of-tree cross-build, SDK, or release. Do NOT jump to a fix in a downstream lane while the failing lane is unproven.
- [ ] **⛔ BLOCKING — Collect evidence at that lane.** Gather the bounded artifacts in *Evidence First* before ranking causes. No fix proposal until the failure is evidenced by a log line, a `printvars` value, or a `-graph-depends`/`show-info` output.
- [ ] **⚠️ REQUIRED — Rank causes, validate ONE.** Propose the single most likely cause and ONE command or ONE edit that confirms or refutes it. Keep steps small; stop and request the result.
- [ ] **⚠️ REQUIRED — Persist config before mutating the tree.** Any `menuconfig`/`linux-menuconfig` change is saved (Iron Law) before you clean or hand off.
- [ ] **⚠️ REQUIRED — Confirm before destructive ops.** `make clean`/`distclean`/`<pkg>-dirclean` and external-toolchain path writes pass the *Confirmation gates* first.
- [ ] **⚠️ REQUIRED — Close with the Output contract.** Root cause → evidence → exact fix/command → validation command.

---

## Confirmation gates

You MUST stop and get explicit user confirmation before any command that discards build state or config. Default to read-only inspection; require an explicit opt-in to mutate; pair every mutating command with the work needed to recover from it.

- **`make distclean`** — deletes the entire `output/` tree INCLUDING `.config`. You MUST confirm `make savedefconfig` (and `linux-update-defconfig`) have run first; otherwise every unsaved menuconfig change is lost irrecoverably. Recover by re-loading `<board>_defconfig`.
- **`make clean`** — deletes `output/build`, `output/target`, `output/host`, `output/staging`, and images, but keeps `.config` and `output/dl` (downloads). Confirm before running; recovery is a full rebuild (long), not a data-loss event.
- **`make <pkg>-dirclean`** — removes one package's build directory and stamps; the next `make` re-fetches, re-configures, rebuilds, reinstalls it. Lower blast radius, but still confirm on a slow-to-build package (toolchain, gcc, qt).
- **External toolchain path / download dir writes** — confirm the exact path before any command that writes outside `output/`.

### Safety

- MUST NOT run `make clean`/`distclean`/`<pkg>-dirclean` unprompted to "get a clean slate" — a lost unsaved `.config` or a multi-hour rebuild is the cost.
- MUST NOT edit `output/.config` by hand as the deliverable — edit via `menuconfig` then `savedefconfig`, or edit the committed defconfig and reload it.
- MUST NOT hand-edit generated files under `output/` (the CMake toolchain file, the Meson cross file, `.br2-external.mk`) — they are regenerated and your edit vanishes.
- For U-Boot env, `extlinux.conf`, boot-flow, and FIT changes, route to **uboot-dev** and follow its safety contract; Buildroot only selects the U-Boot version and defconfig.

---

## Evidence First

Before diagnosing, inspect (or ask the user for) the artifacts that pin the failing lane. Keep every capture BOUNDED — `make foo 2>&1 | tail -40`, never a raw full build log.

- The exact failing line: `make <pkg> 2>&1 | tail -40`.
- The package build log and config: `ls output/build/<pkg>-<ver>/`, then `config.log` (autotools) or `CMakeFiles/CMakeError.log` (cmake).
- The effective value of a variable: `make -s printvars VARS=<PKG>_SITE` (accepts wildcards, e.g. `VARS='BUSYBOX_*'`).
- The dependency graph: `make <pkg>-graph-depends` or `make <pkg>-show-info` (JSON metadata).
- For an invisible/unset symbol: see `references/kconfig-troubleshooting.md`.

```bash
# What actually built and where it failed
make <pkg> 2>&1 | tail -40
ls output/build/<pkg>-<ver>/

# Drop into the exact build environment for a package
make <pkg>-shell

# Resolve a Buildroot/package variable (wildcards allowed)
make -s printvars VARS=<PKG>_SITE
make -s printvars VARS='<PKG>_*'

# Package metadata + dependency graph
make <pkg>-show-info
make <pkg>-graph-depends       # needs host graphviz; BR2_GRAPH_OUT=svg for SVG

# Confirm the persisted config matches the tree
make savedefconfig && git diff -- configs/<board>_defconfig
```

---

## Output contract

Every diagnostic answer MUST end with these four, in order:

1. **Root cause** — the single proven cause and mechanism (which lane, which symbol/variable/stamp).
2. **Supporting evidence** — the build-log line, `printvars` value, `graph-depends` edge, or Config.in dependency that proves it.
3. **Exact fix** — the precise command or the `.mk`/`Config.in`/defconfig edit (real variable names, real paths).
4. **Validation** — the command that confirms the fix (`make <pkg>-rebuild`, `make -s printvars …`, `make savedefconfig && git diff`).

If the cause is not yet proven, say so and give the ONE next command that would prove it — do NOT present a guess as a diagnosis.

---

## Version awareness

Buildroot ships an LTS release every year plus quarterly releases; Kconfig symbols, package infrastructure, and helper scripts drift across them. Before giving syntax-specific guidance you MUST confirm the release (`make --version` or `git describe` in the tree).

- **Kconfig symbols** are renamed and removed between releases — verify a `BR2_*` symbol exists in the target release before recommending it (`make menuconfig` search with `/`, or grep the release's `Config.in` files).
- **Package infrastructure** gains new types and setup backends over time (e.g. `python-package` `SETUP_TYPE` values, `golang-package`, `cargo-package`). Confirm the macro exists in the release.
- **Helper script paths** (`support/scripts/genimage.sh`, `utils/`) move; check the tree, do not assume.

When the release is unknown, state which answer applies per era rather than assuming one.

---

## Anti-patterns

- MUST NOT treat `output/.config` as the deliverable — it is not persisted (Iron Law). Save a minimal defconfig and commit that plus the referenced kernel/BusyBox/U-Boot config files.
- MUST NOT expect a config change to remove an already-installed package. Deselecting a package leaves its files in `output/target`; you MUST `make clean` (or `make <pkg>-dirclean`) and rebuild — through the *Confirmation gates*.
- MUST NOT rely on `make` alone after editing a package's source or `.mk` — stamp files mean an already-built package is skipped. Use `make <pkg>-rebuild` (re-configure+build+install) or `<pkg>-reinstall`, then `make` to regenerate the image.
- MUST NOT set `<PKG>_SITE_METHOD` to a made-up value like `https` — it is auto-detected from the site URL (`git://`/`.git` → git, `http(s)://`/`ftp://` → wget, `file://` → file); set it explicitly only to override, and only to a real method (`git`, `svn`, `hg`, `bzr`, `cvs`, `scp`, `file`, `local`, `wget`).
- MUST NOT assume a downstream package can link a library that is not staged — a library other packages link against MUST set `<PKG>_INSTALL_STAGING = YES` (headers + `.so` into `$(STAGING_DIR)`).
- MUST NOT reach for a "runtime dependency" / RDEPENDS variable — Buildroot has none. `<PKG>_DEPENDENCIES` is a build-ORDER list; because those deps are themselves target packages they are also installed to `$(TARGET_DIR)`. Runtime presence is governed by what is enabled in the config, via `Config.in` `depends on`/`select` — see `references/buildroot-packages.md`.
- MUST NOT chase a "silently unmet" `Config.in` dependency by eye — an option hidden by an unmet `depends on`, or force-enabled by a `select` that skips a `depends on`, is the usual cause. See `references/kconfig-troubleshooting.md`.
- MUST NOT mismatch external-toolchain libc with `BR2_TOOLCHAIN_*_LIBC` — a glibc external toolchain cannot back a musl/uClibc target; Buildroot validates declared features and errors at configure time.
- MUST NOT drop a rootfs-overlay file at a path missing its leading `/` structure — overlay paths mirror the absolute target path exactly (`overlay/etc/foo` → `/etc/foo`).

---

## Reference pointers

Canonical upstream docs (cite the release-matched version):

- Buildroot manual: buildroot.org/downloads/manual/manual.html (also `make manual` in-tree). It is the authority for package infrastructure variables and `BR2_EXTERNAL` layout.
- External toolchains: toolchains.bootlin.com. Community knowledge base: elinux.org.
- genimage: github.com/pengutronix/genimage. Its config syntax is not Buildroot-specific.

`references/`:

- `buildroot-packages.md` — package infrastructure types (generic/cmake/meson/autotools/python/kernel-module, host-* variants), `Config.in` structure, key `.mk` variables, fetch methods, staging vs target install, rebuild commands, host and build-order dependencies, and package-failure debugging.
- `buildroot-board-support.md` — board directory layout, defconfig structure, rootfs overlays, post-build/post-image scripts, build-provenance logging, genimage partition layout, device/permission tables, init-system selection, and kernel config persistence.
- `buildroot-advanced.md` — `BR2_EXTERNAL` (single and multi-tree), external toolchains, out-of-tree CMake/Meson against the staging sysroot, `pkg-config` sysroot, SDK generation and `environment-setup`, `make legal-info`, reproducible builds, dependency graphs, out-of-tree `O=` builds, and ccache.
- `kconfig-troubleshooting.md` — reading `make menuconfig` search, `depends on` vs `select` vs `imply` semantics, why a symbol is invisible, "unmet direct dependencies" from an unguarded `select`, and dependency-loop diagnosis.
