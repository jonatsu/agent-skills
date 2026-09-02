# Security Tools — what is real, and how to use it

**Last verified: 2026-07-27** against primary sources. Verdicts below reflect
what each tool actually does — several marketplace badges claim more than they
deliver for markdown-only skills.

## The core problem

A skill is markdown (an instruction/prompt-injection surface) plus optional
bundled scripts (an executable/supply-chain surface). These need different
checks, and **no single scanner is authoritative** — ML injection detectors have
false negatives, and dependency scanners do not apply to markdown. Reliability
comes from layering reproducible checks and weighting provenance, not from
trusting one badge. `scripts/verify_skill.sh` is the reproducible local core (L1).

## Verified tools

| Tool | Status | What it actually does | Invocation |
|---|---|---|---|
| **Snyk agent-scan** | CONFIRMED | `github.com/snyk/agent-scan`, PyPI `snyk-agent-scan`. Scans skills + MCP across many agents. Issue codes `E004` prompt injection, `E005` suspicious URL, `E006` malicious code are real but **experimental** (may change). Requires `SNYK_TOKEN`; **uploads content to Snyk's API**. | `uvx snyk-agent-scan@latest --skills <dir>` |
| **skill-audit** | CONFIRMED (small) | `github.com/pors/skill-audit`, MIT, ~59★, single maintainer. Local: prompt-injection/jailbreak patterns, secrets (trufflehog/gitleaks), shellcheck, semgrep, SARIF output. Candid about limits (no obfuscated/novel/runtime detection). | `skill-audit audit <dir>` |
| **Socket** | CONFIRMED (narrow) | General dependency/supply-chain scanner (`socket scan create`). Its skill-specific scanning runs **server-side** via the skills.sh integration; no verified standalone `socket scan <skill>` CLI for SKILL.md. Meaningless for markdown-only skills. | `socket scan create` (deps only) |
| **Gen Sage** | CONFIRMED (runtime) | `github.com/gendigitalinc/sage`, Apache-2.0. **Runtime** interceptor that hooks tool calls and blocks dangerous commands/URLs/credential leaks live. This is L4, not a pre-install scan. | installs as an agent plugin |

## Misapplied / do-not-trust

- **Gen "Skill Scanner" / Agent Trust Hub** — its pre-install lookup API is
  scoped to **ClawHub** (the OpenClaw ecosystem), NOT Claude/OpenCode skills.
  Do NOT cite it as a scanner for skills found here.
- **Marketplace security badges** — a verdict read off a marketplace page covers
  only skills on that one marketplace and is not reproducible. Treat as weak
  corroboration, never as the gate.
- **Dependency-scanner "0 alerts" on a markdown-only skill** — means the scanner
  did not run, not that the skill is safe.

## How verify_skill.sh maps to the layers

| Check | Layer | Blocker vs warn |
|---|---|---|
| Hidden / bidi Unicode | L1 | BLOCK |
| Secrets (betterleaks/gitleaks/trufflehog) | L1 | BLOCK |
| `curl\|bash` / `base64\|sh` remote exec | L1 | BLOCK |
| Credential paths near network commands | L1 | WARN (review) |
| shellcheck / semgrep on bundled scripts | L1 | WARN (review) |
| Reading the SKILL.md instructions yourself | L2 | agent judgment |

Install any of the optional scanners (`betterleaks`, `gitleaks`, `trufflehog`,
`shellcheck`, `semgrep`) to strengthen L1. The script probes `PATH` and nothing
else: one secrets scanner is enough, and when none is present the check degrades
to a reported skip rather than an error. NEVER read a skip as a pass — it means
the check did not run.
