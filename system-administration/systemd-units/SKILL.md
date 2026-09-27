---
name: systemd-units
description: Write, review, harden, and debug Linux systemd units. Use for .service, .timer, and .socket files, drop-ins, dependencies, failed system or user services, journal diagnosis, and resource controls. Use systemd-networking for networkd link configuration and resolved DNS routing.
license: MIT
compatibility: Requires Linux with systemd and its command-line tools; available directives vary by systemd version.
metadata:
  author: Joonas Onatsu
---

# systemd Units

Use the target system's manual pages and installed tools as the authority. A directive available in upstream's
latest documentation may not exist on the target host. Start by recording `systemd --version`, then consult the
relevant local manual page such as `systemd.unit(5)`, `systemd.service(5)`, `systemd.exec(5)`, or
`systemd.timer(5)`.

This skill covers system and user units, service lifecycle, dependencies, timers, sockets, journal-based diagnosis,
sandboxing, and cgroup resource controls. Use the separate `systemd-networking` skill for systemd-networkd,
systemd-resolved, `.network`, `.netdev`, and `.link` configuration.

## Establish the Target

Determine these facts before editing or diagnosing:

- the target systemd version and distribution;
- whether the system manager or a user manager owns the unit;
- the effective unit definition, including drop-ins;
- whether the task is static authoring, offline image work, or a live-host change; and
- which state-changing commands the user has already authorized.

Inspect the effective definition with `systemctl cat UNIT` or `systemctl --user cat UNIT`. Use
`systemctl show UNIT` when exact properties matter. Do not infer the active configuration from one file on disk.

## Put Configuration in the Correct Scope

Never edit package-owned unit files. Choose the local configuration location from the manager and lifetime:

- System manager: use `/etc/systemd/system/` for persistent files and `/run/systemd/system/` for runtime files.
- Current user's manager: use `${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user/` for persistent files and
  `$XDG_RUNTIME_DIR/systemd/user/` for runtime files.
- All user managers: find the persistent path with `systemd-path systemd-user-conf`; inspect the target's unit search
  path for other locations.

Prefer `systemctl edit UNIT` or `systemctl --user edit UNIT` for a small override. Use `--full` only when a drop-in
cannot express the change. List-valued service commands such as `ExecStart=` may require an empty assignment before
the replacement; confirm reset behavior in the directive's manual page.

After a hand edit, reload the same manager that owns the unit:

- system manager: `systemctl daemon-reload`
- user manager: `systemctl --user daemon-reload`

`systemctl edit` normally reloads the selected manager itself. Application configuration changes do not require
`daemon-reload`; reload or restart the application only when its own behavior requires it.

## Author Units from Behavior

Choose directives from the program's actual lifecycle and dependencies:

- Select `Type=` from the program's readiness behavior. Use `notify` only when the program sends systemd readiness
  notifications, and use `forking` only for a daemon that forks into the background.
- Treat dependency and ordering as separate decisions. `Wants=` and `Requires=` pull units into a transaction;
  `After=` and `Before=` order jobs. Add ordering only when one unit must wait for another.
- Keep a timer and its activated service separate. Test calendar expressions with `systemd-analyze calendar`, and
  ensure a recurring timer's target can become inactive before the next activation.
- Confirm whether a socket-activated program accepts inherited file descriptors. A `.socket` unit cannot make an
  arbitrary daemon socket-aware.
- Use directory directives such as `StateDirectory=` when systemd should create and own service storage. Avoid
  embedding secrets in `Environment=` because unit properties and process environments may expose them.

Do not copy a generic hardening block into a service. Start with the service's required files, devices, address
families, capabilities, syscalls, writable paths, and runtime behavior. Add restrictions incrementally and exercise
the real workload after each meaningful group of changes. Treat `systemd-analyze security` as a list of possible
improvements, not a safety verdict or universal score target.

## Diagnose from Observed State

Collect evidence that is available for the reported failure. On a live host, the usual starting set is:

```text
systemctl status UNIT
systemctl show UNIT -p LoadState -p ActiveState -p SubState -p Result
journalctl -u UNIT --since TIME
```

Use `--user` with `systemctl` for a user unit. Use `journalctl --user-unit=UNIT` when the journal supports user-unit
filtering. Ask for `journalctl -xeu UNIT` only when catalog explanations and the end of the current log are useful;
`-x` adds generated explanatory text that should usually be omitted from bug reports.

Follow the evidence:

- `LoadState=not-found` points to naming, installation, or search-path problems.
- `LoadState=masked` means a `/dev/null` mask blocks activation.
- an exit status in systemd's 200-range usually means process setup failed before the executable ran; decode the
  exact value with `systemd.exec(5)` on the target version;
- repeated fast failures may reach the start-rate limit; inspect the earlier failure before using `reset-failed`;
- a unit that never receives a start job may have a dependency, condition, assertion, or transaction problem; and
- slow boot diagnosis needs `systemd-analyze critical-chain` or `plot`; `blame` alone does not identify the critical
  path.

If the user supplied sufficient status and journal output, analyze it directly. Do not require redundant live-host
access. When the target is unavailable, state which diagnosis remains unverified and provide the exact read-only
command that would settle it.

## Validate in the Target Environment

Run `systemd-analyze verify FILE...` for authored or edited units against the target systemd version and filesystem.
A check on another distribution may reject valid target directives or resolve users, executables, and dependencies
differently. Use the target host, a matching image, or the tool's supported offline options when those differences
matter.

For a live change, verify the outcome that the task requires:

- inspect the merged unit after reload;
- start, reload, or restart only when already authorized;
- read status and relevant journal entries after activation;
- exercise the service's real behavior; and
- inspect resource or sandbox effects when those settings changed.

Before stopping, restarting, masking, or otherwise changing a live unit, reuse authorization already present in the
request. Ask first when the command's target, blast radius, or authorization remains unclear. Never present a static
validation result as proof that the service works at runtime.

## Primary References

- `man systemd.unit`, `man systemd.service`, `man systemd.exec`, `man systemd.timer`, and `man systemd.socket`
- `man systemctl`, `man journalctl`, and `man systemd-analyze`
- [Upstream systemd manual](https://www.freedesktop.org/software/systemd/man/latest/)
