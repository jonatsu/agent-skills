# Docker Compose

Use Compose to define a multi-container application and its local resource relationships.

## Model the Application

Give the project a stable name when scripts, units, or operators invoke it from different directories. Declare each
service's image or build, command, mounts, ports, networks, health check, restart behavior, and dependencies from its
actual role.

Use separate overlays or profiles when development and production genuinely differ. Inspect the merged model with:

```bash
docker compose -f compose.yaml -f compose.production.yaml config --quiet
```

The quiet form avoids printing an interpolated model that may contain credentials. It still evaluates interpolation and
file references, so supply the same environment and files the deployment will use.

## Handle State and Secrets

Identify every named volume and bind mount before changing lifecycle commands. Prefer long bind-mount syntax with
`create_host_path: false` when a missing host path should fail instead of becoming a new directory.

Grant a Compose secret to each service that needs it. For a file-backed secret, host file ownership remains
load-bearing: Docker Compose implements it as a bind mount and ignores long-syntax `uid`, `gid`, and `mode` remapping.
Check the effective permissions as the container user.

Keep development placeholder credentials out of production overlays. Do not render secret-bearing configuration into
logs or review output.

## Express Readiness Correctly

A health check should test the service behavior needed by its consumers and use a command available inside the image.
Long-form `depends_on` can wait for a healthy dependency or a successful one-shot job during startup. Applications must
still tolerate dependency loss after startup.

Use exec-form commands and stop signals that let the workload receive termination. Set `stop_grace_period` from measured
shutdown behavior, including state flushes and in-flight work.

## Harden Per Service

For a compatible Linux workload, start with:

```yaml
services:
  app:
    image: registry.example/app@sha256:<resolved-digest>
    user: "10001:10001"
    read_only: true
    tmpfs:
      - /tmp:size=64m,mode=1777
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges=true
    pids_limit: 256
```

Add writable mounts, capabilities, devices, published ports, and resource values from workload evidence. Validate the
result on the target engine because host security modules and rootless mode can change effective behavior.

## Classify Lifecycle Commands

Compose commands sort into `SKILL.md`'s "Preserve User Authority" classification: `config --quiet`, `ps`, and ordinary
log reads inspect; `pull`, `build`, `create`, `start`, `up`, `stop`, `restart`, and `exec` mutate; `down`, `rm`,
`down --volumes`, and volume removal destroy alongside the commands already named there.

Resolve the project name, files, profiles, services, and volumes before a destructive command. Obtain explicit authority
when the request did not already name that operation and target.
