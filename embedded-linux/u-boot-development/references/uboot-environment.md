# U-Boot Environment

Identify the configured and selected backend before diagnosing persistence. U-Boot changes its working environment in
RAM; a saved backend is separate state.

## Contents

- [Defaults and persistence](#defaults-and-persistence)
- [Backup and restore](#backup-and-restore)
- [Scripting](#scripting)
- [Bootcount and health confirmation](#bootcount-and-health-confirmation)

## Defaults and persistence

Text defaults normally come from `board/<vendor>/<board>/<CONFIG_ENV_SOURCE_FILE>.env`, falling back to the board name
when that setting is empty. Legacy C defaults also exist and can override text values. Read the generated default
artifact when both participate. A `.env` file supplies initial values; it does not make their RAM copies immutable.

[Environment documentation](https://docs.u-boot.org/en/v2025.10/usage/environment.html) describes default sources and
variables. Confirm the resolved `CONFIG_ENV_IS_IN_*` settings, runtime backend selection where supported, storage
device, hardware partition, offsets, sizes, and erase geometry. Use the actual Linux implementation and version of
`fw_printenv` and `fw_setenv`; identical executable names do not establish identical formats or configuration.

| Backend           | Check before writes                                                                                  |
| ----------------- | ---------------------------------------------------------------------------------------------------- |
| MMC               | Device, eMMC hardware partition, `CONFIG_ENV_OFFSET`, size, redundancy, any board-specific selection |
| NAND              | Offset and range, erase blocks, bad-block handling and space for every copy                          |
| SPI flash         | Bus and device, offset, sector geometry, size and redundant region                                   |
| UBI or filesystem | Volume or device, partition, and file identity, backend-specific save and recovery behavior          |
| `ENV_IS_NOWHERE`  | No save callback; save fails or the command is absent, depending on build                            |

`setenv name value` changes RAM; `setenv name` deletes from RAM. `env default -a` replaces RAM values with compiled
defaults. `saveenv` and `env save` attempt persistence; inspect their status. `printenv` immediately afterward still reads
RAM. Verify the saved backend independently and perform an authorized reset and reload before declaring persistence proven.
The [nowhere driver](https://github.com/u-boot/u-boot/blob/v2025.10/env/nowhere.c) and
[save dispatcher](https://github.com/u-boot/u-boot/blob/v2025.10/env/env.c) distinguish unavailable saving from success.

Redundancy needs correct backend support, distinct regions, valid sizes and geometry, and tested selection after interrupted
writes. One Kconfig symbol does not prove power-loss safety. Derive erase ranges and `/etc/fw_env.config` offsets from
this board's resolved configuration. `env erase` affects backend state; it is neither a backup nor a universal factory reset.
Resetting update variables is also different from resetting all environment state.

## Backup and restore

Choose what must be recovered before selecting a format:

| Capture                | What it preserves                                     | Recovery limits                                                         |
| ---------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------- |
| Console transcript     | Visible name and value evidence                       | Not a lossless import file; may be truncated or expose secrets          |
| Text export (`-t`)     | Escaped name and value text                           | Match importer escaping and newlines and complete exported length       |
| Binary export (`-b`)   | NUL-separated RAM values                              | Preserve full length; lacks raw backend headers and layout              |
| Checksum export (`-c`) | Environment export with checksum header               | Not automatically an exact redundant-media snapshot                     |
| Raw backend backup     | Captured bytes, including relevant headers and copies | Restore only through a qualified procedure aware of layout and geometry |

For a RAM snapshot, reserve a verified safe buffer large enough for the complete environment, separate from every load,
DT, stack, heap, and reserved region. Export success sets `filesize`; capture that length before any other operation
changes it. An export followed by `md.b ... 200` displays only 0x200 bytes and is not a durable backup.

The following is a **U-Boot command template**, not host Bash. Resolve the addresses, capacity and length before use;
record them outside the environment too, because replacement import can delete helper variables. Binary export
always fills the full environment data area and sets `filesize` to `CONFIG_ENV_SIZE`, so reserve at least
`CONFIG_ENV_SIZE` bytes.

```text
if env export -b ${backup_addr}; then
    setenv backup_len ${filesize}
else
    echo "Environment export failed; stop before mutation"
fi
```

When recovery must survive reset, transfer exactly the captured bytes to an authorized durable destination and verify
length and digest there. Use the project's available transfer command with explicit status checks. Reload the verified
backup into safe RAM before restore. With the recorded literal address and length, replacement import is:

```text
env import -d -b <verified-address> <recorded-length>
```

Without `-d`, import merges and retains newly introduced variables. With `-d` and no variable list, it replaces the
working environment, subject to configured access controls. Check status and compare all required variables, including
absences, spaces and multiline values. Persist only under the existing write authorization, then verify a reset and reload.
See the [import/export implementation](https://github.com/u-boot/u-boot/blob/v2025.10/cmd/nvedit.c).

For Linux-side recovery, `fw_printenv > env.bak` followed by `fw_setenv -s env.bak` is not a lossless round trip.
U-Boot's [host script parser](https://github.com/u-boot/u-boot/blob/v2025.10/tools/env/fw_env.c) accepts `name=value`
lines, but it reads one variable per line. Each continuation line of a multiline value becomes a separate variable
named after its first word, and leading blanks in every value are dropped. A script also sets only the variables it
lists, so it cannot delete variables added since the capture. Use a tool-supported lossless method or a qualified raw
backup of the exact backend and both redundant copies. Stop if the available interface cannot restore the required
values.

Before a production write, demonstrate the procedure with a disposable backend containing an environment longer than 512
bytes, spaces, multiline values, and changed, deleted, and added variables. Demonstrate persistence after restoring it.
A fresh-default reset is appropriate only when defaults are the intended result, with device-specific data accounted
for.

## Scripting

In U-Boot, semicolons continue after failure. Guard every dependent load, `source`, and boot step using supported Hush
conditionals or `&&`. Use the guarded examples in [boot scripts](uboot-boot-scripts.md#guarded-loads).

`run name` executes a variable as commands. It can write media or jump into arbitrary code; RAM storage of the variable
does not constrain its effects. Use `test` for string comparisons and `itest` for appropriate numeric comparisons,
checking the command's radix rules. Preserve each artifact's `filesize` separately before loading the next one.

## Bootcount and health confirmation

With a nonzero limit, the generic test is **`bootcount > bootlimit`**, not `>=`. At limit 3, counts 2 and 3 do not take
the over-limit branch; count 4 does. A zero limit disables this threshold. An absent `altbootcmd` can leave the system at
a prompt; it is not an implicit rollback. See [bootcount.h](https://github.com/u-boot/u-boot/blob/v2025.10/include/bootcount.h).

The counter's increment, persistence and health writer depend on its backend and stage. Establish initialization,
watchdog and reset behavior, storage durability and update gating from the selected driver. The
[environment backend](https://github.com/u-boot/u-boot/blob/v2025.10/drivers/bootcount/bootcount_env.c) and
[filesystem backend](https://github.com/u-boot/u-boot/blob/v2025.10/drivers/bootcount/bootcount_fs.c) are different:
`upgrade_available` and `fw_setenv bootcount 0` are not a universal protocol for every backend.

The updater owns trial activation and health confirmation. RAUC's `BOOT_ORDER` and `BOOT_x_LEFT` integration is distinct
from the generic counter. Test limit minus one, the limit, and limit plus one, a disabled limit, missing fallback,
watchdog and power resets, and userspace confirmation against the actual storage backend. See [A/B
integration](uboot-porting.md#ab-integration).
