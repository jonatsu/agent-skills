# Target Debug Connections

Debug pins, protection traps, and recovery per target family. Facts checked 2026-09-30 against vendor documentation
and the tools' sources; the sources are named per section. Protection behaviour varies inside a family, so confirm
against the part's reference manual before any protection or recovery step.

## Contents

- RP2040 and RP2350
- STM32
- Nordic nRF52, nRF53, nRF91
- ESP32 family
- Raspberry Pi 4 and 5

## RP2040 and RP2350

Source: the RP2040 and RP2350 datasheets (build 2025-02-20) and OpenOCD's `rp2040.cfg` and `rp2350.cfg`.

- **SWD only**, on the 3-pin SWD header (SWCLK, GND, SWDIO).
- **RP2040** puts each core behind its own debug port on a multidrop SWD bus: core 0 answers at `0x01002927`, core 1
  at `0x11002927`. A third, the Rescue DP (`0xf1002927`), recovers a chip whose firmware stops the system clock or
  otherwise locks up: a rescue hard-resets the chip, and the boot ROM halts before running flash code. In OpenOCD,
  start once with `-c "set RESCUE 1"` before `-f target/rp2040.cfg`, then restart normally and load new code. A
  rescue changes no flash, so it is in the free tier.
- **RP2350** does the same through its RP-AP (`rescue_reset` in OpenOCD's `rp2350.cfg`), and multidrop is optional.
  Each of its two core sockets runs either a Cortex-M33 or a Hazard3 RISC-V core, chosen from OTP at reset; Arm is the
  default. The debug server must be told which: OpenOCD's `USE_CORE` takes `cm0`/`cm1` or `rv0`/`rv1`, and probe-rs
  has separate `RP235x` and `RP235x_riscv` targets. Setting the OTP boot architecture is a fuse write, always-ask.
- SEGGER's RP2040 page notes that the boot ROM needs a valid second-stage bootloader in flash even for RAM
  debugging, and that J-Link's reset halts at `0x20041F00`.

## STM32

Source: ST's STM32F4 readout-protection article on the ST Community (the reference manuals could not be fetched)
and OpenOCD's STM32 flash-driver documentation.

- SWD on SWCLK (PA14) and SWDIO (PA13) on most parts; wire NRST for connect-under-reset.
- **Readout protection (RDP)** has three levels. Level 0 is open. Level 1 blocks debug access to flash, backup
  SRAM, and backup registers; reading protected memory from the debugger halts the chip until a power cycle.
  Returning from level 1 to level 0 mass-erases flash and backup SRAM, can take up to 20 seconds, and leaves the part
  locked with its program deleted if reset during the erase. **Level 2 is permanent**: it can never be undone, and
  the system bootloader becomes unreachable. Never set it outside a deliberate production step that the user runs.
- Newer TrustZone families (STM32L5, U5, H5) have different regression rules, including password- or key-based
  ones; read the part's reference manual before touching protection there.
- Connect-under-reset recovers a part whose firmware disables SWD or sleeps at once: OpenOCD
  `reset_config srst_only connect_assert_srst`, probe-rs `--connect-under-reset`.

## Nordic nRF52, nRF53, nRF91

Source: the nRF Connect SDK's AP-Protect documentation (`doc/nrf/security/ap_protect.rst`) and OpenOCD's Nordic
target files.

- SWD on SWDCLK and SWDIO, plus reset.
- **AP-Protect** blocks all debugger access to registers and memory. Removing it takes `ERASEALL` through the
  CTRL-AP, which erases flash, RAM, and UICR: a recovery is always a full erase, always-ask.
- Older nRF52 hardware and the nRF9160 ship with AP-Protect off and keep whatever `UICR.APPROTECT` says. The nRF53,
  nRF54L, nRF91x1, and newer nRF52 builds ship with it **on and re-enable it at every hard reset**; after a recovery,
  debug access lasts until the next reset unless the firmware disables AP-Protect in software on each boot. A target
  that locks again after every reset is behaving as designed, not failing.
- `UICR.ERASEPROTECT`, where present, blocks `ERASEALL`. With both it and AP-Protect enabled the device cannot be
  recovered at all.
- Recovery commands: OpenOCD's `nrf52_recover`, `nrf53_recover`, and `nrf91_recover`, which need a CMSIS-DAP or
  J-Link (an ST-Link cannot reach the CTRL-AP). pyOCD recovers an nRF52 automatically on connect unless run with
  `-O auto_unlock=false`, so pass that option for any nRF52 whose protection state is unknown.

## ESP32 Family

Source: ESP-IDF's JTAG debugging guide and the chips' `soc_caps.h`.

- **The original ESP32 and ESP32-S2 have no SWD and no built-in USB debugger**; debug them over JTAG with an
  external adapter. Original ESP32 pins: TDI on GPIO12 (MTDI), TCK on GPIO13 (MTCK), TMS on GPIO14 (MTMS), TDO on
  GPIO15 (MTDO), plus ground. There is no TRST. The Pico probe cannot drive JTAG; use the J-Link.
- **GPIO12 is a strapping pin** that selects the flash supply voltage at power-up: low gives 3.3 V, high 1.8 V. A
  probe pulling it high at boot can starve a 3.3 V flash chip. Espressif's OpenOCD board files take
  `ESP32_FLASH_VOLTAGE` for 1.8 V modules.
- Firmware that reuses GPIO12 to GPIO15 breaks JTAG; the pre-flashed AT firmware on ESP32-WROOM-32 modules does.
- **Flash encryption or secure boot disables JTAG permanently by default**: the bootloader burns an eFuse on first
  boot unless `CONFIG_SECURE_BOOT_ALLOW_JTAG` is set. Enabling either is an always-ask fuse operation.
- **Built-in USB-Serial-JTAG** on ESP32-S3, C3, C5, C6, C61, H2, and P4, among others: a USB cable to the chip's
  D+ and D- pins (GPIO19 and GPIO18 on the C3) is the whole debug connection. It needs Espressif's udev rules,
  `60-openocd.rules` from `openocd-esp32`.
- Debug ESP32 parts with Espressif's OpenOCD fork, `openocd-esp32`, installed by ESP-IDF, or with probe-rs, which
  covers the Xtensa and RISC-V ESP32 chips.

## Raspberry Pi 4 and 5

Source: Raspberry Pi's `config.txt` documentation, the probe.rs Raspberry Pi page, and SEGGER's Raspberry Pi 5 page.

- **JTAG on the GPIO header, all models:** add `enable_jtag_gpio=1` to `config.txt` on the boot partition; it puts
  GPIO22 to GPIO27 into JTAG mode. Pins: GPIO22 TRST, GPIO23 RTCK, GPIO24 TDO, GPIO25 TCK, GPIO26 TDI, GPIO27 TMS.
  Connect at least TDO, TCK, TDI, TMS, and ground, and the probe's VTref to a 3.3 V pin. Editing `config.txt` is a
  change to the target's boot media, so it needs the user's agreement.
- The Pi 4's four Cortex-A72 cores are reachable with OpenOCD's `target/bcm2711.cfg` or probe-rs
  (`probe-rs gdb --protocol jtag --chip RaspberryPi4B`; state the protocol, since SWD is not supported there). SEGGER
  lists no Pi 4 device, so J-Link falls back to its generic ARMv8-A support and may need a script file.
- The Pi 5's Cortex-A76 cores have probe-rs support (`BCM2712`, variant `RaspberryPi5B`, not documented beyond the
  target file) and J-Link device names `BCM2712_A76_0` to `BCM2712_A76_3` (J-Link software 8.36 or newer).
- **Unresolved for the Pi 5:** SEGGER's page wires SWD to the 3-pin connector J16, while Raspberry Pi documents that
  connector as a UART port. Start from GPIO JTAG, which Raspberry Pi documents; try SWD on J16 only with a J-Link, and
  report what worked.
