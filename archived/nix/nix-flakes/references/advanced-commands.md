# Advanced Flake Commands

## Additional flake commands

```bash
nix flake prefetch        # Fetch and compute hash without building
nix flake archive         # Copy flake + inputs to a store (for offline use)
nix flake clone           # Clone flake source to local directory
nix flake init -t <template>  # Initialize from specific template
```

## nix profile management (advanced)

```bash
nix profile history              # Show profile generations
nix profile diff-closures        # Compare two profile generations
nix profile wipe-history         # Delete old profile generations
```

**WARNING**: `nix profile` and `nix-env` are incompatible. Do not mix them on the same profile — they use
different internal formats.

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
3. `defaultPackage.<system>.package` (deprecated)

## Output selection syntax

```bash
nix build .#package^*      # Build all outputs (out, dev, doc, etc.)
nix build .#package^out    # Build specific output
nix build .#package^dev    # Build dev output only
```

## Key flags (additional)

| Flag                             | Effect                                        |
| -------------------------------- | --------------------------------------------- |
| `--inputs-from <flake>`          | Use another flake's lock file inputs          |
| `--print-out-paths`              | Print resulting store paths to stdout         |
| `--no-update-lock-file`          | Don't update lock file even if inputs changed |
| `--override-flake <input> <url>` | Override flake input at eval time             |
