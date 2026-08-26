# systemd-resolved

Reference for `systemd-resolved`, the local caching/validating DNS stub resolver,
LLMNR/mDNS resolver-responder, and `/etc/resolv.conf` manager. Sources:
`systemd-resolved.service(8)`, `resolved.conf(5)`, `resolvectl(1)` (systemd upstream),
cross-checked against the ArchWiki "Systemd-resolved" page — man pages win on conflicts
(noted inline).

## Contents

1. Core architecture
2. `resolved.conf` key directives
3. Per-link DNS config vs. global settings (split-horizon DNS)
4. `resolvectl` — diagnosing DNS
5. Common failure modes

## 1. Core architecture

`systemd-resolved` exposes name resolution three ways: a D-Bus API
(`org.freedesktop.resolve1`, richest, async, DNSSEC-status-aware), a Varlink socket at
`/run/systemd/resolve/io.systemd.Resolve`, and glibc NSS via `nss-resolve` (backs
`getaddrinfo(3)`/`gethostbyname(3)`, synchronous, no DNSSEC status exposed). It also
runs a **DNS stub listener**: full-featured on `127.0.0.53:53` (LLMNR/mDNS included,
DNSSEC-validating), and a limited pass-through proxy on `127.0.0.54:53` (no local
processing, no DNSSEC, no LLMNR/mDNS — just forwards to upstream, translating to
DNS-over-TLS if needed).

**`/etc/resolv.conf` has four supported modes**, auto-detected by what the file
currently is:

| Mode | Mechanism | When used |
|---|---|---|
| **stub** (recommended) | symlink → `/run/systemd/resolve/stub-resolv.conf` | Lists only `127.0.0.53` as nameserver plus live search domains; all resolution flows through resolved, including per-link routing. Used by systemd-networkd/NetworkManager/iwd setups since it always reflects current config. |
| **static** | symlink → `/usr/lib/systemd/resolv.conf` | Also points at `127.0.0.53` but with **no search domains** — for images/containers where the file must exist read-only pre-boot. |
| **uplink** | symlink → `/run/systemd/resolve/resolv.conf` | Lists the actual upstream DNS servers directly (no stub, no per-interface DNS concept) — for tools that bypass local resolution entirely. |
| **foreign/static file** | a regular file, not a resolved-owned symlink | resolved treats it as *input* (reads DNS servers/search domains from it) rather than managing it — used when another package (e.g. classic `resolvconf`, manual admin) owns the file. |

