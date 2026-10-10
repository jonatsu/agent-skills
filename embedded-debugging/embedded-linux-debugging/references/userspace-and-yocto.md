# Userspace Debugging and Yocto Debug Symbols

Checked 2026-09-30 against the GDB 18.1 manual, Linux v7.2's sysctl documentation, systemd v262, and the Yocto
Project 6.0 "Wrynose" manuals and OpenEmbedded-Core. GDB commands themselves belong to `gdb-debugging`.

## Contents

- gdbserver
- Core dumps
- Yocto: getting symbols onto the host
- Yocto: features that changed

## gdbserver

Use cross-GDB with the exact executable and matching target libraries and debug information. Set its sysroot to the
matching development or debug tree; a sysroot supplies file lookup, and it cannot create debug symbols absent from
those files.

Prefer gdbserver over an authenticated SSH stdio transport when the target supports it:

```text
(gdb) file /path/to/matching/unstripped/myapp
(gdb) set sysroot /path/to/matching/target-sysroot
(gdb) target remote | ssh -T board gdbserver --once stdio /usr/local/bin/myapp
(gdb) continue
```

Use a trusted SSH alias and an appropriate target user; a program started this way gets `/dev/null` for standard
input. For attaching or multi-process sessions, use `gdbserver --attach` or `--multi`, and end the session explicitly.
Check whether the process should resume or terminate; `disconnect` performs no recovery.

gdbserver has no built-in authentication. If TCP is necessary, establish real firewall or network isolation before
opening the listener, and verify its addresses. The host part of gdbserver's `host:port` argument is ignored, so
writing `localhost` there is not a loopback security control. Close the listener after use.

## Core Dumps

- `/proc/sys/kernel/core_pattern` names the file (default `core`, with `%p`, `%e`, `%t` and other specifiers), or, when
  it starts with `|`, a program that receives the dump on standard input.
- The dump is written only if the process's core limit allows it: `ulimit -c unlimited` in the shell that starts it,
  or `LimitCORE=` for a systemd service.
- With systemd, `systemd-coredump` owns the pattern and stores dumps in `/var/lib/systemd/coredump/`. On kernels 6.19
  and newer it uses the kernel's coredump socket instead of a pipe. On small flash, set `Storage=none` or a small
  `ExternalSizeMax=` in `coredump.conf`.
- `coredumpctl list` shows dumps; `coredumpctl dump -o core.bin <match>` extracts one; `coredumpctl debug` starts GDB,
  but on the board itself.
- For a cross-built target, copy the dump to the host and open it there with the cross GDB, the matching ELF, and
  `set sysroot` pointing at the image's debug sysroot (below).

## Yocto: Getting Symbols Onto the Host

Four routes, from quickest to most complete:

- **Debug filesystem.** In `local.conf`, `IMAGE_GEN_DEBUGFS = "1"` and `IMAGE_FSTYPES_DEBUGFS = "tar.bz2"` build a
  companion `<image>-dbg.rootfs.tar.bz2` holding the `-dbg` and `-src` packages. It is a fragment, so unpack the image's
  rootfs and then the `-dbg` tarball into one `debugfs` directory. On the host:
  `set sysroot debugfs`, `set substitute-path /usr/src/debug debugfs/usr/src/debug`, then connect.
  `IMAGE_CLASSES += "image-combined-dbg"` makes the build combine them.
- **SDK.** `bitbake <image> -c populate_sdk` builds an SDK whose target sysroot already carries `dbg-pkgs` and
  `src-pkgs`. Sourcing its `environment-setup-*` script sets `$GDB` to the matching cross debugger; point
  `set sysroot` at `$SDKTARGETSYSROOT`.
- **debuginfod.** With the `debuginfod` distro feature (on by default in OE-Core and Poky), run `oe-debuginfod` on the
  build host (port 8002) and set `DEBUGINFOD_URLS="http://<host>:8002/"` on the target or host; GDB then fetches debug
  info on demand.
- **devtool.** `devtool modify <recipe> --debug-build`, then
  `devtool ide-sdk <recipe> <image> --target root@<board>`, generates deploy scripts and a debugger configuration for
  one recipe.

`EXTRA_IMAGE_FEATURES:append = " tools-debug"` puts `gdbserver` on the image. `dbg-pkgs` installs debug symbols on the
target itself, which costs flash; prefer the host-side routes on small images. The symbols must come from the same
build as the running image.

## Yocto: Features That Changed

- `tools-debug` installs `gdb`, `gdbserver`, `strace`, and, with glibc, `libc-mtrace`; not `ltrace`, which is in
  meta-oe.
- `debug-tweaks` was removed in Yocto 5.2. It controlled only root login; the replacements are `allow-empty-password`,
  `allow-root-login`, `empty-root-password`, and `post-install-logging`. A layer still setting it names a feature that no
  longer exists.
- `src-pkgs` works through OE-Core's package globs but is not in the 6.0 manual.
- `PACKAGE_DEBUG_SPLIT_STYLE` defaults to `debug-with-srcpkg` (symbols in `-dbg`, sources in `-src`);
  `debug-file-directory` puts symbols under `/usr/lib/debug`, which some tools, such as `perf` on the target, expect.
