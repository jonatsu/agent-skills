# ESP32 Panics and RISC-V Exceptions

Checked 2026-09-30 against ESP-IDF 6.1's fatal-errors, IDF Monitor, and core-dump guides, the RISC-V privileged
specification, and the RP2350 datasheet.

## ESP32 Panic Output

A panic prints `Guru Meditation Error: Core 0 panic'ed (<cause>). Exception was unhandled.`, a register dump, and a
backtrace line of `PC:SP` pairs, the fault first:

```text
Backtrace: 0x400e14ed:0x3ffb5030 0x400d0802:0x3ffb5050
```

Common causes: `IllegalInstruction`, `LoadProhibited`, `StoreProhibited`, an interrupt-watchdog timeout, a cache error,
a corrupt heap, and stack overflow (a stack-protection fault, or a stack-canary watchpoint on chips without the
hardware assist). Xtensa dumps show `EXCCAUSE` and `EXCVADDR`; RISC-V ESP32 dumps show `MEPC`, `MCAUSE`, and `MTVAL`.

- `idf.py monitor` decodes the addresses. By hand, with the chip's toolchain prefix, such as `xtensa-esp32-elf` or
  `riscv32-esp-elf`:

  ```bash
  xtensa-esp32-elf-addr2line -pfiaC -e build/<project>.elf 0x400e14ed
  ```

- The panic action is `CONFIG_ESP_SYSTEM_PANIC`: print and reboot (the default), print and halt, silent reboot, or
  start a GDB stub on the console UART. The stub is post-mortem only: no breakpoints and no continuing.

- With a JTAG debugger attached and `CONFIG_ESP_DEBUG_OCDAWARE` on (the default), a panic halts into the debugger
  instead, and prints no dump.

- Core dumps: `CONFIG_ESP_COREDUMP_ENABLE_TO_FLASH` (needs a `coredump` partition) or `..._TO_UART`, then
  `idf.py coredump-info` or `idf.py coredump-debug`. Only stack variables are meaningful unless
  `CONFIG_ESP_COREDUMP_CAPTURE_DRAM` is on, and an encrypted coredump partition cannot be read by those commands.

- After the reset, `esp_reset_reason()` reports `ESP_RST_PANIC`, `ESP_RST_INT_WDT`, or `ESP_RST_TASK_WDT`.

## RISC-V Exceptions

On a trap into machine mode, `mcause` holds the cause (its top bit set for an interrupt), `mepc` the address of the
faulting instruction, and `mtval` the faulting address or instruction where the platform provides it.

| `mcause` | Exception                      | `mcause`   | Exception                           |
| -------- | ------------------------------ | ---------- | ----------------------------------- |
| 0        | Instruction address misaligned | 6          | Store/AMO address misaligned        |
| 1        | Instruction access fault       | 7          | Store/AMO access fault              |
| 2        | Illegal instruction            | 8          | Environment call from U-mode        |
| 3        | Breakpoint                     | 11         | Environment call from M-mode        |
| 4        | Load address misaligned        | 12, 13, 15 | Instruction, load, store page fault |
| 5        | Load access fault              |            |                                     |

Newer specification versions add 16 (double trap), 18 (software check), and 19 (hardware error); older cores do not
report them.

**RP2350 Hazard3** reports codes 0 to 8 and 11, jumps to `mtvec`'s address for every exception, and hardwires `mtval`
to zero. To find a bad load or store address, disassemble the instruction at `mepc` and recompute the address from
the saved registers. `POWMAN.CHIP_RESET` bit 27 records a system reset requested by the Hazard3 debugger.
