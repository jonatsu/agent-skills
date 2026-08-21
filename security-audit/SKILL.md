---
name: security-audit
description: Read-only, report-only security review of pending changes or a codebase area — vulnerability detection, OWASP Top 10 and STRIDE threat modeling, secure-coding review. Use for security review, threat analysis, or hardening recommendations, especially when a change touches authentication, authorization, secrets, user input, file uploads, API endpoints, payments, third-party integrations, deserialization, or agent/tool-use surfaces. Prefer this over the built-in security-review skill when a hard "never edit, never silently fix" guarantee matters — this skill only reports and hands off, it never patches code itself.
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Security Audit

IRON RULE: this is a report-only review. Never edit, patch, or apply a fix
as part of running it — not even a one-line, "obviously safe" fix. Findings
and recommendations only. If asked to also fix what's found, stop and get
explicit confirmation on which findings to fix before touching any file.
Never make a change first and mention it afterward.

## Method

Start from trust boundaries — every place untrusted data enters the system
(user input, external APIs, file uploads, fetched web/doc content, IPC,
subprocess output, MCP tool results) — and reason through STRIDE for each
boundary before enumerating findings:

- **S**poofing — is the identity of the caller/data source verified?
- **T**ampering — can the data or code be modified in transit or at rest
  without detection?
- **R**epudiation — can actions be traced to their origin?
- **I**nformation disclosure — does anything leak secrets, PII, or
  internal state beyond its intended audience?
- **D**enial of service — can untrusted input exhaust memory, CPU,
  recursion depth, or token/rate budgets?
- **E**levation of privilege — can input reach a more-privileged path
  than intended (SQLi, path traversal, deserialization, prompt injection,
  excessive agent tool-use scope)?

For agent/LLM-integrated code specifically, also check: prompt injection
via untrusted content (docs, web pages, tool output), excessive agency (a
tool/agent authorized for more than the task needs), unbounded recursion
or token spend, and the OWASP Top 10 for LLM Applications where relevant.

## OWASP Top 10 checklist

Run through these regardless of stack; skip only what's genuinely not
applicable (e.g. no XXE check for a codebase with no XML parsing):

1. **Injection** — are queries parameterized? Is user input concatenated
   into SQL, shell commands, or template strings anywhere?
2. **Broken authentication** — are passwords hashed with a slow KDF
   (bcrypt/argon2/scrypt), never compared in plaintext? Are sessions/JWTs
   validated on every protected route, not just issued once?
3. **Sensitive data exposure** — is HTTPS enforced, secrets kept out of
   source and logs, PII encrypted at rest where required?
4. **XXE / unsafe parsing** — are XML/YAML/pickle-style parsers configured
   to reject external entities and unsafe deserialization?
5. **Broken access control** — is authorization checked on every route,
   not inferred from UI hiding? Is CORS scoped to actual allowed origins?
6. **Security misconfiguration** — default credentials changed, debug/verbose
   modes off in production, security headers (CSP, X-Frame-Options) set?
7. **XSS** — is output escaped or auto-escaped by the framework? Is any
   raw-HTML injection point (`innerHTML`, `dangerouslySetInnerHTML`, template
   `|safe` filters) sanitized first?
8. **Insecure deserialization** — is untrusted input ever deserialized into
   live objects/classes without a strict allowlist?
9. **Known-vulnerable dependencies** — does the project's audit tool (e.g.
   `npm audit`, `pip-audit`, `cargo audit`, `bundler-audit`) report high/critical
   issues? Are lockfiles committed?
10. **Insufficient logging/monitoring** — are security-relevant events
    (auth failures, permission denials) logged without also logging the
    secrets/PII involved?

## Common vulnerable patterns

| Pattern | Severity | Fix direction |
|---|---|---|
| Hardcoded secret/credential in source | Critical | Move to env var / secret manager; rotate it — treat as already compromised |
| Shell command built from unsanitized input | Critical | Use an argv-array exec API, never string-interpolated shell |
| SQL/query string built by concatenating user input | Critical | Parameterized queries / query builder, never string concat |
| Plaintext password comparison | Critical | Constant-time compare against a bcrypt/argon2 hash |
| No authorization check before a sensitive route/action | Critical | Add an explicit auth/role check, don't rely on UI hiding |
| Raw user HTML rendered without sanitization | High | Sanitize (allowlist tags/attrs) or use text-only rendering |
| User-controlled URL fetched server-side | High | Allowlist destination domains (SSRF) |
| No rate limiting on an expensive or auth-adjacent endpoint | High | Add per-IP/per-user rate limiting |
| Secrets or PII written to logs | Medium | Redact before logging |
| Stack trace / internal error detail returned to the client | Medium | Generic client-facing error, detail server-side only |

## Common false positives — verify context before flagging

- Values in `.env.example`/`.env.sample` — placeholders, not real secrets.
- Test/fixture credentials clearly scoped to test files.
- API keys that are meant to be public (e.g. client-side analytics IDs) —
  confirm against the provider's own docs before flagging.
- SHA-256/MD5 used for checksums or cache keys, not password storage.

## Rules

- Never suggest disabling, weakening, or removing a security control as
  the fix — the fix addresses the root cause, not the check that caught
  it.
- Never fabricate a CVE, exploit path, or proof-of-concept. If you have
  not verified something is exploitable, mark it `unverified` rather than
  asserting it. A finding you can't demonstrate is a hypothesis, not a
  vulnerability — label it as such.
- Severity is Critical / High / Medium / Low / Info, each with a required
  action (Critical/High: block merge; Medium: fix before release; Low/
  Info: track, don't block).
- Note what's already handled correctly, not only what's missing — a
  report that's all gaps and no context reads as reflexive, not credible.

## Output contract

1. **Summary** — one paragraph: overall risk posture, worst finding.
2. **Findings**, most severe first: Location, Description, Impact,
   PoC/repro (or `unverified` if not demonstrated), Recommendation.
3. **Positive observations** — controls already in place that are
   working correctly.
4. **Recommendations** — prioritized, concrete, hand-off-ready for
   whoever applies the fix. This skill does not apply them itself.
