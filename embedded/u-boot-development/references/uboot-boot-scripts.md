# U-Boot Boot Scripts and Images

Trace the active boot framework and file selection before editing a script or image. Examples use upstream v2025.10;
resolve board addresses, paths, formats and enabled commands before running them.

## Contents

- [Boot selection](#boot-selection)
- [Guarded loads](#guarded-loads)
- [Image commands](#image-commands)
- [Signed FIT construction](#signed-fit-construction)
- [Network loading](#network-loading)

## Boot selection

Inspect `bootcmd` and generated defaults. For legacy distro boot, `boot_targets` orders devices/targets such as `mmc0`
and `usb0`, not a global list of boot methods. The scan iterates prefixes, usually `/ /boot/`, trying extlinux before
scripts **within each prefix**. Thus `/boot.scr` can run before `/boot/extlinux/extlinux.conf`, while extlinux wins when
both candidates are under the same prefix and boot succeeds. Failed or returning candidates can continue the scan.
See [config_distro_bootcmd.h](https://github.com/u-boot/u-boot/blob/v2025.10/include/config_distro_bootcmd.h).

For bootstd, inspect enabled bootdevs/bootmeths and their actual order using the release's `bootflow`/`bootmeth` commands
and configuration. Do not assign a framework from the release date alone; vendor defaults can retain legacy scripts.
Reproduce the selected device, partition, prefix and method before changing a file that might never be read.

An illustrative extlinux entry, for a filesystem containing these paths and a separately identified root filesystem:

```text
label linux
    kernel /boot/Image
    fdt /boot/board.dtb
    append console=ttyS0,115200 root=PARTUUID=<root-partition-uuid> rootwait
```

The UUID and console are project inputs. Confirm supported fields from the release's parser; `fdtdir`, overlays, initrd,
menu handling and image support depend on configuration. Environment expansion in `append` makes the environment an
input to the final kernel command line. An editable extlinux file is not authenticated merely because its kernel is
signed. For an authorized manual boot, `sysboot mmc <dev:part> any <safe-config-address> <config-path>` loads and runs
the selected configuration; it is not inspection.

## Guarded loads

U-Boot semicolons do not stop on failure. Use nested conditionals so a failed first or second load cannot execute stale
RAM. This **Hush template** assumes authorized MMC 0:1, a raw Image, and prevalidated non-overlapping RAM capacities.
`validate_loaded_pair` is a project-supplied validation command variable; its absent/failing status prevents boot.
It must check recorded lengths against capacities, expected formats and artifact identities before returning success.
A short memory dump or a DT model string cannot supply those checks.

```text
if load mmc 0:1 ${kernel_addr_r} /boot/Image; then
    setenv kernel_size ${filesize}
    if load mmc 0:1 ${fdt_addr_r} /boot/board.dtb; then
        setenv fdt_size ${filesize}
        if run validate_loaded_pair; then
            booti ${kernel_addr_r} - ${fdt_addr_r}
        else
            echo "Loaded artifacts rejected"
        fi
    else
        echo "DT load failed"
    fi
else
    echo "Kernel load failed"
fi
```

Bound the inputs before loading as well: checking overlap after a load cannot undo memory corruption. Account for FIT
expansion, decompression and relocation destinations, U-Boot's own state, DT padding and reserved memory. When loading a
ramdisk, save `ramdisk_size` immediately and use that value rather than a later load's `filesize`.

To wrap a reviewed command file as a legacy script on the host:

```bash
mkimage -T script -n 'Board boot sequence' -d boot.cmd boot.scr
```

Regenerate after every source change. Guard loading and execution too:

```text
if load mmc 0:1 ${scriptaddr} /boot.scr; then
    setenv script_size ${filesize}
    if run validate_loaded_script; then
        source ${scriptaddr}
    fi
fi
```

`validate_loaded_script` is likewise a required project validation variable, not a built-in command. Validate capacity
before loading and identity before `source`. Legacy script CRCs detect damage but do not authenticate the author.
Use an enforcing authenticated path where the threat model requires it.

## Image commands

| Command   | Select only with these prerequisites                                                                                                          |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `booti`   | Supported architecture's Image; configured compressed formats also need `kernel_comp_addr_r`, `kernel_comp_size` and safe decompression space |
| `bootz`   | Supported zImage and architecture/build support                                                                                               |
| `bootm`   | Supported FIT or enabled legacy uImage; named FIT configuration uses `address#configuration`                                                  |
| `bootefi` | Supported EFI application/stub, enabled loader and compatible architecture/DT                                                                 |

Use `<ramdisk-address>:<captured-ramdisk-size>` where a raw ramdisk size is required, or `-` for none. Confirm syntax
with release-matched command help. The [booti contract](https://docs.u-boot.org/en/v2025.10/usage/cmd/booti.html) includes
compressed formats and decompression memory requirements; it is not limited to uncompressed arm64 files in every build.

## Signed FIT construction

A FIT's hashes detect component damage. A configuration signature authenticates the selected composition only when the
trusted verifier enforces it. The example below is a host-side schema example for arm64, with deliberately
board-specific load/entry addresses that must be replaced from the board memory map. It includes a real signing node.

```dts
/dts-v1/;
/ {
    description = "Board kernel and device tree";
    #address-cells = <1>;
    images {
        os-image {
            data = /incbin/("Image");
            type = "kernel";
            arch = "arm64";
            os = "linux";
            compression = "none";
            load = <0x80080000>;
            entry = <0x80080000>;
            hash-1 { algo = "sha256"; };
        };
        board-tree {
            data = /incbin/("board.dtb");
            type = "flat_dt";
            arch = "arm64";
            compression = "none";
            hash-1 { algo = "sha256"; };
        };
    };
    configurations {
        default = "boot-main";
        boot-main {
            kernel = "os-image";
            fdt = "board-tree";
            signature-1 {
                algo = "sha256,rsa2048";
                key-name-hint = "release";
                sign-images = "kernel", "fdt";
            };
        };
    };
};
```

In a new task-owned host directory, prepare a test RSA key/certificate as `keys/release.key` and `keys/release.crt`.
Use protected production signing infrastructure for release keys. With a copy of the verifier's actual control DT:

```bash
mkimage -f image.its -k keys -K verifier-control.dtb -r image.itb
fdtget verifier-control.dtb /signature/key-release required
```

Require command success and the expected `conf` policy on the **control DT key node**. `-k` selects key material, `-K`
updates the verifier DT, and `-r` marks the used keys required there. These options do not create a missing ITS signature
node. Do not place `required = "conf"` in the untrusted FIT as if it controls the verifier. Package the exact modified
control DT into the verifier and authenticate that verifier through the preceding boot stage.
See [FIT enforcement](uboot-security-and-provenance.md#fit-enforcement) and the
[signing implementation](https://github.com/u-boot/u-boot/blob/v2025.10/tools/image-host.c).

`mkimage -F` modifies/re-signs an existing FIT. Key rotation needs a coordinated verifier-key and signed-image rollout,
including rollback and any required-key policy; re-signing the payload alone cannot update a deployed trust anchor.

`dumpimage -l image.itb` lists metadata and signature material. It does not establish cryptographic validity or required
policy. Extraction writes a host file, for example `dumpimage -T flat_dt -p 0 -o kernel.out image.itb`; confirm the index
from the listing and compare the extracted bytes with the intended source. Signature acceptance/rejection must be tested
with an enforcing verifier, including unsigned, wrong-key and tampered inputs.

## Network loading

Network boot avoids repeated flash writes during authorized development, but executes code and can mount a writable NFS
root. Decide whether that is within scope. For DHCP address acquisition only, set `autoload no` first. Set `autostart no`
before explicit TFTP loads; confirm actual command/environment behavior on the release.

Guard DHCP, each TFTP load, validation and boot in the same nested sequence as the MMC example. Save the kernel size
before loading the DT and save the DT size immediately afterward. A successful network configuration is not evidence
that either payload loaded. Do not boot after any failed transfer. Define `bootargs` with the actual NFS server/export,
protocol options and access mode only when that root filesystem is intended; it remains a trust input requiring the
[final handoff checks](uboot-security-and-provenance.md#final-kernel-inputs).
