# OWASP FSTM stage 2: obtaining IoT device firmware

Stage 2 gets a firmware image onto disk, if [stage 1][stage-1]'s open-source search did not already produce one from\
the vendor's site. No single method works for every device; the choice ranges from a direct download to desoldering a\
flash chip, and the right one depends on what stage 1 found about the device's update path and board layout. Distilled\
from [Tarlogic's stage 2 write-up][source] (part of the OWASP FSTM series).

Keep more than one unit of the target device on hand: chip-off extraction risks partial or total physical damage, and\
the same board sometimes doubles as the ongoing test bench.

## Software-side extraction

Try these before opening the case.

- **Direct download.** Check whether the device is remotely upgradeable; an update-check menu is often the fastest path\
  to a copy. When the check only surfaces a download when a newer version exists, or runs over JavaScript, capturing\
  the check request/response can still retrieve the current firmware.
- **Intercept the update.** Audit the device's traffic instead: Wireshark's layered filtering finds the update exchange\
  quickly, and the transferred object becomes a firmware file once you've isolated it (assuming it went over the wire\
  unencrypted). The OWASP ISVS (IoT Security Verification Standard) guide is a good companion here. A wireless update\
  channel can be captured the same way with an SDR (GNU Radio, SigDigger), if the signal can be demodulated.

## Hardware-side extraction

When software-side extraction fails, disassemble the device: hidden screws under labels or rubber feet, or a glued-down\
display, are the usual obstacles. Get full access to the board.

### Reading a port

No single connector table covers every vendor's choices; some hide or leave test points unlabeled deliberately, others\
just ran short of board space. Tools for finding and confirming a port, cheapest first:

- **Multimeter.** Continuity mode maps a port's pins to a known ground point (many devices ground exposed metal for\
  regulatory reasons, and connectors often silkscreen the ground pin). Voltage mode identifies power pins and their\
  level, and can hint at communication activity, though not reliably.
- **Oscilloscope.** Visualizes a signal's voltage over time once its analog range is roughly known; a logic analyzer\
  beats it on cost and ease for a purely digital bus.
- **Logic analyzer.** Reads only high/low, not analog voltage, and most come with software that semi-automatically\
  recognizes common protocols from the captured waveform.
- **USB-UART converter.** Confirms a UART pinout cheaply once suspected from the tools above.
- **J-Link or similar hardware debugger.** Supports the ICSP/JTAG/J-Link family of protocols for reading, writing, and\
  debugging firmware directly.

A UART needs a common ground between the adapter and the target, and TX/RX crossed (the writer's `TX` goes to the\
reader's `RX`). Once wired, autodetect the baud rate (commonly 9600, 57600, or 115200) with a terminal program such as\
RealTerm or CoolTerm. If the boot log shows a bootloader such as U-Boot, interrupting the boot process sometimes\
reaches a shell that can dump memory directly; failing that, the device may present a root shell on boot instead, from\
which `cat`-ing a `/dev` block device through `printf` in hex captures an image to rebuild on the host.

### Reading a memory chip directly

When no port is accessible, identify the flash chip's package (an 8-pin SOIC8 at 1.27 mm pitch is common) and read it\
with a matching EEPROM/flash reader and clip. Chip package and command-set variants are numerous enough that the exact\
manufacturer and part number usually matter to the reader's software; an unsupported or non-standard part may need a\
custom adapter.

Software extraction, even of a signed update package, is often sufficient on its own for a security analysis. Hardware\
extraction takes more equipment and time but, between the two routes, firmware extraction is almost always achievable;\
it is not always achievable at a cost proportionate to the device.

## References

Distilled from OWASP FSTM / Tarlogic: [OWASP FSTM, stage 2: Obtaining IoT device firmware][source].

- [scriptingxss/owasp-fstm][owasp-fstm-repo] — the OWASP FSTM reference project this series is based on.
- [Microchip] — cited for EEPROM/flash part lookups when identifying a memory chip by package.

[microchip]: https://www.microchip.com
[owasp-fstm-repo]: https://github.com/scriptingxss/owasp-fstm
[source]: https://www.tarlogic.com/blog/owasp-fstm-obtaining-iot-device-firmware/
[stage-1]: 01-information-gathering.md
