---
name: containers
description: "Docker and OCI containers end-to-end — Dockerfile authoring, multi-stage builds, docker-compose (dev + prod), BuildKit, CI/CD, security hardening, CVE scanning (Trivy/Grype/Hadolint), SBOM, image signing (cosign), runtime hardening (seccomp, AppArmor, Linux capabilities, read-only fs), Kubernetes pod security (PSA, NetworkPolicy, RBAC, Kyverno), and docker-compose systemd deployment (oneshot units, restart policies, graceful shutdown, GPU passthrough). Use for building, running, hardening, scanning, or debugging containers; Dockerfile reviews; distroless migration; container CVEs; supply-chain security; K8s workload security; compose systemd unit design."
metadata:
  author: Joonas Onatsu
  license: GPL-3.0
  tags:
    - docker
    - dockerfile
    - docker-compose
    - containers
    - containerization
    - security
    - hardening
    - cve
    - trivy
    - grype
    - sbom
    - cosign
    - seccomp
    - apparmor
    - kubernetes
    - distroless
    - ci-cd
    - buildkit
---

# Containers

IRON LAW: Every production container MUST be non-root, use minimal base image, scanned for CVEs before deployment. Missing any of three → skill not done.

Build, run, scan, harden, deploy OCI containers with Docker, docker-compose, BuildKit, Kubernetes.

---

## When to Use This Skill

- Writing, editing, reviewing `Dockerfile`, `docker-compose.yml`, Kubernetes workload manifest
- Multi-stage builds, base image choice (distroless, slim, alpine, scratch), image size
- Container security, hardening, CVE scanning, SBOM, image signing, supply chain
- "Is my Dockerfile secure?", "reduce image attack surface?", "fix container CVEs"
- Trivy, Grype, Snyk, Hadolint, Syft, cosign, Sigstore
- seccomp, AppArmor, Linux capabilities, `--read-only`, `--cap-drop`, runtime security
- Kubernetes Pod Security Admission, NetworkPolicy, RBAC, Kyverno, OPA Gatekeeper
- BuildKit, `docker buildx`, multi-platform builds, build caching
- docker-compose for dev, staging, production

## When NOT to Use This Skill

- General Kubernetes orchestration beyond workload security → other K8s-focused skills
- Application-level security (SQLi, XSS, auth) → API/app-security skills
- Generic CI/CD pipeline design not tied to containers → CI/CD skills

---

## Agent Guardrail: Destructive Actions Require Confirmation

Before executing any command that destroys or irreversibly modifies containers,
images, volumes, networks, or persistent data, ask for explicit user
confirmation. This includes but is not limited to:

- `docker rm`, `docker rmi`, `docker system prune`, `docker volume rm`
- `docker compose down` (with or without `--volumes`, `--remove-orphans`)
- `docker builder prune`
- Any command that deletes or overwrites existing container artifacts

Read-only operations (inspect, logs, ps, config validation, scan) do not
require confirmation.

## Agent Guardrail: Model and Runtime Safety

- **Secrets**: Never echo, log, or persist secrets (tokens, passwords, keys) in
  prompts, command output, or generated files. Use BuildKit
  `--mount=type=secret` for Dockerfile secrets; use Compose `secrets:` for
  runtime. Prefer ephemeral credential helpers over env vars.
- **Least privilege**: Every container MUST run as non-root with
  `--cap-drop ALL`. Re-add capabilities only with documented justification.
  Never suggest `--privileged` or host-network mode without explicit user
  request and warning.
- **Immutable references**: Always pin images to `@sha256:` digest in
  production contexts. Never recommend `:latest` for deployments. Use
  `pull_policy: never` for air-gapped or pinned-digest stacks.
- **Validation**: Scan images (Trivy/Grype) and lint Dockerfiles (Hadolint)
  before suggesting deployment. Validate Compose config with `config --quiet`
  before any `up` command. Never skip scan gates for production images.

---

## Step 1: Understand Context Before Acting

Detect current state before recommending changes:

```bash
# Find Dockerfiles and compose files
find . -maxdepth 4 -type f \( -name 'Dockerfile*' -o -name 'docker-compose*.y*ml' -o -name 'compose*.y*ml' \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*'

# Inspect base images currently in use
grep -rE '^FROM ' $(find . -maxdepth 4 -name 'Dockerfile*' -not -path '*/node_modules/*') 2>/dev/null

# Check for existing security tooling
ls .trivyignore .hadolint.yaml .snyk .dockerignore 2>/dev/null

# Check for Kubernetes manifests
find . -maxdepth 4 -type f -name '*.y*ml' \( -path '*/k8s/*' -o -path '*/manifests/*' -o -path '*/deploy/*' \)
```

Adapt recommendations to:

