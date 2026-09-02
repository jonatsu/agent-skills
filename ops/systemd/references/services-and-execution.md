# systemd.service: Execution Model

Source: `systemd.service(5)` (freedesktop.org "latest", mirrored via manpages.debian.org/unstable).

## Type=

| Type                                                 | "Started" is considered true when...                                                      | Pick when                                                                                                                                        |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `simple` (default if `ExecStart=` given, no `Type=`) | immediately after `fork()`, before `execve()` even runs                                   | Fire-and-forget; **`systemctl start` reports success even if the binary can't be exec'd** (missing `User=`, bad path, etc.)                      |
| `exec`                                               | after `fork()` **and** `execve()` both succeed                                            | Same shape as `simple` but you want real exec failures reflected as `start` failure                                                              |
| `forking`                                            | parent process exits (child continues as the real service)                                | Traditional double-forking daemons; pair with `PIDFile=`                                                                                         |
| `oneshot`                                            | process exits (implied default if neither `Type=` nor `ExecStart=` set)                   | One-off scripts/setup; add `RemainAfterExit=yes` or the unit shows "dead" immediately after running once                                         |
| `notify` / `notify-reload`                           | daemon sends `READY=1` via `sd_notify()`                                                  | Daemon supports the notify protocol; `notify-reload` additionally implements the `ExecReload=`-free reload handshake via `RELOADING=1`/`READY=1` |
| `dbus`                                               | daemon acquires its configured `BusName=` on the bus                                      | D-Bus-activatable services; implicit `Requires=`+`After=` on `dbus.socket`                                                                       |
| `idle`                                               | like `simple`, but actual exec is delayed until other active jobs finish (5s timeout cap) | Only to avoid console output interleaving — not a general ordering tool                                                                          |

Recommendation straight from the man page: prefer `exec` over bare `simple` for anything long-running, since
`simple` can silently "succeed" on a broken binary; use `notify`/`notify-reload`/`dbus` over `forking` when
the daemon supports it.

## Exec\* semantics

- Commands run in order given; a non-prefixed command that fails aborts the rest and fails the unit.

- `ExecStart=` only runs after all non-`-`-prefixed `ExecStartPre=` succeed.

- `ExecStop=` only runs if the service **actually started successfully**; if start failed/timed out,
  `ExecStop=` is skipped and only `ExecStopPost=` runs — so cleanup-on-failed-start belongs in
  `ExecStopPost=`, not `ExecStop=`.

- Prefixes (stackable) on any Exec\* command:

  | Prefix            | Effect                                                                                   |
  | ----------------- | ---------------------------------------------------------------------------------------- |
  | `-`               | Non-zero/abnormal exit of this command is not a failure                                  |
  | `@`               | Next token is passed as `argv[0]` instead of the real path                               |
  | `:`               | Skip environment-variable substitution for this command                                  |
  | `+`               | Run with full privileges — bypasses `User=`/`Group=`/namespacing for *this* command only |
  | `!`               | Like `+`, but only bypasses `User=`/`Group=`/`SupplementaryGroups=`                      |
  | `\|` (standalone) | Invoke `User=`'s default shell                                                           |

## Restart= and RestartSec

`Restart=no|on-success|on-failure|on-abnormal|on-watchdog|on-abort|always` (default `no`). `on-failure` is the
broadest useful policy — covers non-zero exit, signal death (excluding the 4 "clean" signals), timeouts, and
watchdog expiry. `Type=oneshot` rejects `always`/`on-success` outright (a clean one-shot exit is
definitionally not a restart trigger). `RestartSec=` (default **100ms**) is the delay before each restart
attempt; restart activity is still bounded by `StartLimitIntervalSec=`/`StartLimitBurst=` at the unit level —
hit that and systemd stops auto-restarting until `systemctl reset-failed` or the interval elapses.

## Timeouts

`TimeoutStartSec=` / `TimeoutStopSec=` both default to **90s**
(`DefaultTimeoutStartSec=`/`DefaultTimeoutStopSec=` in `system.conf`, same 90s for user managers). A
`notify`/`notify-reload` service can push past the start/stop timeout by repeating `EXTEND_TIMEOUT_USEC=...`.
Reload operations (`ExecReload=` or the `notify-reload` protocol) are bounded by `TimeoutStartSec=` too — a
hung reload fails and leaves the old config live, it does **not** kill the running service.

## User=/Group=, Environment=/EnvironmentFile=, WorkingDirectory=

- `EnvironmentFile=/path` — file must exist/be readable/parse or the **service fails to start**; prefix with
  `-` (`EnvironmentFile=-/path`) to make a missing/bad file silently ignored instead. Values from the file
  override `Environment=` set directly in the unit; later files win over earlier ones on conflicting keys.
- `WorkingDirectory=` defaults to `/` for system-manager services, or the invoking user's home dir for
  `--user` services; `WorkingDirectory=~` = the home dir of whoever `User=` names. Prefix with `-` to tolerate
  a missing directory instead of failing the start.
- `%h`/`%u`/`%U` specifiers resolve to the service-manager's own user, **not** the unit's `User=` — a common
  trap when writing generic template units (see `references/units-and-dependencies.md` §2 for the full
  specifier table).

## Minimal illustrative snippets

```ini
# Traditional forking daemon
[Unit]
Description=My Simple Daemon
[Service]
Type=forking
ExecStart=/usr/sbin/my-simple-daemon -d
[Install]
WantedBy=multi-user.target
```

```ini
# Notify-protocol service, hard dependency + ordering on a cache
[Unit]
Description=App Server
After=memcached.service
Requires=memcached.service
[Service]
Type=notify-reload
ExecStart=/usr/sbin/app-server
Restart=on-failure
RestartSec=2
EnvironmentFile=-/etc/default/app-server
[Install]
WantedBy=multi-user.target
```

## Version-specific naming note

Older systemd docs use `try-reload-or-restart`; current "latest" docs show `reload-or-try-restart`. Confirm
against the locally installed `systemctl --version` and its own `--help`/man page rather than assuming one
spelling.
