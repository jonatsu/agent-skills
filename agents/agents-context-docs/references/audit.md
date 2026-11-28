# Audit Repository Context

An audit determines whether the context system works for its intended clients and repository tasks. It does
not authorize edits.

## Establish the Audit Surface

Identify target clients, repository boundaries, root entrypoints, nested files, vendor-specific rules, symlink
targets, pointers, includes, and generated sections. Use live loaded-context inspection when available.
Otherwise reconstruct the candidate set and label the method and uncertainty.

Read [loading-model.md](loading-model.md) when client behavior affects a finding. Follow effective includes
and pointers far enough to assess the behavior under review. Do not make a focused audit pay for unrelated
complete-tree inspection.

For a ruleset that is rendered rather than read in place, the surface is the source it is written in plus
every output it renders to, and a finding must say which of the two it belongs to: a wording problem lives in
the source, a drift problem only appears in an output. Such a ruleset also makes behavioral claims rather than
claims about a repository, so most of it cannot be verified against a tree; assess it against whether a rule
changes what an agent does, and do not record a dimension as unassessed merely because no repository fact
backs it.

## Assess Separate Dimensions

Report each dimension independently when relevant:

- **Mechanical validity:** files parse where required, links and references resolve, and placeholders are
  absent. `../scripts/check-agent-context.py` covers evidence-link resolution, orphaned evidence, and size
  against budget; run it before assessing this dimension by hand.
- **Loading and topology:** intended clients receive the right effective context without conflicts, silent
  gaps, or unsupported assumptions.
- **Content quality:** instructions are verified, specific, actionable, non-duplicative, and
  behavior-changing, and each earns the cost of being loaded on every session rather than on demand. Count MCP
  tool descriptions and schema field descriptions a repository ships as always-loaded text too: every session
  using the server pays for them. Some clients never show a server's own instructions to the model, so a tool
  description that repeats them is not a duplicate.
- **Whole-ruleset coherence:** precedence, nested scope, examples, templates, and enforcement do not
  contradict the rules.
- **Maintenance safety:** generated boundaries and update practices preserve hand-written knowledge and avoid
  divergent copies.
- **Behavioral evidence:** realistic tasks show whether agents discover, follow, and benefit from the context
  at acceptable context and workflow cost.

Do not calculate a universal weighted total or letter grade. Use measurements only when they answer a
decision, such as unresolved links, effective lines, distinct rules, stale paths, duplicated content, or
observed task outcomes.

## Evidence and Findings

Verify command and path claims against authoritative repository sources. Label vendor-documentation claims,
controlled observations, user reports, and inferences distinctly. Name a dimension as unassessed in Scope when
required evidence is unavailable.

Report in these parts:

1. **Verdict:** `Ready`, `Ready after changes`, or `Not ready`, then one sentence on whether the context works
   for its clients, such as "Codex loads none of the root rules, because it reads no `CLAUDE.md` (F1)".
2. **Scope:** the target clients, the surface, the method behind each dimension (live inspection,
   reconstruction, a script run, or behavioral cases), and each dimension's result kept separate, with any
   unassessed dimension named.
3. **Findings**, tagged `F1`, `F2`, and so on, most consequential first. Each gives:
   - where it is, and for a rendered ruleset whether it lives in the source or in an output;
   - the dimension;
   - what is wrong and its consequence for the affected clients or tasks;
   - the evidence, with its label;
   - the tier; and
   - the smallest credible correction.
4. **Unverified:** inferences and claims the evidence cannot settle, each with the check that would.
5. **Next checks:** behavioral cases and script runs still to do, and the reviews to run next.
6. **What holds**, only when a rule or structure should survive the corrections: at most two sentences, with
   its location.

Give each finding one tier:

- **Must fix:** an agent acts wrongly. An effective rule reaches the wrong client or none, contradicts
  another, or grants autonomy for risky actions.
- **Should fix:** a cost or maintenance defect, such as duplication, accumulated narrative, copies prone to
  drift, or prose where a gate is needed.
- **Consider:** an optional improvement. Report at most five, and say how many you left out.

The verdict is `Ready` when no Must fix finding is open, `Ready after changes` when the corrections need no
restructuring, and `Not ready` when they do.

Always report as a finding, at the tier its consequence sets:

- an instruction file that has accumulated incident narrative, dated measurements, commit identifiers, or
  superseded-state history in place of imperative rules, and the always-loaded cost that imposes;
- a file that includes another, such as through an `@path` import, and also restates, summarizes, or points
  back to the content it includes, so every reader receives it twice;
- one rule stated several times with rising emphasis, which is one rule paying for many;
- divergent real files that different clients load;
- instructions placed at filenames or scopes no target client reads;
- contradictions among effective rules, examples, templates, or gates;
- required behavior expressed only as prose when deterministic enforcement is needed;
- autonomy grants, unconditional completion demands, or self-approved risky actions;
- generated or third-party text treated as adopted repository policy without evidence; and
- updates that remove non-obvious knowledge or make independently maintained copies drift-prone.

## Behavioral Evaluation

Use realistic tasks when document inspection cannot answer whether the system works. Valuable cases include
initialization for known clients, truthful degradation for an unfamiliar client, a focused update,
divergent-file recovery, and preservation of a non-obvious rule.

Record the request, inputs, client or model and version, date, observable success conditions, and result.
Compare with no skill or a prior version only when the comparison resolves a real uncertainty. Keep evaluation
artifacts outside the target repository unless the user requested them there.
