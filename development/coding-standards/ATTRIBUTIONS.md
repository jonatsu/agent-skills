# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## Third-party Sources

### nguyenhuuca: assessment

- Source: <https://github.com/nguyenhuuca/assessment>, `docs/claude/rules/code-quality.md`
- License: `LicenseRef-No-License`
- Version: `9a34e179849504db74bfc4015ff36fe20125c1c4`

The repository declares no license, so all rights remain with its author. The rule file supplied the selection of
SOLID, performance checklist, and quality-gate items, and the two-hats refactoring framing in
`references/solid-and-quality.md`. Nothing was copied.

### vitalykovalgit: Sencilla

- Source: <https://github.com/vitalykovalgit/Sencilla>, `promts/claude/rules/self-explanatory-code-commenting.md`
- License: `LicenseRef-No-License`
- Version: `5bed4a03a28becbbef86efe2790fa9483f18685d`

The repository README names MIT but ships no license file, so no license is established. The rule file supplied the
structure of paired good and bad comment examples, the annotation vocabulary, and the comment anti-patterns in
`references/comments.md`. Nothing was copied.

### steeef: dotfiles

- Source: <https://github.com/steeef/dotfiles>, `nix/home/claude/rules/comments.md`
- License: `LicenseRef-No-License`
- Version: `9e05ad1a4811b9d7730a6bfe96cca92a1d7b494d`

The repository declares no license, so all rights remain with its author. The rule file supplied the keep-comments-short
and legacy-file cleanup guidance in `references/comments.md`. Nothing was copied.

### Sam McDavid: dotfiles

- Source: <https://github.com/samcdavid/dotfiles>, `claude/rules/comment-style.md`
- License: `LicenseRef-No-License`
- Version: `d5474888639bfcabd45cf2362b2e91fc1890cad7`

The repository declares no license, so all rights remain with its author. The rule file supplied the why-versus-how
framing and the rename-instead-of-commenting rule in `references/comments.md`. Nothing was copied.

### Affaan Mustafa: ECC

- Source: <https://github.com/affaan-m/ECC>, `skills/coding-standards/SKILL.md`
- License: `MIT`
- Version: `d29cf651c795869f733669c33e3d33dfd8307d10`

The skill supplied the subjects of the formatting guidance, the type-system escape-hatch sentence, premature
optimization under KISS, and the sequential-await and over-fetching items in the performance checklist of
`references/solid-and-quality.md`. Nothing was copied.

### Miqdad Badjuber: antislop `antislop-code` skill

- Source: <https://github.com/miqdadbadjuber/anti-slop>, `skills/antislop-code/`
- License: `MIT`
- Version: `44b3547ed6d6f21eed777271602da113efc53c94`

The skill supplied four ideas for the comment rules: a doc-comment says only what the signature cannot, keeping a
comment and its length are separate tests, a label survives only with a checkable fact, and numbered step comments
point to functions waiting to be extracted. The rules were written independently; no text was copied.

### luongnv89: claude-howto `clean-code-reviewer` agent

- Source: <https://github.com/luongnv89/claude-howto>, `04-subagents/clean-code-reviewer.md`
- License: `MIT`
- Version: `b9a973bf32bc28bdccb106012397e10235779bc3`

The agent supplied the split of a maintainability review from a correctness review, and the categories that
review checks. No text was copied.

### FerroxLabs: wayland `clean-code` skill

- Source: <https://github.com/FerroxLabs/wayland>,
  `src/process/resources/skills-library/bodies/skills/software-engineering/clean-code/SKILL.md`
- License: `AGPL-3.0-or-later`
- Version: `4c030c7b01c241df7b6e3535635a970f10d781af`

The repository's `package.json` declares the licence, and the file's frontmatter claims Apache-2.0. The skill
supplied four ideas: positive booleans, replacing noise words, one level of abstraction per function, and
separating commands from queries. Every rule was written independently, and no text was copied.

### Alexis King: Parse, don't validate

- Source: <https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/>
- License: `LicenseRef-No-License`
- Version: 2019-11-05

The post declares no license, so all rights remain with its author. It supplied the rule to parse input at the
system boundary into types the rest of the code trusts, in `SKILL.md` and `references/testing-standards.md`.
Nothing was copied.

### Jim Shore: Fail Fast

- Source: <https://martinfowler.com/ieeeSoftware/failFast.pdf>
- License: `LicenseRef-Proprietary`
- Version: IEEE Software, vol. 21, no. 5, 2004

The article is copyrighted by IEEE. It supplied the fail-fast layer of the testing bar and the line between loud
checks and tests: checks guard the seams, and tests still own the logic inside a function. Nothing was copied.

### Oracle: Programming With Assertions

- Source: <https://docs.oracle.com/javase/8/docs/technotes/guides/language/assert.html>
- License: `LicenseRef-Proprietary`
- Version: Java SE 8

The guide is copyrighted by Oracle. It supplied the rule to keep assertions for states the code rules out and to
check public arguments explicitly, because assertions can be disabled. Nothing was copied.

### Kent Beck: answer on how much to test

- Source: <https://stackoverflow.com/a/153565>
- License: `CC-BY-SA-2.5`
- Version: 2008-09-30

The answer supplied the aim of testing for confidence rather than coverage. Nothing was copied.

### Kent Beck: Canon TDD

- Source: <https://tidyfirst.substack.com/p/canon-tdd>
- License: `LicenseRef-No-License`
- Version: 2023-12-11

The post declares no license, so all rights remain with its author. It supplied the point that writing a test
first decides when a test is written, not whether it is worth writing. Nothing was copied.

### Titus Winters, Tom Manshreck, and Hyrum Wright: Software Engineering at Google

- Source: <https://abseil.io/resources/swe-book>, chapter 12, "Unit Testing"
- License: `CC-BY-NC-ND-4.0`
- Version: first edition, O'Reilly, 2020

The chapter supplied the rule to test behaviors rather than methods, and the rule that a bug fix includes the
test case that was missing. Nothing was copied.

### Koen Claessen and John Hughes: QuickCheck

- Source: <https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf>
- License: `LicenseRef-Proprietary`
- Version: ICFP 2000

The paper is copyrighted by ACM. It supplied property-based testing as the replacement for many hand-picked
examples over a large input space. Nothing was copied.
