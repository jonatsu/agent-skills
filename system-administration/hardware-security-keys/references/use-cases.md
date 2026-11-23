# What Each Function Is For

Read on 2026-11-23 from first-party sources: OpenSSH 10.x man pages and `PROTOCOL.u2f`, systemd 262
(`systemd-cryptenroll(1)`, `crypttab(5)`), pam-u2f 1.4.0, GnuPG 2.5 `gpg-agent` documentation, `git-config`, GitHub and
GitLab documentation, and the vendor guides. Use this file to explain a function in plain words, then to recommend
uses for what the person actually does. Check the token's device file for which functions it has.

Sections: FIDO2 and U2F, `hmac-secret`, OpenPGP card, PIV, OATH codes, keyboard slots, choosing an SSH method, Git
signing, full-disk unlock, login and `sudo`, password managers, and a default setup.

## FIDO2 and U2F

FIDO2 keeps private keys on the token and signs a challenge bound to the website's domain, so a look-alike site gets
nothing it can use. U2F is the older protocol: second factor only, touch and no PIN.

- **Second factor on a website.** The site asks for the password, then a touch. The token stores nothing per site, so
  this uses no storage. It resists phishing, which TOTP and SMS codes do not.
- **Passkey on the token.** A discoverable (formerly "resident") credential that the token stores, used with the PIN,
  replaces password and second factor. Storage is limited and shared with resident SSH keys; the device file gives
  the count.
- **Register two tokens on every site.** No FIDO credential can be exported, so a second token, registered separately,
  is the only recovery besides the site's recovery codes. Keep recovery codes in the password manager.
- **Traps.** The FIDO2 PIN allows 8 tries; after that only a FIDO reset helps, and a reset deletes every credential on
  the token.

## `hmac-secret`

The token mixes a salt from the computer with a secret that never leaves the token and returns the result, which the
computer uses as a key. Browsers expose it as the WebAuthn `prf` extension.

- Uses: full-disk unlock (`systemd-cryptenroll --fido2-device`), an age identity (`age-plugin-fido2-hmac`, in
  [tools.md](tools.md)), and unlocking a password manager with a passkey where the manager and browser support `prf`.
- Trap: a FIDO reset replaces the token's secret, so everything derived from it is gone. Keep another way in for each.

## OpenPGP Card

The token acts as a smart card with up to three OpenPGP keys, to sign, decrypt, and authenticate, behind a PIN. GnuPG
sends it the work, so the private keys stay on the card.

- Uses: email and file signing and encryption, SSH through `gpg-agent` (`enable-ssh-support`), and Git signing. One
  identity then covers all three.
- Traps: a key generated on the card has no backup, so a lost card leaves old encrypted mail unreadable; generate off
  the card and keep the secret in the password manager before `keytocard`. The user PIN and the admin PIN each block
  after 3 wrong tries.
- Offer it to someone who already uses OpenPGP or needs encrypted mail. For SSH and Git signing alone, FIDO2 is simpler.

## PIV

PIV is a government smart-card standard: keys with X.509 certificates in named slots, reached through PKCS#11 (OpenSC or
a vendor module). Its slots have fixed roles: 9a authentication (PIN once per session), 9c signing (PIN before every
signature), 9d encryption, 9e card authentication (no PIN), and 82 to 95 retired slots.

- **When it helps on Linux:** a service that wants a client certificate or a PKCS#11 token, such as a VPN (OpenVPN
  `--pkcs11-id`, strongSwan's `pkcs11` plugin), browser client certificates, code signing (`osslsigncode`), smart-card
  login through SSSD or `pam_p11`, or an organisation that runs a certificate authority. An age identity that never
  leaves the token (`age-plugin-yubikey`) is the one personal use with no certificate authority behind it.
- **When it does not:** for personal SSH, Git signing, and web sign-in, FIDO2 does the same with less setup.
- **SSH through PIV:** `ssh -I /path/to/module.so` or `PKCS11Provider`; `ssh-keygen -D MODULE -e` prints the public key.
  The slot needs a certificate even for SSH, because the PKCS#11 library reads the public key from it. `ssh-agent`
  loads only modules under `/usr/lib*/` or `/usr/local/lib*/` unless `-P` widens that.
- **Traps:** a slot's PIN and touch policies are set when its key is generated or imported and cannot change later. Each
  use needs a certificate from some authority; the token only protects the private key.

## OATH Codes (TOTP and HOTP)

The token holds the same shared secret an authenticator app would and produces the six-digit code on request, so any
site that accepts an authenticator app accepts it.

- Gain: the secret sits in hardware and travels with the token. An access password (`ykman oath access change`) or a
  touch per code (`--touch`) protects it.
- Traps: the secret cannot be read back, so load it into both tokens in one sitting, or keep it in the password manager
  too. A code can still be phished, unlike FIDO2. The computer supplies the time; a token that types codes itself
  keeps a clock the computer must set first.
- Offer it as a fallback for sites with no FIDO2 support.

## Keyboard Slots (Static Passwords, Vendor OTP, Challenge-Response)

