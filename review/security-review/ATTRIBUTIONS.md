# Attributions

## Current Skill

- Skill: `security-review`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original skill. Its predecessor is this repository's own `security-audit`, and two external skills
  influenced its structure and several of its rules. No text, example, or code was copied from either.

The skill descends from `security-audit`, previously deployed from this repository and now under
`skills/archived/review/security-audit/`. That skill was written by the same author under MIT, so its
STRIDE-per-trust-boundary method, its report-only constraint, its ban on fabricated proofs of concept, and its
requirement to record working controls carry forward without an external attribution obligation.

## Influencing Source: getsentry/skills

- Original author: Sentry (Functional Software, Inc.) and contributors
- Upstream project: [getsentry/skills](https://github.com/getsentry/skills)
- Upstream skill: `security-review`
- Source path: `skills/security-review/`
- Source commit: `c2f99a5b04b4cd992ec3022d7c2c3e23e938d241`
- Source file:
  <https://github.com/getsentry/skills/blob/c2f99a5b04b4cd992ec3022d7c2c3e23e938d241/skills/security-review/SKILL.md>
- License status: the repository is Apache-2.0. The skill's reference material is derived from the OWASP Cheat
  Sheet Series under CC BY-SA 4.0, and the package carries that license text.

Ideas retained, each expressed independently here:

- gating a finding on confidence before severity, and suppressing the lowest tier rather than reporting it;
- separating the scope reported on from the scope researched, so reading beyond the diff is required while
  reporting beyond it is not;
- classifying a value as attacker-controlled or operator-controlled as the decisive step before flagging; and
- routing to a topic reference chosen by the surface under review.

The classification table, the confidence criteria, the severity definitions, the reference topics, and every
sentence of the reference files were written for this skill. CC BY-SA 4.0 governs the upstream expression and
does not reach independently written expression, so nothing here is redistributed under it. The upstream
material was read, not adapted, and this package therefore ships no `LICENSE.upstream`.

Two upstream defects were deliberately not carried over. Its reference router names seven files that the
package does not contain, and its general guidance is written around specific Python and JavaScript
frameworks, which conflicts with this skill's language-agnostic scope.

## Influencing Source: openai/skills

- Original author: OpenAI and contributors
- Upstream project: [openai/skills](https://github.com/openai/skills)
- Upstream skill: `security-best-practices`
- Source path: `skills/.curated/security-best-practices/`
- Source commit: `49f948faa9258a0c61caceaf225e179651397431`
- Source file:
  <https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-best-practices/SKILL.md>
- License status: Apache-2.0. The upstream repository is marked deprecated.

Ideas retained, each expressed independently here:

- treating a documented project exception as an answer rather than as a finding to repeat;
- judging transport controls against the environment that runs the code, so a missing TLS or `Secure` cookie
  setting in local development is not reported as a vulnerability, and HSTS is recommended only with its
  consequence stated; and
- fix hygiene after approval: one finding per change, awareness that insecure code usually has a dependent,
  and use of the repository's own test and commit conventions.

No wording, example, or reference file was taken from the upstream package. Its language and framework
reference set was deliberately excluded, because this skill is language-agnostic by design.

## Coverage Note

The vulnerability classes come from the author's domain knowledge, checked against the two sources above. No
OWASP, CWE, or vendor document was read during authoring, so the skill reproduces no catalogue and cites none.
Where a finding depends on a specific catalogue entry or framework behavior, the skill requires the reviewer to
verify it against that source at the time.
