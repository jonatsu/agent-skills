# Skill Sources — channels, query methods, install flows

Volatile facts (star counts, install thresholds, vendor lists, API limits) drift.
**Last verified: 2026-07-27.** Re-check against the linked primary sources before
relying on any specific number.

## Tier 1 — Official / first-party (highest trust)

Official vendor repositories are plain GitHub repos of `SKILL.md` files; any
SKILL.md-compatible agent consumes them by clone/copy. Provenance is the trust
signal — no per-skill scanning needed beyond an L2 content read.

| Source | URL | Notes |
|---|---|---|
| Agent Skills spec | https://agentskills.io (`github.com/agentskills/agentskills`) | Vendor-neutral standard (open, Dec 2025). Canonical format authority. |
| Anthropic | `github.com/anthropics/skills` | Example + document skills. Some document skills are source-available, not OSS. |
| Anthropic curated marketplace | `github.com/anthropics/claude-plugins-official` | Auto-registered in Claude Code; Anthropic curates inclusion. |
| Google | `github.com/google/skills` | Google Cloud + Workspace skills. |
| OpenAI | `github.com/openai/skills` | "Skills Catalog for Codex." |
| Cloudflare | `github.com/cloudflare/skills` | Workers, Pages, R2, D1, Agents SDK, WAF, IaC. |
| Microsoft | `microsoft/azure-skills` (via marketplaces) | Azure storage/compliance/rbac/kusto, etc. |

Query: browse the vendor repo's `skills/` directory, or search GitHub within the
org. Install: clone/copy, or (Claude Code) `/plugin marketplace add <owner/repo>`
then `/plugin install <plugin>@<marketplace>`.

## Tier 2 — Curated / screened

| Source | URL | Query method | Trust signal |
|---|---|---|---|
| officialskills.sh | https://officialskills.sh | Browse the vendor list, then `<vendor>/skills`; no text search API | Verified-vendor-only curation (~651 skills, ~54 vendor orgs) |
| Claude community marketplace | `github.com/anthropics/claude-plugins-community` | `/plugin marketplace add anthropics/claude-plugins-community` | Automated validation + safety screening; pinned to commit SHA. **Claude Code only.** |
| VoltAgent awesome list | `github.com/VoltAgent/awesome-agent-skills` | Browse/README search | Awesome-list PR review; mixes official + community |

Other community awesome-lists (varying rigor): `ComposioHQ/awesome-claude-skills`,
`travisvn/awesome-claude-skills`, `karanb192/awesome-claude-skills`.

## Tier 3 — Popularity-indexed (popularity ≠ safety)

| Source | URL | Query method | Signal |
|---|---|---|---|
| skills.sh | https://skills.sh | `npx skills find <query>`; leaderboard at `/` and `/trending`. No documented public search API. | Install counts (popularity only; mixes vendor + unverified community) |
| skillsmp.com | https://skillsmp.com | REST API at `skillsmp.com/docs/api`; also `/search?q=<query>` | ~2.3M aggregated SKILL.md from GitHub; site states it does **not** certify safety/quality |

Install (skills.sh): `npx skills add <owner/repo@skill> -g -y` (third-party
installer — a supply-chain hop; prefer clone for anything sensitive).

## Tier 4 — Raw GitHub (last resort, no gatekeeping)

```
read https://github.com/topics/agent-skills?q=<query>&o=desc&s=stars
```

Evaluate by stars, last-commit recency, and whether `SKILL.md` exists at the repo
root or under `skills/<name>/`. Full Verification Pipeline required.

## Reading raw SKILL.md for L2

```
# multi-skill repo:
read https://raw.githubusercontent.com/<owner>/<repo>/refs/heads/main/skills/<name>/SKILL.md
# single-skill repo:
read https://raw.githubusercontent.com/<owner>/<repo>/refs/heads/main/SKILL.md
```

## Trusted vendor org handles (exact, case-insensitive match required)

`anthropics`, `google`, `openai`, `cloudflare`, `microsoft`, `getsentry`,
`auth0`, `apollographql`, `huggingface`, `firebase`, `flutter`, `trailofbits`,
`googleworkspace`, `WordPress`. Typo-squats (`microsft`, `anthropic` without the
trailing `s`) are NOT trusted — reject them.
