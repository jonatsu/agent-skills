---
name: writing-skill-descriptions
description: Write, audit, and test Agent Skill descriptions so a skill loads for the requests it serves and stays out of the rest. Use when drafting or revising a description, when a skill fails to trigger or triggers on the wrong requests, or when comparing description variants or measuring trigger rates. Use skill-forge for the rest of the skill package.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Skill Descriptions and Triggers

A description is a skill's routing pointer: it states the capability and the conditions for reaching the skill.
Write it so the skill triggers on the requests its body serves and on no others. Work from the skill's contract
and its intended invocation, not from a preferred sentence formula.

This skill covers a new skill's first description as well as revisions to an existing one. A review-only
request authorizes a proposed replacement, not edits.

## 1. Establish the Routing Contract

Read the target skill's body, its relevant bundled references, any current description, and the target
repository's instructions. Identify the concrete job, the distinct request branches the body supports, the
neighboring skills, and the consequential exclusions. Use real requests or observed missed and false triggers
when available; otherwise label the audit as heuristic.

When the complaint is that a skill never loads, first confirm that the target client can discover the installed
package. A missing or invalid package needs a packaging or deployment repair, not a longer description.

Settle two independent properties before drafting. When the skill is being authored, reuse the choices that
work already made.

1. **Scope:** Is the skill portable across environments, or bound to one repository? Follow the target
   repository's declared convention rather than treating a metadata field as a universal client control.
2. **Invocation goal:** Should the agent select it from a realistic user request, or should the user invoke it
   explicitly? Judge from the job and available evidence. When either goal is plausible and the choice would
   change routing, ask the user before drafting.

A portable skill can be opt-in, and a repository-specific skill can be agent-selected. When the behavior applies
at a moment users never express as a request, report that discovery limit rather than promising a description
repair.

## 2. Draft the Description

Build the description from these steps:

1. State the capability in concrete terms.
2. When it names a specialized tool, product, or artifact, add the plain context that makes routing accurate:
   the capability and the user intent the name stands for. Leave out concepts the agent already knows.
3. List the distinct request branches the body supports, and write each one once in words a user is likely to
   use, including requests that do not name the skill or its tool. Put the most important trigger first.
4. Add an exclusion only for a nearby skill or task that could plausibly be misrouted.
5. Remove implementation detail and instructions that matter only after the skill loads. Leave out any summary
   of the skill's workflow: an agent that finds the steps in the description can follow them from there and
   skip the body, including every step the summary left out.

Claim only branches the body supports. When a request needs a branch the body lacks, narrow the description or
raise the skill-design question. Synonyms for one branch are one branch; long lists blur boundaries and attract
false triggers. Imperative wording such as `Use when` can help an agent recognize a condition, but its absence
alone is not a defect.

Then fit the draft to its scope and invocation goal:

- **Portable:** describe reusable user tasks without relying on the authoring repository, local paths, installed
  tools, configuration, or client. A tool intrinsic to the job may be named to explain the capability; the
  skill itself declares and checks that requirement.
- **Repository-specific:** name the repository and its bounded task when that helps selection. Use local
  artifact names or paths only when they distinguish a request the skill handles; a file being present or
  modified is not evidence that the user wants the skill's workflow.
- **Agent-selected:** a request phrased by its outcome, without the skill's name, should still match.
- **Explicit-only:** describe the opt-in job without cues from surrounding work. Wording expresses intent but
  does not enforce it, so verify the client's explicit-only mechanism before claiming the skill cannot be
  selected automatically.

```yaml
# Too vague
description: Helps with PDFs.

# Too broad
description: Creates, reads, writes, edits, changes, fixes, processes, analyzes, and manages documents and files.

# Discriminating
description: Extract PDF text and tables, fill forms, and merge files. Use for extraction, forms, or assembly.

# Assumes the router already knows the tool
description: Build and maintain justfiles.

# Carries the capability and the user intent
description: Build and maintain Just command-runner files for repeatable project tasks.
```

## 3. Fit the Form and Length

Follow the target repository's scalar convention. An inline value on one physical line is the safe default;
some deployment tooling mishandles folded (`>-`) and literal (`|`) block scalars.

Budget the description by characters, not by line width. It cannot wrap while it stays an inline scalar, and
Markdown linters commonly skip frontmatter, so a column ceiling does not govern it. The Agent Skills
[specification](https://agentskills.io/specification) caps a description at 1024 characters, and a repository
may set a tighter budget. Where a client preloads every description, the whole collection pays that cost on
every request, so spend it on distinct branches and necessary exclusions.

## 4. Review the Candidate

Check the candidate against each of these, and compare it with the current description when one exists:

- It names both the capability and the conditions that trigger it.
- Every trigger phrase maps to a distinct branch the body supports.
- A representative unrelated request, and each close neighbor's typical request, does not appear to match.
- Specialized names carry enough context for routing, without unneeded definitions.
- No routing guidance is left in the body, where it arrives too late to affect triggering.
- Every declared client has a verified automatic or explicit path for the intended use.
- It meets the specification and any tighter repository form or length policy.

Explain each material change through a supported branch, a realistic missed request, or a close false trigger,
and keep wording that already works. Static checks are validity and design evidence, not proof of triggering.

For a review-only request, deliver the exact proposed description and its reasons. When edits are authorized,
change only the description and required routing metadata, run the target repository's validators, review the
diff, and deploy through its normal procedure. Keep unrelated package changes in a separate change.

## 5. Measure Triggers When Authorized

Model runs cost time and allowance. Offer a bounded trigger evaluation when static review leaves a
consequential routing question, and run it only with authorization for that cost and any client side effects.
Follow the [Agent Skills trigger-evaluation method](https://agentskills.io/skill-creation/optimizing-descriptions):
use realistic should-trigger requests and close should-not-trigger cases, keep validation queries separate from
revisions, and compare the current and candidate descriptions under the same client conditions.

Write each should-trigger query as a concrete, substantive request with the detail a real user supplies: the
files, the context, and the outcome wanted. An agent consults a skill only when the task needs one, so a
trivial one-step request may load no skill at all and says nothing about the description. Write each
should-not-trigger query as a near miss that shares vocabulary or artifacts with the skill but needs another
capability, since an obviously unrelated query passes every description.

Run each query several times, because the same query can trigger on one run and not the next. Set the
repetition count and the trigger-rate threshold before the runs; three runs with a threshold of 0.5 is a
workable default. Keep the held-out queries and their scores away from whoever writes the next candidate,
person or model. A writer who sees them tunes toward those queries, and the held-out score then stops
measuring whether the description generalizes. Select the candidate by its held-out score, finish with fresh
queries, and never copy a query's wording into the description to make it pass.

Verify how the client exposes skill loading before treating its logs as evidence. When loading is not
observable, report the measurement as inconclusive or use a separately justified behavioral probe; a missing log
entry alone does not show the skill failed to trigger. Report results per client, the cases and repetitions
run, and the routing behavior that remains untested.
