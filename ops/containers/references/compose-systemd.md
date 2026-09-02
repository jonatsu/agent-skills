# Managing Docker Compose Stacks with systemd

## Purpose

Defines operating model for managing multi-service Docker Compose stack as single systemd unit when splitting
services into separate systemd units is not possible.

Recommended architecture:

- **systemd** manages host boot ordering, config validation, deployment, admin start/stop/reload, bounded
  startup retries.
- **Docker** supervises individual containers through restart policies.
- **Docker Compose** defines service relationships, health checks, startup dependencies, resource constraints,
  graceful shutdown.
- **External monitoring** detects services that remain running but become unhealthy or degraded.

Do not make systemd continuously supervise attached `docker compose up` process. Docker supervises container
lifecycle after deployment.

## Minimum Requirements

Requires Docker Compose v2.20+ for:

- `depends_on` long-form with `restart: true`
- `--wait` / `--wait-timeout` flags
- `deploy.resources` honored in non-Swarm mode

Verify:

```bash
docker compose version
```

## Recommended systemd Architecture

Treat entire Compose project as one deployment unit.

Use:

```ini
Type=oneshot
RemainAfterExit=yes
```

Run Compose in detached mode:

```bash
docker compose up --detach
```

systemd unit becomes active after Compose successfully deploys stack. Docker then manages containers.

## Example systemd Unit

```ini
# /etc/systemd/system/example-stack.service

[Unit]
Description=Example Docker Compose stack
Documentation=file:/opt/example-stack/README.md

Wants=network-online.target
After=network-online.target docker.service
Requires=docker.service

# Ensure filesystems containing bind mounts and Compose files are mounted.
RequiresMountsFor=/opt/example-stack
RequiresMountsFor=/srv/example-data

# Bound repeated startup failures.
StartLimitIntervalSec=300
StartLimitBurst=3

[Service]
Type=oneshot
RemainAfterExit=yes

WorkingDirectory=/opt/example-stack

# Validate fully rendered Compose configuration before deployment.
ExecStartPre=/usr/bin/docker compose \
    --project-name example \
    --project-directory /opt/example-stack \
    --file /opt/example-stack/compose.yaml \
    config --quiet

# Pull images before startup to avoid pull-timeout races during deploy.
# Skip this step for air-gapped or pinned-digest deployments using
# pull_policy: never — see Pull Policy section.
ExecStartPre=-/usr/bin/docker compose \
    --project-name example \
    --project-directory /opt/example-stack \
    --file /opt/example-stack/compose.yaml \
    pull

# Deploy stack and wait for service readiness.
ExecStart=/usr/bin/docker compose \
    --project-name example \
    --project-directory /opt/example-stack \
    --file /opt/example-stack/compose.yaml \
    up --detach --wait --wait-timeout 180 --remove-orphans

# Reconcile running deployment with current configuration.
ExecReload=/usr/bin/docker compose \
    --project-name example \
    --project-directory /opt/example-stack \
    --file /opt/example-stack/compose.yaml \
    up --detach --wait --wait-timeout 180 --remove-orphans

# Gracefully stop containers without dismantling deployment.
# No --timeout: let per-service stop_grace_period govern each container.
ExecStop=/usr/bin/docker compose \
    --project-name example \
    --project-directory /opt/example-stack \
    --file /opt/example-stack/compose.yaml \
    stop

TimeoutStartSec=300
TimeoutStopSec=90

# Retry only when initial deployment fails.
# Note: after successful start, unit is active (exited). Restart= is inert
# for oneshot units post-success — Docker restart policies handle runtime
# container failures, not systemd.
Restart=on-failure
RestartSec=15s

# Prevent interactive Compose behavior.
Environment=COMPOSE_ANSI=never

StandardOutput=journal
StandardError=journal
SyslogIdentifier=example-stack

[Install]
WantedBy=multi-user.target
```

