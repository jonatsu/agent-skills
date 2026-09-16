---
name: systemd-networking
description: Configure and troubleshoot Linux networking and DNS with systemd-networkd and systemd-resolved. Use for .network, .netdev, .link, resolved.conf, interface matching, DHCP, routes, bridges, bonds, VLANs, per-link DNS, or unexpected resolver routing. Diagnose with networkctl and resolvectl while checking which network manager owns the configuration. Use systemd for service units and lifecycle problems.
license: MIT
compatibility: Requires Linux with systemd-networkd or systemd-resolved; commands and settings vary by systemd version.
metadata:
  author: Joonas Onatsu
---

# systemd Networking

Use this skill for systemd-networkd link configuration and systemd-resolved DNS routing. Use the `systemd` skill for
unit files, service lifecycle, timers, sockets, hardening, and general journal diagnosis.

Treat the target host's manual pages as authoritative. Record `systemd --version` and consult the installed
`systemd.network(5)`, `systemd.netdev(5)`, `systemd.link(5)`, `networkctl(1)`, `resolved.conf(5)`, and `resolvectl(1)`
documentation before choosing settings or apply commands.

## Establish Ownership and Access

Identify the component that owns each interface and `/etc/resolv.conf` before changing configuration:

```text
networkctl list
networkctl status INTERFACE
resolvectl status
readlink -f /etc/resolv.conf
```

Check NetworkManager, netplan, distribution generators, container tooling, or cloud provisioning when present. Do not
configure the same interface through two managers. Generated files may identify their source; edit the source system
instead of the generated output.

Determine whether the host is local or reached through the interface or DNS path being changed. A remote network
change needs an independent recovery path or an explicit rollback procedure. Reuse authorization already present in
the request, and ask before applying a change when loss of access remains plausible.

## Configure systemd-networkd

Place persistent administrator files under `/etc/systemd/network/`. Do not edit package-owned files in lower-priority
directories. Choose filenames after inspecting every configured search directory because matching and lexicographic
precedence vary by file type.

Keep each file type's responsibility clear:

- `.link` selects low-level link properties during udev processing;
- `.netdev` creates a virtual network device; and
- `.network` matches an existing link and assigns addresses, routes, DHCP behavior, DNS data, or membership in a
  virtual device.

Test match assumptions against observed interface names, permanent addresses, drivers, and paths. For `.network`
files, the first matching file wins; later matching files do not merge. Avoid a broad early filename that captures an
interface intended for a more specific file.

Model virtual devices as a complete graph. A bridge, bond, or VLAN may need both the `.netdev` that creates it and
`.network` files that configure the virtual device and attach its member links. Assign layer-3 configuration to the
interface that should own the address rather than to every member.

Apply changes according to file type and installed version:

- Use `networkctl reload` to reload `.network` and `.netdev` definitions when the local manual documents that
  behavior. Use `networkctl reconfigure INTERFACE` when the target version requires or benefits from an explicit
  reconfiguration.
- A `.link` change is handled by udev. Reloading networkd does not retroactively apply it. Follow the installed
  `systemd.link(5)` and `udevadm(8)` instructions, then use a controlled device event, replug, or reboot as appropriate.
- Some virtual-device properties are fixed at creation. Confirm whether the device must be recreated, and treat that
  operation as disruptive.

Do not restart a network manager as a default apply step. Confirm the supported reload path and verify the resulting
addresses, routes, carrier, and reachability.

## Configure systemd-resolved

Use a drop-in under `/etc/systemd/resolved.conf.d/` for global administrator settings. Prefer per-link DNS and routing
domains when different links serve different namespaces. A route-only domain starts with `~`; `~.` routes otherwise
unmatched DNS queries to that link or server set.

Global file changes normally require an authorized restart of `systemd-resolved`; confirm the installed unit has no
supported reload operation before choosing the command. Per-link changes made through `resolvectl` take effect at
runtime and may later be replaced by the network manager that owns the link.

Inspect the current `/etc/resolv.conf` mode before replacing its symlink or contents. The stub, uplink, and externally
managed modes expose different behavior to applications. Preserve the mode required by the host's network manager and
application stack.

Diagnose resolution by comparing configuration with an actual query:

```text
resolvectl status
resolvectl dns INTERFACE
resolvectl domain INTERFACE
resolvectl query NAME
```

Check which link and protocol answered, whether the expected search or route-only domain is present, and whether
DNSSEC or DNS-over-TLS policy rejected the response. Do not weaken validation merely to clear an error; identify
whether the upstream resolver, local policy, or zone data caused it.

## Protect Secrets

Do not place private WireGuard keys or other credentials in output, logs, or world-readable files. Prefer the
credential mechanism documented by the installed systemd version. When a file is required, restrict ownership and
permissions for the account that reads it.

## Verify the Outcome

Verify the specific layer changed:

- link ownership, setup state, carrier, and addresses with `networkctl status` and `ip`;
- routes with `ip route` and `ip -6 route`;
- DHCP or address acquisition in the networkd journal;
- DNS servers and routing domains with `resolvectl status`;
- forward and reverse queries with `resolvectl query`; and
- application reachability through the intended interface and resolver path.

After a remote change, keep the recovery channel available until these checks pass. Report partial validation when
the environment does not permit a real link, route, DNS, or connectivity test.

## Primary References

- `man systemd.network`, `man systemd.netdev`, `man systemd.link`, and `man networkctl`
- `man systemd-resolved`, `man resolved.conf`, and `man resolvectl`
- [Upstream systemd manual](https://www.freedesktop.org/software/systemd/man/latest/)
