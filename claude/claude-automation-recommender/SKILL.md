---
name: claude-automation-recommender
description: Analyze a codebase and recommend Claude Code automations (hooks, subagents, skills, plugins, MCP servers). Use when user asks for automation recommendations, wants to optimize or audit their Claude Code setup, mentions improving Claude Code workflows, asks how to first set up Claude Code for a project, asks what hooks or MCP servers this project should have, or wants to know what Claude Code features they should use. Read-only and report-only — for actually writing a hook, skill, agent, or settings change, use the relevant authoring skill instead.
allowed-tools: Read, Glob, Grep, Bash, WebSearch, WebFetch
metadata:
  author: Joonas Onatsu
  license: Apache-2.0
---

# Claude Automation Recommender

IRON LAW: Inventory the existing configuration before recommending anything.
NEVER recommend an automation the setup already has, and NEVER pad a category to
hit a quota — "already covered" is a valid, useful answer.

**This skill is read-only.** It analyzes and reports. It MUST NOT create or
modify files, install MCP servers, or install plugins. The user implements the
recommendations, or asks separately for help building them.

**Every command in the report MUST be runnable as printed.** Verify a command's
syntax with `--help` before emitting it. NEVER invent a flag, subcommand, or
service endpoint.

## Workflow

Copy this checklist and check items off:

```text
Automation Recommender Progress:
- [ ] Phase 0: Inventory the existing setup ⛔ BLOCKING
- [ ] Phase 1: Analyze the codebase ⚠️ REQUIRED
- [ ] Phase 2: Match signals to automations (subtract what Phase 0 found)
- [ ] Phase 3: Write the report
- [ ] Pre-delivery checklist
```

## Automation Types Overview

| Type | Best For |
|------|----------|
| **Hooks** | Automatic actions on tool events (format on save, lint, block edits) |
| **Subagents** | Specialized reviewers/analyzers that run in parallel |
| **Skills** | Packaged expertise, workflows, and repeatable tasks (invoked by Claude or user via `/skill-name`) |
| **Plugins** | Installable bundles of skills, commands, agents, and hooks |
| **MCP Servers** | External tool integrations (databases, APIs, browsers, docs) |

### Phase 0: Inventory the Existing Setup ⛔ BLOCKING

MUST run before Phase 1. Recommending what is already installed is the single
most common failure of this skill.

```bash
# Project-level config
ls -la .claude/ .mcp.json CLAUDE.md AGENTS.md 2>/dev/null
cat .claude/settings.json .claude/settings.local.json 2>/dev/null
ls .claude/skills/ .claude/agents/ .claude/commands/ 2>/dev/null

# User-level config (CLAUDE_CONFIG_DIR overrides ~/.claude)
CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
cat "$CFG/settings.json" 2>/dev/null
ls "$CFG/skills/" "$CFG/agents/" 2>/dev/null

# Live runtime state — MUST NOT be silenced; a failure here is a finding
command -v claude >/dev/null && claude mcp list || echo "INVENTORY GAP: claude CLI unavailable"
command -v claude >/dev/null && claude plugin list || echo "INVENTORY GAP: claude CLI unavailable"
```

**A failed inventory is not an empty inventory.** If any probe above could not
run — no `claude` on PATH, an unreadable settings file, a sandbox that blocks
the command — MUST say so in the report and MUST mark the affected categories
as unverified. NEVER treat "the command produced no output" as "nothing is
configured": that is exactly how the Iron Law gets violated silently.

Record, per category, what already exists. Then apply these rules in Phase 2:

- MUST omit any automation already configured, at either scope.
- MUST NOT recommend an MCP server whose capability an installed server already
  covers — name the overlap instead.
- When a category is fully covered, say so in one line and recommend nothing for
  it. This is a result, not a gap in the analysis.
- MAY recommend an improvement to an *existing* automation (a hook that is too
  broad, an agent with excess tool access) — mark it clearly as a change, not an
  addition.

### Phase 1: Analyze the Codebase ⚠️ REQUIRED

Gather evidence for every recommendation. NEVER recommend a toolchain hook
without a config file or dependency proving that toolchain is in use.

```bash
# Project type and toolchain manifests
ls -la package.json pyproject.toml Cargo.toml go.mod pom.xml build.gradle \
       Gemfile composer.json mix.exs 2>/dev/null

# Formatter / linter / type-checker config (drives hook recommendations)
ls -la .prettierrc* prettier.config.* .eslintrc* eslint.config.* \
       ruff.toml .ruff.toml mypy.ini pyrightconfig.json tsconfig.json \
       .rustfmt.toml rustfmt.toml .golangci.yml .pre-commit-config.yaml 2>/dev/null

# Dependencies (language-appropriate — do not assume JS)
grep -E '"(react|vue|angular|next|express|fastapi|django|prisma|supabase|convex|stripe)"' package.json 2>/dev/null
grep -iE '^(django|fastapi|flask|sqlalchemy|pydantic|boto3)' requirements.txt pyproject.toml 2>/dev/null
grep -E '^(name|\[dependencies\])' Cargo.toml 2>/dev/null

# Tests, CI, containers
ls -la tests/ test/ __tests__/ .github/workflows/ Dockerfile docker-compose.yml 2>/dev/null

# Structure and scale (scale drives subagent recommendations)
git ls-files 2>/dev/null | wc -l
ls -la src/ app/ lib/ components/ pages/ api/ 2>/dev/null
```

