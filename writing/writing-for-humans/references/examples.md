# Worked Rewrites

Two rewrites that walk a multi-step procedure. Single-pattern fixes are not shown here: `phrases.md` and
`structures.md` name those patterns and the replacement is mechanical once named.

## 1. Running the dash ladder

Four dashes in one paragraph, each doing a different job. The rewrite runs the ladder from `SKILL.md` on each
aside in turn.

**Before:**

> The cache — which we added last spring — is the real bottleneck. Every read hits it first — even the ones we
> know will miss — and the lookup costs more than the fetch it was meant to avoid — a problem nobody noticed
> until the traffic doubled.

**After:**

> The cache is the real bottleneck. Every read hits it first, including the ones we know will miss, and the
> lookup costs more than the fetch it was meant to avoid. Nobody noticed until traffic doubled.

Aside by aside: step 1 cut "which we added last spring", which carried nothing. Step 3 turned the second aside
into a comma clause. Step 2 promoted the last aside to its own sentence, where it reads as the finding it
always was. Zero dashes remain, so the paragraph is under budget rather than at it.

Claim audit: all four claims survive — the cache is the bottleneck, every read hits it, the lookup costs more
than the fetch, nobody noticed until traffic doubled.

## 2. Naming the actor, without inventing one

**Before:**

> Over time the complaint becomes a fix, and the culture shifts toward ownership.

Nothing here names who did anything. Two rewrites are possible, and which one is correct depends entirely on
what the writer knows.

**When the writer has the history** and the draft merely omitted it:

> Priya filed the bug in March and the platform team shipped the fix in April. Two other teams copied the
> pattern that quarter.

Every name, date and count in that rewrite came from the writer, NOT from the original sentence.

**When the draft is all you have:**

> Someone filed the complaint and someone fixed it. This note does not record who, or whether anything changed
> afterwards.

**You MUST NOT supply an actor, a date or a number you do not have.** "Name the actor" is a retrieval
instruction, NEVER a licence to invent one. When the draft does not say who acted, ask the author, or state
the gap and drop the unsupported claim. A rewrite that reads better because it fabricated specifics has broken
the Iron Law in the worst available way: the prose now carries confident detail that nothing supports.

## Why this warning is here

Other AI-writing skills teach the opposite, and they teach it through their worked examples rather than their
rules, which is where a model actually learns the behaviour. Reviewed 2026-08-24, `jpeggdev/humanize-writing`
demonstrates its rewriting procedure on a passage about AI coding assistants and produces an "after"
containing two named interviewees with direct quotes, a "2024 study by Google" reporting 55% faster
completion, and a "2024 Uplevel study" reporting no significant difference. None of it appears in the
"before". Smaller instances run through the same skill's other passes: a rewrite gains a purpose clause the
original never stated, another gains "which is considered a delicacy".

The prose is better in every respect the rules measure, which is what makes the failure worth recording.
Specificity is the reward those rules optimise for, and fabricating it is the cheapest way to earn that
reward. **A rule that asks for concrete detail creates pressure to invent concrete detail.** Assume that
pressure applies to you, and check the source of every specific your rewrite gained.