The token acts as a keyboard: a touch types a fixed password, a vendor one-time code, or a challenge-response answer.

- A static password has no PIN in front of it, and the token types it into whatever window has focus. A password
  manager is the better home.
- Yubico OTP needs a validation service, and `yubico-pam` is end of life; use FIDO2 for new work.
- HMAC-SHA1 challenge-response is what KeePassXC uses to unlock a database. It is a separate feature from FIDO2
  `hmac-secret`.

## Choosing an SSH Method

- **FIDO2 (`ed25519-sk`, or `ecdsa-sk` where the token lacks Ed25519)** is the simplest. A non-resident key keeps only
  a handle in the key file, so losing the file loses the key even with the token present. A resident key
  (`-O resident`) lets `ssh-keygen -K` restore the handle on any machine, uses a storage slot, and gives a thief who has
  the token more to try.
- `-O verify-required` asks for the PIN; touch is the default anyway. `sshd` refuses a key made with
  `-O no-touch-required` unless `authorized_keys` allows it. To the server, a FIDO key counts as one factor even with a
  PIN; use `AuthenticationMethods` for two.
- **OpenPGP authentication subkey** through `gpg-agent`, for someone who already keeps an OpenPGP identity on the card.
- **PIV through PKCS#11**, for an organisation with a certificate authority. A key on a token can also sign SSH
  certificates as a CA (`ssh-keygen -s ca.pub -D MODULE` or `-U`); servers then trust the CA through
  `TrustedUserCAKeys`.

## Git Signing

- **SSH signing:** `git config gpg.format ssh` and `user.signingKey`; Git 2.34 or later. An existing authentication key
  can sign, but GitHub and GitLab need it registered again as a signing key. Local verification needs
  `gpg.ssh.allowedSignersFile`: copy each line from the key's `.pub` file, because a FIDO key's type starts
  with `sk-ssh-ed25519`, not `ssh-ed25519`. GitLab lists `ED25519_SK` and `ECDSA_SK` as signing types and marks a
  commit unverified when the committer email is not a verified address on the account.
- **OpenPGP signing:** the default `gpg.format`; keys can expire and be revoked, at the cost of more setup and often a
  PIN per signature.
- A FIDO key asks for a touch on every commit, and for the PIN too with `verify-required`. Say so before setting it up.

## Full-Disk Unlock (`systemd-cryptenroll`)

- Works on LUKS2 only. `--fido2-device=auto` needs `hmac-secret`; by default it asks for the PIN and a touch.
  `--pkcs11-token-uri=auto` needs a certificate or public key on the token with its key pair, such as a PIV slot set up
  first. systemd's own advice is that FIDO2 is usually the better choice.
- Unlock needs a `/etc/crypttab` entry with `fido2-device=auto` or `pkcs11-uri=auto`. For the root volume, the
  initramfs must read crypttab (systemd-based initramfs, dracut); test the unlock there before relying on it.
- Enrolling needs an existing unlock method, and a PKCS#11 key cannot be used to enroll another one. Always keep a
  passphrase or a recovery key (`--recovery-key`), and enroll the second token too.

## Login and `sudo` (`pam_u2f`)

- `pamu2fcfg` registers a token; `pamu2fcfg -n` appends a second one. In `/etc/pam.d/sudo`, `required` adds the token to
  the password and `sufficient` replaces the password.
- Keep a root shell open while changing PAM: a wrong line can lock everyone out. Keep the mapping file under `/etc`
  (`authfile=`), because a mapping file in an encrypted home cannot be read before login. Register both tokens.
- Avoid `nouserok`, which lets a user with no mapping in without a token; versions before 1.3.1 also had a flaw in it
  (CVE-2025-23013). The default origin is `pam://` plus the host name, so set `origin=` and `appid=` before sharing a
  mapping across machines.
- It works only at a local session, not over SSH. PIV logins use SSSD or `pam_p11` instead.

## Password Managers

- Register both tokens as the second factor, and keep the recovery code somewhere other than the token. Bitwarden also
  accepts a passkey for login and, with a `prf`-capable browser and token, for unlock. 1Password accepts a security key
  as its second factor only through U2F, so U2F must be enabled on the token.
- Losing the token without the recovery code or another method can lock the vault for good. Set up the recovery path
  before relying on the key.

## A Default Setup for Two Tokens

Offer this as the starting point, then adjust it to what the person uses:

1. Two tokens, both registered everywhere, the spare kept elsewhere, and a FIDO2 PIN on both.
2. The key as a second factor on most sites, and passkeys on it only for a few accounts that matter most: the main
   email, the password manager, and the code host.
3. One resident `ed25519-sk` key per token with `verify-required`, both public keys registered on servers and the code
   host.
4. Git signing with that SSH key.
5. Full-disk unlock with both tokens, plus a recovery key and the passphrase.
6. `pam_u2f` for `sudo` as `required`, after the other steps work.
7. TOTP on the token only as a fallback; OpenPGP only for someone who already uses it; PIV only when a service asks for
   a certificate.