**Key Indicators to Capture:**

| Category | What to Look For | Informs Recommendations For |
|----------|------------------|----------------------------|
| Language/Framework | Manifest files, import patterns | Hooks, MCP servers |
| Formatter/linter | `.prettierrc`, `ruff.toml`, `.pre-commit-config.yaml` | Formatting and lint hooks |
| Frontend stack | React, Vue, Angular, Next.js | Playwright MCP, frontend skills |
| Backend stack | Express, FastAPI, Django | API documentation tools |
| Database | Prisma, Supabase, Convex, raw SQL | Database / backend MCP servers |
| External APIs | Stripe, OpenAI, AWS SDKs | Docs-lookup MCP |
| Testing | Jest, pytest, Playwright configs | Testing hooks, subagents |
| CI/CD | GitHub Actions, GitLab CI | GitHub MCP server |
| Issue tracking | Linear, Jira references | Issue tracker MCP |
| Docs patterns | OpenAPI, JSDoc, docstrings | Documentation skills |

**When a pre-commit framework is already configured** (`.pre-commit-config.yaml`,
Husky, lefthook), formatting and lint hooks are largely redundant — the checks
already run at commit time. Say so instead of recommending a duplicate.

### Phase 2: Match Signals to Automations

Generate candidates per category, then subtract everything Phase 0 found.
Surface the top 1-2 survivors per category; if the user asked about one
category, give 3-5 there and skip the rest.

Reference files load on demand — read only the ones a category actually needs.

#### A. MCP Servers

See [references/mcp-servers.md](references/mcp-servers.md).

| Codebase Signal | Recommended MCP Server |
|-----------------|------------------------|
| Frontend with UI testing needs | **Playwright** — browser automation/testing |
| Uses Supabase | **Supabase MCP** — direct database operations |
| Uses Convex | **Convex MCP** — deployment introspection, queries/mutations, env vars, logs |
| PostgreSQL/MySQL database | **Database MCP** — query and schema tools |
| GitHub repository | **GitHub MCP** — issues, PRs, actions |
| Uses Linear for issues | **Linear MCP** — issue management |
| AWS infrastructure | **AWS MCP** — cloud resource management |
| Sentry error tracking | **Sentry MCP** — error investigation |
| Docker containers | **Docker MCP** — container management |
| Heavy use of fast-moving libraries | **Docs-lookup MCP** — see the reference for self-hosted vs hosted |

MUST flag, for every hosted MCP server recommended: it receives your queries,
and it needs credentials. State both in the report. Prefer a self-hosted
equivalent when one exists.

#### B. Skills

See [references/skills-reference.md](references/skills-reference.md).

Create skills in `.claude/skills/<name>/SKILL.md`.

| Codebase Signal | Skill to Create | Invocation |
|-----------------|-----------------|------------|
| API routes | **api-doc** (with OpenAPI template) | Both |
| Database project | **create-migration** (with validation script) | User-only |
| Test suite | **gen-test** (with example tests) | User-only |
| Component library | **new-component** (with templates) | User-only |
| PR workflow | **pr-check** (with checklist) | User-only |
| Releases | **release-notes** (with git context) | User-only |
| Code style | **project-conventions** | Claude-only |
| Onboarding | **setup-dev** (with prereq script) | User-only |

#### C. Hooks

See [references/hooks-patterns.md](references/hooks-patterns.md) for runnable
configurations, the stdin/exit-code contract, and per-hook latency costs.

| Codebase Signal | Recommended Hook | Cost |
|-----------------|------------------|------|
| Prettier configured | PostToolUse: format the edited file | Low |
| ESLint/Ruff configured | PostToolUse: lint the edited file | Low |
| TypeScript project | PostToolUse: `tsc --noEmit` | **High on large repos** |
| Tests directory exists | PostToolUse: run the related test file | **Medium-high** |
| `.env` files present | PreToolUse: block `.env` edits | None |
| Lock files present | PreToolUse: block lock file edits | None |
| Security-sensitive code | PreToolUse: require confirmation | None |

MUST state the cost when recommending a whole-project check (type-check, full
test run) and MUST scope the command to the edited file where the toolchain
supports it.

#### D. Subagents

See [references/subagent-templates.md](references/subagent-templates.md).

