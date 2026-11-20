# Vacation mode: feature brief

Our smart-thermostat app for iOS and Android gets a vacation mode. Nothing is designed yet.

- Purpose: keep the home at a frost-safe or energy-saving temperature while the residents are away, and have it
  warm again when they come back.
- Engineering wants the settings shown as the firmware names them: "setback setpoint", "hysteresis band (K)",
  and "pre-heat lead time (min)".
- Product wants a confirmation dialog on every change, because support calls spike when people turn the heating
  off by mistake.
- Marketing wants vacation mode on the home screen behind a single toggle.
- Most users turn it on in the last minutes before leaving home, often at the front door. A large share of them
  are over 65. Some homes are holiday rentals, where a guest uses the app rather than the owner.
- While vacation mode is on, the thermostat's wall panel shows only the room temperature.
