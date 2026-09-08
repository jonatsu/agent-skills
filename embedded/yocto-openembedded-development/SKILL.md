---
name: yocto-openembedded-development
description: "Yocto/OpenEmbedded build partner: BitBake recipes (.bb/.bbappend/.bbclass), meta-layers, bblayers.conf/local.conf, sstate, devtool, wic images, SDKs, and reproducible release prep. Use when a BitBake task fails (do_fetch/do_compile/do_package/do_rootfs), packaging QA fails (installed but not shipped), an override stops applying after a release upgrade (`_append` vs `:append`), a `.bbappend` has no effect, sstate serves stale artifacts, or a release needs SBOM/SPDX, cve-check or license archives. Route kas configs to kas-build-orchestration, and kernel, board or driver debugging to embedded-linux-bringup."
license: MIT
compatibility: Requires a BitBake/OE-Core checkout and a Linux host meeting that release's build prerequisites. Commands assume an initialised build directory (`oe-init-build-env`); `devtool deploy-target` additionally needs SSH access to a running target. Class names, variables and override syntax are release-specific.
metadata:
  author: Joonas Onatsu
---

# Yocto / OpenEmbedded Development

**IRON LAW: Confirm the release era from the actual checkout BEFORE giving any syntax- or class-specific answer.
Override syntax changed at Honister 3.4 (`_append` → `:append`, `_remove` → `:remove`), and the two directions fail
differently. You MUST NOT emit `_append`/`:append`, a class name, or a variable-behavior claim until the era is known or
explicitly assumed and LABELLED.**

The two failure directions are not symmetric, and the asymmetry decides how you diagnose:

- **Old syntax on a Honister-or-newer tree fails loudly.** BitBake raises a fatal error naming the variable, the file
  and the line — `Variable %s contains an operation using the old override syntax`. It is not a silent no-op.
- **New syntax on a pre-Honister tree is the silent one.** There `:` is not an override separator, so
  `IMAGE_INSTALL:append` parses as an ordinary, inert variable name and quietly does nothing.

So `IMAGE_INSTALL_append` is correct on Dunfell and a hard parse failure on Kirkstone, while `IMAGE_INSTALL:append` is
correct on Kirkstone and silently dead on Dunfell. Pin the era first, then answer.

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

| Task / symptom                                                                                                                                                                                      | Reference                            |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| Layer model, BitBake operators, task lifecycle, recipe anatomy, packaging (`PACKAGES`/`FILES`, `PACKAGECONFIG`), `.bbappend`, sstate mechanics, devtool, SDK, wic, offline builds, debugging a task | `references/yocto-workflow.md`       |
| Where a setting belongs, layer hygiene, release checklist, sstate sharing, CI, common traps                                                                                                         | `references/yocto-best-practices.md` |
| SBOM/SPDX, `cve-check`, `LIC_FILES_CHKSUM`, archiver / copyleft source release                                                                                                                      | `references/compliance-and-sbom.md`  |
| "Which manual, which section?" keyed to the release                                                                                                                                                 | `references/official-doc-map.md`     |

---

## Workflow

Two shared steps, then branch by what the task actually is. ⛔ BLOCKING MUST complete before the next; ⚠️ REQUIRED MUST
be done but MAY interleave.

**Shared entry (both lanes):**

- [ ] **⛔ BLOCKING — Lock the release era.** Establish the *actual* BitBake/OE-Core revision in use: the poky checkout's
  tag or branch (`git -C <poky> describe --tags`), or `DISTRO_VERSION`/`poky.conf`. `LAYERSERIES_COMPAT` is a
  *compatibility declaration* — a layer may legitimately list several codenames — so read it as "which releases this
  layer claims to support", never as proof of which release is checked out. This gates override syntax, class names and
  variable behavior (Iron Law). If it cannot be established, state the assumed era and LABEL the assumption.
- [ ] **⚠️ REQUIRED — Lock build context.** Record `MACHINE`, `DISTRO`, and the active layer set (Poky only?
  meta-openembedded? custom BSP?).

