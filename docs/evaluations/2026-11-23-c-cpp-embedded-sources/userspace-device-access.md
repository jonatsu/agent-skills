# Userspace device access: research notes

Read date: 2026-11-23. Scope: sources for the skill `linux-userspace-device-access`.

Labels: **SS** = the source states it. **INF** = my inference from sources. **BG** = background knowledge from memory,
not verified when the notes were written. The short names below stand for public documents and are cited with a slide
page or chapter path:

- `kernel-docs v7.3` is the kernel's rendered documentation at v7.3, published at <https://docs.kernel.org/>.
- `bootlin-embedded-linux` is Bootlin's "Embedded Linux system development" training, slides and BeagleBone labs,
  at <https://bootlin.com/doc/training/embedded-linux/>.
- `bootlin-linux-kernel` is Bootlin's "Linux kernel and driver development" training, slides and labs, at
  <https://bootlin.com/doc/training/linux-kernel/>.

## 0. Sources, pins and licences

| Source                                                        | Pin                                                                                                                                                        | Licence                                                                                                                           | Route                                                      |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `kernel-docs` v7.3                                            | rendered documentation, v7.3                                                                                                                               | GPL-2.0-only                                                                                                                      | public release                                             |
| `bootlin-embedded-linux`                                      | release dated 2026-09-25; slides p.N of 551; labs chapters 08 and 10                                                                                       | CC-BY-SA-3.0                                                                                                                      | public release                                             |
| `bootlin-linux-kernel`                                        | release dated 2026-09-25; slides p.N of 446                                                                                                                | CC-BY-SA-3.0                                                                                                                      | public release                                             |
| Linux kernel docs, uAPI headers, Kconfig                      | tag `v7.3` (tag object `091b06388b117fefdcb63336ac09956a4914b961`)                                                                                         | docs GPL-2.0; uAPI headers `GPL-2.0-only WITH Linux-syscall-note` (spidev.h and i2c-dev.h are `GPL-2.0+ WITH Linux-syscall-note`) | raw.githubusercontent.com via docs-mcp                     |
| Kernel `lib/Kconfig.debug` STRICT_DEVMEM help                 | `master` (read 2026-11-23; v7.3 file timed out)                                                                                                            | GPL-2.0                                                                                                                           | gh_grep                                                    |
| libgpiod 2.x docs, NEWS, COPYING, examples                    | tag `v2.3.2` (commit `3435867dd1469c8058924267b4f869058d3c4e52`, 2026-11-03), docs from readthedocs `master`, NEWS and COPYING from GitHub mirror `master` | LGPL-2.1-or-later (library and C++ bindings, since v2.2); GPL-2.0-or-later (tools, tests, examples); CC-BY-SA-4.0 (text files)    | docs-mcp; upstream git.kernel.org is behind an Anubis wall |
| man-pages `termios(3)`, `TIOCEXCL(2const)`, `capabilities(7)` | man-pages 6.19, man7.org HTML rendered 2026-09-09                                                                                                          | man pages are mostly BSD/GPL-2+ free-form per page; not individually checked                                                      | docs-mcp                                                   |
| systemd man pages                                             | `latest` on freedesktop.org, page footer shows systemd 262; rules from `systemd/systemd` `main`                                                            | LGPL-2.1-or-later (sd-device.h header SPDX)                                                                                       | docs-mcp                                                   |
| Crate and PyPI metadata                                       | crates.io API and PyPI JSON, read 2026-11-23                                                                                                               | per package, listed in the tables below                                                                                           | docs-mcp                                                   |

## Q1 GPIO

### Kernel status of the interfaces

- SS: the userspace ABI is a character device per chip, `/dev/gpiochip0` to `/dev/gpiochipN`.
  (`kernel-docs v7.3 driver-api/gpio/using-gpio`)
- SS: kernel policy. "The most obvious, natural and preferred way to use GPIO lines is to let kernel hardware drivers
  deal with them." The userspace ABI is "intended for one-off deployments": prototypes, factory lines, maker
  projects, production tools, industrial automation, PLC-type use, door controllers. "Do not under any circumstances
  abuse the GPIO userspace ABI to cut corners in any product development projects. If you use it for prototyping,
  then do not productify the prototype: rewrite it using proper kernel drivers. Do not under any circumstances
  deploy any uniform products using GPIO from userspace." (same page)
- SS: `drivers-on-gpio` lists the kernel drivers that already cover common GPIO jobs: `leds-gpio` (LED sysfs),
  `ledtrig-gpio`, `gpio-keys` and `gpio-keys-polled` (with debounce), `gpio_mouse`, `gpio-beeper`, and others.
  (`kernel-docs v7.3 driver-api/gpio/drivers-on-gpio`)
- SS: the chardev ABI v2 "First added in 5.10". It carries the note: "Do NOT abuse userspace APIs to control
  hardware that has proper kernel drivers", and points to SPI, I2C, PWM and W1 subsystems for multi-function
  lines. (`Documentation/userspace-api/gpio/chardev.rst` at v7.3)
- SS: ABI v1 is deprecated. Header comment: "This version of the ABI is deprecated. Use the latest version of the
  ABI". Kconfig `GPIO_CDEV_V1`: "This ABI version is deprecated." (`include/uapi/linux/gpio.h`,
  `drivers/gpio/Kconfig`, v7.3)
- SS: sysfs `/sys/class/gpio` status. `Documentation/userspace-api/gpio/sysfs.rst` (v7.3): "This API is obsoleted by the
  chardev.rst ... New developments should use the chardev.rst, and existing developments are encouraged to migrate as
  soon as possible, as this API will be removed in the future." Kconfig `GPIO_SYSFS` is `bool ... if EXPERT`, "This ABI
  is deprecated", and it `select GPIO_CDEV`. `GPIO_SYSFS_LEGACY` (global number space) is a separate option.
  `Documentation/ABI/obsolete/sysfs-gpio` says it "will be removed after 2020"; the interface still exists at v7.3, so
  that date was missed.
  - INF: status is deprecated and obsolete, still compiled when `CONFIG_GPIO_SYSFS` is set, no firm removal date.
    Code for new targets should not use it. A skill can say "present only if the kernel enables `GPIO_SYSFS`".
- SS: Bootlin names two sysfs shortcomings: GPIOs stay exported when the owning process crashes, and the GPIO numbers
  must be computed and are not stable. (`bootlin-embedded-linux` slides p.281)
- SS: the libgpiod docs state the chardev interface "guarantees all allocated resources are freed after closing the
  device file descriptor" and adds reliable event polling, multi-line get and set, and open-drain and open-source
  drive. The docs say the chardev was introduced in kernel 4.8; the Rust gpio-cdev README says v1 was stabilised in
  Linux 4.4. These two dates conflict; I did not resolve them. (libgpiod readthedocs index; gpio-cdev README)

### uAPI v2 semantics (`Documentation/userspace-api/gpio/*.rst` and `gpio.h`, v7.3)

