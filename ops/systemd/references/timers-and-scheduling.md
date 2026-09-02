# Timers and Scheduling

Sources: `systemd.timer(5)`, `systemd.time(7)`, `systemd.target(5)` (freedesktop.org, systemd latest),
cross-checked against ArchWiki `Systemd/Timers`.

## Contents

1. `systemd.timer` directive reference
2. `OnCalendar=` syntax
3. `Persistent=` catch-up semantics
4. Timer/service naming and `Unit=`
5. `systemctl list-timers`
6. Timers vs cron

## 1. systemd.timer directive reference

A `.timer` unit needs a matching unit to activate — by default a `.service` of the same basename (`foo.timer`
→ `foo.service`). Timer files carry `[Unit]`/`[Install]` sections like any unit, plus a `[Timer]` section.

**Monotonic timers** — relative to a starting point, paused during suspend unless `WakeSystem=yes`:

| Directive            | Relative to                                                                                                                      |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `OnActiveSec=`       | moment the timer unit itself is activated                                                                                        |
| `OnBootSec=`         | machine boot-up (in containers, aliased to `OnStartupSec=`)                                                                      |
| `OnStartupSec=`      | when the *service manager* was first started (matters mainly for the per-user manager, which starts at first login, not at boot) |
| `OnUnitActiveSec=`   | last activation of the unit being triggered                                                                                      |
| `OnUnitInactiveSec=` | last deactivation of the unit being triggered                                                                                    |

Multiple directives (same or different types) may be combined — the timer fires whenever *any* elapses.
Monotonic and `OnCalendar=` expressions can coexist in one unit. If `OnBootSec=`/`OnStartupSec=` computes to a
point already in the past when the timer activates, it fires immediately; the other monotonic directives do
not have this behavior. Assigning the empty string to any of these resets *all* timers (monotonic and
calendar) on the unit.

`OnCalendar=` — wall-clock/realtime timer using calendar event syntax (§2). May be specified multiple times
(OR semantics). Timer units with at least one `OnCalendar=` gain automatic
`After=time-set.target`/`After=time-sync.target` ordering so they don't fire before the clock is correct — on
hardware without a battery-backed RTC, enable `systemd-time-wait-sync.service` too. While the system is
suspended, an elapsed calendar timer is *not* acted on immediately; on resume it catches up and fires once
(not once per missed occurrence) — this is a distinct mechanism from `Persistent=` (§3), which survives full
power-off.

`AccuracySec=` (default **1min**) — the timer is allowed to slip within a window `[T, T+AccuracySec]`; systemd
places the actual firing at a host-specific stable position inside that window to coalesce wakeups across
timers and save power. Set to `1us` for maximum precision. Don't confuse with `RandomizedDelaySec=` — accuracy
*coalesces* (fewer wakeups), randomized delay *spreads* (avoids thundering herd). They compose: delay is added
first, then the result may be further shifted for coalescing.

`RandomizedDelaySec=` (default **0**) — adds a delay uniformly chosen in `[0, N]` on top of the next elapse
time, recomputed on each iteration unless `FixedRandomDelay=yes` pins it (derived from machine ID + UID + unit
name, stable across restarts). Use `AccuracySec=1us` + a nonzero `RandomizedDelaySec=` to genuinely spread
firings instead of coalescing them.

`RandomizedOffsetSec=` (systemd ≥258, default **0**) — like `RandomizedDelaySec=` but the offset is stable and
independent of manager start time, so it preserves calendar periodicity across reboots (a laptop restarted
more often than its randomized delay would otherwise never fire the timer). Only applies to `OnCalendar=`
timers.

`Unit=` — the unit to activate; suffix must not be `.timer`. Defaults to a same-named service. Recommended:
keep the timer and target unit identically named except for suffix, and only use `Unit=` for the
differently-named case (see §4).

`Persistent=` (default **false**) — see §3, the most commonly misunderstood directive.

`WakeSystem=` (default **false**, system manager only, needs privileges) — an elapsing timer resumes the
system from suspend if hardware supports it; does *not* re-suspend afterward. Also swaps which monotonic clock
backs `OnActiveSec=`/`OnBootSec=`/etc.: `CLOCK_MONOTONIC` (pauses during suspend) when false, `CLOCK_BOOTTIME`
(keeps advancing) when true.

`RemainAfterElapse=` (default **true**) — if true, the timer unit stays loaded/queryable after it elapses and
its target unit deactivates again; restarting it a second time then has no effect. Set false for transient
timers so the unit unloads and can be started again to refire the service.

Two more boolean options: `OnClockChange=`/`OnTimezoneChange=` (default false) — trigger the unit when the
realtime clock jumps relative to monotonic time, or the local timezone changes.

Note on re-triggering: if the target unit is still active when the timer next elapses, it is **not** restarted
— it's simply left running. This makes `RemainAfterExit=yes` services a poor fit for repeated timer activation
(they only ever get one activation, then sit "active" forever); target units used this way need
`StopWhenUnneeded=yes` so they stop themselves after each activation.

## 2. OnCalendar= syntax

General form: `Weekday Year-Month-Day Hour:Minute:Second[.fraction] [Timezone]`. Any field may be `*` (match
all); comma-separated lists; `A..B` ranges; `VAL/REPEAT` step values (e.g. `2/3` = 2 and every 3rd value
after); ranges can carry a step too (`A..B/N`). `~` anchors to the *last* day of the month (`*-02~03` =
3rd-to-last day of February; `Mon *-05~07/1` = last Monday in May). Omitted date defaults to `*-*-*`, omitted
time to `00:00:00`, omitted seconds to `:00`. Timezone: `UTC`, an IANA zone name (`Europe/Paris`), or an
offset — defaults to local time.

