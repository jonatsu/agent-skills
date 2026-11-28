# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### CNCF SOPS project: sops

- Source: <https://github.com/getsops/sops>
- License: `MPL-2.0`
- Version: `v3.13.3`, `26e2f4784ca61353082c32dbd987c25eda086dc9`

The source code, help text, changelog, and issues 52, 571, 1117, and 2254 supplied the command behaviour, the
configuration lookup and rule matching, the environment `exec-env` passes on, and the merge and hook limits. No code
was copied.

### CNCF SOPS project: SOPS documentation

- Source: <https://github.com/getsops/docs>, the source of <https://getsops.io/docs/>
- License: `CC-BY-4.0`
- Version: `b2aae9d6dec115d384e96bdf8b1d09fe5ec73bb3`

The documentation supplied the creation-rule syntax, the `encrypted_regex` example for Kubernetes Secrets, the diff
driver, and the order for removing a compromised key. No prose was copied.

## Third-party Sources

### Jessica Black: agents `using-sops` skill

- Source: <https://github.com/jssblck/agents>, `skills/using-sops/`
- License: `GPL-3.0-only`
- Version: `e1294cd9041643344c849e88d7fa5a2342f11a3b`

The skill supplied the ideas of checking access with a command that prints nothing, keeping the age key variables out
of a child's environment, and a separate key per scope such as CI. No prose was copied due to the license.

### darkmatter: skills `sops-secret-access` skill

- Source: <https://github.com/darkmatter/skills>, `skills/sops-secret-access/`
- License: `LicenseRef-No-License`
- Version: `1d9f6b47ca1a4cbc0f56194790013551c4906da5`

The repository states no license, so all rights remain with its author. The skill supplied the ideas of reading key
names from the encrypted file, filtering decrypted output down to the one fact needed, and checking `git status` after
writing plaintext. No prose was copied.
