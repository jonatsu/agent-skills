# Review Mode

Judge whether a skill reliably improves agent behavior for its intended job. Credit structure, length, polish,
and optional techniques only for the benefit they produce. Apply [rubric.md](rubric.md) for gates, tiers,
evidence classes, and verdicts.

## Contents

1. Establish the contract
2. Check the hard gates
3. Inspect the design
4. Choose the tier
5. Run full evaluation when authorized
6. Form findings
7. Deliver the verdict

## 1. Establish the Contract

Read the user's request and applicable repository instructions. Inventory the complete package. Read
`SKILL.md` and the instruction resources relevant to its contract, and inspect scripts, assets, binaries,
generated files, and large references at the depth the review requires.

Identify:

- the task the skill enables and representative requests;
- the single coherent job that owns its content, and why that job requires each additional subject, tool,
  language, workflow, or output;
- observable successful outcomes and consequential failures;
- intended invocation behavior;
- declared clients, models, tools, environments, and compatibility limits;
- portable or explicitly repository-specific scope;
- safety, authorization, licensing, and provenance obligations; and
- whether this is review lite or an authorized full evaluation.

Where the package leaves these implicit, infer only what the package and its environment support, and mark
consequential uncertainty rather than grading against an invented contract. Record unread files and
unavailable environments as coverage limits.

For a revision, identify the behavior that must stay stable and the corrections the user authorized. Inspect
available prior versions, cases, and execution evidence. The author's claims and cases are inputs to verify,
not the whole contract: derive obligations from the intended task, and name the consequential boundaries the
author's cases omit.

## 2. Check the Hard Gates

Run and report the [hard gates](rubric.md#hard-gates). A failed gate sets the verdict to `invalid`; continue the
design inspection only as far as it helps the repair.

## 3. Inspect the Design

Apply the four always-on lenses, then each other lens the package's content makes relevant:

- **Discovery:** the name and description pass the review checks of the `skill-descriptions-and-triggers`
  skill.
- **Scope coherence:** every aspect serves one coherent job under the rule in `SKILL.md`. Judge only the
  purpose the package establishes; an invented unifying purpose hides the defect.
- **Behavioral value:** each instruction earns its place through a decision, action, or necessary
  understanding. Shortness alone earns nothing.
- **Lean execution:** shared essentials stay available, and branch-specific instructions, modules, and data load
  only when selected work needs them. Apply this without waiting for a cost complaint.
- **Workflow fit:** sequences, branches, iteration, delegation, scripts, gates, and templates exist only where
  the task's dependencies or risks justify them. Workflows that change state, repeat operations, resume, or
  share state have a defined, enforced operational contract.
- **Clarity and completion:** requirements are distinguishable from recommendations, and consequential work
  has observable completion criteria.
- **Consistency:** metadata, instructions, references, scripts, examples, and the skill's own conduct agree.
- **Collection fit:** the skill does not duplicate a deployed neighbor, an always-loaded rule, or a
  repository-local skill in the consuming repository.
- **Recoverability and maintenance:** facts a reliable runtime source provides are pointed to, and every
  resource earns its context and maintenance cost.
- **Portability:** format, runtime, and client portability are assessed independently against the declared
  targets.
- **Provenance, evidence, and safety:** attribution is complete, claims rest on legible evidence, and the
  workflow keeps within the user's authority and reports failure truthfully.

Judge optional structures by their effect. A missing Iron Law, checklist, anti-pattern section, script,
reference, negative trigger, or strict template is a finding only when its absence causes a concrete problem.

Read [review-lenses.md](review-lenses.md) when a lens needs its diagnostic questions or when choosing a repair.

## 4. Choose the Tier

Perform review lite unless the user has authorized full evaluation. When the rubric's conditions for
recommending full evaluation hold, recommend it with the cost details the rubric lists, and continue with
review lite while the user decides.

## 5. Run Full Evaluation When Authorized

Read [full-evaluation.md](full-evaluation.md) before designing or running any part of it. Cover several
realistic prompts, several relevant models, or both, without growing every review into an exhaustive matrix.
Execution that changes external state, spends model allowance, or needs new authority waits for the user's
approval.

## 6. Form Findings

Report a finding only when evidence supports a behavioral consequence, a hard-gate failure, or a material
maintenance risk. Give each material finding:

- **severity:** blocker, high, medium, or low, ranked from consequence and likelihood rather than textual
  prominence;
- **confidence:** confirmed or suspected;
- **evidence:** a file and location, validator output, observed run, or authoritative source;
- **consequence:** the effect on discovery, execution, safety, portability, maintenance, or evidence;
- **repair:** the smallest correction that preserves working behavior; and
- **validation:** how to prove the repair worked.

Consolidate findings that share one root cause. Include only what helps the user decide or act: no generic
praise, repeated summaries, or narration of routine checks. Mention a strength only when a revision must
preserve it.

Leave the reviewed package unchanged until the user separately authorizes repair. An authorized repair
follows [authoring.md](authoring.md), preserves working behavior, and reruns the affected review tier.

## 7. Deliver the Verdict

Lead with material findings. Then report:

- **Verdict:** one of the rubric's four, with the unmeasured behavior named when it is `ready with risks`;
- **Validity:** each validator's result, kept separate;
- **Evidence:** evaluations performed, their baseline, coverage limits, and each item's evidence class;
- **Findings:** ordered by severity; and
- **Preserve:** effective design choices a repair must not regress, when any matter.
