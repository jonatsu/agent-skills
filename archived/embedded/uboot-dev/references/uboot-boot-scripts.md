# U-Boot Boot Scripts and Images

Boot-method precedence, `extlinux.conf`, `boot.scr`, distro/standard boot, the
`booti`/`bootz`/`bootm`/`bootefi` selection, FIT authoring/signing/inspection,
and network boot. `dumpimage -l` and `printenv` are read-only; treat everything
that writes media as mutating.

## Contents

- [Boot-method hierarchy](#boot-method-hierarchy)
- [extlinux.conf](#extlinuxconf)
- [boot.scr (U-Boot script)](#bootscr-u-boot-script)
- [distro_bootcmd](#distro_bootcmd)
- [Boot commands](#boot-commands)
- [FIT images (.its)](#fit-images-its)
- [Inspecting and extracting a FIT (dumpimage)](#inspecting-and-extracting-a-fit-dumpimage)
- [Network boot (TFTP + NFS)](#network-boot-tftp--nfs)

## Boot-method hierarchy

`distro_bootcmd` tries boot methods in the order set by `boot_targets`. The
typical priority (highest to lowest) on most platforms:

1. `extlinux.conf` (SYSLINUX-compatible; easiest to edit from Linux)
2. `boot.scr` (a U-Boot script binary)
3. PXE (network)
4. DHCP boot

If both `extlinux.conf` and `boot.scr` are present, `extlinux.conf` wins on most
platforms. Standard boot (`bootstd`/`bootflow`, `CONFIG_BOOTSTD`) supersedes
`distro_bootcmd` from ≈v2021.10 — confirm the framework before debugging boot
selection.

## extlinux.conf

A SYSLINUX-compatible config parsed via `sysboot`. Easiest to update from a
running Linux system — no special tools required.

### Search path

U-Boot looks for the file in order:

1. `/extlinux/extlinux.conf`
2. `/boot/extlinux/extlinux.conf`

For network/PXE boot: `pxelinux.cfg/default`.

### Format

```
# /boot/extlinux/extlinux.conf
default linux
timeout 10

label linux
    kernel /boot/Image
    fdt /boot/myboard.dtb
    append console=ttyS0,115200 root=/dev/mmcblk0p2 rw rootwait

label linux-fallback
    kernel /boot/Image.bak
    fdt /boot/myboard.dtb
    append console=ttyS0,115200 root=/dev/mmcblk0p2 rw rootwait panic=5
```

Supported fields:

| Field | Notes |
|-------|-------|
| `kernel` | Kernel image path (Image, zImage, uImage, or FIT) |
| `fdt` | Explicit DTB path |
| `fdtdir` | Directory; U-Boot appends `${fdtfile}` to form the path |
| `fdtoverlays` / `devicetree-overlay` | Space-separated overlay paths |
| `initrd` | Initramfs/ramdisk path |
| `append` | Extra kernel command-line arguments |
| `default` | Label booted if no key is pressed during `timeout` |
| `timeout` | Tenths of a second (0 = wait forever, absent = no wait) |

### Env-variable expansion in `append`

U-Boot expands env variables inside `append`:

```
append console=ttyS0 root=/dev/mmcblk0p${bootpart} rootwait
```

This drives A/B slot selection without duplicating configs.

### Manual trigger

```bash
sysboot mmc 0:1 any $pxefile_addr_r /boot/extlinux/extlinux.conf
```

## boot.scr (U-Boot script)

A binary-wrapped U-Boot script — more capable than `extlinux.conf` (full
scripting), but MUST be regenerated with `mkimage` whenever the text changes.

### Creating boot.scr

```bash
cat > boot.cmd << 'EOF'
load mmc 0:1 $kernel_addr_r /boot/Image
load mmc 0:1 $fdt_addr_r /boot/myboard.dtb
setenv bootargs "console=ttyS0,115200 root=/dev/mmcblk0p2 rw rootwait"
booti $kernel_addr_r - $fdt_addr_r
EOF

mkimage -T script -d boot.cmd boot.scr
mkimage -T script -n "My Boot Script" -d boot.cmd boot.scr   # named variant
```

### Loading and executing

```bash
fatload mmc 0:1 $scriptaddr boot.scr
source $scriptaddr

source $scriptaddr#conf-1        # a FIT-wrapped script at a named config
```

`distro_bootcmd` searches for `boot.scr` automatically when
`CONFIG_DISTRO_DEFAULTS` is enabled.

## distro_bootcmd

`distro_bootcmd` is a pre-built `bootcmd` provided by `config_distro_bootcmd.h`.
It iterates `boot_targets`, `boot_prefixes`, and `boot_scripts` to find a
bootable config automatically.

Controlling variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `boot_targets` | board-specific | Ordered list, e.g. `mmc0 mmc1 usb0 pxe dhcp` |
| `boot_prefixes` | `/ /boot/` | Directories searched for boot files |
| `boot_scripts` | `boot.scr.uimg boot.scr` | Script filenames tried |
| `fdtfile` | arch/board derived | DTB filename appended to `fdtdir` in extlinux |

Enable with `CONFIG_DISTRO_DEFAULTS=y`.

## Boot commands

Pick the command by image format — the wrong one produces "Bad Magic" or
"Wrong Image Format".

### booti — ARM64 Linux Image

```bash
booti $kernel_addr_r - $fdt_addr_r                       # kernel + no ramdisk + DTB
booti $kernel_addr_r $ramdisk_addr_r:$filesize $fdt_addr_r   # with ramdisk
```

Use for `arm64` boards with an uncompressed `Image`.

### bootz — ARM32 zImage

```bash
bootz $kernel_addr_r - $fdt_addr_r
bootz $kernel_addr_r $ramdisk_addr_r:$filesize $fdt_addr_r
```

Use for 32-bit ARM boards with a self-decompressing `zImage`.

### bootm — FIT / legacy uImage

```bash
bootm $loadaddr              # FIT default config, or a legacy uImage
bootm $loadaddr#conf-1       # FIT named config
```

`bootm` handles both the legacy uImage format and FIT. FIT is the recommended
modern format — it bundles kernel + DTB + ramdisk into one hashed, optionally
signed file.

### bootefi — UEFI

```bash
bootefi $kernel_addr_r $fdt_addr_r
bootefi bootmgr                 # run the UEFI boot manager
```

EFI-stub kernels (`CONFIG_EFI_STUB`) boot this way — useful for UEFI-based OS
installers on arm64.

## FIT images (.its)

FIT (Flattened Image Tree) bundles kernel, DTB, and ramdisk with hashes and
optional RSA signatures into a single `.itb` binary.

### Minimal .its for arm64

```dts
/dts-v1/;
/ {
    description = "Kernel + DTB";
    #address-cells = <1>;

    images {
        kernel {
            data = /incbin/("Image");
            type = "kernel";
            arch = "arm64";
            os = "linux";
            compression = "none";
            load = <0x80080000>;
            entry = <0x80080000>;
            hash { algo = "sha256"; };
        };

        fdt-1 {
            data = /incbin/("myboard.dtb");
            type = "flat_dt";
            arch = "arm64";
            compression = "none";
            hash { algo = "sha256"; };
        };
    };

    configurations {
        default = "conf-1";
        conf-1 {
            description = "Default config";
            kernel = "kernel";
            fdt = "fdt-1";
        };
    };
};
```

### Building the FIT

```bash
mkimage -f image.its image.itb
```

### Signing a FIT

```bash
# Generate an RSA key pair
mkdir -p keys
openssl genpkey -algorithm RSA -out keys/dev.key -pkeyopt rsa_keygen_bits:2048
openssl req -new -x509 -key keys/dev.key -out keys/dev.crt -days 3650

# Build + sign; inject the public key into the U-Boot control FDT
mkimage -f image.its -k keys -K u-boot.dtb -r image.itb
# -k keys/       key directory
# -K u-boot.dtb  inject the public key into the U-Boot control FDT
# -r             require all configs to be signed

# Re-sign an existing FIT (rotate the key without rebuilding source)
mkimage -F -k keys -K u-boot.dtb image.itb
```

Enable verification in U-Boot:

```
CONFIG_FIT_SIGNATURE=y
CONFIG_RSA=y
```

See `uboot-security-and-provenance.md` for making the signature *required*
(rejecting unsigned images) and extending trust down to the SPL.

## Inspecting and extracting a FIT (dumpimage)

`dumpimage` reads and unpacks FIT and legacy images on the host. Listing is
read-only — use it to confirm what a FIT actually contains before rebuilding or
flashing it.

```bash
# List every sub-image, its hash, and any signature status (read-only)
dumpimage -l image.itb

# List a legacy uImage header
dumpimage -l uImage

# Extract sub-image at position N from a FIT into a file
dumpimage -T flat_dt -p 0 -o kernel.out image.itb    # first image
dumpimage -T flat_dt -p 1 -o fdt.out image.itb       # second image

# Round-trip check: extracted kernel should match the source
dumpimage -T flat_dt -p 0 -o kernel.out image.itb && sha256sum Image kernel.out
```

`-l` shows whether a signature node is present and which algorithm it uses, so
it answers "is this FIT signed, and with what?" without booting the board.

## Network boot (TFTP + NFS)

```bash
# DHCP — sets $ipaddr, $serverip, $gatewayip, $netmask
dhcp

# TFTP load
tftp $kernel_addr_r Image
tftp $fdt_addr_r myboard.dtb

# NFS rootfs bootargs
setenv bootargs "console=ttyS0,115200 root=/dev/nfs \
    nfsroot=${serverip}:/srv/nfs/rootfs,v3,tcp rw ip=dhcp"

booti $kernel_addr_r - $fdt_addr_r
```

Network boot is the preferred reversible path for iterating on a kernel or DTB
without reflashing boot media.
