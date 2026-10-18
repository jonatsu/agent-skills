# Acquisition and Input Verification

## Prefer the Supplied Image for Analysis

Identify raw physical memory, compressed/crash formats, process dumps, and hypervisor checkpoint formats from metadata\
and a format-aware reader. File extensions alone are not reliable. Preserve hashes, original name, source identity,\
available acquisition time/timezone, tool/version, and accompanying metadata.

A raw image need not equal installed RAM size. Reserved ranges, sparse representation, compression, capture format, and\
unreadable pages can change size. Conversely, a plausible size does not prove completeness. Check format headers,\
documented address coverage, missing/truncated ranges, and analyzer diagnostics.

VM snapshots may require configuration or companion files to resolve physical mapping. Do not assume every `.vmem` or\
saved-state file is interchangeable raw RAM. A process dump lacks many kernel and unrelated process artifacts. A\
reconstructed executable extracted from memory is another distinct input type.

## Plan Acquisition Separately

Confirm authorized system/VM, acquisition objective, tolerated pause or footprint, destination capacity, privileges,\
compatible capture tool, and recovery before live action. Capture can alter memory, load drivers, pause a guest, and\
write sensitive data. Record those effects rather than claiming a pristine instant snapshot.

On Windows, select a supported acquisition utility with compatible driver signing and target-build support. On Linux, a\
kernel-module approach needs a matching kernel/build environment and permission to load it. On macOS, current hardware\
and platform protections constrain available methods; historical tool names do not establish support. Read the selected\
tool's official release instructions before proposing a command.

Do not use copying `/proc/kcore` or `/dev/mem` as a universal physical-memory acquisition recipe. Access and content\
are platform/configuration dependent, and the resulting artifact may not meet the intended analyzer contract.

For a hypervisor, discover its documented memory-only dump or checkpoint export behavior, required permissions,\
companion metadata, guest pause semantics, and output format. An existing management connection does not authorize\
interrupting another guest. Present any required operational decision before the capture step.

## Prerequisite Recommendations

Determine host OS/version and selected capture route. Use its package catalog and official tool instructions to verify\
names and compatibility. State the missing tool, why needed, required privilege, expected footprint, and whether\
offline analysis can continue. Installing a capture driver or changing kernel security settings needs separate\
authority; it is not an automatic dependency repair.

## Preserve and Check the Result

Hash the resulting artifact, record acquisition start/end and interruptions if available, and verify that the selected\
reader can open representative mapped ranges. Preserve error logs and coverage metadata. Acquisition smear can combine\
objects from different moments; correlate timestamps cautiously. Store captures and derived private artifacts with\
access controls appropriate to their contents.
