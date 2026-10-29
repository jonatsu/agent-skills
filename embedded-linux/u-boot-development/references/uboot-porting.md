# U-Boot Porting and Integration

Start from a supported board with the same SoC and boot arrangement in the project's exact U-Boot release. A generic
C file with a guessed RAM size or a made-up architecture symbol is not a compilable board port.

## Board configuration and device tree

1. Build the nearby supported defconfig unchanged in a separate output directory. Record toolchain, effective `.config`,
   build commands, artifacts and logs. This establishes a usable baseline before board-specific changes.
2. Trace its Kconfig selection to `SYS_BOARD`, `SYS_VENDOR`, `SYS_SOC` and `SYS_CONFIG_NAME` where used. Add only the
   board-specific identifiers and Makefile wiring required by that release. Use Kconfig for supported settings;
   inspect remaining header macros individually rather than mass-renaming `CONFIG_` to `CFG_`.
3. Carry over the release's actual include and declaration requirements and SoC initialization interfaces. In v2025.10,
   `common.h` is not a valid generic board include; access to `gd` needs the applicable global-data declaration.
   Copying an obsolete skeleton and guessing DRAM capacity can compile incorrectly or fail before useful diagnostics.
4. Identify the **control DT** consumed by each bootloader stage separately from the **OS DT** handed to Linux.
   `CONFIG_OF_UPSTREAM` selects Linux-derived files in `dts/upstream`; other builds use local `arch/*/dts` files or a
   board-supplied DT. Inspect `CONFIG_DEFAULT_DEVICE_TREE`, `DEVICE_TREE` overrides, vendor paths, generated dependencies,
   and `*-u-boot.dtsi` additions. Follow the final packaged DT back to that provider.
5. Build after each bounded board change. Inspect the generated DT, map, SPL and packaged image before a target trial.
   A source DT edit or a standalone DTB is insufficient if the image builder embeds a different DT.

Example host invocation for an existing supported target, with project-resolved absolute paths and a bounded job count:

```bash
make -C "$source_root" O="$build_dir" "$supported_defconfig"
make -C "$source_root" O="$build_dir" CROSS_COMPILE="$toolchain_prefix" -j4
```

