# Review Lenses

Diagnostic questions for the lenses in [review.md](review.md). Use them to investigate relevant risks. A
missing technique is a finding only when its absence harms the skill's declared job.

## Contents

- Discovery
- Scope coherence
- Behavioral value
- Collection fit
- Lean execution and information hierarchy
- Workflow fit and operational guarantees
- Practical execution
- Completion and failure
- Consistency
- Recoverability and maintenance
- Portability and scope
- Provenance, evidence, and safety
- Choosing the repair

## Discovery

Judge the name and description with the review checks of the `writing-skill-descriptions` skill. Read the
scalar form directly: a folded or literal block scalar passes the reference validator and Markdown linters
alike.

When triggering matters, prepare discovery cases as [testing-guide.md](testing-guide.md) describes, and run
them only in an authorized full evaluation. Keywords alone say nothing about how reliably a skill triggers.

## Scope Coherence

Inventory each subject, tool, language, workflow, and output, then find the shared task or decision boundary
the package establishes for them. One workflow whose safe execution crosses those boundaries is a deliberate
relationship. Unrelated guidance is a material defect that makes the skill `not ready`; recommend splitting
or removing it.

## Behavioral Value

Classify material qualitatively when that sharpens a recommendation:

- **Expert:** non-obvious decisions, tradeoffs, edge cases, or procedures the target agent lacks.
- **Activation:** known behavior the agent is liable to miss unless prompted.
- **Recoverable:** facts better obtained from a reliable authoritative source during execution.
- **Redundant:** material that does not change the target agent's behavior.

Keep expert material and useful reminders. Replace recoverable facts with pointers when the source is
reachable and accurate. Apply the deletion test: would removing a passage weaken correct execution,
understanding, or recovery? If not, recommend its removal, naming the passage and why it adds no useful
meaning. Where value depends on untested model behavior, state the uncertainty.

Check shortening proposals for lost conditions, exceptions, ordering, evidence requirements, and recovery
behavior. Flag cryptic wording that forces the agent to reconstruct a consequential distinction. A reminder
that prevents a specific likely failure may be useful; repetition that only adds emphasis is expendable. Judge
by these questions rather than by word counts or compression ratios, which cannot see a lost condition.

Weigh the useful outcome against the cost the skill induces: context, reasoning, tool calls, latency,
distraction, and maintenance. Size and complexity are screening signals for that weighing, not grounds for
removing a specific instruction without examining its purpose.

## Collection Fit

A sound standalone skill can still duplicate a neighbor, contradict a global rule, or activate in place of a
better neighbor.

- Does another deployed skill already own this job, or a large part of it?
- Does the description overlap a neighbor's trigger surface so that selection becomes arbitrary?
- Does the guidance repeat, or conflict with, an always-loaded rule the agent already follows?
- Does a repository-local skill in the consuming repository already cover the subject against its actual code?
  A globally deployed copy then costs discovery budget in every session for no reader.

Deliberate overlap with its boundary stated where an agent reads it is acceptable. Duplication with two homes
that can drift apart is a finding.

## Lean Execution and Information Hierarchy

- Is material needed by every execution available in `SKILL.md`?
- Is branch-specific detail behind a pointer that states when to read it?
- Can the agent reach every necessary resource before the decision it informs?
- Does splitting improve relevance, or merely scatter one cohesive procedure?
- Does any meaning appear in several places and risk inconsistent updates?

Trace representative paths through instructions, executable modules, and external records separately. For each
path, state what it needs, when it needs it, and whether unrelated work happens before selection. Look for
unconditional reference reads, unnecessary module initialization, and detailed retrieval where summaries
suffice. Name the affected path and recommend the smallest correction.

Distinguish intended loading from observed loading. Verify boundaries with available traces and deterministic
checks for imports or external calls where practical. File separation and valid links prove organization and
reachability, not selective loading, and absent telemetry does not prove waste. Treat actual model-context
loading as unmeasured unless the client exposes trustworthy evidence; a walkthrough does not authorize a model
run to obtain it.

Quantitative budgets belong where they enforce a justified boundary or detect regressions. Lean execution is
required with or without one. A small, self-contained skill may meet the criterion without extra machinery.

## Workflow Fit and Operational Guarantees

Judge each control-flow structure against the condition that justifies it in
[workflow-patterns.md](workflow-patterns.md), and each Iron Law, question, anti-pattern, or guidance form
against [writing-techniques.md](writing-techniques.md). Freedom should follow fragility: open-ended judgment
needs principles and criteria, and fragile operations need exact sequences, validation, or scripts.

For workflows that change state, repeat operations, resume later, or share mutable state, check the author's
contract against the six questions in [operational-workflows.md](operational-workflows.md) and against the
implementation and verified tool contracts. Statements such as "retry safely" or "verify success" fail when
the caller must invent how.

