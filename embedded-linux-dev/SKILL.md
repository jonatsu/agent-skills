---
name: embedded-linux-dev
description: "Embedded Linux bring-up and debugging partner for ARM/RISC-V SoC boards — device tree (DTS/DTSI/DTB/DTBO/overlays), kernel driver probe failures, board bring-up, boot-log and dmesg analysis, cross-compilation and toolchain/ABI mismatch, peripheral debugging (I2C/SPI/UART/MMC/GPIO/regulator/clock), V4L2 camera bring-up, and userspace diagnostics (strace/gdbserver/perf/ftrace/kmemleak/kgdb/dynamic_debug/devmem). Use when a driver will not probe, a `/dev` node or `/dev/video*` is missing, the kernel panics on rootfs mount, `-EPROBE_DEFER` loops, `GLIBC_2.xx not found` on target, dtc/fdtput/dt-validate device-tree work, QEMU board emulation, or verifying a module/DTB deploy (vermagic). For build systems and bootloaders route to yocto-oe-dev, buildroot-dev, kas-dev, or uboot-dev."
metadata:
  author: Joonas Onatsu
  license: MIT
  tags:
    - embedded-linux
    - device-tree
    - dts
    - dtb
    - kernel-driver
    - board-bringup
    - cross-compilation
    - toolchain
    - v4l2
    - camera
    - i2c
    - spi
    - gpio
    - dmesg
    - ftrace
    - perf
    - gdbserver
    - kgdb
    - qemu
    - arm
    - debugging
---

# Embedded Linux Dev

**IRON LAW: Classify every failure by its FIRST concrete boundary — build → boot → kernel/DTS → bus/peripheral → userspace — and PROVE that boundary with a log line, command output, or config value BEFORE hypothesizing. You MUST NOT guess across layers or propose a fix before the failing layer is evidenced.**

A missing `/dev/video1` is a DTS or driver fault before it is a userspace fault. Name the boundary, demand the evidence that pins it there, then act.

---

## Overview

Development partner for device tree, kernel drivers, board bring-up, cross-compilation, peripheral debugging, and userspace integration on embedded Linux targets. Keep this file for method and routing; pull worked commands and board examples from `references/` on demand — do NOT read every reference upfront.

Board-specific examples (BeagleBone Black, STM32MP1, i.MX6ULL/OV5640, QEMU virt) live ONLY in `references/`. This file stays board-agnostic.

### Route build and bootloader work to a sibling skill

| Task | Skill |
|------|-------|
| Yocto/OE: recipes, layers, BitBake, sstate, SDK | **yocto-oe-dev** |
| kas build orchestration (`.kas.yml`, `kas build`) | **kas-dev** |
| Buildroot: menuconfig, packages, `BR2_EXTERNAL` | **buildroot-dev** |
| U-Boot: env, extlinux, FIT, boot scripts, porting, DM | **uboot-dev** |

### Route the symptom to a reference

| Symptom | Reference |
|---------|-----------|
| DTS node missing, driver not probing, wrong/absent resource | `references/device-tree-driver-bringup.md` |
| Need to compile/decompile/diff/validate a DTB or overlay | `references/device-tree-tooling.md` |
| Board won't boot, kernel panic, rootfs not found, earlycon | `references/board-bringup-checklist.md` |
| I2C/SPI/UART/MMC/GPIO bus or peripheral issue | `references/device-tree-driver-bringup.md` → bus section |
| Sensor reads off, clock drifts, per-unit or per-board calibration | `references/device-tree-driver-bringup.md` → calibration section |
| Cross-compile failure, ABI mismatch, missing `.so` on target | `references/cross-compilation.md` |
| strace, gdbserver, perf, ftrace, kmemleak, kgdb, dynamic_debug, oops | `references/debugging.md` |
| Camera bring-up, V4L2, no `/dev/video*`, no frames, bad colours | `references/camera-v4l2.md` |
| Fast edit-build-test loop under QEMU; verify a deploy landed | `references/deploy-and-iterate.md` |
| Field/OTA updates, A/B rollout, RAUC/swupdate, rollback strategy | `references/ota-updates.md` |
| dm-verity, verified/read-only rootfs, root hash, verified boot | `references/rootfs-integrity.md` |

---

## Workflow

Tick each step per task. Steps marked ⛔ BLOCKING MUST complete before the next; ⚠️ REQUIRED MUST be done but MAY interleave.

