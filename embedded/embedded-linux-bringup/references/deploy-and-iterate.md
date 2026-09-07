# Deploy and Iterate

Prove the identity and selection of the artifacts before attributing a target failure to the latest source change.
Use emulation only for behavior the selected machine can represent.

## Verify the Relevant Artifact

Keep these claims separate:

| Claim                        | Evidence and limitation                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------------------------------- |
| The file arrived intact      | Hash the exact host artifact and destination file; a matching file may still be unused                  |
| The artifact is compatible   | Inspect ELF ABI or module metadata against the target; this does not identify its code                  |
| The boot path selected it    | Inspect boot selection and logs, including fallback paths; a file on the boot partition is insufficient |
| The running instance uses it | Correlate build identity, loaded module state, live DT properties, and process executable               |
| The change works             | Exercise the relevant device or application behavior on that running instance                           |

For a userspace binary, use the same path in the transfer and verification steps:

```bash
# Host and target respectively; board is the configured SSH alias.
sha256sum ./myapp
ssh board sha256sum /usr/local/bin/myapp
```

Treat a failed hash command as unverified. When a process was already running, replacing its pathname does not replace
its executable image. Check its actual executable and use the application's authorized restart procedure.

For a module, inspect `modinfo -F vermagic ./mymod.ko`, its hash/build identity, the intended kernel build configuration,
and the target's load result. `uname -r` supplies only the release string.
Equal vermagic neither proves identical code nor covers symbol CRCs, signatures, dependencies, and load-time failures.
An installed reference module can itself be stale. Do not force-load a rejected module to bypass these checks.
See the target release's [module checks](https://github.com/torvalds/linux/blob/v6.12/kernel/module/version.c).

For a DTB, verify both the selected boot artifact and the intended live properties.
Bootloader fixups and overlays can legitimately change memory, bootargs, addresses, and random seeds.
Use [device-tree-tooling.md](device-tree-tooling.md) to distinguish a missing change from a legitimate transformation.
For bootargs, compare each required property with `/proc/cmdline`; do not turn the presence of `rootwait` into a
universal success condition. A system using an initramfs or another root path may not need it.

Report each applicable check as matched, different, failed, or unverified. Do not print an overall build match from
a partial compatibility check or from a skipped comparison.

## Decide Whether QEMU Can Exercise the Change

Record QEMU version, machine, CPU, attached devices, kernel configuration, and the intended test.
The [QEMU v10.1 virt model](https://github.com/qemu/qemu/blob/v10.1.0/docs/system/arm/virt.rst)
is a virtual platform, not an emulator for an arbitrary real board.
A custom DTB describes existing modeled hardware; it does not create a controller, sensor, clock, or interrupt route.

- Use DT schema checks for structural/binding correctness without claiming that hardware works.
- Use QEMU for compatible userspace, generic kernel paths, and devices the chosen machine actually models.
- Test board-specific drivers only against a corresponding model with the necessary implementation and wiring.
- Verify pinmux, power sequencing, electrical behavior, DMA coherency, timing, and silicon errata on suitable hardware.

Start with the machine-generated DTB. If a custom tree is needed, derive it for the same machine configuration and
verify its addresses, interrupts, memory, and attached devices. Do not substitute a physical board's DTB into `virt`.

```bash
# Host: inspect this exact machine configuration's generated tree.
qemu-system-aarch64 -M virt,dumpdtb=virt.dtb -cpu cortex-a53 -m 1024 -nographic
dtc -I dtb -O dts -o virt.dts virt.dtb
```

Machine defaults can change between releases. Record or select an available versioned machine when the test requires
stable virtual hardware. Regenerate its DTB when machine options or devices change.

## A Compatible ARM64 Iteration Loop

The examples require an ARM64 kernel with PL011 console support and a matching userspace.
The initramfs must contain an executable init plus its interpreter/libraries, and the kernel must support its compression.

```bash
qemu-system-aarch64 \
  -M virt -cpu cortex-a53 -m 1024 -nographic -nic none \
  -kernel Image -initrd rootfs.cpio.gz \
  -append 'console=ttyAMA0 rdinit=/sbin/init'
```

For a raw ext4 filesystem image, attach storage explicitly. This example uses virtio-mmio; build its transport,
block driver, and ext4 support into the kernel when no initramfs loads modules first.

```bash
qemu-system-aarch64 \
  -M virt -cpu cortex-a53 -m 1024 -nographic -nic none -snapshot \
  -kernel Image \
  -drive file=rootfs.ext4,format=raw,if=none,id=rootfs \
  -device virtio-blk-device,drive=rootfs \
  -append 'console=ttyAMA0 root=/dev/vda rw rootwait'
```

Here `/dev/vda` contains a filesystem directly. A partitioned disk requires the appropriate partition root instead.
`-snapshot` makes guest disk writes disposable; it is not a backup or protection for arbitrary host exports.
Use separate writable state and ports for concurrent runs.

For SSH iteration, replace `-nic none` with an explicit backend and device, for example:

```text
-netdev user,id=n0,hostfwd=tcp:127.0.0.1:2222-:22 -device virtio-net-device,netdev=n0
```

The guest needs its network driver, network configuration, and an SSH server. Connect through host port 2222.
This does not configure an NFS rootfs; NFS needs its own reachable server and early guest networking.

For early debugging, add `-gdb tcp:127.0.0.1:1234 -S` and connect cross-GDB to that port with matching `vmlinux`.
The stub has no authentication. Loopback constrains remote reachability but not hostile users on the same host.
Use an isolated development host, stop the stub after testing, and account for a halted guest's watchdog behavior.
See [QEMU's invocation options](https://github.com/qemu/qemu/blob/v10.1.0/qemu-options.hx).

Capture a bounded boot log and an observable guest result for each iteration. A QEMU process that starts successfully
does not establish that Linux booted, that the test ran, or that the real board is qualified.
