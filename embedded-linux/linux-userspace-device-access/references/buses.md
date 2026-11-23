# GPIO, I2C, SPI, UIO, and `/dev/mem`

The interfaces for driving a bus or a register block from userspace. Each section names the kernel document to read
in the target tree, because the details change between releases.

## Contents

- GPIO
- I2C
- SPI
- UIO and VFIO
- `/dev/mem`

## GPIO

Read `Documentation/userspace-api/gpio/chardev.rst` and `include/uapi/linux/gpio.h` in the target kernel.

The interface is one character device per GPIO chip, `/dev/gpiochipN`. Its v2 ioctls arrived in kernel 5.10. The v1
ioctls and the `/sys/class/gpio` interface are both deprecated:

- `/sys/class/gpio` exists only when the kernel sets `CONFIG_GPIO_SYSFS`, which needs `CONFIG_EXPERT`. Its exported
  lines stay exported when the owning process crashes, and its global numbers are not stable. The kernel planned to
  remove it and still carries it, so code for a kernel that has the character device must not depend on it.
- `CONFIG_GPIO_CDEV_V1` keeps the v1 ioctls for old programs.

Use libgpiod rather than raw ioctls. Its v2 series has C, C++, Python, and Rust bindings and the command-line tools
`gpiodetect`, `gpioinfo`, `gpioget`, `gpioset`, and `gpiomon`. From v2.3, libgpiod builds with Meson, not autotools. In
Rust, `gpiocdev` is a pure-Rust equivalent of libgpiod; the older `gpio-cdev` crate appears to implement only the v1
ioctls, so check its source against the target before choosing it.

The rest of this section describes libgpiod 2.x on the v2 ioctls, from kernel 5.10. For libgpiod 1.x, the v1 ioctls,
or sysfs, read the documents for that interface in the target tree.

A v2 request in C takes this shape:

1. Open the chip with `gpiod_chip_open("/dev/gpiochipN")`.
2. Build a `gpiod_line_settings` with direction, edge detection, bias, debounce period, and output value.
3. Add the settings to a `gpiod_line_config` for the line offsets.
4. Set a consumer name in a `gpiod_request_config`.
5. Call `gpiod_chip_request_lines()`, and keep the returned request until the state no longer needs to hold.
6. Release it with `gpiod_line_request_release()`.

The v2 interface's rules for a request:

- A request holds at most 64 lines. A line that another request or a kernel driver holds fails with `EBUSY`.
- The requested state holds until the request file descriptor closes. After that the line may revert to its default.
- Edge detection needs an input line with interrupt support, and fails with `ENXIO` otherwise.
- Debounce applies to inputs only. The kernel emulates it in software when the hardware lacks it.
- The line information reports the requested configuration, not what the hardware does. Userspace cannot tell
  whether bias, debounce, or drive mode is implemented in hardware, emulated, or ignored.
- Edge events are read whole from the request file descriptor. Wait with `poll()`. The kernel buffers 16 events per
  line by default and drops the oldest on overflow; a gap in `seqno` or `line_seqno` shows the loss.
- Edge polarity follows the logical value, so an active-low line swaps rising and falling edges.

libgpiod objects are not thread-safe: use each from one thread at a time. Find a line by its name with the tools or
`gpiod_chip_get_line_offset_from_name()` rather than by a number copied from a schematic.

## I2C

Read `Documentation/i2c/dev-interface.rst` in the target kernel.

The `i2c-dev` driver exposes each adapter as `/dev/i2c-N`. Find the bus through `/sys/class/i2c-dev/` or
`i2cdetect -l`, matching the adapter's name.

- Select the device with `ioctl(fd, I2C_SLAVE, addr)`. `I2C_SLAVE_FORCE` uses the address even when a kernel driver
  owns it; use it only on a bench, never as the fix for a busy address.
- Use `I2C_RDWR` for a register read, which needs a write and a read without a stop between them. Plain `read()` and
  `write()` cannot combine the two. Check `I2C_FUNCS` for `I2C_FUNC_I2C` first.