- Tech stack (Go/Rust static → scratch, Node/Python → distroless/slim, JVM → distroless-java)
- Docker-only or Kubernetes target
- CI platform in use (scanner integration)
- Distance of current base images from best practice

---
## Decision Tree: What Task Am I On?

| Task | Primary reference | Key output |
|---|---|---|
| Write / edit Dockerfile | `references/dockerfile-patterns.md`, `references/base-image-comparison.md` | Multi-stage, non-root, pinned digest, healthcheck |
| Compose for dev or prod | `references/docker-compose.md` | Compose file with hardening at prod tier |
| Compose systemd deployment | `references/compose-systemd.md` | Type=oneshot unit, restart policies, graceful shutdown, GPU passthrough |
| Set up build in CI | `references/ci-cd.md` | GHA workflow with buildx + cache + SHA-pinned actions |
| Scan image for CVEs | `references/image-scanning.md` | Trivy/Grype scan, SBOM, `.trivyignore` with justifications |
| Sign / verify images | `references/image-scanning.md` (Cosign section) | Cosign keyless via OIDC, SBOM attestation |
| Harden `docker run` / compose | `references/runtime-security.md` | `--read-only`, `--cap-drop ALL`, seccomp, no-new-privs |
| Kubernetes workload security | `references/kubernetes-pod-security.md` | PSA `restricted`, NetworkPolicy default-deny, minimal RBAC |
| Choose base image | `references/base-image-comparison.md` | Distroless > slim > alpine > full; scratch for static |

---

## The Five Layers of Container Security

```
1. Image Build        → Minimal base, no secrets, non-root, pinned digest
2. Image Scanning     → CVE scan, SBOM, secret scan, Dockerfile lint
3. Runtime Security   → Capabilities, seccomp, AppArmor, resource limits, read-only fs
4. Supply Chain       → Signed images, pinned digests, trusted registries, attestations
5. Kubernetes Layer   → Pod Security Admission, NetworkPolicy, RBAC, Kyverno / OPA
```

Work through layers in order — hardening image gives most leverage.

---

## Layer 1: Dockerfile — Minimum Bar

Every production Dockerfile MUST have all of the following. See `references/dockerfile-patterns.md` for full examples.

- [ ] `# syntax=docker/dockerfile:1` at top (enables BuildKit features)
- [ ] Multi-stage build — build tools and dev dependencies excluded from runtime
- [ ] Minimal base image — distroless preferred, then slim; avoid full `node:20`, `ubuntu:*`
- [ ] Base image pinned to `@sha256:...` digest, not just tag
- [ ] `USER` directive switches to non-root before `CMD` / `ENTRYPOINT`
- [ ] No secrets in `ENV`, `ARG`, or `RUN` — use `RUN --mount=type=secret,id=...` (BuildKit)
- [ ] `HEALTHCHECK` defined
- [ ] `ENTRYPOINT` in exec form (`["node", "server.js"]`), not shell form
- [ ] OCI labels (`org.opencontainers.image.source`, `.revision`, `.licenses`)
- [ ] `.dockerignore` excludes `.git`, `.env`, secrets, tests, docs, `node_modules`

Full hardened Dockerfile example, secrets mount pattern, non-root user setup for debian/alpine/distroless: `references/dockerfile-patterns.md`.

Base image trade-offs (scratch vs distroless vs alpine vs slim, sizes, CVE counts, musl vs glibc): `references/base-image-comparison.md`.

---

## Layer 2: Image Scanning — Fail CI on HIGH/CRITICAL

Every production image MUST be scanned in CI. Use Trivy (recommended), Grype, or Snyk. Add Hadolint for Dockerfile linting.

Minimum CI checks:

```bash
# Dockerfile lint
hadolint --failure-threshold warning Dockerfile

# Vulnerability scan — fail on HIGH/CRITICAL
trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:${SHA}

# Secret scan
trivy image --scanners secret myapp:${SHA}

# SBOM
syft myapp:${SHA} -o cyclonedx-json > sbom.json
```

Full scanner setup (Trivy, Grype, Hadolint, `.trivyignore`, `.hadolint.yaml`), CI integration (GitHub Actions with SHA-pinned action versions and SARIF upload), SBOM generation, cosign keyless signing/attestation, admission control policies: `references/image-scanning.md`.

---

## Layer 3: Runtime Hardening — Minimum `docker run` / Compose Flags

Every production container MUST run with:

```bash
docker run \
  --read-only \
  --tmpfs /tmp:noexec,nosuid,size=100m \
  --user 10001:10001 \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  --security-opt seccomp=./seccomp.json \
  --pids-limit 100 \
  --memory 512m --cpus 1.0 \
  myapp:latest
```

