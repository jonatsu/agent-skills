---
name: optimizing-descriptions
description: Audit and improve Agent Skill descriptions for accurate selection. Use when a user asks to review existing SKILL.md descriptions, diagnose missed or false activation, or compare description variants. Not for routine skill authoring.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Optimizing Skill Descriptions

Improve how an existing skill reaches the requests it can serve, without making it claim work its body does
not support. A description is a routing pointer: it states the capability and the conditions for reaching the
skill. Work from the target skill's contract and the user's desired invocation behavior, not from a preferred
sentence formula.

This skill handles focused description audits and revisions. Initial description writing belongs with
authoring the whole skill. A description review alone authorizes a proposed replacement, not edits.

## Establish the Routing Contract

Read the target skill's description, body, relevant bundled references, and the target repository's
instructions. Identify the concrete job, supported request branches, neighboring skills, and consequential
exclusions. Use real requests or observed missed and false activations when available; otherwise label the
audit as heuristic.

If the complaint is that a skill never loads, confirm that the target client can discover the installed
package before attributing the failure to wording. A missing or invalid package needs a packaging or
deployment repair, not a longer description.

Determine two independent properties before drafting:

1. **Scope:** Is the target skill portable across environments, or bound to one repository? Follow the target
   repository's declared convention rather than treating a metadata field as a universal client control.
2. **Invocation goal:** Should the agent select it from a realistic user request, or should it be invoked only
   through an explicit user action? Judge from the job and available evidence. If either goal is plausible and
   the choice would change routing, ask the user which behavior they want before rewriting.

These properties do not imply each other. A portable skill can be opt-in, and a repository-specific skill can
be selected from a request. If the behavior applies at a moment users do not express as an intent, identify
that discovery limit instead of promising a description repair.

## Draft for Scope and Invocation

For a **portable target**, describe reusable user tasks without relying on its authoring repository, local
paths, installed tools, configuration, client, or any other surrounding environment. A tool intrinsic to the
job may be named to explain the capability, but its presence is not assumed: the skill declares material
requirements and checks them when used. Keep environment setup and execution detail out of the description.

For a **repository-specific target**, name the repository and its bounded task when that helps selection.
Use local artifact names or paths only when they distinguish a request the skill actually handles. The mere
presence or modification of a file is not evidence that the user wants the skill's workflow.

For **agent selection from a request**, cover each distinct supported branch once in words a user might use,
including outcomes that do not name the skill or tool. Put the most important trigger early. Add nearby
exclusions only when they prevent plausible misrouting; avoid lists of synonyms and unrelated symptoms.

For **explicit-only use**, describe the requested opt-in job without ambient triggers. Wording can express
intent, but it does not enforce an invocation rule. Check whether the target client has an actual explicit-only
mechanism before claiming that the skill cannot be selected automatically.

Do not add a capability to the description just to improve matching. If the body does not support a claimed
branch, narrow the description or surface the larger skill-design decision. Imperative wording such as
`Use when` can help, but its absence alone is not a defect.

## Review the Candidate

Compare the candidate with the current description and explain each material change through a supported
branch, a realistic missed request, or a close false-trigger request. Preserve effective wording. Check that
the candidate communicates both what the skill does and when to use it, stays within the Agent Skills
[description limit](https://agentskills.io/specification), and follows any tighter repository form or length
policy. Treat static checks as validity and design evidence, not proof of activation.

For a review-only request, deliver the exact proposed description and its reasons without editing. When edits
are authorized, change only the description and required routing metadata. Apply the target repository's
validators, review the diff, and use its normal deployment procedure. Keep unrelated package changes separate.

## Measure Activation When Authorized

Model runs consume time and allowance. Offer a bounded trigger evaluation when static review leaves a
consequential routing question; run it only with authorization for that cost and any client side effects.
Follow the [Agent Skills trigger-evaluation method](https://agentskills.io/skill-creation/optimizing-descriptions):
use realistic should-trigger requests and close should-not-trigger cases, keep validation queries separate
from revisions, and compare current and candidate descriptions under the same client conditions.

Verify how that client exposes skill loading before using its logs as evidence. If loading is not observable,
report the measurement as inconclusive or use a separately justified behavioral probe; absence of a log entry
alone does not prove non-activation. Report per-client results, the cases and repetitions run, and the
remaining untested routing behavior. Do not claim that a passing validator or deployment proves discovery.