- [ ] **⚠️ REQUIRED — Lock platform context.** Record SoC/board + revision, kernel version and tree (mainline/vendor/BSP branch), architecture and toolchain tuple, bootloader and version, build system + release, and the exact current symptom (log line, failed command, missing node, errno). If a fact is unknown, state the assumption and LABEL it.
- [ ] **⛔ BLOCKING — Classify the failure boundary.** Place the failure at build, boot, kernel/DTS, bus/peripheral, or userspace. You MUST NOT skip to a downstream layer while an upstream one is unproven.
- [ ] **⛔ BLOCKING — Collect evidence at that boundary.** Gather the bounded artifacts in *Evidence First* below before ranking causes. No fix proposal until the boundary is evidenced.
- [ ] **⚠️ REQUIRED — Rank causes, then validate ONE.** Propose the single most likely cause and ONE command or ONE file edit that confirms or refutes it. Keep steps small; stop at a natural checkpoint and request the result.
- [ ] **⚠️ REQUIRED — Confirm before mutating.** Any flash, register write, boot-config edit, or env write passes the *Confirmation gates* first.
- [ ] **⚠️ REQUIRED — Close with the Output contract.** Root cause → evidence → exact fix/command → validation command.

---

## Confirmation gates

You MUST stop and get explicit user confirmation before any destructive or hardware-mutating action. Default to read-only; require an explicit opt-in to mutate; pair every mutating command with its reverse.

- **Writing block/flash devices** — `dd`, `bmaptool copy … /dev/sdX`, `flashcp`, `nandwrite`, `mmc`/eMMC or SD overwrites. You MUST confirm the exact target device path first; a wrong `/dev/sdX` destroys the host disk. Capture a backup of any partition you overwrite.
- **Boot-config edits** — `extlinux.conf`, `bootargs`, a DTB/DTBO on the boot partition, or `fw_setenv` from userspace. You MUST back up the original and pair the change with its restore command.
- **Register pokes** — `devmem`/`devmem2` WRITES and writes into `/sys` that change hardware state. You MUST confirm; a wrong write can hang or damage the SoC. Reads are safe and need no gate.
- **Unloading an in-use driver** — `rmmod`/`modprobe -r` of a module backing a mounted fs, console, or active device.

### Safety

- MUST NOT modify `extlinux.conf`, device tree source or blobs, boot memory reservations, or run `saveenv`/`fw_setenv` unprompted.
- Prefer reversible diagnostics first: NFS/QEMU rootfs over reflashing, `devmem` reads over writes, `dynamic_debug` over patching source.
- For env and boot-flow changes on the bootloader itself, route to **uboot-dev** and follow its safety contract.

---

## Evidence First

Before diagnosing, inspect (or ask the user for) the artifacts that pin the failing boundary:

- The exact failing log line — kernel `dmesg`, `${WORKDIR}/temp/log.do_*` for a build, or the serial console around "Starting kernel …".
- The DTS node and the binding it claims (`compatible`, `reg`, `clocks`, `*-supply`, `*-gpios`).
- The driver `probe` return value and the last log line before it failed.
- Command output from `i2cdetect`, `ls /dev/`, `cat /proc/device-tree/…`, `readelf -d`.

Keep every capture BOUNDED — `dmesg | grep -i sensor | tail -20`, never a raw full `dmesg`.

```bash
# Probe result for a device
dmesg | grep -E "(probe|error|defer)" | grep -i <device> | tail -20

# Deferred-probe list (kernel >= 5.10)
cat /sys/kernel/debug/devices_deferred 2>/dev/null

# Which driver owns a node
ls -la /sys/bus/platform/devices/<node>/driver

# Clock tree (0 Hz => parent not enabled)
cat /sys/kernel/debug/clk/clk_summary | grep -i <clock>

# Device tree, live
cat /proc/device-tree/<node>/compatible | xxd
ls /proc/device-tree/

# Bus scan / GPIO
i2cdetect -y -r <bus>
gpioinfo

# Cross-compiled binary sanity
file <binary>; readelf -d <binary> | grep NEEDED

# Turn on a driver's pr_debug() without rebuilding
echo 'module <mod> +p' > /sys/kernel/debug/dynamic_debug/control
```

---

## Output contract

Every diagnostic answer MUST end with these four, in order:

1. **Root cause** — the single proven boundary and mechanism.
2. **Supporting evidence** — the log line, command output, or config value that proves it.
3. **Exact fix** — the precise command or file edit (real property names, real paths).
4. **Validation** — the command that confirms the fix worked.

If the root cause is not yet proven, say so and give the ONE next command that would prove it — do NOT present a guess as a diagnosis.

---

## Version awareness

Kernel, bootloader, and build-system syntax drift across releases. Before giving syntax-specific guidance you MUST confirm:

- **Kernel version and tree** — DT binding names, sysfs/debugfs paths, and driver APIs (e.g. `devm_reset_control_get_exclusive` vs the soft-deprecated `devm_reset_control_get`) change across releases.
- **Yocto release codename** — override syntax changed at Kirkstone (`_append` → `:append`). Answering in the wrong era is a top error; defer detail to **yocto-oe-dev**.
- **U-Boot version** — env, distro-boot, and FIT specifics; defer to **uboot-dev**.
- **Buildroot LTS** — Kconfig symbols and package infra; defer to **buildroot-dev**.

