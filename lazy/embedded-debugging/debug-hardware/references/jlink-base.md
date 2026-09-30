# SEGGER J-Link Base

Current known: J-Link software 9.80 (getting-started guide UM08001, 2026-09-23) and SEGGER's knowledge base at
<https://kb.segger.com/UM08001_J-Link_/_J-Trace_User_Guide>, checked 2026-09-30. Confirm options with each tool's
`-?` or its KB page before relying on them; SEGGER renames options between major versions.

## Contents

- Capabilities and limits
- Included software
- Installing on Linux
- Reaching the probe from WSL2
- J-Link Commander in batch mode
- When J-Link cannot connect

## Capabilities and Limits

- Interfaces: JTAG, cJTAG, SWD, and SWO, on the 20-pin 0.1 inch connector. SWO is UART-encoded only; Manchester is
  not supported.
- Speed: up to 15 MHz on the target interface; SEGGER advises staying under 10 MHz for JTAG. SWD speed should not
  exceed ten times the target CPU clock.
- Levels: 1.2 V to 5 V, set by the target's voltage on VTref (pin 1). VTref must connect without a series resistor.
  The probe can also generate a fixed reference with the Commander command `VTREF <mV>` (0 returns to auto-detect).
- Reset: open drain, with a 100 ohm series resistor, on pin 15.
- Target power: pin 19 can supply 5 V at up to 300 mA, switched with the Commander commands `Power on` and
  `Power off`; appending `perm` makes the setting the probe's default. Enabling it is an always-ask operation.
- Pin 2 is not connected in the probe. A target that feeds VCC on pin 2 needs pins 1 and 2 tied on its connector.
- VCOM, a virtual serial port through the debug connector, ships disabled. It works only in SWD mode and on hardware
  version 9 or newer, uses pin 5 as J-Link Tx and pin 17 as J-Link Rx, and runs at up to 115200 baud. Enable it with
  `VCOM enable` in Commander, then power-cycle the probe.

## Included Software

SEGGER's comparison table marks these for the Base model:

| Included                               | Not included (needs a PLUS or a licence)          |
| -------------------------------------- | ------------------------------------------------- |
| Flash download, GDB Server, RTT, VCOM  | J-Flash, J-Flash SPI, Ozone, RDI, unlimited flash |
| J-Flash Lite, Commander, Remote Server | breakpoints, monitor mode                         |

The knowledge base also describes unlimited flash breakpoints as usable for evaluation, which conflicts with the
table. Plan on the core's hardware breakpoints alone; `monitor flash breakpoints = 0` disables the software ones in
the GDB Server. SEGGER positions the Base as a probe for OpenOCD and similar tools as well as its own.

## Installing on Linux

The software pack comes as DEB, RPM, or TGZ for x86, x64, arm32, and arm64 from
<https://www.segger.com/downloads/jlink/>. The DEB and RPM install the udev rules; for a TGZ, copy `99-jlink.rules`
from the pack to `/etc/udev/rules.d/` and reload udev. SEGGER's USB vendor ID is `1366`. The pack's command-line tools
include `JLinkExe` (Commander), `JLinkGDBServerCLExe`, `JLinkRemoteServerCLExe`, and `JLinkRTTClient`; confirm the
names with `ls` after installing, since SEGGER's pages name some of them only in their GUI forms.

## Reaching the Probe From WSL2

Two routes; choose by the tool that will drive the probe.

- **`usbipd-win`:** the probe appears inside Linux and every tool works: SEGGER's, OpenOCD, pyOCD, and probe-rs.
- **Remote Server on Windows:** run J-Link Remote Server on the Windows side, where the probe stays attached. Linux
  connects with `JLinkExe` and `IP <address>`, or `JLinkGDBServerCLExe -IP <address>`; the listener defaults to port
  19020\. In WSL2's default NAT networking, the Windows host is Linux's default gateway
  (`ip route show default`); in mirrored networking it is `127.0.0.1`. Windows' firewall must allow the port. Only
  SEGGER's tools use this route. Tunnel mode routes through SEGGER's public server; use the local address instead.

## J-Link Commander in Batch Mode

Run Commander non-interactively with a command file, one command per line:

```bash
JLinkExe -Device <DeviceName> -If SWD -Speed 4000 -AutoConnect 1 -ExitOnError 1 -NoGui 1 \
  -CommandFile check.jlink
```

Always pass the device name: SEGGER's reset and flash handling depend on it, and a core name alone is not enough for
RTT or flash. End every command file with `exit`, or a headless run may wait for input. `-USB <serial>` selects one
of several probes.

Commands by tier:

- **Free:** `ShowFWInfo`, `ShowHWStatus`, `IsHalted`, `Regs`, `Mem32 <addr> <count>`, `SaveBin <file> <addr> <bytes>`,
  `VerifyBin <file> <addr>`, `Halt`, `Go`, `Step`, `Reset`, `SetBP`, `ClearBP`.
- **Flash, with the task's agreement:** `LoadFile <file> [<addr for .bin>]`, which verifies and resets by default.
- **Always ask:** `Erase` (all flash, or a range), `Write1`/`Write2`/`Write4` to peripheral or option registers,
  `Power on`, and the persistent probe settings (`VCOM`, `Power ... perm`, `SetNickname`, `WinUSBEnable`).

On a write-protected STM32, the J-Link software offers to unlock the part, which mass-erases it. Decline in an
interactive session, and do not start an unattended run against a part whose protection state is unknown.

## When J-Link Cannot Connect

SEGGER's order, first fault wins:

1. Commander reports the probe over USB and prints its firmware. On a TGZ install, the udev rules are in place.
2. The target voltage reads non-zero. `VTref is 0.000V` means the target is unpowered or VTref is not wired.
3. The interface is right (SWD or JTAG) at a low speed, such as 100 kHz.
4. No debug line is unconnected or shared with a peripheral or an on-board debugger.
5. The application does not disable or remap the debug pins, enter low power, or enable security right after
   reset. With the exact device name, J-Link can connect under reset or halt in the bootloader.