| Codebase Signal | Recommended Subagent |
|-----------------|---------------------|
| Large codebase (>500 files) | **code-reviewer** — parallel code review |
| Auth/payments code | **security-reviewer** — security audits |
| API project | **api-documenter** — OpenAPI generation |
| Performance critical | **performance-analyzer** — bottleneck detection |
| Frontend heavy | **ui-reviewer** — accessibility review |
| Needs more tests | **test-writer** — test generation |

#### E. Plugins

See [references/plugins-reference.md](references/plugins-reference.md) for the
install contract — a marketplace MUST be added before any plugin installs, and
ids take the form `plugin@marketplace`.

| Codebase Signal | Recommended Plugin |
|-----------------|-------------------|
| Building plugins or skills | **plugin-dev** |
| PR-based workflow | **pr-review-toolkit** |
| Frontend development | **frontend-design** |
| Wants hooks written from conversation | **hookify** |

### Phase 3: Output Recommendations Report

Use this structure. Fill every bracket with codebase-specific evidence; a
recommendation with a generic reason is a failed recommendation. Skip categories
with no surviving candidate, and list fully-covered categories under
"Already covered".

> ## Claude Code Automation Recommendations
>
> ### Codebase Profile
> - **Type**: [detected language/runtime]
> - **Framework**: [detected framework]
> - **Key Libraries**: [relevant libraries detected]
>
> ### Already Covered
> [Category — what is already configured, at which scope. One line each.]
>
> ### 🔌 MCP Servers
>
> #### [server name]
> **Why**: [specific reason, citing the detected dependency]
> **Install**: [verified command]
> **Data flow**: [self-hosted, or: hosted — queries leave the machine; needs an API key]
>
> ### 🎯 Skills
>
> #### [skill name]
> **Why**: [specific reason]
> **Create**: `.claude/skills/[name]/SKILL.md`
> **Invocation**: User-only / Both / Claude-only
> **Frontmatter**: `name`, `description`, plus `disable-model-invocation: true` for user-only
>
> ### ⚡ Hooks
>
> #### [hook name]
> **Why**: [specific reason, citing the detected config file]
> **Where**: `.claude/settings.json`
> **Cost**: [per-edit latency]
> **Config**: [runnable JSON from references/hooks-patterns.md]
>
> ### 🤖 Subagents
>
> #### [agent name]
> **Why**: [specific reason based on codebase patterns]
> **Where**: `.claude/agents/[name].md`
>
> **Want more?** Ask for additional recommendations in any category.
> **Want help implementing these?** Ask and I can set any of them up.

Note that hook and MCP changes need a Claude Code restart to take effect.

## Decision Framework

**MCP servers** — external service integration, docs lookup, browser
automation, team tooling, cloud infrastructure. Weigh the cost: every server
adds tool definitions to the context of every session.

**Skills** — repeated prompts, project-specific tasks with arguments, templates
or scripts bundled with a workflow, quick actions via `/skill-name`, workflows
that should run isolated (`context: fork`).

Invocation control:
- `disable-model-invocation: true` — user-only (side effects: deploy, commit, send)
- `user-invocable: false` — Claude-only (background knowledge)
- omit both — either can invoke

**Hooks** — deterministic post-edit actions, protection rules, validation. Best
when the check is fast and scoped to the changed file.

**Subagents** — specialized expertise, parallel review, background quality
checks.

**Plugins** — several related capabilities at once, team standardization,
first-time setup.

## Anti-Patterns

- **Recommending what is already installed.** The Phase 0 output exists to be
  subtracted. NEVER skip Phase 0 because the project looks small.
- **Filling the quota.** "1-2 per category" is a ceiling, not a target.
- **Unscoped hook commands.** `prettier --write .` on every edit reformats the
  whole repository. Pass the edited file.
- **Recommending a toolchain the repo does not use.** No `ruff.toml`, no Ruff
  hook — regardless of what the reference tables list.
- **Emitting an unverified command.** Every install line MUST come from
  `--help` output or a reference file in this skill.
- **Silent third-party data flow.** NEVER recommend a hosted MCP server without
  stating that queries leave the machine and credentials are required.
- **Generic justification.** "Improves productivity" is not a reason. Cite the
  file or dependency that triggered the recommendation.

## Pre-Delivery Checklist

- [ ] Phase 0 ran, and its findings appear in the report (as omissions or an
      "Already covered" section)
- [ ] Every recommendation names the file or dependency that triggered it
- [ ] Every command was verified against `--help` or a reference file
- [ ] Every hook config is complete, scoped to the edited file, and carries a
      cost note
- [ ] Every hosted MCP server carries a data-flow and credentials note
- [ ] No category padded past its surviving candidates
- [ ] Any inventory gap from Phase 0 is stated, with the affected categories
      marked unverified
- [ ] No file was created or modified by this skill
