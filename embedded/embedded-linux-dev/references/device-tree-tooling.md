# Device Tree Tooling

Tools for turning device tree source into blobs and back, building and applying
overlays, reading and patching a compiled DTB, diffing two trees, validating
against dt-schema, and inspecting the tree the running kernel actually parsed.

For node structure, resource ownership, and the driver probe path, see
`device-tree-driver-bringup.md`.

## Contents

- [Compile and Decompile with `dtc`](#compile-and-decompile-with-dtc)
- [Overlays](#overlays)
- [Inspect and Patch a Blob: `fdtget` / `fdtput` / `fdtdump`](#inspect-and-patch-a-blob-fdtget--fdtput--fdtdump)
- [Diff Two Trees: `dtx_diff`](#diff-two-trees-dtx_diff)
- [Validate Against Bindings: `dt-validate` / dt-schema](#validate-against-bindings-dt-validate--dt-schema)
- [The Live Tree: `/proc/device-tree`](#the-live-tree-procdevice-tree)
- [Worked Example: confirm a board's DTB matches its source](#worked-example-confirm-a-boards-dtb-matches-its-source)

## Compile and Decompile with `dtc`

`dtc` is the device tree compiler. It converts between source (`.dts`/`.dtsi`) and
the flattened binary blob (`.dtb`), in both directions.

```bash
# Source -> blob
dtc -I dts -O dtb -o my-board.dtb my-board.dts

# Blob -> source (decompile a DTB pulled off a target or build tree)
dtc -I dtb -O dts -o my-board.dts my-board.dtb

# Decompile to stdout for a quick look, keeping input as-is
dtc -I dtb -O dts my-board.dtb | less
```

Useful flags:

- `-@` — emit a `__symbols__` node so the blob can be a target for overlays.
- `-@ -H epapr` / `-H`  — control the header/handle format when required by the platform.
- `-W no-unit_address_vs_reg` and friends — silence specific lint warnings; prefer
  fixing the warning over suppressing it.
- `-p <bytes>` — pad the blob with extra free space so it can be patched in place
  by `fdtput` or the bootloader.

Kernel builds usually invoke `dtc` for you; call it directly when you have a blob
without matching source, or when reproducing a bootloader's compile step by hand.

## Overlays

An overlay (`.dtbo`) modifies a base tree at load time — adding a node, changing a
`status`, or wiring an endpoint — without editing the base DTB.

```bash
# Base tree MUST be compiled with symbols so overlays can resolve labels
dtc -@ -I dts -O dtb -o base.dtb base.dts

# Compile the overlay source to a .dtbo
dtc -@ -I dts -O dtb -o sensor-overlay.dtbo sensor-overlay.dts

# Apply an overlay onto a base blob offline (fdtoverlay, from dtc/libfdt)
fdtoverlay -i base.dtb -o merged.dtb sensor-overlay.dtbo

# Decompile the merged result to verify the overlay landed
dtc -I dtb -O dts merged.dtb | less
```

An overlay whose labels do not resolve against the base tree is almost always the
base tree compiled without `-@`. Runtime overlay application (via configfs or a
bootloader) requires kernel support and a base compiled with symbols.

## Inspect and Patch a Blob: `fdtget` / `fdtput` / `fdtdump`

These read and modify a compiled DTB directly, without a decompile/recompile round
trip — handy when you only have the blob.

```bash
# Read one property (path, then property name)
fdtget my-board.dtb /soc/i2c@21a0000/sensor@3c compatible
fdtget -t x my-board.dtb /soc/i2c@21a0000 clock-frequency   # -t x = hex, -t i = int, -t s = string

# List the child nodes of a path, then the properties of a node
fdtget -l my-board.dtb /soc/i2c@21a0000
fdtget -p my-board.dtb /soc/i2c@21a0000/sensor@3c

# Patch a property IN PLACE (needs free space — compile the blob with dtc -p)
fdtput -t s my-board.dtb /soc/i2c@21a0000/sensor@3c status okay
fdtput -t i my-board.dtb /soc/i2c@21a0000 clock-frequency 400000

# Full human-readable dump of a blob (structure + values + string table)
fdtdump my-board.dtb | less
```

`fdtput` mutates the blob — treat it like any boot-artifact edit: back up the
original first and keep the reverse value to restore. Prefer editing source and
recompiling when you have the source.

## Diff Two Trees: `dtx_diff`

`dtx_diff` (shipped in the kernel `scripts/dtc/`) normalises and diffs any two DT
inputs — source or blob, in any combination — so a "did my change take effect"
question becomes a clean textual diff.

```bash
# Diff two blobs (e.g. old vs newly built board DTB)
scripts/dtc/dtx_diff old-board.dtb new-board.dtb

# Diff source against the compiled blob shipped in an image
scripts/dtc/dtx_diff my-board.dts /path/to/deployed/my-board.dtb

# Diff what the running kernel parsed against your source
scripts/dtc/dtx_diff /proc/device-tree my-board.dts
```

Because it canonicalises both sides first, the diff shows only real structural or
value differences, not formatting noise. This is the fastest way to prove a rebuilt
DTB actually differs from the one on the target.

## Validate Against Bindings: `dt-validate` / dt-schema

`dt-schema` provides `dt-validate`, which checks a tree against the YAML binding
schemas so property names, types, and required fields are caught before boot.

```bash
# One-time install of the schema tooling
pip install dtschema

# In a kernel tree: build DTBs in the schema-checking YAML form and validate them
make dtbs_check                       # validates all boards against bindings
make DT_SCHEMA_FILES=vendor,model.yaml dtbs_check   # scope to one binding

# Validate a standalone blob against the installed processed schema
dt-validate -s /path/to/processed-schema.json my-board.dtb
```

This is what catches a typo like an unknown property (for example a made-up
`enable-regulators` in place of the correct `<rail>-supply`) or a wrong value type,
at build time rather than as a silent probe failure. Always run it after editing a
binding-governed node.

## The Live Tree: `/proc/device-tree`

The kernel exposes the tree it actually parsed under `/proc/device-tree` (a view of
the same data as `/sys/firmware/devicetree/base`). Each property is a file; each
node is a directory.

```bash
# The compatible string the running kernel sees for a node
cat /proc/device-tree/soc/i2c@21a0000/sensor@3c/compatible | xxd

# A numeric property is big-endian bytes — decode with xxd or hexdump
cat /proc/device-tree/soc/i2c@21a0000/clock-frequency | xxd   # e.g. 00 06 1a 80 = 400000

# Is a node enabled?
cat /proc/device-tree/.../status 2>/dev/null   # absent often means "okay"

# Reconstruct the whole live tree as source for inspection
dtc -I fs -O dts /proc/device-tree | less
```

`dtc -I fs -O dts /proc/device-tree` is the ground truth: it is the tree after the
bootloader's fixups, not your source. When source and target disagree, this tells
you which DTB actually booted.

## Worked Example: confirm a board's DTB matches its source

On an i.MX6ULL board where a freshly built sensor node does not appear to take
effect:

```bash
# 1. Reconstruct the live tree the kernel booted with
dtc -I fs -O dts /proc/device-tree > /tmp/live.dts

# 2. Diff it against the source you think you deployed
scripts/dtc/dtx_diff /tmp/live.dts arch/arm/boot/dts/imx6ull-myboard.dts

# 3. If they differ, the target booted a stale DTB — check what the bootloader loaded
#    and re-copy the freshly built arch/arm/boot/dts/imx6ull-myboard.dtb.
#    (Bootloader DTB selection lives in uboot-dev.)
```

A non-empty diff here is the single most common "my device tree change did nothing"
root cause: the edited source compiled fine but a stale `.dtb` is on the boot
partition.
