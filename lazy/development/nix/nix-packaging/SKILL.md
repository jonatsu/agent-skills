---
name: nix-packaging
description: "Package software for Nix as a derivation, from source or from a prebuilt .deb, .rpm, tarball, or AppImage. Use when writing or fixing a mkDerivation, fetching and hashing sources, sorting build and runtime dependencies, fixing a prebuilt binary's missing libraries, or wrapping a program with makeWrapper or an FHS environment. For flake structure and inputs, use nix-flakes."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Nix Packaging

For third-party software, point `src` at a fetcher over the original published archive or repository, with its
hash; a pre-extracted directory loses the checksum and reproducibility. A project's own flake may package its tree
with `src = ./.` or `lib.fileset`.

## Step 1: Identify Packaging Type

Decide binary or source from the artifact itself before writing the derivation; the two have different structures.

- **Binary packaging**: `.deb`, `.rpm`, `.AppImage`, tarball with pre-built binaries, or a single
  statically-linked binary. Use `autoPatchelfHook` to fix library paths.
- **Source packaging**: Source tarball or git repository. Use the project's build system (meson, cmake, cargo,
  go, etc.).

## Step 2: Gather Source

```bash
# For arbitrary URLs
nix-prefetch-url --type sha256 https://example.com/file.deb

# For GitHub archives
nix-prefetch-url --unpack https://github.com/owner/repo/archive/v1.0.0.tar.gz
```

Common fetchers:

- `fetchurl` — any URL. Requires `url` and `hash`.
- `fetchFromGitHub` — GitHub repos. Requires `owner`, `repo`, `rev`, `hash`. Pin `rev` to a tag or commit; a
  branch name moves and breaks reproducibility.
- `fetchzip` — zip archives. Auto-extracts.
- `fetchgit` — raw git repos. Use sparingly; prefer `fetchFromGitHub`.

Use `lib.fakeHash` only while scaffolding: the first build fails and prints the real hash, which replaces it.

```nix
# For .zip archives, add unzip to nativeBuildInputs
nativeBuildInputs = [ unzip ];
```

## Step 3: Write Derivation

### Binary Packaging (.deb)

```nix
{ stdenv, lib, autoPatchelfHook, dpkg, fetchurl, gtk3, glib }:

stdenv.mkDerivation (finalAttrs: {
  pname = "example";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/example-${finalAttrs.version}.deb";
    hash = lib.fakeHash;  # replace after first build
  };

  nativeBuildInputs = [ autoPatchelfHook dpkg ];
  buildInputs = [ stdenv.cc.cc.lib gtk3 glib ];

  unpackPhase = ''
    dpkg-deb -x $src .
  '';

  installPhase = ''
    mkdir -p $out
    cp -r usr/* $out/
  '';
})
```

```nix
# Alternative: use ar instead of dpkg-deb
unpackPhase = ''
  ar x $src
  tar xf data.tar.xz
'';
```

### Binary Packaging (.rpm)

```nix
{ stdenv, lib, autoPatchelfHook, rpm, fetchurl, ... }:

stdenv.mkDerivation (finalAttrs: {
  pname = "example";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/example-${finalAttrs.version}.x86_64.rpm";
    hash = lib.fakeHash;
  };

  nativeBuildInputs = [ autoPatchelfHook rpm ];

  unpackPhase = ''
    rpm2cpio $src | cpio -idmv
  '';

  installPhase = ''
    mkdir -p $out
    cp -r usr/* $out/
  '';
})
```

### Simple Binary (no extraction needed)

```nix
stdenv.mkDerivation (finalAttrs: {
  pname = "tool";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/tool-${finalAttrs.version}-linux-amd64";
    hash = lib.fakeHash;
  };

  dontUnpack = true;

  installPhase = ''
    mkdir -p $out/bin
    cp $src $out/bin/tool
    chmod +x $out/bin/tool
  '';
})
```

### Source Packaging

```nix
{ stdenv, lib, fetchFromGitHub, meson, ninja, pkg-config, gtk3 }:

stdenv.mkDerivation (finalAttrs: {
  pname = "example";
  version = "1.0.0";

  src = fetchFromGitHub {
    owner = "owner";
    repo = "example";
    rev = "v${finalAttrs.version}";
    hash = lib.fakeHash;
  };

  nativeBuildInputs = [ meson ninja pkg-config ];
  buildInputs = [ gtk3 ];

  mesonFlags = [ "-Dexample=true" ];
})
```

The `(finalAttrs: { ... })` argument form is `mkDerivation`'s fixpoint: `finalAttrs.version` refers to the
final attribute value, so it stays correct under `overrideAttrs`. Prefer it over `rec`, which binds early and
silently keeps the old value when overridden. A plain attrset has no `version` in scope at all, so `src` cannot
refer to it.

### AppImage Packaging

Use `appimageTools` — the canonical nixpkgs route. `wrapType2` handles extraction and bundles the common
runtime libraries:

```nix
{ lib, appimageTools, fetchurl }:

appimageTools.wrapType2 rec {
  pname = "app";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/app-${version}.AppImage";
    hash = lib.fakeHash;
  };

  # Libraries the app loads at runtime beyond appimageTools' defaults
  extraPkgs = pkgs: [ pkgs.libsecret ];
}
```

Need files from inside the image (`.desktop` entry, icons)? `appimageTools.extract { inherit pname version src; }`
yields the unpacked squashfs tree; copy from it in `extraInstallCommands`.

For a one-off run without packaging: `nix run nixpkgs#appimage-run -- ./app.AppImage`.

