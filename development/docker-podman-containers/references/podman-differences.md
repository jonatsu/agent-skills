# Podman Differences

Podman runs the same OCI images and a Docker-compatible CLI, so the Dockerfile, Compose, runtime-security,
scanning, and CI guidance in the other references applies unchanged unless a point below overrides it. This
reference covers only where Podman diverges from Docker. Confirm every version-gated behavior against installed
`--help`, `podman info`, and the official documentation; Podman's defaults have moved across major versions.

Podman is a Docker-compatible CLI, not a guaranteed strict drop-in. Do not assume a Docker command or default
carries over; check the specific point.

## Runtime Model

- **Daemonless, fork-exec.** There is no long-running engine daemon; each `podman` invocation runs the
  container directly. A systemd unit that orders `docker.service` (see `compose-systemd.md`) has no daemon to
  require under Podman — order the Podman socket or the generated unit instead.
- **Rootless by default, via user namespaces.** Rootless Podman maps container root to the invoking user
  through `/etc/subuid` and `/etc/subgid`; missing entries make commands fail. Container UID 0 is already
  isolated from host root without `--userns` remapping.
- **Ports below 1024** cannot be bound rootless without `net.ipv4.ip_unprivileged_port_start`, a capability
  grant, or a proxy — an unprivileged process is denied `CAP_NET_BIND_SERVICE`.
- **Volume mount suffixes Docker lacks:** `:U` recursively chowns the source to the container's UID/GID (slow
  on many-inode volumes); `:z` applies a shared SELinux label, `:Z` a private one. In a pod every container
  shares the pod's SELinux label, so one container's `:Z` exposes the volume to the whole pod.
- **Rootless networking:** pasta is the default rootless network tool since Podman 5.0 (previously
  slirp4netns); netavark is the default network backend since 4.0 (CNI is deprecated). pasta copies the host
  interface IP into the container, so cross-container connectivity can need explicit configuration. Rootless
  bridge port-forwarding uses `rootlessport`, which does not preserve the client source IP unless
  `rootless_port_forwarder="pasta"` is set (experimental).

## Compose

Three paths, all pointing at the Podman socket
(`unix:///run/user/$UID/podman/podman.sock` rootless, `unix:///run/podman/podman.sock` rootful):

| Path                             | What it is                                                             |
| -------------------------------- | ---------------------------------------------------------------------- |
| `podman compose`                 | thin wrapper that execs an external provider against the Podman socket |
| `podman-compose`                 | a separate Python implementation of the Compose spec                   |
| Docker Compose via `DOCKER_HOST` | stock `docker compose` pointed at the Podman socket                    |

`podman compose` prefers `docker-compose` over `podman-compose` when both are installed; override with
`compose_providers` in `containers.conf` or `PODMAN_COMPOSE_PROVIDER`. The official docs state this precedence
but recommend no single path; choose from what the target has and verify the compose features it actually
supports. `docker-compose` behavior against the Podman socket is otherwise the `docker-compose.md` guidance.

## Quadlet — Podman's systemd Integration

Quadlet is a systemd generator: it reads declarative unit files at boot and on `systemctl daemon-reload` and
generates real `.service` units. It **replaces the deprecated `podman generate systemd`** (that command
survives for bug fixes only). For a Podman workload managed by systemd, prefer Quadlet over the
Docker-Compose-oneshot pattern in `compose-systemd.md`; load the `systemd-units` skill for unit semantics and
target-version checks.

- **Unit file types:** `.container`, `.pod`, `.kube`, `.network`, `.volume`, `.build`, `.image` (and
  experimental `.artifact`). Keys in `[Container]`/`[Pod]` map to the matching `podman create`/`pod create`
  options; standard `[Service]` and `[Install]` keys pass through to systemd.
- **Search paths.** Rootful, in precedence order: `/run/containers/systemd/`, `/etc/containers/systemd/`,
  `/usr/share/containers/systemd/`. Rootless: `$XDG_RUNTIME_DIR/containers/systemd/`,
  `~/.config/containers/systemd/`, then the `/etc` and `/usr` `.../users/${UID}` variants.
- **`daemon-reload` (or reboot) is required** for the generator to pick up new or changed files.
- **A rootless Quadlet is one placed in a rootless search path** under the user's own systemd instance.
  Quadlet does not honor `User=`/`Group=`/`DynamicUser=`; do not try to make a system unit "rootless" that way.
- **Restart gotcha:** a `.pod` defaults to `ExitPolicy=stop`, so a pod whose containers all exit cleanly
  returns 0 and does **not** trip `Restart=on-failure`. Set `Restart=always` when clean-exit restart is wanted.
- `.kube` wraps `podman kube play` against a `Yaml=` path; `podman kube play --down`/`--replace` manages that
  workload outside Quadlet.

## Buildah and Containerfile

- `podman build` uses Buildah's Go API; Buildah is likewise daemonless. `Containerfile` and `Dockerfile` share
  identical syntax and both names are recognized (`Containerfile` is Podman's preferred name). The
  `dockerfile-patterns.md` guidance applies as-is.
- Podman/Buildah-specific: a `LABEL io.containers.capabilities=CAP1,CAP2` in the Containerfile records the
  capability subset the resulting container should run with — no Docker equivalent.

## Security-Default Divergences

A Docker-hardening habit ported to Podman must account for these; do not assume the engine defaults match.

- **Smaller default capability set.** Podman defaults to 11 capabilities and drops `AUDIT_WRITE`, `MKNOD`, and
  `NET_RAW` that Docker grants. A workload relying on `NET_RAW` (raw sockets, `ping`) or `MKNOD` (device nodes)
  needs an explicit `--cap-add` under Podman that Docker did not require.
- **`userns` defaults to `host`.** On rootless Podman that already means the isolating subuid/subgid-mapped
  namespace, so Docker's `--userns=auto` reflex is redundant; `--userns=auto` on Podman instead requests a
  separate per-container allocation from the `containers` subuid/subgid range (a stronger, non-default mode
  needing its own `/etc/subuid` entry).
- **Seccomp** is a profile shared across Podman, Buildah, and CRI-O (`seccomp_profile` in `containers.conf`),
  not Docker's bundled default. Compare the actual profiles when the syscall set matters.

## Pods

A pod shares kernel namespaces across its containers through a default infra container (`--infra=true`, running
`/pause`). Kubernetes-style YAML runs directly via `podman kube play`; the `.pod` and `.kube` Quadlet types are
the systemd-managed wrappers around pod creation and `kube play`.

## CLI Parity Pitfalls

- No Podman equivalent for `docker buildx`/`builder`, `config`, `context`, `node`, `plugin`, `stack`, `swarm`,
  or `container update`/`update` (Podman does not alter a running container — recreate it). Orchestration is
  delegated to Kubernetes/CRI-O.
- `podman volume create` errors if the volume exists (Docker's is idempotent), and a bind mount of a
  nonexistent host path errors instead of creating it. Do not rely on the Docker auto-create behavior in a
  script.
