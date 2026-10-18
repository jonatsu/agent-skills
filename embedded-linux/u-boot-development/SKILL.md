---
name: u-boot-development
description: "Develop and debug the U-Boot bootloader: board ports, SPL sizing, environment persistence, boot scripts, extlinux and bootstd, FIT signatures, driver model, A/B boot counting, and build provenance. Use when saveenv or fw_setenv changes do not persist, a boot script is never read, a FIT is rejected, SPL overflows, or a bootcmd change loses the console. Route U-Boot GDB sessions to embedded-linux-debugging, kernel boot failures to embedded-linux-bringup, and build recipes to Buildroot, Yocto, or kas skills."
license: MIT
compatibility: Requires release-matched U-Boot source and build tools; target access is task-specific. The provenance helper requires Bash 4+, Git, and GNU coreutils on Linux.
metadata:
  author: Joonas Onatsu
---

# U-Boot Development

Develop the bootloader stages and their handoff to Linux. Before changing environment or boot flow, establish the
board, U-Boot revision, boot medium, and active configuration. A working recovery procedure must restore the intended
state, including persistent storage when required; compiled defaults are not a backup.

The technical reference baseline is upstream **v2025.10**. Check the project's actual release and vendor changes before
applying a command or configuration symbol. Read the relevant reference when entering its branch.

## Routing

| Task                                                                  | Reference                                                              |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Environment defaults, backups, persistence, bootcount                 | [Environment](references/uboot-environment.md)                         |
| Boot selection, scripts, image formats, FIT creation, network loading | [Boot scripts](references/uboot-boot-scripts.md)                       |
| Board port, DT source, driver model, SPL memory, A/B integration      | [Porting](references/uboot-porting.md)                                 |
| Signature enforcement, shell access, SoC lifecycle, artifact identity | [Security and provenance](references/uboot-security-and-provenance.md) |

Use **embedded-linux-bringup** for the kernel's device tree, runtime drivers, rootfs integrity, OTA integration, and
host flashing checks. Use **buildroot-development** for `BR2_TARGET_UBOOT_*`, **yocto-openembedded-development** for
recipes and `UBOOT_CONFIG`, and **kas-build-orchestration** for kas configuration and checkout orchestration. Use
**embedded-linux-debugging** to step through U-Boot or SPL with GDB, including reloading symbols after relocation, and
to decode a U-Boot exception.

## Workflow

1. Establish the task mode. For **authoring**, record the intended boot chain, interfaces, constraints, and a nearby
   release-matched board or test fixture. A new board does not need a failure log. For **diagnosis**, identify the first
   evidenced failure boundary and inspect its configuration, inputs, and console output before ranking causes.
2. Identify the source revision and the effective `.config`. Record the board, the SoC, and the silicon revision when
   it matters. Record the boot medium, the environment backend and layout, the active `bootcmd` and boot framework, and
   the exact artifacts involved. Separate known values from assumptions, and resolve consequential unknowns before a
   dependent target action.
3. Trace the relevant branch through the loaded reference. Compare the observed result with the required result.
   Test the most likely mechanism and its nearest failure boundary before broadening the diagnosis.
4. For **target mutation**, identify the exact destination, existing authorization, backup, recovery procedure, and
   persistence or trust boundary. Reuse explicit authorization. Ask only for missing intent, target identity, or
   permission for consequential actions outside it.
5. Validate the resulting behavior, including failure cases. Report the cause or design decision, the supporting
   evidence, the changed files and commands, the recovery conditions, and the observed validation. Label unresolved
   hypotheses and untested hardware or client behavior. A successful listing or build does not prove persistence or
   signature enforcement.

## State and authority boundaries

Source edits, host-side image construction, RAM changes, persistent writes, and OTP provisioning have different effects.
An authorized local development task permits its ordinary source and build changes; it does not imply permission to
flash a board or change its trust anchors.

Before `saveenv`, `fw_setenv`, environment erase, or boot-media writes, identify the backend, the device, and the exact
region. Capture the prior state using the [environment recovery
procedure](references/uboot-environment.md#backup-and-restore). Qualify recovery before the first production write. If
recovery cannot be established, state the uncovered risk and pause the dependent write. Rebuilding a source file is not
a reversal for a deployed policy that rejects the old image.

Before restricting console access or deploying an enforcing verifier, test both intended boot and failure and recovery paths
under that policy. Fuse and OTP changes are irreversible and require explicit provisioning authorization for the exact
silicon, values, lifecycle transition, and vendor procedure. Treat every fuse write as permanent, because no command
reverses it. A signed image booting in
an open or non-enforcing state is insufficient evidence for closing the device.

RAM-only does not mean passive or reversible. `env export` writes memory; `md` can read MMIO with side effects; device
queries can probe hardware. Network commands can fetch or autostart images. Confirm safe RAM ranges and network behavior
before use. Loading or executing a script can perform any action the script contains.

## Diagnostic evidence

Use bounded captures of relevant variables and failures. A complete recovery export is a separate artifact and may
contain secrets; protect it and avoid placing its full contents in logs.

| Boundary       | Useful evidence and its limit                                                                                                        |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Identity       | `version`, source revision, generated version header, effective config; a banner alone cannot identify every payload                 |
| Environment    | Relevant `printenv` values, backend config, Linux tool, version, and config; printenv shows RAM, not saved bytes                     |
| Load           | Command status, actual address, captured size, expected format and hash, RAM layout; a short `md` or DT model string is insufficient |
| SPL            | Last output plus source stage and map; SPL can fail before or after DRAM initialization                                              |
| Boot selection | `bootcmd`, targets, prefixes, bootmeth order and selected file; no universal extlinux-first rule                                     |
| Driver model   | `dm tree` bound and probed state, compatible match and dependencies; DM topology is not every DT node                                |
| FIT            | `dumpimage -l` for structure, trusted control DT for keys and policy, enforcing verifier for acceptance and rejection                |
| Handoff        | Kernel console and actual command line and DT; upstream image authentication does not cover every later fixup                        |

## Version and configuration checks

Inspect the active build rather than inferring behavior from a release date. The boot framework, the default
environment sources, `CONFIG_` and `CFG_` placement, and the control DT provider vary by release and board, and the
matching reference covers each one. Follow the built artifact to its actual provider before editing.

## Build identity

Record build provenance with the bundled helper only after a successful, quiescent build. Its interface, inputs, and
limits are in [Security and provenance](references/uboot-security-and-provenance.md#build-provenance-helper).

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources this skill is based on.
