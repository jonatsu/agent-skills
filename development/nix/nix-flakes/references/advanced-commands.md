# Flake Commands

## Build and run

```bash
nix build .#name              # Build specific output
nix build .                   # Build default package
nix run .#name -- args        # Run app with args
nix develop .#name            # Enter named devShell
nix develop -c command args   # Run command in dev env
```

## Flake management

```bash
nix flake init                # Create flake.nix from template
nix flake init -t <template>  # Initialize from specific template
nix flake show                # List all outputs
nix flake check               # Evaluate + run checks
nix flake metadata            # Show lock info
nix flake update              # Update ALL inputs (rewrite lock)
nix flake update nixpkgs      # Update specific input only
nix flake lock                # Create lock, never update existing
nix flake prefetch            # Fetch and compute hash without building
nix flake archive             # Copy flake + inputs to a store (for offline use)
nix flake clone               # Clone flake source to local directory
```

`nix flake update` and `nix flake update <input>` replace the deprecated `--recreate-lock-file` and
`--update-input` flags.

## Profile management

```bash
nix profile install nixpkgs#hello
nix profile list
nix profile remove hello
nix profile upgrade
nix profile rollback
nix profile history              # Show profile generations
nix profile diff-closures        # Compare two profile generations
nix profile wipe-history         # Delete old profile generations
```

Manage each profile with one tool: `nix profile` and `nix-env` use incompatible internal formats.

## nix develop phase shortcuts

```bash
nix develop --unpack        # Run only unpackPhase
nix develop --configure     # Run through configurePhase
nix develop --build         # Run through buildPhase
nix develop --check         # Run through checkPhase
nix develop --install       # Run through installPhase
```

## Installable resolution

`nix build .#package` resolves in this order:

1. `packages.<system>.package`
2. `legacyPackages.<system>.package`

For the bare default installable (`nix build .`), the deprecated fallback `defaultPackage.<system>` is still
consulted after `packages.<system>.default`.

## Output selection syntax

```bash
nix build .#package^*      # Build all outputs (out, dev, doc, etc.)
nix build .#package^out    # Build specific output
nix build .#package^dev    # Build dev output only
```

## Key flags

| Flag                             | Effect                                        |
| -------------------------------- | --------------------------------------------- |
| `--impure`                       | Allow mutable paths, `$NIX_PATH`              |
| `--override-input path url`      | Override input at eval time                   |
| `--override-flake <input> <url>` | Override flake input at eval time             |
| `--inputs-from <flake>`          | Use another flake's lock file inputs          |
| `--no-write-lock-file`           | Don't write lock                              |
| `--no-update-lock-file`          | Don't update lock file even if inputs changed |
| `--commit-lock-file`             | Auto-commit lock changes                      |
| `--print-out-paths`              | Print resulting store paths to stdout         |
| `-L`                             | Show full build output                        |
