# ARMv7 runtime helpers and calling-convention variants

Three AArch32 conventions routinely distort a decompiler's output: the floating-point calling variant, which decides\
where float arguments live; the `__aeabi_*` compiler-runtime helpers, which a decompiler shows as ordinary calls; and\
the Linux system-call convention, which a decompiler shows as one opaque trap. This reference catalogs all three so\
recovered arguments and reconstructed logic match the binary. The register roles and helper semantics follow the Arm\
AAPCS32 and Run-time ABI, and the system-call convention follows the Linux kernel's ARM entry code.

## Contents

- Soft-float and VFP calling variants
- Why runtime helpers appear
- Integer and 64-bit helpers
- Soft-float arithmetic, comparison, and conversion
- Memory helpers
- What the helpers mean for reconstruction
- Linux system calls

## Soft-float and VFP calling variants

Determine the floating-point variant before recovering any float argument, because the two variants place the same\
arguments in different registers.

Under the base, soft-float variant, every argument travels in `r0`–`r3` and then the stack, floating-point values\
included. A double-word type occupies an even-aligned register pair (`r0:r1` or `r2:r3`) or a double-word-aligned stack\
slot. One argument at most may split between the last core registers and the stack. A result returns in `r0`, a\
double-word result in `r0:r1`, and a composite larger than four bytes through a caller-provided pointer passed as a\
hidden first argument in `r0`.

Under the VFP, hard-float variant, floating-point and short vector arguments, and homogeneous aggregates of one to four\
float or double members, travel in `s0`–`s15`/`d0`–`d7`, with the result in `s0`/`d0`/`q0`; `r0`–`r3` then carry only\
the integer arguments. The variant preserves `s16`–`s31` (`d8`–`d15`) across a call and treats `s0`–`s15` as volatile.\
Unused float registers back-fill from earlier alignment gaps until the first float argument spills to the stack.

A variadic function always uses the base variant, whatever the rest of the binary uses. Tell the variants apart from\
the call boundary: VFP load or move instructions marshalling values into `s`/`d` registers at a call site, or a\
`Tag_ABI_VFP_args` build attribute, indicate the VFP variant. Their absence does not prove soft-float, so confirm from\
an actual float-passing call rather than assuming.

## Why runtime helpers appear

A compiler emits a call to a standard helper when the hardware or the base instruction set cannot perform an operation\
inline: integer or 64-bit division, software floating point, and bulk memory moves. The helpers carry the vendor prefix\
`__aeabi_` (GCC also emits legacy libgcc names such as `__udivsi3` and `__divdi3` for the same roles). They are\
compiler-inserted, not\
application code, and they follow the base (soft-float) interface even on a core with floating-point hardware:\
arguments and results pass in the integer core registers. An implementation may corrupt `r0`–`r3`, `ip`, `lr`, and the\
condition flags, like any conforming call.

## Integer and 64-bit helpers

| Helper                                         | Computes                        | Register convention                                                   |
| ---------------------------------------------- | ------------------------------- | --------------------------------------------------------------------- |
| `__aeabi_idiv`, `__aeabi_uidiv`                | 32-bit signed/unsigned division | quotient in `r0`                                                      |
| `__aeabi_idivmod`, `__aeabi_uidivmod`          | 32-bit division with remainder  | `{quotient, remainder}` in `{r0, r1}`                                 |
| `__aeabi_ldivmod`, `__aeabi_uldivmod`          | 64-bit division with remainder  | quotient in `{r0, r1}`, remainder in `{r2, r3}`                       |
| `__aeabi_idiv0`, `__aeabi_ldiv0`               | divide-by-zero handler          | called by the division helpers; may return a value, or raise `SIGFPE` |
| `__aeabi_lmul`                                 | 64-bit multiplication           | result in `{r0, r1}`                                                  |
| `__aeabi_llsl`, `__aeabi_llsr`, `__aeabi_lasr` | 64-bit shifts                   | value in `{r0, r1}`, count in `r2`                                    |
| `__aeabi_lcmp`, `__aeabi_ulcmp`                | 64-bit comparison               | negative, zero, or positive in `r0`, like `strcmp`                    |

The `divmod` helpers returning two values in a register pair are the most common distortion: a decompiler may render\
the pair as a single scalar, or split one call into two. A lone quotient call is `idiv`/`uidiv`; a call whose remainder\
is also used is `idivmod`/`uidivmod`.

## Soft-float arithmetic, comparison, and conversion

Double-precision helpers take a `d` prefix, single-precision an `f`. Operands pass in source order, except the reverse\
helpers `drsub`/`frsub`, which compute `y - x`.

| Group            | Helpers                                                                                  | Note                                                            |
| ---------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Arithmetic       | `__aeabi_dadd`, `ddiv`, `dmul`, `dsub`, `drsub`; `fadd`, `fdiv`, `fmul`, `fsub`, `frsub` | map directly to a C arithmetic operator                         |
| Boolean compare  | `__aeabi_dcmpeq`, `dcmplt`, `dcmple`, `dcmpge`, `dcmpgt`, `dcmpun`; `fcmp*`              | return 1 or 0 in `r0`; `*un` is the C99 unordered test          |
| Flag compare     | `__aeabi_cdcmpeq`, `cdcmple`, `cdrcmple`; `cfcmp*`                                       | return the result in the CPSR `Z` and `C` flags, not `r0`       |
| Float to integer | `__aeabi_d2iz`, `d2uiz`, `d2lz`, `d2ulz`; `f2iz`, `f2uiz`, `f2lz`, `f2ulz`               | the `z` suffix rounds toward zero, matching a C cast to integer |
| Integer to float | `__aeabi_i2d`, `ui2d`, `l2d`, `ul2d`; `i2f`, `ui2f`, `l2f`, `ul2f`                       | —                                                               |
| Float width      | `__aeabi_d2f`, `f2d`; `h2f`, `f2h` (half precision)                                      | —                                                               |