**Authoring lane** — new recipe, new layer, `.bbappend`, image or SDK config, compliance wiring:

- [ ] **⚠️ REQUIRED — State the target and its placement.** What is being added, and which file owns it per *Where Does
  a Setting Belong?* in `references/yocto-best-practices.md`.
- [ ] **⚠️ REQUIRED — Write it, then name its validation.** Produce the recipe, append or config, and give the command
  that would prove it works (`bitbake-getvar`, `bitbake -c <task>`, `bitbake-layers show-appends`). A failing build is
  not a prerequisite for authoring — do not manufacture one.
- [ ] **⚠️ REQUIRED — Run the already-authorized local checks** rather than stopping to ask after each one. Parse and
  variable-inspection commands are read-only; batch them and report the results together.

**Diagnosis lane** — a task fails, a variable holds the wrong value, or an override does not apply:

- [ ] **⛔ BLOCKING — Collect evidence.** Gather the bounded artifacts in *Evidence First* below before ranking causes.
  No fix proposal until the failing task is evidenced.
- [ ] **⚠️ REQUIRED — Rank causes, validate the top one.** Propose the most likely cause and the command or file edit
  that confirms or refutes it. Read-only checks you can already run, run — reserve a checkpoint for a result only you
  cannot obtain (target access, a long build, a mutating command).
- [ ] **⚠️ REQUIRED — Close with the Output contract.** Root cause → evidence → exact fix/command → validation command.

**Both lanes:**

- [ ] **⚠️ REQUIRED — Confirm before mutating.** Any `cleansstate`/`cleanall`, sstate prune, target deploy, or image
  write to `/dev/sdX` passes the *Confirmation gates* first.
- [ ] **⚠️ REQUIRED — Honor a stop request.** If the user asks to stop, stop. See the pseudo note under *Anti-patterns*
  for what interrupting BitBake actually costs.

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
- **Writing to a live target** — `devtool deploy-target` opens an SSH session to a running board and installs the
  recipe's `do_install` output onto it. Local `devtool add`/`modify`/`build`/`finish` touch nothing outside the build
  directory and need no gate; `deploy-target` mutates the board and does. Confirm the target identity, and reuse an
  authorization the user already gave for that board rather than re-asking each invocation. See the devtool section of
  `references/yocto-workflow.md` for what it does and does not deploy.

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
- The actual release, plus each layer's compatibility claim — the poky checkout's tag or branch for the former,
  `LAYERSERIES_COMPAT` in each `layer.conf` for the latter. When they disagree, that mismatch is often the bug.

Keep every capture BOUNDED — grep the log, do not paste a full build transcript.

