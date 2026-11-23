# OnlyKey (Duo and Six-Button)

Current known versions on 2026-11-23: firmware v3.0.4-prod (2022-12-14, the latest signed release), OnlyKey App v5.5.0,
`onlykey-cli` from the PyPI package `onlykey` 1.2.10, `onlykey-agent` 1.1.15. The vendor repositories' `master`
branches carry newer, unreleased code; treat the published versions as the supported ones. Facts marked *observed*
were seen on a Duo on firmware v3.0.4; the rest come from the vendor's firmware and client source, because several
documentation pages are stale or copied from the six-button model.

## Capabilities

- **FIDO2 and U2F:** resident credentials (12 on a Duo), `hmac-secret`, `credProtect`, ES256 and Ed25519. A resident
  `ed25519-sk` SSH key with `verify-required` works (*observed*).
- **No OpenPGP card and no PIV:** the key has no smart-card interface, so `gpg --card-status` finds nothing and
  scdaemon is not involved. Offer no PIV step. OpenPGP and SSH-agent keys run through the host tools `onlykey-gpg` and
  `onlykey-agent` instead.
- **Slots typed as a keyboard:** 24 slots on a Duo (four colour profiles of six), each with a password up to 56
  characters and one second factor (TOTP, Yubico OTP, or U2F). TOTP needs the host to set the key's clock
  (`onlykey-cli settime`); with no clock it types `NOTSET`.
- **Key slots:** 4 RSA and 16 ECC slots for signing and decryption, and a separate HMAC-SHA1 challenge-response (used
  by KeePassXC), which is unrelated to FIDO2 `hmac-secret`.

## Set Up in the App Before Any FIDO Use

The first FIDO request to an unconfigured Duo, such as a website registration or `ssh-keygen -t ed25519-sk`,
provisions it with no device PIN and locks the backup key for good. Only a factory reset undoes that, and the reset
drops every FIDO credential. A button hold on an unconfigured Duo starts a keyboard-typed quick setup that types the
backup passphrase into the focused window. Set up an unconfigured Duo in the OnlyKey App, backup passphrase first, before
any button press or FIDO use.

## Inventory

```bash
onlykey-cli fwversion        # firmware, such as v3.0.4-prodn; reads cleanly only while unlocked
onlykey-cli getkeylabels     # the 4 RSA and 16 ECC slot labels
fido2-token -L               # find the FIDO device node
fido2-token -I /dev/hidrawN  # FIDO2 versions, extensions, clientPin
fido2-token -L -r /dev/hidrawN   # resident credentials; asks for the FIDO2 PIN
```

- The letter after the version is `c` on the six-button model and another letter on a Duo. The vendor source says `p`
  and `n` also mean PIN set and no PIN; a reading on a device did not settle that.
- `onlykey-cli getlabels` fails on the Duo in 1.2.10 with a `TypeError` (*observed*). Read the slot labels by holding
  button 2 for 5 seconds, which types them into the focused window.
- `getkeylabels` failed once with a `KeyError` and worked on the next run (*observed*). With no key plugged in,
  `onlykey-cli` prints an `AttributeError` about `_hid` on exit; the result is unchanged (*observed*).
- `onlykey-cli version` prints the CLI version; `--version` is not an option.

## PINs, Wipes, and Resets

- The device PIN is optional and separate from the FIDO2 PIN. With a device PIN set, the key does nothing for FIDO, SSH,
  or the CLI until the PIN is entered after each plug-in. On a Duo, the buttons type digits 1 to 3, and holding one for
  a second types 4 to 6; the firmware requires 7 to 16 characters.
- Wrong device PINs: 3 per plug-in, counted across plug-ins, and the key wipes itself after 10. A self-destruct PIN, if
  set, wipes it at once. Leave the wipe mode at its default, data only: full wipe also erases the firmware and cannot be
  switched back.
- The FIDO2 PIN is entered on the computer and allows 8 tries (*observed*: the counter fell from 8 to 7 after one
  wrong try). Running out locks FIDO2 only, until a FIDO reset.
- The four colour profiles are banks of slots under one PIN; the Duo has no second PIN for plausible deniability.
- A FIDO reset (`fido2-token -R` or `onlykey-cli reset`, with a touch) clears only FIDO2 and U2F: it regenerates the
  master secret, which ends every resident and non-resident registration and every `hmac-secret` identity. Password and
  key slots stay.
- Factory reset by hand: hold button 1 for 10 seconds or more (config mode), then button 2 for 20 seconds. A Duo
  without a PIN enters config mode with no authentication, so anyone holding it can wipe it.

## Config Mode and Firmware

- Config mode is button 1 held for 10 seconds or more on a Duo; documentation that says button 6 was copied from the
  six-button model. Config mode is needed to set the backup passphrase, load keys, restore a backup, and load firmware.
- Only the OnlyKey App's Firmware tab flashes firmware; the CLI cannot. Back up first and treat an update as able to wipe
  the key. The signed file is `Signed_OnlyKey_3_0_4_STD.txt`; check its SHA-256 against the release notes.

## Backup and Restore

- A backup needs a backup passphrase or key set first. The App refuses a passphrase under 25 characters. On a Duo
  without a device PIN, setup sets the passphrase once and then locks it.
- Unlocked, with a local editor focused, hold button 1 for 5 to 9 seconds: the key types an AES-256-GCM encrypted block
  between `-----BEGIN ONLYKEY BACKUP-----` and `-----END ONLYKEY BACKUP-----` (*observed* at about 6 seconds). A hold
  of 10 seconds or more enters config mode instead. Save the block as a file attachment, never in a single-line field.
- By the firmware source, a backup covers the slots, the RSA and ECC keys, the FIDO2 state, and every resident
  credential, so FIDO2 registrations and `hmac-secret` identities should survive a restore. A credential made after
  the last backup is not in it, so back up again after every enrollment. This has not been confirmed on a device.
- Restore needs the same passphrase on the target, config mode, and the App's Backup/Restore tab. It overwrites slot by
  slot without erasing first, and the same file can fill a second key.

## Linux

- `lsusb -d 1d50:60fc` detects the key (*observed* on a Duo); the six-button model shares that ID.
- The key types as a US keyboard layout. Switch the desktop layout to US before a backup or any typed output
  (*observed*), and tell the operator which window to focus for each step, because the text goes to whatever has focus.
- systemd's own rules should grant a normal user the FIDO interface (read from the rules, not confirmed on a device).
  The App and `onlykey-cli` use a second interface that needs the vendor's udev rule, `49-onlykey.rules`. As published,
  that rule grants every user read and write access (`MODE="0666"`); adapt it to `TAG+="uaccess"` or a group.
- The App's only Linux build is the v5.5.0 `.deb` from 2023, which reinstalls that rule on upgrade; the snap needs
  `--devmode`. Weigh both before installing.
- `onlykey-agent` 1.1.15 fails on Python 3.14 (`No module named 'pkg_resources'`), and `onlykey-gpg init` has an open
  failure with GnuPG 2.4.7. `onlykey-gpg` expects its own `GNUPGHOME`; set it per command rather than globally, or the
  daily keyring disappears.
