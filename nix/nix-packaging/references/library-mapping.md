# Common Library → Package Mapping

## Finding Missing Libraries

```bash
# Check what's missing after build
ldd result/bin/app | grep "not found"

# Find which nix package provides a library
nix-locate libGL.so.1

# Or build nix-index first
nix run nixpkgs#nix-index
nix-locate libGL.so.1
```

## Library → Package Table

| Library              | Nix package                              |
| -------------------- | ---------------------------------------- |
| `libGL.so.1`         | `mesa`                                   |
| `libgtk-3.so.0`      | `gtk3`                                   |
| `libglib-2.0.so.0`   | `glib`                                   |
| `libstdc++.so.6`     | `stdenv.cc.cc.lib`                       |
| `libcrypto.so`       | `openssl`                                |
| `libcurl.so`         | `curl`                                   |
| `libSDL2-2.0.so.0`   | `SDL2`                                   |
| `libX11.so.6`        | `xorg.libX11`                            |
| `libasound.so.2`     | `alsa-lib`                               |
| `libpulse.so.0`      | `libpulseaudio`                          |
| `libz.so.1`          | `zlib`                                   |
| `libssl.so`          | `openssl`                                |
| `libfreetype.so.6`   | `freetype`                               |
| `libfontconfig.so.1` | `fontconfig`                             |
| `libdbus-1.so.3`     | `dbus`                                   |
| `libxkbcommon.so.0`  | `libxkbcommon` (NOT `xorg.libxkbcommon`) |
| `libGL.so.1`         | `mesa` or `libglvnd`                     |
| `libnss3.so`         | `nss`                                    |
| `libnspr4.so`        | `nspr`                                   |
| `libasound.so.2`     | `alsa-lib`                               |
