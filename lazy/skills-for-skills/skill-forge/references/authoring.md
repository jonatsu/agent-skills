# Authoring Mode

Create or update the smallest skill that reliably changes agent behavior for the requested task. Deliver a
reviewable candidate with author-side evidence and a closing review lite.

## Contents

1. Establish the job
2. Choose scope, invocation, and clients
3. Preserve provenance
4. Design the package
5. Write for reliable behavior
6. Preflight and review the draft
7. Finish and hand off

## 1. Establish the Job

When updating a skill, inventory the complete package before editing. Read `SKILL.md` and the instruction
resources the change affects. Inspect scripts, assets, binaries, generated files, and large references at the
depth the change requires.

Before substantially changing an existing workflow, record the externally visible behavior that must stay
stable: representative inputs, expected outcomes, known failure behavior, and available execution evidence.
Separate requirements being preserved from defects the requested change should correct.

Establish:

- the concrete task the skill enables;
- representative requests and successful outcomes;
- the decisions or knowledge a capable agent lacks without the skill;
- the current author and applicable license;
- whether the work is a new skill, a substantial revision, or a focused update; and
- whether reading an external source changed the skill in a way
  [provenance.md](provenance.md) treats as attribution-bearing.

Define one coherent unit of work that composes with other skills, under the "One coherent job" rule in
`SKILL.md`. Split unrelated guidance into separate skills or omit it.

Ground domain guidance in real execution, authoritative documentation, or existing project artifacts. A model
asked to invent a skill from general training knowledge produces plausible advice that changes nothing. When
extracting a skill from completed work, capture:

- the procedure that produced the successful result;
- every user correction or steering decision;
- required input and output forms;
- project conventions, constraints, and failure modes the agent initially missed; and
- successful behavior worth preserving, not only failures.

Useful project evidence includes runbooks, API specifications, schemas, configuration, review comments, issue
history, version-control fixes, and recorded failures with their resolutions. Label unsupported guidance as
uncertain or omit it.

**Observe the unaided failure before writing guidance.** When the user authorizes model runs for authoring,
run the representative requests without the skill first. Write guidance for the failures that control run
shows, and drop planned guidance whose control already succeeds, because that guidance pays context to change
nothing. Without authorization, tie each rule to a recorded failure, a user correction, or an authoritative
source instead. A control run is observation: comparing the finished candidate against a baseline belongs to
full evaluation.

For a new skill, run `python3 <skill-forge-root>/scripts/init_skill.py --help`. Use the initializer when its
minimal scaffold fits the requested package, and replace every generated placeholder before validation.
Create files manually when the scaffold would need more cleanup than it saves.

Ask the user only when a missing answer would change behavior, scope, portability, provenance,
compatibility, or cost. Proceed when the repository and request settle those choices.

Before adding guidance, check whether the agent can recover it from an authoritative runtime source. Point to
that source when it is accurate and available during use. Include the information when the source is
unavailable, unreliable, or silent on the judgment the skill must supply.

**Version facts.** Avoid pinning a tool's version by default. A pin in an install command or a version check in a
script goes stale within weeks, and makes an agent install an old release on purpose. Record a version as
*current known* instead: one line per tool naming the version and the date the skill's claims were last checked,
and the command or document that confirms them, such as `--help` or the changelog. Keep minimum requirements in
`compatibility`. Pin only where the version is the subject, and state the reason beside the pin: guidance that
differs per release line, such as Yocto releases; behavior that exists only from a given version; or a known-bad
release to avoid.

The step is complete when every item in the list above has an answer or a named gap, and each planned rule has
a grounding.

## 2. Choose Scope, Invocation, and Clients

Choose portable or repository-specific scope under "Portable is the default" in `SKILL.md`. A portable skill
may require tools intrinsic to its job; declare them in `compatibility`, check them when used, and report
missing dependencies.

