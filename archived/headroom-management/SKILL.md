---
name: headroom-management
description: >-
  Headroom proxy setup, deployment, service management, backend selection,
  and troubleshooting. Use for headroom install, persistent service vs
  ephemeral wrap, proxy routing, stale proxy cleanup, port contention,
  perf/savings/metrics debugging, backend translation vs passthrough,
  context-tool integration, llms.txt doc checks, temp-dir probe isolation,
  or service-vs-ephemeral testing. Triggers: headroom, headroom proxy,
  headroom wrap, headroom service, headroom install, headroom backend,
  headroom savings, headroom perf, stale proxy, port contention, proxy
  routing broken, headroom troubleshooting, headroom health check.
---

# Headroom Management

IRON LAW: NEVER debug Headroom against live user config or a live install first. Start from the documented healthy-case baseline, then run isolated probes in temp directories with explicit env overrides.

Red Flags (return to Step 1 if any appear):

- "I think the problem might be..." (guessing, not analyzing)
- Making config changes before confirming the documented baseline
- Probe output looks correct but you cannot explain the routing path
- Zero metrics but you have not verified whether traffic reached the proxy at all

## Workflow Checklist

Copy this checklist and check off items as you complete them:

- [ ] Step 1: Establish Healthy Baseline ⛔ BLOCKING
- [ ] Step 2: Load local context ⛔ BLOCKING
- [ ] Step 3: Isolate every probe run ⚠️ REQUIRED
- [ ] Step 4: Choose simplest context-tool path
- [ ] Step 5: Choose service-first vs ephemeral testing
- [ ] Step 6: Guard against stale proxies and port contention ⚠️ REQUIRED
- [ ] Step 7: Debug in layers, not all at once
- [ ] Step 8: Check upstream issues
- [ ] Step 9: Delegation constraints (conditional)
- [ ] Step 10: Confirm before applying any fix ⚠️ REQUIRED
- [ ] Step 11: Output contract ⚠️ REQUIRED

## Detailed Steps

### 1. Establish the documented healthy case first ⛔ BLOCKING

Before debugging, MUST create a short **Healthy Baseline** section separate from all bug analysis. MUST NOT proceed to Step 3 until this is complete.

Healthy Baseline MUST start from Headroom upstream `llms.txt`:

- `https://raw.githubusercontent.com/headroomlabs-ai/headroom/refs/heads/main/llms.txt`

From `llms.txt`, MUST fetch the current docs that cover:

- install/service workflow
- proxy / OpenAI-compatible base URL usage
- `headroom wrap` subcommands for any supported client
- context-tool setup (`rtk`, `lean-ctx`, or current replacement)
- perf / savings / metrics expectations

Healthy Baseline MUST answer these questions **before** any debugging steps:

1. In a healthy setup, is the user expected to use a persistent Headroom service, ephemeral wrap, or both?
2. For OpenAI-compatible clients, what base URL/path is documented?
3. What does the relevant `headroom wrap <client>` subcommand claim to inject or modify?
4. What metrics should appear when the setup is working?
5. Which context tool is the default documented path?

Do NOT mix Healthy Baseline bullets with failure analysis. Keep them in their own section.

### 2. Load local context before re-testing ⛔ BLOCKING

Before repeating probes, MUST check local context sources. MUST NOT proceed to Step 3 until prior findings are loaded.

- Search project memories via `ctx_search(query="headroom ...")` for prior findings, constraints, and architecture notes.
- If a preserved investigation bundle exists under `docs/investigations/` or similar, consult its key artifacts (results, probes, patches) rather than re-deriving.

Do NOT hard-code memory IDs or investigation paths into your reasoning — they drift. Re-search each time.

Ask: Has this exact symptom been investigated before? If yes, what was the proven root cause?

### 3. Isolate every probe run ⚠️ REQUIRED

MUST use temp directories for any Headroom or client probe.

Minimum rule:

- setting only one env var (e.g., `OPENCODE_HOME`, `XDG_CONFIG_HOME`, or equivalent) is NOT sufficient isolation

Before launching a probe, MUST inspect related shell env vars and override the ones that would leak into live state.

Generic env var categories to check:

