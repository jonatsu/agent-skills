---
name: systemd
description: "Reference and troubleshooting guide for systemd: unit files, services, timers, journald/journalctl, sandboxing/hardening, cgroup resource control, socket activation, and systemd-networkd/systemd-resolved. Use to write, edit, review, harden, or debug unit files (.service, .timer, .socket, .target, .mount, .path, .slice), configure systemd-networkd (.network, .netdev, .link) or systemd-resolved (DNS, resolvectl), diagnose failed/masked units, read journalctl, or interpret systemd-analyze verify/blame/critical-chain/security output. Triggers: systemd, systemctl, journalctl, journald, unit file, timer unit, socket unit, target unit, .service, .timer, .socket, .target, .network, .netdev, .link, networkd, resolved, resolvectl, networkctl, systemd-analyze, ExecStart, WantedBy, OnCalendar, drop-in, daemon-reload, ProtectSystem, NoNewPrivileges, DynamicUser, socket activation, cgroup, ordering cycle, masked unit, service won't start."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# systemd

IRON LAW: NEVER HAND-EDIT A UNIT FILE OR .network/.netdev/.link FILE UNDER A VENDOR/PACKAGE-OWNED PATH (`/usr/lib/systemd/...`). ALWAYS PLACE NEW OR OVERRIDDEN CONFIG UNDER `/etc/systemd/...` (`systemctl edit` / a `.d/` drop-in), AND ALWAYS CALL OUT `systemctl daemon-reload` (or `networkctl reload`) WHEN AN ALREADY-LOADED UNIT'S ON-DISK DEFINITION CHANGES. A vendor-path edit is silently discarded on the next package upgrade, and a missed reload makes a fix look like it "didn't work" when it simply never took effect.

## Workflow

Copy this checklist and check off items as you complete them:

```text
systemd Progress:

- [ ] Step 1: Identify the task category ⚠️ REQUIRED
- [ ] Step 2: Load the matching reference file(s) before writing directives from memory ⛔ BLOCKING
- [ ] Step 3: Author, review, or debug using the loaded reference
- [ ] Step 4: Verify before declaring done ⚠️ REQUIRED
  - [ ] 4.1 `systemd-analyze verify` on any authored/edited unit file
  - [ ] 4.2 `systemd-analyze security <unit>` if hardening directives were added/changed
  - [ ] 4.3 `systemctl status` + `journalctl -xeu <unit>` if debugging a failure
- [ ] Step 5: Confirm before executing changes on a live/production system ⚠️ REQUIRED (conditional — see below)
```

## Step 1: Identify the Task Category

Ask: which of these does the task actually need?

| Category | Load |
|---|---|
| Unit anatomy, `[Unit]`/`[Install]`, dependency directives (`Wants=`/`Requires=`/`After=`...), specifiers, safe overrides, `systemctl enable`/`daemon-reload` | `references/units-and-dependencies.md` |
| `systemd.service` specifics: `Type=`, `Exec*=`, `Restart=`, timeouts, `User=`/environment | `references/services-and-execution.md` |
| Timers, `OnCalendar=` syntax, `Persistent=`, timers vs cron | `references/timers-and-scheduling.md` |
| journald config, `journalctl` filters, persistent journal, structured logging | `references/journald-and-logging.md` |
| Sandboxing/hardening directives, `systemd-analyze security`, cgroup resource control | `references/sandboxing-and-hardening.md` |
| Socket-activated services (`.socket`, `LISTEN_FDS`, `Accept=`) | `references/socket-activation.md` |
| A unit/service won't start, is masked, is in a weird state, boot is slow, ordering cycle | `references/troubleshooting.md` |
| `systemd-networkd`: `.network`/`.netdev`/`.link`, static IP, DHCP, bridges, VLANs | `references/networkd.md` |
| `systemd-resolved`: DNS, `resolved.conf`, split-DNS, `resolvectl`, `/etc/resolv.conf` modes | `references/resolved.md` |

Most real tasks touch 2+ of these (e.g. "write a hardened timer-triggered backup job"
needs `services-and-execution.md` + `timers-and-scheduling.md` +
`sandboxing-and-hardening.md`). Load all that apply — don't guess at directive names or
defaults for a category whose reference hasn't been loaded yet.

## Step 2: Load Before Writing ⛔ BLOCKING

Ask: is every directive name, default value, and section placement in the answer
something just confirmed against a loaded reference (or the man page), or is any of it
recalled from general training-data familiarity with systemd?

systemd's directive surface is large, versioned, and full of easy-to-invent-sounding
names that don't actually exist (or exist with different semantics than expected —
`Wants=` vs `Requires=` vs `BindsTo=` is the single most common confusion, see
`references/units-and-dependencies.md` §3). Treat unverified recall as a guess, not an
answer.

## Step 3: Author, Review, or Debug

