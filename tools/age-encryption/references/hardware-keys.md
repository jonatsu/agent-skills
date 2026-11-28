# Hardware Keys as age Identities

Each route keeps the private key, or the secret it is derived from, on a token. An identity file tells age which token
and key to use, and the matching `age-plugin-*` binary must be on PATH. Decrypting needs the token, its PIN where one
is set, and usually a touch, so a run nobody attends cannot use one. Every hardware recipient is classic, so a file
encrypted to a token cannot also have post-quantum recipients.

Current known: age-plugin-yubikey 0.5.1, age-plugin-fido2-hmac 0.5.0, and age-plugin-openpgp-card 0.1.3, checked
2026-11-28 against their READMEs and source. None was run on a token.

## Choose the Route

| Token                                                        | Plugin                    | Where the key lives                      |
| ------------------------------------------------------------ | ------------------------- | ---------------------------------------- |
| YubiKey 4 or 5                                               | `age-plugin-yubikey`      | Generated on the token; never leaves it  |
| Nitrokey 3, or a YubiKey, holding an OpenPGP Curve25519 key  | `age-plugin-openpgp-card` | On the card                              |
| Any FIDO2 token with `hmac-secret`, Nitrokey 3 and YubiKey 5 | `age-plugin-fido2-hmac`   | Derived on the token, copied into memory |

The Nitrokey 3 has a PIV applet, but `age-plugin-yubikey` supports only YubiKey 4 and 5, and a user report says it
fails on a Nitrokey 3. Treat that pairing as unsupported. Provisioning a token, its PINs, and its OpenPGP keys belongs
to the `hardware-security-keys` skill; this file covers only the age side.

## YubiKey: age-plugin-yubikey

1. On Linux, start `pcscd`, the smart-card daemon the plugin talks through.

2. Generate the key and its identity file, here with the default policies shown:

   ```bash
   age-plugin-yubikey --generate --name backups --pin-policy once --touch-policy always > yubikey-identity.txt
   ```

   Running `age-plugin-yubikey` with no flags walks through the same choices interactively. It uses one of the 20
   retired PIV slots, never slots 9a to 9e, so PIV keys for SSH or certificates stay untouched. `--slot N` picks a
   slot, and `--force` overwrites a filled one; confirm that with the user first.

3. Expect the first run to replace a default PIN, setting the PUK to the same value, and to replace a default
   management key with a random one stored under the PIN. Have the user record the new PIN before it runs.

4. Take the recipient from `age-plugin-yubikey --list`. Release 0.5.1 prints `age1yubikey1...`. The next release
   prints `age1tag1...`, which age 1.3 encrypts to natively; other clients need the plugin on PATH as `age-plugin-tag`.

5. Decrypt with `age -d -i yubikey-identity.txt -o out FILE.age`.

The identity file is a stub with no secret in it. Regenerate a lost one with `age-plugin-yubikey --identity --slot N`.
PIN policy `once` asks once per session, which ends when the token is unplugged or another applet such as FIDO2 is
used. A YubiKey 4 asks every time.

## OpenPGP Card: age-plugin-openpgp-card

The card must already hold a Curve25519 encryption key. Install the plugin with
`cargo install --locked age-plugin-openpgp-card`; on Linux it needs `pcscd`, not GnuPG. Run `age-plugin-openpgp-card`
with no arguments: for each connected card it prints a `# age1...` recipient line and an `AGE-PLUGIN-OPENPGP-CARD-1...`
identity stub. Save the stub as the identity file; it can be printed again the same way.

The recipient is an ordinary `age1` key, so encrypting needs no plugin and no token. Decrypting runs
`age -d -i identity.txt`, and the plugin asks for the card's PIN.

## FIDO2: age-plugin-fido2-hmac

The plugin is experimental until its 1.0 release, and it needs libfido2. Enroll with `age-plugin-fido2-hmac -g`, which
uses no FIDO2 storage slot. Answer its questions this way:

- **Require a PIN: yes.** The PIN becomes part of the derived secret, so a forgotten PIN loses the data.
- **Separate identity: yes.** You get a native `age1` recipient and files nobody can link to the token. The identity
  file holds the credential ID and a salt but no secret, and without it the token cannot decrypt, so keep copies.
- **Post-quantum:** add `-pq` to `-g` for a post-quantum recipient; enrolment is classic by default.

Take the recipient from the identity file's `# public key:` line. `age-plugin-fido2-hmac -y` prints a long
`age1fido2-hmac1...` plugin recipient instead, and needs the token to do it. Without a separate identity, every file
carries the credential ID and salt, decrypts with `age -d -j fido2-hmac FILE`, and can be linked to the token.
`FIDO2_HMAC_PQ=0` or `1` answers the post-quantum question when an identity file is used as a recipient, as in
`age -e -i identity.txt`.

Each decryption copies the derived identity into memory, which is weaker than a key that never leaves a card. With
several tokens, the plugin waits for a touch on any of them; `FIDO2_TOKEN` names one device path. With the token
absent, the plugin waits for it, up to 50 seconds in its source, though it has been seen waiting longer. Given a
native identity as well, in either order, age decrypts with the native one at once. Bound such a test with
`timeout 70` and `< /dev/null`. A FIDO2 reset ends every identity enrolled this way.

## Back Up and Recover

- Encrypt each file to at least two recipients that do not share a token: a second token enrolled separately, or a
  classic software key kept offline, such as in a password manager. The backup must be classic, because every
  hardware recipient is.
- A lost or reset token loses its key. YubiKey PIV keys and FIDO2 secrets cannot be exported, and an OpenPGP card key
  survives only when it was generated off the card and backed up.
- Re-encrypting to a new set of recipients needs a remaining identity to decrypt each file first.
- Decrypt a test file with every backup identity before relying on it.

## Use a Hardware Identity With SOPS

sops 3.10 and later accept plugin recipients in `.sops.yaml` and an identity stub in `SOPS_AGE_KEY_FILE`, with the
plugin on PATH. The PIN and touch prompts need a terminal, so CI keeps a software key. sops does not encrypt to
`age1tag1...` itself: it looks for `age-plugin-tag` on PATH. The OpenPGP card route avoids both, because its
recipient is a plain `age1` key.
