# Attributions

## Current skill

- Skill: `lint-config-audit`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original text; ideas influenced by one upstream skill

## Idea-level influence

- Upstream project: [agentydragon/ducktape](https://github.com/agentydragon/ducktape), skill
  `skills/lint_audit/SKILL.md`.
- Upstream revision: `4ad338af25ea537dc7f817390b2e25c2a7a903f0`, read on 2026-09-30.
- Upstream license: AGPL-3.0, as stated in the repository's README. The repository root carries no licence
  file.

The ideas taken: an audit that inventories each language's checkers before proposing anything; proving every
suppression against the code it covers; treating zero-violation candidates as free guardrails; findings ordered
from misconfiguration through free guardrails, rules worth enabling with real examples, and tightenings; noting
open work that touches the same configuration; one change per commit; and a comment recording each rejected
rule.

No upstream text was copied or adapted. Because the AGPL-3.0 does not fit this repository's MIT skills, every
sentence here was written independently. Three parts are this skill's own, not upstream's: the proof that a
zero count could have seen a violation, the checkers' built-in unused-suppression detectors in
`references/checker-recipes.md`, and stopping on a behavior-changing fix instead of adding a new suppression.