| Topic           | What the source states                                                                                                                                                                                                                                                                                                                                                                                 |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Request         | `GPIO_V2_GET_LINE_IOCTL` on the chip fd returns a request fd. The process gets exclusive access to value and configuration. A line already in use gives `EBUSY`.                                                                                                                                                                                                                                       |
| Lifetime        | Line state "is guaranteed to remain as requested until the returned file descriptor is closed". After close the line "may revert to its default state". Closing the chip fd does not affect requests.                                                                                                                                                                                                  |
| Limits          | At most 64 lines per request (`GPIO_V2_LINES_MAX`), 10 per-line attributes, consumer and line name buffers of 32 bytes.                                                                                                                                                                                                                                                                                |
| Consumer label  | `consumer` field in the request, for example "my-bitbanged-relay". `gpio_v2_line_info.consumer` shows the current user, and is empty when unused or when the user set none. `GPIO_V2_LINE_FLAG_USED` marks a line unavailable.                                                                                                                                                                         |
| Direction       | INPUT and OUTPUT cannot be combined. With neither, the line is taken "as-is" (only ACTIVE_LOW allowed).                                                                                                                                                                                                                                                                                                |
| Drive and bias  | OPEN_DRAIN or OPEN_SOURCE need OUTPUT; one drive flag; one bias flag; bias needs a direction flag.                                                                                                                                                                                                                                                                                                     |
| Edge            | Edge flags need INPUT. Edge detection on a line without interrupt support fails with `ENXIO`.                                                                                                                                                                                                                                                                                                          |
| Debounce        | `debounce_period_us` attribute, inputs only. It applies to values and edges. The kernel emulates it in software if hardware lacks it. The event timestamp is the end of the debounce period.                                                                                                                                                                                                           |
| Support policy  | Bias: best effort. Debounce: emulate. Direction: reject. Drive: emulate. Edge detection: reject. "Userspace cannot determine if a feature is supported in hardware, is emulated, or is best effort." The reported line info is the requested configuration, not the result.                                                                                                                            |
| Events          | `read()` on the request fd returns whole `gpio_v2_line_event` structs. Default clock `CLOCK_MONOTONIC`, with REALTIME and HTE flags. Kernel buffer defaults to 16 events per line. On overflow the oldest event is dropped, and `seqno` and `line_seqno` reveal the loss. Blocking unless `O_NONBLOCK`; use `poll()`. Edge polarity follows the logical value, so ACTIVE_LOW swaps rising and falling. |
| Line info watch | REQUESTED, RELEASED, CONFIG events show who took or released a line.                                                                                                                                                                                                                                                                                                                                   |

### libgpiod v2 (pin: v2.3.2)

- SS: `libgpiod` is a low-level C library, bindings and tools. Bindings in the tree: C++, GLib, Python, Rust. Tools:
  `gpiodetect`, `gpioinfo`, `gpioget`, `gpioset`, `gpiomon`, `gpionotify`. A D-Bus daemon (`gpio-manager`) and client
  arrived in v2.2. (readthedocs `bindings`, `gpio_tools`; NEWS)
- SS: v2.0 "breaks compatibility with the v1.6.x series": the whole API was reworked, including C++ and Python, and
  `gpiofind` was dropped. (NEWS) INF: code and docs written for v1 (`gpiod_line_request_*` style from 1.x,
  `gpiod_chip_open_by_name`) do not apply to v2.
- SS: core API shape (from `examples/toggle_line_value.c` and `watch_line_value.c` at v2.3.2): `gpiod_chip_open(path)`,
  `gpiod_line_settings_new` plus setters (direction, edge detection, bias, debounce period in microseconds, output
  value), `gpiod_line_config_add_line_settings(cfg, offsets, n, settings)`, `gpiod_request_config_set_consumer`,
  `gpiod_chip_request_lines(chip, req_cfg, line_cfg)`, `gpiod_line_request_set_value`, and
  `gpiod_line_request_read_edge_events` into a `gpiod_edge_event_buffer`. The request holds the lines until
  `gpiod_line_request_release`.
- SS: thread safety. "thread-aware but does not provide any further thread-safety guarantees": at most one thread
  works with an object at a time. Passing NULL to a method aborts. Errors set `errno`. (core_api page)
- SS: tool behaviour that matters for scripts. `gpioset` "maintains the line output state until the process exits,
  but after that is not guaranteed"; by default it does not exit; `--daemonize` detaches, `--toggle` repeats and a
  final period of 0 makes it exit. Default consumer names equal the tool name (`gpioset`, `gpiomon`), override with
  `-C`. `gpiomon` has `--edges`, `--debounce-period`, `--event-clock`, `--idle-timeout`, `--num-events`. Lines can
  be addressed by name; chips by number, name or path. The tool docs note that when a process exits its lines are
  released and "the state of a line may be modified by the kernel or another process".
- SS: libgpiod "provides ... arbitration for multiple simultaneous consumers on the same GPIO chip" (kernel doc
  `using-gpio`). INF: this means several processes can each request different lines of one chip; the kernel arbitrates
  by line (EBUSY), while libgpiod itself adds no inter-process lock.
- SS: build system. Meson replaced autotools in v2.3 ("replace autotools with meson & ninja", NEWS; commit
  `97bab4c` dated 2026-05-04 on the mirror). Bootlin's lab (v2.2.x) still uses `autogen.sh` and `configure`; do not
  copy that part. (`bootlin-embedded-linux` bbb-labs chapter "Third party libraries and applications", section
  "Compiling libgpiod")
- SS: Python. PyPI `gpiod` 2.6.0 (2026-11-04), LGPL-2.1-or-later, Python >=3.10, "official Python bindings"; the C
  library is vendored in the wheel, and `LINK_SYSTEM_LIBGPIOD=1` links the system one. Trap: `gpiod` 1.5.4 and
  earlier is a different, deprecated, unofficial pure-Python package; the official API starts at 2.0.2 and is not
  backward compatible. Documented API: `gpiod.request_lines(path, consumer=..., config={line: LineSettings(...)})`,
  `gpiod.Chip`. (PyPI JSON for `gpiod`; readthedocs python_api)
- INF: the PyPI package version (2.6.0) does not match the libgpiod release version (2.3.2). I did not find a source
  that explains the numbering; the NEWS only say the core C API version was decoupled from the project version.
- SS: Licences. COPYING: library LGPL-2.1-or-later; tools, tests, examples GPL-2.0-or-later; uAPI headers
  GPL-2.0-only with Linux-syscall-note. The C++ bindings were relicensed to LGPL-2.1-or-later in v2.2 (NEWS).
  The upstream repository is on git.kernel.org; the GitHub repository `brgl/libgpiod` states it is a mirror used for
  discussion and issues.
