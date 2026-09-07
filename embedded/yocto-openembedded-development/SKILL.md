---
name: yocto-openembedded-development
description: "Yocto Project and OpenEmbedded build partner — BitBake recipes (.bb/.bbappend/.bbclass), meta-layers and BSP layers, bblayers.conf/local.conf/site.conf, sstate-cache, DL_DIR, devtool, wic/.wks images, SDK (populate_sdk/populate_sdk_ext), and reproducible release prep. Use when a BitBake task fails (do_fetch/do_compile/do_package/do_rootfs), an override silently no-ops after a Kirkstone upgrade (`_append` vs `:append`), a `.bbappend` will not apply, sstate serves stale artifacts, `LIC_FILES_CHKSUM` mismatch fails do_populate_lic, you need SBOM/SPDX (`create-spdx`), CVE audit (`cve-check`), or license-compliance archives for a release. Route kas build orchestration (`.kas.yml`, `kas build`) to kas-build-orchestration; general board bring-up, device tree, drivers, and debugging to embedded-linux-bringup; Buildroot to buildroot-development; U-Boot to u-boot-development."
license: MIT
metadata:
  author: Joonas Onatsu
  tags:
    - yocto
    - openembedded
    - bitbake
    - poky
    - meta-layer
    - bsp
    - recipe
    - bbappend
    - bbclass
    - sstate
    - devtool
    - wic
    - sdk
    - sbom
    - spdx
    - cve-check
    - license-compliance
    - reproducible-builds
    - release-engineering
---

# Yocto / OpenEmbedded Development

**IRON LAW: Confirm the Yocto release codename BEFORE giving any syntax- or class-specific answer. Override syntax and
class names changed at Honister/Kirkstone (`_append` → `:append`, `_remove` → `:remove`); a pre-Kirkstone answer applied
to a Kirkstone+ tree is a SILENT no-op, and answering in the wrong era is the top error this skill makes. You MUST NOT
emit `_append`/`:append`, a class name, or a variable-behavior claim until the codename is known or explicitly assumed
and LABELLED.**

The same `IMAGE_INSTALL_append` line is correct on Dunfell and dead weight on Kirkstone. Pin the era first, then answer.

---

## Overview

Development partner for BitBake, the layer model, recipe and `.bbappend` authoring, sstate, `devtool`, SDK generation,
`wic` images, and reproducible release preparation. Keep this file for method, routing, and the version gate; pull
worked commands and detail from `references/` on demand — do NOT read every reference upfront.

Board-specific values (a concrete `MACHINE`, a real `.wks` layout) appear ONLY in `references/` worked examples. This
file stays board-agnostic.

**kas is a separate concern.** For build orchestration with `.kas.yml`, `kas build`, `kas-container`, and lockfiles,
route to **kas-build-orchestration**. Yocto builds run fine without kas; reach for kas-build-orchestration only when a
`.kas.yml` is in play.

### Route to a sibling skill

| Task                                                                     | Skill                       |
| ------------------------------------------------------------------------ | --------------------------- |
| kas orchestration (`.kas.yml`, `kas build/checkout/dump`, kas-container) | **kas-build-orchestration** |
| Board bring-up, device tree, driver probe, dmesg/boot debugging          | **embedded-linux-bringup**  |
| Buildroot: menuconfig, packages, `BR2_EXTERNAL`                          | **buildroot-development**   |
| U-Boot: env, extlinux, FIT, boot scripts, porting                        | **u-boot-development**      |

### Route the task to a reference

| Task / symptom                                                                                                                                     | Reference                            |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| Layer model, BitBake operators, task lifecycle, recipe anatomy, `.bbappend`, sstate mechanics, devtool, SDK, wic, offline builds, debugging a task | `references/yocto-workflow.md`       |
| Where a setting belongs, layer hygiene, release checklist, sstate sharing, CI, common traps                                                        | `references/yocto-best-practices.md` |
| SBOM/SPDX, `cve-check`, `LIC_FILES_CHKSUM`, archiver / copyleft source release                                                                     | `references/compliance-and-sbom.md`  |
| "Which manual, which section?" keyed to the release                                                                                                | `references/official-doc-map.md`     |

---

## Workflow

Tick each step per task. ⛔ BLOCKING MUST complete before the next; ⚠️ REQUIRED MUST be done but MAY interleave.

- [ ] **⛔ BLOCKING — Lock the release era.** Record the Yocto release codename and version (Scarthgap 5.0, Nanbield 4.3,
  Kirkstone 4.0, Dunfell 3.1, …), from `LAYERSERIES_COMPAT` in `layer.conf` or the poky checkout. This gates override
  syntax, class names, and variable behavior (Iron Law). If unknown, state the assumption and LABEL it.
- [ ] **⚠️ REQUIRED — Lock build context.** Record `MACHINE`, `DISTRO`, the active layer set (Poky only?
  meta-openembedded? custom BSP?), and the exact symptom: failing task, error line, or wrong variable value.
