# Units, Dependencies, and Safe Overrides

Sources: `systemd.unit(5)`, `systemctl(1)` (freedesktop.org "latest", mirrored via
manpages.debian.org/unstable — content-identical DocBook-generated text), cross-checked
against ArchWiki "Systemd". Where ArchWiki frames something as distro-specific
(e.g. "avoid conflicts with pacman"), treat it as the distro-agnostic fact that any
package manager overwrites `/usr/lib` on upgrade.

## Contents

1. Unit file anatomy (search path, sections, naming, templates)
2. Specifiers (verbatim `man 5 systemd.unit` Table 5)
3. Dependency directives
4. `WantedBy=`/`RequiredBy=` and `systemctl enable`
5. Overriding units safely
6. `systemctl` essentials and `daemon-reload`

## 1. Unit file anatomy

### Search path precedence

Unit files are looked up across three trees; **first match wins** (highest precedence first):

| Path | Owner |
|---|---|
| `/etc/systemd/system/` | sysadmin, permanent |
| `/run/systemd/system/` | sysadmin/generators, runtime-only (gone after reboot) |
| `/usr/lib/systemd/system/` | distro package manager |

`$SYSTEMD_UNIT_PATH` overrides this list entirely if set (append the default list by
ending the value with a trailing `:`). User-mode search order is analogous under
`$XDG_CONFIG_HOME`, `$XDG_DATA_HOME`, `$XDG_DATA_DIRS`, plus `/run` runtime units. Query
the live, fully-resolved list with:

```
systemctl show --property=UnitPath
```

The same precedence applies to **drop-in** `.d/` directories, and drop-ins always win
over a same-named full unit file wherever it lives: `/etc` drop-ins beat `/run` drop-ins
beat `/usr/lib` drop-ins beat any unit file fragment.

### [Unit] / [Install] sections

`[Unit]` carries generic metadata and dependency/ordering directives (see §3).
`[Install]` is **not read at runtime** — systemd only consults it when `systemctl
enable`/`disable` run; it exists purely to drive symlink creation (§4). Unknown
directives log a warning but don't fail unit load; an unknown *section* prefixed `X-`
is silently ignored — useful for embedding application-specific metadata in a unit file.

### Naming, escaping, templates

- Valid name: `prefix` + `.type`, prefix chars are `A-Za-z0-9:-_.\`, max 255 chars total.
  Type suffix is one of `.service .socket .device .mount .automount .swap .target .path
  .timer .slice .scope`.
- **Escaping**: arbitrary strings (e.g. filesystem paths) become unit-name-safe via
  `systemd-escape`. `/` → `-`; other non-alphanumeric bytes → `\xNN`. `/foo//bar/baz/` →
  `foo-bar-baz` (root `/` alone escapes to a single `-`).
- **Templates**: `name@.service` is a template; `name@somearg.service` is an instance.
  If the literal instance name isn't found on disk, systemd strips everything between
  `@` and the suffix and loads the template file instead, substituting the instance
  string back in via specifiers.

### Drop-in override anatomy

```
/etc/systemd/system/httpd.service.d/local.conf
```

```ini
[Service]
# Reset the list before re-adding — Exec*, list-type non-dependency directives
# don't merge, they need an explicit empty reset first.
ExecStart=
ExecStart=/usr/sbin/httpd -f /etc/httpd-custom.conf
Nice=0
```

Dependency directives (`After=`, `Wants=`, etc.) **cannot** be reset to empty in a
drop-in — you can only *add* dependencies this way; removing one requires overriding
the whole unit file. Multiple drop-in `.conf` files apply in lexicographic filename
order regardless of which precedence-tier directory they're in. A top-level `service.d/`,
`socket.d/`, etc. (no unit name) applies to *every* unit of that type, at lower
precedence than name-specific overrides.

For unit names containing dashes, drop-ins are also searched at each truncation point:
for `foo-bar-baz.service`, systemd searches `foo-bar-baz.service.d/`, `foo-bar-.service.d/`,
and `foo-.service.d/` — useful for defining a shared drop-in across a family of
dash-separated unit names (this convention is built around mount/automount/slice naming).

## 2. Specifiers

