# Scoring Rubric

Six criteria, 100 points. Every criterion names the evidence required to score
it. **A criterion whose evidence was not gathered is reported `not assessed` and
its points leave the denominator.** Scoring from the instruction file's text
alone, for a criterion that requires the codebase, produces a number that looks
like measurement and is not.

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

**Evidence required**: the project's task runner or manifest — whichever this
repo actually has. Discover it; do NOT assume an ecosystem. Without it, the
criterion is `not assessed`.

**A repository may have more than one, and they may not agree.** A polyglot repo
can carry several manifests, and a second runner in a subdirectory may be only
partly forwarded to from the root — so "documented" against one runner can still
leave a whole surface undocumented. Establish which is the entry point and which
are independent BEFORE scoring, state that reading in the report, and score
against all of them. A file that documents the root runner completely while
never mentioning a non-forwarded sibling is incomplete, not complete.

| Anchor | Meaning |
|--------|---------|
| 20 | Every command a contributor needs is present, and each matches the runner |
| 15 | Present but incomplete — a documented path (test, lint, or deploy) is missing |
| 10 | Only the obvious build/run pair |
| 5 | Commands named without invocation, or scattered in prose |
| 0 | None |

Deduct to the next anchor down when documented commands duplicate what the
runner already exposes with no added context. A transcription of the runner's
own recipe list costs tokens and adds nothing. The version worth keeping carries
what the runner does not state — a flag together with the reason it exists: a
test command forced to run sequentially *because the suite shares a database*,
or a build invoked through the project's environment manager *because the
ambient interpreter resolves differently*.

## 2. Architecture Orientation (15)

**Evidence required**: the actual directory tree, at least two levels.

| Anchor | Meaning |
|--------|---------|
| 15 | Names the non-obvious structure: which directory owns what, where the entry points are, which boundaries matter |
| 10 | Correct but partly derivable from a directory listing |
| 5 | A directory listing reproduced as prose |
| 0 | Absent, or contradicted by the tree |

**A directory tree the agent can produce with one listing command is not worth
context.** Score high only for what reading the tree does not reveal: why a
boundary exists, which of two similar directories is authoritative, what the
dead code is. Score a verbatim tree dump at 5 and recommend cutting it.

## 3. Non-Obvious Knowledge (20)

**Evidence required**: the file text alone is sufficient to score this.

| Anchor | Meaning |
|--------|---------|
| 20 | Several entries that took real debugging: ordering dependencies, environment quirks, workarounds with reasons |
| 15 | Some genuine gotchas, plus filler |
| 10 | One or two, or advice that is merely uncommon rather than project-specific |
| 5 | Generic best practice dressed as project knowledge |
| 0 | None |

This is the highest-value content in any instruction file and the hardest to
reconstruct. "Tests must run sequentially due to shared database state" is a
20-point line. "Write meaningful variable names" is a 0-point line that costs
the same tokens forever.

## 4. Density (15)

**Evidence required**: the file text, plus every included file.

| Anchor | Meaning |
|--------|---------|
| 15 | Every line earns its place; no restatement of the code or the environment |
| 10 | Mostly tight, some padding |
| 5 | Verbose; explanations where a line would do |
| 0 | Mostly filler, or explains a well-known technology |

Judge the **effective** size — entrypoint plus includes — against the file's
budget, never the entrypoint alone. Report both numbers when they differ. Where
the repository sets no budget of its own, 150 to 200 effective lines is the
usual point at which a root file stops being read carefully.

**The line budget is a heuristic, and this criterion is where it must be allowed
to lose.** Some repositories genuinely need a longer file — one whose subject
matter *is* agent configuration, or one where the guidance is load-bearing every
session. If the only way to score higher is to extract content that must not be
missed, the rubric is wrong for that repo: say so in the Evidence column, score
what the file is worth, and NEVER propose an extraction whose sole benefit is
this number. An edit that raises Density by moving critical instructions
somewhere they may never load has made the file worse and the score better.

## 5. Currency (20)

**Evidence required**: verification against the repository. Check that
referenced paths exist, that documented commands exist in the runner, and that
named tools appear in the manifest. Running a build is not required; confirming
a command is still *defined* is.

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
- **The score answers "does this file have the right shape", never "is the
  knowledge still here".** An edit that deletes a hard-won convention to meet a
  line budget scores higher afterwards. Run the preservation check in Phase 7;
  never let the score stand in for it.

## Red Flags

Findings worth reporting regardless of score:

- **`AGENTS.md` and `CLAUDE.md` both present as real files with divergent
  content.** Three agents read three different things; see
  `loading-model.md`. Report it — never auto-resolve it.
- An instruction file at a filename no first-class agent reads
- **An instruction file stating a rule that its own examples, templates or code
  blocks break.** Both halves read as correct alone; only checking them against
  each other finds it, and nothing about the file looks wrong until you do
- Agent-agnostic guidance living in a directory named for one agent, reachable
  by the others only through a pointer
- Path-scoping frontmatter on a rule file → treat that file as **not loaded**
- Contradictions between two instruction files in the same repository — on at
  least one agent both texts are in context and neither wins
- An include chain deeper than the shallowest first-class agent's limit;
  everything past it is silently absent
- Guidance that depends on include expansion in a repository whose agents
  include one that does not parse includes
- A relative include written as if it resolved from the working directory
  rather than from the including file
- Content duplicated between a root file and a nested one, paying twice for one
  instruction
- A per-package instruction file with no pointer row in the root file
- An instruction that must hold every time, written as prose rather than a hook
  or a CI gate
- **A safety rule with no hook or gate behind it.** It reads as a control and is
  not one — a reviewer who sees it stops looking for the real gate, so this
  scores worse than the rule's absence
- An autonomy grant, an "always finish no matter what", or an instruction that
  the agent may approve its own risky action. The file cannot confer authority it
  does not hold, and the user's own turn outranks it
- Vendored, generated, or third-party text cited as a source of this repo's
  conventions — data the repository stores, not guidance it has adopted
- `TODO` entries that predate the last release
- A file over its effective line budget with nothing extracted and pointed at