Shorthand expressions:

```
minutely      → *-*-* *:*:00
hourly        → *-*-* *:00:00
daily         → *-*-* 00:00:00
monthly       → *-*-01 00:00:00
weekly        → Mon *-*-* 00:00:00
yearly        → *-01-01 00:00:00
quarterly     → *-01,04,07,10-01 00:00:00
semiannually  → *-01,07-01 00:00:00
```

Examples:

```
OnCalendar=daily                          # 00:00:00 every day
OnCalendar=*-*-* 03:00:00                 # daily at 3am
OnCalendar=*:0/15                         # every 15 minutes → *-*-* *:00,15,30,45:00
OnCalendar=Mon..Fri 09:00                 # weekdays only, 9am
OnCalendar=*-*-~03 00:00:00               # 3rd-to-last day of every month
OnCalendar=*-*-* 00/2:00:00                # every 2 hours on the hour
OnCalendar=Sat *-*-1..7 18:00:00          # first Saturday of every month, 18:00
OnCalendar=Mon,Tue *-*-01..04 12:00:00    # 1st-4th of the month at noon, but only if Mon/Tue
```

Test and normalize any expression with `systemd-analyze calendar`, which also prints the next occurrence(s):

```
$ systemd-analyze calendar weekly
$ systemd-analyze calendar "Mon,Tue *-*-01..04 12:00:00" --iterations=5
```

(ArchWiki tip: pair with `faketime` to test firing behavior at arbitrary simulated "now" times.)

Time-span syntax (for `OnBootSec=`, `AccuracySec=`, `RandomizedDelaySec=`, etc.) accepts space-separated
`value+unit` terms, summed: `usec/us/μs`, `msec/ms`, `sec/s`, `min/m`, `hr/h`, `day/d`, `week/w`, `month/M`
(30.44 days), `year/y` (365.25 days). Unit optional (defaults to seconds); spaces between terms optional.
Examples: `2h 30min`, `2hours`, `48hr`, `1y 12month`, `55s500ms`. Normalize with
`systemd-analyze timespan "5h 30min"`.

## 3. Persistent= — catch-up semantics (commonly misunderstood)

`Persistent=true` only affects `OnCalendar=` timers (monotonic timers ignore it). When set, systemd records
the last-trigger time of the *unit* on disk. On timer *activation* (enable/start/boot), if the calendar
schedule would have fired **at least once** while the timer was inactive (e.g. machine was powered off through
the scheduled time), the service unit is triggered immediately — subject to `RandomizedDelaySec=` still
applying. It is a boot/startup catch-up mechanism, distinct from the "elapsed-while-suspended" catch-up that
`OnCalendar=` timers always get regardless of `Persistent=` (suspend keeps the realtime clock running, so that
case is handled unconditionally and results in exactly one activation, never a backlog).

The stamp is a zero-length file per timer unit, stored under `/var/lib/systemd/timers/stamp-<unit>` for system
timers, `~/.local/share/systemd/timers/` for user timers. If a timer "gets out of sync," the canonical way to
reset it is `systemctl clean --what=state <timer-unit>`, not deleting the file by hand.

```ini
[Timer]
OnCalendar=weekly
Persistent=true
```

If the box was off when `weekly` was due, the service runs once, immediately, at next boot.

## 4. Timer vs service naming, and Unit=

Convention: `foo.timer` pairs with `foo.service` by basename match — this is implicit and requires no `Unit=`.
When the target must be named differently, use `Unit=<name>` (suffix anything but `.timer`) in the timer's
`[Timer]` section:

```ini
# nightly-report.timer
[Timer]
OnCalendar=daily
Unit=generate-report.service
```

Best practice: still prefer identical basenames except suffix; reserve `Unit=` for genuine exceptions
(templated units, shared services triggered by multiple timers, etc.).

## 5. systemctl list-timers

```
$ systemctl list-timers
NEXT                          LEFT        LAST                          PASSED     UNIT                          ACTIVATES
Thu 2014-07-10 19:37:03 CEST  11h left    Wed 2014-07-09 19:37:03 CEST  12h ago    systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
Fri 2014-07-11 00:00:00 CEST  15h left    Thu 2014-07-10 00:00:13 CEST  8h ago     logrotate.timer               logrotate.service
```

Columns: `NEXT`/`LEFT` — absolute and relative time to the next scheduled elapse; `LAST`/`PASSED` — absolute
and relative time of the previous elapse. `ACTIVATES` names the unit that will be triggered (relevant when
`Unit=` differs from the timer's basename). By default only *active* (loaded) timers show; pass `--all` to
include inactive ones. A service's own `systemctl status` will show `inactive` between runs — that's expected,
not a failure, unless it's currently mid-trigger.

## 6. Timers vs cron

systemd timers are strictly better than cron whenever the job needs anything beyond "run this command on a
schedule": each job is a full unit, so it gets dependency ordering (`After=`/`Requires=` on network, mounts,
other services), resource control (cgroup accounting inherited from `systemd.resource-control`, see
`references/sandboxing-and-hardening.md`), structured logging into the journal for free
(`journalctl -u foo.service` — no more grepping mail spools), the `Persistent=` catch-up semantics above (no
cron equivalent without extra tooling like anacron), and independent testability
(`systemctl start foo.service` runs the job right now, decoupled from its timer). The one thing cron has that
timers lack out of the box is `MAILTO=`-style failure notification email — wire `OnFailure=` to a notification
unit instead. Timers also require two files (`.timer` + `.service`) versus cron's one-line entry — a minor
ergonomic cost for the above gains.
