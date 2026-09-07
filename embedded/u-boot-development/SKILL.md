---
name: u-boot-development
description: "Develop and debug U-Boot: board porting, SPL/TPL, environment persistence, extlinux.conf/boot.scr, bootstd, FIT signatures, driver model, A/B bootcount, and build provenance. Use for saveenv/fw_setenv failures, missing boot scripts, rejected FITs, SPL overflows, new defconfigs, or bootcmd changes that lose console access. Route kernel/runtime faults to embedded-linux-bringup and build-system integration to Buildroot, Yocto/OE, or kas skills."
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

Use **embedded-linux-bringup** for kernel/OS DT, runtime drivers, rootfs integrity, OTA integration, and host flashing
checks. Use **buildroot-development** for `BR2_TARGET_UBOOT_*`, **yocto-openembedded-development** for recipes and
`UBOOT_CONFIG`, and **kas-build-orchestration** for kas configuration and checkout orchestration.

## Workflow

1. Establish the task mode. For **authoring**, record the intended boot chain, interfaces, constraints, and a nearby
   release-matched board or test fixture. A new board does not need a failure log. For **diagnosis**, identify the first
   evidenced failure boundary and inspect its configuration, inputs, and console output before ranking causes.
2. Identify the source revision and effective `.config`, board/SoC and silicon revision when relevant, boot medium,
   environment backend and layout, active `bootcmd` and framework, and the exact artifacts involved. Distinguish known
   values from assumptions; resolve consequential unknowns before a dependent target action.
3. Trace the relevant branch through the loaded reference. Compare the observed result with the required result.
   Test the most likely mechanism and its nearest failure boundary before broadening the diagnosis.
4. For **target mutation**, identify the exact destination, existing authorization, backup, recovery procedure, and
   persistence or trust boundary. Reuse explicit authorization. Ask only for missing intent, target identity, or
   permission for consequential actions outside it.
5. Validate the resulting behavior, including failure cases. Report the cause or design decision, supporting evidence,
   changed files/commands, recovery conditions, and observed validation. Label unresolved hypotheses and untested
   hardware/client behavior. A successful listing or build is not proof of persistence or signature enforcement.

## State and authority boundaries

Source edits, host-side image construction, RAM changes, persistent writes, and OTP provisioning have different effects.
An authorized local development task permits its ordinary source/build changes; it does not imply permission to flash a
board or change its trust anchors.

Before `saveenv`, `fw_setenv`, environment erase, or boot-media writes, identify the backend/device and exact region.
Capture the prior state using the [environment recovery procedure](references/uboot-environment.md#backup-and-restore).
Qualify recovery before the first production write. If recovery cannot be established, state the uncovered risk and
pause the dependent write. Rebuilding a source file is not a reversal for a deployed policy that rejects the old image.

Before restricting console access or deploying an enforcing verifier, test both intended boot and failure/recovery paths
under that policy. Fuse/OTP changes are irreversible and require explicit provisioning authorization for the exact
silicon, values, lifecycle transition, and vendor procedure. Never invent a reverse command. A signed image booting in
an open or non-enforcing state is insufficient evidence for closing the device.

RAM-only does not mean passive or reversible. `env export` writes memory; `md` can read MMIO with side effects; device
queries can probe hardware. Network commands can fetch or autostart images. Confirm safe RAM ranges and network behavior
before use. Loading or executing a script can perform any action the script contains.

## Diagnostic evidence

Use bounded captures of relevant variables and failures. A complete recovery export is a separate artifact and may
contain secrets; protect it and avoid placing its full contents in logs.

| Boundary       | Useful evidence and its limit                                                                                                    |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Identity       | `version`, source revision, generated version header, effective config; a banner alone cannot identify every payload             |
| Environment    | Relevant `printenv` values, backend config, Linux tool/version/config; printenv shows RAM, not saved bytes                       |
| Load           | Command status, actual address, captured size, expected format/hash, RAM layout; a short `md` or DT model string is insufficient |
| SPL            | Last output plus source stage and map; SPL can fail before or after DRAM initialization                                          |
| Boot selection | `bootcmd`, targets, prefixes, bootmeth order and selected file; no universal extlinux-first rule                                 |
| Driver model   | `dm tree` bound/probed state, compatible match and dependencies; DM topology is not every DT node                                |
| FIT            | `dumpimage -l` for structure, trusted control DT for keys/policy, enforcing verifier for acceptance/rejection                    |
| Handoff        | Kernel console and actual command line/DT; upstream image authentication does not cover every later fixup                        |

## Version and configuration checks

Inspect the active build instead of choosing an era by approximate migration dates. `distro_bootcmd` and bootstd can
coexist; default environment sources and `CONFIG_`/`CFG_` placement depend on release and board. U-Boot may use the
Linux-derived `dts/upstream` subtree with `CONFIG_OF_UPSTREAM`, local arch DTS files, or a board-supplied control DT.
Follow the built artifact to its actual provider before editing.

Select boot commands by architecture, format, enabled support, and memory requirements. `booti` can accept configured
compressed Image formats with suitable decompression memory; `bootm` handles supported FIT/legacy images. Persisting an
environment with `ENV_IS_NOWHERE` is unavailable, not a successful no-op. `bootdelay=0` still allows interruption;
`-2` suppresses the abort check but does not alone remove shell paths after failed boot.

## Build identity

Run the bundled helper immediately after a successful, quiescent build, using evidence captured by that build:

```bash
bash <skill-root>/scripts/stamp-uboot-provenance.sh \
  <source-root> <build-dir> <new-record-path> <build-identity-file> <artifact> [artifact ...]
```

All paths must be absolute. The identity file records the actual build invocation, defconfig, compiler/wrapper identity,
and relevant dependency pins. The helper hashes it, the effective `.config`, and required artifacts, records the
explicit source checkout's current revision/status, and refuses to replace any existing output. It cannot reconstruct
historical inputs or prove that supplied artifacts came from that source. See the reference for its full contract.

Source influence and historical uncertainty are recorded in [ATTRIBUTIONS.md](ATTRIBUTIONS.md).
