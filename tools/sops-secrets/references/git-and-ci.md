# SOPS Files in Git and CI

## Read Diffs Without Printing Secrets

A plain `git diff` of an encrypted file shows which keys changed, because key names stay plaintext; the values show
as `ENC[...]`. That is usually enough, and it prints nothing secret.

A diff driver shows the decrypted change instead. Add it only when the user asks, and scope the pattern to encrypted
files, because `sops decrypt` fails on ordinary YAML:

```bash
printf 'secrets/** diff=sopsdiffer\n' >> .gitattributes
git config diff.sopsdiffer.textconv "sops decrypt"
```

The driver then decrypts in every `git diff`, `git log -p`, and `git show`, including yours, and the output lands in
the transcript. In a checkout that has it, pass `--no-textconv` to those commands for paths under `secrets/`.

## Resolve a Merge Conflict

Two branches that change one encrypted file always conflict, at least on the `mac` and `lastmodified` fields, and a
hand-merged file fails with `MAC mismatch`. Keep one side whole and redo the other side's change with sops:

1. Find which keys each side changed with `git diff --no-textconv <base> <branch> -- <file>`.
2. Take one side whole: `git show :3:<file> > <file>` keeps the branch being merged in, and `:2:` keeps your own.
   During a rebase the two swap: `:2:` is the branch you rebase onto.
3. Re-apply the other side's changes with `sops set --value-stdin` or `sops edit`. Ask the user for any value you
   cannot read from the other side without printing it.
4. Run `sops decrypt <file> >/dev/null`, then stage the file.

The conflict is resolved when the file decrypts and holds both sides' changes. Keeping secrets in several small files
makes such conflicts rarer.

## Reject Plaintext at Commit Time

sops ships no hook, but `sops filestatus` prints `{"encrypted":true}` only for a file with sops metadata and a MAC.
This pre-commit hook checks the staged copy of each file under `secrets/`, not the worktree copy:

```bash
#!/usr/bin/env bash
# Reject a commit whose staged copy of a file under secrets/ is not sops-encrypted.
set -uo pipefail
fail=0
while IFS= read -r -d '' f; do
  case "${f##*.}" in
    yaml | yml) type=yaml ;;
    json) type=json ;;
    env) type=dotenv ;;
    ini) type=ini ;;
    *) type=binary ;;
  esac
  if [[ "$(git show ":${f}" | sops filestatus --input-type "${type}" /dev/stdin 2>/dev/null)" != '{"encrypted":true}' ]]; then
    printf 'not encrypted: %s\n' "${f}" >&2
    fail=1
  fi
done < <(git diff --cached --name-only -z --diff-filter=ACMR -- secrets/)
exit "${fail}"
```

Change `secrets/` to the repository's secrets paths, the same ones its `.sops.yaml` rules match.

## Give CI a Key

- Give CI its own age key, and name its public key only in the rules for files CI needs.

- Store the private key in the CI system's secret store, and expose it to the job as `SOPS_AGE_KEY`.

- Run the job's commands through `sops exec-env --pristine` or `sops exec-file`, so later steps never see the key.

- Install sops from a release and check it against the release's checksum file before running it:

  ```bash
  v=3.13.3  # set to the latest release
  base="https://github.com/getsops/sops/releases/download/v${v}"
  curl -fsSLO "${base}/sops-v${v}.linux.amd64"
  curl -fsSLO "${base}/sops-v${v}.checksums.txt"
  sha256sum --check --ignore-missing "sops-v${v}.checksums.txt"
  ```

  The release also carries `sops-v<version>.checksums.sigstore.json`, a signature over the checksum file for cosign.
