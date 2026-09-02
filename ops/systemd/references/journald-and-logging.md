# Journald and Logging

Sources: `systemd-journald.service(8)`, `journald.conf(5)`, `journalctl(1)` (freedesktop.org, systemd latest),
cross-checked against ArchWiki `Systemd/Journal`.

## Contents

1. `journald.conf` key directives
2. Making the journal persistent
3. `journalctl` essential filters
4. Correlating a failed service with its logs
5. Structured logging (brief)

## 1. journald.conf key directives

All options live in the `[Journal]` section of `/etc/systemd/journald.conf` (or drop-ins under
`/etc/systemd/journald.conf.d/*.conf`, which take precedence; `/run/systemd/journald.conf.d/`; vendor drop-ins
under `/usr/lib/systemd/journald.conf.d/`).

- **`Storage=`** — `volatile` (memory only, `/run/log/journal/`), `persistent` (disk-preferred,
  `/var/log/journal/`, falls back to volatile if `/var/` isn't writable yet), `auto` (behaves like
  `persistent` if `/var/log/journal/` already exists, else `volatile` — existence of the directory, not the
  setting, decides), `none` (drop everything; forwarding targets like console/syslog still work). Compiled-in
  default is `persistent`. Journald always *starts* on volatile storage and switches over on
  `journalctl --flush` (or `SIGUSR1`), which `systemd-journal-flush.service` triggers automatically at boot.
- **`Compress=`** — boolean (default **on**); can also take a byte threshold (default 512 bytes) below which
  objects aren't compressed.
- **`SystemMaxUse=`/`RuntimeMaxUse=`** — disk-space ceiling for `/var/log/journal` and `/run/log/journal`
  respectively. Default ~10% of the filesystem, capped at 4G. Paired with `SystemKeepFree=`/`RuntimeKeepFree=`
  (default ~15%, also capped at 4G) — journald honors whichever of the two (max-use vs keep-free) is smaller.
  Only *archived* files are deleted to reclaim space; the active file is never truncated, so actual usage can
  exceed the configured cap until rotation happens.
- **`SystemMaxFileSize=`/`RuntimeMaxFileSize=`** — per-file rotation size, default 1/8 of the corresponding
  MaxUse, capped at 128M (or 4G if journal "compact mode" is active).
- **`SystemMaxFiles=`/`RuntimeMaxFiles=`** — cap on number of archived files kept (default 100).
- **`MaxFileSec=`** (default 1 month) — time-based rotation regardless of size; `0` disables.
- **`MaxRetentionSec=`** (default **0** = off) — deletes journal files containing only entries older than this
  span; use to enforce a hard retention policy independent of disk-space pressure. Accepts unit suffixes
  `year`/`month`/`week`/`day`/`h`/`m`.
- **`ForwardToSyslog=`/`ForwardToKMsg=`/`ForwardToConsole=`/`ForwardToWall=`/`ForwardToSocket=`** — booleans
  (address for the socket variant) controlling live forwarding. Only `ForwardToWall=` defaults on.
  `ForwardToConsole=` is synchronous within journald and can block it if the console (e.g. a slow cloud serial
  port) hangs — prefer `journalctl -f` redirected to console for production instead.
- **`RateLimitIntervalSec=`/`RateLimitBurst=`** (default 30s / 10000) — per-service burst limiter; excess
  messages in the window are dropped with a summary message. The effective burst scales up with more free
  filesystem space (up to 6x at ≤1TB free). A service can override this for itself via
  `LogRateLimitIntervalSec=`/`LogRateLimitBurst=` in its unit's `[Service]` section.
- **`SplitMode=`** (`uid`/`none`, default `uid`) — whether regular users get their own per-UID journal files
  (enables unprivileged `journalctl --user` access); only applies to persistent storage.

## 2. Making the journal persistent

Default behavior: if `/var/log/journal/` doesn't exist, journald logs to `/run/log/journal/` only — logs are
lost on reboot. To opt in permanently:

```
# mkdir -p /var/log/journal
# systemd-tmpfiles --create --prefix /var/log/journal
```

The `systemd-tmpfiles` step sets the correct ownership (root:systemd-journal) and ACLs (systemd ≥219 uses ACLs
on this tree) — don't `mkdir` alone and skip it. This is independent of the `Storage=` setting; on most
distros `Storage=` already defaults to `persistent`/`auto`, so directory existence alone flips behavior. Grant
read access to non-root humans by adding them to the `systemd-journal` group, or system-wide via ACL:

