---
name: skill-review
description: "Review Agent Skills for defects and readiness. Use for review lite, comparative behavioral evaluation, discovery diagnosis, or assessing a skill before an authorized repair. Not for creating a new skill or editing one during a review-only request."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Skill Review

Review whether a skill reliably improves agent behavior for its intended job. Do not reward visible structure,
length, polish, or optional techniques unless they produce a relevant benefit.

Use two review tiers:

1. **Review lite is the default.** Inspect heuristically and run mechanical checks. Do not start subagents or
   model evaluations.
2. **Full evaluation is optional and strongly recommended.** Run controlled behavioral comparisons when the
   user authorizes their time, model allowance, and side effects.

Without full evaluation, report at most `ready with risks`. This status permits provisional use while behavior
remains unproven. Only full evaluation can support `ready`.

Keep three judgments separate:

1. **Validity:** Does the package satisfy its specification and applicable repository policy?
2. **Design:** Does its content plausibly guide the intended behavior without creating material risks or
   waste?
3. **Evidence:** What observed behavior supports or contradicts those claims?

A valid package can still be ineffective. A strong static design can still lack behavioral evidence. Do not
combine these into an aggregate score that hides the distinction.

## Review Workflow

### 1. Establish the Contract

Read the user's request and applicable repository instructions. Inventory the complete package. Read
`SKILL.md` and instruction resources relevant to its contract. Inspect scripts, assets, binaries, generated
files, and large references at the depth the review requires.

Identify:

- the task the skill enables and representative requests;
- the single coherent job that owns the skill's content;
- every additional subject, tool, language, workflow, or output and why that job requires it;
- observable successful outcomes and consequential failures;
- intended invocation behavior;
- declared clients, models, tools, environments, and compatibility limits;
- portable or explicitly repository-specific scope;
- safety, authorization, licensing, and provenance obligations; and
- whether the review is review lite or an authorized full evaluation.

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
- **Portability:** Format, runtime, and client portability are assessed independently against the declared
  targets.
- **Safety and authority:** The workflow preserves user intent, scope, confirmation boundaries, and truthful
  failure reporting.
- **Maintenance:** Every resource earns its context and maintenance cost; duplication and fragile assumptions
  are absent.

Optional structures are never requirements by themselves. Do not penalize a skill for lacking an Iron Law,
checklist, anti-pattern section, script, reference, negative trigger, or strict template unless the absence
causes a concrete problem.

Read [references/review-lenses.md](references/review-lenses.md) when a lens needs detailed diagnostic
questions or when checking consistency with applicable authoring conventions.

### 4. Choose the Review Tier

Perform review lite unless the user authorizes full evaluation. Review lite combines contract inspection,
relevant design lenses, package consistency, and mechanical validation. It starts no subagents or model runs.

Strongly recommend full evaluation for new skills, substantial rewrites, cross-client claims, unreliable
discovery, recurring failures, or uncertain context cost. State the likely case count, clients, repetitions,
time, allowance, side effects, and evidence gain before requesting authority.

The user may defer full evaluation. When review lite finds no material defect, return `ready with risks` for
provisional use. Preserve observed real-use failures and corrections as cases for later evaluation.

### 5. Run Full Evaluation When Authorized

Read [references/behavioral-evaluation.md](references/behavioral-evaluation.md) before designing or running the
full process. Use realistic isolated requests and observable outcomes. Select baselines, clients, and models
from the decision rather than a fixed matrix.

Cover multiple realistic prompts, multiple relevant models, or both. Use enough variation to test the intended
job without turning every review into an exhaustive matrix.

Preflight the harness before any model call. Keep candidate, fixture, harness, dependency, permission, and
inconclusive failures distinct. Execution that changes external state, consumes model allowance, or needs
additional authority requires the user's approval.

### 6. Form Findings

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

Do not edit the reviewed package unless the user separately authorizes repair. When repair is authorized,
preserve working behavior and rerun the affected review tier.

### 7. Deliver the Verdict

Lead with material findings. Then report:

- **Verdict:** `invalid`, `not ready`, `ready with risks`, or `ready`;
- **Validity:** specification and repository-policy results, kept separate;
- **Evidence:** evaluations performed, their comparison baseline, and coverage limits;
- **Findings:** ordered by severity; and
- **Preserve:** effective design choices that a repair should not regress, when any matter.

Use `invalid` for a failed hard requirement and `not ready` for a material design, behavioral, or safety defect.
Use `ready with risks` when review lite finds no material defect or when full evaluation leaves bounded risks.
Use `ready` only when full evaluation supports the intended job without a material unresolved risk.

A skill with unjustified scope mixing is `not ready`. A description that relies on an unexplained specialized
name without communicating the underlying capability or user intent is a high-severity discovery defect and
makes the skill `not ready`.

Do not assign a numeric score unless the user needs one for a stated decision. If requested, define a
task-specific rubric from the contract, keep hard gates outside it, show raw observations, and label
judgment-based weights as subjective. Never reuse a universal weighted total across unlike skills.
