---
name: linux-userspace-device-access
description: Write or review Linux userspace code that drives hardware on an embedded device, such as GPIO, I2C, SPI, UIO, serial and RS-485, input, LEDs, sensors, and the watchdog. Covers choosing a kernel driver or userspace access, the current interfaces and libraries, udev and systemd device permissions, and stable device names. Use when code opens /dev/gpiochip, /dev/i2c-N, spidev, uio, or tty nodes, or uses sysfs GPIO or /dev/mem. Bring-up goes to embedded-linux-bringup, drivers to linux-kernel-development.
license: MIT
compatibility: A Linux target or its BSP sources. libgpiod, i2c-tools, and systemd are optional and checked when used.
metadata:
  author: Joonas Onatsu
---

# Linux Userspace Device Access

Application code on an embedded Linux device that talks to hardware through the kernel's userspace interfaces. The
kernel replaces these interfaces over time, and products pin old kernels for years, so every rule below starts from
the kernel and libraries on the target. Write the C or C++ itself to `c-cpp-style`; this skill decides which
interface the code uses and how it holds the device.

## Decide Whether Userspace Is the Right Place

Search the kernel tree for a driver before writing userspace access: `git grep -i <part-number>` in the target's
kernel source, then the `Kconfig` option that enables it. Bootlin's training shows the usual case: a GPIO expander on
I2C already has a kernel driver, and enabling it lets other drivers use its lines for resets and interrupts.

Choose a kernel driver when any of these holds:

- a kernel driver for the part already exists, in mainline or the vendor tree;
- the line or chip serves another device, such as an LED, a button, a reset, an interrupt, a chip select, or a
  regulator (`leds-gpio`, `gpio-keys`, and device-tree hogs cover the common GPIO jobs);
- the device needs interrupts with bounded latency, DMA, sharing between several programs, or power management;
- the device fits a kernel class, such as hwmon, IIO, RTC, input, network, or serial, which gives every application
  the same interface;
- the product is built in volume. The kernel's GPIO documentation says to use proper kernel drivers in any uniform
  product, and keeps the GPIO userspace interface for one-off systems, prototypes, factory tools, and similar.

Userspace access fits prototypes, test benches, production-line tools, simple protocols to a microcontroller that
change often, and memory-mapped devices with one user and no matching subsystem (UIO). State the choice and its
reason before writing code. This step is done when you can name the driver you searched for and why userspace wins.

## Read the Target First

1. Read the target kernel's version: `uname -r` on the device, or the top `Makefile` of its source.
2. Read its configuration from the BSP's defconfig, `/proc/config.gz` (present only with `CONFIG_IKCONFIG_PROC`), or
   `/boot/config-*`. Without either, `/lib/modules/$(uname -r)/modules.builtin` and `modules.alias` show which
   drivers exist.
3. Read the versions of the libraries the image ships, such as libgpiod, i2c-tools, and systemd.
4. Read the interface documents in that kernel's `Documentation/`. In recent trees they are `userspace-api/gpio/`,
   `i2c/dev-interface.rst`, `spi/spidev.rst`, `driver-api/uio-howto.rst`, and `watchdog/watchdog-api.rst`. Older
   trees place some elsewhere, so search `Documentation/` by name, and read the uAPI header under
   `include/uapi/linux/` when no document exists.

This step is done when you know the kernel version, which interfaces its configuration enables, and the library
versions. Version-dependent facts follow:

- GPIO has three userspace interfaces: the character device's v2 ioctls from kernel 5.10, its older v1 ioctls, and
  the deprecated `/sys/class/gpio`. libgpiod 2.x needs v2; the 1.6 series uses v1. On a kernel with only v1 or only
  sysfs, say so to the user, and read that interface's documents in the target tree rather than the v2 rules here.
- libgpiod 2.0 is not compatible with the 1.x API, so examples written for 1.x do not build against 2.x.
- The Python package `gpiod` up to 1.5.4 is an unrelated, deprecated project; the official bindings are 2.0.2 and
  later.
- Confirm every ioctl and sysfs attribute you use in the target's headers or `Documentation/ABI/`, because they
  are added and deprecated between releases.

## Choose the Interface