```
# setfacl -Rnm g:wheel:rx,d:g:wheel:rx,g:adm:rx,d:g:adm:rx /var/log/journal/
```

## 3. journalctl essential filters

- `-u <unit>` / `--unit=` — filter by systemd unit (matches `_SYSTEMD_UNIT=`); glob patterns allowed.
  User-unit equivalent is `--user-unit=`.
- `-f` / `--follow` — tail continuously, like `tail -f`.
- `-x` / `--catalog` — appends explanatory help text from the message catalog. **Do not use `-x` when
  attaching journalctl output to bug reports** — it adds extraneous prose.
- `-e` / `--pager-end` — jump to the end of output in the pager.
- `--since=`/`-S`, `--until=`/`-U` — bound by timestamp. Format `YYYY-MM-DD HH:MM:SS`; time/seconds/date
  components can be progressively omitted. Also accepts `yesterday`/`today`/`tomorrow`/`now` and relative
  offsets (`-20min`/`"20 min ago"`). Full grammar in `systemd.time(7)`.
- `-p <priority>` / `--priority=` — single level or `FROM..TO` range, by name or number: `emerg`(0),
  `alert`(1), `crit`(2), `err`(3), `warning`(4), `notice`(5), `info`(6), `debug`(7). A single value shows that
  level *and everything more severe* (lower number); a range shows exactly that range inclusive.
- `-b [[ID]±offset]` / `--boot=` — bare `-b` = current boot. `-b -1` = previous boot, `-b -2` = two boots
  back, `-b 1` = first boot in the journal (chronological). Can combine a specific boot `ID` with a relative
  `±offset` from that boot.
- `-k` / `--dmesg` — kernel messages only (`_TRANSPORT=kernel`); implies `--boot=0` unless a different boot is
  specified.
- `-o <mode>` / `--output=` — `short` (default), `short-iso` (RFC 3339 timestamps), `short-precise` (+
  microseconds), `short-monotonic`, `verbose` (full structured record, every field), `export` (binary-ish
  transfer format), `json`, `json-pretty`, `json-sse`, `cat` (bare message text, no metadata), `with-unit`
  (shows unit name instead of syslog identifier).
- `--disk-usage` — total bytes used by all archived + active journal files.
- `--vacuum-size=`, `--vacuum-time=`, `--vacuum-files=` — trim *archived* files by cumulative size, age, or
  file count. Active files aren't touched; combine with `--rotate` first if a file needs trimming but hasn't
  rotated out yet.
- `--grep=<pattern>` — server-side message-content filter; prefer this over `journalctl | grep` since it
  avoids journald doing wasted work only for grep to discard it.

## 4. Correlating a failed service with its logs

Canonical combo:

```
$ systemctl status <unit>
$ journalctl -xeu <unit>
```

`-x` pulls in catalog explanations alongside the log lines — often the fastest way to get a plain-language
cause and suggested fix. `-e` jumps straight to the newest entries. `-u <unit>` scopes to just that unit's
matches.

**Gotcha**: for very short-lived services that fail before journald's async metadata collection catches up,
`journalctl -u foo.service` can show nothing even though the process definitely ran and logged.
`_SYSTEMD_UNIT`/`_COMM` fields are populated by reading `/proc` after the fact — if the process is already
gone, that enrichment can race and lose. Workaround: get the PID from `systemctl status` and query by it
directly: `journalctl _PID=123`. This is a known upstream limitation (systemd/systemd#2913), not user error.

## 5. Structured logging (brief)

Services logging via the native Journal API (`sd_journal_print()`/`sd_journal_send()`) or via `systemd-cat`
can attach arbitrary `KEY=VALUE` fields per entry (uppercase convention, e.g. `CODE_FILE=`, custom app
fields), not just a flat message string. View the full field set per entry with:

```
$ journalctl -u myservice -o verbose
```

or machine-parse with `-o json`/`-o json-pretty`. Plain stdout/stderr from a unit is still captured as
unstructured text (split into records at newline/NUL) unless the process itself uses the native protocol.

`Type=notify` in `systemd.service`/`systemd.exec` is a related but separate mechanism — it's about *service
readiness signaling* via `sd_notify()` (e.g. `READY=1`) over `NOTIFY_SOCKET`, not journal field logging (see
`references/services-and-execution.md` for `Type=` detail). Both mechanisms use adjacent native systemd IPC
protocols but serve different purposes (log data vs. lifecycle state).
