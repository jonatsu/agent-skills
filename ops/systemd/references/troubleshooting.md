# Troubleshooting and Diagnostics

Sources: `systemd-analyze(1)`, `systemctl(1)`, `systemd.exec(5)` (exit-code appendix), `systemd(1)`
(unit-state concepts) — fetched via man.archlinux.org (bot-accessible mirror of the freedesktop.org "latest"
man pages) and cross-verified against systemd's own source (`src/shared/exit-status.h`,
`src/core/transaction.c`) for exact numeric tables and log message strings, since DocBook→markdown conversion
tends to lose table columns. Cross-checked against ArchWiki "Systemd" troubleshooting sections.

## Contents

1. Reading unit state: LOAD / ACTIVE / SUB
2. `systemctl status` anatomy
3. masked vs disabled vs static vs enabled
4. Ordering cycles
5. `systemd-analyze verify`
6. Boot performance and dependency graphs
7. Troubleshooting decision tree
8. systemctl exit codes for scripting

## 1. Reading unit state correctly: LOAD / ACTIVE / SUB

Every unit has three independent state fields shown by `systemctl list-units`, `systemctl status`, and
`systemctl show`. Checking only `ACTIVE` (or only "is it green") misses real failures.

```
UNIT                         LOAD   ACTIVE SUB     DESCRIPTION
sys-module-fuse.device       loaded active plugged /sys/module/fuse
systemd-journald.service     loaded active running Journal Service
● user@1000.service          loaded failed failed  User Manager for UID 1000
```

