# Cortex-M Fault Registers and Reset Causes

Checked 2026-09-30 against the Cortex-M7 and Cortex-M33 Generic User Guides, the Cortex-M4 TRM, the Cortex-M0+
Generic User Guide, CMSIS 6, and vendor headers (STM32 CMSIS device packs, nrfx 4.6.0, pico-sdk 2.3.1, ESP-IDF 6.1).
Addresses are in the System Control Block, base `0xE000ED00`.

## Contents

- Fault registers
- CFSR bits
- Stacked frame and EXC_RETURN
- Precise bus faults and fault handlers
- Armv8-M stack limits
- Armv6-M
- Reset causes

## Fault Registers

| Register | Address      | Holds                                                                  |
| -------- | ------------ | ---------------------------------------------------------------------- |
| `SHCSR`  | `0xE000ED24` | Fault handler enables (MEMFAULTENA 16, BUSFAULTENA 17, USGFAULTENA 18) |
| `CFSR`   | `0xE000ED28` | MMFSR [7:0], BFSR [15:8], UFSR [31:16]                                 |
| `HFSR`   | `0xE000ED2C` | VECTTBL [1], FORCED [30], DEBUGEVT [31]                                |
| `DFSR`   | `0xE000ED30` | Why the core entered debug state, not why it faulted                   |
| `MMFAR`  | `0xE000ED34` | MemManage address, valid only with `MMARVALID`                         |
| `BFAR`   | `0xE000ED38` | Bus-fault address, valid only with `BFARVALID`                         |

`CFSR` and `HFSR` bits are sticky and cleared by writing 1. `MMFAR` and `BFAR` are one physical register on the
Cortex-M4, so only one valid bit is set at a time, and the address is updated only while its valid bit is clear: a
stale valid bit hides a later address.

From GDB: `x/wx 0xE000ED28` for `CFSR`, `x/wx 0xE000ED2C` for `HFSR`.

## CFSR Bits

| Bit | Name          | Meaning                                                                       |
| --- | ------------- | ----------------------------------------------------------------------------- |
| 0   | `IACCVIOL`    | Instruction fetch from a non-executable region; stacked PC is the instruction |
| 1   | `DACCVIOL`    | Load or store not permitted; `MMFAR` holds the address                        |
| 3   | `MUNSTKERR`   | MemManage fault while unstacking on exception return                          |
| 4   | `MSTKERR`     | MemManage fault while stacking on exception entry; the frame may be wrong     |
| 5   | `MLSPERR`     | MemManage fault during lazy FP state preservation                             |
| 7   | `MMARVALID`   | `MMFAR` is valid                                                              |
| 8   | `IBUSERR`     | Instruction bus error                                                         |
| 9   | `PRECISERR`   | Precise data bus error; stacked PC is the instruction, `BFAR` the address     |
| 10  | `IMPRECISERR` | Imprecise data bus error; stacked PC is unrelated                             |
| 11  | `UNSTKERR`    | Bus fault while unstacking                                                    |
| 12  | `STKERR`      | Bus fault while stacking                                                      |
| 13  | `LSPERR`      | Bus fault during lazy FP state preservation                                   |
| 15  | `BFARVALID`   | `BFAR` is valid                                                               |
| 16  | `UNDEFINSTR`  | Undefined instruction                                                         |
| 17  | `INVSTATE`    | Invalid state, such as a branch to an address with bit 0 clear                |
| 18  | `INVPC`       | Invalid `EXC_RETURN` loaded into PC                                           |
| 19  | `NOCP`        | Coprocessor access, such as FPU use with the FPU disabled                     |
| 20  | `STKOF`       | Stack-limit violation (Armv8-M only)                                          |
| 24  | `UNALIGNED`   | Unaligned access, when `CCR.UNALIGN_TRP` is set; LDM, STM, LDRD, STRD always  |
| 25  | `DIVBYZERO`   | Division by zero, when `CCR.DIV_0_TRP` is set                                 |

Armv8-M with the Security Extension adds SecureFault, reported in `SFSR`, and banks `MMFSR`, `MMFAR`, and `UFSR`
between security states.

## Stacked Frame and EXC_RETURN

On exception entry the core pushes eight words, lowest address first: R0, R1, R2, R3, R12, LR, PC, xPSR. With an
active FPU context, S0 to S15, FPSCR, and one reserved word follow. The stack pointer after stacking points at R0, so
the stacked PC is at offset 24.

