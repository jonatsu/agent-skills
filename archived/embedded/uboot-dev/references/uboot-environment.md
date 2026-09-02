# U-Boot Environment

How the environment loads and persists, the backends, the essential variables,
scripting, and A/B / factory-reset patterns. Pair every persisting or erasing
command with its restore — see the Safety contract in `SKILL.md`.

## Contents

- [How the environment works](#how-the-environment-works)
- [Default environment sources](#default-environment-sources)
- [Persistent backends](#persistent-backends)
- [Essential environment variables](#essential-environment-variables)
- [Commands](#commands)
- [Scripting in environment variables](#scripting-in-environment-variables)
- [A/B slot via environment](#ab-slot-via-environment)
- [Factory reset pattern](#factory-reset-pattern)

## How the environment works

U-Boot keeps a working copy of the environment in RAM. At startup:

1. It tries to load the saved env from the configured persistent backend.
2. If loading fails (corrupt, first boot, `ENV_IS_NOWHERE`), it falls back to
   the compiled default environment.
3. `setenv` changes the RAM copy only. `saveenv` writes the RAM copy back to
   storage.

```
Compiled default env  ──→  RAM working copy  ──→  saveenv  ──→  persistent backend
                        ↑
                     saved env loaded at boot (if valid)
```

MUST re-read after any `saveenv` — a "successful" save on a misconfigured
backend can persist nothing (see `ENV_IS_NOWHERE` below).

## Default environment sources

U-Boot resolves the default env in this order:

1. **Text env file** (preferred): `board/<vendor>/<board>/<CONFIG_ENV_SOURCE_FILE>.env`.
   If `CONFIG_ENV_SOURCE_FILE` is unset, it uses
   `board/<vendor>/<board>/<CONFIG_SYS_BOARD>.env`.
2. **Legacy C macro**: `include/env_default.h` plus `CFG_EXTRA_ENV_SETTINGS`
   from the board header.

Where both exist, the C-macro values override the text-env values. Prefer the
text `.env` format for new boards — it reads and diffs cleanly.

## Persistent backends

The backend is fixed at compile time via `CONFIG_ENV_IS_IN_*`:

| Kconfig option | Storage | Notes |
|----------------|---------|-------|
| `ENV_IS_IN_MMC` | eMMC/SD (raw sectors) | Most common; `CONFIG_ENV_MMC_DEV/PART/OFFSET` |
| `ENV_IS_IN_NAND` | NAND flash | MUST align to the erase block |
| `ENV_IS_IN_SPI_FLASH` | SPI NOR | `CONFIG_ENV_OFFSET`, `CONFIG_ENV_SIZE` |
| `ENV_IS_IN_UBI` | UBI volume | For systems with a full UBI stack |
| `ENV_IS_NOWHERE` | No storage | `saveenv` is a no-op; always uses default env |

**`ENV_IS_NOWHERE`:** `saveenv` returns success but saves nothing. This is the
correct choice for a production image that MUST stay locked to compiled
defaults, but it also means `setenv` + `saveenv` from the console has no effect
across reboots. Confirm the backend (`CONFIG_ENV_IS_IN_*`) before trusting a
save.

**NAND erase-block alignment:** `CONFIG_ENV_OFFSET` MUST align to the NAND
erase-block size. Misalignment corrupts the env on `saveenv` silently.

**Redundant env:** set `CONFIG_ENV_OFFSET_REDUND` to keep a second copy. U-Boot
selects the newer valid copy at boot, which survives a power loss during
`saveenv`.

## Essential environment variables

| Variable | Purpose |
|----------|---------|
| `bootdelay` | Seconds before `bootcmd` runs (0 = no delay, -1 = no autoboot, -2 = no abort) |
| `bootcmd` | Command(s) run after the autoboot timeout |
| `bootargs` | Kernel command line, passed via the DTB `/chosen` node or a register |
| `fdtfile` | DTB filename used by distro/standard boot scripts |
| `loadaddr` | Default RAM address for file loads |
| `kernel_addr_r` | Relocatable RAM address for the kernel |
| `fdt_addr_r` | Relocatable RAM address for the DTB |
| `ramdisk_addr_r` | Relocatable RAM address for the initramfs |
| `pxefile_addr_r` | RAM address for the PXE / extlinux config |
| `scriptaddr` | RAM address for boot scripts |
| `serverip` | TFTP server IP (auto-set by `dhcp`) |
| `ipaddr` | Target IP (auto-set by `dhcp`) |
| `ethaddr` | MAC address |

The `*_addr_r` variables follow the relocatable-address convention — boards set
them in the default env to place images in non-overlapping RAM regions.

## Commands

```bash
# Read
printenv                # all variables
env print               # same
printenv bootcmd        # one variable

# Set (RAM only, not persisted)
setenv myvar "hello world"
env set myvar "hello world"

# Delete
setenv myvar            # no value = delete
env delete myvar

# Snapshot before any write (capture restore state FIRST)
env export -t $loadaddr; md.b $loadaddr 200

# Persist to storage (mutating — gate this)
saveenv
env save

# Reset to compiled defaults (mutating — gate this)
env default -a
env default myvar       # reset one variable

# Run a variable as a command sequence
run bootcmd
run altbootcmd
```

To restore from a snapshot, re-import it: `env import -t <addr>`; from Linux,
`fw_setenv -s env.bak`.

## Scripting in environment variables

Env scripting uses `;` for sequencing and `if`/`test`/`itest` for conditionals:

```bash
# Sequential commands in one variable
setenv myboot 'mmc dev 0; fatload mmc 0:1 $kernel_addr_r Image; booti $kernel_addr_r - $fdt_addr_r'
run myboot

# String equality
setenv slot a
if test "$slot" = "a"; then echo "slot A"; else echo "slot B"; fi

# Integer comparison
setenv bootcount 3
setenv bootlimit 3
if itest $bootcount -ge $bootlimit; then run altbootcmd; fi

# Arithmetic
setexpr result $x + 1
setexpr hex_val fmt %08x $loadaddr

# String presence
if test -n "$fdtfile"; then echo "fdtfile is set"; fi
```

## A/B slot via environment

```bash
# In the default env or bootcmd:
setenv bootcmd '
  part list mmc 0 -bootable bootpart;
  if test -z "$bootpart"; then setenv bootpart 2; fi;
  setenv bootargs "console=ttyS0,115200 root=/dev/mmcblk0p${bootpart} rootwait";
  ext4load mmc 0:${bootpart} $kernel_addr_r /boot/Image;
  ext4load mmc 0:${bootpart} $fdt_addr_r /boot/myboard.dtb;
  booti $kernel_addr_r - $fdt_addr_r
'
```

Boot-failure fallback with `bootcount_limit`:

```bash
setenv bootlimit 3           # max failed boots before fallback
setenv altbootcmd 'echo fallback; run bootcmd_b'
```

With `CONFIG_BOOTCOUNT_LIMIT`, U-Boot increments `bootcount` on every boot and
runs `altbootcmd` once `bootcount >= bootlimit`. The Linux updater resets
`bootcount=0` and clears `upgrade_available` via `fw_setenv` (from `u-boot-tools`
or `libubootenv`) after a confirmed healthy boot.

## Factory reset pattern

```bash
# From U-Boot: wipe saved env so the next boot uses compiled defaults
env erase               # erases the env partition/area (mutating — gate + back up first)
# Next reboot loads the compiled defaults automatically

# From Linux (libubootenv / u-boot-tools)
fw_setenv bootcount 0
fw_setenv upgrade_available 0
```

For `ENV_IS_IN_MMC` at a known offset:

```bash
mmc erase <start-block> <count>   # erase the raw sectors holding the env
```

Worked example — Linux-side env access via `/etc/fw_env.config`:

```
# device         offset    size
/dev/mmcblk0     0x3F0000  0x2000
```