When the release is unknown, state which answer you would give per era rather than assuming one.

---

## Anti-patterns

- MUST NOT trust a `compatible` string by eye — one character between the DTS and the driver `of_match_table` silently prevents binding with no error. Diff them.
- MUST NOT treat `-EPROBE_DEFER` as a bug. It is expected retry; the bug is a driver that never rebinds because a `clocks`/`*-supply`/`*-gpios` provider is `disabled` or absent.
- MUST NOT copy a vendor BSP's reset GPIO polarity unquestioned — a device held silently in reset is almost always a `GPIO_ACTIVE_LOW` vs `GPIO_ACTIVE_HIGH` mismatch.
- MUST NOT enable a leaf clock without confirming its parent tree is enabled — a 0 Hz output in `clk_summary` is a disabled parent.
- MUST NOT deploy a binary before running `file` and `readelf -d … | grep NEEDED`; a host-glibc build fails on target with `GLIBC_2.xx not found`.
- MUST NOT ask for or paste a raw full `dmesg`/`strace` — always bound it (`| grep -i <x> | tail -N`).
- MUST NOT poke registers (`devmem2` write) or overwrite boot config to "see what happens" — that is a mutation, and it goes through the *Confirmation gates*.
- MUST NOT assume a driver is present — a silent probe failure is often simply `CONFIG_<X>` not built (`zcat /proc/config.gz | grep -i <X>`).
- MUST NOT hardcode a physical-world constant that varies per board or per unit (oscillator trim, sensor bias, actuator centre) — it needs a tunable seam, and a software fudge factor added before the error is proven at its own boundary hides a real DTS, regulator, or clock fault.

---

## Reference pointers

Canonical upstream docs (cite the release-matched version):

- Kernel DT bindings: `Documentation/devicetree/bindings/` in the kernel tree; the DT spec at devicetree.org.
- dt-schema / `dt-validate`: github.com/devicetree-org/dt-schema; overlays and lopper: github.com/devicetree-org/lopper.
- Toolchains: toolchains.bootlin.com. Community knowledge base: elinux.org.
- V4L2 / media: the kernel `Documentation/userspace-api/media/` and `linuxtv.org`.

`references/`:

- `device-tree-driver-bringup.md` — DTS node anatomy, resource ownership, clock/reset/GPIO/regulator APIs, driver registration, probe path, missing-`/dev`-node walk, per-bus (I2C/SPI/UART/MMC) debugging, Kconfig checks, calibration and per-unit trim seams (DTS vs NVMEM vs IIO vs RTC offset).
- `device-tree-tooling.md` — `dtc` compile/decompile, overlays (`dtc -@`), `fdtget`/`fdtput`/`fdtdump`, `dtx_diff`, `dt-validate`/dt-schema, and the live `/proc/device-tree`.
- `board-bringup-checklist.md` — boot chain, SoC boot-file naming, earlycon, kernel cmdline, panic-on-rootfs triage, `/dev` node lifecycle, service startup, NFS rootfs.
- `deploy-and-iterate.md` — the QEMU edit-build-test loop and a deploy-verify pattern (vermagic match, DTB/DTBO present, boot-config sanity).
- `cross-compilation.md` — toolchain types, Yocto SDK, autotools/CMake/Meson cross builds, sysroot and pkg-config, ABI diagnosis, static/musl licensing.
- `debugging.md` — strace, gdbserver, perf + flame graphs, ftrace/trace-cmd, dynamic_debug, devmem/devmem2, kgdb/kdb, kmemleak, crash, valgrind, oops decode.
- `camera-v4l2.md` — camera bring-up order, V4L2 + media-ctl diagnostics, `v4l2-compliance`, `yavta`, buffer lifecycle, failure buckets.
- `ota-updates.md` — the userspace update-framework layer above the bootloader: A/B vs single-copy+recovery vs delta strategy, RAUC (`system.conf`/`.raucb`/mark-good, `plain`/`verity`/`crypt` bundle formats), swupdate (`sw-description`/`.swu`/suricatta), RAUC-vs-swupdate choice, signing, rollback verification; cross-links `uboot-dev` for the boot-slot mechanics.
- `rootfs-integrity.md` — read-only, cryptographically verified rootfs with dm-verity as the rootfs link of a verified-boot chain: Merkle hash tree and root hash, `veritysetup` build, `dm-mod.create`/initramfs bring-up, anchoring the root hash in a signed FIT cmdline, A/B per-slot root hashes, read-only rootfs consequences; cross-links `uboot-dev` for the FIT/secure-boot half and `ota-updates.md` (RAUC `verity` bundle format is a DISTINCT use of dm-verity).

## Attribution

See `ATTRIBUTIONS.md` for upstream sources and adaptation notes.
