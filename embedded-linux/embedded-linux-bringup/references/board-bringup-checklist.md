# Board Bring-up and Boot Failures

Use serial output, boot selection, and artifact identities to locate the handoff that failed.
The chain may include ROM, SPL/TPL, TF-A, firmware, U-Boot, Linux, initramfs, and the final userspace.
Do not require a particular banner or stage on platforms that omit it or suppress its console.

## Before Changing the Boot Path

Record board revision, boot medium, current image set, console wiring/settings, bootloader configuration, and recovery
access. Get boot-file names, partition layout, and raw offsets from the matching board/SoC boot documentation.
Offsets from another SoC or boot mode are not safe templates.
Route U-Boot commands, image formats, environment edits, and flashing to **u-boot-development**.

If output ends at `Starting kernel`, investigate both sides of the handoff: loaded image/address, CPU entry state,
DTB, firmware requirements, and early console. That message does not prove the kernel received a valid handoff.
Kernel output can also be absent while the system runs successfully on a different console.

## Kernel and Root Mount

Inspect the actual command line and the selected kernel's configuration.
`console=` needs the correct device and console driver. `earlycon` needs a supported UART description, such as the
appropriate DT stdout path or a verified explicit parameter. Never copy an MMIO UART address from another board.
`loglevel=8` permits all ordinary kernel message levels; `ignore_loglevel` is another diagnostic choice with output cost.
See the matching [kernel parameter reference](https://docs.kernel.org/admin-guide/kernel-parameters.html).

For `VFS: Unable to mount root fs`, determine whether the root device was found before guessing the filesystem fault:

| Evidence                                 | Next check                                                                              |
| ---------------------------------------- | --------------------------------------------------------------------------------------- |
| Root device absent                       | Bootargs, storage driver, firmware, pinctrl, supplies, enumeration and discovery timing |
| Device exists but partition differs      | Actual partition table and selected medium; use stable identifiers when supported       |
| Device exists but mount fails            | Filesystem type, driver availability, corruption and image/partition layout             |
| Verity mapping absent or rejects reads   | [Rootfs integrity](rootfs-integrity.md): backing devices, parameters and trust          |
| Initramfs starts but final root does not | Its scripts, required modules, root selection and mount/switch_root errors              |

`rootwait` waits for device discovery; it does not repair a missing driver, wrong device, or corrupt filesystem.
Without an initramfs that loads modules, storage and filesystem support needed for root must be built into the kernel.
Use a bounded serial window around discovery and mount, not only the final panic line.

An example disk-root command line is `console=ttyS0,115200 root=/dev/mmcblk0p2 rw rootwait`.
Every device name and option must match the target. `init=/bin/sh` can help inspect the final root; an initramfs
uses its own init selection, commonly `rdinit=`. Account for security policy and the lack of normal service startup.

## From Init to Device Nodes

Confirm the root mounted, init executed, and required mounts/services started.
A device can register correctly in sysfs while its `/dev` node is absent from the application's namespace.

1. Inspect the subsystem class, for example `/sys/class/video4linux/`, and its device/driver links.
2. Read the class device's `dev` attribute when it represents a character/block device.
3. Check whether devtmpfs is configured and mounted at the `/dev` visible to the process.
4. Check the platform's node manager: kernel devtmpfs, BusyBox mdev, udev, or static node provisioning.
5. Check numbering, permissions, symlinks, container/device policy, and mount namespaces before changing the driver.

Linux's [devtmpfs implementation](https://github.com/torvalds/linux/blob/v6.12/drivers/base/devtmpfs.c)
can create device nodes directly; a running udev daemon is not a universal prerequisite.
Not every peripheral exposes a `/dev` node. For cameras, locate devices with `v4l2-ctl --list-devices` and the media
graph rather than assuming the intended camera is `/dev/video0` or `/dev/video1`.

For udev systems, inspect applicable rules and bounded events using `udevadm info` and `udevadm monitor`.
Reloading rules and triggering events changes system behavior; scope those operations to the intended device.
Do not issue a global trigger or change every video device's permissions to test a single missing node.

## Service and Application Boundary

On systemd targets, inspect the failed unit and a bounded journal window:

```bash
systemctl --failed
systemctl status app.service --no-pager -l
journalctl -u app.service -b -n 100 --no-pager
```

Use the target's equivalent on BusyBox/SysV systems. Check actual dependencies, executable/interpreter identity,
working directory, credentials, device permissions, and mounts.
`systemd-analyze blame` lists elapsed startup times, not a proof of the critical dependency causing delay.
Route unit authoring to the systemd-units skill; use [cross-compilation.md](cross-compilation.md) for ELF/ABI failures.

## Faster Iteration with an NFS Root

Use a dedicated development export and identify exactly which target clients can access it.
Root access to a writable export can modify host-side files; `no_root_squash` is a deliberate trust decision,
not a default for an entire site subnet. Keep the export separate from valuable source and host system directories.

The target needs early network/NFS support and a reachable server before mounting root.
An example boot argument fragment is `root=/dev/nfs nfsroot=192.0.2.1:/srv/board-root,v3,tcp ip=dhcp`;
replace it with the actual server, export, protocol, and network setup.
Follow the [kernel NFS-root documentation](https://docs.kernel.org/admin-guide/nfs/nfsroot.html).
Do not edit host exports, restart services, or populate a shared directory without the established scope.

## Bring-up Completion

Record the booted image identities, final command line, successful root/init transition, required driver bindings,
interface visibility, and a functional peripheral/application check.
Name any remaining hardware, performance, recovery, or release qualification rather than treating a shell prompt as
completion. [Deploy and iterate](deploy-and-iterate.md) separates the artifact checks from those functional results.