`EXC_RETURN`, the value in LR on handler entry:

- Armv7-M: `0xFFFFFFF1` (return to Handler, MSP), `0xFFFFFFF9` (Thread, MSP), `0xFFFFFFFD` (Thread, PSP), and
  `0xFFFFFFE1`, `0xFFFFFFE9`, `0xFFFFFFED` for the same with an FP frame. Bit 2 selects PSP, bit 3 Thread mode, and a
  clear bit 4 means an FP frame was stacked.
- Armv8-M: bits [31:24] are `0xFF`; bit 2 SPSEL (PSP), bit 3 Mode (Thread), bit 4 FType (0 means FP context), bit 5
  DCRS, bit 6 S (secure stack), bit 0 ES. Do not apply the Armv7-M constants to an Armv8-M image unchanged.

In GDB, after reading LR: `x/8wx $psp` or `x/8wx $msp` shows the frame, and `info symbol` on the seventh word names
the faulting function.

## Precise Bus Faults and Fault Handlers

- `ACTLR` at `0xE000E008`, bit 1 `DISDEFWBUF`, disables the write buffer for default-memory-map accesses, which makes
  every bus fault precise at a performance cost. It exists on Cortex-M3 and M4 only.
- With `SHCSR`'s MEMFAULTENA, BUSFAULTENA, and USGFAULTENA clear, every fault arrives as a HardFault with
  `HFSR.FORCED` set and the cause still in `CFSR`. Enabling them gives each fault class its own handler. Set them with
  a read-modify-write.

## Armv8-M Stack Limits

`MSPLIM` and `PSPLIM` hold the lowest allowed value of each stack pointer; going below raises a UsageFault with
`CFSR.STKOF`. They reset to 0, so they do nothing until firmware or an RTOS sets them. With the built-in guard the
context may not be stacked on overflow, so the reported PC is unreliable. Cortex-M23 has the limit registers but no
UsageFault, so a violation there becomes a HardFault.

## Armv6-M

Cortex-M0 and M0+ have no `CFSR`, `HFSR`, `MMFAR`, `BFAR`, or `AFSR`. Every fault is a HardFault, or a lockup inside
the NMI or HardFault handler. `DFSR` and `SHCSR` exist but only a debugger can read them. `EXC_RETURN` is one of
`0xFFFFFFF1`, `0xFFFFFFF9`, `0xFFFFFFFD`. The stacked PC and the instruction there are the evidence: an unaligned
access, a `BKPT` with no debugger, an invalid branch, or a bad memory access.

## Reset Causes

| Target    | Register                             | Flags                                                                                                        |
| --------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| STM32F4   | `RCC_CSR` at `0x40023874`            | BOR 25, PIN 26, POR 27, SFT 28, IWDG 29, WWDG 30, LPWR 31; RMVF 24 clears                                    |
| STM32H743 | `RCC_RSR` at `0x580244D0`            | CPU 17, D1 19, D2 20, BOR 21, PIN 22, POR 23, SFT 24, IWDG1 26, WWDG1 28, LPWR 30                            |
| nRF52840  | `POWER->RESETREAS` at `0x40000400`   | RESETPIN 0, DOG 1, SREQ 2, LOCKUP 3, OFF 16, LPCOMP 17, DIF 18, NFC 19, VBUS 20                              |
| RP2040    | `CHIP_RESET` at `0x40064008`         | HAD_POR 8, HAD_RUN 16, HAD_PSM_RESTART 20                                                                    |
| RP2040    | `WATCHDOG->REASON` at `0x40058008`   | TIMER 0, FORCE 1; both zero after a hardware reset                                                           |
| RP2350    | `POWMAN->CHIP_RESET` at `0x4010002C` | HAD_POR 16, HAD_BOR 17, HAD_RESCUE 21, watchdog bits 22 to 24 and 28, HAD_HZD_SYS_RESET_REQ 27               |
| RP2350    | `WATCHDOG->REASON` at `0x400D8008`   | TIMER 0, FORCE 1; cleared by a debugger reset of either core                                                 |
| ESP-IDF   | `esp_reset_reason()`                 | `ESP_RST_PANIC`, `ESP_RST_INT_WDT`, `ESP_RST_TASK_WDT`, `ESP_RST_BROWNOUT`, `ESP_RST_CPU_LOCKUP`, and others |

Other STM32 families and nRF parts use different layouts; read the part's CMSIS device header. The nRF and STM32
flags stay set until written, so a value may include earlier resets.