- SS: Bootlin lab examples use `gpiodetect`, `gpioinfo`, `gpioget -c gpiochip0 28`, `gpioset -c gpiochip0 -t0 28=1`,
  and note libgpiod sets the input direction itself. (`bootlin-embedded-linux` bbb-labs, same chapter, "Testing
  libgpiod")
- Gap: I did not read the libgpiod C++ API pages, and did not read the Rust bindings source.

### Rust options

| Crate                  | Version, date     | Licence                    | uAPI                                                                                                    | Note                                                                                                           |
| ---------------------- | ----------------- | -------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `gpiocdev`             | 0.8.0, 2025-11-19 | Apache-2.0 OR MIT          | v1 and v2 (the `gpiocdev-uapi` crate has `v1.rs` and `v2.rs`)                                           | "the equivalent of libgpiod, but in pure Rust" (README); same author as the libgpiod contributor `warthog618`. |
| `gpio-cdev`            | 0.6.0, 2023-09-12 | MIT OR Apache-2.0          | v1 only (SS: `src/ffi.rs` defines `GET_LINEHANDLE` and `GET_LINEEVENT` ioctls; no v2 ioctl found there) | Older. README says sysfs was "planned to be removed ... after year 2020". Has a tokio feature.                 |
| `libgpiod`             | 1.0.0, 2025-09-30 | Apache-2.0 OR BSD-3-Clause | v2, wraps the C library                                                                                 | Repository field points at git.kernel.org; this is the in-tree Rust binding.                                   |
| `gpiod`, `tokio-gpiod` | 0.3.0, 2024-05-11 | MIT                        | not checked                                                                                             | Not examined.                                                                                                  |

- INF: for new Rust code, `gpiocdev` is the better default. It speaks v2 and needs no C library. `gpio-cdev` is v1
  only and has not been released since 2023. The `libgpiod` crate fits when the project already ships libgpiod.
- Caveat: `gpio-cdev` v1-only is from reading `src/ffi.rs` on `master`, not from its docs.

## Q2 I2C and SPI

### i2c-dev (`Documentation/i2c/dev-interface.rst`, v7.3; `include/uapi/linux/i2c-dev.h`)

- SS: load module `i2c-dev`. Nodes are `/dev/i2c-N`, character major 89. Adapter numbers "are assigned somewhat
  dynamically ... They can even change from one boot to the next"; inspect `/sys/class/i2c-dev/` or `i2cdetect -l`.
- SS: set the address with `ioctl(fd, I2C_SLAVE, addr)`. `I2C_SLAVE_FORCE` uses the address "even if it is already
  in use by a driver!". Plain `read()` and `write()` cannot do combined transactions, so "this interface is almost
  never used by user-space programs" in that form.
- SS: `I2C_RDWR` does a combined read and write without a stop in between. It needs `I2C_FUNC_I2C`. The address and
  10-bit flag are per message and override `I2C_SLAVE`. The header limit is `I2C_RDWR_IOCTL_MAX_MSGS` = 42.
  Other ioctls: `I2C_FUNCS`, `I2C_TENBIT`, `I2C_PEC`, `I2C_SMBUS`, `I2C_RETRIES`, `I2C_TIMEOUT` (units of 10 ms).
- SS: "SMBus commands are preferred if the device supports them." The `i2c_smbus_*` helpers come from `libi2c` in
  i2c-tools, which also supplies `i2cdetect`. Include `<linux/i2c-dev.h>` and `<i2c/smbus.h>`. "Because of the use
  of inline functions, you *have* to use '-O' or some variation when you compile". SMBus block buffers need not
  exceed 32 bytes. Return -1 and `errno` on failure.
- SS: Bootlin lab: `i2cdetect -r 1` warns "This program can confuse your I2C bus". A device already bound to a kernel
  driver shows as `UU`; a device that answers but has no driver shows its address. (`bootlin-embedded-linux` bbb-labs
  chapter 08)
- SS: the i2c-dev doc says i2c-dev "can be thought of as a generic I2C chip driver that can be programmed from
  user-space" and that all validation of user parameters happens there.
- Library crates and packages: Rust `i2cdev` 0.6.2 (2025-11-11, MIT/Apache-2.0), `i2c-linux` 0.1.2 (2018, MIT,
  stale). Python `smbus2` 0.6.1 (2026-04-09, MIT), `python-periphery` 2.5.0 (2026-10-29, MIT; covers GPIO, LED, PWM,
  SPI, I2C, MMIO, serial). BG: smbus2 uses the same ioctls.
- INF: with a kernel driver bound, `I2C_SLAVE` fails with `EBUSY` and `I2C_SLAVE_FORCE` bypasses that check; forcing
  access to a device a driver owns is a conflict, not a fix. (EBUSY is BG; the force comment is SS.)

### spidev (`Documentation/spi/spidev.rst`, `Documentation/spi/instantiating-devices.rst`, `spidev.h`, v7.3)

- SS: nodes `/dev/spidevB.C` (bus B, chip select C), character major 153, created by udev or mdev when the `spidev`
  driver binds. "Do not try to manage the /dev character device special file nodes by hand."
- SS: `read()` and `write()` are half-duplex with chip select released between calls. Full duplex and composite
  transfers use `SPI_IOC_MESSAGE(N)` with an array of `struct spi_ioc_transfer` (`tx_buf` and `rx_buf` as `__u64`,
  `len`, `speed_hz`, `bits_per_word`, `delay_usecs`, `cs_change`, `tx_nbits`, `rx_nbits`, `word_delay_usecs`, `pad`).
  "Zero-initialize the structure, including currently unused fields." The layout is the same in 32-bit and 64-bit
  userspace.
- SS: configuration ioctls: `SPI_IOC_RD/WR_MODE` (byte), `SPI_IOC_RD/WR_MODE32`, `..._LSB_FIRST`, `..._BITS_PER_WORD`,
  `..._MAX_SPEED_HZ`. Modes are `SPI_MODE_0` to `SPI_MODE_3` or `SPI_CPOL` and `SPI_CPHA`. The controller may not
  hit the requested speed, and "there's currently no way to report the actual bit rate".
- SS limits: no async I/O; userspace cannot change chip-select polarity; one request is limited to one page by
  default (module parameter); no I/O error appears when talking to an absent device, since SPI has no
  acknowledgement.
- SS: the stated reasons to use it: prototyping where "stray pointers in userspace won't normally bring down any
  Linux system", and simple protocols to microcontrollers that change often. "There are drivers that can never be
  written in userspace, because they need to access kernel interfaces (such as IRQ handlers ...)".
- SS: device-tree rule. "It used to be supported to define an SPI device using the 'spidev' name ... compatible =
  'spidev'. But this is no longer supported by the Linux kernel and instead a real SPI device name as listed in one of
  the tables must be used. Not having a real SPI device name will lead to an error being printed and the spidev driver
  failing to probe." `instantiating-devices.rst` adds: spidev "explicitly rejects the bare 'spidev' compatible string
  in device-tree because spidev is a Linux implementation detail, not a hardware description. Vendor-specific
  compatible strings for spidev (e.g. 'vendor,board-spidev') are also generally not accepted upstream", and device-tree
  overlays do not change this.
- SS: what to do instead. (1) Add the real device name to the spidev tables (`spidev_spi_ids`, `spidev_dt_ids`,
  `spidev_acpi_ids`) by posting a patch to the linux-spi mailing list. (2) Bind from sysfs:
  `echo spidev > /sys/bus/spi/devices/spiB.C/driver_override` then `echo spiB.C > /sys/bus/spi/drivers/spidev/bind`. (3)
  New in the v7.3 docs: `/sys/class/spi_master/spiN/new_device` takes
  `<modalias> <chip_select> [<max_speed_hz> [<mode>]]` and `delete_device` takes the chip select. Devices made this way
  have no IRQ, no DT properties, and no platform data. A `change` uevent on the controller lets a udev rule write to
  `new_device`.
  - Gap: I did not check when `new_device` first appeared.
- Library crates and packages: Rust `spidev` 0.7.1 (2025-10-31, MIT/Apache-2.0); Python `spidev` 3.8 (2025-09-15, MIT),
  `python-periphery`.
- SS (Bootlin): the user-space kernel mechanisms are "I2C: i2c-dev; SPI: spidev; Memory-mapped: UIO; USB:
  /dev/bus/usb, through libusb; PCI: sysfs entries". (`bootlin-embedded-linux` slides p.262)

### When a kernel driver is better (I2C and SPI)

- SS (Bootlin): a GPIO expander driven over `/dev/i2c-0` "is what's not recommended"; the kernel driver is preferred,
  so other kernel drivers can use its GPIOs for reset and interrupt signals. (`bootlin-embedded-linux` slides pp.263-264)
- SS: example search: `git grep -i max7313` finds `drivers/gpio/gpio-pca953x.c`, so the right move is to enable
  `CONFIG_GPIO_PCA953X`. (`bootlin-embedded-linux` slides pp.266-267)
- INF: a kernel driver is also the answer when the chip needs an interrupt line, shares a bus with other drivers, must
  survive suspend, or already has an upstream driver; spidev and i2c-dev expose none of that.

## Q3 UIO, VFIO and `/dev/mem`

### UIO (`kernel-docs v7.3 driver-api/uio-howto`)

- SS: UIO is for hardware where "creating a Linux kernel driver is overkill". Ideal hardware has all three: mappable
  memory that fully controls the device, usually interrupts, and no fit in a standard subsystem. Devices handled by
  networking, serial or USB "are no candidates".
- SS: `mmap()` of `/dev/uioX` maps registers or RAM. Mapping N is selected with `mmap` offset N times the page size.
  Per-map sysfs: `/sys/class/uio/uioX/maps/mapN/{name,addr,size,offset}`; add `offset` to the returned pointer when the
  region is not page aligned. `/sys/class/uio/uioX/{name,version,event}` exist, and the directory may be a symlink.
- SS: interrupts: a blocking `read()` of exactly 4 bytes returns the cumulative interrupt count; a jump above 1 means
  missed interrupts; `select()` works. `write()` of a 32-bit value (0 or 1) calls the driver `irqcontrol()` to disable
  or enable the interrupt and returns `-ENOSYS` if the driver has none. INF: the same HOWTO also says "`/dev/uioX` is a
  read-only file", which is stale next to the `write()` text.
- SS: a kernel part is still required. "You cannot rely on the userspace part of your driver. Your userspace program
  can terminate at any time", so anything the hardware needs after each interrupt must happen in the kernel handler.
- SS: generic kernel parts: `uio_pdrv_genirq` (disables the IRQ line in the kernel; userspace re-enables it by writing
  `0x00000001`; line must not be shared; device-tree use needs the `of_id` module parameter and optional
  `linux,uio-name`), `uio_dmem_genirq` (dynamic DMA regions), `uio_pci_generic` (PCI 2.3 and PCIe, bind with `new_id`,
  userspace must clear the Interrupt Disable bit before waiting), `uio_hv_generic`.
- SS: userspace needs no special library and "can use floating point numbers". x86 I/O ports cannot be mapped;
  use `ioperm()` or `iopl()`, and see `/sys/class/uio/uioX/portio/`.
- SS (Bootlin): UIO is the "memory-mapped devices" option. It "can only be used if" no kernel subsystem is needed and
  one application uses the device. (`bootlin-linux-kernel` slides p.46)

### VFIO (`kernel-docs v7.3 driver-api/vfio`)

- SS: VFIO is "an IOMMU/device agnostic framework for exposing direct device access to userspace, in a secure, IOMMU
  protected environment", intended to allow "safe, non-privileged, userspace drivers". It replaces UIO for such
  uses: "UIO ... has no notion of IOMMU protection, limited interrupt support, and requires root privileges to access
  things like PCI configuration space". Ownership unit is the IOMMU group; the container node is `/dev/vfio/vfio`.
- SS: a no-IOMMU mode exists for "unsafe DMA" without protection, enabled with
  `/sys/module/vfio/parameters/enable_unsafe_noiommu_mode`.
- INF: VFIO targets PCI devices behind an IOMMU. Typical small embedded SoCs with memory-mapped peripherals use UIO,
  the existing subsystems, or `/dev/gpiochip`, `i2c-dev`, `spidev`, not VFIO.
- Gap: I did not read the VFIO device-cdev and iommufd sections.

### `/dev/mem` (`bootlin-linux-kernel` slides p.299, chapter "I/O memory"; kernel Kconfig)

- SS (Bootlin): `/dev/mem` gives access to physical addresses. "For security reasons, on x86, arm, arm64, riscv,
  powerpc, parisc, s390: `CONFIG_STRICT_DEVMEM` restricts /dev/mem to non-RAM addresses (from v5.12).
  `CONFIG_IO_STRICT_DEVMEM` goes beyond and only allows to access idle I/O ranges (not appearing in /proc/iomem)."
  The slide names `devmem2`; BusyBox ships a `devmem` applet (listed in `bootlin-embedded-linux` slides, chapter
  "BusyBox").
- SS (`lib/Kconfig.debug`, master): `STRICT_DEVMEM` "Filter access to /dev/mem"; default y only for
  `PPC || X86 || ARM64 || S390`. If disabled, "you allow userspace (root) access to all of memory, including kernel and
  userspace memory". If enabled with `IO_STRICT_DEVMEM=n`, "/dev/mem file only allows userspace access to PCI space and
  the BIOS code and data regions". CONFLICT: Bootlin lists arm and riscv among the architectures; the Kconfig default
  list I read does not include 32-bit ARM or RISC-V (they may select it elsewhere). Not resolved.
- SS (`capabilities(7)`, man-pages 6.19): `CAP_SYS_RAWIO` covers opening `/dev/mem` and `/dev/kmem`, `iopl`, `ioperm`
  and mapping `/proc/bus/pci` files. systemd `PrivateDevices=` removes `/dev/mem`, `/dev/port`, `CAP_SYS_RAWIO` and
  `CAP_MKNOD`, and blocks the `@raw-io` syscalls.
- SS (systemd `50-udev-default.rules.in`, main): `/dev/mem`, `kmem`, `port` get `GROUP="kmem", MODE="0640"`.
- INF, why `/dev/mem` is the wrong tool: it bypasses the kernel driver model (no arbitration with a driver that owns
  the same registers, no interrupt delivery, no clock, power or pinmux handling), needs root or `CAP_SYS_RAWIO`,
  and `STRICT_DEVMEM` blocks RAM ranges and, with `IO_STRICT_DEVMEM`, ranges a driver has claimed. Register-level poking
  is acceptable for bring-up and debugging only. The reasons are inferred from the cited facts; no single source gives
  this list.

## Q4 Serial ports

- SS (`termios(3)`, man-pages 6.19): `cfmakeraw()` sets
  `c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL | IXON)`, `c_oflag &= ~OPOST`,
  `c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN)`, `c_cflag &= ~(CSIZE | PARENB)` and `c_cflag |= CS8`. It does
  not set `CREAD` or `CLOCAL`, and it does not set `VMIN` and `VTIME` (INF, from the list: neither appears).
- SS: non-canonical read cases. `MIN == 0, TIME == 0`: polling read, returns 0 if no data. `MIN > 0, TIME == 0`:
  blocks until MIN bytes. `MIN == 0, TIME > 0`: returns when at least one byte arrives or the TIME timer (tenths of a
  second, started at `read()`) expires, then 0. `MIN > 0, TIME > 0`: inter-byte timer, restarted after each byte and
  started only after the first byte, so at least one byte is read.
- SS (`TIOCEXCL(2const)`): `TIOCEXCL` puts the terminal in exclusive mode; further `open()` fails with `EBUSY` "except for
  a process with the CAP_SYS_ADMIN capability". `TIOCGEXCL` (Linux 3.8) reads the state; `TIOCNXCL` clears it.
  INF: exclusive mode stops other normal openers but not root, and it does not stop a process that opened the port
  before the call; it is not a substitute for a lock file or `flock` between cooperating programs.
- SS (`kernel-docs v7.3 driver-api/serial/serial-rs485`): RS-485 is configured with `TIOCSRS485` and read back with
  `TIOCGRS485` using `struct serial_rs485` (`flags`, `delay_rts_before_send`, `delay_rts_after_send`, addressing
  fields). Flags include `SER_RS485_ENABLED`, `SER_RS485_RTS_ON_SEND`, `SER_RS485_RTS_AFTER_SEND`,
  `SER_RS485_RX_DURING_TX`, `SER_RS485_TERMINATE_BUS`, `SER_RS485_ADDRB`, `SER_RS485_MODE_RS422`. "The set function
  returns the new state, with any unsupported bits reverted appropriately." The serial core sanitises the structure
  against the driver's `rs485_supported`. Delays are in milliseconds. Device tree can give boot-time RS-485 defaults
  (`rs485.yaml`). The doc's own example leaves `rs485conf` uninitialised before `|=`. INF: zero the struct (or
  `TIOCGRS485` first) and re-read after the set.
