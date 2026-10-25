# OWASP FSTM stage 4: extracting the filesystem

Stage 4 identifies and pulls the filesystem(s) out of a firmware image, building on [stage 2][stage-2]'s dump and\
[stage 3][stage-3]'s section analysis. A filesystem can sit in the clear, compressed, or encrypted; the first two need\
only the right identification and extraction tool, while an encrypted one needs more vendor research or a trip forward\
to [stage 6][stage-6]/[stage 7][stage-7]. Distilled from [Tarlogic's stage 4 write-up][source] (part of the OWASP FSTM\
series).

## Identifying the filesystem

`file` names a filesystem directly when it starts at the very beginning of the image, but more often the image opens\
with a bootloader or a blank section first. `strings` finds a filesystem's magic number even off a fixed offset; common\
embedded filesystem and compression magics:

| Format                   | Magic bytes               |
| ------------------------ | ------------------------- |
| CramFS                   | `45 3D CD 28`             |
| UBIFS                    | `31 18 10 06`             |
| JFFS2                    | `85 19`                   |
| SquashFS (little-endian) | `73 71 73 68` (`sqsh`)    |
| SquashFS (big-endian)    | `68 73 71 73` (`hsqs`)    |
| zip                      | `50 4B 03 04`             |
| rar                      | `52 61 72 21 1A 07 01 00` |
| 7z                       | `37 7A BC AF 27 1C`       |
| xz                       | `FD 37 7A 58 5A 00`       |

Byte order in a signature follows the image's endianness, and some vendors modify a filesystem's magic outright to fit\
their build or to obfuscate it: DD-WRT's router firmware, for example, can carry `tqsh` (big-endian) instead of the\
standard SquashFS magic. `binwalk -E`'s entropy study (as in [stage 3][stage-3]) separates a compressed section (high\
entropy, a signature usually nearby) from an encrypted one (uniformly high entropy, no signature at the boundary); the\
latter needs vendor research or a later stage before it yields.

## Extracting it

`binwalk` (no flags) reports every section it detects; `binwalk -e` extracts them automatically into\
`firmware/<filesystem_type>`, covering SquashFS, UBIFS, RomFS, RootFS, JFFS2, YAFFS2, CramFS, and initramfs. Its\
signature-based detection produces frequent false positives, especially on 1-2 byte signatures, so verify every hit in\
a hex editor, and expect the occasional extraction failure or corrupted output. When that happens, fall back to a\
manual extraction:

1. Get the filesystem's offset and, if available, size from `binwalk` or `fdisk -l`.
2. Cut the section out: `dd if=firmware.img of=section bs=1 skip=<offset> count=<size>`.
3. Extract with the format-specific tool: `unsquashfs` or `sasquatch` for SquashFS, `cpio` for cpio, `jefferson` for\
   JFFS2, `uncramfs` or `cramfsck` for CramFS.

A firmware image can also carry a full partition table (FAT, NTFS, ext) rather than a bare filesystem; `fdisk -l`\
reveals it, and `kpartx -a` (or `losetup`) creates loop devices per partition for `mount`. When a partition's declared\
size does not match its actual extent, the kernel driver refuses to mount it (`extends beyond EOD`); extract that\
partition to its own file with `dd` and mount it with `squashfuse` instead, since the FUSE driver tolerates the size\
mismatch the kernel one does not.

When a vendor has deliberately altered a filesystem's signature or layout and `binwalk` cannot produce consistent\
results, fall back to manual hex-editor analysis using whatever vendor-specific detail [stage 1][stage-1] already\
surfaced; vendor or device forums occasionally document the variant and its extraction tool ahead of you.

SquashFS and CramFS are the most common embedded filesystem formats, with JFFS2, UBIFS, RomFS, and cpio also frequent.\
`binwalk` automates most of the detection and extraction, but `file`, `strings`, a hex editor, `dd`, and `fdisk` stay\
necessary for the cases it gets wrong.

## References

Distilled from OWASP FSTM / Tarlogic: [OWASP FSTM, stage 4: Extracting the filesystem][source].

- [scriptingxss/owasp-fstm][owasp-fstm-repo] — the OWASP FSTM reference project this series is based on.
- [Firmware Mod Kit (Kali tools)][fmk] — a packaged toolset for unpacking and repacking common firmware filesystem\
  formats.
- [OWASP/IoTGoat][iotgoat] — the deliberately vulnerable firmware image used in the worked examples.
- [Pen Test Partners, "How to do firmware analysis: tools, tips and tricks"][pentestpartners] — a companion\
  practitioner walkthrough of the same extraction techniques.
- [k3170makan, "Reverse Engineering Primer: Unpacking Firmware"][k3170makan] — a worked binwalk/entropy unpacking\
  example.

[fmk]: https://www.kali.org/tools/firmware-mod-kit/
[iotgoat]: https://github.com/OWASP/IoTGoat/
[k3170makan]: https://blog.k3170makan.com/2018/06/reverse-engineering-primer-unpacking.html
[owasp-fstm-repo]: https://github.com/scriptingxss/owasp-fstm
[pentestpartners]: https://www.pentestpartners.com/security-blog/how-to-do-firmware-analysis-tools-tips-and-tricks/
[source]: https://www.tarlogic.com/blog/owasp-fstm-stage-4-extracting-the-filesystem/
[stage-1]: 01-information-gathering.md
[stage-2]: 02-obtaining-firmware.md
[stage-3]: 03-analyzing-firmware.md
[stage-6]: 06-firmware-emulation.md
[stage-7]: 07-dynamic-analysis.md
