# Sandboxing, Hardening, and Resource Control

Sources: `systemd.exec(5)` (Sandboxing + Process Properties sections),
`systemd.resource-control(5)`, `systemd-analyze(1)` (`security` subcommand) — systemd
GitHub `main` branch DocBook source, which the rendered freedesktop.org man pages are
generated from. Cross-checked against the ArchWiki `systemd/Sandboxing` page —
divergences noted inline as **[Arch]**.

## Contents

1. Sandboxing directives by category
2. A reasonably hardened template
3. `systemd-analyze security <unit>`
4. Resource control (`systemd.resource-control`)

## 1. Sandboxing directives by category

All directives live in `[Service]` (or any exec-context unit: service/socket/mount/swap).
Defaults shown are systemd's own defaults, not what any distro preset applies.

### Filesystem

| Directive | Default | Effect |
|---|---|---|
| `ProtectSystem=` | `off` | `true`: mounts `/usr/` and boot loader dirs (`/boot`, `/efi`) read-only. `full`: also mounts `/etc/` read-only. `strict`: entire FS hierarchy read-only except API filesystems (`/dev`, `/proc`, `/sys`, which need `PrivateDevices=`/`ProtectKernelTunables=`/`ProtectControlGroups=` to also lock down). Implied by `DynamicUser=`. |
| `ProtectHome=` | `false` | `true`: `/home/`, `/root`, `/run/user` made inaccessible+empty. `read-only`: same three dirs read-only. `tmpfs`: tmpfs mounted over them (use with `BindPaths=`/`BindReadOnlyPaths=` to poke holes). Implied by `DynamicUser=`. |
| `PrivateTmp=` | `false` | New mount namespace; `/tmp` and `/var/tmp` are private and wiped on stop. `disconnected`: backing storage is not the host's real `/tmp` (implied by `DynamicUser=`); plain `true` keeps backing storage on host `/tmp`. |
| `PrivateDevices=` | `false` | New `/dev/` with only API pseudo-devices (`null`, `zero`, `random`, PTYs) — no physical devices. Also blocks `@raw-io` syscalls, drops `CAP_MKNOD`/`CAP_SYS_RAWIO`, sets `DevicePolicy=closed`, mounts new `/dev` read-only+`noexec` (can break `mmap()` of `/dev/zero` for executable memory). |
| `ReadOnlyPaths=` / `ReadWritePaths=` / `InaccessiblePaths=` | unset | Space-separated path lists inside the mount namespace. `ReadWritePaths=` nested inside `ReadOnlyPaths=` carves out writable subdirs — needed alongside `ProtectSystem=strict` to allow-list write targets. Cannot force writes onto a read-only-mounted superblock. |
| `ProtectKernelTunables=` | `off` | `/proc/sys`, `/sys`, `/proc/sysrq-trigger`, `/proc/latency_stats`, `/proc/acpi`, `/proc/timer_stats`, `/proc/fs`, `/proc/irq` read-only; `/proc/kallsyms`, `/proc/kcore` inaccessible. Implies `MountAPIVFS=yes`. |
| `ProtectKernelModules=` | `off` | Denies explicit module load/unload; drops `CAP_SYS_MODULE`; blocks module syscalls; makes `/usr/lib/modules` inaccessible. Automatic module autoloading via kernel mapping tables can still occur as a side effect. |
| `ProtectKernelLogs=` | `off` | Drops `CAP_SYSLOG`; blocks the `syslog(2)` syscall (kernel ring buffer, not libc `syslog(3)`); makes `/dev/kmsg`, `/proc/kmsg` inaccessible. |
| `ProtectControlGroups=` | `off` | `true`: `/sys/fs/cgroup/` read-only. `private`: cgroup namespace with private *writable* cgroupfs mount. `strict`: cgroup namespace with private *read-only* mount. `private`/`strict` downgrade to `false`/`true` unless unified hierarchy + cgroup namespaces are supported. Implies `MountAPIVFS=yes`. |
| `ProtectClock=` | `off` | Denies writes to hw/system clock; drops `CAP_SYS_TIME`+`CAP_WAKE_ALARM`; installs syscall filter; implies `DeviceAllow=char-rtc r` — `/dev/rtc*` becomes read-only. |
| `ProtectProc=` | `default` | Controls `hidepid=` for the unit's `/proc` mount: `noaccess` (can't access others' `/proc/PID`), `invisible` (other users' processes hidden), `ptraceable` (only ptrace-able processes visible), `default` (no restriction). Root is unaffected unless combined with `User=`/`DynamicUser=yes` and lack of `CAP_SYS_PTRACE`. Namespacing-based — incompatible with services that install mounts on the host. |
| `ProcSubset=` | `all` | `pid`: hides all `/proc` files/dirs not directly about process introspection (via `subset=` mount option) — breaks many programs that read other kernel APIs under `/proc`; niche setting. |

