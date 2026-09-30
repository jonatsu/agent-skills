---
name: serial-console-debugging
description: "Capture, read, and drive a target's serial console for debugging: boot logs, kernel and bootloader consoles, MCU UART output, and interactive shells. Use when choosing a baud rate or port, capturing a full boot log, sending break or SysRq, interrupting U-Boot, driving a console through the serial MCP server or tio and picocom, or when output is garbled or missing. Wiring and levels belong to debug-hardware; kgdb to embedded-linux-debugging."
license: MIT
compatibility: Needs a USB-serial adapter or probe UART visible to the host; the serial MCP server (jonatsu/serial-mcp-server, command serial_mcp) or tio or picocom for access.
metadata:
  author: Joonas Onatsu
---

# Serial Console Debugging

A serial console is the one channel most targets offer from the first instruction to a full shell. Use it to capture
evidence and to drive the target. Wiring, levels, and WSL2 passthrough belong to `debug-hardware`; what the kernel
prints and how to make it print more belong to `embedded-linux-debugging`.

## 1. Find the Port

- CDC devices appear as `/dev/ttyACM*`: the Pico probe's and Debug Probe's UART bridge, a J-Link's VCOM, and ESP32
  chips with built-in USB. FTDI, CP210x, and CH340 adapters appear as `/dev/ttyUSB*`.
- Use the stable names under `/dev/serial/by-id/`, which survive replugging and a changed enumeration order.
- Access needs the `dialout` group, or the udev rules the adapter's tools install.
- On WSL2 a missing port usually means the adapter is not attached; ask the user to attach it (`debug-hardware`).

## 2. Choose the Tool, One Owner per Port

A port has one reader at a time; a second one steals bytes from the first.

- **The serial MCP server** for a session the agent drives: open, read until a prompt, write, with pacing for slow
  targets. It is not configured globally. When a project needs it, add it to that project's own configuration, as
  [references/serial-mcp-server.md](references/serial-mcp-server.md) describes, and start a new session.
- **`tio` or `picocom`** for the user to watch or type.
- **Both at once:** the MCP server's PTY mirror lets the user watch (`ro`) or type (`rw`) through a linked device while
  the agent drives.

## 3. Get Readable Output

The common settings are 115200 baud, 8 data bits, no parity, 1 stop bit (8N1), and no flow control. Diagnose by
symptom:

- **Garbled characters:** wrong baud rate, or mismatched voltage levels. Try the board's documented rate first; a
  boot ROM may use a different rate from the application (the original ESP32's ROM prints at 115200 and many boards
  change later).
- **Nothing at all:** wrong port, TX and RX not crossed, ground missing, or the target's console not enabled or on
  another UART. For Linux, check `console=` and `earlycon` in `embedded-linux-debugging`.
- **Output stops early:** the console moved to another device during boot, or the target reset.
- **Characters dropped on input:** the target cannot keep up; pace the writes (section 5).

## 4. Capture Evidence

- Start the capture before resetting or powering the target, so it holds the first line.
- Opening a port can toggle DTR and RTS, which resets ESP32 and Arduino-style boards on open. Know whether the board
  resets on open before treating a capture's first line as the start of the boot.
- Keep the whole log with timestamps. Quote the lines around a failure, and keep the original for anything the quote
  omits.
- The MCP server's trace records each call; `tio --log` or `picocom --logfile` records a human session.

## 5. Drive the Console

- **Read before writing:** wait for the prompt with `read_until`, then send one command, then read its result.
- **Interrupt U-Boot:** send a key within its autoboot delay; start reading before the reset so the window is not
  missed.
- **Break and SysRq:** a serial break followed by a key sends Linux's magic SysRq; `g` there enters kgdb. The
  commands and tool keys are in [references/console-recipes.md](references/console-recipes.md).
- **Slow targets:** a bootloader or MCU shell with no receive buffering drops characters. Pace writes with the MCP
  server's `inter_char_delay_ms`, or `chunk_size` with `chunk_delay_ms`.
- **Stay within the task.** A bootloader or root shell can change the target: `saveenv`, memory writes, flash
  commands, or `reboot`. Read and inspect freely; run a command that changes state only when the task authorizes it.

The work is done when the capture holds the output that answers the question, from before the failure through its
end, and any command sent to the target stayed within the task.
