# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### Filippo Valsorda and the age authors: age

- Source: <https://github.com/FiloSottile/age>
- License: `BSD-3-Clause`
- Version: `v1.3.2`, `b74dce4cdbe35b5e5f66c06d9612b72f89028758`

The README, the `age` and `age-keygen` man pages, and the command source supplied the flags, key types, the
post-quantum and classic mixing rule, the SSH key limits, the plugin naming, and the stated security limits. No prose
was copied.

### C2SP: age format specification

- Source: <https://c2sp.org/age>
- License: `LicenseRef-No-License`
- Version: `v1.1.0`, 2025-12-22

The repository states no license, so all rights remain with its authors. The specification supplied the rule that a
passphrase stanza stands alone in a file.

### Filippo Valsorda: "age and Authenticated Encryption"

- Source: <https://words.filippo.io/dispatches/age-authentication/>
- License: `LicenseRef-Proprietary`
- Version: published 2022-09-29

The post supplied what age does not authenticate, and the signing tools it names as companions.

### Jack Grigg: rage

- Source: <https://github.com/str4d/rage>
- License: `MIT OR Apache-2.0`
- Version: `v0.12.1`, `7a854c9c8c02dab2ebea19e02e6693a5730a8b2a`

The README supplied where rage's command line differs from age's.

### Jack Grigg: age-plugin-yubikey

- Source: <https://github.com/str4d/age-plugin-yubikey>
- License: `MIT OR Apache-2.0`
- Version: `v0.5.1`, `9329e31dd3d0819d5d7b739aef59e455e10fcfa1`

The README, changelog, and source supplied the supported tokens, the retired-slot use, the PIN and touch policies,
the first-run PIN and management-key changes, and the coming `age1tag1` recipients. A user report in issue 216
supplied its failure on a Nitrokey 3.

### olastor: age-plugin-fido2-hmac

- Source: <https://github.com/olastor/age-plugin-fido2-hmac>
- License: `MIT`
- Version: `v0.5.0`, `e900059b946c4963bfc5ff92c3c663cc82b44572`

The README, the v2 specification, and the source supplied the enrolment choices, what the identity file holds, the
post-quantum flag and variable, and the device wait.

### Wiktor Kwapisiewicz: age-plugin-openpgp-card

- Source: <https://github.com/wiktor-k/age-plugin-openpgp-card>
- License: `Apache-2.0 OR MIT`
- Version: `v0.1.3`, `c191a18198c800d9fed964e31ed34f92cf67e7a1`

The README supplied the card requirements, the identity stub, and plugin-free encryption to the card's recipient.

### Nitrokey: Nitrokey documentation

- Source: <https://docs.nitrokey.com/>
- License: `LicenseRef-No-License`
- Version: read 2026-11-28

The documentation states no license, so all rights remain with Nitrokey. It supplied the Nitrokey 3's PIV applet.
