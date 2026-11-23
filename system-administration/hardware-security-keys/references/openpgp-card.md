# OpenPGP Card Procedure

The order that put an offline OpenPGP identity on a Nitrokey 3 and a YubiKey 5, checked with GnuPG 2.4.8 on
2026-11-23. It holds for any token with a real OpenPGP card; the touch commands and factory PINs differ per token, so
read its device file too. Run each numbered part as one witnessed-log block, and check its result in the next.

Sections: defaults, temporary home, keys, export and verify, card PINs and data, `keytocard` and touch, daily keyring
and tests, and later changes.

## Defaults to Offer

- An ed25519 certify-only primary key with a 10-year expiry, and ed25519 sign, cv25519 encrypt, and ed25519
  authenticate subkeys with 2-year expiries.
- Touch required for signing and authentication, and the PIN required for every signature (forced signature PIN).
- The passphrase, user PIN, Admin PIN, reset code, secret-key export, public key, and revocation certificate all in the
  password manager.

## 1. Temporary Home

Work in a GnuPG home on tmpfs, with the daily `gpg.conf` and `scdaemon.conf` copied in. Without the daily
`scdaemon.conf` (for example its `disable-ccid`), the temporary scdaemon uses its internal driver, and once `pcscd` holds
the token, `keytocard` fails with "selecting card failed: No such device".

```bash
DAILY_GNUPGHOME="${GNUPGHOME:-$HOME/.gnupg}"
WORK=$(mktemp -d -p "$XDG_RUNTIME_DIR" openpgp.XXXXXX)
export GNUPGHOME=$(mktemp -d -p "$XDG_RUNTIME_DIR" gnupg.XXXXXX)
cp "$DAILY_GNUPGHOME"/gpg.conf "$DAILY_GNUPGHOME"/scdaemon.conf "$GNUPGHOME"/
gpgconf --kill scdaemon
```

## 2. Keys

Build the user ID from stored data, such as the dotfiles manager's data file, rather than having the operator type an
address. Each command asks for the passphrase. A cancelled prompt fails only that command, so list the keys afterwards
and check for exactly one subkey per capability: `[S]`, `[E]`, and `[A]`.

```bash
gpg --quick-gen-key "$USER_ID" ed25519 cert 10y
FPR=$(gpg --list-keys --with-colons "$USER_ID" | awk -F: '/^fpr/ {print $10; exit}')
gpg --quick-add-key "$FPR" ed25519 sign 2y
gpg --quick-add-key "$FPR" cv25519 encr 2y
gpg --quick-add-key "$FPR" ed25519 auth 2y
gpg -K --with-subkey-fingerprints "$FPR"
```

## 3. Export and Verify

Write each file with `>|`, so a rerun after a cancelled prompt replaces it under `noclobber`. Keep the revocation
certificate with its leading colon; remove the colon only when revoking.

```bash
gpg --armor --export-secret-keys "$FPR" >| "$WORK/secret.asc"
gpg --armor --export "$FPR" >| "$WORK/public.asc"
cp "$GNUPGHOME/openpgp-revocs.d/$FPR.rev" "$WORK/revocation.asc"
```

Store the files in the password manager, then read each one back and `cmp` it with the export. Then import the secret
export into a throwaway keyring with `disable-scdaemon`, so a plugged-in card's key cannot stand in for it, and list
`sec` and `ssb`:

```bash
CHECK=$(mktemp -d -p "$XDG_RUNTIME_DIR" gnupg-check.XXXXXX)
echo disable-scdaemon >| "$CHECK/gpg-agent.conf"
gpg --homedir "$CHECK" --pinentry-mode loopback --import "$WORK/secret.asc"
gpg --homedir "$CHECK" --list-secret-keys --with-colons | grep -E '^(sec|ssb)' | cut -d: -f1,5,12,15
gpgconf --homedir "$CHECK" --kill all; rm -rf "$CHECK"
```

Import with `--pinentry-mode loopback`. Through pinentry, GnuPG 2.4.8 rejected a cv25519 subkey (`Bad secret key`)
yet still reported `secret keys imported: 1`. The check passes only when every `sec` and `ssb` line ends in `+`; a
`#` means that secret is missing.

## 4. Card PINs and Data

1. Unplug every other card, then run `gpg --card-status` and confirm the serial matches the inventory.

2. Run `gpg --change-pin` and choose, in this order: 3 for the Admin PIN, 4 for the reset code (it needs the Admin PIN),
   then 1 for the user PIN. Name the factory PINs from the device file in the block; most cards ship `123456` and
   `12345678`.

3. In `gpg --edit-card`, run `admin`, then `key-attr`: choose ECC and Curve 25519 for each of the three slots. Set the
   cardholder data there too (`name`, `lang`, `login`, `url`).

4. Set the forced signature PIN with a command that checks first, because `forcesig` toggles the flag:

   ```bash
   gpg --card-status | grep -q 'Signature PIN.*not forced' && gpg-card forcesig
   gpg --card-status | grep 'Signature PIN'
   ```

## 5. `keytocard` and Touch

Move one subkey at a time in `gpg --edit-key "$FPR"`: `key 1`, `keytocard`, slot 1 (Signature), then `key 1` again to
deselect it; `key 2`, `keytocard`, slot 2 (Encryption), `key 2`; `key 3`, `keytocard`, slot 3 (Authentication); then
`save`. `gpg -K` now shows `ssb>` for each subkey. Only the temporary keyring loses its secret copies; the backup from
part 3 keeps them.

Set touch after `keytocard`, never before: on a YubiKey 5 with firmware 5.7.4, `keytocard` was observed to reset every
slot's touch policy to Off. Use the device file's command, kill scdaemon before a vendor tool, and check the result
with that tool's info command.

## 6. Daily Keyring and Tests

```bash
gpgconf --kill all; rm -rf "$GNUPGHOME"
export GNUPGHOME="$DAILY_GNUPGHOME"   # or unset GNUPGHOME when the daily home is the default
gpg --import "$WORK/public.asc"
gpg --card-status                     # creates the secret-key stubs
echo "$FPR:6:" | gpg --import-ownertrust
echo test | gpg --clearsign >| /dev/null && echo signed
echo test | gpg --encrypt --recipient "$FPR" | gpg --decrypt
```

Test SSH with `ssh-add -L` through gpg-agent's socket, or `gpg --export-ssh-key "$FPR"` where no such socket exists,
such as on a host whose password manager owns SSH. Publish as `tools.md` describes. Once every backup is verified,
`shred -u` the files in `$WORK` and remove it.

## Later Changes

Each needs the primary secret: import `secret.asc` from the password manager into a fresh temporary home (part 1).
Import `secret.asc` with `--pinentry-mode loopback` and run part 3's check. Before a new export replaces the backup,
run `gpg --list-packets` on it and confirm that no secret key shows `gnu-dummy`. A keyring that lost a subkey exports
it as a stub, and the card would become that subkey's only copy.

- **Renew:** `gpg --quick-set-expire "$FPR" 2y '*'` renews every subkey; `gpg --quick-set-expire "$FPR" 10y` renews the
  primary. Export the public key, import it into the daily keyring, and publish it. The card needs no change.
- **Replace a subkey:** add a new subkey of the same capability, `keytocard` it into the same slot, and revoke the old
  one (`key N`, `revkey`). Back up and publish again.
- **Lost card:** revoke the lost card's three subkeys, create new ones, and move them to the new card. The identity
  and its fingerprint stay.
- **Revoke the identity:** remove the revocation certificate's leading colon, `gpg --import` it, and publish the result.
