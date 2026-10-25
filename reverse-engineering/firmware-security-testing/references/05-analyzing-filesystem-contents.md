# OWASP FSTM stage 5: analyzing filesystem contents

Stage 5 reads the filesystem [stage 4][stage-4] extracted without executing anything in it, aiming for a list of\
configuration files, keys, and executables worth deeper attention in [stage 7][stage-7] onward, plus the boot process,\
running services, and default users. Distilled from [Tarlogic's stage 5 write-up][source] (part of the OWASP FSTM\
series).

## The boot process

Identifying the boot style first pays off disproportionately: studying it routinely surfaces the bulk of this stage's\
findings on its own. Three common Unix styles:

- **BSD**: runs `/etc/rc`, `/etc/rc.local`, `/etc/rc.conf`, and the scripts under `/etc/rc.d`.
- **System V**: common on embedded devices via BusyBox; reads `/etc/inittab` and runs the scripts it references from\
  `/etc/init.d`.
- **systemd**: the modern desktop/server default, uncommon on embedded devices; configured from `/etc/systemd/`.

Find which one applies by inspecting `/sbin/init` (or the kernel's `init=` argument, when present in the image; absent\
that string, the executable lives at `/sbin/init`): a symlink to `/bin/busybox` means BusyBox + System V, a symlink to\
`/lib/systemd/systemd` means systemd, and a plain ELF executable needs `file`, `strings`, and a disassembler (Ghidra,\
IDA) to work out.

Once the style is known, read the startup scripts it runs in order: the `init`/`rcS` script, anything it links or calls\
under `/etc/init.d`, and any script it sources for default configuration. A single pass through this chain routinely\
reveals: which services start automatically (a web server, `telnetd`, and similar), how `/etc/passwd` and `/etc/group`\
get populated (an empty root password is a common finding here), and default credentials baked into a sourced\
configuration script. The serial console's baud rate, if not already known from [stage 2][stage-2], often shows up in\
the kernel command line inside one of these same scripts (`console=ttyS1,115200n8`, for example).

## Searching for files of interest

After the boot-process pass, sweep the rest of the filesystem for anything not reached from the boot path: outdated or\
misconfigured servers, hardcoded or weakly stored credentials, default API services, update functionality, source and\
startup scripts, compiled executables. Priority locations:

| Path                                                                          | What it holds                           |
| ----------------------------------------------------------------------------- | --------------------------------------- |
| `/etc/passwd`, `/etc/shadow`, `/etc/group`                                    | Users, password hashes, groups          |
| `/etc/fstab`                                                                  | Mounted volumes and their configuration |
| `/etc/init.d`, `/etc/runlevels`, `/etc/inittab`                               | Startup scripts, if not already covered |
| `/bin`, `/sbin`, `/usr/bin`, `/usr/sbin`, `/usr/local/bin`, `/usr/local/sbin` | Executables and tools                   |
| `/etc`                                                                        | Remaining configuration                 |
| `/var/log`                                                                    | Logs                                    |
| `/root`, `/home`                                                              | User home directories                   |

`find` automates the rest by pattern: `.pem`/`.crt` for keys and certificates, `.conf` for configuration, `.sh` for\
scripts, executable-permission files, unlabeled `.bin` binaries, known web servers (`nginx`, `apache`), and\
remote-access daemons (`ssh`, `telnet`, `tftp`, `dropbear`). Inside configuration files, grep for the keywords `admin`,\
`pass`, `password`, `remote`, `key`; for the unsafe C functions `gets`, `strcpy`, `stpcpy`, `strcat`, `printf`,\
`sprintf`; and for URLs, IP addresses, or email addresses.

## Automation tools

Treat every tool below as a source of leads to verify manually, not a finished report.

- **[Firmwalker]** — a bash script that sweeps an extracted or mounted filesystem root for the\
  password/key/config/service patterns above: `./firmwalker filesystem_root`.
- **[FACT]** (the Firmware Analysis and Comparison Tool) — automates content identification, filesystem extraction,\
  key/certificate detection, and CWE weakness matching. Ships as a Docker image or install script; start with\
  `sudo ./start_all_installed_fact_components` and reach it on ports 5000/80.
- **[EMBA]** — a bash framework bundling filesystem extraction, static executable analysis, and known-vulnerability\
  identification; run with `sudo ./emba.sh -l ./log_file -f /firmware_image`. `EMBArk` adds a web UI for team use.

## References

Distilled from OWASP FSTM / Tarlogic: [OWASP FSTM, stage 5: Analyzing filesystem contents][source].

- [scriptingxss/owasp-fstm][owasp-fstm-repo] — the OWASP FSTM reference project this series is based on.
- [craigz28/firmwalker][firmwalker] — the Firmwalker automated filesystem sweep.
- [fkie-cad/FACT_core][fact] — the Firmware Analysis and Comparison Tool.
- [e-m-b-a/emba][emba] — the Embedded Analyzer framework.

[emba]: https://github.com/e-m-b-a/emba
[fact]: https://github.com/fkie-cad/FACT_core
[firmwalker]: https://github.com/craigz28/firmwalker
[owasp-fstm-repo]: https://github.com/scriptingxss/owasp-fstm
[source]: https://www.tarlogic.com/blog/owasp-fstm-analyzing-filesystem-contents/
[stage-2]: 02-obtaining-firmware.md
[stage-4]: 04-extracting-filesystem.md
[stage-7]: 07-dynamic-analysis.md