Enable unit:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now example-stack.service
```

## Why Use `Type=oneshot`

`docker compose up --detach` exits after creating and starting containers.

Without `RemainAfterExit=yes`, systemd considers service inactive immediately after command exits.

With:

```ini
Type=oneshot
RemainAfterExit=yes
```

systemd records deployment as active even though no long-running Compose CLI process remains.

Use:

```bash
docker compose up --detach --wait
```

to make startup succeed only after services are running or healthy.

Use:

```bash
--wait-timeout 180
```

to prevent indefinite startup waits.

## Use `stop`, Not `down`, for Normal Shutdown

Use for ordinary systemd shutdown:

```ini
ExecStop=/usr/bin/docker compose ... stop
```

`docker compose stop`:

- Stops containers.
- Preserves containers.
- Preserves networks.
- Preserves volumes.
- Preserves deployment metadata.
- Allows next `compose up` to start or reconcile existing deployment.

Do not pass `--timeout` to `compose stop` — it overrides every service's `stop_grace_period`, cutting graceful
shutdown short. Let per-service `stop_grace_period` settings govern each container individually.

Avoid in normal unit lifecycle:

```ini
ExecStop=/usr/bin/docker compose ... down
```

`docker compose down` removes containers and project networks. Reserve for deliberate teardown.

Never use in ordinary service unit:

```bash
docker compose down --volumes
```

That can destroy persistent data.

Use deliberate teardown separately:

```bash
sudo systemctl stop example-stack.service

docker compose \
  --project-name example \
  --project-directory /opt/example-stack \
  --file /opt/example-stack/compose.yaml \
  down --remove-orphans
```

## Docker Restart Policies

Every long-running service MUST have explicit `restart:` policy. Prefer `unless-stopped` for persistent
services, `on-failure` for retryable jobs, `"no"` for one-shot containers. Never rely on systemd `Restart=`
for runtime container failures — after oneshot unit completes, systemd no longer observes individual container
processes.

## Health Checks

Health check should test whether service can perform actual role.

Do not merely check whether process exists.

### Database Example

```yaml
services:
  database:
    image: postgres:18
    restart: unless-stopped

    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U "$${POSTGRES_USER}" -d "$${POSTGRES_DB}"
      interval: 10s
      timeout: 5s
      retries: 6
      start_period: 30s
```

### HTTP Service Example

```yaml
services:
  application:
    healthcheck:
      test:
        - CMD
        - wget
        - --quiet
        - --tries=1
        - --spider
        - http://127.0.0.1:8080/health/ready
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s
```

Ensure container image contains command used by health check.

Health check MUST test actual service role, not merely process existence. Set `start_period` >= 60s for slow
cold starts (model loading, large cache warmup). Ensure container image contains the health-check command.

For services with slow cold starts (model loading, large cache warmup), set generous `start_period` — 60s or
more.

## Dependency Readiness

Plain `depends_on` controls startup order, but not readiness.

Use dependency conditions:

```yaml
services:
  application:
    depends_on:
      database:
        condition: service_healthy
        restart: true
        required: true

      migration:
        condition: service_completed_successfully

      optional-cache:
        condition: service_started
        required: false
```

Use:

```yaml
condition: service_healthy
```

when dependent service must be healthy before startup proceeds.

Use:

```yaml
condition: service_completed_successfully
```

for migrations, schema initialization, data generation, other one-shot setup tasks.

Use:

```yaml
required: false
```

(Compose v2.20+) when dependency is optional — only warns if unavailable instead of failing. Default: `true`.

### One-Shot Initialization Containers

For tasks like model pulling, schema setup, or data seeding, use a dedicated one-shot container that exits
successfully when done.

Example — pulling a model before serving:

```yaml
services:
  model-pull:
    image: ollama/ollama:latest
    command: ["ollama", "pull", "mxbai-embed-large"]
    volumes:
      - model-storage:/root/.ollama
    restart: "no"

  model-serve:
    image: ollama/ollama:latest
    depends_on:
      model-pull:
        condition: service_completed_successfully
    volumes:
      - model-storage:/root/.ollama
    restart: unless-stopped
