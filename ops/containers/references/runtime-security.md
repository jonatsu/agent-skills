# Runtime Security — `docker run` Hardening

Runtime hardening for Docker and Compose: read-only filesystem, Linux capability drops, seccomp, AppArmor,
`no-new-privileges`, resource limits, and how to audit which syscalls your app actually uses.

See also:

- `seccomp-profile-template.json` — ready-to-use minimal syscall allowlist
- `docker-compose.md` — compose equivalents of these flags
- `kubernetes-pod-security.md` — Kubernetes equivalents

---

## 1. Full `docker run` Hardening Flags

```bash
docker run \
  --read-only \                                    # Read-only root filesystem
  --tmpfs /tmp:noexec,nosuid,size=100m \           # Writable tmpfs for /tmp only
  --tmpfs /var/run \                               # For PID files if needed
  --user 10001:10001 \                             # Non-root UID:GID
  --cap-drop ALL \                                 # Drop ALL Linux capabilities
  --cap-add NET_BIND_SERVICE \                     # Re-add only what's truly needed
  --security-opt no-new-privileges:true \          # Prevent setuid escalation
  --security-opt seccomp=./seccomp.json \          # Custom seccomp profile
  --security-opt apparmor=docker-default \         # AppArmor profile
  --pids-limit 100 \                               # Prevent fork bomb
  --memory 512m \                                  # OOM protection
  --memory-swap 512m \                             # Disable swap
  --cpus 1.0 \                                     # CPU limit
  --network none \                                 # No network (if not needed)
  --health-cmd "curl -f http://localhost:3000/health || exit 1" \
  --health-interval 30s \
  myapp:latest
```

---

## 2. Linux Capabilities — Drop All, Add Selectively

Drop ALL capabilities, then explicitly re-add only what your app requires.

| Capability          | Purpose                      | Keep?                                  |
| ------------------- | ---------------------------- | -------------------------------------- |
| `NET_BIND_SERVICE`  | Bind ports < 1024            | Only if binding a privileged port      |
| `CHOWN`             | Change file ownership        | No — set ownership at build time       |
| `SETUID` / `SETGID` | Switch user identity         | No — always drop                       |
| `SYS_ADMIN`         | Broad privileged operations  | No — most dangerous capability         |
| `NET_ADMIN`         | Configure network interfaces | No (only network tools)                |
| `SYS_PTRACE`        | Debug / trace processes      | No (only debugger containers)          |
| `DAC_OVERRIDE`      | Override file permissions    | No — run as correct user instead       |
| `NET_RAW`           | Raw sockets (ping)           | No (blocked by default seccomp anyway) |
| `MKNOD`             | Create device nodes          | No                                     |
| `SYS_TIME`          | Set system clock             | No                                     |

**Most web apps need ZERO capabilities.** `--cap-drop ALL` alone is often sufficient.

Investigate before adding a capability back. `SYS_ADMIN` in particular is almost always avoidable — it grants
powers roughly equivalent to root.

---

## 3. Read-Only Root Filesystem

Prevents attackers who compromise a process from modifying the running application, dropping persistent
backdoors, or writing to `/etc/passwd`.

```bash
docker run \
  --read-only \
  --tmpfs /tmp:noexec,nosuid,size=100m \           # Apps that use /tmp
  --tmpfs /var/run:noexec,nosuid,size=10m \        # Apps that use PID files
  --tmpfs /var/log:noexec,nosuid,size=50m \        # Apps that log to disk
  myapp:latest
```

If the app writes elsewhere (`/var/lib/<app>`, `/data`), mount a named volume for that path only:

```bash
--mount type=volume,source=myapp-data,target=/var/lib/myapp
```

`tmpfs` flags to always include:

- `noexec` — cannot execute binaries from tmpfs
- `nosuid` — setuid bits ignored
- `size=` — cap memory usage

---

## 4. `no-new-privileges`

Blocks `setuid` and `setgid` binaries inside the container from gaining elevated privileges. Blocks a whole
family of container escapes.

```bash
--security-opt no-new-privileges:true
```

MUST enable for every production container. Zero downside for the vast majority of workloads.

---

## 5. Seccomp — Syscall Filtering

The Docker default seccomp profile blocks ~44 dangerous syscalls (`kexec_load`, `mount`, `setns`, `reboot`,
etc.). For stricter allowlist-based filtering, use a custom profile.

### Workflow: build a custom seccomp profile