Run the second command only after configuration succeeds. These variables are caller inputs, not a board skeleton.
For integration into Buildroot or Yocto, use the sibling build-system skill instead of bypassing its artifact pipeline.
The [devicetree guide](https://github.com/u-boot/u-boot/blob/v2025.10/doc/develop/devicetree/control.rst) explains the
providers; editing another kernel checkout does not automatically update U-Boot's build inputs.

## Trimming a defconfig

A meta-option `select`s other options, sometimes through a chain, and `savedefconfig` omits every option a select or
an `imply` sets. Unsetting a meta-option therefore drops options that no defconfig diff shows. In v2026.10,
`BOOTSTD_DEFAULTS` selects `BOOTMETH_DISTRO`, which selects `BOOTMETH_SCRIPT`, which selects `HUSH_PARSER`; see
[boot Kconfig](https://github.com/u-boot/u-boot/blob/v2026.10/boot/Kconfig). Without hush, a boot script's `while`
or `if` fails with `Unknown command 'while'`, and the simple parser rejects a command longer than
`CONFIG_SYS_CBSIZE` with `## Command too long!`.

1. Run `olddefconfig` before and after the change, and diff the two resolved `.config` files.
2. Set every option the boot script and boot flow need explicitly in the defconfig, at least `CONFIG_HUSH_PARSER=y`
   for a script that uses hush syntax.
3. Add a build step that fails when a required option is missing from the resolved `.config`, such as a Yocto
   `do_configure` append that checks `${B}/.config`.

## Driver model

A `udevice` is a bound device instance and may still be unprobed. A `uclass` groups a device class; a driver implements
operations for matched hardware. Binding creates the instance. Probing initializes it for use and can enable clocks,
reset devices or access registers. A lookup that probes is not a passive diagnostic.

`uclass_get_device()` finds a bound device and requests probing; it does not bind it afresh on every lookup. Distinguish
find-only APIs from get-and-probe APIs when debugging. Examine return status, dependency providers, `of_to_plat`, and the
active flag before assuming initialization completed. See the
[uclass implementation](https://github.com/u-boot/u-boot/blob/v2025.10/drivers/core/uclass.c).

Use `dm tree` and `dm uclass` to inspect bound and probed state; use `dm drivers` and `dm compat` when available to examine
matching. DM topology is not an exact rendering of all DT nodes: driver matching, buses, providers, subnodes and stage
filtering affect which instances exist.

`CONFIG_OF_CONTROL` enables DT-based configuration. `CONFIG_OF_LIVE` separately selects a live representation;
`ofnode` and `dev_read_*` let callers work with supported flat and live forms. Prefer these APIs in new drivers, checking
return values and property binding requirements. GPIO consumer properties need the appropriate GPIO API and binding,
not an arbitrary phandle interpreted as a device. Qualify SPL's representation and available APIs from its resolved
configuration; do not infer them from U-Boot proper. See [DT Kconfig](https://github.com/u-boot/u-boot/blob/v2025.10/dts/Kconfig).

For a probe failure, compare the same bound device before and after the first get operation, then inspect its provider
failures. Where both forms are supported, run the relevant test with flat and live DT configurations.

## SPL and TPL memory

Locate the failing stage from its code and log. SPL may initialize DRAM, then load, authenticate, relocate or hand off a
later payload; a hang in SPL is not necessarily pre-DRAM. TPL, VPL, and SPL arrangements and ROM load rules vary by board.

Establish these independent constraints from the exact silicon manual, board config and build:

- ROM-accepted load region, alignment, image header and packaged size;
- linked text and data size and load address;
- BSS placement, stack, global data, heap and reserved buffers;
- lifetime and overlap before and after DRAM initialization or relocation;
- padding, authentication data, appended DT and any other image-builder content.

Inspect `spl/u-boot-spl`, its map and `spl/u-boot-spl.bin`, plus the final container actually loaded by ROM. Use the
matching toolchain's `size`/`readelf` for sections and memory regions. `CONFIG_SPL_MAX_SIZE` and image size limits do not
necessarily count the same bytes; inspect [SPL Kconfig](https://github.com/u-boot/u-boot/blob/v2025.10/common/spl/Kconfig)
and the associated linker and build checks. Test just below, at, and just above the relevant bound in a disposable build.

Take the SRAM budget from the board's own defconfig and ROM documentation. v2025.10's `imx8mp_evk_defconfig` uses
`SPL_MAX_SIZE=0x26000`, while `sama5d3_xplained_mmc_defconfig` uses `0x18000`; neither is a universal allowance for that
family. A linker or image-size failure is useful evidence, not an inevitable silent boot hang.

Trim only code not required by the actual boot, recovery and authentication paths. Measure each change. Falcon mode
(`CONFIG_SPL_OS_BOOT` where supported) skips U-Boot proper, so qualify its kernel and DT loading, escape and recovery
path and signature enforcement independently. Removing a stage also removes any policy enforced only by that stage.

## A/B integration

Use the updater's documented slot state and interruption-recovery protocol. A bootable partition attribute by itself
does not encode installation completeness, remaining attempts or health. `part list ... -bootable` can return zero,
one or multiple numbers; reject ambiguous selection instead of treating its result as a scalar or defaulting to slot A.
See the [partition command](https://github.com/u-boot/u-boot/blob/v2025.10/cmd/part.c).

Write down the actual layout before scripting: the bootloader regions, each slot's kernel, DT, rootfs, and
configuration, shared files and persistent data. If both slots contain `/boot/extlinux/extlinux.conf`, load from the
selected slot. If a shared FAT partition contains that file, explain how its authenticated configuration selects the
slot's matching payloads. Keep one filesystem layout throughout an example.

Keep three transitions separate: verify installation into the inactive slot; atomically or recoverably select it for a
trial boot; confirm health after boot. Clearing one partition flag and setting another in separate commands has a
power-loss gap. Use an updater-supported mechanism whose on-media commit and recovery behavior is documented; do not
invent an equivalent transaction from two `fw_setenv` or partition-table writes.

Test interruption at every activation write, zero or multiple selected slots, failed trial boots, exhausted attempts and
health confirmation. Expected recovery must choose a verified usable slot or an explicit recovery state. Partition-table
verification checks layout, not this protocol. Physical power-cut qualification remains specific to the board and backend.

Use **embedded-linux-bringup** for RAUC and SWUpdate integration. For generic U-Boot counter semantics and
backend-specific health writers, see [bootcount](uboot-environment.md#bootcount-and-health-confirmation).
