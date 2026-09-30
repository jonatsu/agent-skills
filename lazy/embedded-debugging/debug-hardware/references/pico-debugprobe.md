# Raspberry Pi Debug Probe and Pico Probes

Current known: debugprobe firmware `debugprobe-v2.3.1`, from <https://github.com/raspberrypi/debugprobe>, checked
2026-09-30. The pin assignments come from the firmware's `include/board_*_config.h`; check them there for a newer
release.

## One Firmware, Three Builds

The Raspberry Pi Debug Probe is an RP2040 board with a case, two 3-pin JST-SH ports, and cables. A plain Pico or
Pico 2 runs the same firmware, built for its own pins. Pick the release asset by the hardware:

| Hardware                 | Release asset             |
| ------------------------ | ------------------------- |
| Raspberry Pi Debug Probe | `debugprobe.uf2`          |
| Pico (RP2040)            | `debugprobe_on_pico.uf2`  |
| Pico 2 (RP2350)          | `debugprobe_on_pico2.uf2` |

The builds use different pins, so the wrong one produces a probe that enumerates and never sees a target. To flash,
the user holds BOOTSEL while plugging the board in and copies the `.uf2` onto the drive that appears. On WSL2 the
drive belongs to Windows, so the copy happens there. A Pico W is not supported. Building from source needs Pico SDK 2
or newer; the released files avoid the build.

## What It Speaks

- CMSIS-DAP, with both a v1 (HID) and a v2 (bulk) interface. Hosts prefer v2, which is faster.
- SWD only. There is no JTAG and no SWO, so for SWO trace or a JTAG-only target use the J-Link. Log over RTT, which
  rides on SWD, or over the UART bridge instead.
- Default SWD clock 1 MHz. Raspberry Pi's documentation uses 5 MHz with OpenOCD; the firmware's divider allows more,
  but wiring and the target set the real limit.
- A USB serial port bridged to the probe's UART: 115200 baud by default. Setting the host port to the magic rate 9728
  turns on autobaud; any other rate turns it off.

## Pins

| Signal       | Plain Pico or Pico 2       | Debug Probe                |
| ------------ | -------------------------- | -------------------------- |
| SWCLK        | GP2 (pin 4)                | GP12, on the "D" connector |
| SWDIO        | GP3 (pin 5)                | GP14, on the "D" connector |
| Target reset | GP1 (pin 2)                | none                       |
| UART TX / RX | GP4 (pin 6) / GP5 (pin 7)  | on the "U" connector       |
| Ground       | any GND pin, such as pin 3 | on both connectors         |

Physical pin numbers for the Pico follow its standard pinout. The Debug Probe has no reset line, so connect-under-reset
needs the target's reset wired another way or a different probe.

The Debug Probe's ports are labelled "D" (SWD) and "U" (UART), and follow Raspberry Pi's 3-pin debug connector
specification, with ground on the middle pin. On the header cables, orange is SC or TX (probe output), black is
ground, and yellow is SD or RX. To wire a Pico target, connect its SWCLK,
GND, and SWDIO to orange, black, and yellow.

Both probes drive 3.3 V. The Debug Probe runs at 3.3 V nominal I/O and can read a 1.8 V signal on its SD pin, but it
does not translate levels; a target whose pins are not 3.3 V tolerant needs a level shifter. A plain Pico has plain
3.3 V GPIO, so treat it the same way. When the target has its own supply, connect ground between probe and target
before any signal line: Raspberry Pi warns that a potential difference can damage the probe.

## Known Issues

- RP2350 targets need an OpenOCD that includes `target/rp2350.cfg`, which is on OpenOCD's master branch and in
  Raspberry Pi's builds but not in release 0.12.0. Issue #206 in the
  firmware repository reports "cannot read IDR" against an RP2350 even with a development build, unresolved at the
  time of checking.
- Some Linux serial tools cannot set the custom 9728 baud rate, so autobaud may be unreachable from them.
- Only one UART is exported.
