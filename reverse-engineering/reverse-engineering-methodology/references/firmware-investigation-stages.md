# Firmware investigation stages

The [OWASP Firmware Security Testing Methodology][fstm] provides a nine-stage assessment map: reconnaissance,\
acquisition, image analysis, filesystem extraction, content analysis, emulation, dynamic analysis, runtime analysis,\
and binary exploitation. Use its stages to locate missing evidence, not as a requirement to perform every operation. An\
explanation-only reverse-engineering request may end before execution or exploitation.

## Context and acquisition

Collect relevant CPU/OS/boot, component versions, manuals, source releases, update formats, and prior findings. Acquire\
firmware through the supplied authorized source and record model/build identity and hashes. Hardware acquisition,\
intercepted downloads, and chip access have their own authority and preservation requirements. Keep original capture\
bytes and any acquisition transformations separate from analysis copies.

## Image and filesystem analysis

Classify headers and boundaries before carving. Record offsets, sizes, checksums, and transformation parameters. High\
entropy alone cannot distinguish encryption from compression or random padding. Treat signature hits as candidates and\
validate the corresponding format before trusting an extractor's output. For NAND or encoded dumps, document any\
out-of-band removal or format conversion without discarding the original.

Extract into a fresh unprivileged location with resource limits and inspect results as untrusted data. Archive paths\
and symlinks must not escape the selected destination. Prefer userspace extraction to host mounts; mounting an unknown\
filesystem exposes the host kernel to the image parser. Follow startup configuration and component dependencies without\
executing extracted scripts. Choose binaries and inputs by the research question rather than reporting every suspicious\
string as a vulnerability.

## Execution and behavior

Determine whether one executable, one routine, or a whole-system image is needed. A guest kernel for a generic machine\
does not supply a proprietary board's peripherals or initialized device state. Use explicit input/environment models\
and record missing devices or stubs. Emulation can establish behavior under that model; physical equivalence requires\
relevant hardware evidence.

Dynamic and runtime analysis can add API/syscall traces, registers, memory, and decoded code/data. Select breakpoints\
or instrumentation that discriminate hypotheses from static analysis. For device-bound behavior that cannot execute,\
retain static corroboration and name the unresolved runtime dependency.

Exploitation is a separate possible assessment outcome, not an automatic escalation from analysis. Keep live traffic,\
hardware state changes, firmware patches, and attack execution within the user's actual scope.

[fstm]: https://github.com/scriptingxss/owasp-fstm
