# Socket Activation

Source: `systemd.socket(5)`, `sd_listen_fds(3)`, `systemd-analyze(1)` — systemd GitHub
`main` branch DocBook source.

## 1. Core concept

Socket activation lets systemd own the act of *listening* on a socket (or FIFO)
independently of the daemon process that will eventually handle it:

- **On-demand start**: the daemon process doesn't need to be running at all until the
  first connection/datagram arrives — systemd starts it lazily.
- **Parallelized boot**: dependent services don't have to wait for the daemon to
  initialize before *they* can connect — the connection just queues at the kernel socket
  level while systemd starts the daemon in parallel with everything else. This breaks a
  huge class of ordering dependencies during boot.
- **Restart resilience**: because the listening socket is owned by systemd (a `.socket`
  unit), a daemon crash/restart doesn't drop already-queued/established connections —
  clients don't see connection refused during a restart window.

The mechanism: systemd creates and binds the socket(s) itself (as configured in a
`.socket` unit), then **passes the already-open file descriptor(s)** to the spawned
service process via standard `fork`+`exec` fd-inheritance, setting two environment
variables the daemon reads at startup:

- `LISTEN_PID` — the PID the fds were meant for (a sanity check so a fd doesn't get
  misused after an `exec` chain).
- `LISTEN_FDS` — the number of fds passed.

Per `sd_listen_fds(3)`: fd numbering is always contiguous starting at 3
(`SD_LISTEN_FDS_START`; fds 0–2 remain stdin/stdout/stderr). Use the library call
instead of hand-parsing the env vars — it validates `LISTEN_PID` against the caller's
own PID and clears the env vars after first use (by default) so they don't leak to
child processes.

## 2. systemd.socket key directives

| Directive | Effect |
|---|---|
| `ListenStream=` / `ListenDatagram=` / `ListenSequentialPacket=` | Address to listen on for `SOCK_STREAM` / `SOCK_DGRAM` / `SOCK_SEQPACKET`. Address forms: absolute path starting with `/` → `AF_UNIX` filesystem socket; `@name` → `AF_UNIX` abstract-namespace socket (`@` replaced with NUL before binding); `host:port`, `port`, or IPv6 forms → `AF_INET`/`AF_INET6` TCP/UDP. Repeatable — one `.socket` unit can listen on multiple addresses. |
| `ListenFIFO=` | Listen on a named pipe path instead of a socket — same activation model, useful for simple one-way IPC. |
| `Accept=` | **`no`** (default): all listening sockets are passed to one spawned service instance, which must `accept()` connections itself — one long-lived service handles everything. **`yes`**: systemd `accept()`s each connection itself and spawns a *separate* instance of a templated service (`foo@.service`) per connection, handing that instance only the one connected socket. Ignored for datagram sockets and FIFOs — a single service unconditionally handles all traffic regardless. |
| `SocketMode=` | Octal file-mode for filesystem `AF_UNIX` socket/FIFO/message-queue nodes on creation. Default `0666`. |
| `Service=` | Explicitly names the service unit to activate on traffic; only valid with `Accept=no`. Defaults to the same-named `.service` unit — override only when a non-matching name is needed. |

## 3. Minimal `.socket` + `.service` pairs

**`Accept=no`** — one long-running service handles all connections itself (recommended
default for performance-sensitive daemons — activation cost paid once):

```ini
# /etc/systemd/system/echo.socket
[Unit]
Description=Echo server socket

[Socket]
ListenStream=127.0.0.1:7777

[Install]
WantedBy=sockets.target
```

```ini
# /etc/systemd/system/echo.service
[Unit]
Description=Echo server

[Service]
ExecStart=/usr/local/bin/echo-server
# reads LISTEN_FDS / calls sd_listen_fds(), accept()s in a loop itself
```

Tradeoff: the daemon must implement its own multiplexed accept loop (or use an
event-loop library that does), but pays the systemd activation/startup cost exactly once
regardless of connection volume.

**`Accept=yes`** — one instance per connection, via a templated service:

```ini
# /etc/systemd/system/echo.socket
[Unit]
Description=Echo server socket (per-connection)

[Socket]
ListenStream=127.0.0.1:7777
Accept=yes

[Install]
WantedBy=sockets.target
```

```ini
# /etc/systemd/system/echo@.service
[Unit]
Description=Echo server connection %i

[Service]
ExecStart=/usr/local/bin/echo-worker
StandardInput=socket
```

Here systemd itself calls `accept()`, and each connection gets its own
`echo@<N>.service` instance receiving only that one connected socket on fd 3 — no
`accept()` loop needed in the daemon at all. Tradeoff: simpler per-connection code and
stronger isolation (each connection's sandboxing directives apply independently), at the
cost of one service-spawn's worth of overhead per connection — a poor fit for
high-connection-rate services, a good fit for sporadic/low-volume or security-sensitive
protocols.

## 4. Testing and inspection

- `systemctl list-sockets` — lists all `.socket` units, their listen addresses, and the
  unit they'll activate; confirms a socket is actually loaded/listening before testing.
- Trigger activation by simply connecting to the configured address (`nc 127.0.0.1
  7777`, `curl`, etc.) — the first connection causes systemd to start the paired service
  if it isn't already running; `systemctl status foo.service` immediately afterward
  should show it transitioned to active.
- `journalctl -u foo.socket -u foo.service` — correlate socket-level activation events
  with the service's own startup log lines when debugging why activation didn't fire or
  the service failed post-activation.
