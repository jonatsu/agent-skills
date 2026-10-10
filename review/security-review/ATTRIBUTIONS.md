# Attributions

## Current Skill

- Skill: `security-review`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original skill containing four adapted passages in `SKILL.md`. Its predecessor is this repository's
  own `security-audit`. Two external skills influenced it, and one of them supplied material that was adapted
  rather than merely read.

The six reference files, the procedure, the STRIDE section, the false-positive list, the rules, and the fix
phase were written for this skill. Four passages in `SKILL.md` are adaptations and are named below.

The skill descends from `security-audit`, previously deployed from this repository. Its redundant archived
package was deleted on 2026-09-11; the source remains in Git history at
`f1879f39fb161e8b89a01fb5b2c18cdef6278a10:archived/review/security-audit/`.
That skill was written by the same author under MIT, so its
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

**Material adapted from the upstream `SKILL.md`.** Four passages in this skill's `SKILL.md` follow the
upstream's structure and wording closely enough that they are adaptations rather than independent expression:

- the severity table, whose Critical and Low definitions remain close to the upstream sentences and whose High
  and Medium rows are paraphrases. The required-action column is new;
- the confidence table, which keeps the upstream's three tiers, their order, and their criteria, with the
  lowest tier suppressed rather than reported;
- the attacker-controlled against operator-controlled table, whose two-column form and row selection follow
  the upstream. The rows were de-Pythonised, four were added, and the qualification that operator-controlled
  is not the same as safe is new; and
- the output contract, which keeps the upstream's field set and order with renamed fields and identifiers.

The bolded `Report on` and `Research` labels in the scope contract also come from the upstream.

Ideas retained and expressed independently:

- gating a finding on confidence before severity;
- separating the scope reported on from the scope researched, so reading beyond the diff is required while
  reporting beyond it is not; and
- routing to a topic reference chosen by the surface under review.

**Licensing.** The adapted material is from the upstream `SKILL.md`, which the repository licenses under
Apache-2.0. Its text is preserved verbatim in `LICENSE.upstream`, and the upstream project supplies no
`NOTICE` file. CC BY-SA 4.0 attaches to the upstream's `references/` tree, derived from the OWASP Cheat Sheet
Series; no material from that tree was read into this skill's reference files, which were written from the
domain. The package's top-level `license: MIT` governs the independently written material.

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

No wording, example, or reference file was taken from this upstream package. Its language and framework
reference set was deliberately excluded, because this skill is language-agnostic by design.

## Coverage Note

The vulnerability classes come from the author's domain knowledge, checked against the two sources above. No
OWASP, CWE, or vendor document was read during authoring, so the skill reproduces no catalogue and cites none.
Where a finding depends on a specific catalogue entry or framework behavior, the skill requires the reviewer to
verify it against that source at the time.
