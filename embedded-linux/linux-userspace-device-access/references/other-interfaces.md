# Serial, Input, LEDs, Sensors, Watchdog, Uevents, and Device-Tree Properties

The device classes whose kernel driver already exists, so userspace only consumes the interface it exposes. Each
section names the document to read in the target tree or its man pages.

## Contents

- Serial and RS-485
- Input
- LED and Backlight
- hwmon and IIO
- Watchdog
- Device Arrival
- Device-Tree Properties

## Serial and RS-485

Read `termios(3)` and, for RS-485, `Documentation/driver-api/serial/serial-rs485.rst` in the target kernel.

For a binary protocol, put the port in raw mode:

1. Read the current settings with `tcgetattr()`.
2. Call `cfmakeraw()`, which turns off echo, canonical input, signals, and all input and output translation.
3. Set `CREAD` and `CLOCAL` yourself, because `cfmakeraw()` sets neither.
4. Set the speed with `cfsetispeed()` and `cfsetospeed()`.
5. Set `VMIN` and `VTIME`, which `cfmakeraw()` leaves alone, by the read behaviour the protocol needs.
6. Apply the settings with `tcsetattr()`, then read them back to confirm.

`VTIME` counts tenths of a second. The four combinations behave differently:

| `VMIN` | `VTIME` | `read()` returns                                                                             |
| ------ | ------- | -------------------------------------------------------------------------------------------- |
| 0      | 0       | At once, with whatever is available, possibly 0 bytes                                        |
| > 0    | 0       | After `VMIN` bytes, blocking without limit                                                   |
| 0      | > 0     | After the first byte, or 0 bytes once `VTIME` expires                                        |
| > 0    | > 0     | After `VMIN` bytes, or when `VTIME` passes between bytes; the timer starts at the first byte |

`ioctl(fd, TIOCEXCL)` makes further opens of the port fail with `EBUSY`, except for a process with `CAP_SYS_ADMIN`. It
does not affect a process that already holds the port open, so it does not replace a lock between cooperating
programs.

For RS-485, read the current `struct serial_rs485` with `TIOCGRS485`, change the flags and delays, write it with
`TIOCSRS485`, and read it back. The kernel clears the bits the driver does not support and returns the accepted
state, so compare before relying on a feature. The delays are in milliseconds. A device tree can set RS-485 defaults
at boot through the `rs485` binding properties.

Platform UARTs such as `ttyS*` and `ttymxc*` have fixed names from the device tree. USB adapters do not; find them
through `/dev/serial/by-id/`, which systemd's rules build from the adapter's USB serial number. Two identical
adapters without serial numbers can collide there, so check the links on the target and use `/dev/serial/by-path/` for them.

Libraries: `serialport` in Rust; `pyserial` or `python-periphery` in Python.

## Input

Read `Documentation/input/input.rst` in the target kernel.

Read buttons, keys, touch, and similar devices through evdev, `/dev/input/eventN`. Every `read()` returns whole
`struct input_event` records, and `poll()` works on the node. For an `EV_KEY` event, a value of 0 means release, 1
press, and 2 autorepeat. The event codes are in `include/uapi/linux/input-event-codes.h`.

A button on a GPIO line belongs to the `gpio-keys` driver in the device tree, which debounces it and reports it
through evdev. Do not poll the GPIO line from userspace. Find the right event node by its name in
`/sys/class/input/eventN/device/name` or a udev symlink, never by its number.

In C, the `libevdev` library wraps the interface; in Rust, the `evdev` crate; in Python, `python-evdev`.

## LED and Backlight

Read `Documentation/leds/leds-class.rst` and `Documentation/ABI/stable/sysfs-class-backlight` in the target kernel.

- An LED appears under `/sys/class/leds/<devicename:color:function>/`. Write a value from 0 to
  `max_brightness` into `brightness`. Writing 0 also clears an active trigger.
- Let the kernel blink an LED through `trigger`. The `timer` trigger takes `delay_on` and `delay_off` in
  milliseconds, so no userspace loop is needed.
- A backlight appears under `/sys/class/backlight/<name>/`. Write `brightness` and read it to decide, not
  `actual_brightness`, which the kernel documents as the value read from hardware. `bl_power` turns it on (0) and
  off (4).
- When several backlights exist, prefer type `firmware`, then `platform`, then `raw`.

An LED on a GPIO line belongs to the `leds-gpio` driver in the device tree, which gives it this interface.

## hwmon and IIO

Read `Documentation/hwmon/sysfs-interface.rst`, `Documentation/iio/iio_devbuf.rst`, and the ABI files
`Documentation/ABI/testing/sysfs-class-hwmon` and `sysfs-bus-iio` in the target kernel. Take each attribute's unit
and scaling from those files, never from memory.

- Find a hwmon chip through `/sys/class/hwmon/hwmon*/` and its `name` file, because the number can change. Attribute
  files hold one fixed-point value each, such as `temp1_input`. The kernel recommends `libsensors`, which applies the
  conversions and labels.
- Read an IIO channel once through its sysfs attributes, such as `in_voltage0_raw` with its `_scale` and `_offset`.
- To stream IIO samples, enable each channel's `_en` attribute in `bufferY/scan_elements`, set `length` and
  `watermark`, and write `enable` last. Then read `/dev/iio:deviceX`. Each channel's `_type` attribute gives the
  sample format, such as `le:s12/16>>4`, and samples are naturally aligned with padding.
- Use `libiio` for a C or C++ library over IIO.

When a chip has a hwmon or IIO driver, use it rather than reading the chip over raw I2C or SPI.

## Watchdog

Read `Documentation/watchdog/watchdog-api.rst` in the target kernel and `systemd-system.conf(5)` and
`systemd.service(5)` when systemd is init.

Give the hardware watchdog one owner, because each ping and each close acts on the whole system. When systemd is init,
let it own the device:

- `RuntimeWatchdogSec=` in `system.conf` makes systemd open the hardware watchdog and ping it at half that interval.
- Each critical service sets `WatchdogSec=` in its unit and calls `sd_notify(0, "WATCHDOG=1")` at least every half
  of the interval. `sd_watchdog_enabled()` reads the interval systemd passed. When a service misses it, systemd kills
  it with `SIGABRT` and `Restart=` restarts it.

Without systemd, one daemon opens `/dev/watchdog`:

- Opening the device starts the watchdog, and any write or `WDIOC_KEEPALIVE` pings it.
- Set the timeout with `WDIOC_SETTIMEOUT`, then read back the value the driver chose, which may differ.
- Ping at about half the timeout.
- Before an intentional stop, write `V` and close, so a driver with magic close stops the watchdog. A close without
  `V` lets the board reset, which is the intended behaviour when the daemon dies.
- `CONFIG_WATCHDOG_NOWAYOUT` makes the watchdog impossible to stop once started.

## Device Arrival

Wait for a device to appear by monitoring uevents, filtered by subsystem, rather than polling `/dev`. In new code, use
the `sd_device_monitor_*` functions from `libsystemd`, declared in `<systemd/sd-device.h>`. systemd documents
`libudev` as supported but not for new projects. In Python, `pyudev` wraps libudev.

## Device-Tree Properties

A program that reads a property of the running device tree, such as the board's `model` or a vendor property, reads a
file under `/proc/device-tree`. Integer properties are sequences of big-endian 32-bit cells. Read each cell by copying
4 bytes with `memcpy` into a `uint32_t` and converting it with `be32toh`, never by reading the file straight into an
integer, and check that the file's length is a whole number of cells. A string property ends in a NUL byte, and a
string list holds several. For exploring the tree by hand, use `embedded-linux-bringup`.
