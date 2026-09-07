# Device Tree and Driver Bring-up

Work from the actual device, binding, and driver implementation. Resource names and sequencing are device contracts;
names taken from a neighboring sensor are not substitutes for its binding.

## Establish the Device and Its Owner

1. Inspect the live node and its ancestors. A disabled bus can prevent child enumeration.
   Linux treats absent `status`, `okay`, and `ok` as available; distinguish missing properties from missing nodes.
2. Identify the enumerated bus device and its driver symlink. Probe logs are useful but not every successful probe logs.
3. Check the running kernel configuration and module availability. `lsmod` omits built-in drivers.
4. Inspect the driver's matching tables and registration path. Check module aliases/autoloading separately from matching.
5. Follow its probe error and resource acquisition, including deferred suppliers, before editing the DT.

```bash
# Target: substitute the enumerated bus/address or platform device name.
ls -l /sys/bus/i2c/devices/1-003c/driver
cat /sys/bus/i2c/devices/1-003c/uevent
ls -l /sys/bus/platform/devices/DEVICE/driver
```

Use the target's accessible configuration, such as `/proc/config.gz` with IKCONFIG support or a verified build config.
An absent module file does not disprove a built-in driver. Loading a module can change hardware state;
do so only within the established target and diagnostic scope.

A matched driver can still fail before registering its subsystem interface. For a missing `/dev` entry, inspect the
subsystem's registered class device and dev_t, then node creation and namespace visibility.
See [board-bringup-checklist.md](board-bringup-checklist.md) and [camera-v4l2.md](camera-v4l2.md).
Neither all I2C devices nor all successful driver probes create a dedicated character device.

## Resource Map

For each consumer, identify its provider, binding property, driver lookup, enabled state, and required sequencing.

| Resource       | Questions that discriminate causes                                                                                     |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Clock          | Does `clock-names` match the driver's lookup? Is the provider bound? What rate and enable/prepare counts are reported? |
| Regulator      | Does each named `<rail>-supply` match the binding? Is the provider available and the voltage suitable?                 |
| Reset/GPIO     | Does the driver use logical assertion or a raw level? Who owns the line, and what are its active level and timing?     |
| Pinctrl        | Is the required state selected? Does another peripheral own those pins?                                                |
| Interrupt      | Does the specifier match the interrupt controller's cells and polarity/trigger contract?                               |
| DMA            | Are channels, addressability, reserved memory, and coherency constraints appropriate for this driver?                  |
| Media endpoint | Do both endpoints identify the intended connection and supported bus/lane configuration?                               |

Missing resources can produce explicit errors, deferred probing, optional fallbacks, or later failures depending on
the driver. Read that path instead of assuming every missing resource is silent.

`-EPROBE_DEFER` requests a retry when a dependency is unavailable; it is not itself a root cause.
If debugfs is supported and mounted, inspect `/sys/kernel/debug/devices_deferred` and the supplier's own probe result.
Availability and detail vary by kernel; absence of that file does not prove no deferrals occurred.
Check provider configuration, enumeration, driver binding, firmware, and probe errors as well as DT status.

## Clocks and Reset

