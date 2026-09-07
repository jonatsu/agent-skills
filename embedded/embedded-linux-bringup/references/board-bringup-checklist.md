# Board Bring-Up Checklist

## Contents

- [Boot Chain Overview](#boot-chain-overview)
- [SoC-Specific Boot File Naming](#soc-specific-boot-file-naming)
- [Bootloader Stage](#bootloader-stage)
- [Kernel Bring-Up](#kernel-bring-up)
- [Rootfs and Userspace](#rootfs-and-userspace)
- [First-Boot Checklist](#first-boot-checklist)
- [NFS Rootfs for Development](#nfs-rootfs-for-development)

## Boot Chain Overview

```
Power-on
  └─ Boot ROM (SoC-internal, reads boot source selection pins)
       └─ SPL / TPL (Secondary Program Loader — minimal DDR init)
            └─ U-Boot proper (full bootloader, loads kernel + DTB)
                 └─ Linux kernel (decompresses, parses DTB)
                      └─ Device driver probe sequence
                           └─ rootfs mount → init → services → application
```

Each layer can fail silently if the next stage produces no console output. Always confirm which stage you are at before
assuming the next one is reached.

## SoC-Specific Boot File Naming

Different SoCs require their boot files in specific locations and formats. These are worked examples, not defaults —
always confirm against your board's reference manual.

| SoC / Board                      | First-stage file              | Location                          |
| -------------------------------- | ----------------------------- | --------------------------------- |
| BeagleBone / AM33xx              | `MLO` (SPL)                   | FAT partition                     |
| BeagleBone / AM33xx              | `u-boot.img`                  | FAT partition                     |
| i.MX6 / i.MX7                    | `u-boot.imx`                  | raw at **1 KB offset** on SD card |
| STM32MP1 (TF-A/FIP, recommended) | `tf-a.stm32` (TF-A BL2)       | GPT partition `fsbl1` and `fsbl2` |
| STM32MP1 (TF-A/FIP, recommended) | `fip.bin` (U-Boot inside FIP) | GPT partition `fip`               |
| STM32MP1 (SPL chain, basic)      | `u-boot-spl.stm32` (SPL)      | GPT partition `fsbl1` and `fsbl2` |
| STM32MP1 (SPL chain, basic)      | `u-boot.img`                  | GPT partition `ssbl`              |
| AM62x / BeaglePlay               | `tiboot3.bin`                 | FAT partition                     |
| AM62x / BeaglePlay               | `tispl.bin`                   | FAT partition                     |
| AM62x / BeaglePlay               | `u-boot.img`                  | FAT partition                     |
| Allwinner                        | `u-boot-sunxi-with-spl.bin`   | raw at **8 KB offset** on SD card |

The Boot ROM searches for the first-stage image in a fixed location — the wrong filename or offset causes a silent hang
at power-on.

## Bootloader Stage

Confirm the board reaches and completes the bootloader before blaming the kernel: the serial console MUST show
bootloader banner output, a correct DDR size, and a kernel + DTB load from the expected medium.

For U-Boot console commands, environment, `extlinux.conf`/distro-boot, storage inspection, FIT images, and bootloader
porting, use **u-boot-development**. The one signal this file relies on: if the console shows the bootloader but goes
silent right after "Starting kernel …", the failure is a kernel/DTB or console-mismatch problem, covered below — not a
bootloader problem.

## Kernel Bring-Up

### Bootargs must match kernel and rootfs

The kernel command line is set by the bootloader but consumed by the kernel; a mismatch here shows up as a kernel-side
failure. The `console=` device and baud MUST match the physical UART, or kernel output disappears after "Starting kernel
…" even though the bootloader printed fine. `root=` MUST point at the real rootfs partition, and `rootwait` covers a
storage driver that probes after the mount attempt.

```
console=ttyS0,115200 root=/dev/mmcblk0p2 rw rootwait
```

Setting these in the bootloader environment is **u-boot-development** territory.

### Early boot log signals

```
[    0.000000] Booting Linux on physical CPU 0x0              ← kernel started
[    0.000000] Machine model: My Board Rev 1.0                ← DTB matched
[    0.000000] Memory: 1024M available                        ← DDR detected
...
[    2.345678] VFS: Mounted root (ext4 filesystem) on device  ← rootfs mounted
[    2.500000] Run /sbin/init as init process                 ← init started
```

If the log stops before "VFS: Mounted root", the failure is in the kernel or driver probe phase — not a userspace issue.

### Kernel panic: rootfs not found

```
Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0)
```

Cause checklist:

- `root=` bootarg points at the wrong device (check `ls /dev/mmcblk*` on a live system).
- Rootfs filesystem driver not compiled in (ext4, f2fs, squashfs — `zcat /proc/config.gz | grep EXT4`).
- MMC/storage driver did not probe before the mount attempt — add `rootwait`.
- Wrong partition number (`mmcblk0p2` vs `mmcblk1p2` when two eMMC/SD devices are present).

### Kernel Command-Line Parameters for Bring-Up

| Parameter                             | Effect                                                                                                   |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `earlycon`                            | Early console output before the full UART driver is up — uses a port from the DTS or a hardcoded default |
| `earlycon=uart8250,mmio32,0xFF030000` | Explicitly specify the UART base address for earlycon                                                    |
| `earlyprintk`                         | Legacy early printk (older kernels; prefer `earlycon`)                                                   |
| `console=ttyS0,115200`                | Full UART console once the driver is up                                                                  |
| `rootwait`                            | Wait indefinitely for the root device to appear                                                          |
| `init=/bin/sh`                        | Drop to a shell instead of running init (rootfs debug)                                                   |
| `panic=5`                             | Reboot 5 seconds after a kernel panic                                                                    |
| `loglevel=7`                          | Maximum kernel log verbosity (0–7)                                                                       |

`earlycon` is the most useful parameter when boot stalls between "Starting kernel …" and the first kernel timestamp — it
prints before the console driver initialises.

### Analyzing `dmesg` efficiently

```bash
# Filter for a specific driver/device
dmesg | grep -i "sensor\|camera\|i2c" | head -40

# Show only errors and warnings
dmesg --level=err,warn

# Human-readable timestamps (kernel >= 3.5)
dmesg -T | tail -50

# Continuous monitor during bring-up (serial console or SSH)
dmesg -w
```

## Rootfs and Userspace

### `/dev` node lifecycle

```
Driver probe succeeds
  └─ Driver calls device_create() or equivalent
       └─ uevent sent to udev/mdev
            └─ udev rule matches and creates /dev/<node>
```

If the `/dev` node is missing after a successful probe:

```bash
# Is udev/mdev running?
ps aux | grep -E "udev|mdev"

# Was the uevent fired?
udevadm monitor --kernel   # watch in one terminal while probing in another

# What rule would apply?
udevadm test /sys/bus/i2c/devices/1-003c 2>&1 | grep -i "SYMLINK\|NAME\|RUN"

# Force udev to re-scan
udevadm trigger
udevadm settle
```

### Service startup failures

```bash
# systemd: which units failed?
systemctl --failed
systemctl status <service-name> --no-pager -l

# Startup order issue (service starting before a dependency)
systemctl list-dependencies <service-name>

# Boot-time analysis
systemd-analyze
systemd-analyze blame          # sorted unit startup times
systemd-analyze critical-chain # critical path to default.target

# BusyBox / SysV init
cat /var/log/messages | grep -i "error\|fail" | tail -30
dmesg | grep -i "init\|service" | tail -20
```

### Permission issues on `/dev` nodes

```bash
# Check ownership and mode
ls -la /dev/<node>

# Add a udev rule to fix permissions
echo 'SUBSYSTEM=="video4linux", MODE="0664", GROUP="video"' \
    > /etc/udev/rules.d/99-camera.rules
udevadm trigger
```

## First-Boot Checklist

Work through these in order. Do not skip a layer.

- [ ] Serial console connects and shows bootloader output
- [ ] Bootloader reports the correct DDR size
- [ ] Correct DTB filename loaded (bootloader `fdtfile`/equivalent — see u-boot-development)
- [ ] Kernel command line has the correct `console=`, `root=`, and `rootwait`
- [ ] Kernel log shows "Machine model:" matching the board
- [ ] Kernel log shows "VFS: Mounted root"
- [ ] Shell prompt appears (or `init` output visible)
- [ ] `dmesg` shows the target peripheral driver probe success
- [ ] `/dev/<node>` exists for each expected peripheral
- [ ] Basic userspace test succeeds (e.g. `i2cdetect -y 1`, `v4l2-ctl --list-devices`)
- [ ] Application starts and logs expected output

## NFS Rootfs for Development

NFS rootfs eliminates the flash-then-boot cycle during bring-up. For the QEMU edit-build-test loop and deploy
verification, see `deploy-and-iterate.md`.

```bash
# On host: export rootfs via NFS
echo "/srv/nfs/rootfs 192.168.1.0/24(rw,no_root_squash,sync)" >> /etc/exports
exportfs -a
systemctl restart nfs-server

# Populate the rootfs (from a build system image)
sudo tar -xf tmp/deploy/images/<machine>/core-image-minimal-<machine>.tar.bz2 \
    -C /srv/nfs/rootfs

# Bootloader bootargs for NFS (set in u-boot-development)
#   console=ttyS0,115200 root=/dev/nfs \
#   nfsroot=192.168.1.1:/srv/nfs/rootfs,v3,tcp rw ip=dhcp
```

Advantage: edit files on the host, immediately visible on the target without reflashing. Cost: requires a stable
Ethernet link from first boot.