```

This separates init from serve. `--wait` blocks until `model-pull` completes successfully before starting
`model-serve`. For multi-GB pulls, raise `--wait-timeout` or pull out-of-band before enabling unit.

Compose dependency conditions control initial startup only. They do not guarantee runtime resilience.

Applications must tolerate dependencies disappearing after startup.

Implement:

- Connection retries.
- Exponential or bounded backoff.
- Database reconnection.
- Idempotent initialization.
- Graceful handling of unavailable caches.
- Graceful handling of unavailable message brokers.
- Recovery after dependency restart.

## Graceful Shutdown

Define appropriate shutdown behavior for each service.

```yaml
services:
  application:
    init: true
    stop_signal: SIGTERM
    stop_grace_period: 30s
```

Use `init: true` to run a lightweight init process (tini) as PID 1. Recommended for images with shell wrappers
or PID1 reaping issues — without it, SIGTERM may not reach the real workload, making `stop_grace_period`
ineffective. Verify the workload handles SIGTERM correctly regardless; well-built images with exec-form
entrypoints may not need it.

Applications should:

1. Stop accepting new work.
2. Finish or safely abandon in-flight work.
3. Flush state.
4. Close network and database connections.
5. Exit before grace period expires.

systemd setting:

```ini
TimeoutStopSec=
```

must cover the entire stack shutdown worst case — not just the longest single `stop_grace_period`.
`compose stop` may stop containers sequentially (respecting dependency order), so total shutdown time can be
the sum of sequential grace periods plus Docker overhead. Calculate: sum of sequential `stop_grace_period`
values + Docker per-container overhead (~5-10s each).

Example:

```ini
TimeoutStopSec=90
```

with container grace period of:

```yaml
stop_grace_period: 30s
```

provides enough headroom for a single-service stack. For multi-service stacks with sequential shutdown, raise
`TimeoutStopSec` to cover the cumulative worst case. If systemd kills `compose stop` mid-shutdown, containers
receive SIGKILL — defeating the purpose of graceful shutdown.

## Resource Constraints

Containers have no meaningful resource constraints by default.

Runaway service can exhaust host memory, CPU, PIDs, or disk space and destabilize entire stack.

Use `deploy.resources` (modern Compose spec, honored in non-Swarm mode):

```yaml
services:
  application:
    deploy:
      resources:
        limits:
          memory: 1g
          cpus: "2.0"
          pids: 512
        reservations:
          memory: 512m
```

Apply limits based on measured behavior.

Important considerations:

- Reserve memory for Docker.
- Reserve memory for systemd.
- Reserve memory for SSH and administration.
- Reserve memory for filesystem caches.
- Reserve memory for monitoring.
- Use `pids_limit` to contain process explosions.
- Avoid overly tight CPU limits for latency-sensitive services.
- Do not disable OOM killer to hide memory sizing problems.

## GPU and Device Passthrough

Some services require access to host devices (GPUs, accelerators, serial ports, USB devices). These
requirements conflict with full hardening — device access needs relaxed `cap_drop`, `read_only`, and
`security_opt`.

### NVIDIA GPUs

```yaml
services:
  gpu-service:
    image: ollama/ollama:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]  # required field
    # Cannot use read_only: true — GPU runtime writes to /dev/shm, /tmp
    # Cannot use cap_drop: [ALL] — needs device access capabilities
    restart: unless-stopped
```

`capabilities` is required. Values: `gpu` (graphics accelerator), `tpu` (AI accelerator), or driver-specific
(e.g., `nvidia-compute`). `count` and `device_ids` are mutually exclusive.

### AMD GPUs

```yaml
services:
  gpu-service:
    image: my-amd-app:latest
    devices:
      - /dev/kfd
      - /dev/dri
    # May also need: cap_add: [SYS_PTRACE] for ROCm profiling
    restart: unless-stopped
