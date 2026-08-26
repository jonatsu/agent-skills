# systemd-networkd

Reference for `systemd-networkd`, the system service that manages network links,
creates virtual devices, and assigns addresses/routes. Sources: `systemd.network(5)`,
`systemd.netdev(5)`, `systemd.link(5)`, `systemd-networkd.service(8)`, `networkctl(1)`
(systemd upstream GitHub source), cross-checked against the ArchWiki "Systemd-networkd"
page — man pages win on conflicts (noted inline as **[Arch]**).

## Contents

1. File types and precedence
2. `[Match]` section and file precedence
3. `.network` sections: static IP, DHCP, common options
4. `.netdev` examples: bridge and VLAN
5. `networkctl`: applying config changes
6. Interaction with NetworkManager

## 1. File types and precedence

Three config file types, all ini-style, read from four directories in ascending
priority: `/usr/lib/systemd/network/` (vendor) < `/usr/local/lib/systemd/network/` <
`/run/systemd/network/` (runtime) < `/etc/systemd/network/` (highest, local admin).
Files across all four directories are **collectively sorted and processed in one
alphanumeric order by filename**, regardless of which directory they live in.
Convention: prefix filenames with a two-digit number (e.g. `10-eth0.link`); keep numbers
below `70` to leave room for OS-generated/higher-priority local drop-ins. Drop-ins live
in `<file>.d/*.conf` alongside the main file and are merged in their own lexical order,
applied after the main file.

Processing order matters because of **when** each type is applied:

- **`.link`** — applied earliest, by `systemd-udevd`'s `net_setup_link` builtin, during
  the udev device event for the NIC — i.e. *before* the kernel/userspace interface
  renaming takes final effect. Governs low-level, one-time device properties: MAC
  address policy and interface naming policy. An empty file or a symlink to `/dev/null`
  disables it entirely for matched devices.
