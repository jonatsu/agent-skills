# OWASP FSTM stage 6: firmware emulation

Stage 6 runs the firmware, or one executable from it, virtually rather than on the physical device, using\
[stage 2][stage-2]'s dump and [stage 4][stage-4]'s extracted filesystem. Emulation removes the hardware bottleneck from\
testing: several attack strategies can run in parallel from a single extracted image, and a service with a bounded\
retry limit can be tested indefinitely by restarting the emulator instead of the device. Distilled from\
[Tarlogic's stage 6 write-up][source] (part of the OWASP FSTM series).

Emulation comes in two grades, in increasing cost: **partial** (user-space), emulating one service or executable, and\
**total** (system-wide), emulating the whole device. Partial emulation only works when every input the executable\
needs, files, peripherals, other processes, is supplied by hand; total emulation is almost always the more expensive of\
the two, since hardware and software are tightly coupled and changing one without faithfully replicating the other\
typically breaks execution. Choosing between them, and how much peripheral emulation a partial run actually needs,\
should draw on everything [stage 1][stage-1] already learned about the target's architecture and hardware.

## Options, in increasing order of effort

- **User-space emulation of one executable.** The emulator supplies a generic kernel to load and run a binary built for\
  another architecture. Tools: QEMU (`qemu-<arch>-static`), Qiling.
- **User-space emulation with simulated files.** When an executable expects hardware-backed file behavior, CUSE or FUSE\
  can stand in for the real device without emulating a kernel.
- **System emulation without a bootloader.** Load and run a kernel directly in memory; may need custom code to emulate\
  whatever physical devices that kernel expects at boot.
- **Full system emulation from earliest initialization.** The most effortful mode, and correspondingly the one needed\
  when a firmware's compression or encryption is undocumented or obfuscated, precisely the case where documentation is\
  scarcest.

## Tools

- **QEMU.** "System emulation" mode models a full virtual machine (CPU, memory, virtual devices), optionally under a\
  hypervisor (KVM, Xen, Hax); "user emulation" mode (`qemu-<arch>`) emulates just the source CPU and translates\
  instructions to the host. Prefer the `-static` build for either mode: a static binary carries no dependency on host\
  system libraries, which matters when the working directory is a chroot that should not also carry the host's own\
  libraries.
- **Unicorn.** A CPU-emulation library, not a full-system emulator, exposed through a simple multi-language API, built\
  for flexible, high-performance emulation of isolated code fragments and low-level dynamic analysis. Its flexibility\
  costs setup time: expect to write custom peripheral emulation and to need real platform knowledge before a target\
  runs.
- **Renode.** QEMU-based, purpose-built for IoT/embedded and real-time-OS targets (though capable of Linux too), with\
  sensor, display, and FPGA-hardware bridging. Configuring it means mapping devices to memory regions (MMIO); a device\
  tree blob (DTB), often present in firmware, or the vendor's manual, supplies that mapping. Typical workflow: start\
  with a minimal device set, run until something fails, add the missing device, repeat.
- **Qiling.** A Python framework on top of Unicorn, adding filesystem emulation, dynamic-library loading, and other\
  high-level OS behavior Unicorn alone lacks; needs the extracted firmware's own filesystem alongside the target\
  executable. Integrates with AFL++ for fuzzing an emulated target.
- **Firmadyne.** Automates filesystem extraction, architecture identification, and building a runnable VM from a\
  firmware image, plus web-service inspection, SNMP enumeration, and Metasploit testing modules. Easier to get running\
  than the alternatives, but weaker execution-flow control and more error-prone; GDB integration needs a statically\
  compiled `gdbserver` added to the firmware's own filesystem.
- **ARMX.** A script/kernel/filesystem bundle over QEMU targeting an ARM-IoT virtual machine, with eleven ARM device\
  models supported directly and documented steps for adding a new one.

## Worked example: emulating one executable with QEMU

1. Identify architecture and endianness: `readelf -h <binary>` (QEMU defaults to little-endian when unspecified).
2. Copy the matching static QEMU binary (e.g. `qemu-x86_64-static`) into the working directory, alongside the unpacked\
   filesystem and target executable.
3. Run it: `./qemu-x86_64-static ./<binary> [args]` for a self-contained executable, or\
   `sudo chroot . ./qemu-<arch>-static [options] <filename>` when it depends on the rest of the filesystem.
4. Trace syscalls with `-strace`: `qemu-x86_64-static -strace <binary> [args]`, to watch kernel interaction in real\
   time.

A successful emulation reproduces the native run's output exactly; the `-strace` trace confirms which syscalls ran\
during startup (`arch_prctl`, `sched_getaffinity`, `mmap`, and similar, in the QEMU documentation's own `devd`\
example).

A finding that only reproduces in emulation is not automatically real on the physical device: a working exploit there\
can depend on a parameter the emulation modeled incorrectly or not at all, so treat an emulation-only result as a\
strong lead until it is checked against the physical device.

## References

Distilled from OWASP FSTM / Tarlogic: [OWASP FSTM step 6: firmware emulation][source].

- [scriptingxss/owasp-fstm][owasp-fstm-repo] — the OWASP FSTM reference project this series is based on.
- [qemu/qemu][qemu] — the QEMU machine emulator and virtualizer.
- [renode/renode][renode] and its [documentation][renode-docs] — the Renode embedded-emulation framework, with its\
  supported-device and board lists.

[owasp-fstm-repo]: https://github.com/scriptingxss/owasp-fstm
[qemu]: https://github.com/qemu/qemu
[renode]: https://github.com/renode/renode
[renode-docs]: https://renode.readthedocs.io/en/latest/
[source]: https://www.tarlogic.com/blog/owasp-fstm-step-6-firmware-emulation/
[stage-1]: 01-information-gathering.md
[stage-2]: 02-obtaining-firmware.md
[stage-4]: 04-extracting-filesystem.md
