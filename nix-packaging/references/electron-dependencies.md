# Electron App Dependencies

Electron apps often need these runtime dependencies:

```nix
buildInputs = with pkgs; [
  stdenv.cc.cc.lib
  alsa-lib
  at-spi2-atk
  at-spi2-core
  cairo
  cups
  dbus
  expat
  gdk-pixbuf
  glib
  gtk3
  libdrm
  libxkbcommon
  mesa
  nspr
  nss
  pango
  pipewire
  systemd
  xorg.libX11
  xorg.libxcb
  xorg.libXcomposite
  xorg.libXdamage
  xorg.libXext
  xorg.libXfixes
  xorg.libXrandr
  xorg.libXrender
  xorg.libXtst
];
```