- [ ] **⚠️ REQUIRED — Classify the task.** Layer setup / recipe authoring / `.bbappend` override / build config /
  sstate-cache / devtool / image·wic / SDK / compliance·SBOM / release. One lane at a time.
- [ ] **⛔ BLOCKING — Collect evidence.** Gather the bounded artifacts in *Evidence First* below before ranking causes.
  No fix proposal until the failing task is evidenced.
- [ ] **⚠️ REQUIRED — Rank causes, validate ONE.** Propose the single most likely cause and ONE command or ONE file edit
  that confirms or refutes it. Stop at a checkpoint; request the result.
- [ ] **⚠️ REQUIRED — Confirm before mutating.** Any `cleansstate`/`cleanall`, sstate prune, or image write to
  `/dev/sdX` passes the *Confirmation gates* first.
- [ ] **⚠️ REQUIRED — Close with the Output contract.** Root cause → evidence → exact fix/command → validation command.

---

## Confirmation gates

You MUST stop and get explicit user confirmation before any destructive or irreversible action. Default to read-only;
pair every mutating command with its reverse or its cost.

- **Discarding cached build work** — `bitbake -c cleansstate <recipe>` and `bitbake -c cleanall <recipe>` delete the
  recipe's sstate (and `cleanall` its downloads too), forcing a from-scratch rebuild. Not data loss, but potentially
  hours of rebuild. Confirm the recipe and that a rebuild is intended; prefer scoping to one recipe over a global wipe.
- **Writing an image to a block device** — `bmaptool copy … /dev/sdX` and `dd … of=/dev/sdX` destroy whatever is on the
  target device. You MUST confirm the exact device path first; a wrong `/dev/sdX` overwrites the host disk. Verify with
  `lsblk` immediately before writing.
- **Pruning sstate** — `find ${SSTATE_DIR} … -atime +N -delete` and `sstate-cache-management.sh --remove-*` permanently
  remove cache entries. Confirm the cache directory and the age threshold; a mistyped path or `${SSTATE_DIR}` that
  expanded empty deletes from `/`.

### Safety

- MUST NOT run `cleansstate`, `cleanall`, or any sstate prune unprompted; each throws away reusable work or cache.
- MUST NOT issue a `dd`/`bmaptool` write to a device path the user has not confirmed this session. Re-confirm the path
  even if it was given earlier — devices renumber across replug.
- MUST NOT delete from `${SSTATE_DIR}` or `${DL_DIR}` without first echoing the expanded absolute path; never run a
  `find … -delete` whose base directory could be empty or `/`.
- Prefer reversible diagnostics first: `bitbake -e`/`bitbake-getvar` over editing config to "see what happens";
  `bitbake -c listtasks` over a speculative `cleansstate`.

---

## Evidence First

Before diagnosing, inspect (or ask for) the artifacts that pin the failing task:

- The exact BitBake error and the task log at `${WORKDIR}/temp/log.do_<task>` (path printed in the failure).
- The variable's real build-time value — `bitbake-getvar VAR` (shows every assignment and the final value) or
  `bitbake <recipe> -e | grep '^VAR='`.
- Which layer and which appends are in play — `bitbake-layers show-recipes | grep <recipe>` and
  `bitbake-layers show-appends | grep <recipe>`.
- The release and compatibility declaration — `LAYERSERIES_COMPAT` in each `layer.conf`.

Keep every capture BOUNDED — grep the log, do not paste a full build transcript.

```bash
# Release / layer sanity
bitbake-layers show-layers
grep -R LAYERSERIES_COMPAT */conf/layer.conf

# Final vs per-assignment variable value
bitbake-getvar IMAGE_INSTALL              # all assignments + final value
bitbake <recipe> -e | grep '^SRC_URI='    # value at build time for one recipe

# What provides / appends a recipe
bitbake-layers show-recipes | grep <recipe>
bitbake-layers show-appends | grep <recipe>

# Task-level introspection
bitbake -c listtasks <recipe>
bitbake -g <recipe> && grep <recipe> pn-buildlist   # dependency tree

# Package/file ownership (backfill)
oe-pkgdata-util find-path /usr/bin/foo    # which package ships a path
oe-pkgdata-util list-pkg-files <pkg>      # files in a built package
```

---

## Output contract

Every diagnostic answer MUST end with these four, in order:

1. **Root cause** — the single proven mechanism (task, variable, override era, layer).
2. **Supporting evidence** — the log line, `bitbake-getvar` output, or `layer.conf` value that proves it.
3. **Exact fix** — the precise recipe edit or command, with real variable and task names and the override syntax
   matching the confirmed release.
4. **Validation** — the command that confirms the fix (`bitbake-getvar`, a rebuilt task, a manifest check).

If the root cause is not yet proven, say so and give the ONE next command that would prove it — do NOT present a guess
as a diagnosis.

---

## Version awareness

