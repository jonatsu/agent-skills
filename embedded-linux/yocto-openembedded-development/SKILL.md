---
name: yocto-openembedded-development
description: "Build and troubleshoot Yocto and OpenEmbedded images with BitBake. Use for writing recipes, bbappends, layers, and image or distro configuration; a failed BitBake task or packaging QA error; overrides that stop applying after a release upgrade; suspected stale sstate; devtool, SDKs, and wic; and pinned, offline-capable releases with licence manifests and copyleft sources. Route kas to kas-build-orchestration, on-target debugging to embedded-linux-debugging, CVEs or SBOMs to yocto-vulnerability-management."
license: MIT
compatibility: Requires a BitBake/OE-Core checkout and a Linux host meeting that release's build prerequisites. Commands assume an initialised build directory (`oe-init-build-env`); `devtool deploy-target` additionally needs SSH access to a running target. Class names, variables and override syntax are release-specific.
metadata:
  author: Joonas Onatsu
---

# Yocto / OpenEmbedded Development

Establish the release from the checkout before giving any syntax, class, or variable answer. Override syntax, source
directories, configuration files, and several defaults differ by release; *Version awareness* lists the changes
that decide answers most often. When the release cannot be established, answer for each era and label the
assumption.

## Route to a sibling skill

| Task                                                                     | Skill                              |
| ------------------------------------------------------------------------ | ---------------------------------- |
| kas orchestration (`.kas.yml`, `kas build/checkout/dump`, kas-container) | **kas-build-orchestration**        |
| Board bring-up, device tree, driver probe, dmesg/boot debugging          | **embedded-linux-bringup**         |
| gdbserver, tracing, profiling, kernel oops, Yocto debug symbols          | **embedded-linux-debugging**       |
| Buildroot: menuconfig, packages, `BR2_EXTERNAL`                          | **buildroot-development**          |
| U-Boot: env, extlinux, FIT, boot scripts, porting                        | **u-boot-development**             |
| CVE scanning and triage, SBOM/SPDX generation, VEX, release CVE gates    | **yocto-vulnerability-management** |
| Configuring a security control and proving it on the artefact            | **yocto-security-hardening**       |
| Auditing what a built image actually ships for security defects          | **yocto-security-audit**           |

## Route the task to a reference

| Task / symptom                                                                                                                                                                                      | Reference                                |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| Layer model, BitBake operators, task lifecycle, recipe anatomy, packaging (`PACKAGES`/`FILES`, `PACKAGECONFIG`), `.bbappend`, sstate mechanics, devtool, SDK, wic, offline builds, debugging a task | `references/yocto-workflow.md`           |
| Where a setting belongs, layer hygiene, release checklist, sstate sharing, CI, common traps                                                                                                         | `references/yocto-best-practices.md`     |
| `LIC_FILES_CHKSUM`, licence manifest, on-target licence texts, archiver / copyleft source release                                                                                                   | `references/compliance-and-licensing.md` |
| "Which manual, which section?" keyed to the release                                                                                                                                                 | `references/official-doc-map.md`         |

## Workflow

Do the two entry steps, then follow the lane that matches the task.

1. **Lock the release.** Read the OE-Core checkout's tag with `git -C <oe-core-checkout> describe --tags`, whatever
   the directory is called, or read `bitbake-getvar DISTRO_VERSION`. Treat `LAYERSERIES_COMPAT` as the releases a
   layer claims, not as the release checked out.
2. **Lock the build context.** Record `MACHINE`, the `DISTRO` that `bitbake-getvar DISTRO` reports, and the active
   layers from `bitbake-layers show-layers`.

**Authoring lane** (a new recipe, layer, `.bbappend`, image, SDK, or compliance setting):

3. Name the file that owns the change, using *Where Does a Setting Belong?* in `references/yocto-best-practices.md`.
4. Write the change, then give the command that proves it, such as `bitbake-getvar`, `bitbake -c <task>`, or
   `bitbake-layers show-appends <recipe>`. Run read-only parse and variable checks yourself, and report the results
   together.

**Diagnosis lane** (a failed task, a wrong variable value, or an override that does not apply):

3. Collect the artifacts in *Evidence First*. Propose a cause only after the failing task is evidenced.
4. Rank the causes, and run the read-only check that confirms or refutes the top one. Ask the user only for a result
   you cannot obtain yourself, such as target access or a long build.
5. Close with the *Output contract*.

Any mutating command in either lane passes the *Confirmation gates* first.

## Confirmation gates

Prefer read-only diagnostics, such as `bitbake-getvar` and `bitbake -c listtasks`, before any change. Get the user's
confirmation before each action below, and state its cost or how to reverse it.

- **Discarding cached work.** `bitbake -c cleansstate <recipe>` deletes the recipe's local sstate, and `cleanall`
  also deletes its downloads. Either forces a rebuild that can take hours. Confirm the recipe, and scope the clean to
  one recipe.
- **Pruning sstate or downloads.** Expand `${SSTATE_DIR}` or `${DL_DIR}` to an absolute path and show it first. Run
  a `find … -delete` only when its base directory cannot expand to empty or to `/`.
- **Writing an image to a block device.** `bmaptool copy` and `dd` destroy the device's contents. Run `lsblk`
  immediately before writing, and confirm the exact path in this session, because devices renumber across replug.
- **Writing to a live target.** `devtool deploy-target` installs the recipe's output onto a running board over SSH.
  Confirm the target identity, and reuse an authorization the user already gave for that board. Local `devtool add`,
  `modify`, `build`, and `finish` stay inside the build directory and need no gate.

## Evidence First