Trace a successful operation, an interruption after a consequential effect, and continuation against changed
state where they apply. For state-changing scripts, check whether callers can recognize completed work,
distinguish partial or unknown outcomes, keep the identities they need, and tell whether retry is safe.
Review-lite traces stay heuristic unless safe execution evidence exists, and they never authorize external
writes.

Separate demonstrated failures, design omissions, and missing execution evidence, each with its concrete
consequence. Require a phase framework, checkpoint schema, or recovery machinery only where the task needs one.

## Practical Execution

Ask three questions separately, because a failure in one needs its own consequence and repair:

- **Acts now:** can the agent execute without inventing a missing decision, input, or operation?
- **Acts safely:** does it preserve authority, validate consequential output, and stop truthfully on unsafe
  conditions?
- **Still works elsewhere or later:** are dependencies, paths, fallbacks, and changing empirical claims handled
  within the declared compatibility boundary?

## Completion and Failure

- Can the agent distinguish completion from partial progress for consequential steps?
- Do checks observe the result rather than request vague quality?
- Do anticipated failures produce enough information to recover or stop truthfully?
- Do fallbacks preserve the claimed outcome, or should they be reported as reduced capability?
- Do examples and scripts cover the difficult boundary rather than only the happy path?

## Consistency

Check relationships across files, since these defects look correct in isolation:

- assertion against assertion;
- a rule against its examples and templates;
- a command against the environment and prerequisites it claims;
- a countable package claim against the current package; and
- the skill's own conduct against the behavior it requires.

A contradiction is material when it leaves the agent with competing actions or a false belief; cosmetic
wording variation is not.

For revisions, compare changed behavior against the preservation requirements. Separate authorized corrections
from unintended regressions, check that changes to tests or expected results have independent justification,
and add counterexamples where the requirements expose gaps in the supplied cases.

Keep the review proportional: independence does not require duplicating adequate checks or launching another
agent.

## Recoverability and Maintenance

Prefer authoritative runtime lookup for flags, schemas, versions, inventories, and other changing facts. Keep
copied information when the source is unavailable during use, unreliable, or lacks the judgment the skill must
supply. Content that records where an apparent authority is wrong can be high-value expert guidance.

Look for stale caches, unexplained version pins, duplicated meanings, orphaned resources, authoring-machine
assumptions, unnecessary dependencies, and instructions that no longer affect behavior. Recommend deletion only
after identifying what execution path, if any, still depends on the material.

Bundled scripts follow their language's conventions and pass its standard checks. A departure is a finding only
when it causes a concrete problem, or when the self-contained constraint does not explain it.

## Portability and Scope

Judge format, runtime, and client portability against [portability.md](portability.md), which owns the
authoring rules, including the standalone-script requirement. Read every bundled script and ask what it would
do on a machine that has never seen the authoring repository. A script that runs only under its author's
checkout is a portability defect however portable the prose is, and it passes every check until someone else
installs the skill.

Infer repo-local scope only from declared `metadata.scope: repo-local`, never because undeclared local
bindings make that reading convenient. Inside a repo-local skill, report avoidable environment coupling as a
lower-severity finding rather than exempting it, since the repository's own layout and runner also move.

A tool-subject skill may depend on its subject without pretending to be tool-agnostic. That exception does not
cover secondary tools, repository runners, or authoring-machine paths; check each of those normally.

## Provenance, Evidence, and Safety

- Does original work identify its current author and applicable top-level license?
- Does each source match its required record in [provenance.md](provenance.md), including pinned identity,
  upstream license text, and any required notice?
- Are load-bearing empirical claims supported by an authoritative source or observed behavior?
- Is the evidence legible enough for another reviewer to audit? Diligence claimed without an artifact is not
  evidence.
- Does the skill stay within the user's task and authority?
- Are destructive, costly, sensitive, or outward-facing actions gated only where prior authorization falls
  short?
- Are validation failures and reduced-capability paths reported rather than presented as success?

Scale evidence demands to the consequence and freshness of the claim rather than requiring citations on every
sentence.

Verify which revision, inputs, environment, and behavior each artifact covers. When prior evidence is
unavailable, state the limitation and its consequence; missing evidence neither proves a regression nor
licenses an invented baseline.

When the verdict depends on whether tests or preservation evidence existed before a change, verify that order
from reliable version history or execution records. A finished package alone cannot establish when its contents
were created, so report an unsupported sequence as unverified.

Keep observed behavior, textual evidence, inference, and project preference distinct in the report. Predicted
behavior is not a measurement.

## Choosing the Repair

Match the repair to what the material is failing at:

- **Removal** for guidance whose marginal value does not cover its cost.
- **Revision** for guidance that is useful but unclear, unscoped, or wrongly placed.
- **Narrower loading** for specialized material that only some executions need.
- **Deterministic enforcement**, a script or a gate, for a mechanically decidable requirement whose failure is
  unacceptable.

Every repair preserves the skill's intended outcome, authority boundaries, safety constraints, triggers,
exceptions, and completion conditions. A simplification that drops one of those is a regression.
