# Review Sequence for High-Stakes Documents

Read this before reviewing a design, specification, or reference that others will build on. Read it also before
delegating any review or readability pass to a subagent.

## The Sequence

1. **Correct the facts against the source.** A source-check pass compares every claim about an upstream
   mechanism with the pinned source and writes a working note citing each location as `repository@commit:path:line`.
   Spot-check its most consequential claims yourself before relaying or applying them.
2. **Review the structure and design.** Use an architecture review, and a security review for a security design.
   Apply the findings.
3. **Re-review once, focused on what changed.** Then apply the design bar that `technical-design` sets: a first-time
   reader could re-derive the implementation from the documents alone. Delete the working note once nothing in it is
   still needed.
4. **Run a readability pass on a draft copy.** The pass applies this skill's understandable prose rules and
   **reader-ready** pass, plus `writing-for-humans`' own reader-ready pass, and writes a revised copy to
   a separate draft file rather than the tracked document. Read the word diff against the guidelines yourself.
   Correct what the pass got wrong, and commit the result as its own change.

Diff the draft against the right base. When the tracked file already carries staged or uncommitted changes, a
diff against the last commit mixes them into the pass's own edits. A mechanical pass with an explicit "no content
change" rule, such as splitting semicolon chains, may edit the tracked file directly. It needs no draft copy.

## What a Delegated Pass Needs in Its Prompt

A subagent inherits none of the conversation. Its prompt carries:

- the full writing guidelines it applies, not a summary;
- the pinned source locations it may check facts against;
- the passages the user has approved, which it must leave unchanged;
- the path of the draft or report file it writes; and
- the rule to report a place where it cannot derive a concept's purpose, rather than inventing one.

Give it these rules as well:

- **Never merge sentences.** Split a long sentence instead. A shortening pass that merges sentences into
  semicolon chains makes the text denser, the opposite of its goal.
- **Leave approved wording alone,** even where a shorter phrasing exists.
- **Check each replacement, not only the defect it fixes.** A rewrite of a key-first opener can arrive in the
  passive.
- **Reject a damaged copy whole.** A pass told to rewrite while preserving content can return a near-verbatim copy
  whose only changes are damage, such as line continuations stripped from code. Dispatch it again with a
  before-and-after example rather than patching its output.

## Verify What a Pass Adds

Fact-check every explanation a pass adds. Passes asked to explain concepts have written plausible wrong facts.
Examples include placing a userspace daemon in the kernel and describing a hash tree as covering each image when
it covers the whole payload. The draft-copy workflow makes this check cheap, because every addition appears in the diff.
When a pass must leave code untouched, prove every code block unchanged with `markdown-tools`.

Keep parallel passes on disjoint files. Keep a concurrent formatter or pre-commit run away from files a pass
is editing.
