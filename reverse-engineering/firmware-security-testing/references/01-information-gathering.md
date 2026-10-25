# OWASP FSTM stage 1: information gathering and reconnaissance

Stage 1 collects everything findable about a target device before touching it, using open-source intelligence (OSINT)\
rather than a physical unit. The point is not volume: too little context and too much unfiltered information both slow\
the later stages down, so the search stays organized around what the next stages actually need. Distilled from\
[Tarlogic's stage 1 write-up][source] (part of the OWASP FSTM series).

## Where to look

- The manufacturer's own site: technical specs, drivers, apps, and sometimes datasheets, firmware, schematics, or\
  teardown photos directly.
- The manufacturer's regional sites: different jurisdictions can force disclosure of different detail about the same\
  product.
- Other manufacturers' sites: a rebadged, jointly developed, or inherited (via merger or acquisition) product can be\
  internally identical to the target while exposing documentation the target's own vendor does not.
- Certification registries (FCC and PTCRB in the US, IC and PTCRB in Canada, CE/GCF/RoHS in Europe, TELEC in Japan):\
  compliance reports can include internal photos, hardware detail, prototype photos, and third-party supplier\
  documents.
- Code repositories (GitHub, GitLab, BitBucket, SourceForge, or a vendor's own FTP server): open-source license terms\
  often force publication of at least part of the firmware's source, and some jurisdictions let a requester compel\
  disclosure when a vendor ignores that obligation.
- Vendor and product-specific forums: useful, but needs heavier filtering than official sources.

## What to document, and why it matters later

- **CPU architecture.** Simplifies reversing and emulation ([stage 3][stage-3], [stage 6][stage-6]) and flags\
  security-relevant peripherals (crypto modules, TPMs, trusted execution zones) that may hold secrets or encrypt part\
  of the platform.
- **OS platform.** Open-source systems accumulate more known vulnerabilities but get them fixed faster; closed-source\
  systems patch more slowly. A managed IoT platform (AWS IoT, GCP IoT, Azure IoT, Zephyr OS) eases testing and OTA\
  updates; otherwise expect a vendor-customized embedded Linux with its own update process.
- **Bootloader setup** (U-Boot, Libreboot, the Android bootloader, CFE). An unprotected disk-loader recovery mode can\
  dump the OS along with the keys and certificates it uses; see [stage 7][stage-7] for bootloader interaction once\
  hardware is in hand.
- **Hardware schematics**, official or reverse-engineered: identify buses that can be read raw or manipulated, a direct\
  expansion of the attack surface.
- **Component datasheets**, especially ROM (SPI flash, eMMC) and encryption chips: the highest-value components for\
  [stage 2][stage-2] extraction and later attack-surface work.
- **Estimated source lines of code (SLOC).** A small binary favors reversing (a bounded time investment); a large one\
  favors fuzzing ([stage 7][stage-7]), since more code raises the odds a fuzzing budget finds a bug.
- **Change logs.** A hardware bug can only be fixed by a new product revision, unlike a software bug; a device with no\
  OTA policy stays vulnerable to every logged bug indefinitely.
- **Design and dataflow diagrams**, from the vendor's site or executive material; absent these, approximate the\
  device's operation well enough to find its most likely input vectors.
- **Prior penetration-test reports and bug trackers.** Rule out already-explored paths quickly, or find a reported\
  defect worth chasing on an older firmware version still in the field. Downloading a vendor's own repositories to run\
  its already-configured static/dynamic security tests is often worth the time: the code is usually solid, but not\
  always.

## References

Distilled from OWASP FSTM / Tarlogic: [OWASP FSTM, stage 1: Information gathering and reconnaissance][source].

- [scriptingxss/owasp-fstm][owasp-fstm-repo] — the OWASP FSTM reference project this series is based on.

[owasp-fstm-repo]: https://github.com/scriptingxss/owasp-fstm
[source]: https://www.tarlogic.com/blog/owasp-fstm-information-gathering/
[stage-2]: 02-obtaining-firmware.md
[stage-3]: 03-analyzing-firmware.md
[stage-6]: 06-firmware-emulation.md
[stage-7]: 07-dynamic-analysis.md
