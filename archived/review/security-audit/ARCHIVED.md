# Archived: security-audit

- Archived: 2026-09-02
- Reason: Removed from deployment with the intact `review/` domain while unused, then reviewed on 2026-09-04 and
  replaced. Its OWASP checklist was the 2017 list, it had no confidence gate and no data-flow tracing step, so it
  emitted pattern matches as findings
- Last deployed to: Claude Code, OpenCode, GitHub Copilot CLI, and Codex
- Successor: `skills/shared/review/security-review/`, which keeps the STRIDE trust-boundary method, the
  report-only constraint and the ban on fabricated proofs of concept, and adds confidence gating, data-flow
  tracing, six topic references, and an approval-gated fix phase. Evidence in
  `docs/evaluations/2026-09-04-security-review.md`
