---
name: embedded-linux-bringup
description: "Bring up and debug embedded Linux targets. Use for DTS/DTB/overlay changes, kernel boot or rootfs failures, driver probe and peripheral faults, V4L2 cameras, cross-compiled binary/ABI problems, tracing and debugging, artifact deployment checks, and verified-rootfs or update-recovery diagnostics. Covers runtime kernel, hardware, and userspace boundaries; route build-system integration and bootloader internals to their specialist skills."
license: MIT
compatibility: Requires access to Linux source/build artifacts and target evidence. Commands depend on host/target tools, kernel configuration, privileges, and the BSP; check these at each branch. Hardware and emulation tests require suitable targets.
metadata:
  author: Joonas Onatsu
---

# Embedded Linux Bring-up

Establish what the target actually runs, then investigate the boundary supported by the evidence.
Keep an observation, a hypothesis, and a proven cause distinct. A missing device node alone does not locate the fault.

## Choose the Task

Record the board/SoC revision, kernel version and tree, architecture, build system/release, boot path, and relevant
toolchain. Use available artifacts to recover these facts; label unknowns instead of inventing defaults.

- **Planned bring-up or authoring:** identify the required hardware behavior, binding/API, current configuration,
  artifact path, and recovery method. Make a scoped change and define how its effect will be observed.
  An existing failure log is not a prerequisite.
- **Diagnosis:** capture the failing operation, return status, and relevant logs. Locate the first evidenced failure
  among build, boot handoff, kernel, bus/peripheral, and userspace. Rank hypotheses and run the smallest useful check.
  Revisit the boundary when new evidence contradicts it; initramfs userspace can run before the final root is mounted.
- **Deployment or recovery verification:** distinguish artifact identity, compatibility, selection at boot, loaded
  state, and functional behavior. Passing one check does not establish the others.

Continue authorized work when tools can obtain evidence. Ask for a result when target access is unavailable, or for
clarification when the next action exceeds the established scope. Report missing tools and untested outcomes explicitly.

## Route by Boundary

Read the relevant reference when that branch becomes useful; the entire package need not be loaded for every task.

| Task                                                             | Reference                                                           |
| ---------------------------------------------------------------- | ------------------------------------------------------------------- |
| Driver probe, resources, I2C/SPI/UART/MMC/GPIO, calibration      | [Device tree and drivers](references/device-tree-driver-bringup.md) |
| Compile, validate, compare, or apply a DTB/overlay               | [Device tree tools](references/device-tree-tooling.md)              |
| Boot handoff, console, root mount, init, missing device nodes    | [Board bring-up](references/board-bringup-checklist.md)             |
| Toolchain, SDK, sysroot, cross-build, ELF/ABI mismatch           | [Cross-compilation](references/cross-compilation.md)                |
| Userspace/kernel debugging, tracing, profiling, crash analysis   | [Debugging](references/debugging.md)                                |
| Sensor/media graph, video registration, capture, performance     | [Camera and V4L2](references/camera-v4l2.md)                        |
| Artifact identity and compatible QEMU iteration                  | [Deploy and iterate](references/deploy-and-iterate.md)              |
| Update installation, boot confirmation, rollback/recovery faults | [Update diagnostics](references/ota-updates.md)                     |
| dm-verity mapping, root hash, verified-rootfs boot faults        | [Rootfs integrity](references/rootfs-integrity.md)                  |

Build-system integration belongs to **buildroot-development** or **yocto-openembedded-development**;
multi-repository build orchestration belongs to **kas-build-orchestration**.
U-Boot environment, FIT authoring, boot scripts, and bootloader porting belong to **u-boot-development**.
Keep their runtime interfaces here only where they help locate a target failure.
General fleet rollout strategy and general-purpose VM management are outside this skill.

## Establish Evidence

Capture the command, status, target identity, and a bounded time window around the event.
Keep the original bounded log before presenting filtered excerpts; a keyword filter can hide the failing dependency.
For a probe failure, correlate the device's driver link, binding, resources, and kernel diagnostics.
Debugfs, tracefs, `/proc/config.gz`, and vendor overlay interfaces depend on the running kernel and mounts.
Their absence does not establish a hardware fault.

Use the matching source tree and release documentation for syntax and APIs. Examples are starting points, not board
defaults. Kernel DTS preprocessing, GPIO utility syntax, and vendor driver APIs differ by release.
The Yocto override transition was in Honister 3.4; route version-specific build syntax to its owning skill.

Close diagnosis with the demonstrated cause and evidence, the applied or proposed change, and its verification result.
If the cause is unknown, give the next discriminating check and explain what its outcomes would mean.
For authoring, report the implemented behavior and the observations still needed to qualify it.

## Hardware Access and Recovery

Reuse the user's authorization for the known operation and target. Obtain missing authorization before destructive
actions, uncovered hardware changes, or consequential external effects. A generic debugging request does not authorize
flashing a disk, changing boot selection, exposing a debugger, or interrupting a critical device.

- **Storage and boot state:** resolve the exact device, partition, selected slot, and current consumer before writing.
  Preserve the affected data/configuration and a usable recovery path. Backups alone do not establish recoverability.
  Do not overwrite a mounted production root or the only working recovery image as a diagnostic experiment.
- **MMIO and bus transactions:** reads may acknowledge interrupts, consume FIFO data, or fault on an unpowered block.
  Check the device manual, address, width, power/clock state, and driver ownership before access.
  I2C scans send transactions; neither `i2cdetect` nor `i2cget` is universally passive. Prefer inventory and driver
  diagnostics, then use only device-supported transactions within the authorized scope.
- **GPIO and reset:** inspect ownership before requesting a line. A utility read may change direction.
  Derive polarity and sequencing from the schematic, binding, and driver's logical GPIO operations; do not swap
  polarity merely because a device is silent. A driver-owned line is not a free test pin.
- **Driver lifecycle:** before unloading, unbinding, or reprobeing a driver, check mounted filesystems, consoles,
  active consumers, and recovery access. Do not interrupt them without authorization for that effect.
- **Debug sessions:** constrain listener access and account for pauses, watchdogs, trace overhead, and output storage.
  Record existing debug settings and restore the settings changed by the session. Never reset another session's traces.

Not every hardware operation has a reverse: clear-on-read, write-one-to-clear, FIFO, reset, and fuse semantics differ.
Use a documented recovery procedure instead of promising to restore hardware by writing back a saved value.

## Sources

Prefer the target kernel's `Documentation/`, DT bindings, device manuals, and the tool's own release documentation.
Source baselines and retained influences are recorded in [ATTRIBUTIONS.md](ATTRIBUTIONS.md).
Client deployment is not evidence of automatic activation or correct task execution.