Choose the invocation goal separately from scope. Decide from the job and representative requests whether the
agent should select the skill or the user should invoke it explicitly. When both goals stay plausible and the
choice changes routing, ask the user. An agent-selected skill needs a realistic request-time intent. An
explicit-only skill needs a verified client mechanism, because description wording alone does not enforce that
policy. A habit with neither path belongs in always-loaded instructions or another deliberately loaded
artifact.

Identify how each declared client loads the skill under that goal, and verify each client separately, since
one client's discovery result says nothing about another's. When a real invocation path exists, repair weak
routing rather than abandoning the skill. When no declared client can load the behavior reliably, change the
artifact form.

The step is done when scope, invocation goal, and each declared client's loading path are stated, or the
artifact form has changed.

## 3. Preserve Provenance

Every new skill records its current author in `metadata.author` and its license in the specification's
top-level `license` field. These conservative policies may exceed a license's legal minimum. Discover
authorship and licensing from authoritative repository or upstream sources.

An external source is attribution-bearing when reading it changes what the skill contains: adopted ideas,
mechanisms, structure, examples, terminology, or failure modes, even when no wording or code is copied. Record
each such source in `ATTRIBUTIONS.md`, naming the exact influence and separating independently expressed ideas
from copied or adapted material. Copied, adapted, translated, or vendored material also ships its upstream
license text. A source used only to verify public facts or runtime behavior needs no package attribution; cite
it near the affected claim when useful. Preserve every existing provenance file during updates.

Read [provenance.md](provenance.md) whenever an external source influenced the skill or supplied adapted or
vendored material.

The step is done when `metadata.author` and `license` are set from authoritative sources and every
influencing source has its `ATTRIBUTIONS.md` entry.

## 4. Design the Package

Establish how the workflow behaves before choosing files. When it coordinates several state changes, may
repeat an operation after uncertain completion, pauses for later resumption, or shares mutable state with
another actor, read [operational-workflows.md](operational-workflows.md) and settle its contract before
treating the candidate as complete.

Design for lean execution and progressive loading. Keep routing in metadata, shared execution guidance in
`SKILL.md`, and branch-specific material in resources. Make routing possible before loading the detail it
selects, and prefer summary observations before retrieving full records. A small, self-contained skill may
meet this without extra files. Verify the target client before claiming what it preloads or defers.

For each representative request, walk through execution from a capable agent's starting knowledge. Extract
only resources that improve repeated execution:

- Put essential shared instructions and decisions in `SKILL.md`.
- Put branch-specific detail in a focused reference and link it where that branch becomes relevant.
- Put repeated deterministic or fragile operations in scripts when an existing tool does not suffice.
- Put files consumed by the output in assets.

Suppose the user asks, "Turn our incident-triage workflow into a skill that reads service logs and fills our
postmortem template." A capable agent can summarize logs, but it lacks the service event schema and the team's
triage order. It would also repeat timestamp normalization.

```text
incident-summary/
├── SKILL.md
├── references/event-schema.md
├── scripts/normalize-timestamps.py
└── assets/postmortem-template.md
```

Keep triage and source ordering in `SKILL.md`. Put the stable event schema in the reference. Include the script
only when an existing tool cannot normalize timestamps reliably. Include the asset because the consumer
requires that exact template.

Link each reference directly from `SKILL.md` or from the mode file that uses it. Open a reference longer than
about 100 lines with a table of contents, because an agent often previews the first lines of a file and needs
to see its whole scope there.

Routing metadata may enter broad client context, while the body and each reference add context only when
loaded. A client may execute a script without loading its source; verify that before relying on the saving.

Keep each meaning in one authoritative place, and leave facts that a reliable live source provides cheaply to
that source. A short, self-contained skill is complete when it contains everything its task needs.

Read [workflow-patterns.md](workflow-patterns.md) when real prerequisites, branching, iteration, gates, or
strict output contracts make control flow consequential. Read [pro-agent.md](pro-agent.md) when deciding
whether repeated or fragile logic belongs in a script.

The step is done when every representative request walks through the planned files with each resource
justified by a request that needs it.