Let `appimageTools` do the extraction. Files in the Nix store are not executable, so a hand-written `unpackPhase`
that runs `$src --appimage-extract` fails.

### Electron Apps

See [references/electron-dependencies.md](references/electron-dependencies.md) for the complete Electron
runtime dependency list.

## Step 4: Handle Dependencies

### Dependency Categories

| Attribute               | When to use                                                                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `nativeBuildInputs`     | Tools needed at BUILD time only: compilers, code generators, `pkg-config`, `cmake`, `meson`, `makeWrapper`                                       |
| `buildInputs`           | Libraries needed at BUILD and RUN time: `gtk3`, `glib`, `mesa`, `openssl`                                                                        |
| `propagatedBuildInputs` | Libraries needed by consumers of this package at their build time. Use sparingly — only when headers or pkg-config files are required downstream |

`autoPatchelfHook` resolves only libraries listed in `buildInputs`, so put every library a prebuilt binary links
against there. Reference store content through package interpolation (`${gtk3}/lib`), never a literal
`/nix/store/...` path.

See [references/library-mapping.md](references/library-mapping.md) for the complete library→package mapping
and debugging commands. One frequent miss: the package is `libxkbcommon`, not `xorg.libxkbcommon`.

### makeWrapper Pattern

Use `makeWrapper` to wrap binaries with environment variables or extra PATH entries:

```nix
{ stdenv, lib, makeWrapper, coreutils, gsettings-desktop-schemas, ... }:

stdenv.mkDerivation {
  # ...

  nativeBuildInputs = [ makeWrapper ];

  installPhase = ''
    install -Dm755 $src/bin/app $out/bin/app
    wrapProgram $out/bin/app \
      --prefix PATH : ${lib.makeBinPath [ coreutils ]} \
      --set GSETTINGS_SCHEMA_DIR ${gsettings-desktop-schemas}/share/gsettings-schemas/${gsettings-desktop-schemas.name}
  '';
}
```

## Step 5: Test the Package

```bash
# Build the package
nix build .#package-name

# Quick smoke test in FHS environment (for binary packages)
nix-shell -p steam-run --run "steam-run result/bin/app"

# Check for missing libraries
ldd result/bin/app | grep "not found"

# Run the binary directly
./result/bin/app --help
```

```bash
# Debug autoPatchelf failures — check build log
nix log /nix/store/...-drv
# Or during build:
nix build .#package-name -L  # -L shows full build output
```

## Step 6: Add to Flake Outputs / Overlay

### Flake Parts (perSystem)

```nix
perSystem = { pkgs, ... }: {
  packages.example = pkgs.callPackage ./nix/example.nix { };
  packages.default = pkgs.callPackage ./nix/example.nix { };
};
```

### Overlay

```nix
overlays.default = final: prev: {
  example = final.callPackage ./nix/example.nix { };
};
```

## Binary Overlay Pattern

See [references/binary-overlay-pattern.md](references/binary-overlay-pattern.md) for the full
platform-specific binary overlay pattern with hash conversion.

## Step 7: Verify

Deliver the derivation once every item holds:

- [ ] `nix build .#package-name` succeeds.
- [ ] `ldd result/bin/* | grep "not found"` returns nothing; a successful build alone does not prove the binary
  runs.
- [ ] `nix flake check` passes.
- [ ] Every hash is real, not `lib.fakeHash`.
- [ ] The package is in the flake outputs or an overlay.
- [ ] `meta` has at least `license` and `description`, plus `platforms` for a multi-platform package and
  `mainProgram` when it ships several binaries (for `nix run`).

## FHS Escape Hatch (Last Resort)

Try `autoPatchelfHook` first. Use `buildFHSEnv` when it cannot resolve the dependencies, such as binaries that
hardcode `/usr/lib` paths or dlopen libraries at runtime:

```nix
{ buildFHSEnv }:

buildFHSEnv {
  name = "app-fhs";
  targetPkgs = pkgs: [ pkgs.app ];
  runScript = "app";
}
```

## Module-System Wrappers

`makeWrapper`/`symlinkJoin` wrap a single derivation, and the wrapping usually lives inside one NixOS or
home-manager config. When a **configured** executable (baked-in flags, env vars, generated config files) must
stay portable across NixOS, home-manager, nix-darwin, devshells, and plain `nix build`, a module-system
wrapper library such as BirdeeHub's
[nix-wrapper-modules](https://github.com/BirdeeHub/nix-wrapper-modules) is the better fit: it evaluates a
small module system per program and emits an ordinary derivation usable anywhere. Stay with `makeWrapper` for
a one-off env-var or PATH tweak; reach for a wrapper-module library once the wrapping needs generated config
or cross-environment reuse.

| Approach                      | Scope             | Portability                            |
| ----------------------------- | ----------------- | -------------------------------------- |
| `makeWrapper` + `symlinkJoin` | Single derivation | NixOS/HM only                          |
| `nix-wrapper-modules`         | Module system     | NixOS, HM, nix-darwin, devshell, shell |
| `buildFHSEnv`                 | FHS sandbox       | Anywhere (heavy)                       |

## Unfree Packages

```nix
meta = {
  license = lib.licenses.unfree;
};
```

Users must enable unfree packages in their configuration to build it. Under a flake, that means config passed to
`import nixpkgs`, because pure evaluation ignores `NIXPKGS_ALLOW_UNFREE` and `~/.config/nixpkgs/config.nix`.
See the `nix-flakes` skill for the mechanisms and the evaluation evidence.
