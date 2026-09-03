---
name: nix-packaging
description: "Nix packaging — create derivations for source or binary packages, handle library dependencies, autoPatchelfHook, overlays, and flake outputs. Use when packaging .deb/.rpm/.tar.gz/AppImage, writing mkDerivation, finding missing libraries, or creating overlays. Triggers on: nix package, derivation, mkDerivation, autoPatchelf, buildInputs, nativeBuildInputs, fetchurl, fetchFromGitHub, overlay, devShell, FHS, makeWrapper, nix-prefetch."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Nix Packaging

IRON LAW: ALWAYS SOURCE FROM THE ORIGINAL ARCHIVE — NEVER FROM PRE-EXTRACTED DIRECTORIES. PRE-EXTRACTED DIRS
LOSE METADATA, CHECKSUMS, AND REPRODUCIBILITY. THE `src` ATTRIBUTE MUST POINT TO A FETCHED ARCHIVE, NOT A
LOCAL DIRECTORY.

## Workflow

```text
Nix Packaging Progress:

- [ ] Step 1: Identify packaging type (binary vs source) ⚠️ REQUIRED
- [ ] Step 2: Gather source (fetchurl, fetchFromGitHub, etc.)
- [ ] Step 3: Write derivation
- [ ] Step 4: Handle dependencies
- [ ] Step 5: Test the package
- [ ] Step 6: Add to flake outputs / overlay
- [ ] Step 7: Verify ⚠️ REQUIRED
```

## Step 1: Identify Packaging Type ⚠️ REQUIRED

Determine whether the software is distributed as a pre-compiled binary or as source code.

- **Binary packaging**: `.deb`, `.rpm`, `.AppImage`, tarball with pre-built binaries, or a single
  statically-linked binary. Use `autoPatchelfHook` to fix library paths.
- **Source packaging**: Source tarball or git repository. Use the project's build system (meson, cmake, cargo,
  go, etc.).

⛔ BLOCKING: Do NOT proceed without confirming the packaging type. Binary and source derivations have
fundamentally different structures.

## Step 2: Gather Source

Fetch the original archive. NEVER use a pre-extracted directory.

```bash
# For arbitrary URLs
nix-prefetch-url --type sha256 https://example.com/file.deb

# For GitHub archives
nix-prefetch-url --unpack https://github.com/owner/repo/archive/v1.0.0.tar.gz
```

Common fetchers:

- `fetchurl` — any URL. Requires `url` and `hash`.
- `fetchFromGitHub` — GitHub repos. Requires `owner`, `repo`, `rev`, `hash`.
- `fetchzip` — zip archives. Auto-extracts.
- `fetchgit` — raw git repos. Use sparingly; prefer `fetchFromGitHub`.

MUST use `lib.fakeSha256` only during initial scaffolding. Replace with real hash before final delivery.

```nix
# For .zip archives, add unzip to nativeBuildInputs
nativeBuildInputs = [ unzip ];
```

## Step 3: Write Derivation

### Binary Packaging (.deb)

```nix
{ stdenv, lib, autoPatchelfHook, dpkg, fetchurl, gtk3, glib, stdenv.cc.cc.lib }:

stdenv.mkDerivation {
  pname = "example";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/example-${version}.deb";
    hash = lib.fakeSha256;  # replace after first build
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
}
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

stdenv.mkDerivation {
  pname = "example";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/example-${version}.x86_64.rpm";
    hash = lib.fakeSha256;
  };

  nativeBuildInputs = [ autoPatchelfHook rpm ];

  unpackPhase = ''
    rpm2cpio $src | cpio -idmv
  '';

  installPhase = ''
    mkdir -p $out
    cp -r usr/* $out/
  '';
}
```

### Simple Binary (no extraction needed)

```nix
stdenv.mkDerivation rec {
  pname = "tool";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/tool-${version}-linux-amd64";
    hash = lib.fakeSha256;
  };

  sourceRoot = ".";
  dontUnpack = true;

  installPhase = ''
    mkdir -p $out/bin
    cp $src $out/bin/tool
    chmod +x $out/bin/tool
  '';
}
```

### Source Packaging

```nix
{ stdenv, lib, fetchFromGitHub, meson, ninja, pkg-config, gtk3 }:

stdenv.mkDerivation {
  pname = "example";
  version = "1.0.0";

  src = fetchFromGitHub {
    owner = "owner";
    repo = "example";
    rev = "v${version}";
    hash = lib.fakeSha256;
  };

  nativeBuildInputs = [ meson ninja pkg-config ];
  buildInputs = [ gtk3 ];

  mesonFlags = [ "-Dexample=true" ];
}
```

```nix
# Use rec to reference version in src URL/filename
stdenv.mkDerivation rec {
  pname = "app";
  version = "1.0.0";
  src = ./app-${version}.tar.gz;  # rec allows version reference
}
```

### AppImage Packaging

For AppImage files, prefer `appimage-run` for execution, or extract and patch:

