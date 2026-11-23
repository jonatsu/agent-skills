# Host-Side Tool Facts

These facts hold whatever token is plugged in. Current known versions, checked on real tokens or against upstream source
on 2026-11-23: GnuPG 2.4.8, OpenSSH 10.2, age 1.3.2, age-plugin-fido2-hmac v0.5.0. Before relying on a fact with a newer
version, re-check it against that tool's `--help` or changelog.

Sections: OpenPGP cards with GnuPG, FIDO2 SSH keys and `ssh` key selection, age identities through FIDO2,
password-manager CLIs, and GitHub key registration.

## OpenPGP Cards (GnuPG)

- Run `gpgconf --kill scdaemon` before a vendor tool talks to the card, and before `gpg --card-status` after one has:
  scdaemon holds the card otherwise.
- Layout: a certify-only primary key kept offline (in the password manager), with sign, encrypt, and authenticate
  subkeys on the card. A lost card then costs new subkeys, not the identity. `keytocard` replaces the local secret with
  a stub; `sec#` means the primary secret is absent, `ssb>` means the subkey is on a card.
- Generate in a temporary `GNUPGHOME` on tmpfs (`$XDG_RUNTIME_DIR`). Save and restore the daily `GNUPGHOME` rather than
  unsetting it, because a non-default daily path breaks when unset.
- A plugged-in card with keys becomes gpg's default signing key even in a fresh `--homedir`, because that home's agent
  starts scdaemon. A throwaway keyring that must sign with its own key needs `disable-scdaemon` in its
  `gpg-agent.conf`, or `--local-user` on each call.
- Make the old key's revocation certificate before a reset; after it, the old key cannot sign one. gpg prefixes the
  armor line of a generated revocation with a colon so it cannot be imported by accident; remove it to use it.
- keys.openpgp.org: `gpg --send-keys` cannot start user-ID verification. Upload with
  `gpg --export FPR | curl -T - https://keys.openpgp.org`, which prints the verification link; later updates to a
  verified key can use `--send-keys`.
- `gpg-agent` serves the card's authentication key over SSH with `enable-ssh-support`; the socket path comes from
  `gpgconf --list-dirs agent-ssh-socket` (a non-default `GNUPGHOME` adds a hashed directory).

## FIDO2 SSH Keys and `ssh` Key Selection

- Create a resident key with `ssh-keygen -t ed25519-sk -O resident -O verify-required -O application=ssh:NAME`. The key
  file holds only a handle; leave its passphrase empty. `ssh-keygen -K` restores the handle from the token, named after
  the application (`id_ed25519_sk_rk_NAME`).

- An aborted first run can leave the resident key on the token; the rerun then asks to overwrite the same application.
  Check the log for a first run before treating that prompt as an old key.

- `ssh` offers every key its agent holds before any key file, whatever the order of the `IdentityFile` lines (seen with
  `ssh -v`: agent keys show as "explicit agent", files as "explicit authenticator"). To make a hardware key primary,
  offer it alone while the token is present. The example tests for any Yubico device; use the token's own USB ID from
  its device file:

  ```text
  Match exec "lsusb -d 1050: > /dev/null 2>&1"
      IdentityFile ~/.ssh/HANDLE
  Match !exec "lsusb -d 1050: > /dev/null 2>&1"
      IdentityFile ~/.ssh/PASSWORD_MANAGER_KEY.pub
  Host *
      IdentitiesOnly yes
      AddKeysToAgent no
  ```

- `ssh` talks to one agent per connection (`IdentityAgent` takes one value), so keys in two different agents are never
  both offered. A key that lives on the same token as the FIDO2 key (an OpenPGP authentication subkey) is a manual
  fallback: `ssh -o IdentityAgent=SOCKET -o IdentityFile=KEY.pub HOST`.

- A FIDO2 reset deletes every credential, and also ends every non-resident `hmac-secret` identity (such as an age
  identity), because the token derives them from a device secret that the reset replaces. The FIDO2 PIN allows 8 tries
  and has no unblocking code; after 3 wrong tries in a row the token needs a replug.

## Age Identities Through FIDO2

- `age-plugin-fido2-hmac -g` enrolls without using a FIDO2 slot; the identity file holds the credential ID, so losing
  every copy loses the data. Answer yes to "require a PIN" (the PIN becomes part of the derived secret) and yes to
  "separate identity" (a native recipient, unlinkable files). Set `FIDO2_HMAC_PQ=0` for a classical recipient.
- Take the recipient from the identity file's `# public key:` line. `age-plugin-fido2-hmac -y` prints a long
  `age1fido2-hmac1…` plugin recipient instead and needs the token to do it.
- Decrypting copies the identity into memory, weaker than a key that never leaves a card (a PIV identity).
- `age` refuses to mix post-quantum and classical recipients in one file.
- With the token absent, `age` given only the plugin identity waits for it without end; given a native identity as
  well, in either order, it decrypts with the native one at once. Test with `timeout` and `< /dev/null`.
- Stream a fallback key from the password manager without writing it: `age -d -i <(op read 'op://…') FILE`.

## Password-Manager CLIs

- 1Password `op`: a dot in a field name is read as a section separator, so name fields without dots. `label[file]=PATH`
  attaches a file in both `op item create` and `op item edit`; `'label[delete]'` removes a field; `op read` reads a
  file attachment by its name. An authorization is per terminal session (tty and its start time), so a command run from
  another shell, a hook, or an agent's shell asks again.
- Bitwarden `rbw`: `rbw get --raw ITEM` returns JSON with the note body at `.notes` and custom fields under `.fields[]`
  (`.name`, `.value`); notes keep line breaks. Items with attachments or notes are created in the Bitwarden app; run
  `rbw sync` before reading a new item. Chezmoi's `(rbw "ITEM").notes` reads the same field.

## GitHub Key Registration

- `gh ssh-key add FILE --type authentication|signing --title TITLE` needs the scopes `admin:public_key` and
  `admin:ssh_signing_key` (`gh auth refresh -h github.com -s admin:public_key,admin:ssh_signing_key`).
- One account can hold the same key as both an authentication and a signing key, but GitHub refuses a key that another
  account holds ("key is already in use").
- Check registrations at the public endpoints: `https://github.com/USER.keys` for SSH authentication keys,
  `https://github.com/USER.gpg` for OpenPGP keys, and `https://api.github.com/users/USER/ssh_signing_keys` for SSH
  signing keys, which appear only there.
