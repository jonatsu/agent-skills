# Configuration Findings — Credentials, Services, Filesystem

The findings that need no tool: read the rootfs. These are also the ones most often reported from the build
configuration rather than the artefact, which is what the Iron Law forbids.

Every check below works on an unpacked rootfs with no build tree.

## Credentials

```bash
grep '^root:' rootfs/etc/shadow          # root::…  is an empty password
awk -F: '$2=="" {print $1}' rootfs/etc/shadow          # every passwordless account
awk -F: '$3==0 {print $1}' rootfs/etc/passwd           # every uid-0 account, not just root
awk -F: '$7 !~ /(nologin|false)$/ {print $1, $7}' rootfs/etc/passwd   # accounts with a real shell
```

| Finding                               | Why it matters                                                             |
| ------------------------------------- | -------------------------------------------------------------------------- |
| `root::`                              | empty root password; `empty-root-password` was set, or zapping did not run |
| a second uid-0 account                | a root equivalent that audits and monitoring usually miss                  |
| a shared password hash across devices | one compromised device compromises the fleet                               |
| a hash present at all                 | it is offline-crackable; the question is whether it should be there        |

**The fleet-wide point is the one people miss.** `extrausers` sets the same credentials on every device built
from that image, so a recovered hash is a fleet key, not a device key. You cannot see this from one artefact —
it is a question to ask, not a check to run.

## SSH exposure

```bash
grep -iE '^\s*(PermitRootLogin|PermitEmptyPasswords|PasswordAuthentication)' rootfs/etc/ssh/sshd_config
```

Read the file, not the package list: `openssh` being installed says nothing about its configuration, and
Dropbear has entirely different defaults and flags.

## Worked example, on upstream's own security image

`meta-security`'s `security-test-image` at `scarthgap`, measured 2026-09-08:

```text
root::15069:0:99999:7:::
PermitRootLogin yes
PermitEmptyPasswords yes
```

with `IMAGE_FEATURES = "debug-tweaks ssh-server-openssh"` and `ROOTFS_POSTPROCESS_COMMAND` containing
`ssh_allow_empty_password` and `ssh_allow_root_login`.

Three real findings in an image whose name contains "security" — **and the correct severity is nil**, because
it is a test image that exists so a harness can ssh in. The same three findings in a shipped image are
critical.

That is the whole discipline in one example: **the artefact produces the finding, the intent produces the
severity, and you usually have to ask for the intent.**

## What starts, and what listens

```bash
ls rootfs/etc/systemd/system/*.wants/ rootfs/lib/systemd/system/*.wants/ 2>/dev/null
ls rootfs/etc/rc*.d/ 2>/dev/null                       # sysvinit
grep -rlE '^\s*User\s*=\s*root' rootfs/lib/systemd/system/    # units that stay root
grep -rhE '^\s*(ExecStart|User|Capabilit|NoNewPrivileges|ProtectSystem)' rootfs/lib/systemd/system/*.service
```

Host-side you can see what is **configured** to start. Only on target can you see what **is** listening:

```bash
ss -tulpn          # or netstat -tulpn on a busybox image
```

⛔ **A host-side service audit cannot answer "what is exposed".** A unit can be present and masked, socket
activated, or started by something else entirely. Report which lane the result came from.

Upstream's own negative result is worth carrying: OE-Core's `lighttpd` runs as root. Public-facing services in
OE-Core are not privilege-dropped by default, so "it is an upstream recipe" is not evidence that it drops
privilege.

## Filesystem state

```bash
grep -v '^#' rootfs/etc/fstab                          # what read-only-rootfs actually wrote
find rootfs -perm -4000 -o -perm -2000 2>/dev/null     # setuid and setgid binaries
find rootfs -perm -0002 -type f 2>/dev/null            # world-writable files
getcap -r rootfs 2>/dev/null                           # file capabilities
```

The setuid inventory is the highest-value one: it is short, it is stable across releases, and any addition to
it is a change worth explaining.

Two traps:

- **`read-only-rootfs` edits `/etc/fstab` lines matching `/dev/root`.** The kernel command line still decides
  whether the root filesystem is actually mounted read-only. `/etc/fstab` is a claim; `findmnt` on target is
  the observation.
- **Extracting a rootfs as a non-root user loses ownership and may lose capabilities.** `find -perm` still
  works because modes survive, but `getcap` results from an unprivileged extraction are unreliable. Say so, or
  read the image with a tool that preserves xattrs.

## MAC policy

```bash
ls rootfs/etc/apparmor.d/ rootfs/etc/selinux/ rootfs/etc/smack/ 2>/dev/null
```

Presence of a policy directory means a framework was installed. It does **not** mean the framework is enforcing
— that needs the kernel command line and, on target, `aa-status`, `getenforce` or the SMACK filesystem.

The measured collision from the oeqa run is the cautionary case: an image can enable two LSMs in
`DISTRO_FEATURES` while the kernel command line selects one, so a policy directory exists for a framework that
is not active. See `oeqa-security-suites.md`.

## Reporting these

Configuration findings are the easiest to over-report, because a rootfs will always yield a list. Before
reporting:

- [ ] **Confirm on the artefact, never from `IMAGE_FEATURES`.** `debug-tweaks` predicts an empty root password;
  `grep '^root:'` establishes it.
- [ ] **Ask what the image is for** before assigning severity.
- [ ] **Name the lane** — an unpacked rootfs and a running device answer different questions.
- [ ] **Route CVE questions elsewhere.** "This package is old" is `yocto-vulnerability-management`'s job.
