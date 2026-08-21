# Advanced Patterns

## Sharing a Secret Between Services (Different Owners)

```nix
{
  sops.secrets.shared-db-password = {
    owner = "service1";
    group = "service1";
  };
  # Same secret, different owner — use a second secret entry pointing to same key
  sops.secrets.shared-db-password-service2 = {
    sopsFile = ./secrets/db.yaml;
    key = "db_password";  # Same key in same file
    owner = "service2";
    group = "service2";
  };
}
```

## Impermanence Compatibility

When using sops-nix with impermanence (nix-community/impermanence), secrets must be in tmpfs (not persisted):

```nix
sops.useTmpfs = true;  # Ensures secrets are NOT persisted to disk
```

## Git Diff in Cleartext (sops filter)

Add `.gitattributes` to see cleartext diffs of sops-encrypted files:

```
secrets/*.yaml diff=sopsdiffer
```

Then in `.git/config`:
```ini
[diff "sopsdiffer"]
    textconv = "sops -d"
```