- SS (systemd `60-serial.rules`, main): USB serial ports (`ttyUSB*`, `ttyACM*`) get stable links
  `/dev/serial/by-id/<ID_BUS>-<ID_SERIAL>-if<interface>` (with `-port<N>` for multiport) and `/dev/serial/by-path/...`.
  The by-id rule needs `ID_BUS`, `ID_SERIAL` and `ID_USB_INTERFACE_NUM`, so it does not apply to platform UARTs such
  as `ttyS*` or `ttymxc*`. INF: two identical USB adapters with no serial number may collide on by-id.
- SS (systemd `50-udev-default.rules.in`): `tty[A-Z]*[0-9]`, `ttymxc[0-9]*` and others get `GROUP="dialout"`; the
  `dialout` group exists in `sysusers.d/basic.conf.in`.
- Library crates and packages: Rust `serialport` 4.10.1 (2026-09-08, MPL-2.0). Python `pyserial` 3.5 (2020-11-23, BSD),
  no release since; `python-periphery` has a serial class. BG: pyserial exposes `rs485_mode` and `exclusive=True`.
- Gap: the kernel `tty` docs for line disciplines, `CLOCAL`/`HUPCL` and `serdev` (kernel-side serial device
  binding) were not read.

## Q5 Other interfaces

### Input (evdev)

