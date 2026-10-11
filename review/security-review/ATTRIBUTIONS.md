# Attributions

- Author: Joonas Onatsu
- License: `MIT`

Four passages of `SKILL.md` are modified from an Apache-2.0 work under section 4 of that license. Keep `LICENSE.upstream`
with the skill when redistributing it.

## Third-party Sources

### Sentry: `security-review` skill

- Source: <https://github.com/getsentry/skills>, `skills/security-review/SKILL.md`
- License: `Apache-2.0`
- Version: `c2f99a5b04b4cd992ec3022d7c2c3e23e938d241`

Adapted: the severity table, the confidence table, the attacker-controlled versus operator-controlled table, and the
output contract follow the upstream structure, modified to be language-agnostic. The `Report on` and `Research` labels
in the scope contract also come from the upstream.

### OpenAI: `security-best-practices` skill

- Source: <https://github.com/openai/skills>, `skills/.curated/security-best-practices/SKILL.md`
- License: `Apache-2.0`
- Version: `49f948faa9258a0c61caceaf225e179651397431`

The skill supplied three ideas: treating a documented project exception as an answer rather than a finding to repeat,
judging transport controls against the environment that runs the code, and fix hygiene after approval, such as one
finding per change. The ideas are expressed independently, and nothing was copied.