A `d2iz` or `f2iz` call marks a C cast from floating point to `int`; a `dcmplt` feeding a conditional branch marks a\
`<` comparison on doubles.

## Memory helpers

| Helper                                                    | Role                     | Note                                                                                             |
| --------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------ |
| `__aeabi_memcpy`, `__aeabi_memcpy4`, `__aeabi_memcpy8`    | structure and block copy | the `4`/`8` forms assume that alignment; none must return `dest` in `r0`                         |
| `__aeabi_memmove`, `__aeabi_memmove4`, `__aeabi_memmove8` | overlapping copy         | as above                                                                                         |
| `__aeabi_memset`, `__aeabi_memset4`, `__aeabi_memset8`    | fill                     | argument order is `(dest, n, c)`: the length and fill byte are swapped relative to ANSI `memset` |
| `__aeabi_memclr`, `__aeabi_memclr4`, `__aeabi_memclr8`    | zero-fill                | the `c = 0` special case of `memset`                                                             |
| `__aeabi_read_tp`                                         | read the thread pointer  | preserves `r1`–`r3`; used for thread-local storage                                               |

A compiler replaces a C `memcpy`/`memset` with one of these when it can prove the alignment or ignore the return value,\
so a `__aeabi_memcpy4` call is a structure or array copy between four-byte-aligned objects. The swapped\
`__aeabi_memset` arguments are a frequent misread: the second register is the length and the third is the fill byte.

## What the helpers mean for reconstruction

Do not trace into a helper as if it were application logic; name the operation it stands for and move on. Read a\
multi-register return (`idivmod`, `ldivmod`, `lmul`) as one value, not several. Treat a helper call as evidence of the\
source-level operation: a division, a 64-bit arithmetic step, a float cast, or a block copy the C source expressed\
directly.

## Linux system calls

Three facts decide how a system-call site reads: the binary's ABI, the kernel's architecture, and the kernel version.\
Every EABI case shares one register convention. The code executes `svc #0`, in ARM or Thumb state, with the syscall\
number in `r7`. Arguments occupy `r0`–`r5`, six words with none on the stack, and a 64-bit argument starts at an even\
register pair, so `r1` or `r3` can be padding. The kernel returns the result in `r0`, or a value from -4095 to -1 that\
is a negated errno; a libc wrapper converts that value to a -1 return and sets `errno`.

| Environment                       | Number encoding                               | ARM-private calls                      |
| --------------------------------- | --------------------------------------------- | -------------------------------------- |
| 32-bit ARM kernel, EABI binary    | `r7`; the `svc` immediate is 0                | base `0xf0000`; set depends on version |
| 32-bit ARM kernel, OABI binary    | `swi 0x900000+N`, ARM state only; `r7` unused | same set, base `0x9f0000`              |
| arm64 kernel, AArch32 EABI binary | `r7`; OABI binaries do not run                | `cacheflush` and `set_tls` only        |

On a 32-bit ARM kernel, the ARM-private calls sit at the base plus n. Kernels v3.0 through v4.14 provide `breakpoint`,\
`cacheflush`, `usr26`, `usr32`, and `set_tls` (n = 1 to 5), and v4.15 adds `get_tls` (n = 6). Kernels up to v4.3 also\
define `cmpxchg` at n = `0xfff0`, private to the kernel's own pre-ARMv6 helper; user code should not contain it. A\
vendor kernel can add calls, so check the target kernel's `asm/unistd.h` when one is available. A 32-bit kernel runs\
OABI binaries only when built without EABI or with `CONFIG_OABI_COMPAT`. Native AArch64 code uses `svc #0` with the\
number in `x8` and arguments in `x0`–`x5`; its other conventions are outside this skill.

Tell the ABI apart before reading sites. The top byte of the ELF header's `e_flags` holds the Arm EABI version, 5 for\
current toolchains, which `readelf -h` decodes. A version of 0 means unknown conformance rather than OABI, so confirm\
from a site: a non-zero `svc` immediate in ARM code marks an OABI call.

Recover the number by propagating the constant from the nearest preceding write to `r7` (`mov r7, #N`, `movw`, or a\
literal load) on every path into the `svc`. When `r7` comes from a register or memory, the call is chosen at run time;\
leave it unresolved rather than guess. Map the number through the target kernel's own syscall table, because numbers\
differ between architectures and later kernels append calls.

As of Ghidra 12.2, the ARM and Thumb language definitions lower `svc` to a `software_interrupt` operation that takes\
only the immediate, so every EABI site decompiles as `software_interrupt(0)` with no visible argument or result.\
Ghidra's documented repair gives each syscall a body-less function in an overlay block of the `OTHER` space, and adds a\
`CALLOTHER_CALL_OVERRIDE` reference from the `svc` to it. The bundled `ResolveX86orX64LinuxSyscallsScript` automates\
that repair for x86 and x64 only; ARM needs an adapted script and a supplied number-to-name table.