```

### Intel GPUs / Other Devices

```yaml
services:
  gpu-service:
    image: my-intel-app:latest
    devices:
      - /dev/dri:/dev/dri
    # For Intel oneAPI, may need group_add for render access
    group_add:
      - "44"  # render group GID on host
    restart: unless-stopped
```

### Hardening Tradeoffs

When a service needs device access:

- `read_only: true` usually incompatible — runtimes write to `/dev/shm`, `/tmp`, model caches.
- `cap_drop: [ALL]` usually incompatible — device access needs specific capabilities.
- `no-new-privileges: true` still safe to keep.
- `user:` may need to match host device owner for permission.
- `tmpfs` for `/tmp` and `/dev/shm` still works.

Document why each hardening relaxation is necessary per service.

### Reboot Race with Device-Dependent Containers

With `restart: unless-stopped`, Docker daemon may restart containers before systemd unit runs `compose up -d`
on host reboot. For GPU containers, device may not be ready when Docker's policy fires → restart loop before
systemd intervenes.

Mitigations:

- Use `restart: on-failure` with bounded retry for device-dependent services.
- Order service after GPU driver readiness if possible.
- Accept brief restart loop — systemd reconcile will stabilize once device is ready.
- Pre-pull models out-of-band so cold start is faster once device is available.

## Logging and Disk Protection

Unbounded container logs can fill host filesystem.

Two separate log streams are governed by different settings:

- **Container stdout/stderr** → Docker logging driver (`local`, `journald`, `json-file`).
- **Compose CLI process output** → systemd `StandardOutput=journal`.

These are independent. `StandardOutput=journal` in the systemd unit captures the Compose CLI process output
(config validation, pull progress, startup messages). The Docker logging driver governs what each container
writes to stdout/stderr.

### Docker Daemon Configuration

Prefer `local` driver with rotation, or configure explicitly. Avoid `json-file` without rotation — it has no
rotation by default and will exhaust disk. `local` driver includes rotation by default.

```json
{
  "log-driver": "local",
  "log-opts": {
    "max-size": "20m",
    "max-file": "5"
  }
}
```

Enable `live-restore` to keep containers running across Docker daemon restarts — directly supports "Docker
supervises lifecycle" model:

```json
{
  "live-restore": true
}
```

### Per-Service Configuration

```yaml
services:
  application:
    logging:
      driver: local
      options:
        max-size: 20m
        max-file: "5"
```

After modifying:

```text
/etc/docker/daemon.json
```

validate configuration and restart Docker carefully.

Also monitor:

- Docker data-root usage.
- Volume growth.
- Bind-mounted data directories.
- Application-generated logs.
- Database storage.
- Temporary files.
- Image accumulation.
- Build cache accumulation.

Schedule periodic cleanup:

```bash
docker system prune -f --filter "until=168h"
docker builder prune -f
```

## Deployment Validation

Always validate effective Compose configuration before deployment.

```bash
docker compose \
  --project-name example \
  --project-directory /opt/example-stack \
  --file /opt/example-stack/compose.yaml \
  config --quiet
```

Basic deployment workflow:

```bash
set -euo pipefail

cd /opt/example-stack

docker compose config --quiet
docker compose pull
docker compose up -d --wait --wait-timeout 180 --remove-orphans
docker compose ps
```

Validation should detect:

- Invalid YAML.
- Invalid Compose syntax.
- Missing environment variables.
- Broken file references.
- Invalid merged configuration.
- Unsupported fields.
- Missing bind-mount paths.
- Missing secrets or configuration files.
- Service readiness failures.

## Pin Images and Artifacts

Avoid mutable production image references.

Do not use:

```yaml
image: application:latest
```

Prefer immutable release tags:

```yaml
image: registry.example.com/application:2.8.4
```

For strongest reproducibility, pin image digest:

```yaml
image: registry.example.com/application@sha256:012345...
```

Production deployment should consume already-built and tested images.

Do not implicitly build production images during system startup unless strong operational reason.

Preferred flow:

1. Build.
2. Test.
3. Scan.
4. Publish.
5. Pin.
6. Deploy.
7. Validate readiness.

### Pull Policy

Control when Compose pulls images during `up`:

```yaml
services:
  application:
    image: registry.example.com/application@sha256:012345...
    pull_policy: missing  # default — pull only if not present locally
