# Dockerfile Patterns

Multi-stage builds, base image selection, non-root user setup, secrets handling, and full hardened examples
for common language runtimes.

See also:

- `base-image-comparison.md` for the full distroless / alpine / slim / scratch trade-off matrix
- `image-scanning.md` for scanning the resulting image
- `runtime-security.md` for `docker run` hardening applied to the image

---

## 1. Anatomy of a Hardened Dockerfile

Every production Dockerfile SHOULD follow this structure:

```dockerfile
# syntax=docker/dockerfile:1                       # Enables BuildKit features

# ── Build stage ──────────────────────────────────────────
FROM <build-base>@sha256:<digest> AS builder
WORKDIR /build
COPY <lock-files> ./
RUN <install deps, cached via --mount=type=cache>
COPY . .
RUN <build>

# ── Runtime stage ────────────────────────────────────────
FROM <minimal-runtime-base>@sha256:<digest>
LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.revision="${BUILD_SHA}"
LABEL org.opencontainers.image.licenses="MIT"
WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /build/dist ./dist
USER nonroot:nonroot                              # Never run as root
EXPOSE <port>
HEALTHCHECK <cmd>
ENTRYPOINT ["<binary>", "<arg>"]                  # Exec form, not shell form
```

---

## 2. Multi-Stage Build — Separate Build from Runtime

NEVER ship build tools, compilers, or dev dependencies in the runtime image.

### Node.js

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20-slim AS builder
WORKDIR /build
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build && npm prune --production

FROM gcr.io/distroless/nodejs20-debian12@sha256:<digest>
WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /build/dist         ./dist
COPY --from=builder --chown=nonroot:nonroot /build/node_modules ./node_modules
USER nonroot:nonroot
EXPOSE 3000
CMD ["dist/server.js"]
```

### Python

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3-debian12@sha256:<digest>
WORKDIR /app
COPY --from=builder /venv /venv
COPY --from=builder --chown=nonroot:nonroot /build/app ./app
ENV PATH="/venv/bin:$PATH"
USER nonroot:nonroot
EXPOSE 8000
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Go / Rust — fully static binary → `scratch`

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.22-alpine AS builder
WORKDIR /build
COPY go.* ./
RUN --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=cache,target=/go/pkg/mod \
    go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-s -w -extldflags=-static" -o app .

FROM scratch                                       # Zero attack surface
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /usr/share/zoneinfo            /usr/share/zoneinfo
COPY --from=builder /build/app                     /app
USER 65532:65532
ENTRYPOINT ["/app"]
```

### Java / JVM

```dockerfile
# syntax=docker/dockerfile:1

FROM eclipse-temurin:21-jdk AS builder
WORKDIR /build
COPY . .
RUN ./gradlew bootJar --no-daemon

FROM gcr.io/distroless/java21-debian12@sha256:<digest>
WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /build/build/libs/app.jar ./app.jar
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## 3. Run as Non-Root User

### Debian / Ubuntu base

```dockerfile
RUN groupadd -r appgroup --gid 10001 && \
    useradd -r -g appgroup --uid 10001 --no-log-init appuser

COPY --chown=appuser:appgroup . /app
USER appuser
```

### Alpine base

```dockerfile
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup
USER appuser
```

### Distroless

`nonroot` (UID 65532) is already defined:

```dockerfile
USER nonroot:nonroot
```

### Scratch

There is no user database. Reference by numeric UID:GID:

```dockerfile
USER 65532:65532
```

---

## 4. Pin Base Images to Digest

```dockerfile
# ❌ Mutable — image can be silently overwritten (supply chain attack)
FROM node:20-slim

# ✅ Immutable — SHA256 digest
FROM node:20-slim@sha256:a1b2c3d4e5f6789abcdef0123456789abcdef0123456789abcdef0123456789ab
```

Get the current digest:

```bash
docker pull node:20-slim
docker inspect node:20-slim --format='{{index .RepoDigests 0}}'
```

Automate digest updates with Renovate:

```json
{
  "extends": ["config:base"],
  "dockerfile": { "enabled": true },
  "pinDigests": true
}
```

Or Dependabot:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: docker
    directory: /
    schedule: { interval: weekly }
    open-pull-requests-limit: 5
```

---

## 5. Never Bake Secrets Into Images