Use the source release's [clock framework](https://docs.kernel.org/driver-api/clk.html) and
[reset API](https://docs.kernel.org/driver-api/reset.html).
`devm_clk_get()` acquires a handle; it does not enable the clock.
Pair successful `clk_prepare_enable()` with `clk_disable_unprepare()` on removal and subsequent error paths.
Check the return from rate changes and respect the driver's runtime power-management lifecycle.

`clk_get_rate()` can return a cached or recalculated rate regardless of enable state.
In `clk_summary`, inspect rate, enable/prepare counts, parent selection, and provider behavior separately.
A nonzero rate does not prove a pin toggles; zero does not uniquely identify a disabled parent.
Use a suitable measurement when physical clock behavior is the remaining unknown.

Choose exclusive reset control for a sole consumer and shared control only when its semantics fit the hardware.
Check reset operation errors. The legacy `devm_reset_control_get()` is a transitional alias in Linux v6.12;
prefer the explicit form without claiming that every upstream submission using the alias is rejected.
For GPIO resets, check logical assertion, the binding's polarity, and actual electrical level before changing flags.

When a driver needs no special module setup, use the appropriate `module_platform_driver()` or `module_i2c_driver()`
helper. Populate the driver's matching fields and relevant `MODULE_DEVICE_TABLE` entries.
Register the I2C driver at driver initialization, not from its own probe. Probe registers the device-specific
subsystem interface after the required resources and hardware initialization succeed.

## Bus-specific Checks

### I2C

Inventory adapters with `i2cdetect -l` and inspect bound devices before sending transactions.
Use the datasheet and driver to determine valid addressing, register width, transfer protocol, and read side effects.
Do not apply blanket `-y -r` scans. The
[i2c-tools manual](https://git.kernel.org/pub/scm/utils/i2c-tools/i2c-tools.git/tree/tools/i2cdetect.8?h=v4.4)
documents potentially destructive probes and receive-byte lockups on some devices.
Do not force access around a bound driver's ownership.

Check supplies, reset, pinmux, bus speed, and pull-ups against the schematic and each device's I/O ratings.
VDD and VIO naming is device-specific. Mixed voltage domains may need level translation; see
[NXP UM10204](https://cache.nxp.com/docs/en/user-guide/UM10204.pdf).
Use a bounded I2C trace from a driver-supported transaction when it can distinguish protocol failure from no transfer.

### GPIO and SPI

Start with `gpioinfo` and pinctrl ownership. libgpiod v2 uses chip selection such as `gpioget -c gpiochip0 5`;
v1 positional chip syntax differs. A normal gpioget request selects input direction.
The v2 `--as-is` option preserves direction but still requests the line; it is not a bypass for driver ownership.
Check the installed tool's help before use. See
[libgpiod's tools](https://libgpiod.readthedocs.io/en/master/gpio_tools.html).

For SPI, establish bus instance, chip select, mode, maximum frequency, and the attached device's command protocol.
A generic `spidev_test` payload can be a hardware command. Use it only with a suitable unowned/test device and a
known-safe transaction. Missing `/dev/spidev*` may be correct when a dedicated kernel driver owns the device.

### UART and MMC

For UART, inspect pinmux, clock, signal voltage, flow control, and console ownership before changing terminal settings.
A loopback requires appropriate electrical levels and an unused port; never short an active console as a casual test.
Capture both transmitted and received data under a timeout; an `echo` alone does not test reception.

For MMC/SD, inspect enumeration, supplies, reset/card-detect, pinctrl, and error logs.
Use the host's debugfs `ios` information when available to inspect the selected timing and clock.
A card's speed-class capability is not the current negotiated bus timing. Avoid write tests on a mounted production
filesystem while diagnosing the controller.

## Calibration and Per-unit Trim

First prove that the observed error is calibration-related rather than a clock, power, transport, or unit-conversion
fault. Keep measurements, uncertainty, source, and applied corrections observable.

- Describe board-wide hardware parameters through properties supported by the binding.
- Read per-unit factory values through the device's supported NVMEM/eFuse or storage mechanism.
  Do not encode one unit's trim in a shared board DT.
- For IIO devices, inspect the attributes actually exposed and apply the driver's documented offset/scale convention.
  Do not assume every channel provides calibration controls.
- Distinguish RTC oscillator trim from Linux system-clock discipline. Use the applicable driver interface or time
  synchronization mechanism rather than an unexplained application correction.
- Keep actuator limits in the configuration that owns the hardware/application contract and validate their units.

The [i.MX thermal binding](https://github.com/torvalds/linux/blob/v6.12/Documentation/devicetree/bindings/thermal/imx-thermal.yaml)
is one example of named calibration cells. Resolve cells and providers in the actual SoC tree rather than copying a
partial eFuse node from another board. For DT compilation and validation, use [device-tree-tooling.md](device-tree-tooling.md).
