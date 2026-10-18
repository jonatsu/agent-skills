# Mitigation Interpretation

## Inspect Static Indicators First

Discover tool availability and versions before using them. For ELF, `readelf --help` exposes header, program-header,\
dynamic-section, symbol, relocation, and note inspection. `checksec` implementations have different command syntax;\
inspect the installed implementation rather than assuming an upstream command line.

| Feature         | Useful evidence                                                               | Consequence for analysis and limit                                                  |
| --------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| PIE             | ELF type, entry/interpreter context, relocation and dynamic flags             | Executable may be rebased; ET_DYN alone also describes shared libraries             |
| ASLR            | Runtime mappings across comparable launches and process/system policy         | Runtime property; PIE metadata does not establish randomization                     |
| NX or DEP       | ELF GNU_STACK flags, segment permissions, runtime mappings                    | Stack policy differs from permissions of every executable mapping                   |
| Stack protector | Guard load/check sequence and failure path in a function                      | Imported failure symbol does not prove every function is protected                  |
| RELRO           | GNU_RELRO range and eager binding flags                                       | Loader protects relocation-related ranges; confirm runtime range and permissions    |
| Fortification   | Checked-library calls, inline checks, sizes and failure paths                 | Coverage depends on compiler knowledge and individual call site                     |
| CET             | Architecture notes, landing instructions, loader/OS support and runtime state | Advertised support is distinct from enforced indirect-branch or shadow-stack policy |
| MTE             | AArch64 instructions, tagged accesses, allocation and OS configuration        | Capability does not prove that checked tagged memory is in use                      |

For PE and Mach-O, use format-aware header/load-command tools and runtime mappings. Do not interpret ELF-specific flags\
as universal indicators. Separate binary capability, OS policy, loader activation, and per-region state.

## Explain Observed Differences

Record file offset, image-relative location, preferred analysis base, runtime module base, and the conversion between\
them. Repeated observations need the same module identity and comparable launch conditions. A debugger may alter\
process randomization; inspect its settings before attributing all differences to the binary.

A guard failure can indicate corrupted stack state, a wrong emulation model, or a deliberately forced path. A write or\
execute fault may reflect page permissions, missing mappings, invalid address conversion, or unrelated memory\
corruption. Trace the failing access and mapping before classifying it as protection behavior.

Fortified printing checks are not usefully classified by positional versus sequential `%n` notation. Glibc\
[fortification documentation](https://sourceware.org/glibc/manual/latest/html_node/Source-Fortification.html) describes\
additional checks including the read-only format-string requirement. Explain the actual checked call and failure\
condition rather than inheriting an alleged notation-based bypass.

## Deliver the Constraints

Report the indicator, affected region or function, runtime verification where available, and what remains unknown. Keep\
inspection read-only unless a separate analysis operation authorizes a controlled intervention. Exploit chains,\
mitigation defeat, and host-wide disabling of protections are outside this interpretation workflow.
