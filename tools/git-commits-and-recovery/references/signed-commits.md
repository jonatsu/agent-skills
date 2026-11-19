# Signed Commits

"Is this commit signed?" and "does its signature verify here?" have different answers, and the usual mistake
is answering the wrong one.

## `%G?` Does Not Detect Every SSH Signature

With `gpg.format=ssh` and no `gpg.ssh.allowedSignersFile` configured, a correctly signed commit reports `%G?` = `N` and
`--show-signature` prints `No signature`. Verified on git 2.43.0, 2026-08-26; git does emit
`error: gpg.ssh.allowedSignersFile needs to be configured` on stderr, so it is misleading rather than silent.

A commit that is signed and a commit whose signature this machine can check are different facts, and `%G?`
reports only the second. Reading it as the first is how a correctly signed history gets reported as unsigned.

## Answer the Intended Signature Question

**Is this signature valid?** Then **configure `gpg.ssh.allowedSignersFile`**. That is the fix; verification works
normally afterwards. Fix the one-line misconfiguration itself rather than building a workaround around it.

**Does this commit carry a signature at all?** Read the object header and cut it at the first blank line. A body line
beginning `gpgsig` then cannot impersonate one:

```bash
git cat-file commit <hash> | sed -n '/^$/q;p' | grep -qE '^gpgsig(-sha256)? '
```

**The guard is load-bearing rather than defensive decoration.** An unsigned commit whose message body simply begins
`gpgsig -----BEGIN SSH SIGNATURE-----` is reported as signed without it, and anyone can write that message.

## Before Reporting a Signing Conclusion

- Say which question you answered: carries a signature, or verifies here.
- Name `gpg.format` and whether `gpg.ssh.allowedSignersFile` is set, since an unset one makes every SSH-signed
  commit read as unsigned.
- Check the object header before reporting "unsigned" from `%G?`.
