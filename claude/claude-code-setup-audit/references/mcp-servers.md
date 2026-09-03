# MCP Server Recommendations

MCP servers connect Claude to external tools and services. `SKILL.md` carries the signal-to-server mapping;
this file carries the doctrine that decides whether a mapped server should be recommended at all.

**This file names few servers on purpose.** Most of the mapping is mechanical — a project using a vendor wants
that vendor's server — and a list of vendor names is a snapshot that ages without anyone noticing. What is not
mechanical, and what actually decides the recommendation, is where the queries go, what credential the server
needs, and whether an installed server already covers the ground.

## Where Servers Are Configured

| Scope   | File                               | Reaches                     |
| ------- | ---------------------------------- | --------------------------- |
| Project | `.mcp.json` in the project root    | that directory only         |
| Global  | `.claude.json` in the config dir   | every project for this user |
| Team    | `.mcp.json`, committed to the repo | everyone who clones         |

Recommend the committed `.mcp.json` for anything the whole team needs, so a clone arrives configured.

**The global file is `.claude.json` inside the config directory, which `CLAUDE_CONFIG_DIR` relocates.** It is
not reliably at `~/.claude.json`: verified 2026-09-03 on a machine with `CLAUDE_CONFIG_DIR` set, where
`~/.claude.json` does not exist and the real file sits under the configured directory. Resolve the path from
the environment rather than printing a literal `~/.claude.json` into a report.

Debug a misbehaving server with `claude --debug mcp`. There is no `--mcp-debug` flag; `-d, --debug [filter]`
takes a category filter. Confirmed against `claude --help` on 2.1.239, 2026-09-03.

## Data Flow and Credentials — Decide Before Recommending

Every server is either **self-hosted** (runs on the user's machine or their infrastructure) or **hosted** (a
third party receives the queries).

**MUST state which, for every server recommended, along with the credential it needs.** A recommender that
silently routes a codebase's questions to an external service has made a security decision on the user's
behalf, and the user finds out later.

Prefer a self-hosted equivalent when one exists. Recommend a hosted server only when the capability genuinely
requires the vendor's own service — a hosted issue tracker, error tracker, or cloud provider. "It is quicker
to set up" is not that reason.

Weigh context cost too: every connected server's tool definitions load into every session, so two overlapping
servers cost twice for one capability.

## Deriving a Candidate

Read the candidate off the dependency rather than off a list. A vendor SDK in the manifest implies that
vendor's server; a database driver implies a database server; a hosted service configured in the repo implies
that service's server. Then apply the doctrine above and the exclusions below.

Three signals are worth naming because they are not obvious from a dependency alone:

- **Convex** is detectable from `convex` in dependencies, a `convex/` directory, or `convex.json` at the repo
  root, and its server introspects a live deployment — tables, function specs, environment variables, logs.
  Run with `npx convex mcp start`.
- **Pinned fast-moving libraries** are the signal for a documentation server, not any single dependency. The
  problem it solves is Claude recalling an API instead of reading it.
- **A frontend framework plus any end-to-end testing need** is the signal for browser automation. A frontend
  framework alone is not — the server is only worth its context when something actually drives a browser.

## Documentation Servers: Self-Hosted First

A local documentation indexer indexes the exact versions the project pins, and no query leaves the machine.
That is the default recommendation whenever the project has a documentation-recall problem.

Hosted alternatives are quicker to configure at the cost of sending every documentation query to a vendor plus
an API key. When recommending one, MUST say so explicitly, and MUST verify its current endpoint and auth
requirements against the vendor's own documentation before printing an install command — those change more
often than anything else in this file.

## Do Not Recommend

Servers that duplicate capability Claude Code already has. Each costs context in every session and buys
nothing:

- **Filesystem servers** — Read, Write, Edit, Glob, and Grep already cover this.
- **Generic "memory" servers** — recommend only against a concrete, stated cross-session need. "Remembers
  project context" is not one.
- **A second server covering an installed server's capability** — name the overlap in the report instead, as
  a finding rather than a recommendation.
- **A server for a service the repository does not actually use.** A vendor name in a comment or a lockfile
  transitive is not adoption.

## Verify Before Printing an Install Command

Install syntax is per-server and the transport form is required — a bare `claude mcp add <name>` is not
runnable. Confirm the exact invocation against `claude mcp add --help` and the server's own documentation
before it reaches the report, and never reconstruct one from memory.