```nix
# Option 1: Run with appimage-run (no packaging needed)
nix-shell -p appimage-run --run "appimage-run ./app.AppImage"

# Option 2: Extract and package
stdenv.mkDerivation rec {
  pname = "app";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/app-${version}.AppImage";
    hash = lib.fakeSha256;
  };

  nativeBuildInputs = [ autoPatchelfHook ];

  unpackPhase = ''
    $src --appimage-extract
    cd squashfs-root
  '';

  installPhase = ''
    mkdir -p $out/bin $out/lib
    cp AppRun $out/bin/app
    cp -r usr/* $out/
  '';
}
```

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

See [references/library-mapping.md](references/library-mapping.md) for the complete library→package mapping
and debugging commands.

### makeWrapper Pattern

Use `makeWrapper` to wrap binaries with environment variables or extra PATH entries:

```nix
{ stdenv, lib, makeWrapper, gsettings-desktop-schemas, ... }:

stdenv.mkDerivation {
  # ...

  nativeBuildInputs = [ makeWrapper ];

  installPhase = ''
    install -Dm755 $src/bin/app $out/bin/app
    wrapProgram $out/bin/app \
      --prefix PATH : ${lib.makeBinPath [ pkgs.coreutils ]} \
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

## Step 7: Verify ⚠️ REQUIRED

⛔ BLOCKING: Do NOT deliver the derivation until ALL checks pass.

```bash
# Build must succeed
nix build .#package-name

# Binary must run without missing library errors
ldd result/bin/* | grep "not found"  # MUST return empty

# Flake check must pass
nix flake check
```

## FHS Escape Hatch (Last Resort)

Use `buildFHSUserEnv` ONLY when `autoPatchelfHook` cannot resolve dependencies (e.g., binaries that hardcode
`/usr/lib` paths or dlopen libraries at runtime):

```nix
{ buildFHSUserEnv }:

buildFHSUserEnv {
  name = "app-fhs";
  targetPkgs = pkgs: [ pkgs.app ];
  runScript = "app";
}
```

NEVER use FHS as the first approach. Always attempt `autoPatchelfHook` first.

## Module-System Wrappers (nix-wrapper-modules)

For a **configured** executable (baked-in flags/env/generated config) that stays portable across NixOS,
home-manager, nix-darwin, devshells, and plain shells, use BirdeeHub's
[nix-wrapper-modules](https://github.com/BirdeeHub/nix-wrapper-modules) instead of a hand-rolled wrapper. Full
workflow and API live in the dedicated **`nix-wrapper-modules` skill** — reach for it once wrapping needs
generated config or cross-environment portability rather than a one-off `makeWrapper`.

| Approach                      | Scope             | Portability                            |
| ----------------------------- | ----------------- | -------------------------------------- |
| `makeWrapper` + `symlinkJoin` | Single derivation | NixOS/HM only                          |
| `nix-wrapper-modules`         | Module system     | NixOS, HM, nix-darwin, devshell, shell |
| `buildFHSUserEnv`             | FHS sandbox       | Anywhere (heavy)                       |

## Unfree Packages

```nix
meta = {
  license = lib.licenses.unfree;
};
```

Users MUST enable unfree packages in their configuration to build.

## Anti-Patterns

- **Sourcing from pre-extracted directories** instead of original archives. Violates the IRON LAW. Always use
  `fetchurl`/`fetchFromGitHub`.
- **Using `autoPatchelfHook` without putting libraries in `buildInputs`**. `autoPatchelfHook` can only find
  libraries that are in `buildInputs`.
- **Mixing up `nativeBuildInputs` and `buildInputs`**. Build tools go in `nativeBuildInputs`; runtime
  libraries go in `buildInputs`.
- **Using `lib.fakeSha256` in final derivation**. Only for initial scaffolding. Replace with real hash before
  delivery.
- **Creating FHS environments when `autoPatchelfHook` would work**. FHS is a heavy escape hatch; try
  `autoPatchelfHook` first.
- **Hardcoding absolute store paths** instead of using package references (e.g., `${gtk3}/lib` not
  `/nix/store/abc-gtk3/lib`).
- **Forgetting to test with `ldd` for missing libraries**. A successful build does not guarantee a runnable
  binary.
- **Using `propagatedBuildInputs` when `buildInputs` suffices**. Only propagate when downstream consumers need
  the library at their build time.
- **Skipping `nix flake check`**. Broken flakes block users.
- **Not pinning `rev` in `fetchFromGitHub`**. Unpinned revisions break reproducibility.
- **Using `xorg.libxkbcommon` instead of `libxkbcommon`** — the correct package is `libxkbcommon`, not
  `xorg.libxkbcommon`.
- **Not using `rec` when version appears in `src`** — without `rec`, `version` is not in scope for `src`
  attribute.

## Pre-Delivery Checklist

- [ ] Source fetched from original archive (not pre-extracted directory)
- [ ] Hash is real (not `lib.fakeSha256`)
- [ ] Package added to flake outputs or overlay
- [ ] No hardcoded store paths (all references use `${pkg}` interpolation)
- [ ] `meta` block present with at minimum `license` and `description`
- [ ] `meta.platforms` set for multi-platform packages
- [ ] `meta.mainProgram` set if package has multiple binaries (for `nix run`)