### Process / privilege

| Directive | Default | Effect |
|---|---|---|
| `NoNewPrivileges=` | `false` | Process and children can never gain privileges via `execve()` (setuid/setgid bits, file capabilities) — `PR_SET_NO_NEW_PRIVS`. Simplest, most effective anti-escalation setting. Only affects the unit's own process tree, not things it triggers via `at`/`cron`/`systemd-run`/arbitrary IPC. |
| `CapabilityBoundingSet=` | unmodified | Whitespace-separated capability list (e.g. `CAP_NET_BIND_SERVICE`); listed caps are *kept*, all others removed from the bounding (and effective/permitted/inheritable) sets. Prefix `~` inverts (deny-list). Repeatable — merged by OR (by AND if `~`-prefixed). Empty string resets to empty set; bare `~` resets to full set. |
| `AmbientCapabilities=` | unmodified | Capabilities granted to the process's ambient set even when running as non-root — lets you drop root but keep e.g. `CAP_NET_BIND_SERVICE`. Automatically adds `keep-caps` to `SecureBits=`. Same list/`~`/merge semantics as `CapabilityBoundingSet=`. **Always pair with `CapabilityBoundingSet=` restricting to the same caps** — Ambient alone doesn't limit what's *available*, only what's granted. |
| `User=` / `Group=` | `root` | UNIX user/group processes run as. For system services, any user is settable; for non-root user-manager services, only the invoking user itself is valid. |
| `DynamicUser=` | `false` | Allocates a transient UID/GID pair (range 61184–65519) at start, released at stop; integrated into NSS via `nss-systemd`. Implies `ProtectSystem=strict`, `ProtectHome=`-equivalent behavior, `RestrictSUIDSGID=yes`, `PrivateTmp=disconnected`. Must pair with `StateDirectory=`/`RuntimeDirectory=`/`CacheDirectory=`/`LogsDirectory=`/`ConfigurationDirectory=` since the service can't rely on a fixed home/UID for persistent storage. |

### Network

