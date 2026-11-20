# Source Comparison: antislop-code Against coding-standards

Date: 2026-11-20. Source: <https://github.com/miqdadbadjuber/anti-slop>, commit
`44b3547ed6d6f21eed777271602da113efc53c94`, MIT. Read in full: `skills/antislop-code/SKILL.md` (128 lines, the whole
skill, no other files) and the core rules it cites (`antislop.md`, R-31 at lines 594-605). Ours: `coding-standards`
`SKILL.md` and `references/comments.md`, `solid-and-quality.md`, `testing-standards.md`, plus `python-style` and
`rust-style` where a pattern is language-specific. Cites are `file:line`; source files are relative to the clone,
ours to `development/coding-standards/` unless a path is given.

Facts are marked as such. Judgment is marked "Judgment".

## What the Source Is

Fact: `antislop-code` is a comment-hygiene skill, not a code-quality skill. Its description says "Code comment
hygiene ... never touch the code" (`SKILL.md:3`), and its scope guardrail forbids changing anything but comments
(`SKILL.md:16`). It names 11 patterns, each as Tell, Why, Fix (`SKILL.md:19-87`), then a keep-list (`:89-113`) and a
10-item yes/no checklist (`:115-128`). It carries no pattern about non-comment code: no over-defensive checks, needless
abstraction, or dead branches. So it cannot show any code-slop gap beyond comments.

Fact: the skill is not standalone. It must be read with the 746-line `antislop.md` core, which is a web-UI design
ruleset (`SKILL.md:10,14`). I found no eval, measurement, or benchmark for this skill in the repository. The only
evidence for its claims is one before-and-after image (`README.md:72-74`).

## Patterns Ours Lacks

All of these belong in `references/comments.md` unless noted. Our comment guidance is already good on why-not-what;
the gaps are specific named patterns and one conflict.

- **Doc-comment signature echo** (`SKILL.md:51-55`): a block that only repeats the signature
  (`@param price The price.`). It matters because we push the other way: `SKILL.md:112` and `references/comments.md:54`
  say to keep every public API doc-comment, with nothing in `coding-standards` to stop an echo. Python has the
  counterweight ("omit empty sections and redundant descriptions", `python-style/SKILL.md:50-52`). Rust does not:
  `rust-style/SKILL.md:214` requires `///` on every public item with no echo guard. Owner: `comments.md` for the
  language-agnostic rule, `rust-style` for its own version.
- **A keep-list for comment cleanup that includes legal notices** (`SKILL.md:89-102`). It matters because our
  legacy-file rule says to strip all comments, then re-add each one that earns its place (`references/comments.md:95-98`).
  Applied literally, that deletes a licence header, and nothing in `coding-standards` or the two language skills
  mentions licence headers or tooling directives (a search of all three for `noqa`, `ts-ignore`, `type: ignore`,
  `eslint-disable`, `SPDX`, and `shebang` found nothing). The source's list also omits directives (see defects), so
  the directive carve-out is ours to write. Owner: `comments.md`.
- **End markers** (`SKILL.md:63-67`): `} // end if`, `# End of function`. Our anti-pattern list has dividers, changelog
  comments, and name restating (`comments.md:73-77`), not this. Owner: `comments.md`.
- **Empty labels** (`SKILL.md:39-43`): `// Main logic`, `// Helper function`, `// Note: This is important.` A label
  names a category, not a fact. Not in `comments.md:71-77`. Owner: `comments.md`.
- **Decorative emoji and shouting capitals in comments** (`SKILL.md:21-25,57-61,83-87`). Ours bans dividers only
  (`comments.md:76`). Low value, one clause. Owner: `comments.md`.
- **Stiff register** (`SKILL.md:83-87`): "This function is responsible for validating whether ...". Ours has no
  guidance on register, only on length (`comments.md:43-44`). Judgment: worth one sentence, a plain imperative or
  declarative line. Owner: `comments.md`.
- **Comment density, one per logical block** (`SKILL.md:77-81`). Ours says silence is correct when code needs no
  comment (`comments.md:5-6`) and shows loop narration (`comments.md:29-34`) but gives no density test. Partial gap.
  Owner: `comments.md`.
- **Comments in the pre-commit bar.** The quality gates (`references/solid-and-quality.md:48-54`) list tests, linter,
  type checker, build, and scan, with no comment check. Source: `SKILL.md:115-128`. Judgment: low priority, because
  `SKILL.md:108-114` already points to the comment reference.

## Patterns Ours Already Covers

Ours already covers restating the obvious (`comments.md:11-19,77`), mechanical narration of a loop (`comments.md:29-34`),
decorative dividers (`comments.md:76`), vague TODOs by requiring the resolving condition (`comments.md:59-60`), the
debugging story as a comment (`comments.md:91-93`), a stable external reference rather than an issue trail
(`SKILL.md:116-118`), and short, one-line comments (`comments.md:43-44`).

## Techniques Worth Taking

Write each independently. Nothing is copied, and the source goes in `ATTRIBUTIONS.md` for whatever is taken.

