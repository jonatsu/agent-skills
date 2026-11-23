# YubiKey

Current known versions, checked on a YubiKey 5 with firmware 5.7.4 on 2026-11-23: ykman 5.8.0, age-plugin-yubikey
0.5.1. Before relying on a fact with a newer version, re-check it against `ykman <applet> --help` or the changelog.

## Capabilities

A YubiKey 5 has separate applets for FIDO2 and U2F, OpenPGP (a real OpenPGP card, used through GnuPG), PIV, OATH
(TOTP and HOTP, read with `ykman oath` or Yubico Authenticator), and two OTP slots (Yubico OTP, static password,
challenge-response). Each applet has its own PINs and its own reset.

- Discoverable FIDO2 credentials: 100 from firmware 5.7.4 by Yubico's firmware page; its FIDO page still says 25, so
  read the real count from `ykman fido info` or `fido2-token -I -c`.
- OATH holds 32 accounts, or 64 from firmware 5.7.0. `ed25519-sk` SSH keys need firmware 5.2.3 or later; use
  `ecdsa-sk` below it.

## Inventory

```bash
gpgconf --kill scdaemon     # release the card for ykman
ykman list; ykman info      # model, serial, firmware, enabled applets
ykman fido info             # FIDO2 PIN set or not, retries
ykman fido credentials list # resident credentials; asks for the FIDO2 PIN
ykman piv info              # PIN and PUK retries, management key type, filled slots
ykman openpgp info          # PIN retries, touch policies
ykman oath accounts list
age-plugin-yubikey --list   # age identities in PIV slots
```

## PINs, Resets, and Firmware

- Each reset touches one applet only: `ykman fido reset`, `ykman piv reset`, `ykman openpgp reset`, `ykman oath reset`.
  `ykman fido reset` must run right after the key is inserted and needs a touch. `ykman openpgp reset` does not reset
  the attestation key and certificate.
- The firmware cannot be updated. A feature that needs newer firmware needs a newer key.

## PIV and age

- `age-plugin-yubikey` stores its identity in a retired slot (slot 82 for its slot 1). When it finds the factory PIN, it
  sets the PIN and the PUK to the same new value, so change the PUK afterwards (`ykman piv access change-puk`), and it
  replaces the factory management key with a random TDES key stored on the token behind the PIN. Keep that management
  key: the plugin's Rust library has had trouble with AES management keys.
- A PIV identity's private key never leaves the token, unlike an `hmac-secret` identity, which is derived into memory.

## Linux

- `lsusb -d 1050:` detects any Yubico device; every YubiKey model shares that vendor ID.
- `ykman` reaches the smart-card applets (PIV, OpenPGP, OATH) through `pcscd`, so that service must be running.

## Backup

Nothing generated on a YubiKey can be copied off it. Back up by registering a second key with each service, and by
generating an OpenPGP key off the card and keeping its secret in the password manager before `keytocard`.
