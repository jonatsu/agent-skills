# OpenCode Integration Reference

Loaded when the client under test is OpenCode. Covers OpenCode-specific env
vars, `headroom wrap opencode` behavior, plugin auth layers, and isolation
escalation.

## Env vars to check for OpenCode isolation

Before launching an OpenCode probe, inspect and override these:

- `OPENCODE_HOME` — OpenCode config home
- `OPENCODE_CONFIG` — explicit config file path
- `OPENCODE_CONFIG_CONTENT` — inline config content injection (used by wrap)
- `OPENAI_BASE_URL` — OpenAI provider base URL
- `ANTHROPIC_BASE_URL` — Anthropic provider base URL
- `HEADROOM_CONTEXT_TOOL` — context tool selector
- `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_CACHE_HOME`, `XDG_STATE_HOME`
- relevant `HEADROOM_*`, `RTK_*`, `LEAN_CTX_*`

Setting only `OPENCODE_HOME` is NOT sufficient. Config can still leak into
`~/.config/opencode` via XDG defaults or `OPENCODE_CONFIG_CONTENT`.

## Escalation: temp HOME subshell

If config still leaks after overriding the above, use a temp `HOME` inside a
subshell for the probe only:

```bash
(
  export HOME=$(mktemp -d)
  export XDG_CONFIG_HOME="$HOME/.config"
  export XDG_DATA_HOME="$HOME/.local/share"
  export XDG_CACHE_HOME="$HOME/.cache"
  export XDG_STATE_HOME="$HOME/.local/state"
  opencode ...
)
```

## `headroom wrap opencode` known pitfalls

`headroom wrap opencode` is documented as injecting `OPENCODE_CONFIG_CONTENT`
and provider base URLs. In practice it may mutate or interfere with OpenCode
config instead of reliably routing traffic.

Symptoms observed in prior investigations:

- `OPENAI_BASE_URL` / `ANTHROPIC_BASE_URL` set by wrap but traffic still
  bypassed the proxy
- `OPENCODE_CONFIG_CONTENT` injected but provider config not honored
- proxy log showed only `/health`, `/readyz`, `/livez`, `/stats` — never model
  calls
- `POST /responses` → `302` → `GET /` redirect loop

Preferred alternative: direct env-based routing without wrap:

```bash
OPENAI_BASE_URL=http://127.0.0.1:8787/v1 opencode ...
```

If you must use wrap, treat it as a test subject, not an unquestioned baseline.

## Plugin auth layers

OpenCode plugins can intercept and rewrite provider auth/routing. Known
pitfalls:

- `oc-codex-multi-auth` — hijacked the `openai` provider, targeted
  `https://chatgpt.com/backend-api` instead of configured baseURL. Removed
  from active config.
- `@cortexkit/opencode-openai-auth` (CortexKit) — registers the built-in
  `openai` provider id, supersedes internal OpenAI auth, rewrites outbound
  OpenAI requests into Codex request shape, defaults
  `codexApiEndpoint` to `https://chatgpt.com/backend-api/codex/responses`.
  Treat as an auth/routing layer, not transparent.

Native OpenCode OpenAI OAuth works via:

```bash
bunx opencode-ai@latest auth login --pure -p openai
```

Before debugging routing, verify no auth-rewriting plugin is intercepting
the provider.

## Relevant upstream issues

- `#1679` — with OpenCode Go CLI `v1.16.2`, `headroom wrap opencode` could
  appear to load while traffic bypassed the proxy. Attributed to Go-CLI/plugin
  limitations around `OPENCODE_CONFIG_CONTENT`, plugin option tuples, and
  non-standard plugin hooks. Also reported `OPENAI_BASE_URL` not honored by
  the `opencode-go` provider. Treat as version/provider-specific; test before
  assuming it applies.
- `#1151` — stale proxy persistence. Closed but useful as symptom match.

Do NOT treat closed issues as irrelevant. Use them as prior-art hints.