| Directive | Default | Effect |
|---|---|---|
| `PrivateNetwork=` | `false` | New network namespace with only loopback `lo` — no other devices reachable. Disconnects **all** socket families from the host, including `AF_NETLINK` (udev events won't reach the unit) and abstract-namespace `AF_UNIX` (filesystem-path `AF_UNIX` sockets still work). Share a namespace across units with `JoinsNamespaceOf=`. Implies `PrivateMounts=` unless set otherwise. |
| `RestrictAddressFamilies=` | unset (all allowed) | `none` denies all; otherwise a space-separated allow-list of families (`AF_UNIX`, `AF_INET`, `AF_INET6`, …, see `address_families(7)`); `~`-prefix inverts to deny-list. Doesn't affect `+`-prefixed commands. Almost always include `AF_UNIX` — used pervasively for local IPC/logging. |
| `IPAddressAllow=` / `IPAddressDeny=` (systemd.resource-control) | both empty | Not a syscall filter — an eBPF-based accept/reject filter on `AF_INET`/`AF_INET6` socket traffic, address/prefix-length pairs (e.g. `10.0.0.0/8`). Combines with parent slice lists. Applied to both ingress (source addr checked) and egress (dest addr checked); allow rules checked first, in order. |

### Syscalls

| Directive | Default | Effect |
|---|---|---|
| `SystemCallFilter=` | unset | Space-separated syscall names or named groups (e.g. `@system-service`). Default is allow-list semantics (only listed calls permitted); leading `~` inverts to deny-list. Repeatable (masks merge). `execve`, `exit`, `exit_group`, `getrlimit`, `rt_sigreturn`/`sigreturn`, and time/sleep syscalls are always implicitly allowed. Denied calls get `SIGSYS` by default (configurable via `SystemCallErrorNumber=`). `+`-prefixed commands are exempt. |
| `SystemCallArchitectures=` | empty (no filtering) | Restricts which ABIs' syscalls are permitted — `native` plus any listed archs, or the special value `native` alone. On x86/x86-64 dual-ABI systems, secondary ABIs can be used to bypass a syscall filter defined for the native ABI unless disabled — **`SystemCallArchitectures=native` should almost always accompany `SystemCallFilter=`.** |
| `@system-service` group | — | The recommended baseline allow-list group: "a reasonable set of system calls used by common system services, excluding any special purpose calls." Other notable groups: `@basic-io`, `@network-io`, `@privileged`, `@mount`, `@raw-io`, `@resources`. Full canonical group membership lives in `systemd.exec(5)` § SYSTEM CALL FILTERING (large table, changes across systemd releases — don't hardcode group contents, reference by name). |

### Misc

| Directive | Default | Effect |
|---|---|---|
| `UMask=` | `0022` (system units) | Controls `umask(2)` for the unit; user-unit default is inherited from the per-user manager. |
| `RestrictSUIDSGID=` | `off` | Denies any `chmod`/creation attempt that sets SUID/SGID bits on files or dirs. Implied by `DynamicUser=`. |
| `RestrictRealtime=` | `false` | Refuses `SCHED_FIFO`/`SCHED_RR`/`SCHED_DEADLINE` scheduling — prevents CPU-monopolization DoS. |
| `MemoryDenyWriteExecute=` | `false` | Blocks `mmap(PROT_EXEC+PROT_WRITE)`, `mprotect`/`pkey_mprotect` adding `PROT_EXEC`, and `shmat(SHM_EXEC)`. Breaks JIT engines, executable stacks, C-compiler "trampolines." Can be bypassed via a writable non-`noexec` filesystem (e.g. `/dev/shm`) or `memfd_create()` — combine with `InaccessiblePaths=/dev/shm` and syscall filtering for real effect. |
| `LockPersonality=` | `off` | Locks the `personality(2)` syscall so the kernel execution domain (ABI personality) can't be changed away from default/`Personality=`. |

## 2. A reasonably hardened template

```ini
[Service]
# Identity / privilege
DynamicUser=yes
NoNewPrivileges=yes
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE

# Filesystem
ProtectSystem=strict
ProtectHome=true
PrivateTmp=yes
ReadWritePaths=/var/lib/myapp
StateDirectory=myapp

# Kernel / hardware surface
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
PrivateDevices=yes
ProtectProc=invisible
ProcSubset=pid

# Network (daemon needs the network, so no PrivateNetwork)
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6

# Syscalls
SystemCallFilter=@system-service
SystemCallArchitectures=native

# Misc
RestrictSUIDSGID=yes
RestrictRealtime=yes
MemoryDenyWriteExecute=yes
LockPersonality=yes
UMask=0077
```

A safe starting point for a typical network-facing daemon. `DynamicUser=` alone implies
several other directives listed above, but they're spelled out explicitly here to
document intent for a future reader.

What commonly breaks and why:

- **`ProtectHome=true`** — breaks anything that reads a real user's `$HOME`, dotfiles, or
  SSH keys (backup tools, user-facing agents). Relax to `read-only` (backup services) or
  drop the directive if the daemon must touch `/home`.
- **`PrivateNetwork=true`** (not in the template, but the single most commonly-misapplied
  directive) — breaks *any* network-facing service outright; only appropriate for
  purely local/offline workers.
- **`ProtectSystem=strict`** — breaks services that write outside their state dir
  (installers, self-updaters, ones writing PID files to non-standard paths). Fix by
  adding the path to `ReadWritePaths=`, not by dropping to `full`/`false`.
- **`SystemCallFilter=@system-service`** — breaks services needing calls outside that
  group (containers needing `@mount`, low-level I/O tools needing `@raw-io`). Forgetting
  one required syscall causes a segfault/`SIGSYS` at an arbitrary, possibly
  hard-to-reproduce moment, not a clean startup failure — debug with `systemctl
  log-level debug` and check the journal for the specific blocked syscall. **[Arch]**
- **`MemoryDenyWriteExecute=yes`** — breaks JIT-based runtimes (Java, Node,
  V8/Chromium embedders, .NET, LuaJIT, PHP-with-JIT).
- **`DynamicUser=yes`** — breaks anything expecting a stable/known UID (bind-mount
  ownership checks, some socket-permission schemes); must pair with `*Directory=`
  settings or persistent storage silently doesn't persist correctly across restarts.
  **[Arch]**
- **`ProtectClock=yes`** — reported to break `smartctl` and similar hardware-clock-adjacent
  tools even though it's "supposed" to be safe. **[Arch]**
- **`RestrictAddressFamilies=`** without `AF_UNIX` — breaks local IPC/`syslog(2)`-adjacent
  logging paths; always include `AF_UNIX` unless the service never uses local sockets.
- **`ProcSubset=pid`** — very aggressive; breaks anything reading non-process `/proc`
  APIs (e.g. `/proc/cpuinfo`, `/proc/meminfo` consumers). Treat as opt-in for narrow
  cases, not a default.

## 3. systemd-analyze security <unit>

Analyzes the security/sandboxing settings of one or more service units. With a unit name
given, shows a detailed per-directive breakdown; with none, shows a terse table for all
loaded long-running services. Each checked setting contributes to an **overall exposure
level in the range 0.0–10.0** (low = tightly sandboxed, high = little sandboxing
applied). `--threshold=N` (0–100 scale) makes the command exit non-zero if the unit's
exposure exceeds it — usable as a CI gate.

Man-page caveat (condensed): a high exposure level neither means there's no effective
sandboxing applied by the service code itself, nor that the service is actually
vulnerable — it indicates the service might benefit from additional settings.
Conversely a low score is not proof of safety: the tool only scores per-service
systemd-implemented mechanisms, not application-level mitigations, and settings can be
undone by the service's own code if it retains relevant privileges (e.g. mount
capability can undo several sandboxing options). It also doesn't account for IPC (e.g.
D-Bus) access to *other* unprivileged-looking services that could perform the restricted
operation on the analyzed unit's behalf.