Many settings resolve **specifiers** — placeholders substituted when the unit file is
loaded. This is the full table from `man 5 systemd.unit` ("Table 5. Specifiers available
in unit files"), kept close to verbatim since agents frequently need the exact,
complete list rather than a curated subset.

| Specifier | Meaning | Details |
|---|---|---|
| `%a` | Architecture | A short string identifying the architecture of the local system. A string such as `x86`, `x86-64` or `arm64`. See the architectures defined for `ConditionArchitecture=` for a full list. |
| `%A` | Operating system image version | The OS image version identifier of the running system, read from `IMAGE_VERSION=` in `/etc/os-release`. Empty string if unset. |
| `%b` | Boot ID | The boot ID of the running system, formatted as a string. See `random(4)`. |
| `%B` | Operating system build ID | Read from `BUILD_ID=` in `/etc/os-release`. Empty string if unset. |
| `%C` | Cache directory root | Either `/var/cache` (system manager) or the path `$XDG_CACHE_HOME` resolves to (user managers). |
| `%d` | Credentials directory | The value of the `$CREDENTIALS_DIRECTORY` environment variable, if available. See "Credentials" in `systemd.exec(5)`. |
| `%D` | Shared data directory | Either `/usr/share/` (system manager) or the path `$XDG_DATA_HOME` resolves to (user managers). |
| `%E` | Configuration directory root | Either `/etc/` (system manager) or the path `$XDG_CONFIG_HOME` resolves to (user managers). |
| `%f` | Unescaped filename | The unescaped instance name (if applicable) with `/` prepended, or the unescaped prefix name prepended with `/`. Implements unescaping per the absolute-path escaping rules above. |
| `%g` | User group | Name of the group running the service manager instance. System manager resolves to `root`. |
| `%G` | User GID | Numeric GID of the user running the service manager instance. System manager resolves to `0`. |
| `%h` | User home directory | Home directory of the *user running the service manager instance*. System manager resolves to `/root`. **Not** influenced by a unit's own `User=`. |
| `%H` | Host name | Hostname of the running system at the point the unit configuration is loaded. |
| `%i` | Instance name | For instantiated units, the string between the first `@` and the type suffix. Empty for non-instantiated units. |
| `%I` | Unescaped instance name | Same as `%i`, with escaping undone. |
| `%j` | Final component of the prefix | The string between the last `-` and the end of the prefix name. If there's no `-`, same as `%p`. |
| `%J` | Unescaped final component of the prefix | Same as `%j`, with escaping undone. |
| `%l` | Short host name | Hostname at load time, truncated at the first dot (domain component removed). |
| `%L` | Log directory root | Either `/var/log` (system manager) or `$XDG_STATE_HOME` + `/log` (user managers). |
| `%m` | Machine ID | The machine ID of the running system, formatted as a string. See `machine-id(5)`. |
| `%M` | Operating system image identifier | Read from `IMAGE_ID=` in `/etc/os-release`. Empty string if unset. |
| `%n` | Full unit name | — |
| `%N` | Full unit name | Same as `%n`, with the type suffix removed. |
| `%o` | Operating system ID | Read from `ID=` in `/etc/os-release`. |
| `%p` | Prefix name | For instantiated units, the string before the first `@`. For non-instantiated units, same as `%N`. |
| `%P` | Unescaped prefix name | Same as `%p`, with escaping undone. |
| `%q` | Pretty host name | Read from `PRETTY_HOSTNAME=` in `/etc/machine-info` at load time. Falls back to the short hostname if unset. |
| `%s` | User shell | Shell of the user running the service manager instance. |
| `%S` | State directory root | Either `/var/lib` (system manager) or `$XDG_STATE_HOME` (user managers). |
| `%t` | Runtime directory root | Either `/run/` (system manager) or `$XDG_RUNTIME_DIR` (user managers). |
| `%T` | Directory for temporary files | Either `/tmp` or the path `$TMPDIR`/`$TEMP`/`$TMP` are set to. |
| `%u` | User name | Name of the *user running the service manager instance*. System manager resolves to `root`. **Not** influenced by a unit's own `User=`. |
| `%U` | User UID | Numeric UID of the *user running the service manager instance*. System manager resolves to `0`. **Not** influenced by a unit's own `User=`. |
| `%v` | Kernel release | Identical to `uname -r` output. |
| `%V` | Directory for larger, persistent temporary files | Either `/var/tmp` or the path `$TMPDIR`/`$TEMP`/`$TMP` are set to. |
| `%w` | Operating system version ID | Read from `VERSION_ID=` in `/etc/os-release`. Empty string if unset. |
| `%W` | Operating system variant ID | Read from `VARIANT_ID=` in `/etc/os-release`. Empty string if unset. |
| `%y` | Path to the fragment | Path where the main part of the unit file is located (real path for linked units). Raises an error for units without a fragment file. |
| `%Y` | Directory of the fragment | The directory part of `%y`. |
| `%%` | Single percent sign | Use `%%` in place of `%` to specify a literal percent sign. |

`[Install]` only understands a restricted subset: `%a %b %B %g %G %H %i %j %l %m %n %N
%o %p %u %U %v %w %W %%` — dependency-target specifiers like `%f`/`%t` aren't valid there.

## 3. Dependency directives

**The #1 confusion**: requirement directives (`Wants=`, `Requires=`, ...) control *what
gets pulled into the transaction* — whether a unit starts at all. `Before=`/`After=`
control *relative sequencing* — when, not whether. A unit can be `Wants=`'d without any
`After=`, in which case both start **simultaneously, with no wait**. `systemd.unit(5)`
states this explicitly: "requirement dependencies do not influence the order in which
services are started or stopped." The common working pattern is to set *both*
`Wants=`/`Requires=` **and** the matching `After=` on the same target.

| Directive | Pulls in target? | Failure of target propagates? | Runtime coupling |
|---|---|---|---|
| `Wants=` | yes, best-effort | no — target failing/missing doesn't fail this unit | none |
| `Requires=` | yes, hard | target failing *to start* fails this unit's start job; target *later* stopping/failing does **not** stop this unit | none after start |
| `Requisite=` | no (must already be started) | if target isn't already active, this unit's start fails immediately | none |
| `BindsTo=` | yes, hard (like `Requires=`) | same as `Requires=`, plus: | if combined with `After=`, this unit is stopped the instant the bound unit becomes inactive for **any** reason (including a skipped condition check) |
| `PartOf=` | no ordering/start implication of its own | stopping/restarting the target stops/restarts this unit | doesn't imply pulling-in or ordering at all — pure "lifecycle follows" |
| `Conflicts=` | actively stops the other unit if both would be active | — | no ordering implied — pair with `Before=`/`After=` if stop-then-start ordering matters |
| `Before=`/`After=` | no | n/a | pure ordering: `Before=` = this unit finishes starting before the listed unit starts; `After=` = the inverse. Shutdown order is always the reverse of startup order. If neither has an ordering relationship, both directions run in parallel. |

Decision table:

| You want... | Use |
|---|---|
| B started whenever A is, but A shouldn't fail if B fails | `Wants=B` (+ `After=B` if A needs B ready first) |
| A to fail to start if B fails to start | `Requires=B` |
| A to refuse to start unless B is *already* running | `Requisite=B` |
| A to be stopped automatically the moment B stops/fails, at any time | `BindsTo=B` + `After=B` |
| A's lifecycle to mirror B's stop/restart (start-up not linked) | `PartOf=B` |
| A and B to never run at once, and shutdown of one ordered before start of the other | `Conflicts=B` + `Before=B`/`After=B` |
| Pure sequencing with no pull-in semantics | `Before=`/`After=` alone |

Reverse-direction properties (`RequisiteOf=`, `BoundBy=`, `ConsistsOf=`, `UpheldBy=`) show
up in `systemctl show` output but **cannot be set directly** — they're computed from the
forward directive on the other unit.

`foo.service.wants/` and `foo.service.requires/` directories (symlinks into other unit
files) are the on-disk mechanism `Wants=`/`Requires=` ultimately compile down to — this
is what `systemctl enable` populates from a target's `[Install]` block.

## 4. WantedBy=/RequiredBy= and `systemctl enable`

`[Install]` directives only take effect via `enable`/`disable`; systemd ignores
`[Install]` entirely at runtime otherwise. `WantedBy=target.name` in unit `foo.service`'s
`[Install]` section means: `systemctl enable foo.service` creates the symlink

```
/etc/systemd/system/target.name.wants/foo.service → …/foo.service
```

(`RequiredBy=` → `…/target.name.requires/…`; `Also=` enables/disables the listed extra
units together; `Alias=` creates plain-name symlinks). For a template unit's `[Install]`,
`systemctl enable foo@instance.service` requires either an explicit instance name in the
enable command or `DefaultInstance=` in the unit. `enable`/`disable` accept **only unit
names**, not arbitrary file paths, and both implicitly run the equivalent of
`daemon-reload` after finishing (suppress with `--no-reload`). Enabling ≠ starting —
they're orthogonal; `enable --now` does both.

## 5. Overriding units safely

Never hand-edit a vendor unit under `/usr/lib/systemd/system/` — a package upgrade
silently overwrites it, discarding local changes with no warning.

Two safe patterns, both under `/etc/systemd/system/`:

```
# systemctl edit httpd.service                # drop-in, default name override.conf
# systemctl edit --drop-in=limits.conf httpd  # drop-in, custom name
# systemctl edit --full httpd.service         # full replacement copy, opened in $EDITOR
```

`edit` (without `--full`) opens/creates
`/etc/systemd/system/httpd.service.d/override.conf`, and **auto-runs daemon-reload** on
save — no manual step needed after using `edit`. `--full` creates a full-copy override —
same file, minus vendor updates going forward, so drop-ins are almost always preferable
when only a few directives need changing.

```
systemctl revert httpd.service   # undoes edit/set-property/mask, restores vendor unit
systemctl cat httpd.service      # prints the *effective* merged unit — fragment + all drop-ins, in application order
```

`cat` is the fast way to confirm what's actually in effect after stacking drop-ins across
`/etc`, `/run`, `/usr/lib`. You cannot use `edit` to temporarily modify a unit that
already has an override in `/etc/` (it always wins over `/run/`) — use `systemctl edit
--runtime` to place a drop-in under `/run/systemd/system/` instead, for changes meant to
vanish on reboot (e.g. temporary debug flags).

## 6. systemctl essentials

| Command | What it does |
|---|---|
| `status` | Human-readable state + recent journal lines (`--lines=`, default 10) |
| `start`/`stop` | Activate/deactivate now; orthogonal to enablement |
| `restart` | stop then start; does **not** flush the file-descriptor store or guarantee full resource teardown — use explicit `stop` + `start` if that matters |
| `try-restart` | restart only if currently running; no-op otherwise |
| `reload` | Ask the running process to reload config via `ExecReload=`; fails if unit doesn't support it |
| `reload-or-try-restart` | reload if supported, else restart-if-running, else no-op |
| `enable`/`disable` | Create/remove `[Install]`-driven symlinks; implicit daemon-reload |
| `mask` | Symlinks the unit name to `/dev/null` under `/etc/systemd/system/` (or `/run/` with `--runtime`) — makes it **impossible to start even manually**, stronger than `disable`. Fails if a matching unit file already physically exists in that same directory tier. |
| `unmask` | Removes that `/dev/null` symlink |
| `daemon-reload` | Re-parses **all** unit files + drop-ins from disk; flushes and replaces unit config while preserving runtime state of already-running units |

### When daemon-reload is actually required

- **New unit file added**, or an **existing loaded unit's fragment/drop-in edited by
  hand** (not through `systemctl edit`): required before `start`/`enable`/`restart` will
  see the change — systemd caches parsed unit state in memory and won't re-read disk on
  its own.
- **`systemctl edit` (drop-in or `--full`)**: daemon-reload runs automatically after the
  editor exits successfully — no manual step.
- **`enable`/`disable`/`mask`/`unmask`**: implicit daemon-reload unless `--no-reload` passed.
- **Manually creating/removing `.wants/`/`.requires/` symlinks yourself** instead of via
  `enable`: the man page explicitly warns *you* must run `daemon-reload` — nothing does
  it for you.
- **NOT required**: restarting a service after its own application config file
  (something the daemon reads at runtime, not the unit file) changed — that's just
  `restart` or the app's own `reload` mechanism. Also not required merely to run
  `status`/`start` on a never-yet-loaded new unit — systemd lazily loads a unit file the
  first time it's referenced. The gap is specifically an *already-loaded* unit whose
  on-disk definition changed underneath it.