Most web apps need ZERO Linux capabilities — `--cap-drop ALL` alone often enough. Only re-add specific caps with documented justification. Full docker-compose hardened service definition, seccomp profile authoring workflow, AppArmor setup, capability trade-off table: `references/runtime-security.md`.

Ready-to-use minimal seccomp allowlist for web servers: `references/seccomp-profile-template.json`.

---

## Layer 4: Supply Chain — Sign, Pin, Attest

- Sign every image with Cosign (keyless via OIDC — no long-lived keys)
- Pin base images to `@sha256:` digest; automate updates with Renovate or Dependabot
- Generate SBOM with Syft and attach as attestation via `cosign attest`
- Use registries with built-in scanning (ECR enhanced, GCP Artifact Registry, ACR)
- Verify signatures at admission (Kyverno `verifyImages`)

Full pipeline (GHA workflow signing + SBOM attestation + Kyverno verification policy): `references/image-scanning.md`.

---

## Layer 5: Kubernetes Pod Security — Minimum Spec

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    fsGroup: 10001
    seccompProfile: { type: RuntimeDefault }
  automountServiceAccountToken: false
  containers:
    - name: app
      image: ghcr.io/org/myapp@sha256:<digest>   # digest, not tag
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities: { drop: ["ALL"] }
        runAsNonRoot: true
      resources:
        requests: { memory: 128Mi, cpu: 100m }
        limits:   { memory: 512Mi, cpu: 500m }
```

Enforce with Pod Security Admission at `restricted` level per namespace. Apply default-deny NetworkPolicy, allow only required traffic. Use narrowly-scoped RBAC (specific `resourceNames`, never `verbs: ["*"]`). Use Workload Identity (EKS IRSA / GKE WI) instead of long-lived cloud credentials in Secrets.

Full manifests, PSA rollout (audit → warn → enforce), NetworkPolicy examples, RBAC audit commands, Kyverno / OPA Gatekeeper policy templates, secrets management options (External Secrets Operator, Sealed Secrets, Vault, SOPS), Falco runtime detection: `references/kubernetes-pod-security.md`.

---

## Docker Compose — Dev vs Prod

Compose files diverge sharply between dev and prod:

| Concern | Dev | Prod |
|---|---|---|
| Source mount | `volumes: [.:/app]` | No — image is self-contained |
| Env / debug | `DEBUG=1`, plaintext passwords | env from secrets store; `DEBUG=0` |
| Build context | `build: .` | `image: ghcr.io/org/app@sha256:...` |
| User | root ok for hot-reload tooling | `user: "10001:10001"`, non-root always |
| Filesystem | rw | `read_only: true` + `tmpfs` for writable paths |
| Caps | default | `cap_drop: [ALL]`, add back per-service |
| Resources | unbounded | `mem_limit`, `cpus`, `pids_limit` |
| Ports | exposed | published only where required |
| Healthcheck | optional | required |
| Networks | default | explicit, `internal: true` for backend |

Both examples with full hardening applied at prod tier: `references/docker-compose.md`.

---

## CI/CD — GitHub Actions

Production build workflow requires:

- SHA-pinned action versions (never `@v3` or `@main`)
- BuildKit (`docker/setup-buildx-action`)
- Multi-platform where needed (`--platform linux/amd64,linux/arm64`)
- Layer caching (registry cache or `cache-from: type=gha`)
- OIDC login to registry (no long-lived tokens)
- Lint + scan gates before push
- Cosign signing + SBOM attestation after push
- SARIF upload to GitHub Security tab

Full workflow, cache strategies, multi-platform buildx setup: `references/ci-cd.md`.

---

## Common Pitfalls & Fixes

| Problem | Root Cause | Fix |
|---|---|---|
| Image runs as root | No `USER` directive | Add `RUN useradd ...` + `USER appuser` before CMD |
| Secret in `docker history` | `ENV` or `RUN curl -H "Bearer $TOKEN"` | Use `RUN --mount=type=secret,id=...` |
| Large image, many CVEs | Full base (`node:20`, `ubuntu`) | Switch to `node:20-slim` or distroless |
| App crashes with `--read-only` | Writes to `/tmp` or app dir | Add `--tmpfs /tmp:noexec,nosuid,size=100m` |
| Trivy blocks CI on unfixable CVEs | No ignore file | Add `.trivyignore` with justified entries + issue link |
| Container needs `SYS_ADMIN` | Missing `--cap-drop` investigation | Almost always avoidable — audit what syscall actually needed |
| Tags drift over time | Mutable tags | Pin to `@sha256:`; Renovate/Dependabot auto-PRs |
| K8s pod rejected by PSA | Missing security context fields | Add `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false` |
| App can't write to filesystem in K8s | `readOnlyRootFilesystem: true` | Mount `emptyDir` for writable paths |
| Musl compatibility issues on alpine | native modules (`bcrypt`, `sharp`, numpy) | Switch to `*-slim` (glibc) |
| `.env` accidentally in image | Missing `.dockerignore` | Add `.env`, `.env.*`, `*.pem`, `*.key`, `.git` |
| Compose runs as root by default | No `user:` field | Set `user: "10001:10001"` + build with matching UID |

---

## Pre-Delivery Checklist

### Dockerfile

- [ ] `# syntax=docker/dockerfile:1`
- [ ] Multi-stage build; no build tools or devDeps in runtime image
- [ ] Minimal base (distroless / slim / alpine / scratch) — NOT full `node:20` / `ubuntu:*`
- [ ] Base image pinned to `@sha256:<digest>`
- [ ] Non-root `USER` declared before `CMD` / `ENTRYPOINT`
- [ ] No secrets in `ENV`, `ARG`, or `RUN`
- [ ] `HEALTHCHECK` defined
- [ ] `ENTRYPOINT` in exec form
- [ ] OCI labels present
- [ ] `.dockerignore` excludes `.git`, `.env*`, `*.pem`, tests