- **Keeping and length are separate tests** (`SKILL.md:111-113`). Fact: the source says earning a place states what
  may stay, never how long it may run. Judgment: this is the most useful single idea. It stops an agent defending a
  five-line workaround comment because workarounds are valid. We have the short-comment rule (`comments.md:43-44`) but
  not the explicit separation.
- **A label survives only if it carries a checkable fact** (`SKILL.md:41-43`). "Retries happen only on 5xx" stays,
  "this is important" goes. A clean test for notes of all kinds.
- **A doc-comment keeps only what the signature cannot say** (`SKILL.md:55`): rules, edge cases, units, side effects,
  limits. Makes the echo rule testable. Python already phrases it close to this (`python-style/SKILL.md:50-52`).
- **Narration points at structure, not at a comment** (`SKILL.md:37`). If the flow needs numbered steps to follow, the
  fix is extraction, not annotation. Ours says rename first (`comments.md:8-9`) and caps function length
  (`SKILL.md:127-131`); joining the two is cheap.
- **Verify that a comment-only change left the code untouched.** Judgment, ours rather than the source's: the source
  states the guardrail (`SKILL.md:16`) but gives no way to check it. Comparing the code with comments stripped, before
  and after, is a mechanical check worth naming in a cleanup procedure.

## Not Worth Taking

- **The hard line cap**, "one line, two at most, never three" (`SKILL.md:75`). Judgment: arbitrary, and it clashes with
  the source's own keep-list (`SKILL.md:99,111-113`), which preserves workaround notes. Our "prefer one line"
  (`comments.md:43`) is the right strength.
- **Dropping issue numbers and versions** (`SKILL.md:75`). Judgment: our HACK example names a library version and a
  removal condition (`comments.md:65`), and that is what lets a later reader delete the workaround. Our
  external-reference rule (`SKILL.md:116-118`) already decides this case by whether the reference prevents an editing
  mistake.
- **Deleting a vague TODO outright** (`SKILL.md:47-49`). Judgment: the skill cannot tell an AI TODO from a human
  author's marker. Ours asks for the resolving condition (`comments.md:59-60`), which keeps the information.
- **Judging comments by whether they read as AI** (`SKILL.md:10,31,87`). Ours judges content (`comments.md:3-6`), which
  is more defensible and needs no provenance.
- **The Tell, Why, Fix format with rule numbers.** It depends on the core's R-numbers and its UI purpose test. A
  skill of ours must stand alone (`AGENTS.md`).
- **The source's comment-only guardrail as a general rule.** Ours already scopes changes (`SKILL.md:33-36`).
  The comment-only guardrail suits a cleanup task, not `coding-standards`.

## Defects in the Source

- **Misapplied rule.** The skill cites R-31 as the governing rule for "every comment adds information" and for
  banners (`SKILL.md:25,119`). Fact: R-31 in the core requires a one-line reason for each colour, layout, typography,
  spacing, card, and icon decision (`antislop.md:594-605`). It does not govern comments. The cross-reference is a
  stretch, and the skill cannot be understood without the 746-line UI core (`SKILL.md:10`).
- **The keep-list omits tooling directives**, and the scope guardrail (`SKILL.md:16`) therefore does not hold. Comments
  such as `# noqa`, `# type: ignore`, `// eslint-disable`, `// @ts-ignore`, pragmas, shebangs, and encoding lines
  change tool behaviour, so removing one is not "only comments". The keep-list (`SKILL.md:91-102`) names none. Related:
  the Signature Echo fix, "simplify or remove" (`SKILL.md:55`), is wrong in JavaScript that TypeScript checks. The
  TypeScript handbook says JSDoc annotations supply types in checked `.js` files
  (<https://www.typescriptlang.org/docs/handbook/type-checking-javascript-files.html>, read 2026-11-20), so deleting
  `@param {number} price` can change type results.
- **Self-contradiction on workarounds and length.** Workarounds are preserved (`SKILL.md:99`), but the cure for the
  over-explained comment drops the issue number and version (`SKILL.md:75`), the very facts that mark when a workaround
  can go.
- **No provenance test.** Every Fix says "remove" (`SKILL.md:31-67`) regardless of who wrote the comment. Run over a
  human-written file, it bulk-deletes human notes. Our own legacy-file rule has the same exposure
  (`comments.md:95-98`).
- **Unsupported claims about AI habits**, such as emoji "(✅, 🚀, 🔒) is the AI default vocabulary" (`SKILL.md:61`). I
  found no data or eval for them in the repository.
- **JavaScript bias.** The only code example is JS (`SKILL.md:106-109`), and the signature-echo pattern is
  JSDoc-shaped (`SKILL.md:53`). Python docstrings, Rust `///`, and Go doc comments are not addressed.
- **Name overclaims.** "antislop-code" reads as code slop in general, but the skill is comment cleanup only
  (`README.md:216` lists it as "Comment cleanup").

## Ownership Summary

`coding-standards` `references/comments.md`: echo rule, keep-list with legal notices and directives, end markers,
empty labels, emoji and register, density, keeping-versus-length separation. `rust-style`: echo guard on `///`.
`python-style` already has its echo rule. No other skill is affected; the source has nothing on non-comment code.