- **LOAD** — whether the unit *definition* was parsed successfully: `loaded`, `not-found` (no unit file exists
  under that name — typo or package not installed), `bad-setting` (an essential directive couldn't be parsed),
  `error` (some other load error), `masked` (symlinked to `/dev/null`, see §3).
- **ACTIVE** — the generalized runtime state: `active`, `inactive`, `failed`, `activating`, `deactivating`,
  `maintenance` (inactive + a maintenance op in progress), `reloading` (active + reloading config),
  `refreshing` (active + a new mount is being activated in its namespace).
- **SUB** — a low-level, unit-type-specific state; values vary by type. Common examples: services — `running`,
  `dead`, `exited`, `failed`, `auto-restart`; mounts — `mounted`, `mounting`, `dead`; devices — `plugged`,
  `dead`, `tentative`; sockets — `listening`, `running`, `dead`; timers — `waiting`, `running`, `elapsed`;
  targets — `active`, `dead`.

Read the triple together, not `ACTIVE` alone:

| Triple                    | Meaning                                                                                                                                                                                          |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `loaded/active/running`   | Normal healthy service.                                                                                                                                                                          |
| `loaded/failed/failed`    | Unit file is fine, but the unit **ran and failed**: non-zero exit, crash, timeout, or exceeded `StartLimitBurst=`. Always check `systemctl status` and `journalctl -xeu` next.                   |
| `not-found/inactive/dead` | No unit file was ever found under this name — likely a typo, a package that isn't installed, or a unit defined only for a template you didn't instantiate (`foo@.service` vs `foo@bar.service`). |
| `masked/inactive/dead`    | Explicitly disabled via symlink to `/dev/null`; distinct from `not-found` — the admin (or a dependency) intentionally blocked it. `systemctl start` fails with "Unit is masked."                 |
| `loaded/activating/start` | Mid-startup; check again shortly or watch with `systemctl status` / `journalctl -f`.                                                                                                             |

systemd only keeps units with active/activating/deactivating/failed state (or a live dependency/resource)
resident in memory; anything else is unloaded and reloaded on demand — "not currently loaded" does **not** by
itself mean "doesn't exist."

## 2. systemctl status <unit> anatomy

```
$ systemctl status bluetooth
● bluetooth.service - Bluetooth service
   Loaded: loaded (/usr/lib/systemd/system/bluetooth.service; enabled; preset: enabled)
   Active: active (running) since Wed 2017-01-04 13:54:04 EST; 1 weeks 0 days ago
     Docs: man:bluetoothd(8)
 Main PID: 930 (bluetoothd)
   Status: "Running"
    Tasks: 1
   Memory: 648.0K
      CPU: 435ms
   CGroup: /system.slice/bluetooth.service
           └─930 /usr/lib/bluetooth/bluetoothd
```

- **`Loaded:`** — repeats LOAD state as a word, the unit file path, and the enablement state
  (`enabled`/`disabled`/`static`/… — see §3) plus the applicable preset.
- **`Active:`** — repeats ACTIVE state plus a parenthesized SUB state and a timestamp of the last transition.
- **`Main PID:`** — the tracked primary process. Absent/changed unexpectedly is itself a signal (e.g. a
  forking service that never wrote its PID file).
- **`Process:` lines** appear for a failed/completed unit and show each `Exec*=` command that ran, with its
  outcome:
  - `(code=exited, status=1/FAILURE)` — process called `exit(1)`. The `/NAME` suffix decodes the numeric
    status against systemd's own table (§8) — `1/FAILURE` is generic; `2/INVALIDARGUMENT` … `7/NOTRUNNING` are
    LSB-class codes; `200/CHDIR` … `246/MEMORY_THP` mean **systemd itself** failed to set up the execution
    environment before your binary ever ran (e.g. `203/EXEC` = executable missing/not executable, `216/GROUP`
    = configured `Group=` doesn't exist).
  - `(code=killed, signal=SEGV)` — process was terminated by a signal and did **not** dump core.
  - `(code=dumped, signal=SEGV)` — terminated by a signal **and** dumped core.
  - `(code=exited, status=0/SUCCESS)` — clean exit; shown for `ExecStartPre=`/etc. in verbose contexts.

Interpretation shortcut: `code=exited` + high 200+ status ⇒ **configuration/sandboxing problem** (fix the unit
file, not the app). `code=killed`/`code=dumped` ⇒ **the program itself crashed** (look at core dumps,
`coredumpctl`, application logs). `code=exited` + low status (1–7, or an app-specific code) ⇒
**application-level failure** — read its stdout/stderr in the journal.

By default only the last 10 log lines are shown; use `--lines=`/`--full`, or prefer `journalctl -u <unit>` /
`journalctl -xeu <unit>` for the complete picture — `status` is meant for humans, not scripting (use `show`
for parseable properties).

## 3. masked vs disabled vs static vs enabled

These answer "will this unit start on boot/via triggers," not "is it running now." Reported by
`systemctl is-enabled <unit>` and `systemctl list-unit-files`.

| State                       | Meaning                                                                                                                                                                                                         | `is-enabled` exit code |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| `enabled`                   | Symlinked in per its `[Install]` section (permanently, in `/etc/systemd/system/…wants/`)                                                                                                                        | 0                      |
| `enabled-runtime`           | Same, but symlink only under `/run/` — lost on reboot                                                                                                                                                           | 0                      |
| `static`                    | No `[Install]` section at all — **cannot** be enabled/disabled, only started directly or pulled in as a dependency                                                                                              | 0                      |
| `alias`                     | Unit name is a symlink alias to another unit                                                                                                                                                                    | 0                      |
| `indirect`                  | Not enabled itself, but has a non-empty `Also=` naming other units that are, or an alias not covered by `Also=`                                                                                                 | 0                      |
| `generated`                 | Created dynamically by a generator (`systemd.generator(7)`); cannot be enabled directly                                                                                                                         | 0                      |
| `transient`                 | Created at runtime via the API; cannot be enabled                                                                                                                                                               | 0                      |
| `disabled`                  | Has an `[Install]` section but no symlinks exist — can be enabled                                                                                                                                               | >0                     |
| `linked` / `linked-runtime` | Symlinked in from *outside* the standard unit search path                                                                                                                                                       | >0                     |
| `masked` / `masked-runtime` | Symlinked to `/dev/null` (permanently under `/etc/systemd/system/`, or transiently under `/run/systemd/system/`) — **prevents all activation**, manual and dependency-triggered alike; stronger than `disabled` | >0                     |
| `not-found`                 | Unit file doesn't exist                                                                                                                                                                                         | 4                      |

Key distinctions:

- **`disabled` vs `static`**: both won't auto-start, but only `disabled` can be turned on with plain `enable`;
  `static` units have nothing to hook — enabling them is a no-op/error. A unit becomes `static` by omission
  (no `[Install]`), not by an admin action.
- **`masked` vs `disabled`**: `disabled` still allows the unit to be pulled in as someone else's dependency;
  `masked` blocks that too — it's the strongest "off" switch. `systemctl mask` creates the `/dev/null`
  symlink; `systemctl unmask` removes it. Enabling a masked unit is an error until unmasked.
- List currently masked units: `systemctl list-unit-files --state=masked`.
- `enable` only creates the `[Install]`-declared symlinks; it does **not** start the unit (combine with
  `--now`). `disable` removes symlinks and reloads config, but does not stop the unit (combine with `--now` or
  a separate `stop`).

## 4. Ordering cycles

systemd resolves `Requires=`/`Wants=`/`After=`/`Before=` into a job **transaction** before executing it, and
verifies the transaction is cycle-free. If it isn't, systemd tries to break the cycle automatically by
deleting non-essential jobs from the transaction rather than failing outright.

Verbatim log messages (from systemd's transaction engine, `src/core/transaction.c`):

```
Found ordering cycle
Job foo.service/start deleted to break ordering cycle starting with bar.service/start
```

Look for these in `journalctl -b` around boot, or in `systemd-analyze dump`. Because systemd silently drops a
job to break the loop, the practical symptom is usually **not** a hard boot failure but a unit that
mysteriously never starts (its start job got deleted) — cross-check with `systemctl list-jobs` and unit `SUB`
state.

Common causes:

- Circular `Requires=`/`After=` between two units (`A After=B` + `B After=A`), often introduced by a drop-in
  that adds an ordering dependency without checking the target's own ordering.
- `Wants=`/`Requires=` do **not** imply `After=`; conversely a stray `Before=`/`After=` pair pointing both
  ways across a chain of 3+ units.
- Generator-produced units (mount/fstab-derived) interacting with hand-written units that weren't designed
  with the generated ordering in mind.

Fix by breaking the cycle explicitly — decide which relationship is truly required vs. merely ordered, and
drop the redundant `After=`/`Before=` rather than relying on systemd's automatic (and somewhat arbitrary)
cycle-breaking choice.

## 5. systemd-analyze verify — the standard "did I write this unit correctly" check

Run this before deploying any new or edited unit file. It loads the unit(s) without starting them and prints
warnings/errors for: unknown sections and directives (typos in key names), missing dependencies, man pages
listed in `Documentation=` that don't exist, and commands in `ExecStart=`/etc. that don't exist or aren't
executable.

```
$ systemd-analyze verify ./myservice.service
[./myservice.service:9] Unknown lvalue 'WhatIsThis' in section 'Unit'
[./myservice.service:13] Unknown section 'Srevice'. Ignoring.
Error: org.freedesktop.systemd1.LoadFailed:
   Unit different.service failed to load:
   No such file or directory.
Failed to create user.slice/start: Invalid argument
myservice.service: man nosuchfile(1) command failed with code 16.
```

Treat this as a required gate, equivalent to a linter/typecheck: run it on any unit file generated or edited,
before `daemon-reload` + `start`. It does not catch semantic/logic errors (e.g. a working `ExecStart=`
pointing at the wrong binary) — only structural/reference errors.

## 6. Boot performance and dependency graphs

- **`systemd-analyze blame`** — units ordered by time-to-initialize, useful for finding what's slow:

```
         32.875s pmlogger.service
         20.905s systemd-networkd-wait-online.service
         13.299s dev-vda1.device
            23ms sysroot.mount
             3ms sys-kernel-config.mount
```

Caveat: this only reflects units that ran serially relative to something else; it does not by itself show the
*critical path* (a slow unit off the critical path doesn't delay boot).

- **`systemd-analyze critical-chain [UNIT]`** — the actual time-critical dependency chain that delayed
  reaching the target (default `default.target`, or a given unit):

```
multi-user.target @47.820s
└─pmie.service @35.968s +548ms
  └─pmcd.service @33.715s +2.247s
    └─network-online.target @33.712s
      └─systemd-networkd-wait-online.service @12.804s +20.905s
        └─systemd-networkd.service @11.109s +1.690s
```

`@X` = time the unit became active; `+Y` = time it took. This is the tool to identify what to actually
optimize — `blame` alone can mislead by highlighting slow-but-parallel units.

- **`systemd-analyze dot [PATTERN...]`** — emits a Graphviz `dot` dependency graph (`Requires=`/`After=`/etc.
  edges) for matching units, to render and inspect visually:

```
$ systemd-analyze dot 'avahi-daemon.*' | dot -Tsvg > avahi.svg
```

Useful for untangling ordering-cycle or "why did this pull in that" questions interactively rather than by
reading unit files by hand.

- **`systemd-analyze plot > bootup.svg`** — SVG timeline of the whole boot, same underlying data as
  `blame`/`critical-chain` visualized.
- **`systemd-analyze cat-config <name>`** — dumps a config file plus every drop-in overlaid on it, in
  effective order — the fastest way to check "what configuration is actually in effect" when drop-ins are
  involved.
- **`systemd-analyze unit-paths`** — lists every directory systemd will search for unit files/drop-ins, useful
  when a unit "isn't found" and search-path precedence needs checking.

## 7. Troubleshooting decision tree: "service won't start"

Work top to bottom; each step either resolves it or narrows where to look next.

01. **`systemctl status <unit>`** — read LOAD/ACTIVE/SUB (§1) and any `Process:` exit-code line (§2) first.
    This alone often identifies the failure class (config vs. crash vs. app-level).
02. **`journalctl -xeu <unit>`** — full logs plus systemd's own explanatory context (`-x` adds catalog
    explanations for known message IDs). For short-lived processes that log nothing under their unit name,
    fall back to `journalctl _PID=<pid>` using the PID reported by `status` (see
    `references/journald-and-logging.md` §4).
03. **`systemd-analyze verify <unit-file>`** — rule out structural errors: unknown directives, bad references,
    missing `ExecStart=` (§5).
04. **Check `ExecStart=`'s path** exists and is executable (`test -x`). A missing/non-executable binary
    surfaces as `code=exited, status=203/EXEC`.
05. **Check `User=`/`Group=`** actually exist on the system — surfaces as `status=216/GROUP` or
    `status=217/USER`.
06. **Check `WorkingDirectory=`** exists — surfaces as `status=200/CHDIR`.
07. **Check SELinux/AppArmor** if enforced on the host — a silently-denied syscall/file access can look
    identical to a generic crash or permission error; check `journalctl -k` / `ausearch`/`aa-status` alongside
    the unit's own logs.
08. **Confirm `systemctl daemon-reload` was run** after any unit-file edit — a stale in-memory unit definition
    is one of the most common "I fixed it but it still fails the same way" traps.
09. **Ordering/dependency issues** — if the unit never even attempts to start, check `systemctl list-jobs` and
    `journalctl -b | grep -i "ordering cycle"` (§4), and confirm the units it depends on
    (`After=`/`Requires=`) are themselves active.
10. **Rate-limited restarts** — a unit that keeps failing and restarting can hit
    `StartLimitBurst=`/`StartLimitIntervalSec=` and refuse to start again with "start request repeated too
    quickly"; `systemctl reset-failed <unit>` clears the counters before retrying.

## 8. systemctl exit codes for scripting

`systemctl` follows **LSB 3.0.0** return codes for status-style commands (`status` used as an LSB init-script
wrapper, `is-active`, `is-failed`):

| Code | LSB meaning                                     | systemctl semantics                                                     |
| ---- | ----------------------------------------------- | ----------------------------------------------------------------------- |
| 0    | "program is running or service is OK"           | unit is active                                                          |
| 1    | "program is dead, `/var/run` pid file exists"   | unit **not** failed (the code `is-failed` returns for "nothing failed") |
| 2    | "program is dead, `/var/lock` lock file exists" | unused by systemd                                                       |
| 3    | "program is not running"                        | unit is not active                                                      |
| 4    | "program or service status is unknown"          | no such unit                                                            |

Practical rules: `systemctl is-active <unit>` → 0 if active, non-zero otherwise. `systemctl is-failed <unit>`
→ 0 if the unit is in `failed` state, non-zero otherwise. `systemctl is-enabled <unit>` uses its **own**
distinct code set (§3), not this LSB table — don't conflate the two when scripting. The LSB↔systemd state
mapping is imperfect: prefer checking specific `ACTIVE`/`SUB` values (via
`systemctl show -p ActiveState,SubState`) over relying on raw exit codes for anything beyond simple
active/inactive gating.

Process/service exit-status codes (what shows up after `status=` in `status` output and `$EXIT_STATUS` in
`OnFailure=` handlers), authoritative numbering from systemd's own source (`src/shared/exit-status.h`):

- **C library**: `0` `EXIT_SUCCESS`, `1` `EXIT_FAILURE`.
- **LSB** (`2`–`7`): `2` `EXIT_INVALIDARGUMENT`, `3` `EXIT_NOTIMPLEMENTED`, `4` `EXIT_NOPERMISSION`, `5`
  `EXIT_NOTINSTALLED`, `6` `EXIT_NOTCONFIGURED`, `7` `EXIT_NOTRUNNING`.
- **systemd-specific** (`200`–`246`, two slots — `223`, `234` — are historical placeholders now unused): `200`
  `EXIT_CHDIR`, `201` `EXIT_NICE`, `202` `EXIT_FDS`, `203` `EXIT_EXEC`, `204` `EXIT_MEMORY`, `205`
  `EXIT_LIMITS`, `206` `EXIT_OOM_ADJUST`, `207` `EXIT_SIGNAL_MASK`, `208` `EXIT_STDIN`, `209` `EXIT_STDOUT`,
  `210` `EXIT_CHROOT`, `211` `EXIT_IOPRIO`, `212` `EXIT_TIMERSLACK`, `213` `EXIT_SECUREBITS`, `214`
  `EXIT_SETSCHEDULER`, `215` `EXIT_CPUAFFINITY`, `216` `EXIT_GROUP`, `217` `EXIT_USER`, `218`
  `EXIT_CAPABILITIES`, `219` `EXIT_CGROUP`, `220` `EXIT_SETSID`, `221` `EXIT_CONFIRM`, `222` `EXIT_STDERR`,
  `224` `EXIT_PAM`, `225` `EXIT_NETWORK`, `226` `EXIT_NAMESPACE`, `227` `EXIT_NO_NEW_PRIVILEGES`, `228`
  `EXIT_SECCOMP`, `229` `EXIT_SELINUX_CONTEXT`, `230` `EXIT_PERSONALITY`, `231` `EXIT_APPARMOR_PROFILE`, `232`
  `EXIT_ADDRESS_FAMILIES`, `233` `EXIT_RUNTIME_DIRECTORY`, `235` `EXIT_CHOWN`, `236`
  `EXIT_SMACK_PROCESS_LABEL`, `237` `EXIT_KEYRING`, `238` `EXIT_STATE_DIRECTORY`, `239`
  `EXIT_CACHE_DIRECTORY`, `240` `EXIT_LOGS_DIRECTORY`, `241` `EXIT_CONFIGURATION_DIRECTORY`, `242`
  `EXIT_NUMA_POLICY`, `243` `EXIT_CREDENTIALS`, `244` `EXIT_BPF`, `245` `EXIT_KSM`, `246` `EXIT_MEMORY_THP`.
- **`255`**: `EXIT_EXCEPTION` — systemd's own marker for propagating an abnormal/signal exit, mirroring bash
  convention.

All codes ≥200 mean **systemd failed to prepare the exec environment**, before your program's `execve()` ever
ran — the fault is in the unit file / host environment (missing user, bad directory, resource limits), never
in the application. Signal-based termination is reported separately as
`code=killed`/`code=dumped, signal=<NAME>` rather than as a `status=` number.