- Prefer SMBus commands when the chip supports them. The `i2c_smbus_*` helpers come from `libi2c` in i2c-tools, with
  `<linux/i2c-dev.h>` and `<i2c/smbus.h>`. They are inline functions, so the code must build with optimisation on.
- The SMBus helpers return -1 and set `errno` on failure. Size SMBus block buffers for 32 bytes, the SMBus block
  maximum.

Libraries in other languages: `i2cdev` in Rust, and `smbus2` or `python-periphery` in Python.

## SPI

Read `Documentation/spi/spidev.rst` in the target kernel.

The `spidev` driver exposes `/dev/spidevB.C` for bus B and chip select C, created by udev or mdev when the driver
binds.

- Use `SPI_IOC_MESSAGE(N)` with an array of `struct spi_ioc_transfer` for full-duplex and multi-part transfers.
  `read()` and `write()` are half duplex and release chip select between calls.
- Set the mode, bits per word, and maximum speed explicitly with the `SPI_IOC_WR_*` ioctls. The controller may run
  slower than requested, and nothing reports the actual rate.
- SPI has no acknowledgement, so talking to an absent device returns no error. Verify the device with a read of a
  known register, such as an ID.
- Userspace cannot change chip-select polarity, and one transfer is limited to a page by default.

The device tree must name the real device, never `compatible = "spidev"`. Current kernels reject that string,
because spidev is a Linux implementation detail, not hardware, and upstream does not accept vendor `spidev`
strings either. An old vendor kernel may still accept it; read `spidev.rst` and the ID tables in
`drivers/spi/spidev.c` in the target tree, and use the real device name even where the bare string still works.
The routes the current documentation supports are:

- for a product, add the real device's compatible string to spidev's ID tables in the kernel, or write a driver;
- for a test bench, bind spidev to an existing device through
  `echo spidev > /sys/bus/spi/devices/spiB.C/driver_override`, then
  `echo spiB.C > /sys/bus/spi/drivers/spidev/bind`, after checking that the target kernel has `driver_override`
  for SPI.

Recent kernels also document a `new_device` attribute under `/sys/class/spi_master/spiN/` that creates a device from
userspace. Check `Documentation/spi/` in the target tree before using it.

## UIO and VFIO

Read `Documentation/driver-api/uio-howto.rst` in the target kernel.

UIO fits a memory-mapped device that one program uses and that fits no kernel subsystem. Network, serial, and USB
devices do not qualify. UIO still needs a kernel part. `uio_pdrv_genirq` serves platform devices, and its device-tree
use needs the `of_id` module parameter; `uio_pci_generic` serves PCI devices.

- Read `name`, `version`, and each map's `size` and `offset` under `/sys/class/uio/uioX/` before mapping.
- Map region N with `mmap()` at an offset of N times the page size. Add the map's `offset` to the returned pointer
  when the region is not page aligned.
- Wait for an interrupt with a blocking `read()` of exactly 4 bytes, which returns the total interrupt count. A jump
  of more than one means missed interrupts.
- With `uio_pdrv_genirq`, the kernel disables the interrupt each time it fires. Write a 32-bit 1 to the file to enable
  it again. The interrupt line must not be shared.
- Do in the kernel handler anything the hardware needs after each interrupt, because the userspace program can die
  at any time.

Use VFIO instead when the device does DMA and sits behind an IOMMU, typically a PCI device. VFIO protects memory
through the IOMMU and can run without root; UIO does neither.

## `/dev/mem`

`/dev/mem` maps physical addresses directly. Use it only for bring-up and debugging, with BusyBox `devmem` or a
one-off tool, and never in shipped code:

- it bypasses the driver that owns the registers, so the two can conflict;
- it gives no interrupts, clocks, power management, or pin multiplexing;
- it needs root or `CAP_SYS_RAWIO`.

Keep `CONFIG_STRICT_DEVMEM` enabled in product kernels, which limits `/dev/mem` to non-RAM addresses. Its default
differs between architectures, so read the target's configuration. `CONFIG_IO_STRICT_DEVMEM` further blocks ranges
that a driver has claimed. When a register needs regular access from userspace, write a UIO or kernel driver
instead.
