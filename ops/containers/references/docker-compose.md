# docker-compose — Dev and Prod Examples

Compose files diverge sharply between dev and prod. See the SKILL.md decision table for the summary of
differences; this file gives full examples with hardening applied where required.

See also:

- `dockerfile-patterns.md` for building the image the compose service runs
- `runtime-security.md` for the underlying `docker run` hardening flags that translate into `security_opt` /
  `cap_drop` / etc.

---

## 1. Development Compose

For local development. Optimizes for fast feedback: source mounted, hot reload, plaintext env, permissive
access.

```yaml
# compose.dev.yml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=1
      - DATABASE_URL=postgres://postgres:postgres@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  worker:
    build: .
    command: celery -A myproject worker -l info
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

---

## 2. Production Compose — Hardened

For prod. No source mount, credentials from env / secrets store, resource limits, read-only fs, dropped
capabilities.

```yaml
# compose.prod.yml
services:
  web:
    image: ghcr.io/org/myapp@sha256:<digest>       # Pin to digest
    ports:
      - "8000:8000"
    environment:
      - DEBUG=0
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped

    # ── Hardening ────────────────────────────────
    read_only: true
    user: "10001:10001"
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
      - /var/run:noexec,nosuid,size=10m
    cap_drop: [ALL]
    cap_add:
      - NET_BIND_SERVICE                           # Only if binding port < 1024
    security_opt:
      - no-new-privileges:true
      - seccomp:./seccomp.json
    pids_limit: 100
    mem_limit: 512m
    memswap_limit: 512m
    cpus: 1.0

    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

    networks:
      - backend
      - frontend

  db:
    image: postgres:16@sha256:<digest>
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password
    secrets:
      - postgres_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    networks:
      - backend

  redis:
    image: redis:7-alpine@sha256:<digest>
    restart: unless-stopped
    read_only: true
    tmpfs:
      - /tmp:noexec,nosuid,size=50m
    security_opt:
      - no-new-privileges:true
    cap_drop: [ALL]
    networks:
      - backend

  worker:
    image: ghcr.io/org/myapp@sha256:<digest>
    command: celery -A myproject worker -l info
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - db
      - redis
    restart: unless-stopped
    read_only: true
    user: "10001:10001"
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
    cap_drop: [ALL]
    security_opt:
      - no-new-privileges:true
    mem_limit: 512m
    cpus: 1.0
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true                                 # No external egress from backend

volumes:
  postgres_data:

secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt
```

---

## 3. Common Compose Commands

```bash
# Development
docker compose -f compose.dev.yml up -d
docker compose -f compose.dev.yml logs -f web
docker compose -f compose.dev.yml exec web python manage.py migrate
docker compose -f compose.dev.yml down                 # Stop
docker compose -f compose.dev.yml down -v              # Stop + remove volumes

# Production
docker compose -f compose.prod.yml pull                # Pull latest pinned digests
docker compose -f compose.prod.yml up -d --no-build

# Scale a service
docker compose up -d --scale worker=4

# Rebuild
docker compose up -d --build

# View resource usage
docker compose top
docker stats
```

---

## 4. Compose Anti-Patterns

| Anti-pattern                         | Why it's wrong                                                  | Fix                                                     |
| ------------------------------------ | --------------------------------------------------------------- | ------------------------------------------------------- |
| Same file for dev and prod           | Dev conveniences leak to prod (source mount, plaintext secrets) | Split `compose.dev.yml` / `compose.prod.yml`            |
| Passwords in `environment:`          | Persist in inspect output, logs, `.env` files in Git            | Use `secrets:` with `_FILE` env var pattern             |
| `build:` in prod                     | Prod runs unpinned code                                         | Use `image: ghcr.io/org/app@sha256:...`                 |
| No `depends_on.condition`            | Web starts before db is ready → connection errors               | `condition: service_healthy` with a proper healthcheck  |
| `restart: always` for one-shot jobs  | Restart loop on legitimate exit                                 | `restart: on-failure` or omit                           |
| Missing `healthcheck` in prod        | Compose can't tell healthy from broken                          | Add `healthcheck` and use it in `depends_on`            |
| Exposing DB port in prod             | Database reachable from outside host                            | Remove `ports:`; use `expose:` or internal network only |
| No `mem_limit` / `cpus` in prod      | One runaway service crashes the host                            | Set per-service limits                                  |
| Root user by default                 | Container escape hits host as root                              | `user: "<non-root-uid>:<gid>"`                          |
| Writable filesystem where not needed | Persistence you didn't intend, tampering surface                | `read_only: true` + `tmpfs` for `/tmp`                  |

---

## 5. Compose Override Pattern (`compose.override.yml`)

For local-only overrides on top of a shared `compose.yml`, use the auto-loaded `compose.override.yml`:

```yaml
# compose.yml — shared base (checked in)
services:
  web:
    image: ghcr.io/org/myapp:latest
    read_only: true
    user: "10001:10001"

# compose.override.yml — local dev only (gitignored)
services:
  web:
    build: .
    volumes:
      - .:/app
    read_only: false                               # Override for hot reload
    environment:
      - DEBUG=1
```

`docker compose up` picks both up automatically. In CI, use `docker compose -f compose.yml up` (no override)
to run the prod-shaped config.
