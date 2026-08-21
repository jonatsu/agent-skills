# Namespaces

Namespaces create scoped aspect libraries under `den.ful.<name>`. They can be local, exported, or imported from upstream flakes.

## Creating a Namespace

```nix
# modules/namespace.nix
{ inputs, den, ... }: {
  # Local namespace (not exported)
  imports = [ (inputs.den.namespace "my" false) ];

  # Exported namespace (available via flake.denful.eg)
  imports = [ (inputs.den.namespace "eg" true) ];
}
```

This creates:
- `den.ful.eg` — the namespace attrset (aspects type)
- `eg` — a module argument alias to `den.ful.eg`
- `flake.denful.eg` — flake output (if exported)

## Populating a Namespace

```nix
# Define aspects under the namespace
{ eg, ... }: {
  eg.vim = { homeManager.programs.vim.enable = true; };
  eg.desktop = {
    includes = [ eg.vim ];
    nixos.services.xserver.enable = true;
  };
}
```

## Using Namespaced Aspects

```nix
{ eg, ... }: {
  den.aspects.laptop.includes = [ eg.desktop eg.vim ];
}
```

## Importing from Upstream

```nix
{ inputs, ... }: {
  # Merge "shared" namespace from upstream flakes
  imports = [ (inputs.den.namespace "shared" [ inputs.team-config ]) ];

  # Merge AND export
  imports = [ (inputs.den.namespace "shared" [ inputs.team-config true ]) ];
}
```

## Angle Bracket Syntax

Once `__findFile` is enabled, namespace paths resolve through `<namespace/path>`:

```nix
{ __findFile, ... }: {
  den.aspects.laptop.includes = [ <eg/desktop> ];
}
```
