# Device Tree Tooling

Use the target kernel's build context and binding version. A valid DTB can still describe hardware that is absent,
miswired, or unsupported by the running driver.

## Build and Validate

For a self-contained DTS without C preprocessor directives:

```bash
dtc -I dts -O dtb -o board.dtb board.dts
dtc -I dtb -O dts -o inspected.dts board.dtb
```

Kernel DTS files commonly use C includes and macros. Build them through the matching kernel make target with the
correct `ARCH`, toolchain, configuration, and output directory; passing such a source directly to dtc is insufficient.
Do not overwrite an existing configured build with an unrelated defconfig.

```bash
# In the configured kernel build context; select ARCH/CROSS_COMPILE/O= as needed.
make dtbs_check
make DT_SCHEMA_FILES=vendor,device.yaml dtbs_check
```

These need the release-compatible dt-schema tools and their dependencies.
Use `dt_binding_check` when editing the schema itself. For a standalone blob and prepared matching schemas:

```bash
dt-validate -s /path/to/processed-schema.json board.dtb
```

Check actual errors and unmatched bindings; command completion alone does not mean every node was constrained.
Follow the kernel's [schema guide](https://docs.kernel.org/devicetree/bindings/writing-schema.html).

## Inspect and Patch

Use `fdtget -l` to list children, `fdtget -p` to list properties, and explicit types to inspect values:

```bash
fdtget -t s board.dtb / compatible
fdtget -t x board.dtb /soc/i2c@21a0000 clock-frequency
fdtdump board.dtb
```

Paths are board examples. Resolve them from the actual tree before use.
`fdtput` modifies a file; preserve the original and prefer a source change when source is available.

```bash
cp board.dtb candidate.dtb
fdtput -t s candidate.dtb /soc/i2c@21a0000 status okay
```

dtc v1.7.2's `fdtput` expands its buffer when required. Do not impose a universal `dtc -p` prerequisite.
In-memory bootloader edits can have different allocation constraints.
See [fdtput's implementation](https://github.com/dgibson/dtc/blob/v1.7.2/fdtput.c).

## Overlays

Identify where application occurs: offline, in a bootloader, or in the running kernel.
Label-based targets need symbols in the base. Path-based targets can work without them.

```bash
dtc -@ -I dts -O dtb -o base.dtb base.dts
dtc -@ -I dts -O dtb -o sensor.dtbo sensor-overlay.dts
fdtoverlay -i base.dtb -o merged.dtb sensor.dtbo
```

Check referenced labels/paths and required driver support, then validate the merged tree.
A missing label can be a wrong base or misspelled symbol, not merely an omitted `-@`.
Bootloader application produces a merged tree before Linux boots; it does not require Linux runtime overlay support.
Runtime application needs the target kernel's supported API and policy. Do not assume that a vendor configfs interface
exists in upstream Linux. The [kernel overlay notes](https://docs.kernel.org/devicetree/overlay-notes.html)
describe its in-kernel API, target resolution, and removal constraints.

## Compare Blobs Without Hiding Conversion Failures

`scripts/dtc/dtx_diff` is useful interactively in its matching kernel tree, including its preprocessing context.
Do not use empty output alone as a verification gate: its process substitutions can hide conversion failures.
For two compiled blobs, convert each explicitly before comparing. This standalone `sh` example takes two DTB paths;
use ordinary file paths, prefixed with `./` if a name begins with a hyphen.

```sh
#!/bin/sh
set -eu
[ "$#" -eq 2 ] || { printf 'usage: compare-dtbs.sh expected.dtb actual.dtb\n' >&2; exit 2; }
command -v dtc >/dev/null 2>&1 || { printf 'dtc unavailable\n' >&2; exit 2; }
comparison_dir=$(mktemp -d) || exit 2
trap 'rm -rf -- "$comparison_dir"' 0
trap 'exit 130' INT
trap 'exit 143' TERM
if ! dtc -s -I dtb -O dts -o "$comparison_dir/expected.dts" "$1"; then
    printf 'expected DTB conversion failed\n' >&2
    exit 2
fi
if ! dtc -s -I dtb -O dts -o "$comparison_dir/actual.dts" "$2"; then
    printf 'actual DTB conversion failed\n' >&2
    exit 2
fi
comparison_status=0
diff -u "$comparison_dir/expected.dts" "$comparison_dir/actual.dts" || comparison_status=$?
case "$comparison_status" in
    0) printf 'Canonical DT properties match; boot selection is not verified\n' ;;
    1) printf 'DT properties differ; inspect the differences\n' >&2 ;;
    *) printf 'DT comparison failed\n' >&2 ;;
esac
exit "$comparison_status"
```

This compares canonicalized properties, not byte identity or arbitrary semantic equivalence between differently
encoded trees. Hashes answer byte identity. Symbol/phandle differences may still need interpretation.

## Inspect the Running Tree

When the kernel exposes its live tree, inspect `/sys/firmware/devicetree/base` or its `/proc/device-tree` view:

```bash
dtc -I fs -O dtb -o live.dtb /sys/firmware/devicetree/base
fdtget -t s live.dtb / compatible
```

The live tree includes bootloader fixups and any applied runtime changes. Compare the intended properties and explain
expected transformations; a non-empty source/live diff does not prove a stale boot artifact.
An absent `status` property is normally available under Linux's DT rules; distinguish that from an absent node.
Verify the bootloader's selected blob independently through its configuration, artifact identity, and boot evidence.