- SS (`Documentation/input/input.rst`, v7.3): `evdev` "is the preferred interface for userspace to consume user input,
  and all clients are encouraged to use it". Nodes are `/dev/input/eventN` (static minors 64 to 95, then 256 up). You
  can use blocking, non-blocking and `select()`, and "you'll always get a whole number of input events on a read".
  `struct input_event` has `time`, `type`, `code`, `value`; `EV_KEY` value 0, 1, 2 mean release, press, autorepeat;
  codes are in `include/uapi/linux/input-event-codes.h`. `mousedev` is "a hack to make legacy programs ... work".
- SS (systemd rules): `/dev/input/*` gets `GROUP="input"`, joystick `js*` mode 0664.
- Library: Rust `evdev` 0.13.2 (2025-09-15, Apache-2.0 OR MIT); Python `evdev` 2.0.0 (2026-08-23, BSD-3-Clause).
  BG: C code usually uses `libevdev`; not checked.
- SS (Bootlin lab): `cat /dev/input/event0 | od -x` shows raw events from an I2C joystick driven by a kernel driver.
  (`bootlin-embedded-linux` bbb-labs chapter 08)
- BG, not verified: `EVIOCGRAB` for exclusive grab; `uinput` to create virtual devices (a `uinput.rst` exists in
  `Documentation/input/` at v7.3).

### LED and backlight (sysfs class attributes)

- SS (`Documentation/leds/leds-class.rst`, `Documentation/ABI/testing/sysfs-class-led`, v7.3): LEDs appear in
  `/sys/class/leds/`; `brightness` takes 0 to `max_brightness` (default 255; 1 for on/off-only LEDs); "Writing 0 to
  this file clears active trigger"; `trigger` selects a kernel-side source (the `timer` trigger takes `delay_on` and
  `delay_off` in milliseconds). Names follow `devicename:color:function`. `brightness_hw_changed` supports `poll()`.
- SS (`Documentation/ABI/stable/sysfs-class-backlight`, v7.3): `/sys/class/backlight/<name>/` has `brightness`
  (0 to `max_brightness`, driver-stored value), `actual_brightness` (queried from hardware; "Userspace should
  generally use the values in 'brightness' to make decisions"), `max_brightness`, `bl_power` (0 power on, 4 power
  off), and `type` (`firmware`, `platform`, `raw`; prefer firmware over platform over raw when several exist). A
  `scale` attribute (kernel 5.4) says whether the curve is linear.
- SS (`drivers-on-gpio`): a GPIO-wired LED should use `leds-gpio`, which gives the LED sysfs interface, not a
  userspace GPIO loop.
- INF: sysfs attribute files are normally writable only by root. Giving a service access needs a udev rule that sets
  `ATTR{}` ownership or a service that runs with the matching group; not verified against udev docs.

### hwmon and IIO

- SS (`Documentation/hwmon/sysfs-interface.rst`, v7.3): find chips by following `/sys/class/hwmon/hwmon*`. File names
  are `<type><number>_<item>` (`in`, `temp`, `fan`, with `_input`, `_max`, `_min`, `_label`). One value per file,
  fixed point. "All standard ABI attributes shall be world readable. Writeable standard ABI attributes shall be
  writeable only for privileged users." Alarms are raw chip indications. The doc says bypassing `libsensors` is "not
  recommended" because conversion, labelling and hiding of inputs then fall to the application.
  Units (millidegree Celsius for `temp`, millivolt for `in`) were not found as a plain sentence in that file; the doc
  text only mentions them in passing. BG: `temp*_input` is millidegrees Celsius, `in*_input` millivolts, `fan*_input`
  RPM, per `Documentation/ABI/testing/sysfs-class-hwmon`, which I did not read in the right section.