```bash
# Release / layer sanity
git -C <poky> describe --tags            # what is actually checked out
bitbake-getvar DISTRO_VERSION            # the distro's own release identity
bitbake-layers show-layers
grep -R LAYERSERIES_COMPAT */conf/layer.conf   # what each layer CLAIMS to support

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

- **Override separator changed at Honister (3.4), not Kirkstone.** Pre-Honister used `_` (`SRC_URI_append`,
  `do_install_append`); Honister introduced `:` and shipped `convert-overrides.py` to migrate metadata. From Honister
  onward BitBake *rejects* the old operation syntax: `setVar` raises `bb.fatal` naming the variable, file and line when
  the name contains `_append`, `_prepend` or `_remove`. Match the confirmed era exactly.

  Two consequences worth keeping straight. First, the check is a **substring match on the variable name**, so ordinary
  underscores are untouched — `SRC_URI`, `IMAGE_INSTALL` and `PACKAGE_ARCH` are all fine; only a name containing one of
  those three operation substrings trips it. Second, the error is loud in that direction and silent in the other: see
  the Iron Law.

- **Class names and infrastructure move.** Classes are renamed, split, or relocated to
  `classes-recipe/`/`classes-global/` across releases; `create-spdx` behavior and the SBOM format changed notably
  between Kirkstone, Nanbield, and Scarthgap. Confirm before naming a class or its inherit.

- **Variable semantics shift.** `WORKDIR` layout, `SRCPV`/`PV` handling, and default `INHERIT` sets differ by release.

When the release is unknown, give the answer per era (pre-Honister `_` vs Honister-and-newer `:`) rather than assuming
one, and consult `references/official-doc-map.md` to read the version-matched manual.

---

## Anti-patterns

- MUST NOT emit `_append`/`_remove` (or `:append`/`:remove`) before the release era is known — old syntax on a modern
  tree is a fatal parse error, new syntax on a pre-Honister tree is a silent no-op.
- MUST NOT reach for `+=`/`.=` in `local.conf`/`site.conf` **when a later file may hard-assign the same variable**.
  Global parse order is defined, not undefined (`bitbake.conf` requires and includes `site.conf`, `auto.conf`,
  `local.conf`, then machine, then distro), and that order is exactly the problem: `local.conf` is read *before* the
  machine and distro configs, so a `VAR = "…"` in either overwrites a `VAR += "…"` you wrote earlier. `:append` is
  applied at expansion time, after all parsing, so it survives. `+=` in `local.conf` is legitimate and common for
  variables nothing downstream reassigns — prefer `:append` for anything a machine or distro conf also touches, and do
  not rewrite a working `+=` for its own sake.
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
- MUST NOT add `INSANE_SKIP` (or move a check out of `ERROR_QA`) to clear a packaging failure before the named paths
  are explained. Silencing `installed-vs-shipped` does not package anything — the files ship in nothing and vanish from
  the image, so the build goes green while the defect gets worse.
- MUST NOT treat a green build as compliant — SBOM (`create-spdx`) and `cve-check` are separate gates; see
  `references/compliance-and-sbom.md`.
- MUST NOT judge a build by a piped command's status — `bitbake … | tail` exits with `tail`'s status, so a failed build
  reports success. Capture `$?` before any pipe, and confirm against an artifact (deployed file, `buildhistory`) rather
  than the log alone.
- MUST NOT reach for a forced kill (`SIGKILL`, a second Ctrl-C) as the ordinary way to stop a build. BitBake has two
  distinct stop levels: the first Ctrl-C requests `stateShutdown`, which starts no new tasks and lets running ones
  finish cleanly; a second requests `stateForceShutdown`, which interrupts tasks mid-flight. Only the forced path risks
  leaving pseudo's inode database inconsistent, and even then diagnose the actual error — a later `path mismatch` is
  evidence for that story, not a foregone conclusion of any cancellation. **A user asking to stop is authorization to
  stop:** issue the graceful stop and say what it costs, rather than refusing or continuing.

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
  varflags, recipe anatomy and license/fetch/version fields, packaging (`PACKAGES`/`FILES` splits,
  installed-vs-shipped, `PACKAGECONFIG`), inline/anonymous Python, `.bbappend` + `FILESEXTRAPATHS` detail, sstate
  mechanics,
  devtool, SDK, kernel customization, buildhistory, offline builds, and task-failure debugging including
  `recipetool`/`oe-pkgdata-util`.
- `yocto-best-practices.md` — setting placement (where a variable belongs), layer hygiene, the Poky/production
  distinction, the release checklist, sstate sharing, CI patterns, wic + flashing safety, and a common-traps table.
- `compliance-and-sbom.md` — `create-spdx`/SPDX SBOM, `cve-check` and the security workflow, `LIC_FILES_CHKSUM`
  discipline, and the `archiver` class for copyleft source release.
- `official-doc-map.md` — problem type → exact manual and section, keyed to the release codename.

## Attribution

See `ATTRIBUTIONS.md` for the sources behind this skill. It records an **open licensing question**: a 2026-09-07
investigation established `references/yocto-best-practices.md` as a structural adaptation of a CC BY-SA 3.0 Bootlin
source, which is unresolved against the MIT declaration above. Read it before redistributing this package or relying
on that license field.
