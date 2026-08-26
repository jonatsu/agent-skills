# sops-nix Option Reference

## NixOS — Top-level Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `sops.defaultSopsFile` | `path` | required | Default sops file |
| `sops.defaultSopsFormat` | `str` | `yaml` | Default format (yaml, json, ini, dotenv, binary) |
| `sops.defaultSopsKey` | `str` | `""` | Default key path in sops file |
| `sops.validateSopsFiles` | `bool` | `true` | Validate sops files at eval time |
| `sops.keepGenerations` | `int` | `0` | Keep N generations of secrets |
| `sops.log` | `bool` | `false` | Enable logging |
| `sops.environment` | `attrsOf str` | `{}` | Extra environment variables |
| `sops.package` | `package` | `pkgs.sops` | sops package |
| `sops.validationPackage` | `package` | `pkgs.sops` | Package for validation |
| `sops.useTmpfs` | `bool` | `false` | Use tmpfs for secrets (kernel <6.4 swap warning) |
| `sops.useSystemdActivation` | `bool` | `true` | Use systemd activation for secrets |
| `sops.age.generateKey` | `bool` | `false` | Generate age key if not exists |
| `sops.age.keyFile` | `path` | `null` | Path to age key file |
| `sops.age.sshKeyPaths` | `listOf path` | `[/etc/ssh/ssh_host_ed25519_key]` | SSH keys to convert to age |
| `sops.age.plugins` | `listOf package` | `[]` | age plugins (e.g. age-plugin-yubikey) |
| `sops.gnupg.*` | various | — | GPG backend options |

## NixOS — Per-Secret Options (`sops.secrets.<name>`)

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `sopsFile` | `path` | `defaultSopsFile` | Override sops file for this secret |
| `format` | `str` | `defaultSopsFormat` | Override format for this secret |
| `key` | `str` | `""` | Key path in sops file (`""` = whole file) |
| `path` | `str` | `/run/secrets/<name>` | Decrypted output path (readOnly) |
| `mode` | `str` | `0400` | File permissions |
| `owner` | `str` | `root` | File owner |
| `group` | `str` | `root` | File group |
| `uid` | `int` | `0` | Numeric owner (works even if user doesn't exist) |
| `gid` | `int` | `0` | Numeric group |
| `restartUnits` | `listOf str` | `[]` | systemd units to restart on change |
| `reloadUnits` | `listOf str` | `[]` | systemd units to reload on change |
| `neededForUsers` | `bool` | `false` | Decrypt to /run/secrets-for-users (early decryption) |
| `sopsFileHash` | `str` | readOnly | Hash of sops file (for restartTriggers) |

## home-manager Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `sops.defaultSopsFile` | `path` | required | Default sops file |
| `sops.defaultSopsFormat` | `str` | `yaml` | Default format |
| `sops.defaultSopsKey` | `str` | `""` | Default key path |
| `sops.age.keyFile` | `path` | required | Path to age key file |
| `sops.age.generateKey` | `bool` | `false` | Generate age key if not exists |
| `sops.secrets.<name>.sopsFile` | `path` | `defaultSopsFile` | Override sops file |
| `sops.secrets.<name>.format` | `str` | `defaultSopsFormat` | Override format |
| `sops.secrets.<name>.key` | `str` | `""` | Key path in sops file |
| `sops.secrets.<name>.path` | `str` | `%r/<name>` | Decrypted output path (%r = $XDG_RUNTIME_DIR) |
| `sops.defaultSymlinkPath` | `str` | `%r/secrets` | Default symlink path |
| `sops.defaultSecretsMountPoint` | `str` | `%r/secrets.d` | Mount point for secrets |

**CRITICAL: home-manager sops-nix has NO `owner`, `group`, `uid`, `gid`, `restartUnits`, `reloadUnits`, or `neededForUsers` options.** These are NixOS-only. For service restart on secret change, use `systemd.user.services.<name>.Unit.After = [ "sops-nix.service" ]`.

## Template Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `content` | `str` | `null` | Inline template content |
| `file` | `path` | `null` | External template file |
| `owner` | `str` | `root` | File owner |
| `group` | `str` | `root` | File group |
| `uid` | `int` | `0` | Numeric owner |
| `gid` | `int` | `0` | Numeric group |
| `mode` | `str` | `0400` | File permissions |
| `restartUnits` | `listOf str` | `[]` | Units to restart on change |
| `reloadUnits` | `listOf str` | `[]` | Units to reload on change |
