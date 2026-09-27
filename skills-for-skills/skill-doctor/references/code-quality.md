# Code Quality

Whether the code, tests, and comments the agent produced are well-designed and consistent with the target
repository's conventions.

## Verdicts

| Verdict                 | Description                                                                                                                                                                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `approve`               | The agent produced well-designed, correct code that is consistent with repo conventions, adequately tested, and clean of smells; a senior reviewer would approve it outright, with at most trivial nits.                                         |
| `block`                 | The agent produced code with at least one defect a reviewer would insist on fixing before merge: a correctness or concurrency bug, a missed edge case, an inconsistent pattern, weak or missing tests, or mixed-in artifacts that do not belong. |
| `insufficient_evidence` | The extraction shows no code diff, or too little of one to judge.                                                                                                                                                                                |

## Rubric

Applies to sessions where the agent produced code changes. Evaluate the actual artifact — the edits
themselves, not the process used to produce them. Judge it the way a careful senior reviewer would review the
same pull request, using the target repository's own established conventions as the standard.

The verdict is binary: `approve` means that reviewer would merge the change as-is, with at most trivial nits;
if they would insist on a fix before merging — one real defect is enough — the verdict is `block`. If the
extraction does not show enough of the change to judge, the verdict is `insufficient_evidence` and the session
is excluded from aggregation rather than counted as either. The bullets below are common quality dimensions,
not an exhaustive checklist.

**Assess:**

- **Design.** The shape of the change fits the codebase; it is not premature abstraction, scope creep, or a
  change that belongs somewhere else.
- **Correctness.** The change does what it claims, including edge cases and concurrency safety.
- **Complexity.** No function, type, or expression does more than it needs to; no speculative genericity.
- **Repo conventions.** Follows the same idioms as similar code in the same module. An unexplained deviation
  from a clear local pattern is a defect even if the new code works.
- **Code smells.** Magic numbers or strings without a named constant, copy-paste that should be shared,
  commented-out code, vague or stale TODOs, workarounds patching a symptom, silently swallowed errors, deep
  nesting early returns would flatten.
- **Tests.** Present, and actually verifying the behavior they claim — a broken implementation would fail them
  — rather than asserting trivia or mocking away the logic under test; covering error and edge paths; not so
  coupled to internals that unrelated changes break them.
- **Naming.** Every new identifier communicates what it represents, unambiguously and without noise.
- **Comments.** Explain why, not what; no comment describes an edit, a refactor, or a prior state of the code
  rather than its current behavior.
- **Diff hygiene.** Only the edits intended to be committed — no scratch scripts, debug prints, or verification
  scaffolding left alongside.
- **Documentation.** Updated in the same change when the change affects how the software is built, tested, or
  used.
- **Corrections.** A defect the user pointed out mid-conversation counts against the artifact regardless of
  whether it was ultimately fixed; needing an external correction at all is a negative signal, not just a
  defect left unresolved.

Out of scope: how directly the agent worked, which is Efficiency. Judge the artifact on its own merits.

## Reading the extraction

The extractor caps machine payloads but never user text, so a user correction is reliably present and a large
diff may not be. Do not infer the absence of a defect from the absence of its diff — that is
`insufficient_evidence`.

Read the conventions of the repository the session ran in, from its instruction files, before applying them.

## Reason

One to three sentences citing the specific file, pattern, or defect that drove the verdict — quote or closely
paraphrase the line or convention at issue. **Name what would have caught it: a lint rule, a repository
convention the agent should have searched for, a test case, or a skill.** For `insufficient_evidence`, say what
you could not see.
