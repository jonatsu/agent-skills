# Network Exposure and Firewalling

Deliberately higher-level than the rest of this skill: the mechanisms are general Linux, and only the
packaging and the defaults are Yocto's. The one rule worth stating absolutely is that **the inventory comes
first** — a firewall in front of services nobody enumerated is a guess with a configuration file.

## Enumerate before configuring

```sh
ss -tulpn                      # every listening socket, with the process behind it
systemctl list-sockets         # systemd socket activation, which ss shows only once triggered
systemctl list-units --type=service --state=running
```

and from a second machine, because a target's own view is not the attacker's:

```bash
nmap -sT -p- <target>          # what is reachable, as opposed to what is bound
```

For each listener, answer three questions: does the product need it, does it need to be reachable off-device
(bind to `127.0.0.1` if not), and does it need to be reachable from anywhere or only from a management VLAN.
Most embedded attack surface is closed at this step rather than by a rule set.

Host-side, the equivalent is the manifest: a package that ships a listening daemon you did not choose is a
finding before it is ever booted. See `image-attack-surface.md` for removing it and for dropping the service's
privileges when it must stay.

## What Yocto gives you, and the trap in the defaults

| Tool                                                             | Where                                              | Note                                                 |
| ---------------------------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------- |
| `nftables` 1.0.9                                                 | `meta-openembedded/meta-networking/recipes-filter` | The modern default; needs `meta-networking`          |
| `iptables` 1.8.10                                                | OE-Core, `meta/recipes-extended`                   | **Legacy backend by default** — see below            |
| `ebtables`, `ipset`, `conntrack-tools`, `arno-iptables-firewall` | `meta-networking/recipes-filter`                   | Available if a design needs them                     |
| `sshguard`                                                       | `meta-security/recipes-security`                   | Brute-force response, if ssh is exposed at all       |
| `firewalld`                                                      | **not packaged** in `meta-networking` at scarthgap | Do not design around it without checking your layers |

**The trap:** OE-Core's `iptables` recipe has `PACKAGECONFIG ?= "${@bb.utils.filter('DISTRO_FEATURES', 'ipv6', d)}"`,
so `libnftnl` is **off by default**. Only with that option does the recipe repoint `iptables`,
`iptables-save` and `iptables-restore` at `xtables-nft-multi`. On a stock image, `iptables` therefore writes
**legacy** tables while `nft` writes the nftables tables — two independent rule sets in one kernel, where each
tool shows a complete-looking picture of only its own. A rule set that appears to be missing is usually this.

Pick one. For a new product that means nftables, and it means not installing `iptables` at all.

## A default-drop baseline

The shape, rather than a copy-paste policy, because the accepted ports are the product's:

```text
table inet filter {
  chain input {
    type filter hook input priority filter; policy drop;
    ct state established,related accept
    ct state invalid drop
    iif lo accept
    ip protocol icmp accept          # and icmpv6, which is not optional for IPv6 to work
    tcp dport { 22 } accept          # every accepted port is a decision with a name
  }
  chain forward { type filter hook forward priority filter; policy drop; }
  chain output  { type filter hook output priority filter; policy accept; }
}
```

Two embedded-specific cautions. **Locking yourself out of a board is the common failure**, so bring rules up
with a timeout that reverts them until confirmed, or through the serial console rather than the link you are
filtering. And **`policy drop` on `output` is a bigger commitment than it looks** on a device that also does
DNS, NTP and update fetches; start with `accept` and tighten deliberately.

The Yocto question is only where the policy lives and how it loads: package the ruleset with the recipe that
owns it, load it from a systemd unit ordered before the services it protects, and treat it as release content
rather than as something an operator applies.

## Service-level hardening

- **ssh.** If it ships at all, it is the primary remote surface: keys only (`PasswordAuthentication no`), no
  root login, and a considered decision about whether it is present in the production image at all — many
  products ship it in `dev` and `prod-test` only. `image-attack-surface.md` covers the `IMAGE_FEATURES` that
  silently loosen both settings, including the PAM `nullok` rewrite that an `sshd_config` audit misses.
- **TLS-terminating services** need the same treatment as any server: current protocol versions, a real
  certificate story, and a plan for rotating it on a device that may be offline. Where certificates come from,
  and how they are renewed in the field, is a product decision this skill does not make for you.
- **systemd unit exposure** — `systemd-analyze security <unit>` ranks what each service can reach. The
  directives are general Linux; the Yocto half is which recipe packages the drop-in.

## Verification

```sh
nft list ruleset                 # what is actually loaded, not what the file says
iptables-save                    # non-empty here on an nftables product means both stacks are live
ss -tulpn
systemd-analyze security
```

and, again from another machine, `nmap` against the running product. **Prove the negative case**: a port you
believe is blocked must actually refuse a connection from off-device. A rule set that has never rejected a
connection is a configuration file.

## Stated limit

This file is deliberately generic. It covers enumerating exposure, choosing between the two packaged firewall
stacks, and the default-drop shape. It does not cover VPN or overlay-network design, IDS tuning
(`meta-security` packages `suricata`, `aide`, `samhain` and others — see `meta-security-layer-map.md`), or
per-protocol server hardening beyond the above. Say so rather than generating a policy that looks
authoritative.