**[Arch]** practical caveat: the score is "slightly misleading" — only a trivial `Hello
world` unit can approach a perfect score; no real application can enable every
sandboxing directive simultaneously. Don't chase a numeric target — use the tool to see
which unused directives are cheap wins.

Example output line format: `✗ PrivateNetwork=  Service has access to the host's
network  0.5`, ending with `→ Overall exposure level for X.service: 4.1 OK`. The
glyphs are visual aids, not machine-parseable status beyond exit code + `--threshold`.

## 4. Resource control (systemd.resource-control)

| Directive | Effect |
|---|---|
| `CPUQuota=` | Percentage (e.g. `20%`) of one CPU's time, max, across all cores if `>100%`. Maps to `cpu.max`/`cpu.cfs_quota_us`. Empty value unsets. |
| `MemoryMax=` / `MemoryHigh=` | `MemoryMax=` is the **hard** limit — OOM killer invoked inside the unit's cgroup if exceeded, no negotiation. `MemoryHigh=` is a **throttling** limit — usage may exceed it under unavoidable pressure but the cgroup gets heavily slowed/reclaimed; this is the recommended *primary* control, with `MemoryMax=` as the hard backstop. Both take bytes (K/M/G/T, base 1024) or a percentage of physical RAM; `infinity` disables. `Startup*` variants apply during boot/shutdown only. Effective values reported via `EffectiveMemoryMax=`/`EffectiveMemoryHigh=` (capped by parent slices and physical RAM). |
| `TasksMax=` | Caps `pids.max` — absolute count or percentage of the system-wide task limit; `infinity` disables. System default configurable via `DefaultTasksMax=` in `systemd-system.conf`. |
| `IOWeight=` / `IOReadBandwidthMax=` (& `IOWriteBandwidthMax=`) | `IOWeight=` (1–10000, default 100) sets relative `io.weight` — available I/O bandwidth is split among sibling units in a slice proportional to weight; relative prioritization, not an absolute cap. `IOReadBandwidthMax=`/`IOWriteBandwidthMax=` set absolute bytes/sec caps per-device instead. `StartupIOWeight=` mirrors the CPU/Memory startup-phase pattern. |
| `Slice=` | Places the unit in a slice (cgroup subtree) for hierarchical resource control. Defaults to `system.slice` for non-instantiated units of any type; instantiated units default into a subslice named after the template. User session units nest under `user.slice` → `user-$UID.slice` → per-session/app scopes. |
| `OOMPolicy=` | `continue` (log & keep running), `stop` (log, cleanly terminate unit), `kill` (log, and set `memory.oom.group=1` so the kernel kills *all* remaining processes in the unit's cgroup together) — governs both kernel-OOM and `systemd-oomd.service` userspace-OOM kills. `stop`/`kill` land the unit in the `oom-kill` failed state, after which `Restart=` policy can kick in. |

Slice nesting in practice: `system.slice` holds system services, `user.slice` holds all
logged-in user sessions (each user gets `user-$UID.slice`), and `machine.slice` holds
VMs/containers under `systemd-machined`. Resource settings on a slice apply as
caps/shares to the whole subtree — set `CPUQuota=`/`MemoryMax=` on a slice to bound a
*group* of services collectively, not just one.

## Gaps / not independently re-verified

The full canonical membership list of `@system-service` and sibling syscall-filter
groups lives in a large table in `systemd.exec(5)` § SYSTEM CALL FILTERING that wasn't
reproduced verbatim here (long, changes across systemd versions) — reference it live
rather than hardcoding group contents into generated config.