| Device                | Use                                                                      | Avoid                                         |
| --------------------- | ------------------------------------------------------------------------ | --------------------------------------------- |
| GPIO line             | `/dev/gpiochipN` through libgpiod                                        | `/sys/class/gpio` where the chardev exists    |
| I2C chip              | `/dev/i2c-N` with `I2C_RDWR`, or the `libi2c` SMBus helpers              | `I2C_SLAVE_FORCE` on a driver-owned address   |
| SPI chip              | `/dev/spidevB.C` with `SPI_IOC_MESSAGE`                                  | `compatible = "spidev"` in a device tree      |
| Memory-mapped block   | UIO with a small kernel part; VFIO for PCI behind an IOMMU               | `/dev/mem` in anything that ships             |
| Serial or RS-485 port | termios in raw mode, `TIOCSRS485` for RS-485                             | Canonical mode for binary protocols           |
| Buttons, touch, keys  | evdev, `/dev/input/eventN`                                               | Polling GPIO for a button `gpio-keys` handles |
| LED and backlight     | `/sys/class/leds/` and `/sys/class/backlight/`, `brightness`             | Toggling the LED's GPIO line                  |
| Sensors               | hwmon or IIO attributes and buffers                                      | Raw bus access to a chip with a driver        |
| Watchdog              | systemd's `RuntimeWatchdogSec=` and `WatchdogSec=`; else `/dev/watchdog` | Two programs opening the device               |
| Device arrival        | sd-device or libudev monitors, filtered by subsystem                     | Polling `/dev` for a node                     |

This step is done when each device the code touches has its interface named, and that interface exists in the
target kernel. For each bus interface, its traps, and `/dev/mem`, read [references/buses.md](references/buses.md).
For serial, input, LEDs, sensors, the watchdog, uevents, and device-tree properties, read
[references/other-interfaces.md](references/other-interfaces.md). Command-line bring-up and exploring the running
device tree belong to `embedded-linux-bringup`; a new kernel driver belongs to `linux-kernel-development`.

## Hold the Device Correctly

- Give each device one owner. When a kernel driver is bound, change the device tree or unbind the driver
  deliberately, never force access around it.
- Hold the request for as long as the state must hold. A GPIO line keeps its requested state only until the request
  file descriptor closes, after which the kernel may revert it.
- Label every GPIO request with a consumer name, so `gpioinfo` shows which program holds a line.
- Zero every structure passed to an ioctl, including unused fields, as `spidev.rst` requires.
- Check the result of every ioctl and read `errno`. `EBUSY` from a request usually means another owner holds the
  device.
- Treat configuration as requested, not confirmed. The kernel may emulate debounce and drive modes or ignore bias,
  and reports what was requested; RS-485 setup returns the settings it accepted.
- Wait for events with `poll()` on the file descriptor, never with a sleep loop, and check GPIO event sequence
  numbers for events the kernel dropped.

## Name and Permit Devices

Never hard-code a numbered node. `gpiochipN`, `i2c-N`, `spidevB.C`, and `ttyUSBN` follow probe order, and the I2C
documentation says adapter numbers can change between boots. Find a GPIO line by its name or its chip's label,
an I2C bus through `/sys/class/i2c-dev/`, and a USB serial adapter through `/dev/serial/by-id/`. For anything else,
ship a udev rule that creates a stable symlink.

Run the program as an unprivileged user in a group that owns the device node, not as root. systemd's default rules
give groups only to serial ports, input devices, and a few others; GPIO, I2C, SPI, UIO, and watchdog nodes need the
product's own udev rule and group. Sysfs attributes, such as an LED's `brightness`, are root-writable by default and
need their own setup. For device nodes, sysfs attributes, capabilities, and the systemd sandbox, read
[references/permissions.md](references/permissions.md).

## Done

The code is ready when:

- the choice of userspace over a kernel driver is stated, with the driver search behind it;
- every interface used exists in the target kernel and library versions, and any deprecated one is used only
  because the target lacks its replacement, with that reason stated;
- every device is found by a stable name and held by one owner, which `gpioinfo` shows by consumer name for GPIO;
- every ioctl result is checked and every uAPI structure is zeroed;
- the program runs as an unprivileged user with only the device access it needs, shown by `ls -l` on each node and
  attribute it opens, and set up by a udev rule the image ships, plus a unit file where systemd is init.