```

Options:

- `missing` — pull only if image absent locally (default). `if_not_present` is alias.
- `always` — pull on every `up`, even if present.
- `never` — never pull; fail if image absent.
- `build` — always build from source.
- `daily` — check for updates if last pull > 24h ago.
- `weekly` — check for updates if last pull > 7d ago.
- `every_<duration>` — check if last pull > duration ago (e.g., `every_12h`, `every_30m`).

Gotcha: `latest` tag is always pulled even with `missing` policy.

For air-gapped or pinned-digest deployments, use `pull_policy: never` with `--pull never`:

```bash
docker compose up -d --wait --no-build --pull never
```

`--no-build` prevents implicit builds. `--pull never` prevents registry hits on every boot.

## Stable Project Identity

Always define stable Compose project name.

In Compose:

```yaml
name: example
```

or on every command:

```bash
docker compose --project-name example ...
```

Also pin:

- `--project-directory`
- Every `--file` path
- `WorkingDirectory=`
- Environment-file paths
- Bind-mount paths
- Secret paths
- Configuration paths

Do not depend on:

- Current shell directory.
- Invoking user's environment.
- Implicit `.env` discovery from unstable working directory.
- Directory-name-derived project names.

Unstable project identity can create duplicate:

- Containers.
- Networks.
- Volumes.
- Resource names.
- Orphaned deployments.

## Suggested Directory Layout

```text
/opt/example-stack/
├── compose.yaml
├── compose.production.yaml
├── .env
├── config/
├── scripts/
└── README.md
```

Recommended ownership model:

- Compose definitions: root-owned, not writable by service users.
- Secrets: restrictive permissions.
- Persistent data: owned by required container UID/GID.
- Scripts: root-owned, executable only where required.
- Configuration: version-controlled where practical.
- Runtime-generated data: outside source/configuration tree.

### Compose Secrets

Use Compose `secrets:` mechanism to pass sensitive data without baking into images:

```yaml
services:
  application:
    secrets:
      - db-password

secrets:
  db-password:
    file: /opt/example-stack/secrets/db-password.txt
```

Secret is mounted at `/run/secrets/db-password` inside container. File permissions on host control access.
Secret content never appears in image layers or `docker history`.

### Secret Sources

- `file` — content read from file path on host.
- `environment` — value read from host environment variable (Compose only; not supported with
  `docker stack deploy`).

```yaml
secrets:
  oauth-token:
    environment: "OAUTH_TOKEN"
```

### Long Syntax

Control mount path, ownership, and permissions inside container:

```yaml
services:
  application:
    secrets:
      - source: db-password
        target: /run/secrets/db_password
        uid: "1000"
        gid: "1000"
        mode: 0440
```

Must declare secret in top-level `secrets:` AND explicitly grant to each service.

## Post-Startup Health Monitoring

Oneshot systemd unit cannot represent ongoing Compose stack health.

After:

```bash
docker compose up -d --wait
```

succeeds, systemd only knows initial deployment succeeded.

It does not know whether container later becomes:

- Exited.
- Restarting.
- Unhealthy.
- Deadlocked.
- Non-responsive.
- Unable to reach dependency.
- Functionally degraded.

Docker health status alone does not automatically restart container. Restart policies react to process exit,
not merely to `unhealthy` state.

Use this recovery hierarchy:

1. Application self-recovers.
2. Application exits non-zero when unrecoverable.
3. Docker restart policy restarts container.
4. Monitoring detects persistent failure.
5. Administrator or carefully designed remediation process intervenes.

Avoid blindly restarting entire stack whenever one container becomes unhealthy. That can turn localized
failure into full-stack outage.

## Example Health Check Script

```bash
#!/usr/bin/env bash
set -euo pipefail

