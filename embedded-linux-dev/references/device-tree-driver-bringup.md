# Device Tree and Driver Bring-Up

For compiling, decompiling, diffing, and validating device tree blobs and
overlays, see `device-tree-tooling.md`. This file covers node structure, resource
ownership, the driver probe path, and per-bus debugging.

## Contents

- [Device Tree Source Structure](#device-tree-source-structure)
- [Ownership Questions for Every Device Node](#ownership-questions-for-every-device-node)
- [Calibration and Per-Unit Trim](#calibration-and-per-unit-trim)
- [Kernel Clock and Reset APIs](#kernel-clock-and-reset-apis)
- [Driver Registration Macros](#driver-registration-macros)
- [Debugging a Missing `/dev` Node](#debugging-a-missing-dev-node)
- [Common DTS/Driver Failure Patterns](#common-dtsdriver-failure-patterns)
- [Bus-Specific Debugging](#bus-specific-debugging)
- [Kernel Config Requirements](#kernel-config-requirements)

## Device Tree Source Structure

A device node has these required and common optional elements. Regulator supplies
use the `<name>-supply = <&regulator>;` form — there is no `enable-regulators`
property; a phandle to a regulator is named after the rail the device consumes.

```dts
/* DTS node anatomy */
&i2c1 {
    status = "okay";
    clock-frequency = <400000>;

    my_sensor: sensor@3c {              /* unit-address matches first reg value */
        compatible = "vendor,model";    /* must match driver of_match_table EXACTLY */
        reg = <0x3c>;                   /* I2C address */

        /* Resources */
        clocks = <&ccu CLK_SENSOR>;     /* clock phandle + specifier */
        clock-names = "mclk";           /* must match driver's clk_get("mclk") */
        reset-gpios = <&gpio2 5 GPIO_ACTIVE_LOW>;

        /* Regulator supplies: one "<rail>-supply" per rail the device draws.
         * The property name is what the driver passes to devm_regulator_get();
         * a camera sensor typically wants analog, interface, and core rails. */
        avdd-supply = <&reg_2v8>;       /* analog */
        dovdd-supply = <&reg_1v8>;      /* digital I/O / interface */
        dvdd-supply = <&reg_1v2>;       /* digital core */

        pinctrl-names = "default";
        pinctrl-0 = <&sensor_pins>;

        interrupt-parent = <&gpio3>;
        interrupts = <14 IRQ_TYPE_EDGE_FALLING>;

        port {
            sensor_ep: endpoint {       /* V4L2 / media graph endpoint */
                remote-endpoint = <&csi_ep>;
            };
        };
    };
};
```

## Ownership Questions for Every Device Node

Before diagnosing a probe failure, map ownership:

- Who provides the clock? (check `clocks =` and that the clock provider is `status = "okay"`)
- Who supplies each power rail? (check the `<rail>-supply` phandles — e.g. `avdd-supply`, `dovdd-supply`, `dvdd-supply` — and that each referenced regulator is enabled)
- Who controls reset? (`reset-gpios` — check polarity: `GPIO_ACTIVE_LOW` vs `GPIO_ACTIVE_HIGH`)
- Who controls power-down? (`powerdown-gpios`)
- Who owns the interrupt? (interrupt controller enabled and parent correct?)
- Who allocates DMA channels? (`dmas =`, `dma-names =`)

A missing or wrong value in any of these is invisible to Linux — the driver simply
fails to probe with no error message about the missing resource.

## Calibration and Per-Unit Trim

Silicon is not the datasheet. A crystal drifts with temperature and age, an IMU
carries a fixed bias, a PWM controller's internal oscillator runs a few percent
off nominal, and an ADC is only as accurate as its reference rail. Hardcoding the
nominal constant produces a device that is quietly wrong in the field and
correctable only by a rebuild.

MUST leave a tunable seam for any constant that describes the physical world
rather than the register map. Choose the seam by what the value varies with:

| Value varies with | Where it belongs |
|---|---|
| PCB revision (same for every unit built) | DTS property defined by the device's binding — `clock-frequency`, `spi-max-frequency`, a vendor trim property |
| the individual unit (factory-measured) | an NVMEM/eFuse cell referenced by `nvmem-cells`; a per-unit value in a shared DTS is wrong for every other unit |
| the sensor reading itself | IIO `in_*_offset` / `in_*_scale`; consumers apply the driver's offset and scale instead of their own constants |
| host clock error over time | RTC offset (`/sys/class/rtc/rtc0/offset`) or NTP/`adjtimex`, never a fudge in application code |
| actuator range and centre | DTS or a userspace config file — servo min/max/centre pulse widths differ per horn and per linkage |

Per-unit calibration read from an eFuse, from the upstream i.MX thermal binding:

```dts
efuse@21bc000 {
    compatible = "fsl,imx6sx-ocotp", "syscon";
    reg = <0x021bc000 0x4000>;

    tempmon_calib: calib@38 {
        reg = <0x38 4>;
    };
};

tempmon {
    compatible = "fsl,imx6sx-tempmon";
    nvmem-cells = <&tempmon_calib>, <&tempmon_temp_grade>;
    nvmem-cell-names = "calib", "temp_grade";
};
```

Property and cell names come from the device's own binding — confirm them in
`Documentation/devicetree/bindings/` for the kernel release in use, never by
analogy with another device.

```bash
# What calibration does the driver already expose?
cat /sys/bus/iio/devices/iio:device0/in_accel_x_offset
cat /sys/bus/iio/devices/iio:device0/in_accel_scale

# Did the driver actually read its calibration cell?
dmesg | grep -iE "calib|nvmem|efuse" | tail -20
```

MUST record every applied calibration where it is observable — the value, its
source, and when it was measured. A silently applied correction is
indistinguishable from a bug: the next engineer sees output matching neither the
raw reading nor the datasheet, with no way to tell a calibration from a fault.

MUST NOT add a compensation factor for a suspected hardware error before proving
that error at the boundary that owns it. A software fudge hides a real DTS,
regulator, or clock fault and outlives the fix.

## Kernel Clock and Reset APIs

These are the kernel APIs for acquiring hardware resources in a driver. Prefer the
`devm_` variants so resources are released automatically on probe failure or driver
removal.

### Clock API

```c
/* Acquire a clock handle (does not enable the clock) */
struct clk *clk = devm_clk_get(&pdev->dev, "mclk");  /* name from DTS clock-names */
if (IS_ERR(clk))
    return PTR_ERR(clk);

/* Prepare and enable the clock (both must be called before using the clock) */
ret = clk_prepare_enable(clk);
if (ret)
    return ret;

/* Disable and unprepare when done (e.g. in driver remove or error path) */
clk_disable_unprepare(clk);

/* Query the actual running rate */
unsigned long rate = clk_get_rate(clk);

/* Request a specific rate */
clk_set_rate(clk, 24000000);  /* 24 MHz */
```

`clk_prepare_enable()` and `clk_disable_unprepare()` are paired calls. Calling
`clk_enable()` alone without `clk_prepare()` is wrong for clocks that may sleep
during enabling, which is common on modern SoCs.

### Reset Controller API

```c
/* Acquire reset control handle — prefer the explicit exclusive variant */
struct reset_control *rst = devm_reset_control_get_exclusive(&pdev->dev, NULL);
if (IS_ERR(rst))
    return PTR_ERR(rst);

/* Assert (hold in reset) */
reset_control_assert(rst);

/* Deassert (release from reset) */
reset_control_deassert(rst);
```

`devm_reset_control_get_exclusive()` is the preferred form for a driver that is the
sole consumer of a reset line. Use `devm_reset_control_get_shared()` when multiple
drivers share control. The generic `devm_reset_control_get()` still compiles but is
soft-deprecated and will be flagged on upstream submission.

## Driver Registration Macros

Use the module helper macros instead of hand-writing `module_init`/`module_exit`
when the driver does nothing special at init and exit:

```c
/* Platform driver — replaces the module_init()/module_exit() pair */
module_platform_driver(my_platform_driver);

/* I2C driver — replaces the module_init()/module_exit() pair */
module_i2c_driver(my_i2c_driver);
```

For I2C drivers, declare and register the device ID table so the kernel can match:

```c
static const struct i2c_device_id my_sensor_id[] = {
    { "mysensor", 0 },   /* plain model name — no vendor prefix (that belongs in of_device_id) */
    { }
};
MODULE_DEVICE_TABLE(i2c, my_sensor_id);

static const struct of_device_id my_sensor_of_match[] = {
    { .compatible = "vendor,mysensor" },   /* must match DTS compatible exactly */
    { }
};
MODULE_DEVICE_TABLE(of, my_sensor_of_match);
```

A platform or I2C driver follows this sequence:

```
1. Kernel matches compatible string → calls probe()
2. probe() calls:
   a. devm_clk_get()        — get clock handle
   b. devm_regulator_get()  — get power supply (one per <rail>-supply)
   c. devm_gpiod_get()      — get GPIO descriptors
   d. devm_request_irq()    — register interrupt handler
   e. device-specific init  — write registers, self-test
   f. register with subsystem (v4l2_device_register, i2c_add_driver, etc.)
3. On success: device appears in /sys, /dev node created (if char device)
4. On failure: probe() returns negative errno
   - returns -EPROBE_DEFER  → kernel retries later (dependencies not ready)
   - returns other negative → probe failed, driver unbound
```

Check the probe result:

```bash
# Was probe called?
dmesg | grep -i "probe\|compatible\|<driver-name>" | tail -30

# Did probe fail or defer?
dmesg | grep -E "(probe error|EPROBE_DEFER|-EIO|-ENOMEM|-ENODEV)" | tail -20

# Which driver owns the device?
ls -la /sys/bus/platform/devices/<node-name>/driver
ls -la /sys/bus/i2c/devices/<bus>-<addr>/driver   # e.g. /sys/bus/i2c/devices/1-003c/driver
```

## Debugging a Missing `/dev` Node

Work through these layers in order:

```bash
# 1. Is the DT node present and status = okay?
cat /proc/device-tree/<path>/status 2>/dev/null || echo "node missing or not status=okay"
ls /proc/device-tree/   # top-level nodes

# 2. Was the driver loaded?
lsmod | grep <driver_module>
modprobe <driver_module> && dmesg | tail -20

# 3. Did the driver probe?
grep -r "compatible" /sys/bus/*/devices/*/uevent 2>/dev/null | grep <driver>

# 4. Check for udev/mdev rule mismatch
udevadm monitor --kernel --udev   # watch for device events
udevadm info -a -p /sys/bus/i2c/devices/1-003c

# 5. Is the char device major/minor registered?
cat /proc/devices | grep <name>
ls -la /dev/<expected-node>
```

## Common DTS/Driver Failure Patterns

### Reset GPIO Polarity Mismatch

**Symptom:** driver probes but the device never responds on the bus.

```bash
# Check what the driver sees for the reset GPIO
dmesg | grep -i reset | grep -i <driver>
# Check GPIO value
gpioget <chip> <line>
```

Fix: swap `GPIO_ACTIVE_LOW` ↔ `GPIO_ACTIVE_HIGH` in the DTS node. Vendor BSPs
frequently have this wrong.

### Clock Not Enabled / Wrong Frequency

**Symptom:** device times out or returns a wrong ID on the first register read.

```bash
# Clock tree summary
cat /sys/kernel/debug/clk/clk_summary 2>/dev/null | grep -A2 -i <clock-name>

# From device: is the clock running?
cat /sys/kernel/debug/clk/<clock-name>/clk_rate
```

### `-EPROBE_DEFER` Loop

**Symptom:** the driver keeps deferring and the device never appears; after boot
completes there is still no bind.

```bash
# List deferred probes (kernel >= 5.10)
cat /sys/kernel/debug/devices_deferred 2>/dev/null

# Which dependency is missing?
dmesg | grep -i "defer" | grep <driver>
```

Typical cause: a `clocks`, `<rail>-supply`, or `gpios` phandle references a provider
that is `status = "disabled"` or absent from the DTS.

## Bus-Specific Debugging

### I2C

```bash
# Scan for devices on bus N
i2cdetect -y -r <N>

# Read a register (bus, address, register)
i2cget -y <N> 0x3c 0x00

# Trigger i2c trace (kernel I2C core debug)
echo 1 > /sys/kernel/debug/tracing/events/i2c/enable
cat /sys/kernel/debug/tracing/trace | grep i2c | tail -40
```

Review risks: wrong bus instance, stale DTS from another board, pull-up resistors
missing or the wrong value (I2C needs pull-ups to VDD — not VIO if they differ).

### SPI

```bash
# Verify chip select and device
ls /dev/spidev*

# Manual transfer test (spidev_test)
spidev_test -D /dev/spidev0.0 -v -p "\x9f\x00\x00"
```

### UART

```bash
# Check pinmux ownership (another driver stealing the pins?)
cat /sys/kernel/debug/pinctrl/*/pinmux-pins | grep -A1 <pin-name>

# Test loopback (short TX→RX)
stty -F /dev/ttyS1 115200 raw && echo "test" > /dev/ttyS1
```

### MMC/SD

```bash
# Enumerate MMC devices
ls /sys/bus/mmc/devices/
dmesg | grep -i "mmc\|sdio" | tail -20

# Timing mode actually used
cat /sys/bus/mmc/devices/mmc0:*/speed_class
cat /sys/kernel/debug/mmc0/ios
```

## Kernel Config Requirements

A driver failing silently at probe is often simply not compiled in:

```bash
# Check if driver is built
zcat /proc/config.gz | grep -i <DRIVER_CONFIG_NAME>
# or
grep <DRIVER_CONFIG_NAME> /boot/config-$(uname -r)

# In Yocto, check the active defconfig fragment (see yocto-oe-dev)
bitbake linux-yocto -c kernel_configcheck 2>&1 | grep -i <option>
```