- client config home / config file / config content injection
- provider base URLs (`OPENAI_BASE_URL`, `ANTHROPIC_BASE_URL`, or equivalent)
- Headroom context tool selector and related `HEADROOM_*`
- context-tool-specific vars (`RTK_*`, `LEAN_CTX_*`, or equivalent)
- XDG dirs (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_CACHE_HOME`, `XDG_STATE_HOME`)

For client-specific env var lists and isolation escalation, load `references/opencode-integration.md` if the client is OpenCode.

Probe rules:

- MUST record the exact env overrides used
- MUST keep probe output/log paths under the temp root
- MUST preserve the user's original env/config outside the probe
- MUST prefer virtual/ephemeral tooling over modifying the live installation

If config still leaks into the live config directory, escalate isolation:

- use a temp root for all XDG dirs
- if necessary, use a temp `HOME` inside a subshell for the probe only

### 4. Choose simplest context-tool path

SHOULD test the default documented context tool before reproducing advanced variants.

- inspect env/config that selects the context tool before assuming the wrapper changed it
- if `rtk` is the documented/default path, start there to reduce variables
- use `lean-ctx` only when reproducing lean-ctx-specific behavior or metrics discrepancies

Ask: Are metrics collected proxy-side, wrap-side, or both? If wrap-side, does zero savings mean zero traffic or zero instrumentation?

Important note:

- RTK metrics are collected wrap-side (in `headroom/cli/wrap_rtk_metrics.py`), not proxy-side
- if metrics visibility differs between `rtk` and `lean-ctx`, compare instrumentation paths instead of assuming routing is broken in the same way

### 5. Choose service-first vs ephemeral testing

SHOULD prefer the persistent Headroom service if it is already set up and healthy.

Service-first flow:

1. Check whether a user service/profile already exists.
2. Verify health/status before running client probes.
3. Reuse the healthy service instead of layering an extra ephemeral proxy unless the bug is specifically about wrap behavior.

Ephemeral fallback (conditional):

- if no healthy persistent service exists, use `headroom wrap <client> ...` or equivalent ephemeral testing
- treat wrap behavior as its own test subject, not as an unquestioned baseline

Local caution:

- if prior investigation showed `headroom wrap <client>` may mutate/interfere with client config in this environment, wrap probes MUST be isolated and reversible
- for OpenCode-specific wrap pitfalls, load `references/opencode-integration.md`

Upstream prior art:

- check GitHub issues for reports that `headroom wrap <client>` appeared to load while traffic bypassed the proxy
- treat these as **version/client-specific hypotheses to test**, not as universal truth

### 6. Guard against stale proxies and port contention ⚠️ REQUIRED

MUST check for stale proxy processes before and after failed tests.

Do this especially when:

- `headroom wrap <client>` fails mid-launch
- the probe exits unexpectedly
- the target port remains bound
- traffic/health results look inconsistent between runs

Handle stale proxy cleanup carefully:

- first determine whether the listener is the persistent service or a stray ephemeral proxy
- if it is the persistent service you intentionally reused, keep it unless the test requires restarting it
- if it is a stray wrap-spawned proxy, shut down only that stale process before retrying
- re-check the port after cleanup to avoid false negatives from contention

MAY use closed GitHub issues as symptom/reference matches, not just open ones.

### 7. Debug in layers, not all at once

Use this order:

1. **Docs vs reality** — compare the Healthy Baseline to current behavior.
2. **Environment isolation** — verify the probe did not touch live client state.
3. **Service/proxy state** — verify health, bound ports, and stale-process status.
4. **Client request path** — determine whether the client reaches Headroom at all.
5. **Headroom forwarding path** — inspect whether requests succeed, redirect, or die before counting.
6. **Metrics path** — only after confirming traffic behavior, compare perf/savings/CLI-filtering visibility.

Ask at each layer: Is the failure at this layer, or did it pass through to the next? Only move to the next layer after confirming the current one.

### 8. Check upstream issues

SHOULD inspect both open and closed Headroom GitHub issues for:

- stale proxy persistence
- `wrap <client>` config mutation
- temp-dir / env isolation gaps
- OpenAI-compatible `/v1` path quirks
- context-tool metrics visibility

Do NOT treat closed issues as irrelevant. Use them as prior-art hints.

### 9. Delegation constraints (conditional)

Only if delegating research to subagents.

MUST direct agents to use locally-available models/fallbacks only. Reason: the primary provider may be rate-limited during the investigation.

Delegation prompts MUST state:

- do not assume primary provider availability
- use current locally-configured fallbacks
- do not change live config/install

### 10. Confirm before applying any fix ⚠️ REQUIRED

Present findings to the user. Ask:

- Proceed with the recommended fix?
- Apply only isolated probe-level changes?
- View only, no changes to live config?

⚠️ NEVER proceed without explicit user confirmation. NEVER apply fixes to live config/install as the primary path — fixes MUST be validated in isolation first.

### 11. Output contract ⚠️ REQUIRED

Return results in this order:

1. **Healthy Baseline** — what docs say should happen
2. **Local Known Facts** — reused memories/artifacts
3. **Probe Setup** — temp dirs, env overrides, service/ephemeral choice
4. **Observed Behavior** — only current-run evidence
5. **Deltas from Healthy Case** — exact mismatch list
6. **Next Minimal Probe** — one small next step

## Backend Selection (reference)

`--backend <X>` selects a **translation backend for `/v1/messages` (Anthropic-shaped) only**. It does NOT rewrite upstream URLs.

### What each backend does

| Backend                                               | `/v1/messages` (Anthropic-shaped)                                                                            | `/v1/chat/completions` + `/v1/responses` (OpenAI-shaped)               | Env vars read        |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- | -------------------- |
| `anthropic` (default)                                 | passthrough to `api.anthropic.com`, client auth verbatim                                                     | passthrough to `api.openai.com`, client auth verbatim                  | none server-side     |
| `openrouter`                                          | LiteLLM translates Anthropic→OpenAI, strips inbound auth, calls OpenRouter with `Bearer $OPENROUTER_API_KEY` | passthrough to `api.openai.com`, client auth verbatim (NOT OpenRouter) | `OPENROUTER_API_KEY` |
| `bedrock` / `azure` / `anyllm` / `litellm-<provider>` | translation via respective backend                                                                           | passthrough to `api.openai.com`                                        | backend-specific     |

### Key facts

- `resolve_api_targets` never reads `config.backend` → upstream URLs stay `api.anthropic.com` / `api.openai.com` regardless of backend.
- `create_proxy_backend` returns exactly one backend per process → single instance = single backend.
- Only the Anthropic handler dispatches to `self.anthropic_backend`. OpenAI handler has no backend switch.
- LiteLLM backend strips inbound `Authorization`/`x-api-key` and uses env-sourced key.
- Model names for `--backend openrouter` MUST be provider-prefixed (`openai/gpt-4o`, `anthropic/claude-3.5-sonnet`). Bare names get `openrouter/` prepended and likely 404.
- Multi-upstream routing by model prefix is open feature #1279 (PR #1280 draft, not merged as of v0.30.0).

### Decision rule: single vs two instances

- **OpenAI subscription only, or OpenAI + Anthropic** → single default-backend instance. Client providers point `baseURL` at the proxy. Client auth forwarded verbatim.
- **OpenRouter only** → single `--backend openrouter` instance. Client must send Anthropic-format `/v1/messages` with provider-prefixed model names. `OPENROUTER_API_KEY` required in proxy env.
- **OpenAI subscription + OpenRouter, both compressed** → two instances on different ports (default backend for OpenAI passthrough, `--backend openrouter` for OpenRouter translation). Use distinct `HEADROOM_SAVINGS_PATH` to avoid ledger races. Caveat: clients speaking `/v1/chat/completions` to the openrouter backend get passthrough, not translation — either reconfigure to Anthropic-format, or use `OPENAI_TARGET_API_URL=https://openrouter.ai/api` passthrough on a dedicated instance (bypasses LiteLLM translation, compression still applies).
- **OpenAI subscription + OpenRouter, OpenRouter direct (not compressed)** → single default-backend instance. OpenRouter provider stays pointed at `https://openrouter.ai/api/v1` directly. Simplest correct setup.

### Verification commands

```bash
# Check backend + upstream
curl -s http://127.0.0.1:8787/health | jq '{backend: .config.backend, upstream: .checks.upstream.url}'

# Check routing table (printed at startup)
cat ~/.headroom/deploy/default/runner.log | grep -A10 "^Routing:"

# Confirm passthrough behavior: send OpenAI-shaped request, observe it hits api.openai.com
# Confirm translation behavior: send Anthropic-shaped /v1/messages, observe OPENROUTER_API_KEY used upstream
```

## Anti-patterns

- NEVER start by editing live client config or live Headroom install files.
- NEVER trust a single env var as proof of isolation.
- NEVER mix healthy-case documentation with bug symptoms.
- NEVER retry the same probe without checking for stale proxy state.
- NEVER assume a loaded plugin means the client is honoring its hooks.
- NEVER assume zero `headroom savings` means zero traffic; compare proxy, perf, and wrap-side metrics paths.
- NEVER switch context tools and proxy mode in the same probe unless the goal is interaction testing.
- NEVER use a wrapped probe result as baseline truth when wrap itself is under suspicion.
- NEVER apply a fix to live config without user confirmation and isolated validation first.

## Pre-delivery checklist

- [ ] Healthy Baseline sourced from upstream `llms.txt`
- [ ] Healthy Baseline kept separate from debugging findings
- [ ] Project memories (`ctx_search "headroom"`) + any preserved investigation bundle consulted
- [ ] Probe used temp dirs and explicit env overrides
- [ ] Client-specific isolation vars checked (load `references/opencode-integration.md` if OpenCode)
- [ ] Service-vs-ephemeral choice stated explicitly
- [ ] Stale proxy / port contention checked
- [ ] Upstream issues searched, open and closed
- [ ] No live config/install changes used as the primary path
- [ ] Delegated agents constrained to locally-available models/fallbacks
- [ ] Backend selection matches traffic shape (default for OpenAI passthrough; `--backend openrouter` only translates `/v1/messages`)
- [ ] User confirmed before any fix applied to live config