## 5. Write for Reliable Behavior

**Say what needs to be said; drop everything else.**

Include content that changes the agent's decisions, actions, or understanding needed for correct execution.
Remove filler, repetition, obvious explanations, and generic advice. Preserve necessary conditions,
constraints, failure handling, and examples that resolve ambiguity. Prefer the shortest clear and complete
explanation over cryptic compression.

Match specificity to risk: constrain fragile operations closely and leave room for judgment where several
approaches are valid. Teach a reusable procedure for a class of tasks rather than the answer to one example,
while keeping the exact commands, formats, and templates that correct execution depends on.

Choose a recommended default when one approach usually fits. Give each exception the condition that selects
it, rather than presenting an undifferentiated menu.

Read [writing-techniques.md](writing-techniques.md) before writing any rule, recipe, template slot, or
conditional. It maps each kind of failure to the guidance form that prevents it, and states when a constraint
needs its reason.

Keep a non-obvious prerequisite or gotcha in `SKILL.md` when the agent must know it before it can recognize
the condition for loading a reference. Move later branch detail behind a conditional pointer.

Write the initial description with the `writing-skill-descriptions` skill, passing it the scope and
invocation goal chosen in step 2.

Use a checklist only when order or prerequisites matter; independent rules and judgment read better as prose.
Reuse the user's existing authorization, and add a confirmation gate only when the eventual action needs
information or approval the user has not already supplied.

Make the package's described purpose match its behavior. Disclose consequential network access, credential
use, writes, destructive actions, and authority requirements, since an undisclosed one fails a hard gate in
[rubric.md](rubric.md). Inspect and test bundled executables and dependencies.

The step is done when the draft is complete, with no placeholder left, and you can name the failure each
guidance passage prevents.

## 6. Preflight and Review the Draft

Complete the substantive draft first, because mechanical results on a moving draft go stale. Then run a
structural preflight, which must finish before review lite or any model-based test. Preflight confirms:

- both validators named in the [rubric's hard gates](rubric.md#hard-gates) accept the package;
- the candidate and every promised resource are readable;
- no scaffold placeholders remain; and
- required commands and safe test destinations exist.

A preflight failure is a package defect, not skill behavior; repair it before testing. Preflight proves
loadability and fixture readiness, not that the skill improves behavior.

Run every new or changed script with representative success, invalid-input, and dependency-failure cases,
using safe fixtures for stateful behavior. Run the language's standard format, lint, and type checks on each
new or changed script where they are available, and report any check you could not run.

Read [testing-guide.md](testing-guide.md) to define cases, walk them, check loading boundaries, and prepare
discovery cases when routing is new or changed.

Then perform review lite as [rubric.md](rubric.md#review-tiers) defines it. Leave baseline selection and
comparative grading of the candidate to full evaluation. Preserving pre-change requirements and evidence, and
an authorized control run from step 1, are observation rather than grading.

## 7. Finish and Hand Off

Any content change makes earlier mechanical and behavioral results stale for the changed surface. Rerun the
affected checks, and rerun both validators after the final content change. The vendored specification source is
pinned, but its locked dependencies need network access on their first run.

Before delivery, confirm:

- the result fulfills the requested use cases without unrelated behavior;
- every resource earns its context or maintenance cost, and removing any remaining passage would weaken
  correct execution, understanding, or recovery;
- references are reachable at the point they become relevant;
- declared compatibility and scope match actual dependencies;
- provenance and license artifacts are complete and preserved; and
- no scaffold placeholders remain.

Follow the target repository's applicable mechanical checks and deployment workflow. Add further checks only
when the skill's domain or risk requires them.

Report the status the [rubric's verdicts](rubric.md#verdicts) allow. Deliver the candidate with its intended
behavior, relevant cases, author-side results labeled by evidence class, environment, untested clients, and
unresolved evidence gaps. When the user authorizes full evaluation, hand that package to review mode or the
target repository's review process, and let that process choose isolation, permissions, baselines, graders,
repetitions, and client coverage.
