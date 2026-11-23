# Device Permissions, Names, and Sandboxing

How a program reaches its devices as an unprivileged user: a udev rule for the node, a group for the user, and a
systemd unit that allows only those devices. Read `udev(7)`, `systemd.exec(5)`, and `systemd.resource-control(5)`
for the systemd version on the target, because options are added between releases.

## Contents

- Groups the Defaults Provide
- Write the udev Rule
- Sysfs Attributes
- Configure the Service
- Capabilities

## Groups the Defaults Provide

systemd's default udev rules and `sysusers.d` entries give device groups to serial ports (`dialout`), input devices
(`input`), video and render nodes, audio, disks, the RTC (`clock`), and `/dev/mem` (`kmem`, mode 0640). They create
no group for GPIO chips, I2C adapters, spidev, UIO, IIO, or the watchdog, so these nodes stay root-only until the
product adds its own rule. An image built without systemd, such as one using BusyBox `mdev`, applies its own rules;
read them in the image.

## Write the udev Rule

Read the attributes a rule can match from the running target, never from memory:

```sh
udevadm info --attribute-walk --name=/dev/gpiochip0
```

Match on the `SUBSYSTEM` and `KERNEL` values it prints, then set the group and mode. For example, with values to check
against the `udevadm` output:

```text
SUBSYSTEM=="gpio", KERNEL=="gpiochip*", GROUP="gpio", MODE="0660"
```

Where the node's number can change, add `SYMLINK+="<name>"` to a rule that also matches an attribute of the parent
device, such as `KERNELS==` or `ATTRS{name}==` from a parent in the walk, so the link always names the same chip.

- Create the group the rule names, with a `sysusers.d` entry or the build system's user and group mechanism, such as
  `GROUPADD_PARAM` in Yocto or a users table in Buildroot.
- Install the rule under `/usr/lib/udev/rules.d/` or `/etc/udev/rules.d/` in the image, with a two-digit prefix that
  sorts it after the default rules.
- `ATTR{key}="value"` in a rule writes a sysfs attribute when the device appears. Use it for a one-time setting,
  such as an LED trigger. It does not change who may write the attribute later.
- Test the rule with `udevadm test` on the device's sysfs path, then confirm the result with `ls -l` on the node.

## Sysfs Attributes

LED, backlight, hwmon, and IIO attributes are files under `/sys`, not device nodes, so a rule's `GROUP=` and `MODE=`
do not apply to them. Writable attributes are root-only by default. Give a service write access in one of two ways,
and confirm the result with `ls -l` on the attribute on the target:

- a udev rule for the device that runs `chgrp` and `chmod` on the attribute through `RUN+=`, checked against
  `udev(7)` for the target's systemd version;
- a small privileged helper or service that owns the writes and takes requests from the application.

## Configure the Service

Where systemd is init, run the program as its own user in the device group, and let systemd limit what it can
reach. In this example, the `<...>` paths stand for the nodes or stable links found on the target:

```ini
[Service]
User=sensor-daemon
SupplementaryGroups=gpio i2c
DevicePolicy=closed
DeviceAllow=<gpio-chip-node> rw
DeviceAllow=<i2c-adapter-node> rw
NoNewPrivileges=yes
CapabilityBoundingSet=
```

- `SupplementaryGroups=` adds groups to those the user already has in the group database.
- `DeviceAllow=` takes a path under `/dev/` or a `char-<name>` class from `/proc/devices`, with `r`, `w`, and `m`.
  Read the class name from `/proc/devices` on the target before using one. Its documentation does not say whether
  a path may be a udev symlink, so when the node number can change, use the class form, or test a symlink path on
  the target before relying on it.
- `DevicePolicy=closed` allows only the listed devices and a few standard pseudo-devices. With the default `auto`,
  a unit without any `DeviceAllow=` reaches every device. The device filter and the file permissions are checked
  independently, so the node's group and mode must also allow the user.
- `PrivateDevices=yes` gives the service a private `/dev` without physical devices. It removes `/dev/mem`,
  `/dev/port`, and `CAP_SYS_RAWIO`, so it suits a service that needs no hardware at all. A hardware service uses
  `DevicePolicy=` and `DeviceAllow=` instead.

## Capabilities

The ordinary operations of the GPIO character device, i2c-dev, spidev, evdev, UIO, serial ports, and the watchdog
are checked against the node's file permissions. Once the node's group and mode allow the service's user, start
with `CapabilityBoundingSet=` and `AmbientCapabilities=` empty, and add a capability only for an `EPERM` the
program hits on the target, naming the call that needs it. `TIOCEXCL` is an example: it does not stop a process with
`CAP_SYS_ADMIN`. Raw I/O is the exception: opening `/dev/mem` and calling
`ioperm()` or `iopl()` need `CAP_SYS_RAWIO`, which grants access to all of physical memory. Treat a request for it as
a sign that the design needs a driver.
