# Review Lenses

Use these questions to investigate relevant risks, not as a checklist that every skill must satisfy. A missing
technique is a finding only when its absence harms the skill's declared job.

## Discovery

- Does the description state what the skill does and when it applies?
- Does each trigger phrase represent a distinct supported branch rather than a synonym quota?
- Could a nearby but unsupported request activate it? Would an intended request fail to activate it?
- Is routing information trapped in the body, where it arrives after activation?
- If invocation is explicitly user-only, is the human-facing description suitable for that mode?

Test discovery with realistic positive requests, near-miss negatives, and ambiguous cases when triggering
matters. Do not infer activation quality from keywords alone.

## Behavioral Value

Classify material qualitatively when that sharpens a recommendation:

- **Expert:** non-obvious decisions, tradeoffs, edge cases, or procedures the target agent lacks.
- **Activation:** known behavior the agent is liable to miss unless prompted.
- **Recoverable:** facts better obtained from a reliable authoritative source during execution.
- **Redundant:** material that does not change the target agent's behavior.

Keep expert material, make activation guidance brief, replace recoverable facts with pointers when the source
is reachable and accurate, and remove genuinely redundant content. Do not turn these classes into line-count
ratios. Whether guidance is a no-op depends on the target models and is best settled through behavior when
reviewers disagree.

## Information Hierarchy

- Is material needed by every execution available in `SKILL.md`?
- Is branch-specific detail behind a pointer that states when to read it?
- Can the agent reach every necessary resource before the decision it informs?
- Does splitting improve relevance, or merely scatter one cohesive procedure?
- Does any meaning appear in several places and risk inconsistent updates?

Neither file length nor resource count decides this. A short self-contained skill and a larger routed package
can both be correct.

## Workflow and Freedom

Calibrate freedom to fragility: open-ended judgment usually needs principles and decision criteria;
consequential or fragile operations may need exact sequences, validation, or deterministic scripts.

- Use ordered steps when later work depends on earlier results.
- Use branches when inputs, environment, or user choices select materially different paths.
- Use iteration when an observable criterion supports improvement.
- Use scripts when repeated, exact, or fragile operations benefit from deterministic execution.
- Use confirmation gates only for authority or information not already supplied.
- Use strict templates only when a consumer or formal process requires stable structure.

An Iron Law is useful only when one falsifiable absolute prevents the dominant failure and admits no
reasonable exception. Anti-patterns are useful only when they counter a likely or observed harmful default.
Checklists are useful only when they preserve order, prerequisites, or state across a long workflow.

## Practical Execution

Consider the existing review's three useful questions separately:

- **Acts now:** Can the agent execute without inventing a missing decision, input, or operation?
- **Acts safely:** Does it preserve authority, validate consequential output, and stop truthfully on unsafe
  conditions?
- **Still works elsewhere or later:** Are dependencies, paths, fallbacks, and changing empirical claims
  handled within the declared compatibility boundary?

Do not merge these into one usability score. A failure in one area needs its own consequence and repair.

## Completion and Failure

- Can the agent distinguish completion from partial progress for consequential steps?
- Do checks observe the result rather than request vague quality?
- Do anticipated failures produce enough information to recover or stop truthfully?
- Do fallbacks preserve the claimed outcome, or should they be reported as reduced capability?
- Do examples and scripts cover the difficult boundary rather than only the happy path?

## Consistency

Check relationships, not only isolated statements:

- assertion against assertion across files;
- a rule against its examples and templates;
- a command against the environment and prerequisites it claims;
- a countable package claim against the current package; and
- the skill's own conduct against the behavior it requires.

This cross-file pass catches defects that look correct in isolation. A contradiction is material when it
leaves the agent with competing actions or a false belief; cosmetic wording variation is not.

## Recoverability and Maintenance

Prefer authoritative runtime lookup for flags, schemas, versions, inventories, and other changing facts.
Preserve copied information when the source is unavailable during use, unreliable, or lacks the judgment the
skill must supply. Content that records where an apparent authority is wrong can be high-value expert
guidance. A pointer is an improvement only when its source is reachable and accurate.

Look for stale caches, duplicated meanings, orphaned resources, authoring-machine assumptions, unnecessary
dependencies, and instructions that no longer affect behavior. Recommend deletion only after identifying what
execution path, if any, still depends on the material.

## Portability and Scope

Assess two independent questions:

1. **Frontmatter portability:** Are fields valid under the Agent Skills specification? Are vendor extensions
   deliberate?
2. **Runtime portability:** Does the skill work within its declared tools, environment, and compatibility
   limits?

Portable is the default when no repository scope is declared. A portable skill may require a tool intrinsic to
its job, but should declare material requirements in `compatibility`, avoid authoring-machine paths and
repository-local commands, and report unavailable dependencies truthfully.

A repository-specific skill using `metadata.scope: repo-local` may rely on that repository's paths, commands,
and conventions. It should name the repository and still declare external environment requirements. Do not
infer repo-local scope merely because undeclared local bindings make that interpretation convenient.

A tool-subject skill may depend on its subject without pretending to be tool-agnostic. That exception does not
cover secondary tools, repository runners, or authoring-machine paths. Check each additional dependency
normally.

## Provenance, Evidence, and Safety

- Does original work identify its current author and applicable top-level license?
- Does derived work preserve attribution, pinned source identity, upstream license text, and any required
  notice?
- Are load-bearing empirical claims supported by an authoritative source or observed behavior?
- Is the evidence legible enough for another reviewer to audit? Diligence claimed without an artifact is not
  evidence.
- Does the skill remain within the user's task and authority?
- Are destructive, costly, sensitive, or outward-facing actions gated only when prior authorization is
  insufficient?
- Are validation failures and reduced-capability paths reported rather than presented as success?

Treat missing required provenance and unauthorized behavior as hard failures. Scale evidence demands to the
consequence and freshness of the claim rather than requiring citations on every sentence. Do not infer
authoring order from a finished package; consult history only when the order matters and the repository can
establish it.