project=example

unhealthy="$(
    docker compose \
        --project-name "$project" \
        --project-directory /opt/example-stack \
        --file /opt/example-stack/compose.yaml \
        ps --format json |
    jq -r '
        .[]? // . |
        select(
            (.State != "running") or
            (.Health != null and .Health != "" and .Health != "healthy")
        ) |
        .Service + ": state=" + .State + " health=" + (.Health // "none")
    '
)"

if [[ -n "$unhealthy" ]]; then
    printf '%s\n' "$unhealthy" >&2
    exit 1
fi
```

Requires `jq` installed on host. `ps --format json` outputs NDJSON (one JSON object per line, not a JSON
array). jq reads NDJSON as a stream of objects by default, so `select(...)` works directly. The `.[]? // .`
filter also handles the array case for older Compose versions that may emit a JSON array. Fields: `ID`,
`Name`, `Command`, `Project`, `Service`, `State`, `Health`, `ExitCode`, `Publishers`.

Use script from:

- systemd timer.
- Monitoring agent.
- Local watchdog.
- Metrics exporter.
- Alerting pipeline.

Prefer alerting over unconditional whole-stack restart.

## Security Model

Membership in `docker` group is effectively root-equivalent.

User with Docker daemon access can typically:

- Start privileged containers.
- Mount host filesystem.
- Access host devices.
- Read sensitive bind-mounted files.
- Modify host state.
- Escape intended service boundaries.

Do not assume running systemd service as non-root member of `docker` group provides strong isolation.

For rootful Docker, running system service as root is often clearer and more honest than using nominally
unprivileged account with Docker socket access.

For stronger isolation, consider rootless Docker mode or user namespace remapping.

## Container Hardening

Apply service-specific hardening where compatible.

```yaml
services:
  application:
    read_only: true

    tmpfs:
      - /tmp:size=64m,mode=1777

    cap_drop:
      - ALL

    security_opt:
      - no-new-privileges:true

    user: "10001:10001"

    pids_limit: 256
```

Add capabilities back only when demonstrably required.

Additional hardening considerations:

- Use non-root container users.
- Use read-only root filesystems.
- Provide only required writable paths.
- Use `tmpfs` for ephemeral writable directories.
- Drop all capabilities by default.
- Add only required capabilities.
- Disable privilege escalation.
- Avoid privileged mode.
- Avoid mounting Docker socket.
- Avoid mounting broad host paths.
- Avoid host networking unless required.
- Avoid host PID and IPC namespaces.
- Use restrictive file permissions.
- Separate secrets from images.
- Pin images by digest.
- Scan images and dependencies.
- Use seccomp and AppArmor or SELinux where available.

See GPU and Device Passthrough section for hardening tradeoffs when device access is required.

## Boot Ordering and Mount Dependencies

Use:

```ini
Wants=network-online.target
After=network-online.target docker.service
Requires=docker.service
```

Use:

```ini
RequiresMountsFor=/opt/example-stack
RequiresMountsFor=/srv/example-data
```

for filesystems containing:

- Compose files.
- Bind mounts.
- Persistent data.
- Secrets.
- Certificates.
- Configuration files.

Do not assume `network-online.target` guarantees every external dependency is reachable. Applications must
still implement retries.

For device-dependent services (GPUs, accelerators), `network-online.target` does not guarantee device driver
readiness. See Reboot Race section under GPU and Device Passthrough.

## Bounded Startup Retries

Use bounded systemd retries only for initial deployment failure.

Example:

```ini
StartLimitIntervalSec=300
StartLimitBurst=3
```

and:

```ini
Restart=on-failure
RestartSec=15s
```

This permits retrying failures such as:

- Docker not fully ready.
- Temporary registry failure.
- Transient network failure.
- Delayed mount availability.
- Temporary dependency startup failure.

