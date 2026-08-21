# Scoring Rubric

Six criteria, 100 points. Every criterion names the evidence required to score
it. **A criterion whose evidence was not gathered is reported `not assessed` and
its points leave the denominator.** Scoring from the CLAUDE.md text alone, for a
criterion that requires the codebase, produces a number that looks like
measurement and is not.

Score only at the anchors given. They are coarse on purpose: the underlying
judgment does not support finer resolution, and a `17/20` implies a precision
nobody has.

**Contents**
- [1. Commands and workflows (20)](#1-commands-and-workflows-20)
- [2. Architecture orientation (15)](#2-architecture-orientation-15)
- [3. Non-obvious knowledge (20)](#3-non-obvious-knowledge-20)
- [4. Density (15)](#4-density-15)
- [5. Currency (20)](#5-currency-20)
- [6. Actionability (10)](#6-actionability-10)
- [Reporting the total](#reporting-the-total)
- [Red flags](#red-flags)

---

## 1. Commands and Workflows (20)

**Evidence required**: the project's task runner or manifest — `package.json`
scripts, `justfile`, `Makefile`, `pyproject.toml`, `mise.toml`, `Cargo.toml`, or
the CI workflow. Without it, the criterion is `not assessed`.

| Anchor | Meaning |
|--------|---------|
| 20 | Every command a contributor needs is present, and each matches the runner |
| 15 | Present but incomplete — a documented path (test, lint, or deploy) is missing |
| 10 | Only the obvious build/run pair |
| 5 | Commands named without invocation, or scattered in prose |
| 0 | None |

Deduct to the next anchor down when documented commands duplicate what the
runner already exposes with no added context. A bare list of `package.json`
scripts costs tokens and adds nothing; `npm test -- --runInBand` *because the
suite shares a database* is the version worth keeping.

## 2. Architecture Orientation (15)

**Evidence required**: the actual directory tree, at least two levels.

| Anchor | Meaning |
|--------|---------|
| 15 | Names the non-obvious structure: which directory owns what, where the entry points are, which boundaries matter |
| 10 | Correct but partly derivable from a directory listing |
| 5 | A directory listing reproduced as prose |
| 0 | Absent, or contradicted by the tree |

**A directory tree that Claude can produce with one `ls` is not worth context.**
Score high only for what reading the tree does not reveal: why a boundary
exists, which of two similar directories is authoritative, what the dead code
is. Score a verbatim tree dump at 5 and recommend cutting it.

## 3. Non-Obvious Knowledge (20)

**Evidence required**: the file text alone is sufficient to score this.

| Anchor | Meaning |
|--------|---------|
| 20 | Several entries that took real debugging: ordering dependencies, environment quirks, workarounds with reasons |
| 15 | Some genuine gotchas, plus filler |
| 10 | One or two, or advice that is merely uncommon rather than project-specific |
| 5 | Generic best practice dressed as project knowledge |
| 0 | None |

This is the highest-value content in any CLAUDE.md and the hardest to
reconstruct. "Tests must run sequentially (`--runInBand`) due to shared DB
state" is a 20-point line. "Write meaningful variable names" is a 0-point line
that costs the same tokens forever.

## 4. Density (15)

**Evidence required**: the file text, plus every `@`-imported file.

| Anchor | Meaning |
|--------|---------|
| 15 | Every line earns its place; no restatement of the code |
| 10 | Mostly tight, some padding |
| 5 | Verbose; explanations where a line would do |
| 0 | Mostly filler, or explains a well-known technology |

Judge the **effective** size — entrypoint plus imports — against the 200-line
target, never the entrypoint alone. Report both numbers when they differ.

## 5. Currency (20)

**Evidence required**: verification against the repository. Check that
referenced paths exist (`ls`/`test -e`), that documented commands exist in the
runner, and that named tools appear in the manifest. Running a build is not
required; confirming a command is still *defined* is.

| Anchor | Meaning |
|--------|---------|
| 20 | Every checked reference resolves |
| 15 | One or two stale references, none load-bearing |
| 10 | A documented command or path no longer exists |
| 5 | Several stale references; the file describes an earlier version of the project |
| 0 | Substantially describes a project that no longer exists |

**NEVER score this by reasoning about whether a command would work.** Either the
check was run and the result is citable, or the criterion is `not assessed`.
This is the single easiest place to fabricate a score, and a fabricated Currency
score is worse than no audit — it certifies staleness as freshness.

## 6. Actionability (10)

**Evidence required**: the file text alone.

| Anchor | Meaning |
|--------|---------|
| 10 | Instructions are concrete and checkable — "use 2-space indentation", not "format properly" |
| 5 | Mixed; several instructions cannot be verified by reading a diff |
| 0 | Vague throughout |

The test: could a reviewer tell from the diff alone whether the instruction was
followed? If not, it will not be followed reliably either.

## Reporting the Total

Report `earned / assessed`, then the band — never a bare `X/100` when something
went unassessed, and never an average across files.

| Band | Range |
|------|-------|
| A | 90%+ of assessed points |
| B | 75–89% |
| C | 60–74% |
| D | 40–59% |
| F | under 40% |

Rules:

- List every `not assessed` criterion with the evidence that was missing. A
  reader must be able to see what the score does not cover.
- Score each file separately. Averaging across a root file and a package file
  produces a number with no meaning.
- State the grade's weakest link. A B built on a 0 in Non-obvious knowledge and
  a 20 in Commands needs a different fix than a flat B.

## Red Flags

Findings worth reporting regardless of score:

- A memory file at a path Claude Code never reads (`.claude.md`,
  `.claude.local.md`, or `AGENTS.md` with no importing `CLAUDE.md`)
- Contradictions between scopes — both texts are in context, and neither wins
- An import chain deeper than four hops; everything past the fourth is silently absent
- A relative import written as if it resolved from the working directory rather
  than from the importing file
- Content duplicated between a root file and a nested one, paying twice for one instruction
- An instruction that must hold every time, written as prose rather than a hook
- `TODO` entries that predate the last release
- A file over 200 effective lines with no path-scoped rules extracted
