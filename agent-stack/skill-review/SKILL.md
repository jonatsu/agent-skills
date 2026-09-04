---
name: skill-review
description: Review Agent Skills for defects and readiness. Use when reviewing, comparing, or repairing a skill.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Skill Review

Review whether a skill reliably improves agent behavior for its intended job. Do not reward visible structure,
length, polish, or optional techniques unless they produce a relevant benefit.

Keep three judgments separate:

1. **Validity:** Does the package satisfy its specification and applicable repository policy?
2. **Design:** Does its content plausibly guide the intended behavior without creating material risks or
   waste?
3. **Evidence:** What observed behavior supports or contradicts those claims?

A valid package can still be ineffective. A strong static design can still lack behavioral evidence. Do not
combine these into an aggregate score that hides the distinction.

## Review Workflow

### 1. Establish the Contract

Read the user's request, the complete skill package, and applicable repository instructions. Identify:

- the task the skill enables and representative requests;
- the single coherent job that owns the skill's content;
- every additional subject, tool, language, workflow, or output and why that job requires it;
- observable successful outcomes and consequential failures;
- intended invocation behavior;
- declared clients, models, tools, environments, and compatibility limits;
- portable or explicitly repository-specific scope;
- safety, authorization, licensing, and provenance obligations; and
- whether the review includes execution or is limited to static evidence.

If these are not explicit, infer only what the package and its environment support. Mark consequential
uncertainty rather than grading against an invented contract. Record unread files or unavailable environments
as coverage limits.

### 2. Check Hard Requirements

Use the Agent Skills specification as the authority for package structure and frontmatter. Run its reference
validator when one is available. Run applicable repository-policy validation separately.

Treat these as pass/fail gates, not quality points:

- specification violations;
- repository-policy violations;
- missing or inaccurate required license and provenance material;
- broken resource links, unusable scripts, or unfinished scaffold content;
- material contradictions that leave no reliable execution path; and
- unsafe behavior or side effects beyond the user's authority.

Report the exact validator and result. A substitute validator is not equivalent to the specification
validator. Do not let a passing structural check imply behavioral quality.

### 3. Inspect Design

Always inspect discovery and scope coherence. Review the other lenses relevant to the skill:

- **Discovery:** The name and description communicate the capability, user intent, distinct trigger branches,
  and likely boundaries. When they name a specialized tool, product, or artifact, they provide enough plain
  context for accurate activation instead of relying on the name alone. They need not define concepts the
  target agent can reasonably be expected to know.
- **Scope coherence:** Every aspect serves one coherent job. Multiple aspects pass only when the package
  establishes a deliberate shared task or decision boundary that requires them together. Shared popularity,
  one author's environment, possible integration, or occasional co-use is insufficient. Do not invent a
  unifying purpose that the package does not establish.
- **Behavioral value:** Instructions add decisions, knowledge, or reliable operations the agent would
  otherwise miss.
- **Information hierarchy:** Shared essentials stay available; branch-specific detail is reachable where
  needed.
- **Workflow fit:** Sequences, branches, iteration, delegation, scripts, gates, and templates exist only where
  the task's dependencies or risks justify them.
- **Clarity and completion:** Requirements are distinguishable from recommendations, and consequential work
  has observable completion criteria.
- **Consistency:** Metadata, instructions, references, scripts, examples, and the skill's own conduct agree.
- **Collection fit:** The skill does not duplicate a deployed neighbor, an always-loaded rule, or a
  repository-local skill in the repository that consumes it.
- **Recoverability:** Facts available from a reliable runtime source are pointed to rather than copied, unless
  that source is unavailable, unreliable, or omits necessary judgment.
- **Portability:** Frontmatter portability and runtime portability are assessed independently against the
  declared scope.
- **Safety and authority:** The workflow preserves user intent, scope, confirmation boundaries, and truthful
  failure reporting.
- **Maintenance:** Every resource earns its context and maintenance cost; duplication and fragile assumptions
  are absent.

Optional structures are never requirements by themselves. Do not penalize a skill for lacking an Iron Law,
checklist, anti-pattern section, script, reference, negative trigger, or strict template unless the absence
causes a concrete problem.

Read [references/review-lenses.md](references/review-lenses.md) when a lens needs detailed diagnostic
questions or when checking consistency with `skill-forge` conventions.

### 4. Evaluate Behavior When Warranted

Static review identifies plausible effects; it does not prove them. Recommend or run behavioral evaluation for
new skills, substantial rewrites, unreliable discovery, recurring execution failures, or uncertain
context-cost tradeoffs. For a focused change, test the changed behavior and nearby regressions.

Use realistic isolated requests and observable success conditions. Compare against no skill or the previous
version when the comparison would answer whether the skill adds value. Cover different clients or model
classes only when their differences could materially affect the result.

Read [references/behavioral-evaluation.md](references/behavioral-evaluation.md) when designing, running, or
interpreting an evaluation. Execution that changes external state, incurs material cost, or needs additional
authority still requires the user's approval.

### 5. Form Findings

Report a finding only when evidence supports a behavioral consequence, hard requirement, or material
maintenance risk. For each material finding include:

- **severity:** blocker, high, medium, or low;
- **confidence:** confirmed or suspected;
- **evidence:** a file and location, validator output, observed run, or authoritative source;
- **consequence:** the effect on discovery, execution, safety, portability, maintenance, or evidence;
- **repair:** the smallest correction that preserves working behavior; and
- **validation:** how to prove the repair worked.

Rank severity from consequence and likelihood, not textual prominence. Avoid duplicate findings for one root
cause. Mention strengths only when they identify behavior worth preserving during revision.

### 6. Deliver the Verdict

Lead with material findings. Then report:

- **Verdict:** `invalid`, `not ready`, `ready with risks`, or `ready`;
- **Validity:** specification and repository-policy results, kept separate;
- **Evidence:** evaluations performed, their comparison baseline, and coverage limits;
- **Findings:** ordered by severity; and
- **Preserve:** effective design choices that a repair should not regress, when any matter.

Use `invalid` for a failed hard requirement, `not ready` for a material behavioral or safety defect,
`ready with risks` for bounded weaknesses that do not defeat the intended job, and `ready` only when available
evidence supports that job.

A skill with unjustified scope mixing is `not ready`. A description that relies on an unexplained specialized
name without communicating the underlying capability or user intent is a high-severity discovery defect and
makes the skill `not ready`.

Do not assign a numeric score unless the user needs one for a stated decision. If requested, define a
task-specific rubric from the contract, keep hard gates outside it, show raw observations, and label
judgment-based weights as subjective. Never reuse a universal weighted total across unlike skills.