If `/etc/resolv.conf` is **not** managed by resolved (foreign mode, or missing symlink
entirely with no `nameserver 127.0.0.53` line), resolved falls back to reading it purely
as a source of upstream DNS servers/search domains for its own `DNS=`/`Domains=`
settings (only if those aren't set some other way) — but local clients that read
`/etc/resolv.conf` directly, bypassing NSS/D-Bus, will talk straight to those upstream
servers instead of through resolved, losing LLMNR/mDNS/split-DNS/DNSSEC-status behavior.

**ArchWiki mode-naming note:** ArchWiki labels the four modes "stub, static, uplink,
foreign," matching this structure — no substantive conflict with the man pages, which
describe the same four mechanisms without always using the "uplink"/"foreign" labels
verbatim.

## 2. resolved.conf key directives

Located at `/etc/systemd/resolved.conf` (or drop-ins in
`/etc/systemd/resolved.conf.d/*.conf`, standard systemd precedence: `/etc` > `/run` >
`/usr/local/lib` > `/usr/lib`, drop-ins override the main file).

```ini
# /etc/systemd/resolved.conf.d/example.conf
[Resolve]
DNS=9.9.9.9#dns.quad9.net 149.112.112.112#dns.quad9.net
FallbackDNS=1.1.1.1 8.8.8.8
Domains=~.
DNSSEC=allow-downgrade
DNSOverTLS=opportunistic
MulticastDNS=yes
LLMNR=yes
Cache=yes
```

| Directive | Default | Semantics |
|---|---|---|
| `DNS=` | empty (falls back to `/etc/resolv.conf` contents if present) | Space-separated servers; each may carry `:port`, `%interface`, `#SNI-hostname` |
| `FallbackDNS=` | compiled-in list (varies by distro build) | Only used when *no* other DNS info (per-link, `DNS=`, `/etc/resolv.conf`) is known |
| `Domains=` | empty | Space-separated domains; **without** `~` prefix = search-suffix domains for single-label name qualification; **with** `~` prefix = "route-only" domains that steer multi-label queries to this DNS config without being used as suffixes. `~.` (tilde + DNS root) means "route *all* queries preferentially here" — the standard way to make one set of DNS servers authoritative for everything |
| `DNSSEC=` | `allow-downgrade` (upstream default) | `yes` = hard-fail validation errors, requires a fully DNSSEC-capable resolver or all lookups break; `allow-downgrade` = attempt DNSSEC, silently disable it if the server doesn't support it (trades off downgrade-attack resistance for compatibility); `no` = never validate |
| `DNSOverTLS=` | `no` | `yes` requires the server to support DoT (else all lookups fail); `opportunistic` tries DoT and falls back to plaintext if unsupported (same downgrade trade-off shape as DNSSEC `allow-downgrade`) |
| `MulticastDNS=` | `no` (global default) | `yes`/`resolve` (resolve-only, no responder)/`no`; effective per-link only if **both** global and per-link settings allow it |
| `LLMNR=` | `yes` | Same yes/`resolve`/no tri-state, same global-AND-per-link gating |
| `Cache=` | `yes` | `no-negative` caches only positive answers; caching is auto-disabled for host-local (127.0.0.1/::1) DNS servers regardless (`CacheFromLocalhost=no` default) |
| `ReadEtcHosts=` | `yes` | Whether `/etc/hosts` entries are consulted/take priority before network queries |
| `DNSStubListener=` | `yes` (both udp+tcp) | `udp`/`tcp`/`no` — controls the `127.0.0.53`/`127.0.0.54` stub(s) |

**Arch-specific override worth flagging:** the Arch `systemd` package is **compiled with
`DNSSEC=false`** as its shipped default (disabled), diverging from the upstream
man-page-documented default of `allow-downgrade`. This is a packaging choice, not a doc
conflict, but matters operationally — on Arch, DNSSEC validation is off unless
explicitly configured.

## 3. Per-link DNS config vs. global settings (split-horizon DNS)

`.network` files' `[Network]` section can set link-specific `DNS=`, `Domains=`,
`DNSSEC=`, `DNSOverTLS=`, `LLMNR=`, `MulticastDNS=`, which are picked up dynamically by
`resolved` (also settable at runtime via `resolvectl dns`/`domain`/etc., for links
managed by NetworkManager or scripts instead of networkd — see
`references/networkd.md`). **Per-link settings take precedence over global ones for
queries routed to that link**; for `DNSSEC=`/`DNSOverTLS=` specifically, an *unset*
per-link value falls back to the global `resolved.conf` value — only system-wide DNS
servers (not per-link ones) use the global setting unconditionally.

Split-DNS/routing example: give an interface a route-only domain so internal-zone
queries go to its DNS server while everything else uses the default:

```ini
# /etc/systemd/network/30-vpn.network
[Match]
Name=tun0

[Network]
DNS=10.8.0.1
Domains=~corp.internal
```

To make one link authoritative for *all* unmatched queries (the common "VPN should own
all DNS" ask), set `Domains=~.` on that link instead — this is exactly the routing logic
behind `resolvectl`'s exclusive-mode/`resolvconf` compatibility behavior. Whether a link
counts as a "default route" for DNS (used when a query matches no domain at all) is
auto-derived: true unless the link carries a route-only domain other than `~.`; override
explicitly with `resolvectl default-route IFACE yes|no` or `DNSDefaultRoute=` in the
`.network` file.

## 4. resolvectl — diagnosing DNS

| Command | Purpose |
|---|---|
| `resolvectl status [LINK]` | Global + per-link config in effect: DNS servers, search/route domains, DNSSEC/LLMNR/mDNS state. First thing to run for "DNS isn't resolving right." |
| `resolvectl query NAME` (or an address, for reverse lookup) | Forward/reverse lookup; shows protocol used (DNS/LLMNR/mDNS) and whether the answer was DNSSEC-authenticated |
| `resolvectl dns [LINK [SERVER...]]` | Get/set per-link DNS servers (no args on a link = clear) |
| `resolvectl domain [LINK [DOMAIN...]]` | Get/set per-link search (`DOMAIN`) or route-only (`~DOMAIN`) domains |
| `resolvectl dnssec\|dnsovertls\|llmnr\|mdns [LINK [MODE]]` | Get/set per-link protocol settings |
| `resolvectl default-route [LINK [BOOL]]` | Get/set whether a link is used as the DNS default route |
| `resolvectl revert LINK` | Reset all per-link overrides to defaults |
| `resolvectl flush-caches` | Drop all cached RRs (sync equivalent of `SIGUSR2`) |
| `resolvectl statistics` / `reset-statistics` | Cache hit/miss + DNSSEC validation counters |
| `resolvectl monitor` | Live stream of local resolution queries as they happen |
| `resolvectl reset-server-features` | Forget learned per-server feature-support levels (sync equivalent of `SIGRTMIN+1`) — useful when a server's DNSSEC/DoT support seems stuck misdetected |

Example diagnosing a DNSSEC failure:

```
$ resolvectl query brokendnssec.net
brokendnssec.net: resolve call failed: DNSSEC validation failed: no-signature (RRSIG Missing)
```

## 5. Common failure modes

- **Search domain not applied.** Usually one of: (a) `/etc/resolv.conf` isn't actually
  symlinked to `stub-resolv.conf` (check with `resolvectl status` or `networkctl
  status` — confirm the domain list is non-empty); (b) for systemd-networkd links,
  `UseDomains=` defaults to `false` for DHCP-received search domains — must explicitly
  set `UseDomains=yes` under `[DHCPv4]`/`[DHCPv6]`, or `UseDomains=` under `[Network]`.
  Also remember: unlike classic glibc `nss-dns`, resolved never uses search domains to
  *suffix* multi-label (already-dotted) names — search domains only affect single-label
  lookups and routing decisions, by design (avoids fragile relative-vs-absolute
  ambiguity against ever-growing TLDs).
- **DNSSEC validation failures.** With `DNSSEC=yes` and an upstream resolver that
  mishandles DNSSEC (or a zone with a broken chain), *all* lookups for that zone fail
  hard. Diagnose with `resolvectl query <name>` (reports `no-signature`/
  `failed-auxiliary`/etc.) or `resolvectl statistics`. Fix: switch to
  `DNSSEC=allow-downgrade` (or `no`) if the resolver doesn't support it — Arch ships
  `false` by default for exactly this compatibility reason (see §2).
- **Stub resolver not getting the right per-link routing domain from DHCP.** Check
  `resolvectl domain <iface>` — if empty despite the DHCP server advertising a domain,
  `UseDomains=` is off (see above) or the DHCP lease simply didn't include option
  15/119; `networkctl status <iface>` and `resolvectl domain` should agree.
- **`systemd-resolved` not running or masked.** `nss-resolve` will fail lookups (or fall
  through slowly to `nss-dns` if configured with the `[!UNAVAIL=return]` NSS fallback
  syntax) and `/etc/resolv.conf` will be a stale/broken symlink if resolved never
  started to create `stub-resolv.conf`. Check `systemctl status systemd-resolved` and
  that it isn't masked; `resolvectl status` failing outright is a strong signal the
  service isn't up.
- **LLMNR/mDNS interfering with expected DNS answers** on networks that (against RFC
  6762) define `.local` in real DNS: resolved deliberately does *not* route `.local` to
  unicast DNS unless it's configured explicitly as a search/route domain — a
  network-specific `.local` zone needs an explicit `Domains=` entry to be reachable at
  all.
