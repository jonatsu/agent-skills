# Logging Channels

Checked 2026-09-30 against SEGGER RTT 8.58 (<https://github.com/SEGGERMicro/RTT>), the Arm semihosting specification,
CMSIS 6, OpenOCD master, defmt 1.1.1, and probe-rs 0.32.0.

## RTT

The target links SEGGER's RTT code, which places a control block `_SEGGER_RTT` in RAM: the ID string `SEGGER RTT`, then
up buffers (target to host) and down buffers (host to target). By default there are two of each, with up buffer 0
("Terminal") at 1024 bytes. The ID string is written at run time, so a debugger's scan finds the block only after
`SEGGER_RTT_Init()` or the first write.

Buffer-full behaviour is set per buffer:

- `SEGGER_RTT_MODE_NO_BLOCK_SKIP` (the default): drop the message.
- `SEGGER_RTT_MODE_NO_BLOCK_TRIM`: write what fits.
- `SEGGER_RTT_MODE_BLOCK_IF_FIFO_FULL`: wait for the host. With no host reading, the firmware spins forever once
  the buffer fills. Keep it out of interrupt handlers and out of builds that run without a debugger.

probe-rs defaults its RTT channels to blocking when full (`probe-rs run --rtt-channel-mode`), to avoid losing data;
switch it when the firmware must keep running without a host.

The host side is per tool: OpenOCD `rtt setup` and `rtt server start`, J-Link port 19021, pyOCD `pyocd rtt`, probe-rs
`run` or `attach` (`debug-server-tools` has each). Point the search at the RAM that holds the block when
auto-detection fails.

## defmt (Rust)

defmt, "deferred formatting", keeps format strings in the ELF's `.defmt` section and sends only indexes and
arguments, so the host needs the exact ELF to decode. Setup: link with `-C link-arg=-Tdefmt.x`, one
`#[global_logger]`, and a transport crate:

- `defmt-rtt`, the usual choice; it cannot be combined with `rtt-target`. `DEFMT_RTT_BUFFER_SIZE` sets its buffer at
  build time.
- `defmt-itm` over ITM port 0.
- `defmt-semihosting`, which defmt does not recommend on real hardware.

`DEFMT_LOG=info` (or a per-module list) is a compile-time filter; the default is errors only. `probe-rs run`
decodes defmt, streams it, and catches HardFaults by default; `panic-probe` ends a panic in a HardFault so the run
stops, and with its `print-defmt` feature can print a `defmt::panic!` message twice unless `#[defmt::panic_handler]`
overrides it.

## SWO and ITM

ITM has 32 stimulus ports, output through the TPIU on the SWO pin. Enable, in order: `DEMCR.TRCENA` (bit 24 of
`0xE000EDFC`), `ITM->TCR.ITMENA`, and the port's bit in `ITM->TER`. A debugger usually sets `TRCENA`; firmware that
runs without one must set it itself. CMSIS's `ITM_SendChar()` checks the enables and spins until the port is ready.

- ITM is optional, so a Cortex-M3, M4, M7, or M33 part may lack it. Cortex-M0, M0+, and M23 have none.
- SWO needs the probe to support it (the J-Link does, the Pico probe does not) and the pin wired.
- OpenOCD configures the TPIU: `tpiu create`, then `<name> configure -protocol uart -traceclk <Hz> -pin-freq <Hz>`,
  `<name> enable`, and `itm port <n> on`. The trace clock is usually the core clock.

## Semihosting

Semihosting passes I/O and file operations to the debugger through `BKPT 0xAB` on M-profile, with the operation in R0.
It is slow and ties the firmware to a debugger:

- With no debugger attached, the `BKPT` causes a HardFault or a lockup.
- With a debugger attached but semihosting not enabled in it, the core halts at the `BKPT` and never resumes.

Enable it in the server: OpenOCD `arm semihosting enable`, J-Link `monitor semihosting enable`, pyOCD `-S`,
probe-rs `--semihosting-file`. Remove semihosting calls from firmware that ships or runs unattended.