### Image Scanning

- [ ] Trivy or Grype scan in CI; fails on HIGH/CRITICAL
- [ ] Hadolint passes at `warning` threshold
- [ ] Secret scan run on image
- [ ] SBOM generated (CycloneDX or SPDX) and stored
- [ ] `.trivyignore` entries have justification comments

### Runtime (Docker / Compose)

- [ ] `--read-only` root filesystem, `tmpfs` for writable paths
- [ ] `--cap-drop ALL` (add back only what's documented)
- [ ] `--security-opt no-new-privileges:true`
- [ ] Custom or default seccomp profile applied
- [ ] Resource limits set (`memory`, `cpus`, `pids-limit`)

### Supply Chain

- [ ] Images signed with Cosign (keyless via OIDC preferred)
- [ ] SBOM attached as attestation
- [ ] Registry with scanning enabled

### Kubernetes

- [ ] `readOnlyRootFilesystem: true`
- [ ] `allowPrivilegeEscalation: false`
- [ ] `runAsNonRoot: true` with explicit UID
- [ ] `capabilities.drop: ["ALL"]`
- [ ] Resource `requests` AND `limits` defined
- [ ] `automountServiceAccountToken: false` unless K8s API access needed
- [ ] Namespace labelled with PSA `enforce=restricted`
- [ ] Default-deny NetworkPolicy applied; allow rules narrowly scoped
- [ ] RBAC uses specific `resourceNames`, no wildcard `verbs: ["*"]`
- [ ] Images referenced by `@sha256:` digest

---

## Reference Files

- `references/dockerfile-patterns.md` — Multi-stage patterns, non-root user setup, secrets via BuildKit, hardened Dockerfile example for Node/Python/Go/Rust
- `references/docker-compose.md` — Dev + prod compose examples; hardened service definition; healthchecks; networks
- `references/compose-systemd.md` — systemd unit design for Compose stacks (Type=oneshot), restart policies, graceful shutdown, GPU passthrough, pull policies, air-gapped deployments
- `references/ci-cd.md` — GitHub Actions with SHA-pinned steps, buildx, multi-platform, cache, signing, SARIF
- `references/image-scanning.md` — Trivy, Grype, Hadolint, Syft, cosign; ignore files; CI integration; SBOM + attestation; admission control
- `references/runtime-security.md` — `docker run` hardening flags, Linux capabilities table, seccomp workflow, AppArmor
- `references/base-image-comparison.md` — Size, CVE count, shell / package-manager trade-offs across distroless, alpine, slim, scratch, full
- `references/kubernetes-pod-security.md` — PSA, NetworkPolicy, RBAC, Kyverno/OPA policies, service accounts, Falco, secrets management
- `references/seccomp-profile-template.json` — Minimal syscall allowlist for typical web servers; extend as needed

---

## Related Skills

- `docker` (deprecated after this merge) — general Docker usage
- `container-security-hardening` (deprecated after this merge) — security-only variant
- `github-actions-advanced` — general CI pipeline patterns
- `kubernetes-architect` — full K8s architecture beyond workload security

## Limitations

- Seccomp and AppArmor are Linux-only. Docker Desktop on macOS / Windows uses different mechanisms (Hyper-V VM, WSL2); some hardening flags advisory there.
- Not substitute for penetration testing or formal security audit.
- Kyverno / OPA Gatekeeper snippets are starting points; production policies MUST be reviewed against actual workload requirements.
- Base image size and CVE counts drift over time — verify current values with `trivy image <name>` before decisions.

## Attribution

See `ATTRIBUTIONS.md` for upstream sources and adaptation notes.