Before diagnosing, inspect (or ask for) the artifacts that pin the failing task:

- The exact BitBake error and the task log at `${WORKDIR}/temp/log.do_<task>` (path printed in the failure).
- The variable's real build-time value: `bitbake-getvar -r <recipe> VAR` shows every assignment and the final value.
- Which layer provides the recipe and which appends apply: `bitbake-layers show-recipes <recipe>` and
  `bitbake-layers show-appends <recipe>`.
- The release and each layer's compatibility claim: the OE-Core checkout's tag, and `LAYERSERIES_COMPAT` in each
  active layer's `layer.conf`. A mismatch between them is often the bug.

Keep every capture bounded: grep the log rather than pasting a full build transcript.

```bash
# Release and layer sanity
git -C <oe-core-checkout> describe --tags   # the release actually checked out
bitbake-getvar DISTRO                       # the selected distro; "nodistro" if none
bitbake-getvar DISTRO_VERSION               # the distro's own release identity
bitbake-layers show-layers
for l in $(bitbake-getvar --value --quiet BBLAYERS); do grep -H LAYERSERIES_COMPAT "$l/conf/layer.conf"; done

# Final value and every assignment site
bitbake-getvar -r <recipe> SRC_URI
bitbake -e <recipe> | grep '^SRC_URI='      # where bitbake-getvar is unavailable

# Which layer provides a recipe, and which appends apply
bitbake-layers show-recipes <recipe>
bitbake-layers show-appends <recipe>

# Tasks and dependencies
bitbake -c listtasks <recipe>
bitbake -g <image> && oe-depends-dot -k <recipe> -w task-depends.dot   # why <recipe> is in the build

# Package and file ownership
oe-pkgdata-util find-path /usr/bin/foo      # which package ships a path
oe-pkgdata-util list-pkg-files <pkg>        # files in a built package
```

## Output contract

Every diagnostic answer ends with these four, in order:

1. **Root cause**: the single proven mechanism (task, variable, override era, layer).
2. **Supporting evidence**: the log line, `bitbake-getvar` output, or `layer.conf` value that proves it.
3. **Exact fix**: the precise recipe edit or command, with real variable and task names and the override syntax
   matching the confirmed release.
4. **Validation**: the command that confirms the fix (`bitbake-getvar`, a rebuilt task, a manifest check).

When the root cause is not yet proven, say so and give the one next command that would prove it.

## Version awareness

These release changes decide answers most often. Read the release's migration guide for anything else.

- **Override syntax, Honister (3.4).** Before 3.4 the operators are `_append`, `_prepend`, and `_remove`. From 3.4
  they are `:append`, `:prepend`, and `:remove`. BitBake then stops with a fatal error naming any variable whose name
  contains an old operator; ordinary names such as `SRC_URI` are unaffected. In the other direction,
  `IMAGE_INSTALL:append` on a pre-3.4 tree parses as an unrelated variable and silently does nothing.
- **Source directory, 5.1 and 5.3.** At 5.0 a Git recipe sets `S = "${WORKDIR}/git"`. At 5.1 and 5.2 sources unpack
  into `UNPACKDIR`, and that assignment still works through a compatibility move. From 5.3 the default
  `S = "${UNPACKDIR}/${BP}"` covers Git sources, and `S = "${WORKDIR}/git"` is a fatal QA error.
- **Global configuration, 5.2 and 5.3.** Configuration fragments (`OE_FRAGMENTS`) arrive at 5.2 and `toolcfg.conf`
  at 5.3, and both change the parse order (`references/yocto-best-practices.md`).
- **Image features, 5.2.** `debug-tweaks` is gone; name the features it implied (`references/yocto-workflow.md`).
- **wic, 5.3.** Source plugin names use underscores, so `bootimg-partition` becomes `bootimg_partition`.
- **Setup, 5.3.** `bitbake-setup` exists from 5.3; older trees use `oe-init-build-env` or kas.
- **Classes** move between `classes/`, `classes-recipe/`, and `classes-global/`, and some are renamed or removed.
  Check the release's Classes chapter before naming an `inherit`.

When the release is unknown, give the answer for each era and label the assumption.

## Defaults

- Customize through a `.bbappend` or your own layer, and leave BitBake, OE-Core, and `meta-poky` unmodified, because
  an upgrade replaces them.
- Pin every release recipe's `SRCREV` to a commit SHA.
- Ship a product on your own distro configuration; Poky is a reference distribution
  (`references/yocto-best-practices.md`).
- Explain each path a packaging QA error names before adding `INSANE_SKIP` or moving a check out of `ERROR_QA`. A
  skip packages nothing, so the files vanish from the image.
- Report a green build as one gate passed. Licence obligations (`references/compliance-and-licensing.md`) and CVE or
  SBOM reporting (**yocto-vulnerability-management**) are separate gates.
- Judge a build by BitBake's own exit status and by an artifact, such as a deployed file or `buildhistory`. A pipe
  such as `bitbake … | tail` returns the status of `tail`.
- Use `:append` in `local.conf` for a variable that a machine or distro configuration also assigns. Keep `+=` for
  variables nothing later reassigns (`references/yocto-workflow.md`).
- Stop a build with one Ctrl-C when the user asks to stop. BitBake then starts no new tasks and lets running tasks
  finish. A second Ctrl-C interrupts running tasks and can leave pseudo's database inconsistent.

## Upstream documentation

Cite the manual that matches the release; the codename is a path segment in each docs.yoctoproject.org URL.
`references/official-doc-map.md` maps a problem type to the manual and section.

## Attribution

See `ATTRIBUTIONS.md` for the sources this skill is based on.
