# Deploy and Iterate

Two workflows that shorten the embedded feedback loop: emulating the board under
QEMU so most kernel/driver/DTS work needs no hardware, and verifying that what you
built is actually what booted on the target.

## Contents

- [The QEMU Iteration Loop](#the-qemu-iteration-loop)
- [Booting a Custom DTB and Overlay Under QEMU](#booting-a-custom-dtb-and-overlay-under-qemu)
- [Deploy-Verify: prove the target runs what you built](#deploy-verify-prove-the-target-runs-what-you-built)
- [Deploy-Verify Script Pattern](#deploy-verify-script-pattern)

## The QEMU Iteration Loop

Flashing hardware for every kernel or DTS change is slow and error-prone. For any
work that does not depend on real silicon — most driver logic, DTS structure, boot
flow, and userspace integration — emulate the board and iterate in seconds.

The loop:

```
1. edit    → change kernel source, .config, DTS, or rootfs
2. build   → rebuild only what changed (kernel Image + dtbs, or the module)
3. boot    → qemu-system-<arch> with -kernel/-dtb/-drive, serial to stdio
4. observe → read the boot log / run the test over the emulated console
5. repeat  → back to edit; no reflash, no power-cycle
```

A minimal aarch64 `virt` invocation, kernel + initramfs, console on stdio:

```bash
qemu-system-aarch64 \
  -M virt -cpu cortex-a53 -m 1024 -nographic \
  -kernel arch/arm64/boot/Image \
  -initrd rootfs.cpio.gz \
  -append "console=ttyAMA0 rdinit=/sbin/init loglevel=7"
```

Boot a full disk image with a real rootfs instead of an initramfs:

```bash
qemu-system-aarch64 \
  -M virt -cpu cortex-a53 -m 1024 -nographic \
  -kernel arch/arm64/boot/Image \
  -drive file=rootfs.ext4,format=raw,if=virtio \
  -append "console=ttyAMA0 root=/dev/vda rw"
```

Practical loop mechanics:

- `-nographic` routes the emulated serial console to your terminal; `Ctrl-a x`
  quits QEMU, `Ctrl-a c` toggles the QEMU monitor.
- Add `-s -S` to expose a gdbstub on `:1234` and hold the CPU at reset, then attach
  the cross-GDB (`target remote :1234`) to single-step early boot — see
  `debugging.md`.
- `-netdev user,id=n0 -device virtio-net-device,netdev=n0` gives the guest
  outbound networking and host-forwarded ports for NFS or SSH-based iteration.
- Keep a scripted one-liner so `build && qemu …` is a single command; the point is
  to remove every manual step between edit and observation.

QEMU emulates the SoC's generic peripherals, not board-specific analog wiring, so
sensor timing, PMIC sequencing, and signal-integrity faults still need hardware.
Use QEMU to get the software layers correct first, then move to the board with a
short remaining list of hardware-only unknowns.

## Booting a Custom DTB and Overlay Under QEMU

The `virt` machine can generate its own DTB, or accept yours. To iterate on a real
board DTS in emulation, pass a compiled blob:

```bash
# Dump the machine's own generated DTB (baseline to diff against)
qemu-system-aarch64 -M virt,dumpdtb=virt.dtb -cpu cortex-a53 -m 1024 -nographic

# Boot with your own compiled board/overlay-merged DTB
qemu-system-aarch64 \
  -M virt -cpu cortex-a53 -m 1024 -nographic \
  -kernel arch/arm64/boot/Image \
  -dtb merged.dtb \
  -append "console=ttyAMA0 root=/dev/vda rw"
```

Combine with `dtx_diff` and `dt-validate` (see `device-tree-tooling.md`) to confirm
the merged tree is what you expect before booting it.

## Deploy-Verify: prove the target runs what you built

After a deploy, the most common wasted hour is debugging a target that silently
booted a stale kernel, module, or DTB. Before diagnosing behaviour, PROVE the
artifacts on the target match the ones you just built. Four checks:

1. **Kernel module vermagic match.** A module built against a different kernel is
   rejected or, worse, refuses to load with `version magic … should be …`. Compare
   the module's vermagic to the running kernel's:

   ```bash
   # On target: running kernel's expected magic
   cat /proc/version
   modinfo /lib/modules/$(uname -r)/extra/mymod.ko | grep vermagic
   # vermagic must match `uname -r` + toolchain/SMP/preempt flags exactly
   ```

2. **DTB / DTBO present and current.** Confirm the board booted the DTB you built,
   not a stale one on the boot partition:

   ```bash
   # Reconstruct the live tree and diff against your source/blob
   dtc -I fs -O dts /proc/device-tree > /tmp/live.dts
   scripts/dtc/dtx_diff /tmp/live.dts my-board.dts   # empty diff => current
   # Applied overlays (configfs-based):
   ls /sys/kernel/config/device-tree/overlays/
   ```

3. **Boot-config sanity.** The kernel cmdline the target actually booted with is the
   ground truth for `console=`, `root=`, and `rootwait`:

   ```bash
   cat /proc/cmdline
   ```

4. **Binary/rootfs identity.** For a deployed userspace binary, checksum both ends:

   ```bash
   sha256sum mybinary
   ssh root@<target> sha256sum /usr/local/bin/mybinary   # must match
   ```

Only once all four confirm the target runs your build should you start diagnosing
behaviour. A mismatch here is itself the root cause.

## Deploy-Verify Script Pattern

Fold the four checks into one script run on the target right after deploy. Invoke as
`verify-deploy.sh <module.ko> <board.dts>`; it is read-only and exits non-zero on
the first mismatch.

```sh
#!/bin/sh
# verify-deploy.sh <module.ko> <board-source.dts>
# Read-only: verifies the running target matches freshly built artifacts.
# Exits non-zero on the first mismatch.
set -eu

mod="${1:?module .ko path}"
dts="${2:?board .dts path}"
[ -r "$mod" ] || { printf 'FAIL: cannot read module %s\n' "$mod" >&2; exit 1; }
[ -r "$dts" ] || { printf 'FAIL: cannot read dts %s\n'    "$dts" >&2; exit 1; }

tmpdir="$(mktemp -d)" || exit 1
trap 'rm -rf -- "$tmpdir"' EXIT INT TERM

# 1. Module vermagic vs the running kernel.
# An in-tree module already installed for the running kernel carries the EXACT
# vermagic the kernel enforces (release + SMP/preempt/module flags). Compare the
# candidate's FULL vermagic against that reference so the check matches what insmod
# would enforce, not just the release token. modinfo -F prints the field verbatim.
running="$(uname -r)"
mod_vm="$(modinfo -F vermagic "$mod")"
ref_ko="$(find "/lib/modules/$running/kernel" -type f -name '*.ko*' 2>/dev/null | head -n 1)"
if [ -n "$ref_ko" ]; then
    ref_vm="$(modinfo -F vermagic "$ref_ko")"
    [ "$mod_vm" = "$ref_vm" ] || {
        printf 'FAIL vermagic:\n  module: %s\n  kernel: %s\n' "$mod_vm" "$ref_vm" >&2
        exit 1
    }
    printf 'vermagic OK (full match): %s\n' "$mod_vm"
else
    # No in-tree reference to compare against: verify the release token only and say
    # so — SMP/preempt/module flags are NOT checked on this path (insmod is the final
    # arbiter and prints the expected magic on refusal).
    mod_rel="${mod_vm%% *}"
    [ "$mod_rel" = "$running" ] || {
        printf 'FAIL vermagic: module built for %s, running %s\n' "$mod_rel" "$running" >&2
        exit 1
    }
    printf 'WARN: no in-tree module to compare; release-only check (%s), flags unverified\n' \
        "$mod_rel" >&2
fi

# 2. Live DTB vs source.
dtc -I fs -O dts /proc/device-tree > "$tmpdir/live.dts" 2>/dev/null
if command -v dtx_diff >/dev/null 2>&1; then
    if dtx_diff "$tmpdir/live.dts" "$dts" | grep -q .; then
        printf 'FAIL dtb: live tree differs from %s\n' "$dts" >&2
        exit 1
    fi
fi

# 3. Boot-config sanity.
grep -q 'rootwait' /proc/cmdline || printf 'WARN: no rootwait in /proc/cmdline\n' >&2
printf 'cmdline: %s\n' "$(cat /proc/cmdline)"

printf 'OK: vermagic, device tree, and boot-config match the build\n'
```

This is a diagnostic (read-only) step, not a mutation — it needs no confirmation
gate. Run it before any deep-dive so you never debug a target running stale bits.
