---
name: firmware-security-testing
description: "Conduct a firmware security assessment with OWASP's Firmware Security Testing Methodology (FSTM), stage by stage: reconnaissance, obtaining and extracting firmware, analyzing a raw image and its filesystem, emulation, dynamic and runtime analysis, and exploitation of executables. Use when assessing or pentesting embedded or IoT device firmware end to end, planning which FSTM stage comes next, going from a firmware dump to an extracted filesystem, hunting hardcoded credentials or insecure boot in extracted contents, or turning a suspected memory-corruption bug into a proof of concept. For selecting the next experiment in an open-ended reverse-engineering investigation or tracking evidence across tools, use reverse-engineering-methodology; for deep single-tool operation, the matching tool skill."
license: MIT
compatibility: Each stage's tools are optional routes whose prerequisites must be checked for the selected target and host. Early stages use open-source intelligence and common file-format and binary inspection tools; emulators, debuggers, hardware debug adapters, fuzzers, and exploitation tools apply only to the stages that reach them.
metadata:
  author: Joonas Onatsu
---

# Firmware security testing (OWASP FSTM)

Work a firmware security assessment through the nine stages of the OWASP Firmware Security Testing Methodology\
(FSTM): reconnaissance, firmware acquisition, image analysis, filesystem extraction, content analysis,\
emulation, dynamic analysis, runtime analysis, and exploitation of executables. Each stage has its own reference\
below: what the stage is for, the concrete techniques and tools it uses, the commands and heuristics worth\
remembering, and that stage's own sources.

Reach a stage by the question in front of you, rather than running every stage in order. Use the stages to\
locate the evidence an assessment still lacks, not as a checklist to complete: an explanation-only request can\
stop before emulation or exploitation, and authority for acquisition, live traffic, hardware changes, firmware\
modification, and exploitation stays within the engagement's actual scope.

## Choose a stage

| Stage | Reference                                                                       | Read when you need to…                                                                                                                                                       |
| ----- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | [information gathering](references/01-information-gathering.md)                 | Open-source reconnaissance: manufacturer and certification sources, code repos, and the technical facts worth documenting before touching the device.                        |
| 2     | [obtaining firmware](references/02-obtaining-firmware.md)                       | Get a firmware image: direct download, intercepting an update, or reading it off the board through a debug port or a memory chip.                                            |
| 3     | [analyzing firmware](references/03-analyzing-firmware.md)                       | Turn a raw dump into a standardized binary and locate its sections: format conversion, entropy analysis, signature search, sectioning.                                       |
| 4     | [extracting the filesystem](references/04-extracting-filesystem.md)             | Identify and pull the filesystem(s) out of an image: magic numbers, `binwalk`, manual `dd` extraction, mounting.                                                             |
| 5     | [analyzing filesystem contents](references/05-analyzing-filesystem-contents.md) | Read the extracted filesystem without executing it: the boot process, startup scripts, credentials, and files of interest.                                                   |
| 6     | [firmware emulation](references/06-firmware-emulation.md)                       | Run the firmware, or one executable from it, virtually with QEMU, Unicorn, Renode, Qiling, or Firmadyne, removing the dependency on physical hardware.                       |
| 7     | [dynamic analysis](references/07-dynamic-analysis.md)                           | Study the device while it runs, emulated or real: debugger-attached emulation, physical debug ports, a targeted pentest pass, fuzzing, bootloader and firmware modification. |
| 8     | [runtime analysis](references/08-runtime-analysis.md)                           | Instrument, debug, trace, and log a live process: hardware and software debuggers, `strace`/`ftrace`, Frida, Qiling.                                                         |
| 9     | [exploitation of executables](references/09-exploitation-of-executables.md)     | Turn a suspected memory-corruption bug into a working proof of concept: the bug classes, the mitigations that block them, and the techniques that evade them.                |

## How the stages depend on each other

Working the stages roughly in order pays off: stage 4's filesystem extraction depends on stage 3 having located\
the right section, stage 6's emulation depends on stage 2's dump and stage 4's filesystem, and stage 9's\
exploitation only has a target once stages 5 and 7 have narrowed down a vulnerable executable. A real engagement\
loops back rather than running straight through: an encrypted section found in stage 3 or 4 routinely sends the\
work forward to stage 6 or 7 for the key material, then back.

## Deeper tool operation

Each stage reference carries what FSTM needs to drive its tools. For deeper operation of one tool, reach for the\
matching reverse-engineering skill: binary-file-identification for format and signature work in stages 3-4,\
qemu-emulation for stage 6, gdb-debugging and the embedded-debugging skills for the debug-port and runtime work\
in stages 7-8, and ghidra-firmware-analysis, radare2-firmware-analysis, or binary-analysis-patterns for the\
disassembly those stages lean on. Those skills own tool operation; this skill owns the FSTM stage procedures.\
For choosing the next experiment in an open-ended investigation or tracking evidence across tools,\
reverse-engineering-methodology owns that process.
