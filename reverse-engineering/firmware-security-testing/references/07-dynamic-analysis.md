# OWASP FSTM stage 7: dynamic analysis

Stage 7 studies the device actually running, emulated ([stage 6][stage-6]) or on the physical unit, to dig into the\
weak points [stages 3-5][stage-3] already flagged. Emulation supports deeper study when no hardware debug port exists,\
since emulation frameworks commonly expose a GDB connection; running on the original hardware is simpler and more\
reliable but shallower. Set this stage's objectives from the earlier findings rather than running every technique below\
unfocused: doing so turns the stage into an unfocused traditional pentest instead of a targeted one. Distilled from\
[Tarlogic's stage 7 write-up][source] (part of the OWASP FSTM series).

## Debugging an emulated system

With a working emulation, attaching GDB (directly, or via a `gdbserver` the emulation framework runs) to control\
execution is one of the most useful techniques here, especially for bootloader and kernel internals that are hard to\
study any other way. Combining this with fuzzing enables attacks on the bootloader, kernel, or OS that a traditional\
pentest cannot reach. It is also a reliable way to recover a decrypted or unpacked firmware image: locate the boot\
entry point (an init script or equivalent), set a breakpoint just before it runs, run to that breakpoint, then dump the\
image from memory with the debugger.

## Physical debug ports

Some hardware exposes a developer-only JTAG or UART port that production units failed to disable. A JTAG connection\
typically allows reading and writing ROM/RAM directly; further real-time interaction through known memory mappings\
needs its own study and automation first. A debug UART can reach the bootloader through a terminal and, combined with\
memory access, control the execution flow.

## Traditional pentest pass

Once the firmware is running, standard pentest technique applies, steered by what earlier stages already found:

- **Network reconnaissance**: `nmap`, with its OS/service/version-detection extensions, maps open ports and the server\
  versions behind them.
- **Vulnerability discovery**: cross-reference the detected versions against the NVD or exploit-db.
- **Web pentesting**: a common surface on IoT devices, and complex enough to carry its own bugs; Burp, ZAP, and\
  DirBuster remain the standard tools, and the filesystem analysis from [stage 5][stage-5] should already explain the\
  backend behind whatever the web UI shows.
- **Communications analysis**: vendor-specific or lightly tested protocol implementations are common in IoT devices and\
  often hide undiscovered bugs; use what earlier stages learned about the system to target the non-standard ones first.
- **Vulnerability exploitation**: confirm feasibility once a candidate is found, using an existing PoC or Metasploit\
  module where one exists, or returning to [stage 5][stage-5]'s executable analysis for the deeper study a novel bug\
  needs.

IoT firmware tends to run older versions of otherwise well-tested components; the vendor's own custom code, not those\
upstream components, is usually where the real bugs are.

## Fuzzing

Fuzzing automates finding implementation bugs by feeding a target malformed input. Three variants: **application\
fuzzing** (mutating input data to find code-level bugs, usable white-box or black/gray-box), **file-format fuzzing**\
(mutating both data and container structure to find a parser's deviations from its format standard), and **protocol\
fuzzing** (the same idea against a communication protocol, generated directly or via a mutating proxy). Tooling: AFL++,\
FormatFuzzer, CryptoFuzz, and Google's ClusterFuzz, the last credited with over 25,000 bugs in Google's own products\
and 36,000+ across 550+ open-source projects as of May 2022, a measure of what fuzzing finds at scale.

## Bootloader modification

Manipulating bootloader kernel parameters is a common way to reach an administrator terminal directly, when the vendor\
left the boot process insufficiently protected; the same access can load modified firmware or a modified U-Boot image,\
or reveal enabled debug functionality. It needs either a debug port or a directly connected monitor/keyboard, and often\
a specific key combination to interrupt an otherwise-unprotected bootloader. Useful U-Boot commands once at that\
terminal:

```
printenv                                        # list current environment variables
setenv bootargs ... init=/bin/bash ...          # edit bootargs to launch a root shell at startup
saveenv                                          # persist the change
boot                                             # apply it (or reset the device)
```

Loading a modified U-Boot image over TFTP to gain root: set `ipaddr`/`serverip`, `saveenv`, reset, confirm reachability\
with `ping`, then `tftp ${loadaddr} <ubootImage>` to fetch and stage the image at the given memory address for the next\
boot. [`ubootwrite.py`][ubootwrite] performs the equivalent over a UART interface instead of a network.

## Firmware modification

When a device does not verify firmware origin, loading a modified image carrying a deliberate backdoor (an SSH terminal\
with admin rights starting at boot, for example) is a direct way to get root access for the rest of the analysis. This\
needs the extracted filesystem, the tools to unpack and repackage the image, and a boot-process read to find the right\
insertion point. Keep the modified image's final size unchanged wherever possible: a size change is the most common\
reason a modified image fails to boot. Toolchain choice for compiling the backdoor is architecture- and\
vendor-specific; most embedded architectures (MIPS, ARM, and similar) have a `gcc` target available. Test the compiled\
backdoor in a virtualized environment ([stage 6][stage-6]'s QEMU or chroot) before flashing it, given the size\
constraint, then repackage with the firmware's own packaging tools and upload it as an update.

## References

Distilled from OWASP FSTM / Tarlogic: [OWASP FSTM, step 7: Dynamic analysis][source].

- [scriptingxss/owasp-fstm][owasp-fstm-repo] — the OWASP FSTM reference project this series is based on.
- Securelist, ["Dynamic analysis of firmware components in IoT devices"][securelist] — a companion writeup on the same\
  technique set.
- Open Source For You, ["Dynamic Analysis of Firmware Using Firmadyne"][osfy-firmadyne] — a Firmadyne-specific\
  walkthrough.
- Kaspersky ICS-CERT, ["Dynamic analysis of firmware components in IoT devices"][kaspersky-ics] — the same Securelist\
  report, republished.
- [U-Boot documentation: environment variables][uboot-env] and the\
  [linux-sunxi U-Boot configuration reference][linux-sunxi-uboot] — the `bootargs`/`setenv`/`saveenv` mechanics used\
  above.
- eTutorials, ["Setting Up the Bootloader: U-Boot"][etutorials-uboot] — background on U-Boot's role in the embedded\
  Linux boot process.
- [HorstBaerbel/ubootwrite][ubootwrite] — loads a U-Boot image over UART instead of TFTP.

[etutorials-uboot]: https://etutorials.org/Linux+systems/embedded+linux+systems/Chapter+9.+Setting+Up+the+Bootloader/9.5+U-Boot/
[kaspersky-ics]: https://ics-cert.kaspersky.com/publications/reports/2022/07/06/dynamic-analysis-of-firmware-components-in-iot-devices/
[linux-sunxi-uboot]: https://linux-sunxi.org/U-Boot/Configuration
[osfy-firmadyne]: https://www.opensourceforu.com/2018/09/dynamic-analysis-of-firmware-using-firmadyne/
[owasp-fstm-repo]: https://github.com/scriptingxss/owasp-fstm
[securelist]: https://securelist.com/dynamic-analysis-of-firmware-components-in-iot-devices/106901/
[source]: https://www.tarlogic.com/blog/owasp-fstm-dynamic-analysis/
[stage-3]: 03-analyzing-firmware.md
[stage-5]: 05-analyzing-filesystem-contents.md
[stage-6]: 06-firmware-emulation.md
[uboot-env]: https://u-boot.readthedocs.io/en/latest/usage/environment.html
[ubootwrite]: https://github.com/HorstBaerbel/ubootwrite
