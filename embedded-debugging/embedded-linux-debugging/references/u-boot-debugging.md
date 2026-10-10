# U-Boot Debugging

Checked 2026-09-30 against U-Boot v2026.07's `doc/develop/gdb.rst`, `doc/usage/cmd/bdinfo.rst`, and
`doc/develop/crash_dumps.rst`. Porting and boot flow belong to `u-boot-development`.

## Build and Connect

Build with `CONFIG_CC_OPTIMIZE_FOR_DEBUG=y` (`-Og`) and `CONFIG_LTO=n`, so the debugger can follow the code. Start the
debug server for the board, then load the `u-boot` ELF from the build directory, not `u-boot.bin`:

```text
gdb-multiarch u-boot
(gdb) target extended-remote :3333
```

Before relocation the ELF's addresses are correct as they are.

## After Relocation

U-Boot copies itself to the top of RAM early in boot, and every address moves. Get the new base, then reload the
symbols there:

1. In the U-Boot shell, run `bdinfo` and read the `relocaddr` line. Without a working console, read it from GDB
   through the global-data pointer, which lives in a fixed register: `r9` on 32-bit Arm, `x18` on arm64, `gp` on
   RISC-V:

   ```text
   (gdb) p/x (*(struct global_data*)$r9)->relocaddr
   ```

2. Discard the old symbols and load them at the new address:

   ```text
   (gdb) symbol-file
   (gdb) add-symbol-file u-boot <relocaddr>
   ```

3. Check the result: `info symbol $pc` should name a real function. The documented sequence places the image start at
   `relocaddr`; on a board whose link address (`CONFIG_TEXT_BASE`) is not 0, verify this before trusting a
   backtrace, since the documentation does not cover that case.

## SPL

SPL has no GDB guide of its own. Load `spl/u-boot-spl` as the symbol file; SPL normally runs at its link address,
without the relocation `bdinfo` reports. When building SPL with `DEBUG`, U-Boot's SPL notes say `CONFIG_PANIC_HANG` may
be needed, because `do_reset` is often missing in SPL.

## Crash Output and Early Prints

On an exception U-Boot prints `elr` and `lr` twice: raw, and minus the relocation offset, marked `(reloc)`. Look up the
`(reloc)` value in `u-boot.map` or `objdump -S -D u-boot`; `scripts/decodecode` decodes the `Code:` line.

For output before the serial driver is up, `CONFIG_DEBUG_UART` with a UART-specific option such as
`CONFIG_DEBUG_UART_NS16550` and a `debug_uart_init()` call prints from the first instructions.
