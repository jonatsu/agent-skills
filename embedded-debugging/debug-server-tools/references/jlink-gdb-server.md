# J-Link GDB Server

Checked 2026-09-30 against SEGGER's knowledge base (<https://kb.segger.com/J-Link_GDB_Server>) for J-Link software
9.80. On Linux the command-line server is `JLinkGDBServerCLExe`; confirm the name after installing. Probe setup,
Commander, and Remote Server are in `debug-hardware`'s J-Link reference.

## Starting It

```bash
JLinkGDBServerCLExe -device <DeviceName> -if SWD -speed 4000 -nogui -LocalhostOnly 1 -singlerun
```

- `-device`, `-if`, and `-speed` are required in practice; the default interface is JTAG. `-if` takes `JTAG`, `SWD`,
  `FINE`, or `2-wire-JTAG-PIC32`. `-speed` takes kHz, `auto`, or `adaptive`. Use the exact device name, such as
  `RP2040_M0_0`, `STM32F407VE`, or `BCM2712_A76_0`: SEGGER's reset, flash, and RTT handling depend on it.
- `-LocalhostOnly 1` matters on Linux, where the default listens on every interface.
- `-singlerun` exits when the last client disconnects and fails at once if the target connection fails, which suits
  scripted runs. `-nogui` suppresses dialogs except licence dialogs.
- `-halt` (the default) halts the target on start; `-nohalt` leaves it running; `-noreset` skips the reset.
- `-USB <serial>` selects a probe; `-IP <address>` reaches a J-Link Remote Server. Older guides show `-select USB`,
  which current versions replaced with these.
- `-JLinkScriptFile <file>` supplies a device script, which Cortex-A targets without a device entry often need.
- Ports: GDB 2331 (`-port`), SWO 2332 (`-SWOPort`), telnet 2333 for semihosting and SWO text (`-TelnetPort`), RTT
  19021 (`-RTTTelnetPort`). Several servers at once need distinct ports.
- Exit codes: `-2` port failed to open, `-3` no target voltage or connection failed, `-5` bad options, `-6` unknown
  device name, `-7` no J-Link.

GDB connects with `target remote localhost:2331`, then `monitor reset`, `load`, and so on.

## Monitor Commands

Sent from GDB as `monitor <command>`, case-insensitive:

- Free: `reset` (resets and halts), `halt`, `go`, `step`, `regs`, `memU32 <addr>`, `speed <kHz>`, `sleep <ms>`.
- `flash breakpoints = 0|1` turns software flash breakpoints off or on. The Base model is licensed for the core's
  hardware breakpoints; plan on those alone.
- `semihosting enable`, with output on the telnet port 2333; off by default.
- `SWO EnableTarget <CPUFreq> <SWOFreq> <PortMask> <Mode>`, with 0 for both frequencies to auto-detect.
- `exec <J-Link command>` runs any J-Link command, which is how RTT is configured:
  `exec SetRTTSearchRanges <start> <size>` or `exec SetRTTAddr <address>`.
- `flash erase` erases the flash: always-ask. Flashing itself is GDB's `load`.

## RTT and SWO

While the GDB Server (or Commander) holds the connection, RTT is on `localhost:19021`; `JLinkRTTClient` or any
telnet or `nc` client reads channel 0. Run one reader only, or readers steal each other's data. Auto-detection of the
control block needs the exact device name; otherwise set the address or search range with the `exec` commands above.
RTT is unreliable with low-power modes.

SWO needs an SWO pin and the target's trace clock enabled, works in SWD mode only, and uses UART encoding only.
`JLinkSWOViewer` reads it alongside a debugger.