- **`.netdev`** — creates virtual network devices (bridge, bond, vlan, veth, wireguard,
  tun/tap, dummy, macvlan, vxlan, etc.) respecting their own `[Match]` sections against
  the *environment* (not the device — netdevs don't exist yet).
- **`.network`** — assigns configuration (addresses, routes, DHCP, DNS, bridge/VLAN/bond
  membership) to whichever already-named interface matches its `[Match]` section. Runs
  last in the pipeline, after `.link` naming and after any `.netdev` virtual devices
  exist.

ArchWiki confirms the same three-file model and adds the practical rule of thumb: "if
all conditions in the `[Match]` section are matched, the profile is activated; an empty
`[Match]` section matches everything" — consistent with the man pages.

## 2. [Match] section and file precedence

Common matching keys (all three file types share most of these; `.link` additionally
supports `OriginalName=`, `.network`/`.netdev` support `Kind=`/`SSID=`/`BSSID=`):

| Key | Matches on |
|---|---|
| `Name=` | Device name (shell-style glob), via udev `INTERFACE` property |
| `MACAddress=` | Current hardware address |
| `PermanentMACAddress=` | Permanent (not currently-assigned) MAC address |
| `Driver=` | Kernel driver bound to the device (glob, invertible with `!`) |
| `Type=` | Device type, e.g. `ether`, `wlan`, `loopback`, `wwan` (invertible) |
| `Kind=` | Netdev kind, e.g. `bond`, `bridge`, `gre` (invertible) |
| `Path=` | `ID_PATH` udev property (persistent bus path), shell-glob |
| `Property=` | Arbitrary `NAME=value` udev property pairs (ANDed, invertible) |
| `Host=` | Hostname or machine ID of the local host (invertible) |
| `Virtualization=` | Whether running under virtualization, and which kind |
| `KernelCommandLine=` | A kernel command-line option is set |
| `Architecture=` | CPU architecture |
| `OriginalName=` | (`.link` only) device name as exposed by udev `INTERFACE` |
| `SSID=`/`BSSID=` | (wireless) currently associated network/AP |

**Precedence rule (exact, from `systemd.network`):** "The first (in alphanumeric order)
of the network files that matches a given interface is applied, all later files are
ignored, even if they match as well." The same first-match-wins rule applies
independently to `.link` files against devices and to `.netdev`/`.network` pairs.
Practical consequence: only one `.network` file ever configures a given interface —
there is no merging across multiple matching `.network` files, so overlapping `Name=`
globs are a common misconfiguration. Ensure no other `.network` file matches the same
`Name=` pattern, since only the first hit is used.

## 3. .network sections: static IP, DHCP, and common options

Static IP example:

```ini
# /etc/systemd/network/20-wired.network
[Match]
Name=enp1s0

[Network]
Address=10.1.10.9/24
Address=2001:db8:1234:5678::1/64
Gateway=10.1.10.1
Gateway=fe80::1
DNS=10.1.10.1
DNS=2001:db8:1122::3344:1
```

DHCP client example:

```ini
# /etc/systemd/network/20-wired.network
[Match]
Name=enp1s0

[Link]
RequiredForOnline=routable

[Network]
DHCP=yes
```

Key `[Network]` options and documented defaults:

| Key | Default | Notes |
|---|---|---|
| `DHCP=` | `no` | `yes`, `ipv4`, `ipv6`, or `no` |
| `Address=` / `Gateway=` / `DNS=` / `Domains=` | unset | repeatable |
| `IPv4Forwarding=` | `true` only if `IPMasquerade=` is enabled for IPv4, else per `networkd.conf` | supersedes the older `IPForward=` |
| `IPv6Forwarding=` | `true` if `IPMasquerade=`/`IPv6SendRA=` enabled, else per `networkd.conf` | |
| `IPMasquerade=` | `no` | `ipv4`, `ipv6`, `both`, `no`; enabling implies forwarding |
| `Bridge=` / `Bond=` / `VLAN=` | unset | enslave this interface / stack a VLAN on it |
| `LLMNR=` | `true` | link must also have global LLMNR on |
| `MulticastDNS=` | `false` | ditto for mDNS |
| `DNSOverTLS=` / `DNSSEC=` | unset | falls back to global `resolved.conf` setting when unset |
| `IPv6AcceptRA=` | `true` | `false` when link is itself sending RAs/forwarding/masquerading |

`[Address]` section: `Address=` (mandatory, CIDR), `Peer=` (point-to-point), `Label=`,
`Scope=` (`global` default, `link`, `host`, or 0-255), `Broadcast=` (default `true`,
derived from `Address=`), `AddPrefixRoute=` (default `true`).

`[Route]` section: `Gateway=`, `Destination=` (CIDR), `Metric=`, `GatewayOnlink=` (treat
gateway as directly reachable without a matching on-link route), `Table=`.

`[DHCPv4]` section: `UseDNS=` (default `true`), `UseDomains=` (default `false`),
`UseRoutes=` (default `true`), `RouteMetric=` (unset → kernel default),
`ClientIdentifier=` (default `duid`).

`[DHCPv6]` section: `UseDNS=` (default `true`), `UseDomains=` (default `false`).

## 4. .netdev examples: bridge and VLAN

Bridge `br0` with two enslaved physical interfaces. The bridge's own `.netdev` file must
sort before the `.network` files that enslave interfaces to it (filename ordering
again):

```ini
# /etc/systemd/network/25-br0.netdev
[NetDev]
Name=br0
Kind=bridge
```

```ini
# /etc/systemd/network/26-enp1s0.network
[Match]
Name=enp1s0

[Network]
Bridge=br0
```

```ini
# /etc/systemd/network/26-enp2s0.network
[Match]
Name=enp2s0

[Network]
Bridge=br0
```

```ini
# /etc/systemd/network/27-br0.network
[Match]
Name=br0

[Link]
RequiredForOnline=routable

[Network]
DHCP=yes
```

The enslaved interfaces must carry no `Address=`/`DHCP=` of their own — the bridge
interface is what gets IP configuration. Ensure no other `.network` file also matches
`enp1s0`/`enp2s0` (only the first match wins, per §2).

VLAN example — a tagged VLAN 10 on top of `enp1s0`:

```ini
# /etc/systemd/network/25-vlan10.netdev
[NetDev]
Name=vlan10
Kind=vlan

[VLAN]
Id=10
```

```ini
# /etc/systemd/network/26-enp1s0.network
[Match]
Name=enp1s0

[Network]
VLAN=vlan10
```

```ini
# /etc/systemd/network/27-vlan10.network
[Match]
Name=vlan10

[Network]
Address=192.168.10.5/24
Gateway=192.168.10.1
```

Other `Kind=` values: `bond`, `dummy`, `gre`/`gretap`/`ip6gre`/`ip6gretap`, `ipip`,
`ipvlan`/`ipvtap`, `macvlan`/`macvtap`, `sit`, `tap`/`tun`, `veth`, `vti`/`vti6`, `vxlan`,
`geneve`, `vrf`, `wireguard`, `wlan`, among others. Each has its own section:
`[WireGuard]` (`PrivateKey=`/`PrivateKeyFile=`, `ListenPort=` — integer or `auto`,
`FirewallMark=`) plus one or more `[WireGuardPeer]` blocks (`PublicKey=`,
`PresharedKey=`, `AllowedIPs=`, `Endpoint=`); `[Bridge]` (`STP=`, `ForwardDelaySec=`,
`Priority=`, `VLANFiltering=`); `[Bond]` (`Mode=`); `[Tun]`/`[Tap]` (`User=`, `Group=`,
`MultiQueue=` default `no`, `PacketInfo=`).

## 5. networkctl: applying config changes

| Command | Effect |
|---|---|
| `networkctl list [PATTERN]` | Table of links: index, name, type, operational state, setup state |
| `networkctl status [IFACE]` | Detailed per-link (or overall) status: addresses, gateway, DNS, driver |
| `networkctl reload` | Re-reads `.netdev`/`.network` files from disk |
| `networkctl reconfigure IFACE` | Re-applies config to a *running* link |
| `networkctl edit @IFACE` / `edit FILE` | Opens the matching config (or a drop-in with `--drop-in=`) in `$EDITOR` |
| `networkctl up`/`down IFACE` | Bring a device up/down |
| `networkctl renew`/`forcerenew IFACE` | Renew (or force clients to renew) DHCP lease |

**How changes get applied — precisely, per the man page:** `networkctl reload` re-reads
`.netdev`/`.network` files: a new/modified `.netdev` creates/updates that netdev (though
properties fixed at creation, e.g. VLAN `Id=`, won't change on an already-existing
interface — remove it manually first); a new, modified, or removed `.network` file
causes **all interfaces that match it to be reconfigured automatically** as part of the
reload. `networkctl reconfigure IFACE` re-applies configuration to one already-running
link but explicitly does **not** reload files from disk — "if you edit config files, it
is necessary to call `networkctl reload` first." Neither `reload` nor `reconfigure`
requires restarting `systemd-networkd.service`, and the service itself is designed not
to drop existing interfaces/addresses across a restart either — per
`systemd-networkd.service(8)`: "When systemd-networkd exits, it generally leaves
existing network devices and configuration intact... makes it possible to... restart
the service without breaking connectivity." Note `.link` file changes are a separate
case: reloading udev rules does not retroactively re-run `net_setup_link` on an
already-existing device; a fresh uevent for that interface must be triggered.

**ArchWiki discrepancy:** ArchWiki instructs "After making changes to a configuration
file, restart `systemd-networkd.service`." This is safe but coarser than necessary — the
man pages document `networkctl reload` (plus `reconfigure` for a specific link) as the
supported, non-disruptive way to pick up `.network`/`.netdev` edits without a full
service restart. Prefer `networkctl reload` per upstream docs; a full restart isn't
required and, per the service's own connectivity-preserving design, isn't inherently
better either.

## 6. Interaction with NetworkManager

Only one manager should own a given interface at a time. `Unmanaged=yes` in a `.network`
file tells `systemd-networkd` to explicitly ignore a link (any interface not matched by
any `.network` file is also left unmanaged/untouched by networkd). ArchWiki: "each
network interface should be managed by only one DHCP client or network manager"; find
conflicting services with `systemctl --type=service` and stop/mask the loser. To check
ownership in practice: `networkctl list`/`status` reports `unmanaged` for links
`systemd-networkd` isn't handling; conversely `nmcli device status` (or `nmcli device
show <iface>`) reports `unmanaged` on NetworkManager's side for links it doesn't control
(e.g. via `unmanaged-devices=` in `NetworkManager.conf` or a matching interface name).
The man pages consulted for this reference don't themselves document NetworkManager
coexistence in depth — this section rests on ArchWiki guidance plus the documented
`Unmanaged=` mechanism.
