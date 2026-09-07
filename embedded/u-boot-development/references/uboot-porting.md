# U-Boot Porting and Advanced Topics

Bringing up a new board: defconfig and Kconfig symbols, the legacy board header, the board directory, U-Boot's own
device tree, the driver model, SPL/TPL sizing, and A/B partition patterns. Confirm the U-Boot version first —
`CONFIG_SYS_*` → `CFG_SYS_*` and header → Kconfig migration drift by release.

## Contents

- [Porting a new board](#porting-a-new-board)
- [Driver model (DM)](#driver-model-dm)
- [SPL / TPL sizing](#spl--tpl-sizing)
- [A/B partition update patterns](#ab-partition-update-patterns)

## Porting a new board

### 1. Create the defconfig

```bash
# configs/<target>_defconfig — minimal arm64 example:

CONFIG_ARM=y
CONFIG_ARCH_MYMACHINE=y
CONFIG_TARGET_MYBOARD=y
CONFIG_SYS_CONFIG_NAME="myboard"     # selects include/configs/myboard.h

CONFIG_DEFAULT_DEVICE_TREE="myboard"

CONFIG_BOOTDELAY=3
CONFIG_USE_BOOTCOMMAND=y
CONFIG_BOOTCOMMAND="run distro_bootcmd"
CONFIG_DISTRO_DEFAULTS=y

CONFIG_MMC=y
CONFIG_DM_MMC=y
CONFIG_FS_FAT=y
CONFIG_EXT4_WRITE=y

CONFIG_ENV_IS_IN_MMC=y
CONFIG_ENV_SIZE=0x2000
CONFIG_ENV_OFFSET=0x3F0000
```

Build and test:

```bash
make myboard_defconfig
make menuconfig         # fine-tune
make -j$(nproc) CROSS_COMPILE=aarch64-linux-gnu-
```

### 2. Kconfig board symbols

```kconfig
# arch/arm/mach-mymachine/Kconfig  (or the SoC-level Kconfig)
config TARGET_MYBOARD
    bool "My Board"
    select ARCH_MYMACHINE
    help
      Support for My Board based on MySoC.
```

The board symbol sets the companion identifiers (directly or via `select`):

| Kconfig key              | Purpose                                      |
| ------------------------ | -------------------------------------------- |
| `CONFIG_SYS_BOARD`       | Board directory name under `board/<vendor>/` |
| `CONFIG_SYS_VENDOR`      | Vendor directory name                        |
| `CONFIG_SYS_SOC`         | SoC family name                              |
| `CONFIG_SYS_CPU`         | CPU type                                     |
| `CONFIG_SYS_CONFIG_NAME` | `include/configs/<name>.h` to include        |

### 3. Legacy board header

```c
/* include/configs/myboard.h */
#ifndef __MYBOARD_H
#define __MYBOARD_H

/* These migrate to Kconfig over time, but many boards still use the header. */
#define CONFIG_SYS_MALLOC_LEN       (8 << 20)   /* 8 MB heap */
#define CONFIG_SYS_MAXARGS          64
#define CONFIG_SYS_CBSIZE           2048         /* console buffer */

/* Memory layout */
#define CONFIG_SYS_TEXT_BASE        0x40200000   /* U-Boot load address */
#define CONFIG_SYS_SDRAM_BASE       0x40000000
#define CONFIG_SYS_SDRAM_SIZE       (1 << 30)    /* 1 GB */

#include <config_distro_bootcmd.h>

#endif /* __MYBOARD_H */
```

Trend: new `CONFIG_SYS_*` symbols are migrating to Kconfig. Add new settings to Kconfig rather than the header when the
version supports it. Many runtime `CONFIG_SYS_*` macros were also renamed to `CFG_SYS_*` (≈v2022.10) — check which
prefix your release expects.

### 4. Board directory

```
board/<vendor>/<board>/
├── Kconfig         # selects the SoC, declares board-specific configs
├── Makefile        # compiles board.o and other board-specific sources
├── board.c         # board_init(), dram_init(), misc_init_r(), etc.
└── myboard.env     # text-format default environment (optional)
```

Minimal `board.c`:

```c
#include <common.h>
#include <init.h>

int board_init(void) {
    /* gd->bd->bi_boot_params = PHYS_SDRAM + 0x100; */
    return 0;
}

int dram_init(void) {
    gd->ram_size = CONFIG_SYS_SDRAM_SIZE;
    return 0;
}
```

### 5. Device tree in U-Boot

U-Boot keeps its own DTS under `arch/arm/dts/`. Changes to the kernel DTS do **not** propagate to U-Boot — each tree is
maintained separately.

```bash
# U-Boot DTS location
arch/arm/dts/myboard.dts
arch/arm/dts/mysoc.dtsi

# Point to it in Kconfig / defconfig:
CONFIG_DEFAULT_DEVICE_TREE="myboard"
```

`CONFIG_OF_CONTROL` enables the live DT and DM at runtime. Most modern boards enable it.

## Driver model (DM)

### Key concepts

- **uclass**: abstraction for a class of peripherals (MMC, I2C, SPI, GPIO, …).
- **driver**: a uclass implementation for specific hardware.
- **udevice**: a probed, bound instance of a driver in the DM tree.

DM lifecycle per device:

| Phase        | When               | Purpose                                               |
| ------------ | ------------------ | ----------------------------------------------------- |
| `bind`       | Before `probe`     | Match the DT node to a driver; allocate the `udevice` |
| `of_to_plat` | Before `probe`     | Parse DT properties into platform data                |
| `probe`      | At first use       | Enable clocks, reset, map registers                   |
| `remove`     | On shutdown/unbind | Power down hardware                                   |
| `unbind`     | Cleanup            | Free resources                                        |

`uclass_get_device()` triggers `bind` → `of_to_plat` → `probe` in sequence. The DM tree mirrors the device-tree
hierarchy.

### Shell inspection

```bash
dm tree       # full DM device tree with probe state
dm uclass     # uclasses and their bound devices
dm drivers    # registered drivers
dm compat     # compatible strings per driver
```

### DT access in drivers

```c
/* From struct udevice *dev: */
u32 val = dev_read_u32_default(dev, "my-property", 0);
const char *str = dev_read_string(dev, "label");
struct udevice *gpio_dev;
int ret = uclass_get_device_by_phandle(UCLASS_GPIO, dev, "enable-gpio", &gpio_dev);

/* For subnodes and phandles, use ofnode: */
ofnode node = dev_read_subnode(dev, "port");
if (ofnode_valid(node)) {
    u32 reg = ofnode_read_u32_default(node, "reg", 0);
}
```

Avoid new `fdtdec`-based code — the DM `dev_read_*` / `ofnode` API works across both flat and live device trees and is
the current recommended approach.

**Live tree** (`CONFIG_OF_LIVE`): after relocation, U-Boot converts the flat DT to a hierarchical live tree; SPL still
uses the flat tree. The `ofnode` abstraction handles both transparently.

## SPL / TPL sizing

SPL runs from on-chip SRAM before DRAM init, so its size limits are strict and an overflow is a silent power-on hang.

| Platform         | Typical SPL limit                       |
| ---------------- | --------------------------------------- |
| TI AM335x        | 128 KB                                  |
| Microchip SAMA5D | 64 KB (`CONFIG_SPL_SIZE_LIMIT=0x10000`) |
| i.MX6/7/8        | 68 KB (OCRAM size)                      |

### Trimming SPL size

```bash
# Check SPL size after build
ls -la spl/u-boot-spl.bin
size spl/u-boot-spl

# Disable unused features in the SPL build:
CONFIG_SPL_NET=n
CONFIG_SPL_USB_HOST=n
CONFIG_SPL_NAND_SUPPORT=n    # only if not booting from NAND
CONFIG_SPL_DM_SEQ_ALIAS=n
CONFIG_SPL_OF_LIBFDT=y       # keep only if SPL uses DT nodes

# Fail the build if SPL overflows
CONFIG_SPL_SIZE_LIMIT=0x20000   # 128 KB hard limit
```

### Falcon mode (SPL boots Linux directly)

Skip full U-Boot to minimize boot time:

```
ROM → SPL → Linux (kernel + DTB pre-loaded by SPL)
```

```
CONFIG_SPL_OS_BOOT=y
CONFIG_CMD_SPL=y
```

SPL loads the kernel, DTB, and optionally initramfs, then jumps to the kernel entry point — no full U-Boot command loop.
A serial or GPIO escape path is usually provided for development access.

## A/B partition update patterns

### Partition layout (block device)

```
Disk: myboard-sdcard.img
├── Partition 1: boot (FAT)        — SPL + U-Boot + extlinux.conf
├── Partition 2: rootfs A (ext4)   — active slot
├── Partition 3: rootfs B (ext4)   — inactive slot (update target)
└── Partition 4: data (ext4)       — persistent user data
```

### Slot selection via bootable flag

```bash
# U-Boot: find the bootable partition
part list mmc 0 -bootable bootpart

# Use it in bootcmd
setenv bootcmd '
  part list mmc 0 -bootable bootpart;
  if test -z "$bootpart"; then setenv bootpart 2; fi;
  sysboot mmc 0:${bootpart} any ${pxefile_addr_r} /boot/extlinux/extlinux.conf
'
```

The active rootfs partition is marked bootable. The updater:

1. Writes the new image to the **inactive** partition.
2. Clears the bootable flag on the active partition.
3. Sets the bootable flag on the updated partition.
4. Triggers a reboot.

### Slot selection via bootcount (rollback)

```bash
# In the U-Boot default env:
setenv bootlimit  3
setenv altbootcmd 'echo Boot failed N times, reverting; run revert_slot'
```

`CONFIG_BOOTCOUNT_LIMIT` makes U-Boot increment `bootcount` each boot. When `bootcount >= bootlimit`, U-Boot runs
`altbootcmd` instead of `bootcmd`. The Linux updater (RAUC, SWUpdate, Mender) clears `bootcount=0` via `fw_setenv` after
a confirmed healthy boot.

For the userspace update framework that owns this flow — writing the inactive slot, verifying a signed bundle, and
flipping this env (RAUC's `BOOT_ORDER`/`BOOT_x_LEFT`, or a swupdate `bootenv`/`fw_setenv`) only after a health check —
see **embedded-linux-bringup** `references/ota-updates.md`.

```bash
# On Linux: confirm boot success (from the updater / health-check service)
fw_setenv bootcount 0
fw_setenv upgrade_available 0
```

### Partition-table management

```bash
# U-Boot: rewrite GPT
gpt write mmc 0 $parts
gpt verify mmc 0

# Linux: set the GPT partition bootable attribute
sgdisk --attributes=2:set:2 /dev/mmcblk0   # set attr bit 2 on partition 2
# OR for MBR:
parted /dev/mmcblk0 set 2 boot on
```

### Tools for Linux-side env access

| Tool          | Package        | Notes                                          |
| ------------- | -------------- | ---------------------------------------------- |
| `fw_printenv` | `u-boot-tools` | Read the U-Boot env from Linux                 |
| `fw_setenv`   | `u-boot-tools` | Write the U-Boot env from Linux                |
| `libubootenv` | `libubootenv`  | Library + tools; alternative to `u-boot-tools` |

Configure access via `/etc/fw_env.config`:

```
# device         offset    size
/dev/mmcblk0     0x3F0000  0x2000
```