```dockerfile
# ❌ NEVER — visible in `docker history` and layer cache
ENV AWS_SECRET_ACCESS_KEY=supersecret
RUN curl -H "Authorization: Bearer $TOKEN" https://api.example.com > config.json
ARG API_KEY                                        # Also unsafe

# ✅ BuildKit secret mount — never persisted in any layer
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=api_token \
    curl -H "Authorization: Bearer $(cat /run/secrets/api_token)" \
      https://api.example.com/config > config.json
```

Build with:

```bash
docker build --secret id=api_token,src=./token.txt .
```

Check an existing image for leaked secrets:

```bash
docker history --no-trunc myapp:latest | grep -iE 'secret|key|password|token'
trivy image --scanners secret myapp:latest
```

---

## 6. Healthchecks & Exec-Form Entrypoint

```dockerfile
# ✅ Exec form — no shell process spawned; signals delivered correctly
ENTRYPOINT ["node", "server.js"]

# ❌ Shell form — extra sh process, breaks signal handling
# ENTRYPOINT node server.js

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["node", "-e", "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode===200?0:1))"]
```

For distroless / scratch images that don't have `curl`, use the language runtime for the healthcheck (as
above) or ship a static healthcheck binary from the builder stage.

---

## 7. `.dockerignore` — Minimum Excludes

```dockerignore
# Version control & CI
.git
.github
.gitignore

# Secrets & keys
.env
.env.*
*.pem
*.key
*.crt
secrets/

# Language ecosystems
node_modules
__pycache__
.pytest_cache
.venv
venv/
target/
build/
dist/

# Test & dev
coverage/
tests/
*.log
.DS_Store

# Docker
Dockerfile*
docker-compose*
.dockerignore

# Docs (unless served by the app)
README.md
docs/
```

---

## 8. Full Hardened Node.js Dockerfile (Reference)

```dockerfile
# syntax=docker/dockerfile:1

# ── Build stage ──────────────────────────────────────────
FROM node:20-slim@sha256:<pin-digest> AS builder
WORKDIR /build
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build && npm prune --production

# ── Runtime stage ────────────────────────────────────────
FROM gcr.io/distroless/nodejs20-debian12@sha256:<pin-digest>

LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.revision="${BUILD_SHA}"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /build/dist         ./dist
COPY --from=builder --chown=nonroot:nonroot /build/node_modules ./node_modules

USER nonroot:nonroot
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["node", "-e", "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode===200?0:1))"]

CMD ["dist/server.js"]
```

---

## 9. BuildKit Cache Mounts

BuildKit `--mount=type=cache` avoids re-downloading dependencies between builds without persisting them into
image layers.

```dockerfile
# npm
RUN --mount=type=cache,target=/root/.npm npm ci

# pip
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Go build cache + module cache
RUN --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=cache,target=/go/pkg/mod \
    go build ./...

# apt (Debian/Ubuntu)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends <pkgs>
```

Enable BuildKit:

```bash
export DOCKER_BUILDKIT=1
# or
docker buildx build ...
```

---

## 10. Common Dockerfile Anti-Patterns

| Anti-pattern                            | Why it's wrong                               | Fix                                                                        |
| --------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------- |
| `FROM ubuntu:latest`                    | Massive attack surface, mutable tag          | Use `distroless` / `slim`, pin digest                                      |
| Running as root                         | Container escapes reach host as root         | `USER <non-root>` before `CMD`                                             |
| `apt-get install` without cleanup       | Bloats image with apt cache                  | `&& rm -rf /var/lib/apt/lists/*` in same layer                             |
| `COPY . .` before `RUN npm ci`          | Cache-busts dep install on every code change | Copy lock files first, install deps, then `COPY . .`                       |
| `ENV SECRET=xxx`                        | Secret baked into layer                      | `RUN --mount=type=secret,id=...`                                           |
| Single-stage build with build tools     | Compiler / dev deps ship to prod             | Multi-stage: build in stage 1, copy artifacts to minimal stage 2           |
| `ENTRYPOINT bash -c "..."` (shell form) | Extra process, signals broken                | Exec form: `ENTRYPOINT ["bash", "-c", "..."]` — or better, no shell at all |
| No `HEALTHCHECK`                        | Orchestrator can't tell healthy from broken  | Add `HEALTHCHECK`                                                          |
| `USER 0` or missing `USER`              | Runs as root                                 | Set explicit non-root UID/GID                                              |
| Pinning to floating tag (`node:20`)     | Image drifts silently                        | Pin to `@sha256:` digest; automate with Renovate                           |