Avoid infinite restart loops.

Repeated failures should become visible and require diagnosis.

## Reload Semantics

Useful reload operation:

```ini
ExecReload=/usr/bin/docker compose \
    --project-name example \
    --project-directory /opt/example-stack \
    --file /opt/example-stack/compose.yaml \
    up --detach --wait --wait-timeout 180 --remove-orphans
```

This reconciles running deployment with current Compose configuration. Note: this is a **redeploy**, not an
in-process reload. It may recreate changed containers, remove orphans, and cause brief outages. Do not use
`systemctl reload` expecting zero-downtime config refresh — it runs `compose up` which recreates containers
whose definitions changed.

Use:

```bash
sudo systemctl reload example-stack.service
```

after changing:

- Compose configuration.
- Image references.
- Environment files.
- Mounted configuration.
- Service definitions.

Not every application reloads mounted configuration automatically. Compose may need to recreate affected
container.

## Administrative Commands

### Start

```bash
sudo systemctl start example-stack.service
```

### Stop

```bash
sudo systemctl stop example-stack.service
```

### Enable at Boot

```bash
sudo systemctl enable example-stack.service
```

### Disable at Boot

```bash
sudo systemctl disable example-stack.service
```

### Reconcile Configuration

```bash
sudo systemctl reload example-stack.service
```

### Restart the Deployment

```bash
sudo systemctl restart example-stack.service
```

### Inspect systemd Logs

```bash
journalctl -u example-stack.service
```

### Follow systemd Logs

```bash
journalctl -fu example-stack.service
```

### Inspect Container State

```bash
docker compose \
  --project-name example \
  --project-directory /opt/example-stack \
  --file /opt/example-stack/compose.yaml \
  ps
```

### Follow Container Logs

```bash
docker compose \
  --project-name example \
  --project-directory /opt/example-stack \
  --file /opt/example-stack/compose.yaml \
  logs --follow --tail=200
```

### Validate Configuration

```bash
docker compose \
  --project-name example \
  --project-directory /opt/example-stack \
  --file /opt/example-stack/compose.yaml \
  config --quiet
```

### Pull Updated Images

```bash
docker compose \
  --project-name example \
  --project-directory /opt/example-stack \
  --file /opt/example-stack/compose.yaml \
  pull
```

### Deliberate Teardown

```bash
sudo systemctl stop example-stack.service

docker compose \
  --project-name example \
  --project-directory /opt/example-stack \
  --file /opt/example-stack/compose.yaml \
  down --remove-orphans
```

## Operational Rules

01. Treat Compose project as one systemd-managed deployment unit.
02. Let Docker restart individual containers.
03. Use `Type=oneshot`.
04. Use `RemainAfterExit=yes`.
05. Start stack with `docker compose up -d --wait`.
06. Bound startup with `--wait-timeout`.
07. Validate with `docker compose config --quiet`.
08. Pull images in `ExecStartPre` before deployment (skip for air-gapped/pinned-digest stacks).
09. Use explicit project names and paths.
10. Use `compose stop` for normal shutdown.
11. Do not pass `--timeout` to `compose stop` — let `stop_grace_period` govern.
12. Reserve `compose down` for deliberate teardown.
13. Never use `down --volumes` in normal service lifecycle.
14. Give every long-running service explicit restart policy.
15. Add meaningful health checks.
16. Use dependency readiness conditions.
17. Use `service_completed_successfully` for one-shot init tasks.
18. Make applications resilient to runtime dependency loss.
19. Use `init: true` for proper signal delivery.
20. Define graceful shutdown periods.
21. Bound memory, CPU, PID, and log usage.
22. Use `deploy.resources` for resource constraints.
23. Pin production images.
24. Avoid runtime production builds.
25. Use `pull_policy` to control image freshness.
26. Monitor post-start health separately.
27. Do not assume systemd knows current health of detached containers.
28. Avoid blindly restarting entire stack for one unhealthy service.
29. Treat Docker daemon access as root-equivalent.
30. Apply container hardening where compatible.
31. Relax hardening deliberately for device-dependent services.
32. Ensure required filesystems are mounted before deployment.
33. Keep startup retries bounded.
34. Make failures visible rather than hiding in infinite restart loops.
35. Enable `live-restore` in Docker daemon config.
36. Use Compose `secrets:` for sensitive data.