```bash
# Step 1: Audit syscalls the app actually makes
docker run --security-opt seccomp=unconfined --name audit-run -d myapp:latest

# Capture with strace
strace -c -f -p "$(docker inspect --format '{{.State.Pid}}' audit-run)"

# Or with sysdig (container-friendly)
sysdig -p "%syscall.type" container.name=audit-run | sort -u

# Step 2: Start from the template
cp references/seccomp-profile-template.json ./seccomp.json

# Step 3: Add missing syscalls from the audit; remove obviously unneeded ones
# Step 4: Apply
docker run --security-opt seccomp=./seccomp.json myapp:latest

# Step 5: Verify — check for EPERM errors in app logs during smoke tests
docker logs myapp 2>&1 | grep -iE 'operation not permitted|EPERM'
```

See `seccomp-profile-template.json` for a minimal starting allowlist for typical web servers.

### Kubernetes equivalent

```yaml
securityContext:
  seccompProfile:
    type: RuntimeDefault    # Use containerd/runc default (recommended baseline)
    # or:
    type: Localhost
    localhostProfile: profiles/seccomp.json
```

---

## 6. AppArmor (Linux hosts)

Complementary to seccomp — restricts file / capability access rather than syscalls.

```bash
# Load Docker's default AppArmor profile
sudo apparmor_parser -r /etc/apparmor.d/docker-default

# Apply at runtime
docker run --security-opt apparmor=docker-default myapp:latest

# Generate a custom profile (interactive)
aa-genprof myapp                                   # Run app under aa-complain first
aa-logprof                                         # Convert learned events to enforcement
```

Docker Desktop on macOS / Windows does NOT support AppArmor (Linux-only).

---

## 7. Resource Limits

Prevent one container from starving the host or other containers.

```bash
--memory 512m         # Hard OOM at 512 MB
--memory-swap 512m    # Disables swap (memory-swap == memory)
--memory-reservation 256m   # Soft limit — kernel starts reclaiming
--cpus 1.0            # 100% of one CPU
--cpu-shares 1024     # Relative weight vs other containers
--pids-limit 100      # Cap total processes/threads (fork bomb protection)
--ulimit nofile=1024:2048   # File descriptor limits
--ulimit nproc=100:200      # Process limits (per-user)
```

Compose equivalents:

```yaml
mem_limit: 512m
memswap_limit: 512m
mem_reservation: 256m
cpus: 1.0
pids_limit: 100
ulimits:
  nofile: { soft: 1024, hard: 2048 }
```

---

## 8. Network Hardening

```bash
# No network at all — for batch jobs
--network none

# Custom bridge network — no external egress
docker network create --internal backend
docker run --network backend myapp

# Restrict to specific published ports
-p 127.0.0.1:8080:8080                             # Bind only to localhost
```

Prefer overlay / bridge networks with `--internal` for backend services; only publish ports on the edge.

---

## 9. Auditing a Running Container

```bash
# What capabilities does it actually have?
docker inspect --format='{{.HostConfig.CapAdd}} / {{.HostConfig.CapDrop}}' <container>

# What security-opts?
docker inspect --format='{{json .HostConfig.SecurityOpt}}' <container>

# Is it root?
docker exec <container> id

# Is the filesystem read-only?
docker inspect --format='{{.HostConfig.ReadonlyRootfs}}' <container>

# Resource limits
docker inspect --format='{{.HostConfig.Memory}} / {{.HostConfig.NanoCpus}}' <container>

# Live syscall audit
sysdig container.name=<container>
falco -pk                                          # Alerts on runtime anomalies
```

---

## 10. Runtime Hardening Anti-Patterns

| Anti-pattern                                                | Fix                                                                                                             |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `--privileged`                                              | Almost never needed. Use targeted `--cap-add` and `--device` instead.                                           |
| `--cap-add SYS_ADMIN`                                       | Investigate — this is close to root. Usually a symptom of a poor image (mount attempt, container-in-container). |
| `-v /:/host`                                                | Full host filesystem exposed. Never.                                                                            |
| `-v /var/run/docker.sock:/var/run/docker.sock`              | Container can control the Docker daemon → root on host. Use socket proxy or rootless.                           |
| `--net=host`                                                | Bypasses network namespace isolation. Only for host-level tooling.                                              |
| `--pid=host` or `--ipc=host`                                | Breaks process / IPC isolation. Only for host-level tooling.                                                    |
| `--user root` (or missing `--user` and image has no `USER`) | Runs as root inside the container. Always set `--user <non-root>`.                                              |
| No seccomp / `seccomp=unconfined`                           | Lets every syscall through, including `kexec_load`, `mount`, etc. Use default or custom profile.                |
| No resource limits                                          | One runaway container OOM-kills the host. Always set `--memory`, `--cpus`, `--pids-limit`.                      |
| Publishing DB / cache ports to `0.0.0.0`                    | Externally reachable database. Bind to `127.0.0.1` or use an internal network.                                  |
