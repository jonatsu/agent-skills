# Reverse Engineering

Thirteen self-contained skills support evidence-driven investigation of binaries, firmware, protocols, and memory\
captures. Choose a skill by the question to answer. Tool requirements apply to the selected route, rather than the\
whole group.

## Choose a skill

| Question                                                                                    | Skill                                                                       |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Where should the investigation start, and what experiment comes next?                       | [reverse-engineering-methodology](reverse-engineering-methodology/SKILL.md) |
| What format or container is an unknown file or blob, judged from its signatures?            | [binary-file-identification](binary-file-identification/SKILL.md)           |
| What do native instructions, control flow, and data accesses mean?                          | [binary-analysis-patterns](binary-analysis-patterns/SKILL.md)               |
| How can Ghidra analysis, types, signatures, and names become more accurate?                 | [ghidra-firmware-analysis](ghidra-firmware-analysis/SKILL.md)               |
| How can radare2 query, corroborate, match, and preserve analysis?                           | [radare2-firmware-analysis](radare2-firmware-analysis/SKILL.md)             |
| How should ARMv7 ARM/Thumb instructions and ABI effects be interpreted?                     | [arm-assembly](arm-assembly/SKILL.md)                                       |
| What cryptographic construction is present, and does the evidence support a weakness?       | [crypto-analysis](crypto-analysis/SKILL.md)                                 |
| Can QEMU reach the behavior, and what host/guest prerequisites are missing?                 | [qemu-emulation](qemu-emulation/SKILL.md)                                   |
| Which inputs or path conditions satisfy a bounded routine?                                  | [symbolic-execution-tools](symbolic-execution-tools/SKILL.md)               |
| How does a custom bytecode interpreter encode and execute its program?                      | [vm-and-bytecode-reverse](vm-and-bytecode-reverse/SKILL.md)                 |
| How can debugger/VM checks, packing, or obfuscation obstacles be analyzed and circumvented? | [anti-reversing-techniques](anti-reversing-techniques/SKILL.md)             |
| What message structure and state does an undocumented protocol implement?                   | [protocol-reverse-engineering](protocol-reverse-engineering/SKILL.md)       |
| What do RAM images and process dumps establish about runtime behavior?                      | [memory-forensics](memory-forensics/SKILL.md)                               |

Methodology owns investigation planning and evidence tracking. File identification owns naming a format from its\
signatures, the step before binary analysis, which owns native-code interpretation. Tool\
skills own execution and tool-specific analytical judgment. Each package carries the essentials for its own job.

## Use and install

Copy an individual folder into the chosen client's skills directory, or select `reverse-engineering` as the Kasetto\
source group. The repository's [installation example](../README.md#using-a-skill) describes group selection. Adding the\
group to an existing managed installation requires a corresponding installer configuration entry before updating its\
pinned repository revision.

The skills discover relevant tools and recommend missing prerequisites; they do not assume permission to install them.\
Ghidra supports GUI/MCP and headless routes. Symbolic analysis separates angr from Triton, and custom bytecode machines\
remain distinct from hypervisor-detection checks. Research filing follows the consuming project's documentation setup.

Each package's `ATTRIBUTIONS.md` and `license` field describe its source relationships and redistribution terms.