## Agent Implementation Checklist

An agent implementing this design should verify all of the following.

### systemd Unit

- [ ] Uses `Type=oneshot`.
- [ ] Uses `RemainAfterExit=yes`.
- [ ] Requires `docker.service`.
- [ ] Orders after `docker.service`.
- [ ] Orders after `network-online.target`.
- [ ] Uses `RequiresMountsFor=` for relevant paths.
- [ ] Uses explicit `WorkingDirectory=`.
- [ ] Uses absolute Compose file paths.
- [ ] Uses explicit project name.
- [ ] Runs `compose config --quiet` before startup.
- [ ] Runs `compose pull` in `ExecStartPre` (or skips for air-gapped/pinned-digest).
- [ ] Runs `compose up -d --wait`.
- [ ] Uses bounded wait timeout.
- [ ] Uses `compose stop` (without `--timeout`) for normal shutdown.
- [ ] Has sufficiently long `TimeoutStopSec=`.
- [ ] Has `TimeoutStartSec=300` or higher.
- [ ] Has bounded startup retries.
- [ ] Does not use `down --volumes`.
- [ ] Sends command output to journal.
- [ ] Does not use unverified env vars.

### Compose Configuration

- [ ] Every long-running service has explicit restart policy.
- [ ] Critical services have meaningful health checks.
- [ ] Dependency readiness uses `service_healthy`.
- [ ] One-shot setup jobs use `service_completed_successfully`.
- [ ] Services tolerate runtime dependency failure.
- [ ] Services have `init: true`.
- [ ] Services have graceful shutdown settings.
- [ ] Memory bounded via `deploy.resources.limits.memory`.
- [ ] CPU bounded via `deploy.resources.limits.cpus`.
- [ ] PID counts bounded via `deploy.resources.limits.pids`.
- [ ] Log growth bounded.
- [ ] Images pinned.
- [ ] `pull_policy` set explicitly.
- [ ] Project naming stable.
- [ ] Writable paths explicit.
- [ ] Read-only root filesystems used where possible.
- [ ] Unnecessary capabilities dropped.
- [ ] Privilege escalation disabled.
- [ ] Containers run as non-root where possible.
- [ ] Secrets passed via `secrets:`, not embedded in images.
- [ ] Host mounts minimal and explicit.
- [ ] Device-dependent services document hardening relaxations.

### Monitoring

- [ ] Initial readiness checked with `compose up --wait`.
- [ ] Ongoing health monitored separately.
- [ ] Unhealthy state generates alert.
- [ ] Exited containers generate alert.
- [ ] Restart loops generate alert.
- [ ] Disk usage monitored.
- [ ] Volume growth monitored.
- [ ] Host memory pressure monitored.
- [ ] Docker daemon health monitored.
- [ ] Whole-stack automatic restart avoided unless explicitly justified.

### Validation

- [ ] `systemd-analyze verify` passes for unit.
- [ ] `docker compose config --quiet` passes.
- [ ] Stack starts successfully after reboot.
- [ ] Stack stops gracefully.
- [ ] Stack survives individual container failure.
- [ ] Restart policies behave as intended.
- [ ] Health checks transition correctly.
- [ ] Dependency startup ordering behaves correctly.
- [ ] Logs remain bounded.
- [ ] Persistent data survives restart.
- [ ] Persistent data survives normal systemd stop/start.
- [ ] Deliberate `compose down` does not remove volumes unless explicitly requested.
- [ ] Failure states remain observable.
- [ ] `jq` installed if using health check script.
- [ ] Compose v2.20+ verified on target host.
