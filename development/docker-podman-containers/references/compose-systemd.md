# Compose Managed by systemd

Load the `systemd-units` skill for unit semantics, target-version checks, installation paths, and live-host authority. This
reference covers only the boundary between a Compose project, Docker's container supervision, and a systemd unit. For a
Podman workload under systemd, prefer Quadlet over this oneshot-Compose pattern; see `references/podman-differences.md`.

## Choose Ownership Deliberately

For a single-host Compose project, Docker normally supervises long-running containers through each service's restart
policy. A systemd unit can order initial deployment at boot and provide administrative start, stop, and reconciliation.
External monitoring must observe later container health because an exited Compose CLI does not represent it.

Use a detached oneshot unit only when that ownership model matches the target:

```ini
[Unit]
Description=Example Compose project
Requires=docker.service
After=docker.service network-online.target
Wants=network-online.target
RequiresMountsFor=/opt/example

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/example
ExecStartPre=/usr/bin/docker compose --project-name example --file /opt/example/compose.yaml config --quiet
ExecStart=/usr/bin/docker compose --project-name example --file /opt/example/compose.yaml up --detach --wait
ExecReload=/usr/bin/docker compose --project-name example --file /opt/example/compose.yaml up --detach --wait
ExecStop=/usr/bin/docker compose --project-name example --file /opt/example/compose.yaml stop
TimeoutStartSec=300
TimeoutStopSec=120

[Install]
WantedBy=multi-user.target
```

Confirm every directive and Compose option on the target versions. Set a bounded Compose wait timeout when supported and
derive both systemd timeouts from measured startup and cumulative shutdown behavior.

Do not put `pull`, `--remove-orphans`, `down`, volume removal, image pruning, or builder pruning in the ordinary unit
lifecycle. Those operations have distinct network, replacement, or deletion effects. Run them through an explicitly
authorized deployment or maintenance workflow after resolving the project and persistent data.

Give long-running services an appropriate Compose restart policy. Do not expect `Restart=` on an exited oneshot unit to
supervise individual containers. Ensure applications handle dependency loss after startup; Compose startup ordering does
not provide runtime recovery.

## Validate Before Installation

1. Run `docker compose ... config --quiet` with the deployment environment.
2. Run `systemd-analyze verify` against the unit on the target system or a matching image.
3. Inspect the merged unit definition after installation and manager reload.
4. Start or reload only with authority for the live project.
5. Verify container readiness, restart behavior, graceful stop, persistence, logs, and boot behavior.

Stopping, restarting, enabling, disabling, or reloading a live unit changes host state. Reuse authorization from the
request and ask when the unit, impact, or data boundary remains unclear.