- SS (`Documentation/iio/iio_devbuf.rst`, v7.3): buffered capture reads from `/dev/iio:deviceX`. Buffer attributes under
  `/sys/bus/iio/devices/iio:deviceX/bufferY/`: `length`, `enable` ("should be written last, after length and selection
  of scan elements"), `watermark`, `data_available`, and per-channel `_en`, `_index`, `_type`. `_type` has the form
  `[be|le]:[f|s|u]bits/storagebits[Xrepeat][>>shift]`, for example `le:s12/16>>4`. Samples are "naturally aligned" with
  padding; buffered data is normally raw (no scale or offset applied). A non-blocking read after `poll()` timeout lets
  an application get a maximum delay guarantee with a watermark.
- SS (`Documentation/iio/iio_tools.rst`): kernel example tools `lsiio`, `iio_event_monitor`, `iio_generic_buffer`,
  `iio_utils`; and `libiio` (analogdevicesinc/libiio) as a generic C/C++ library.
- SS (Bootlin): "LED, PWM, IIO ... some devices only have a sysfs interface". (`bootlin-embedded-linux` slides p.280)
- SS (`kernel-docs v7.3 userspace GPIO doc`): "Applications that have a good reason to use the industrial I/O (IIO)
  subsystem from userspace will likely be a good fit for using GPIO lines from userspace as well."
- Gap: I did not read `Documentation/ABI/testing/sysfs-bus-iio`, so the raw, scale and offset formula
  `(raw + offset) * scale` is BG.

### Watchdog (`Documentation/watchdog/watchdog-api.rst`, v7.3; systemd man pages)

- SS: opening `/dev/watchdog` starts the watchdog; writing any data pings it; the device must be pinged within the
  timeout. Closing it disables the watchdog "unless the 'Magic Close' feature is supported". With magic close, the driver
  stops the watchdog only if the character `V` was written just before close; otherwise it assumes userspace died and
  lets the reset happen. `CONFIG_WATCHDOG_NOWAYOUT` (and the `nowayout` module parameter) make the watchdog impossible to
  disable once started.
- SS: ioctls: `WDIOC_KEEPALIVE` (same as a write), `WDIOC_SETTIMEOUT` (driver returns the actual timeout; may differ),
  `WDIOC_GETTIMEOUT`, `WDIOC_SETPRETIMEOUT`, `WDIOC_GETPRETIMEOUT`, `WDIOC_GETTIMELEFT`, `WDIOC_GETSUPPORT` (struct
  `watchdog_info`, options such as `WDIOF_SETTIMEOUT`, `WDIOF_MAGICCLOSE` is not in the part I read), `WDIOC_GETSTATUS`,
  `WDIOC_GETBOOTSTATUS`. The doc's header says "Last reviewed: 10/05/2007 ... describes the state of the Linux 2.4.18
  kernel", so it is old, though still the file the kernel points to.
- SS (systemd): `RuntimeWatchdogSec=` in `systemd-system.conf` makes the system manager open and ping the hardware
  watchdog (`/dev/watchdog0`, or `WatchdogDevice=`), "at least once in half the specified timeout interval"; `off` or `0`
  means no device is opened. `RebootWatchdogSec=` covers the reboot phase. For a service: `WatchdogSec=` plus the service
  calling `sd_notify(0, "WATCHDOG=1")`; the manager passes `WATCHDOG_USEC` and `sd_watchdog_enabled()` reads it;
  notify "every half of the time"; on expiry the service gets `SIGABRT` and `Restart=` can restart it.
  `NotifyAccess=` defaults to `main` once `WatchdogSec=` is set.
- INF: one process must own `/dev/watchdog`. If systemd already holds it via `RuntimeWatchdogSec=`, an application
  watchdog should use `WatchdogSec=` and `sd_notify` instead of opening the device. BG: a second `open` of the same
  watchdog device returns `EBUSY`; I read no source for that.

### uevents and udev monitoring

- SS (systemd `libudev(3)`): "This library is supported, but should not be used in new projects. Please see sd-device(3)
  for an equivalent replacement with a more modern API." sd-device is part of `libsystemd` (pkg-config `libsystemd`).
  The public header `src/systemd/sd-device.h` on `main` declares `sd_device_monitor_new`, `_start`, `_get_fd`, `_receive`
  and filter functions (`sd_device_monitor_filter_add_match_subsystem_devtype`, `..._match_tag`). I found no man page
  for `sd_device_monitor_*` in the `latest` docs (the page fetch returned empty). So the monitor API is declared in the
  header but I could not read prose docs for it.
- SS (libudev): `udev_monitor_new_from_netlink()` was added in version 221; pyudev 0.24.5 (2026-09-28, LGPL-2.1-or-later)
  wraps libudev. Rust `udev` 0.9.3 (2025-01-23, MIT) binds libudev.
- SS (libgpiod NEWS v2.3): GPIO chip hotplug in the daemon uses "add"/"remove" uevents.
- INF: a program that waits for a device to appear (for example a USB serial adapter) should monitor uevents and filter
  by subsystem, not poll `/dev`.

### Device tree

- SS (`drivers/of/base.c`, master): `proc_symlink("device-tree", NULL, "/sys/firmware/devicetree/base")`, commented
  "Symlink in /proc as required by userspace ABI". Bootlin labs use `/sys/firmware/devicetree/base/model` to identify the
  board and explore nodes as directories and properties as files. They also run `dtc -I fs /sys/firmware/devicetree/base/`.
  (`bootlin-embedded-linux` bbb-labs chapter 08; `bootlin-linux-kernel` bbb-labs chapter "Describing hardware devices")
- BG: property files hold raw big-endian cells and NUL-terminated strings, so userspace must byte-swap integers.
  Not verified in a source.
- SS: `dtc -I fs` input format is "/proc/device-tree style directory" (`scripts/dtc/dtc.c`, master).

## Q6 Permissions and naming

- SS (systemd `rules.d/50-udev-default.rules.in`, main, 130 lines, searched in full): default group rules exist for
  `tty` and `dialout` (serial), `input`, `video`, `render`, `audio`, `disk`, `kvm`, `clock` (rtc), `kmem` (`/dev/mem`).
  I found no default rule for `gpio`, `i2c`, `spi`, `watchdog`, `uio` or `iio`. INF: for those, the project must ship its
  own udev rule and group.
- SS (`sysusers.d/basic.conf.in`): the groups systemd creates for hardware access are
  `audio, cdrom, clock, dialout, disk, input, kmem, kvm, lp, render, sgx, tape, tty, video`. INF: `gpio`, `i2c` and
  `spi` are not among them, so a project creates its own groups.
- SS (`udev.rules`): `OWNER`, `GROUP`, `MODE` set node permissions and override the compiled-in defaults; `ATTR{key}` writes
  a sysfs attribute; `SYMLINK+=` creates stable names; `TAG` attaches a tag used by monitor filters. `60-serial.rules` is
  the model for stable names (by-id and by-path).
- BG pattern for a rule file (not verified in a doc): `SUBSYSTEM=="gpio", KERNEL=="gpiochip*", GROUP="gpio", MODE="0660"`
  and the same for `i2c-dev` (`SUBSYSTEM=="i2c-dev"`), `spidev` (`SUBSYSTEM=="spidev"`), `watchdog`, and `uio`.
- SS (`systemd.exec`): `SupplementaryGroups=` "does not override, but extends the list of supplementary groups
  configured in the system group database for the user". `AmbientCapabilities=` "are useful if you want to execute a
  process as a non-privileged user but still want to give it some capabilities". `PrivateDevices=` removes physical
  devices, `/dev/mem` and `/dev/port`.
- SS (`systemd.resource-control`): `DeviceAllow=` takes a node path under `/dev/` or `char-<group>` and `block-<group>`
  where the group name comes from `/proc/devices` (globs allowed in the group names, not in paths), with `r`, `w`, `m`.
  It is implemented with eBPF filtering and cannot be bypassed with a `+` prefix. `DevicePolicy=auto|closed|strict`:
  with `auto`, "allows access to all devices if no explicit DeviceAllow= is present". INF: setting `DeviceAllow=`
  entries with `DevicePolicy=closed` or `strict` makes the unit a device allow-list; the chosen paths should still be
  reachable by Unix permissions, since the two checks are independent.
- SS (`capabilities(7)`): `CAP_DAC_OVERRIDE` bypasses file permission checks; `CAP_SYS_RAWIO` covers `/dev/mem`, `iopl`,
  `ioperm`. Ambient capabilities (Linux 4.3) survive `execve` of an unprivileged program.
- INF: GPIO chardev, i2c-dev, spidev, evdev, watchdog, serial and UIO need only file access, so none of them needs a
  capability if the node's group and mode allow the service user. Raw I/O (`/dev/mem`, ioperm) is the case that needs
  `CAP_SYS_RAWIO`. Therefore a capability list for these interfaces should be empty.
- INF: stable names matter because `gpiochipN`, `i2c-N`, `spidevB.C` and `ttyUSBN` numbers depend on probe order. Sources
  that show instability: i2c "can even change from one boot to the next" (SS); GPIO sysfs numbers "are not always stable"
  (SS). The libgpiod tools can address lines by name, and the kernel exposes chip `label` and line `name` for matching.
- Gap: `/proc/devices` names for `DeviceAllow=char-...` (for example `gpiochip`, `spi`, `i2c`, `uio`) are BG; I saw only
  `register_chrdev(SPIDEV_MAJOR, "spi", ...)` (SS, `drivers/spi/spidev.c`) and the `GPIOCHIP_NAME` constant. Verify with
  `cat /proc/devices` on the target, or use path form `/dev/gpiochip0 rw`.

## Q7 Kernel driver versus userspace driver

| Criterion                                                                           | Kernel driver                                                             | Userspace driver                                                                                                | Source                                     |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Standard interface for apps                                                         | yes, same for the whole class                                             | no, application-specific                                                                                        | `bootlin-embedded-linux` slides p.260 (SS) |
| Other kernel consumers (reset, interrupt, regulator, graphics stack, network stack) | usable                                                                    | not usable                                                                                                      | slides pp.263-264 (SS)                     |
| Interrupt latency                                                                   | in-kernel handler                                                         | "Less straightforward to handle interrupts: increased latency"                                                  | `bootlin-linux-kernel` slides p.47 (SS)    |
| Sharing                                                                             | kernel multiplexes access                                                 | only one application, "no need for the kernel to act as a multiplexer"                                          | `bootlin-linux-kernel` slides p.46 (SS)    |
| Crash isolation                                                                     | a bug can crash the kernel                                                | "Cannot crash the kernel", can be killed and debugged                                                           | slide p.47 (SS)                            |
| Language                                                                            | C and Rust in kernel                                                      | any language, floating point                                                                                    | slide p.47 (SS)                            |
| Licence                                                                             | GPL                                                                       | "Drivers can be kept proprietary"                                                                               | slide p.47 (SS)                            |
| Performance                                                                         | syscalls                                                                  | "Potentially higher performance, especially for memory-mapped devices, thanks to the avoidance of system calls" | slide p.47 (SS)                            |
| Hardware abstraction, helpers                                                       | available                                                                 | none                                                                                                            | slide p.47 (SS)                            |
| Portability across hardware                                                         | apps unchanged                                                            | "Need to adapt applications when changing the hardware"                                                         | slide p.47 (SS)                            |
| Power management                                                                    | runtime PM, suspend                                                       | not covered by any source I read                                                                                | INF only                                   |
| Maintenance                                                                         | mainline gives "cost-free bug and security fixes" and follows API changes | owner maintains it                                                                                              | `bootlin-linux-kernel` slide p.45 (SS)     |

- SS (kernel GPIO doc): for mass-produced systems "using appropriate kernel drivers is paramount"; the userspace ABI is
  for one-off systems and "specialized equipment that is not produced by the numbers". (`using-gpio`)
- SS (Bootlin): out-of-tree vendor drivers: "Quality is often dubious" and "Avoid them when possible!"; and "grep in the
  Linux kernel tree is your best friend" before writing anything. (`bootlin-embedded-linux` slides pp.265-266)
- Power-management and concurrency costs are INF: userspace drivers cannot own clocks, regulators or runtime PM, because
  those are kernel-only APIs (BG). Mark them as inference in the skill.

## Proposed defaults

| Interface         | Recommended API and library                                                                                                                                                                                                                                                                                                                                    | Permission setup                                                                                                                                                                                                                                                           | Use a kernel driver instead when                                                                                                                                                                                                            |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GPIO              | `/dev/gpiochipN` uAPI v2 through libgpiod v2 (C), its C++ and Python bindings (`pip install gpiod>=2.0.2`, not 1.5.4), Rust `gpiocdev`. Request by line name or offset with a consumer label; hold the request fd for as long as the state must hold; use edge events with `poll()`, kernel debounce, and check `seqno` for loss. Never use `/sys/class/gpio`. | udev rule that gives the node to a project group (`gpio`) with mode 0660; systemd `SupplementaryGroups=` and `DeviceAllow=/dev/gpiochipN rw`; no capabilities.                                                                                                             | the line is an LED, key, reset, interrupt, chip-select, regulator or power switch for another device; the system is mass-produced; other kernel drivers need the line. Use `leds-gpio`, `gpio-keys`, DT hogs.                               |
| I2C               | `/dev/i2c-N` with `I2C_RDWR` for combined transfers, or the `libi2c` SMBus helpers; Rust `i2cdev`; Python `smbus2`. Resolve the bus from `/sys/class/i2c-dev` or a stable udev link, not a fixed number. Do not use `I2C_SLAVE_FORCE`.                                                                                                                         | project group (`i2c`), mode 0660; same systemd pattern; no capabilities.                                                                                                                                                                                                   | a mainline driver exists (`git grep` the part number), the chip has an interrupt, other drivers share the bus, or the chip exposes a subsystem class (hwmon, IIO, RTC, input). Run `i2cdetect` only with care ("can confuse your I2C bus"). |
| SPI               | `/dev/spidevB.C` with `SPI_IOC_MESSAGE(N)` (zero the transfer structs), set mode, bits and `max_speed_hz` explicitly; Rust `spidev`; Python `spidev`. Never write `compatible = "spidev"` in a device tree. For a test bench use `driver_override` or `new_device`; for a product add the real device name to the spidev tables upstream or write a driver.    | project group (`spi`), mode 0660.                                                                                                                                                                                                                                          | a real device exists in the tree, the device needs an interrupt, CS polarity control or sharing the bus, or the product ships.                                                                                                              |
| UIO               | `/dev/uioX`: `mmap` registers, blocking `read()` of 4 bytes for the interrupt count, `write()` 1 to re-enable. Needs a kernel part (`uio_pdrv_genirq` for platform devices, `uio_pci_generic` for PCI). Check `name`, `version` and map sizes under `/sys/class/uio` first.                                                                                    | project group (`uio`), mode 0660.                                                                                                                                                                                                                                          | the device needs DMA protection (use VFIO behind an IOMMU), needs per-interrupt work in the kernel, fits a subsystem (network, serial, USB, IIO), or the userspace process may die while the hardware needs service.                        |
| `/dev/mem`        | Not recommended. Bring-up and debug only, with `devmem`. Keep `CONFIG_STRICT_DEVMEM=y`.                                                                                                                                                                                                                                                                        | root or `CAP_SYS_RAWIO`; `kmem` group 0640 by default; use `PrivateDevices=yes` to hide it.                                                                                                                                                                                | always, for anything that ships.                                                                                                                                                                                                            |
| Serial            | termios: `cfmakeraw()` then set speed, \`CREAD                                                                                                                                                                                                                                                                                                                 | CLOCAL`, and `VMIN`/`VTIME`by the four documented cases;`TIOCEXCL`for exclusive open; RS-485 with`TIOCGRS485`then`TIOCSRS485`, re-read to see which bits were reverted. Use `/dev/serial/by-id`for USB adapters; Rust`serialport`, Python `pyserial`or`python-periphery\`. | group `dialout` (systemd default for `ttyS*`, `ttyUSB*`, `ttyACM*`); no capabilities.                                                                                                                                                       |
| Input             | evdev `/dev/input/eventN` (libevdev in C, `evdev` crate, `python-evdev`); do not use `mousedev`.                                                                                                                                                                                                                                                               | group `input` (systemd default).                                                                                                                                                                                                                                           | the device is a GPIO key or button: use `gpio-keys` and read evdev.                                                                                                                                                                         |
| LED and backlight | sysfs `/sys/class/leds/*/brightness`, `trigger`, `/sys/class/backlight/*/brightness`; write `brightness`, not `actual_brightness`.                                                                                                                                                                                                                             | the files are root-writable by default; give a udev `ATTR` rule or a small root helper.                                                                                                                                                                                    | the LED hangs off a GPIO: declare it for `leds-gpio` in the device tree.                                                                                                                                                                    |
| hwmon and IIO     | hwmon: read `/sys/class/hwmon/hwmon*/` attributes (or `libsensors`). IIO: sysfs `in_*_raw`, `_scale`, `_offset` for single reads; for streaming, buffer with `length`, `_en`, `watermark`, `enable` last, then read `/dev/iio:deviceX` or use `libiio`.                                                                                                        | read-only for all by ABI rule for hwmon; IIO nodes via group rule.                                                                                                                                                                                                         | a plain GPIO or I2C chip has an IIO or hwmon driver: use it instead of raw bus access.                                                                                                                                                      |
| Watchdog          | If systemd is init: `RuntimeWatchdogSec=` for the board, `WatchdogSec=` plus `sd_notify("WATCHDOG=1")` for each critical service. Direct `/dev/watchdog` use: open, `WDIOC_SETTIMEOUT`, ping at half the timeout, write `V` before an intentional close; do not combine with systemd owning the device.                                                        | watchdog group only for the one process that opens it.                                                                                                                                                                                                                     | The hardware watchdog needs a driver anyway; nothing to write in userspace.                                                                                                                                                                 |
| uevents           | `sd-device` monitor (`libsystemd`); `libudev` is "supported but should not be used in new projects"; Python `pyudev`. Filter by subsystem.                                                                                                                                                                                                                     | none (netlink read).                                                                                                                                                                                                                                                       | not applicable                                                                                                                                                                                                                              |
| Device tree       | read `/proc/device-tree` or `/sys/firmware/devicetree/base`; mind big-endian cells.                                                                                                                                                                                                                                                                            | world-readable by default (BG).                                                                                                                                                                                                                                            | not applicable                                                                                                                                                                                                                              |

Rules the skill should state:

1. Search the kernel tree for an existing driver first; userspace access is for one-off or prototype work.
2. One owner per device; if a kernel driver is bound, do not force access.
3. Use stable names (udev links, line names) instead of numbered nodes.
4. Run as a normal user in a hardware group; use `DeviceAllow=` and `PrivateDevices=` to narrow access; no capability for
   these interfaces; `CAP_SYS_RAWIO` only for raw I/O.
5. Check `errno` on every ioctl; zero every uAPI struct; treat debounce, bias and drive as requested, not confirmed.

## What I could not verify

- Kernel docs for GPIO uAPI, i2c-dev, spidev and watchdog were read from the `v7.3` tag sources, not the rendered set.
  I could not fetch `lib/Kconfig.debug` at `v7.3`, so the `STRICT_DEVMEM` help text is from `master`.
- libgpiod's upstream site (git.kernel.org) is behind an Anubis wall; I used the readthedocs site and the GitHub mirror.
  I did not read the libgpiod C++ API pages, the GLib bindings, or the D-Bus API in detail.
- `sd_device_monitor_*` has no readable man page; I only confirmed the header declarations on `main`.
- Kconfig default for `STRICT_DEVMEM` on 32-bit ARM and RISC-V conflicts between Bootlin's slide and the Kconfig default
  list.
- When the SPI `new_device` sysfs interface first appeared (it is in the v7.3 docs).
- Chardev introduction version for GPIO (4.4 per gpio-cdev, 4.8 per libgpiod).
- Units in hwmon (`temp*_input` in millidegrees, and so on): BG, since the `sysfs-class-hwmon` section was not read.
- IIO `(raw + offset) * scale` formula: BG; `sysfs-bus-iio` was not read.
- `/proc/devices` names for `DeviceAllow=char-...`; the watchdog single-opener rule; `EVIOCGRAB`, `uinput`, and libevdev
  facts; pyserial `rs485_mode`/`exclusive`; `EBUSY` from `I2C_SLAVE` with a bound driver; udev rule examples for group and
  mode: all BG.
- Power-management cost of userspace drivers: no source read states it; INF.
- Rust `gpio-cdev` v1-only is inferred from `src/ffi.rs` on `master`, and `gpiocdev` v1+v2 from its `uapi` crate file names.
