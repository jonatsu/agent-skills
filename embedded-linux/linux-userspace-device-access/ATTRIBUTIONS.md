# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### The Linux kernel: userspace interface documentation and headers

- Source: <https://github.com/torvalds/linux>, `Documentation/userspace-api/gpio/`, `Documentation/driver-api/gpio/`,
  `Documentation/i2c/dev-interface.rst`, `Documentation/spi/`, `Documentation/driver-api/uio-howto.rst`,
  `Documentation/driver-api/vfio.rst`, `Documentation/driver-api/serial/serial-rs485.rst`, `Documentation/input/`,
  `Documentation/leds/`, `Documentation/hwmon/`, `Documentation/iio/`, `Documentation/watchdog/`,
  `Documentation/ABI/testing/sysfs-class-led`, and `Documentation/ABI/stable/sysfs-class-backlight`, with
  `include/uapi/linux/gpio.h`, `i2c-dev.h`, and `spi/spidev.h`, `drivers/gpio/Kconfig`,
  and `lib/Kconfig.debug`
- License: `GPL-2.0-only`
- Version: `v7.3`

The interfaces, their limits and deprecations, the policy on GPIO from userspace, the spidev device-tree rule, UIO
and VFIO, RS-485 setup, the LED, backlight, hwmon, and IIO attributes, and the watchdog interface come from this
documentation. No prose was copied.

### libgpiod

- Source: <https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git>, its documentation, `NEWS`, and `examples/`
- License: `LGPL-2.1-or-later AND GPL-2.0-or-later`
- Version: `v2.3.2`

The library is `LGPL-2.1-or-later`, and the tools and examples are `GPL-2.0-or-later`. The v2 request sequence,
thread-safety rule, tool behaviour, the v1 to v2 break, the Python package history, and the Meson build come from it. No
code was copied.

### systemd: udev rules and unit documentation

- Source: <https://github.com/systemd/systemd>, `rules.d/50-udev-default.rules.in`, `rules.d/60-serial.rules`,
  `sysusers.d/basic.conf.in`, `src/systemd/sd-device.h`, and the man pages `udev(7)`, `libudev(3)`,
  `systemd.exec(5)`, `systemd.resource-control(5)`, `systemd-system.conf(5)`, and `systemd.service(5)`
- License: `LGPL-2.1-or-later`
- Version: systemd 262 for the man pages; the rules, `sysusers.d`, and header from `main`, read 2026-11-23

The default device groups, the serial by-id links, the libudev status, the device monitor API, and the service
watchdog and device-sandboxing options come from it. No prose was copied.

### The Linux man-pages project

- Source: <https://www.kernel.org/doc/man-pages/>, `termios(3)`, `TIOCEXCL(2const)`, and `capabilities(7)`
- License: `LicenseRef-ManPages`
- Version: man-pages 6.19

Each page states its own licence. The raw-mode settings, the `VMIN` and `VTIME` cases, exclusive mode, and the raw I/O
capability come from these pages. No prose was copied.

## Third-party Sources

### Bootlin: embedded Linux and kernel driver training

- Source: <https://bootlin.com/doc/training/embedded-linux/> and <https://bootlin.com/doc/training/linux-kernel/>,
  slides and labs
- License: `CC-BY-SA-3.0`
- Version: releases dated 2026-09-25

The trade-offs between kernel and userspace drivers, the advice to search the kernel tree for an existing driver,
the GPIO expander example, and the shortcomings of sysfs GPIO come from these slides. The skill states these
facts in its own words; no text or figures were copied.
