# Console Recipes

Tool keys come from each tool's own help; confirm them with `tio --help` and `picocom --help`, since both have
changed bindings between releases.

## tio and picocom

```bash
tio -b 115200 /dev/serial/by-id/<device>                      # 8N1 is the default
tio -b 115200 --log --log-file boot.log /dev/serial/by-id/<device>
picocom -b 115200 --logfile boot.log /dev/serial/by-id/<device>
```

tio's commands start with `Ctrl-t`: `Ctrl-t q` quits and `Ctrl-t b` sends a break. picocom's start with `Ctrl-a`:
`Ctrl-a Ctrl-x` exits and `Ctrl-a Ctrl-\` sends a break.

## Linux Magic SysRq Over Serial

A serial break followed by a command key within a few seconds triggers SysRq on a serial console, when the kernel
has `CONFIG_MAGIC_SYSRQ` and the `kernel.sysrq` sysctl allows the function. Useful keys: `h` help, `w` blocked tasks,
`l` backtraces of all CPUs, `t` all tasks, `m` memory, `g` enter kgdb. `b` reboots immediately and `c` crashes the
kernel, so both need the task's agreement. From a shell on the target, `echo <key> > /proc/sysrq-trigger` does the
same.

## U-Boot

- Interrupt autoboot by sending a key within `bootdelay` seconds; start reading before the target resets.
- `printenv`, `bdinfo`, `version`, and `help` are read-only. `setenv` changes only RAM until `saveenv` writes it to
  storage; `saveenv`, `mw`, and flash or storage commands (`sf`, `mmc write`, `nand`) change the board and need the
  task's agreement.
- `u-boot-development` owns environment and boot-flow changes; `embedded-linux-debugging` owns stepping U-Boot in GDB.

## Raspberry Pi

- The Pi 4's default console is the mini UART on GPIO 14 and 15 (header pins 8 and 10), which needs `enable_uart=1`
  in `config.txt`.
- The Pi 5 has a dedicated 3-pin debug UART connector (`/dev/ttyAMA10` on the Pi); with nothing plugged in there and
  `enable_uart=1`, kernel output goes to GPIO 14 and 15 instead.
- Raspberry Pi's UARTs are 3.3 V.

## ESP32

- Many dev boards wire DTR and RTS to reset and boot-mode pins, so opening the port resets the chip, and a tool that
  holds them in the wrong state keeps it in reset or in the ROM bootloader. The serial MCP server's `set_dtr` and
  `set_rts` control them; `idf.py monitor` handles them itself.
- A garbled line at power-up is often the ROM bootloader's output at a different rate before the application's.

## Pico Probe and Debug Probe UART

The bridge defaults to 115200 baud on the probe's UART; setting the host port to 9728 baud turns on autobaud, but some
Linux tools cannot set that rate. It exports one UART.
