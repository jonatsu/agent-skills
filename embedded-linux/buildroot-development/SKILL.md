---
name: buildroot-development
description: "Develop and troubleshoot embedded Linux systems with Buildroot. Use for defconfigs, BR2_EXTERNAL trees, package .mk/Config.in authoring, toolchains, rootfs overlays, genimage layouts, SDKs, legal-info, reproducible builds, and package or configuration failures. Covers Buildroot integration; use embedded-linux-bringup for runtime kernel/device debugging and u-boot-development for bootloader internals."
license: MIT
compatibility: "Execution requires a Linux host with the selected Buildroot release's build prerequisites. Hook examples use Bash and GNU utilities. Image assembly, SDK, and graph workflows require their corresponding host tools; check availability before use."
metadata:
  author: Joonas Onatsu
---

# Buildroot Development

Produce a persistable configuration and verify the artifacts the user will actually use. Keep package source changes
outside disposable build directories. Choose the smallest rebuild that applies the change; package removal needs a
fresh/full build, because Buildroot does not provide per-package uninstall.

## Establish the Build Context

Identify the Buildroot source, release, output directory, configuration, external trees, and intended result before
editing. Record the architecture and toolchain when they affect the task. Do not infer Buildroot's release from
`make --version`: that reports GNU Make. Inspect the release's `Makefile` or query the configured build:

```bash
make -s printvars VARS='BR2_VERSION BR2_CONFIG CONFIG_DIR BASE_DIR BR2_DEFCONFIG'
```

Run examples below in the selected build context: use the generated output-directory Makefile for an existing `O=`
build, or retain `-C <source> O=<output>` consistently. `BR2_CONFIG` names the active configuration; it is not always
`output/.config`. `CONFIG_DIR` also owns the default `local.mk` override file. Resolve paths before using examples.

Use the target release's manual, configuration symbols, package infrastructure, and `make help` as the primary
references. Third-party recipes can suggest cases, but verify their commands and distinguish wrapper behavior from
native Buildroot. When documentation and code disagree, report the documented contract and verify actual behavior
against that release; do not convert an untested assumption into a requirement.

## Choose the Task

- **Author or change a package/board:** inspect existing project conventions, select the appropriate package
  infrastructure or configuration mechanism, and implement the requested behavior. A new feature does not require
  a pre-existing failure log.
- **Diagnose a failure:** identify the failing stage, collect the relevant log and effective values, then test the
  most likely explanation. Run available checks yourself; ask for results only when the target or evidence is inaccessible.
- **Prepare an SDK or release:** verify persisted inputs, source revisions, expected artifacts, and reproducibility
  or license-evidence requirements. A successful package build alone does not prove the final image is current.

Reuse the user's existing authorization. Ask before discarding unpreserved changes, accepting an uncovered expensive
rebuild, or writing to an unauthorized destination. Ordinary authorized edits to defconfigs, external trees, and board
files do not need a second approval because they live outside the output directory.

## Select the Reference

| Task                                                                                                   | Reference                                                        |
| ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Package infrastructure, fetch inputs, dependencies, local-source iteration, rebuild selection          | [Package infrastructure](references/buildroot-packages.md)       |
| Board configuration, overlays, hooks, image assembly/capacity, provenance, kernel config persistence   | [Board support](references/buildroot-board-support.md)           |
| External trees, external toolchains, out-of-tree application builds, SDKs, legal-info, reproducibility | [Advanced topics](references/buildroot-advanced.md)              |
| Hidden symbols, unmet dependencies, conditional selection, configuration cycles                        | [Kconfig troubleshooting](references/kconfig-troubleshooting.md) |

Keep Buildroot's integration of the kernel and bootloader here. Route runtime driver/DTS work to
`embedded-linux-bringup`, bootloader implementation and console behavior to `u-boot-development`, Yocto/BitBake to
`yocto-openembedded-development`, and kas orchestration to `kas-build-orchestration`.

## Diagnose Without Hiding Failures

Start with an existing log. Reproducing a build may download, compile, and change output; establish that it is appropriate
before running it. Retain the full log locally and show only the relevant excerpt. This Bash example preserves make's
status while keeping displayed output bounded; replace the package name and use a fresh task-specific log path.

```bash
(
  log_file=$(mktemp "${TMPDIR:-/tmp}/buildroot-build.XXXXXX") || exit 1
  status=0
  make V=1 mypkg >"$log_file" 2>&1 || status=$?
  tail -n 40 -- "$log_file"
  printf 'Full build log: %s\n' "$log_file"
  exit "$status"
)
```

Query exact variables or Make `%` patterns, not shell `*` patterns:

```bash
make -s printvars VARS='BUSYBOX_SITE BUSYBOX_SITE_METHOD BUSYBOX_VERSION'
make -s printvars VARS='BUSYBOX_%DEPENDENCIES'
make busybox-show-info
```

For a failing configure/build command, inspect the package log and generated build files. Use `make V=1` to see the
actual invocation and reproduce it only with its environment and working directory understood. Do not invent
`<pkg>-shell` or `<pkg>-list-targets`; use the release's documented targets.

## Preserve Inputs and Verify Completion

Save intentional configuration changes to an explicit project-owned destination, then inspect that file's diff:

```bash
make savedefconfig BR2_DEFCONFIG=/absolute/path/to/project/configs/myboard_defconfig
```

Kernel and other component configurations have their own persistence rules; follow the reference for custom configs,
named defconfigs, and fragments. Do not overwrite an upstream config merely because an example used its path.

Before cleanup, inspect the selected release's rules and resolve their affected paths:

- `clean` removes build products, including package build directories, host/target/staging trees and images, while
  retaining the top-level configuration. Preserve edits made inside package build directories first.
- `distclean` also removes configuration state and can remove the source-tree `dl/` directory. Do not describe it as
  output-only cleanup; inspect overrides, shared caches, and any symlinked locations before executing.
- `<pkg>-dirclean` removes that package's build directory, not its installed files or cached source downloads.

Leave generated output as output: edit its owning configuration or source instead of generated toolchain files or
`.br2-external.mk`. Check which kernel/rootfs image the runner or deployment step consumes. Inspect the final image for
changed or removed files and unintended overlay replacements. Explain what changed, what evidence establishes the
result, and what remains unverified; identify a proven cause only when the evidence supports it.

## Sources

Use the [Buildroot manual](https://buildroot.org/downloads/manual/manual.html) for orientation and the manual bundled
with the selected release for version-specific details. Genimage's [upstream documentation](https://github.com/pengutronix/genimage)
owns image-layout syntax. [Attributions](ATTRIBUTIONS.md) records source influence and the repair's provenance.
