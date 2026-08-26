# Signed commits

Load this when a signature will not verify, when `%G?` reports `N` or `U`, or
when you must prove a commit carries a signature at all. Everything here is
about telling those three questions apart — they have different answers and the
usual mistake is answering the wrong one.

## `%G?` is not the answer under SSH signing

**Do NOT read `%G?` as the answer under SSH signing.** With `gpg.format=ssh` and
no `gpg.ssh.allowedSignersFile` configured, a correctly signed commit reports
`%G?` = `N` and `--show-signature` prints `No signature`. Verified on git 2.43.0,
2026-08-26; git does emit `error: gpg.ssh.allowedSignersFile needs to be
configured` on stderr, so it is misleading rather than silent.

A commit that is signed and a commit whose signature this machine can check are
different facts, and `%G?` reports only the second. Reading it as the first is
how a correctly signed history gets reported as unsigned.

## Two different questions, two different answers

**Is this signature valid?** Then **configure `gpg.ssh.allowedSignersFile`**.
That is the fix; verification works normally afterwards. Do not build a
workaround around a one-line misconfiguration.

**Does this commit carry a signature at all?** Read the object header, cutting at
the first blank line so a body line beginning `gpgsig` cannot impersonate one:

```bash
git cat-file commit <hash> | sed -n '/^$/q;p' | grep -qE '^gpgsig(-sha256)? '
```

The `sed` stops at the header/body boundary; without it the `grep` searches the
message too, which is the whole spoof. **The guard is load-bearing rather than
defensive decoration**: an unsigned commit whose message body simply begins
`gpgsig -----BEGIN SSH SIGNATURE-----` is reported as signed without it, and
anyone can write that message.

## Before reporting a signing conclusion

- Say which question you answered — carries a signature, or verifies here.
- Name `gpg.format` and whether `gpg.ssh.allowedSignersFile` is set, since an
  unset one makes every SSH-signed commit read as unsigned.
- NEVER report "unsigned" from `%G?` alone without checking the object header.
