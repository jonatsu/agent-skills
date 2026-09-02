# MCP Server Recommendations

MCP (Model Context Protocol) servers extend Claude's capabilities by connecting to external tools and
services.

**Note**: These are common MCP servers. Use web search to find MCP servers specific to the codebase's services
and integrations.

## Setup & Team Sharing

**Connection methods:**

1. **Project config** (`.mcp.json`) - Available only in that directory
2. **Global config** (`~/.claude.json`) - Available across all projects
3. **Checked-in `.mcp.json`** - Available to entire team (recommended!)

**Tip**: Check `.mcp.json` into git so your whole team gets the same MCP servers.

**Debugging**: Use `claude --mcp-debug` to identify configuration issues.

## Data Flow and Credentials — Check Before Recommending

Every MCP server below is either **self-hosted** (runs on the user's machine or their infrastructure) or
**hosted** (a third party receives the queries).

MUST state which, for every server recommended, along with the credential it needs. A recommender that
silently routes a codebase's questions to an external service has made a security decision on the user's
behalf.

Prefer a self-hosted equivalent when one exists. Recommend a hosted server only when the capability genuinely
requires the vendor's service — a hosted issue tracker, error tracker, or cloud provider.

Also weigh context cost: every connected server's tool definitions load into every session. Two overlapping
servers cost twice for one capability.

---

## Documentation & Knowledge

### Docs-lookup MCP servers

**Best for**: Projects pinned to fast-moving libraries, where training-data recall produces hallucinated or
outdated APIs

| Recommend When      | Examples                    |
| ------------------- | --------------------------- |
| Frontend frameworks | React, Vue, Angular, Svelte |
| Backend frameworks  | Express, FastAPI, Django    |
| ORMs                | Prisma, Drizzle, SQLAlchemy |
| Third-party APIs    | Stripe, Twilio, SendGrid    |
| Cloud SDKs          | AWS SDK, Google Cloud       |
| AI/ML libraries     | LangChain, vendor SDKs      |

**Value**: Claude reads current documentation instead of recalling it, which cuts invented APIs and deprecated
patterns.

**Self-hosted first.** A local documentation indexer (for example `docs-mcp-server`, run as a container or a
local process) indexes the exact library versions the project pins, and no query leaves the machine. This is
the default recommendation.

**Hosted alternatives** exist and are quicker to set up, at the cost of sending every documentation query to a
vendor plus an API key. When recommending one, MUST say so explicitly and MUST verify its current endpoint and
auth requirements against the vendor's own docs before printing an install command — these change.

---

## Browser & Frontend

### Playwright MCP

**Best for**: Frontend projects needing browser automation, testing, or screenshots

| Recommend When            | Examples               |
| ------------------------- | ---------------------- |
| React/Vue/Angular app     | UI component testing   |
| E2E tests needed          | User flow validation   |
| Visual regression testing | Screenshot comparisons |
| Debugging UI issues       | See what user sees     |
| Form testing              | Multi-step workflows   |

**Value**: Claude can interact with your running app, take screenshots, fill forms, and verify UI behavior.

### Puppeteer MCP

**Best for**: Headless browser automation, web scraping

| Recommend When           | Examples          |
| ------------------------ | ----------------- |
| PDF generation from HTML | Report generation |
| Web scraping tasks       | Data extraction   |
| Headless testing         | CI environments   |

---

## Databases

### Supabase MCP

**Best for**: Projects using Supabase for backend/database

| Recommend When            | Examples                        |
| ------------------------- | ------------------------------- |
| Supabase project detected | `@supabase/supabase-js` in deps |
| Auth + database needs     | User management apps            |
| Real-time features        | Live data sync                  |

**Value**: Claude can query tables, manage auth, and interact with Supabase storage directly.

### Convex MCP

**Best for**: Projects using Convex as the backend (reactive database + server functions + auth + storage +
scheduling, all on one platform)

| Recommend When                       | Examples                                                                  |
| ------------------------------------ | ------------------------------------------------------------------------- |
| Convex project detected              | `convex` in deps, `convex/` directory present, `convex.json` at repo root |
| Real-time / reactive UI              | `useQuery` / `useMutation` / `useAction` from `convex/react`              |
| Mobile + Convex                      | `convex/react-native` in deps                                             |
| AI / chat / agent features on Convex | `@convex-dev/agent` in deps                                               |

**Value**: Claude can introspect the live deployment (tables, function specs, env vars, logs) and execute
queries/mutations against it via tools like `tables`, `function-spec`, `data`, `run-once-query`, `logs`,
`env list/set/get`. Run via `npx convex mcp start`.

### PostgreSQL MCP

**Best for**: Direct PostgreSQL database access

| Recommend When        | Examples            |
| --------------------- | ------------------- |
| Raw PostgreSQL usage  | No ORM layer        |
| Database migrations   | Schema management   |
| Data analysis tasks   | Complex queries     |
| Debugging data issues | Inspect actual data |

### Neon MCP

**Best for**: Neon serverless Postgres users

### Turso MCP

**Best for**: Turso/libSQL edge database users

---

## Version Control & DevOps

### GitHub MCP

**Best for**: GitHub-hosted repositories needing issue/PR integration

| Recommend When           | Examples                    |
| ------------------------ | --------------------------- |
| GitHub repository        | `.git` with GitHub remote   |
| Issue-driven development | Reference issues in commits |
| PR workflows             | Review, merge operations    |
| GitHub Actions           | CI/CD pipeline access       |
| Release management       | Tag and release automation  |

**Value**: Claude can create issues, review PRs, check workflow runs, and manage releases.

### GitLab MCP

**Best for**: GitLab-hosted repositories

### Linear MCP

**Best for**: Teams using Linear for issue tracking

| Recommend When           | Examples                        |
| ------------------------ | ------------------------------- |
| Linear workspace         | Issue references like `ABC-123` |
| Sprint planning          | Backlog management              |
| Issue creation from code | Auto-create issues for TODOs    |

---

## Cloud Infrastructure

### AWS MCP

**Best for**: AWS infrastructure management

| Recommend When          | Examples              |
| ----------------------- | --------------------- |
| AWS SDK in dependencies | `@aws-sdk/*` packages |
| Infrastructure as code  | Terraform, CDK, SAM   |
| Lambda development      | Serverless functions  |
| S3, DynamoDB usage      | Cloud data services   |

### Cloudflare MCP

**Best for**: Cloudflare Workers, Pages, R2, D1

| Recommend When     | Examples            |
| ------------------ | ------------------- |
| Cloudflare Workers | Edge functions      |
| Pages deployment   | Static site hosting |
| R2 storage         | Object storage      |
| D1 database        | Edge SQL database   |

### Vercel MCP

**Best for**: Vercel deployment and configuration

---

## Monitoring & Observability

### Sentry MCP

**Best for**: Error tracking and debugging

| Recommend When       | Examples                      |
| -------------------- | ----------------------------- |
| Sentry configured    | `@sentry/*` in deps           |
| Production debugging | Investigate errors            |
| Error patterns       | Group similar issues          |
| Release tracking     | Correlate deploys with errors |

**Value**: Claude can investigate Sentry issues, find root causes, and suggest fixes.

### Datadog MCP

**Best for**: APM, logs, and metrics

---

## Communication

### Slack MCP

**Best for**: Slack workspace integration

| Recommend When           | Examples           |
| ------------------------ | ------------------ |
| Team uses Slack          | Send notifications |
| Deployment notifications | Alert channels     |
| Incident response        | Post updates       |

### Notion MCP

**Best for**: Notion workspace for documentation

| Recommend When  | Examples             |
| --------------- | -------------------- |
| Notion for docs | Read/update pages    |
| Knowledge base  | Search documentation |
| Meeting notes   | Create summaries     |

---

## Do Not Recommend

Servers that duplicate capability Claude Code already has. Each costs context in every session and buys
nothing:

- **Filesystem MCP** — Read, Write, Edit, Glob, and Grep already cover this.
- **Generic "memory" servers** — recommend only against a concrete, stated cross-session need; "remembers
  project context" is not one.
- **A second server covering an installed server's capability** — name the overlap in the report instead.

---

## Containers & DevOps

### Docker MCP

**Best for**: Container management

| Recommend When      | Examples                |
| ------------------- | ----------------------- |
| Docker Compose file | Container orchestration |
| Dockerfile present  | Build images            |
| Container debugging | Inspect logs, exec      |

### Kubernetes MCP

**Best for**: Kubernetes cluster management

| Recommend When    | Examples           |
| ----------------- | ------------------ |
| K8s manifests     | Deploy, scale pods |
| Helm charts       | Package management |
| Cluster debugging | Pod logs, status   |

---

## AI & ML

### Exa MCP

**Best for**: Web search and research

| Recommend When       | Examples          |
| -------------------- | ----------------- |
| Research tasks       | Find current info |
| Competitive analysis | Market research   |
| Documentation gaps   | Find examples     |

---

## Quick Reference: Detection Patterns

| Look For                                                | Suggests MCP Server                 |
| ------------------------------------------------------- | ----------------------------------- |
| Pinned fast-moving library versions                     | Docs-lookup MCP (self-hosted first) |
| React/Vue/Next.js                                       | Playwright MCP                      |
| `@supabase/supabase-js`                                 | Supabase MCP                        |
| `convex` in deps, `convex/` directory, or `convex.json` | Convex MCP                          |
| `pg` or `postgres`                                      | PostgreSQL MCP                      |
| GitHub remote                                           | GitHub MCP                          |
| `.linear` or Linear refs                                | Linear MCP                          |
| `@aws-sdk/*`                                            | AWS MCP                             |
| `@sentry/*`                                             | Sentry MCP                          |
| `docker-compose.yml`                                    | Docker MCP                          |
| Slack webhook URLs                                      | Slack MCP                           |
