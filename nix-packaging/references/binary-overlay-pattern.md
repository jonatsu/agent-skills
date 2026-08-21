# Binary Overlay Pattern

For platform-specific binary packages, create both packages and overlay output:

```nix
{ stdenv, lib, fetchurl, flake-utils, ... }:

flake-utils.lib.eachSystem [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ] (system:
  let
    pkgs = import nixpkgs { inherit system; };
    version = "1.0.0";

    sources = {
      "x86_64-linux" = {
        url = "https://example.com/tool-linux-amd64-v${version}";
        hash = lib.fakeSha256;
      };
      "aarch64-linux" = {
        url = "https://example.com/tool-linux-arm64-v${version}";
        hash = lib.fakeSha256;
      };
      "x86_64-darwin" = {
        url = "https://example.com/tool-darwin-amd64-v${version}";
        hash = lib.fakeSha256;
      };
      "aarch64-darwin" = {
        url = "https://example.com/tool-darwin-arm64-v${version}";
        hash = lib.fakeSha256;
      };
    };

    source = sources.${system} or (throw "Unsupported system: ${system}");

    toolPackage = stdenv.mkDerivation {
      pname = "tool";
      inherit version;
      src = fetchurl { inherit (source) url hash; };
      sourceRoot = ".";
      dontUnpack = true;
      installPhase = ''
        mkdir -p $out/bin
        cp $src $out/bin/tool
        chmod +x $out/bin/tool
      '';
      meta = with lib; {
        description = "Tool description";
        homepage = "https://example.com";
        license = licenses.unfree;
        platforms = builtins.attrNames sources;
      };
    };
  in {
    packages.default = toolPackage;
    packages.tool = toolPackage;
  }) // {
    overlays.default = final: prev: {
      tool = self.packages.${prev.system}.tool;
    };
  };
```

## Hash Conversion

```bash
# Get hash in base32, convert to SRI format
nix-prefetch-url --type sha256 https://example.com/file
nix hash to-sri --type sha256 <base32-hash>
```
