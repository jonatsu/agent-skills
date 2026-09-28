# Attributions

## Current skill

- Skill: `coding-standards`
- Current author: Joonas Onatsu
- Declared license: MIT
- Status: original synthesis, written 2026-09-22. Most of the body was moved from this repository's own
  always-loaded `agents/shared/rules/coding-style.md`, which the same author wrote. The external sources below
  informed subject selection, structure, and examples for the added material.

**These records are permanent.** A source entry is not closed by later editing, and it is kept in the past
tense once the material it describes is gone, so a reader who reaches an older revision can establish what the
relationship was.

## Informed by (subject selection, structure, and examples)

No text or code was copied from the sources below. Each supplied canonical software-engineering material: SOLID,
the why-not-what commenting rule, the two-hats refactoring discipline, a performance checklist, an annotation
vocabulary, all common knowledge rather than any one repository's property. The material was re-expressed
independently in `SKILL.md` and the references. The sources are recorded because reading them shaped what the
skill covers and how its examples are framed, which this repository treats as attribution-bearing regardless of
whether wording is copied.

- [nguyenhuuca/assessment](https://github.com/nguyenhuuca/assessment/blob/9a34e179849504db74bfc4015ff36fe20125c1c4/docs/claude/rules/code-quality.md),
  `docs/claude/rules/code-quality.md` at `9a34e17`: the SOLID summary, the performance checklist items, the
  quality-gate list, and the two-hats refactoring-discipline framing in `references/solid-and-quality.md`.
- [vitalykovalgit/Sencilla](https://github.com/vitalykovalgit/Sencilla/blob/5bed4a03a28becbbef86efe2790fa9483f18685d/promts/claude/rules/self-explanatory-code-commenting.md),
  `promts/claude/rules/self-explanatory-code-commenting.md` at `5bed4a0`: the good-versus-bad comment example
  structure, the annotation vocabulary, and the comment anti-patterns in `references/comments.md`.
- [steeef/dotfiles](https://github.com/steeef/dotfiles/blob/9e05ad1a4811b9d7730a6bfe96cca92a1d7b494d/nix/home/claude/rules/comments.md),
  `nix/home/claude/rules/comments.md` at `9e05ad1`: the keep-it-short and legacy-file-cleanup guidance in
  `references/comments.md`.
- [samcdavid/dotfiles](https://github.com/samcdavid/dotfiles/blob/d5474888639bfcabd45cf2362b2e91fc1890cad7/claude/rules/comment-style.md),
  `claude/rules/comment-style.md` at `d547488`: the why-versus-how framing and the rename-instead-of-commenting
  rule in `references/comments.md`.
- [affaan-m/ECC](https://github.com/affaan-m/ECC/blob/d29cf651c795869f733669c33e3d33dfd8307d10/skills/coding-standards/SKILL.md),
  `skills/coding-standards/SKILL.md` at `d29cf65` (MIT), compared on 2026-09-28: the subjects of the Formatting
  subsection, the type-system escape-hatch sentence, premature optimization in the KISS principle, and the
  sequential-await and over-fetching items in the performance checklist of `references/solid-and-quality.md`.
  Its framework-specific material and its examples were not adopted.

Licenses were not audited because no material was copied, adapted, or vendored, so no `LICENSE.upstream` applies.
Were any source text later copied into this package, its license would have to be checked and preserved first.
