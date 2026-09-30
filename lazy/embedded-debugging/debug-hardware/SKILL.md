---
name: debug-hardware
description: "Connect and wire debug hardware to embedded targets: SWD and JTAG probes (Raspberry Pi Debug Probe or a Pico running debugprobe, SEGGER J-Link) and USB-serial adapters. Use when choosing a probe or interface, wiring SWD, JTAG, SWO, or UART, checking voltage levels, reset, and target power, reaching a USB probe from WSL2, or when a probe cannot see its target. Debugger and server configuration belongs to debug-server-tools."
license: MIT
compatibility: Needs physical access to the probe and target through the user. On WSL2, USB devices reach Linux only after the user attaches them with usbipd-win.
metadata:
  author: Joonas Onatsu
---

# Debug Hardware

Get a probe or serial adapter electrically and logically connected to a target, so a debug server or terminal can
use it. The agent cannot touch the hardware: the user wires, powers, and plugs. The agent's job is to say exactly
what to connect, check what the host can see, and find the fault when the probe cannot reach the target.

Configuring OpenOCD, pyOCD, probe-rs, or the J-Link GDB Server belongs to `debug-server-tools`; driving GDB belongs
to `gdb-debugging`.

## 1. Know the Permission Tiers

Probe operations change hardware state, and some changes are permanent. Apply these tiers to every command this
skill or its neighbours run:

- **Free:** reading memory and registers, halting, stepping, and resetting.
- **Needs the user's agreement for the task:** writing flash or RAM images.
- **Always ask first, for each operation:** erasing, writing option bytes or fuses, changing protection or security
  levels, unlocking or recovering a protected part (which erases it), and switching probe power onto the target.

Protection changes can lock a part for good: STM32 readout protection level 2 is permanent. Probe power can
back-feed a target that has its own supply. Two tools act at this tier by default, so check before using them:

- pyOCD mass-erases a locked nRF52 or Kinetis part on connect, because its `auto_unlock` option defaults to true.
- pyOCD switches a J-Link's target power on for every session unless `jlink.power` is set false.
- On connecting to a write-protected STM32, the J-Link software offers an unlock, which is a mass erase, in a dialog.

When the user has not stated the target's power arrangement, ask before any command that could enable probe power.

In a repository where hardware work happens, install the probe guard hook bundled with this skill, so the harness
itself stops the "always ask" commands. It goes into that project's own configuration, never the user's global one.
[references/probe-guard.md](references/probe-guard.md) has the install steps for Claude Code, Copilot CLI, and Codex,
and what the guard cannot see.

## 2. Make the Probe Visible to the Host

On WSL2 only, USB devices belong to Windows until the user attaches them. Detect WSL2 from `/proc/version`
containing `microsoft`, or from `WSL_DISTRO_NAME` being set. On native Linux, skip to the udev check below.

Check what Linux sees: `lsusb` for the probe, `ls /dev/ttyACM* /dev/ttyUSB*` for serial ports. When the device is
missing on WSL2, stop and ask the user to attach it, giving them the Windows commands:

```text
usbipd list                              # find the device's BUSID
usbipd bind --busid <BUSID>              # once per device, from an administrator shell
usbipd attach --wsl --busid <BUSID>
```

While attached, the device is unavailable to Windows. An attachment does not survive the device being unplugged or
reset into a bootloader, so a probe re-enumerating after a firmware update needs attaching again.

A J-Link has a second route: J-Link Remote Server on Windows serves the probe over the network, and Linux-side
`JLinkExe` or `JLinkGDBServerCLExe` connect to it with `IP <address>` or `-IP <address>`. Only SEGGER's own tools
speak that protocol; OpenOCD, pyOCD, and probe-rs need the `usbipd` route. See
[references/jlink-base.md](references/jlink-base.md).

Once the device is visible, check permissions: a probe listed by `lsusb` but refused by the tool usually lacks a
udev rule. Each tool ships its own rules file; `debug-server-tools` names them.

## 3. Choose the Probe and Interface

| Probe                             | Interfaces            | Levels       | Notes                                   |
| --------------------------------- | --------------------- | ------------ | --------------------------------------- |
| Pico or Pico 2 running debugprobe | SWD only, CMSIS-DAP   | 3.3 V        | No JTAG, no SWO; UART bridge on GP4/GP5 |
| Raspberry Pi Debug Probe          | SWD only, CMSIS-DAP   | 3.3 V        | Same firmware; no reset line            |
| SEGGER J-Link Base                | JTAG, cJTAG, SWD, SWO | 1.2 V to 5 V | Follows VTref; SWO in UART mode only    |

SWD needs two signals and suits Arm Cortex-M and Cortex-A debug ports. JTAG is the choice for a target that has no
SWD, such as the original ESP32's Xtensa cores, or where a board exposes only JTAG. The per-probe details, firmware,
and pinouts are in [references/pico-debugprobe.md](references/pico-debugprobe.md) and
[references/jlink-base.md](references/jlink-base.md). Per-target debug pins and traps, including the Raspberry Pi 4
and 5, are in [references/target-connections.md](references/target-connections.md).

## 4. Wire and Power

Give the user a pin-to-pin list: probe pin, signal, target pin. Then:

- **Ground first,** and a common ground between probe, target, and any serial adapter.
- **Match levels.** A Pico probe drives 3.3 V; a 1.8 V target needs a level shifter or a probe that follows VTref.
  The J-Link reads the target's voltage on VTref (pin 1) and adapts to it, so VTref must connect to the target's I/O
  supply.
- **Reset.** Wire the target's reset line when the probe has one: it enables connect-under-reset, the recovery for
  firmware that disables the debug pins or sleeps at once.
- **Serial.** Cross TX to RX. Check the adapter's level against the target's UART: 3.3 V, 1.8 V, and RS-232 levels
  are not interchangeable.
- **Order.** Connect the probe to the host, then to the target, then power the target.
- **Length.** Keep SWD and JTAG wires short. Long flying leads are the usual reason a link works only at low speed.

## 5. Make First Contact

Start the connection at a low clock, around 100 kHz to 1 MHz, and confirm that the probe reads the target's ID
(the debug port ID or the JTAG IDCODE) before raising the speed. When the probe cannot see the target, check in
this order, and stop at the first fault found:

1. The host sees the probe (section 2) and the tool reports the probe's firmware.
2. The target is powered, and the probe measures its voltage; a J-Link reporting `VTref is 0.000V` sees no target
   supply.
3. The interface matches the target (SWD versus JTAG), at the lowest speed.
4. Each signal is connected to the right pin, and none is shared with a peripheral or an on-board debugger.
5. The firmware may disable the debug pins, remap them, sleep, or enable protection. Connect under reset, or hold
   the target in its bootloader, before assuming a hardware fault.

The work is done when the probe reads the target's ID at the intended speed, or the report names the check that
failed and what the user should change.
