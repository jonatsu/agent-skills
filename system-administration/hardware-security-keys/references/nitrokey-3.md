# Nitrokey 3

Current known versions, checked on a Nitrokey 3A NFC with firmware v1.9.1 on 2026-11-23: nitropy (pynitrokey) 0.14.1.
Before relying on a fact with a newer version, re-check it against `nitropy nk3 --help` or the firmware release notes.

## Capabilities

A Nitrokey 3 has FIDO2 and U2F, OpenPGP (a real OpenPGP card, used through GnuPG), a secrets app for TOTP, HOTP and
static passwords (up to 50 entries; `nitropy nk3 secrets`, or Nitrokey App 2), and PIV, which nitropy still marks
experimental. Configure it with `nitropy`.

## Inventory

```bash
gpgconf --kill scdaemon                          # release the card for nitropy
nitropy nk3 list
nitropy nk3 get-config opcard.use_se050_backend  # whether OpenPGP keys live in the secure element
nitropy fido2 list-credentials                   # asks for the FIDO2 PIN
nitropy nk3 piv --experimental info
```

## OpenPGP

- `nitropy nk3 set-config opcard.use_se050_backend true` moves OpenPGP keys into the secure element and wipes the
  OpenPGP applet by itself.
- Touch is GnuPG's user interaction flag: `gpg-card uif N on|off|permanent`, with N 1 for signing, 2 for decryption,
  and 3 for authentication. `permanent` cannot be turned off again. Check with `gpg --card-status`.
- `nitropy nk3 factory-reset-app opcard` resets OpenPGP only; `nitropy nk3 factory-reset` wipes every applet.

## PIV (firmware v1.9.1)

- Experimental in nitropy: `--experimental` goes right after `piv`. It offers P-256, P-384, and RSA only, no touch
  policy, no backup of generated keys, and no working age plugin.
- Factory PIN `123456` (6 to 8 digits) and PUK `12345678` (8 characters), with 3 tries each.
- `change-admin-key` takes the new key only as an argument, so it shows briefly in the process list; `admin-auth KEY`
  verifies it. A PIV factory reset needs the PIN blocked first.

## Firmware

`nitropy nk3 update` downloads the latest stable image, checks its signature, asks for a touch, and flashes it. Firmware
1.0.1 and later keep user data across an update, but an update is not a backup.

## Linux

- `lsusb -d 20a0:42b2` detects a Nitrokey 3A NFC.
- Nitrokey publishes udev rules (`41-nitrokey.rules` in its `nitrokey-udev-rules` repository) that let a normal user
  open the device.

## Backup

Secrets generated on the key cannot be copied off it. The only exception is an OpenPGP key generated on the computer
and then copied to the key, whose secret stays in the backup. For everything else, register a second key or another
factor with each service.
