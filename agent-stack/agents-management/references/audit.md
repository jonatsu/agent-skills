# Audit Repository Context

An audit determines whether the context system works for its intended clients and repository tasks. It does not authorize
edits.

## Establish the Audit Surface

Identify target clients, repository boundaries, root entrypoints, nested files, vendor-specific rules, symlink targets,
pointers, includes, and generated sections. Use live loaded-context inspection when available. Otherwise reconstruct the
candidate set and label the method and uncertainty.

Read [loading-model.md](loading-model.md) when client behavior affects a finding. Follow effective includes and pointers
far enough to assess the behavior under review. Do not make a focused audit pay for unrelated complete-tree inspection.

## Assess Separate Dimensions

Report each dimension independently when relevant:

- **Mechanical validity:** files parse where required, links and references resolve, and placeholders are absent.
- **Loading and topology:** intended clients receive the right effective context without conflicts, silent gaps, or
  unsupported assumptions.
- **Content quality:** instructions are verified, specific, actionable, non-duplicative, and behavior-changing.
- **Whole-ruleset coherence:** precedence, nested scope, examples, templates, and enforcement do not contradict the rules.
- **Maintenance safety:** generated boundaries and update practices preserve hand-written knowledge and avoid divergent
  copies.
- **Behavioral evidence:** realistic tasks show whether agents discover, follow, and benefit from the context at acceptable
  context and workflow cost.

Do not calculate a universal weighted total or letter grade. Use measurements only when they answer a decision, such as
unresolved links, effective lines, distinct rules, stale paths, duplicated content, or observed task outcomes.

## Evidence and Findings

Verify command and path claims against authoritative repository sources. Label vendor-documentation claims, controlled
observations, user reports, and inferences distinctly. Mark a dimension unassessed when required evidence is unavailable.

Lead with findings by severity. For each finding, give the evidence, affected clients or tasks, consequence, and smallest
credible correction. Report strengths after risks so the preservation target remains visible.

Always flag:

- divergent real files that different clients load;
- instructions placed at filenames or scopes no target client reads;
- contradictions among effective rules, examples, templates, or gates;
- required behavior expressed only as prose when deterministic enforcement is needed;
- autonomy grants, unconditional completion demands, or self-approved risky actions;
- generated or third-party text treated as adopted repository policy without evidence; and
- updates that remove non-obvious knowledge or make independently maintained copies drift-prone.

## Behavioral Evaluation

Use realistic tasks when document inspection cannot answer whether the system works. Valuable cases include initialization
for known clients, truthful degradation for an unfamiliar client, a focused update, divergent-file recovery, and
preservation of a non-obvious rule.

Record the request, inputs, client or model and version, date, observable success conditions, and result. Compare with no
skill or a prior version only when the comparison resolves a real uncertainty. Keep evaluation artifacts outside the
target repository unless the user requested them there.