Use question-style diagnosis rather than jumping to a fix:

- Writing a unit: what `Type=` does this daemon actually need (does it fork? call
  `sd_notify()`? exit after one run?), and does `[Install]` have the right
  `WantedBy=`/`RequiredBy=` for how it should be pulled in?
- Reviewing a unit: is every `Wants=`/`Requires=` paired with the `After=` it needs, or
  is an ordering assumption being made that the directive doesn't actually provide (see
  `references/units-and-dependencies.md` §3)?
- Hardening a unit: which directives from `references/sandboxing-and-hardening.md` §1
  actually fit what this specific daemon does (network? home-dir access? JIT?), not a
  copy-pasted maximal template?
- Debugging a failure: what do LOAD/ACTIVE/SUB actually say (`references/troubleshooting.md`
  §1), not just "is it green"?

## Step 4: Verify Before Declaring Done ⚠️ REQUIRED

- Any authored or edited unit file: run (or tell the user to run)
  `systemd-analyze verify <file>` — this is the equivalent of a linter/typecheck and
  catches unknown directives, bad references, and missing `ExecStart=` before deploy.
- Any hardening/sandboxing change: run `systemd-analyze security <unit>` and read the
  result as "what's a cheap additional win," not as a pass/fail gate — a low score is
  not proof of safety and a high score is not proof of danger (see
  `references/sandboxing-and-hardening.md` §3).
- Any failure-diagnosis task: don't conclude a root cause without having actually looked
  at `systemctl status` output and `journalctl -xeu <unit>` — decode the specific
  `code=exited`/`code=killed` status shown, don't guess from the unit name alone (see
  `references/troubleshooting.md` §2 and §8).

## Step 5: Confirm Before Executing on a Live System ⚠️ REQUIRED (conditional)

If the task involves actually *running* commands against a live/production host (not
just authoring/reviewing files), stop and confirm before:

- Restarting, stopping, or masking any service whose blast radius isn't fully known.
- Applying `systemd-networkd`/`systemd-resolved` config changes on a host reached over
  SSH/remote access — reconfiguring the network interface or DNS in use for the current
  connection can cut that connection.
- Any change described as "destructive/hard-to-reverse" by the top-level guidance this
  skill operates under (mask, unit deletion, resetting `/etc/resolv.conf`, etc.).

Authoring the config and recommending the command is in scope without asking; actually
executing it against a real running system is not, unless already authorized for that
scope.

## Anti-Patterns to Avoid

- Inventing a directive name or assuming its default without checking the loaded
  reference — systemd has hundreds of directives across unit types and many have
  non-obvious defaults (e.g. `RestartSec=100ms`, `TimeoutStartSec=90s`,
  `ProtectHome=false`).
- Hand-editing `/usr/lib/systemd/system/*.service` or `/usr/lib/systemd/network/*` —
  always use `/etc/systemd/system/` (or `systemctl edit`) / `/etc/systemd/network/`.
- Setting `Wants=`/`Requires=` and assuming it also orders startup — it doesn't; pair
  it with `After=`/`Before=` explicitly whenever ordering is actually needed.
- Recommending a maximal sandboxing template (every directive in
  `references/sandboxing-and-hardening.md` §1 at once) without checking which ones the
  specific service actually needs — `PrivateNetwork=true` on a network daemon or
  `MemoryDenyWriteExecute=yes` on a JIT runtime breaks the service outright.
- Declaring a unit file "correct" without having run or recommended
  `systemd-analyze verify`.
- Treating `systemctl restart`'s success as proof a config change took effect, without
  confirming `daemon-reload` happened first for a hand-edited already-loaded unit.
- Restarting `systemd-networkd`/`NetworkManager`/`systemd-resolved` on a remote host as
  a casual troubleshooting step without flagging the connectivity risk first.
- Reading only the `ACTIVE` field of unit state and ignoring `LOAD`/`SUB` — a unit can
  be `masked` (LOAD) or `failed` (SUB) in ways `ACTIVE` alone doesn't distinguish.

## Pre-Delivery Checklist

- [ ] Every directive name/default/section used was confirmed against a loaded
      reference file (or primary-source man page), not recalled unverified
- [ ] Any new/edited unit or network file targets `/etc/systemd/...`, never
      `/usr/lib/systemd/...`
- [ ] `daemon-reload`/`networkctl reload` called out explicitly wherever an
      already-loaded unit's definition changed
- [ ] `systemd-analyze verify` run or recommended for any authored/edited unit file
- [ ] `Wants=`/`Requires=` paired with a matching `After=`/`Before=` wherever ordering
      is actually required (not left implicit)
- [ ] Hardening directives chosen for what the specific service needs, not
      copy-pasted wholesale from the template
- [ ] Live-system execution (not just authoring) confirmed with the user first if it
      touches service state or network/DNS config on a reachable host