BitBake and OE-Core syntax drift across releases. Before giving syntax-specific guidance you MUST confirm the release,
because:

- **Override separator changed at Kirkstone (4.0).** Pre-Honister used `_` (`SRC_URI_append`, `do_install_append`);
  Honister (3.4) accepted both `_` and `:`; Kirkstone dropped `_`. On Kirkstone+, an `_append` line does not error — it
  becomes an inert variable and silently does nothing. Match the confirmed era exactly.
- **Class names and infrastructure move.** Classes are renamed, split, or relocated to
  `classes-recipe/`/`classes-global/` across releases; `create-spdx` behavior and the SBOM format changed notably
  between Kirkstone, Nanbield, and Scarthgap. Confirm before naming a class or its inherit.
- **Variable semantics shift.** `WORKDIR` layout, `SRCPV`/`PV` handling, and default `INHERIT` sets differ by release.

When the release is unknown, give the answer per era (pre-Kirkstone `_` vs Kirkstone+ `:`) rather than assuming one, and
consult `references/official-doc-map.md` to read the version-matched manual.

---

## Anti-patterns

- MUST NOT emit `_append`/`_remove` (or `:append`/`:remove`) before the release era is known — the wrong separator is a
  silent no-op, not an error.
- MUST NOT use `+=` or `.=` in `local.conf`/`site.conf`; global-file parse order is undefined. Use `:append`/`:prepend`
  (release permitting).
- MUST NOT edit a core layer (`meta`, `meta-poky`, OE-Core, BitBake) to change behavior — upgrades wipe it silently.
  Override via a `.bbappend` in your own layer.
- MUST NOT ship `SRCREV = "${AUTOREV}"` in a release recipe — a floating HEAD is unreproducible and breaks air-gapped
  builds. Pin to a commit SHA.
- MUST NOT ship a product on the Poky distro or its default `PREMIRRORS` — see the Poky note in
  `references/yocto-best-practices.md`; create your own distro.
- MUST NOT rebuild "to fix it" without checking whether stale sstate is the cause; conversely MUST NOT run a global
  `cleansstate` when scoping to one recipe suffices.
- MUST NOT author a `.bbappend` without `FILESEXTRAPATHS:prepend` when it adds files — BitBake will not find them and
  `do_fetch` fails with a confusing "not found".
- MUST NOT declare a recipe's `LICENSE` without a matching `LIC_FILES_CHKSUM` (unless `LICENSE = "CLOSED"`) — a checksum
  mismatch fails `do_populate_lic`, and a wrong license silently corrupts the SBOM and CVE report.
- MUST NOT treat a green build as compliant — SBOM (`create-spdx`) and `cve-check` are separate gates; see
  `references/compliance-and-sbom.md`.
- MUST NOT judge a build by a piped command's status — `bitbake … | tail` exits with `tail`'s status, so a failed build
  reports success. Capture `$?` before any pipe, and confirm against an artifact (deployed file, `buildhistory`) rather
  than the log alone.
- MUST NOT interrupt a running `bitbake` to save time — a killed build can leave pseudo's inode database inconsistent,
  and the next task aborts with `path mismatch`, costing a `-c clean` and full rebuild of that recipe.

---

## Reference pointers

Cite the release-matched version of every manual (the codename is in the docs URL path):

- **docs.yoctoproject.org** — Reference Manual (variables, tasks, classes, QA error index), BitBake User Manual (syntax,
  operators, fetchers), BSP Developer's Guide, Kernel Development Manual, and the **Security manual** (CVE workflow).
  Read the **Migration Guides** for any release-to-release change (this is where the `_append`→`:append` and class moves
  are documented), and the "What I wish I'd known" material for hard-won gotchas.
- **dt-schema / `dt-validate`** — github.com/devicetree-org/dt-schema for device-tree binding validation; device-tree
  work itself routes to **embedded-linux-bringup**.

`references/`:

- `yocto-workflow.md` — layer model, BitBake assignment operators and override order, task lifecycle and dependency
  varflags, recipe anatomy and license/fetch/version fields, inline/anonymous Python, `.bbappend` + `FILESEXTRAPATHS`
  detail, sstate mechanics, devtool, SDK, kernel customization, buildhistory, offline builds, and task-failure debugging
  including `recipetool`/`oe-pkgdata-util`.
- `yocto-best-practices.md` — setting placement (where a variable belongs), layer hygiene, the Poky/production
  distinction, the release checklist, sstate sharing, CI patterns, wic + flashing safety, and a common-traps table.
- `compliance-and-sbom.md` — `create-spdx`/SPDX SBOM, `cve-check` and the security workflow, `LIC_FILES_CHKSUM`
  discipline, and the `archiver` class for copyleft source release.
- `official-doc-map.md` — problem type → exact manual and section, keyed to the release codename.

## Attribution

See `ATTRIBUTIONS.md` for the learning sources that informed this skill and the licensing note.
