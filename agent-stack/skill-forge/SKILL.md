---
name: skill-forge
description: "Create high-quality, production-grade agent skills. Expert guidance on skill architecture, workflow design, prompt engineering, description writing, packaging, and quality control. Use when user wants to create a new skill, build a skill, design a skill, write a skill, update an existing skill, improve a skill, refactor a skill, debug a skill, test a skill, or package a skill. Triggers: 'create skill', 'build skill', 'new skill', 'skill creation', 'write a skill', 'make a skill', 'design a skill', 'improve skill', 'package skill', 'skill development', 'skill template', 'skill best practices', 'write SKILL.md'."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Skill Forge

IRON LAW: Every line in a skill MUST justify its token cost. If it does not make the agent's output better, more consistent, or more reliable, cut it.

## What is a Skill

A skill is an onboarding guide for an agent, transforming it from a general-purpose assistant into a specialized one with procedural knowledge, domain expertise, and bundled tools.

```text
skill-name/
├── SKILL.md           # Required: workflow + instructions (<500 lines)
├── scripts/           # Optional: deterministic, repeatable operations
├── references/        # Optional: loaded into context on demand
└── assets/            # Optional: used in output, never loaded into context
```

**Default assumption:** the agent is already very capable. MUST only add what it does not already know. SHOULD challenge every paragraph: "Does this justify its token cost?"

**Second test — is it recoverable?** "The agent does not know it" is necessary
and NEVER sufficient. Before writing any factual content, ask three questions:

1. Can the agent obtain this at run time from an authoritative live source —
   `--help`, `--version`, a tool schema, `doctor`/`status`, a registry listing,
   or the file itself?
2. Will that source be reachable in the situations where this skill fires?
3. Is that source correct? Measured, NEVER assumed.

Three yeses → MUST write the pointer, NEVER the content. Any no → write it, and
state in one line why the live source does not serve.

Recoverable by default: CLI flags and subcommands, parameter schemas, config
keys, inventory counts, version numbers, supported-language lists, error
catalogues. A skill that transcribes these inherits a maintenance burden it
cannot meet, and its copy is wrong from the next upstream release onward while
still reading as authoritative. One audited skill gave its tool count as 81 in a
title, 76 in two separate notes, and 63 by its own arithmetic, against 80 actual
rows — four answers to a question the running tool answers once, correctly.

Question 3 is load-bearing. Where the live source is WRONG — a published schema
stripped of its combinators, a documented warning that never fires — the skill's
measured correction is among the most valuable content it can hold, and it looks
exactly like the transcription this rule tells you to cut. Question 2 covers the
other exception: a troubleshooting skill cannot route the agent to the `--help`
of the tool that is broken.

The pointer replaces the transcription, NEVER the judgement. "Get the flags from
`<tool> <cmd> --help`" plus the residue `--help` does not carry — the clamped
floor, the credential that never touches disk, which op to prefer for a sweep —
is the correct shape.

## Structure

A `SKILL.md` plus, only where the task needs them, `scripts/`, `references/` and
`assets/`. No ladder of skill types, no classification to make: MUST start with
`SKILL.md` alone and add a directory when something concrete belongs in it, NEVER
in anticipation. **One ceiling governs every skill — under 500 lines — and there is
no per-kind target.** A short skill is correct, not incomplete.

## Workflow

Copy this checklist and check off items as you complete them:

```text
Skill Forge Progress:

- [ ] Step 1: Understand the Skill ⚠️ REQUIRED
  - [ ] 1.1 Clarify purpose and concrete use cases
  - [ ] 1.2 Collect 3+ concrete usage examples
  - [ ] 1.3 Identify trigger scenarios and keywords
  - [ ] 1.4 Decide whether this is an ordered procedure, and which workflow mechanisms it needs
- [ ] Step 2: Plan Architecture
  - [ ] 2.1 Identify reusable resources (scripts, references, assets)
  - [ ] 2.2 Design progressive loading strategy
  - [ ] 2.3 Design parameter system (if applicable)
- [ ] Step 3: Initialize ⛔ BLOCKING (skip if skill already exists)
  - [ ] Run init_skill.py
- [ ] Step 4: Write Description
  - [ ] Load references/description-guide.md
  - [ ] Apply keyword bombing technique
- [ ] Step 5: Write SKILL.md Body
  - [ ] 5.1 Set Iron Law
  - [ ] 5.2 Design workflow checklist
  - [ ] 5.3 Add confirmation gates
  - [ ] 5.4 Add parameter system (if applicable)
  - [ ] 5.5 Apply writing techniques
  - [ ] 5.6 Add anti-patterns list
  - [ ] 5.7 Add pre-delivery checklist
- [ ] Step 6: Build Resources
  - [ ] 6.1 Implement and test scripts
  - [ ] 6.2 Write reference files
  - [ ] 6.3 Prepare assets
- [ ] Step 7: Test ⚠️ REQUIRED
  - [ ] Load references/testing-guide.md
  - [ ] Run trigger tests (5+ positive, 5+ negative)
  - [ ] Run functional tests for each workflow
  - [ ] Compare with/without skill performance
  - [ ] Verify every claim about tool behavior against the tool, with version and date
- [ ] Step 8: Review ⚠️ REQUIRED
  - [ ] Run pre-delivery checklist
  - [ ] Present summary to user for confirmation
- [ ] Step 9: Validate
  - [ ] Run quick_validate.py, and read its warnings as well as its verdict
- [ ] Step 10: Iterate based on real usage
```

## References, and when NOT to load them

Seven files. Each step below names the symptom that earns its load; nothing here needs
reading up front, and reading it all costs more than the body it supports.

**Do NOT load:**

- `architecture-patterns.md` for a single linear procedure. Its eight shapes are for
  skills that route, fan out, loop or degrade; a sequential workflow needs none of them,
  and shopping the list invites structure the skill does not need.
- `pro-agent.md` when no script is in question. It settles script-versus-prose, and read
  outside that decision it argues for scripting work that does not want a script.
- `parameter-system.md` for a skill that takes no arguments. Read speculatively it
  suggests flags, and a flag nobody asked for is a gate nobody wanted.
- `workflow-patterns.md` to decide WHETHER a checklist belongs. It assumes that question
  is settled and supplies the markers; loaded early it answers "yes" by default, which is
  the exact defect Step 5.2 exists to prevent.
- More than one of `description-guide.md`, `writing-techniques.md` and `testing-guide.md`
  at a time. They serve Steps 4, 5 and 7 respectively; needing two at once means the step
  you are on is not the step you think you are on.

## Step 1: Understand the Skill ⚠️ REQUIRED

Ask yourself:
- What specific problem does this skill solve that the agent cannot do well on its own?
- What would a user literally type to trigger this skill?
- What are 3-5 concrete usage examples with realistic inputs and expected outputs?
- Is this an ordered procedure — real sequencing, real prerequisites — or a body of
  judgement the agent applies in whatever order the situation calls for?

If unclear, MUST ask the user. MUST start with the most critical question first.

NEVER proceed until you have at least 3 concrete examples.

## Step 2: Plan Architecture

For each concrete example, ask:
1. What operations are deterministic and repeatable? -> `scripts/`
2. What domain knowledge is needed at specific steps? -> `references/`
3. What files are used in output but not in reasoning? -> `assets/`

Three levels load at three moments, and the split exists to exploit that: `name` +
`description` are always resident, the body arrives on trigger, and the rest costs nothing
until something reaches for it.

Key constraints:
- SKILL.md MUST stay under 500 lines; everything else goes to `references/`. The context
  window is shared with the system prompt, the conversation and every other skill's
  metadata, so a bloated SKILL.md crowds out work that is not yours
- References SHOULD be organized by domain, not by type, one level of nesting only.
  `references/palettes/`, `references/config/` — NEVER `references/checklists/`,
  `references/templates/`, which sort by shape and leave the agent guessing which
  shape holds its answer
- ⛔ Load `references/architecture-patterns.md` when the skill must support several
  distinct operations, fan out to subagents, loop until a quality bar is met, or keep
  working when a tool it wanted is missing — it carries the eight workflow mechanisms
  and what each is for. These describe CONTROL FLOW the task needs, never a kind of
  skill; pick from them by need. Skip the file for a single linear procedure
- ⛔ Load `references/pro-agent.md` when deciding what belongs in a script versus in
  prose, and the call is not obvious — typically when a step is deterministic but
  feels too small to extract

## Step 3: Initialize ⛔ BLOCKING

MUST skip if working on an existing skill. Otherwise run:

```bash
python3 scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates a template with Iron Law placeholder, workflow checklist, and proper directory structure.
It also seeds default frontmatter metadata for newly created skills.

## Step 4: Write Description

The description determines:
1. Whether the skill triggers automatically
2. Whether users find it by search

⛔ Load `references/description-guide.md` before writing the description — every time,
because a description that reads well to its author is the single most common reason a
finished skill never fires.

Key rule: NEVER put "When to Use" info in the SKILL.md body. The body loads after triggering; too late.

## Step 5: Write SKILL.md Body

Load reference files as needed for each sub-step.

### 5.1 Set Iron Law

Ask: "What is the ONE mistake the agent will most likely make with this skill?"
MUST write a rule that prevents it. MUST place it immediately after the H1 title
and before any other prose — that is the top of the body, since every SKILL.md
opens with its H1.

⛔ Load `references/writing-techniques.md` when you cannot name the one mistake, or when
the rule you wrote could be read as advice rather than a prohibition.

### 5.2 Design Workflow Checklist (conditional)

⛔ **One question decides this: does the task have real ordering and real
prerequisites — steps that fail or mislead if run out of sequence?**

If NO, there is no checklist. "Step 1: Inspect narrowly … Step 4: Verify"
instructs the agent to do what it already does, so it costs tokens and buys
nothing. NEVER add one to satisfy this step; skip it, and say in one line that
the task has no ordering.

If YES, the checklist is how the ordering survives contact with a long session.

Where there is no ordering, write the decisions the agent must actually get
right instead: "before X, ask yourself …", each carrying the non-obvious trap
that makes it a decision rather than a habit.

Where there IS ordering, create a trackable checklist with:
- ⚠️ REQUIRED for steps that MUST NOT be skipped
- ⛔ BLOCKING for prerequisites
- Sub-step nesting for complex steps
- (conditional) for steps that depend on earlier choices

⛔ Load `references/workflow-patterns.md` once the ordering question is answered YES and you
need the marker vocabulary — it also covers gates and output shape, so one load serves 5.2,
5.3 and 5.7. Do NOT load it to decide WHETHER a checklist belongs; that decision is above,
and the file assumes it is settled.

### 5.3 Add Confirmation Gates

MUST force the agent to stop and ask the user before:
- Destructive operations (delete, overwrite, modify)
- Generative operations with significant cost
- Applying changes based on analysis

A `--quick`-style flag MAY skip a gate that only collects preferences. It MUST NEVER
skip a destructive-operation gate: one flag typed up front cannot authorize an action
the user had no way to foresee when they typed it.

Already loaded at 5.2 if the task has ordering. Otherwise load it now only if a gate's
wording is unclear — the categories above are usually enough on their own.

### 5.4 Add Parameter System (if applicable)

⛔ Load `references/parameter-system.md` when the skill will accept flags at all — it
carries the `$ARGUMENTS` mechanics and, critically, which gates a `--quick` flag may and
may NOT skip. Skip the file entirely when the skill takes no arguments.

### 5.5 Apply Writing Techniques

Three techniques that dramatically improve output quality:
1. Question-style instructions: give questions, not vague directives
2. Anti-pattern documentation: list what NOT to do
3. Iron Law + red flags: prevent shortcuts

Already loaded at 5.1. Return to it when a directive you have written still reads as a
suggestion after rewording.

### 5.6 Add Anti-Patterns List

Ask: "What would the agent's lazy default look like for this task?" Then MUST explicitly forbid it.

### 5.7 Add Pre-Delivery Checklist

MUST add concrete, verifiable checks. NOT "ensure good quality"; instead "no placeholder text remaining (TODO, FIXME, xxx)".

Covered by `references/workflow-patterns.md` — load it here if you have not already, and
only when a check you wrote cannot be settled by looking at the output.

### Writing Principles

- **Concise**: MUST only add what the agent does not already know
- **Imperative form**: SHOULD use "Analyze the input" not "You should analyze the input"
- **RFC 2119 keywords**: all behavioral directives MUST use ALL CAPS keywords (MUST, SHOULD, NEVER, MAY)
- **Authorship and license metadata**:
  - For a newly created skill, MUST set `metadata.author` to `Joonas Onatsu` and `metadata.license` to `MIT`.
  - For a skill adapted from upstream, MUST still set `metadata.author` to `Joonas Onatsu` and MUST set `metadata.license` to the upstream license.
  - For a skill adapted from upstream, MUST move upstream provenance out of `SKILL.md` frontmatter and into `ATTRIBUTIONS.md`.
  - `ATTRIBUTIONS.md` MUST record original author or authors, upstream project or URL, pinned commit or tag when available, and a short adaptation note.
  - For a skill adapted from upstream, a verbatim copy of the upstream license MUST ship beside `ATTRIBUTIONS.md` as `LICENSE.upstream`, and upstream's own `NOTICE` (where one exists) as `NOTICE.upstream`. A link is NOT compliance: Apache-2.0 sections 4(a) and 4(d) require both to travel with a modified version, and provenance metadata alone satisfies neither. Keep both files with the skill when redistributing or re-deploying it.
  - MUST verify the upstream license against a primary source. `gh repo view --json licenseInfo` misreports repositories that DO carry a LICENSE file; use `gh api repos/OWNER/REPO/license` and fetch the license and NOTICE files themselves.
  - When creating `ATTRIBUTIONS.md`, SHOULD start from `assets/ATTRIBUTIONS.template.md`.
- **Match freedom to fragility**:
  - High freedom (text): multiple valid approaches
  - Medium (pseudocode/params): preferred pattern, some variation OK
  - Low (specific scripts): fragile operations, consistency critical
- **Scope declaration**: `metadata.scope` is either `portable` or `repo-local`,
  and it decides which half of the next rule applies. A **`repo-local` skill
  MUST declare it** — the exemption for naming a repository's runners and paths
  is not available without the declaration. A portable skill MAY omit it, since
  absent already means portable. The burden sits on the exception deliberately:
  a rule that obliges every skill to restate the default is one nobody keeps.
  - `portable` — the default, and what MUST be assumed when the key is absent.
    Runs in any repository on any machine. MUST NOT name a project-local entry
    point, an install path, or an ecosystem the target repo has not evidenced.
  - `repo-local` — ships inside the repository it serves. MAY name that repo's
    runners, paths and conventions directly; they are its contract rather than
    an assumption. MUST name that repository in its opening lines, so the next
    reader does not lift it somewhere it cannot work.
  - A skill carrying local bindings with no `repo-local` declaration is a
    portable skill with a defect, NEVER a repo-local skill that forgot to say
    so. Declare the scope, or remove the bindings.
- **Environment independence**: a skill is universal by nature — it runs on
  machines nobody configured for it, months after it was written. It MUST NOT
  depend on any environmental fact it did not verify at run time.
  - Tool availability MUST be established by a `PATH` probe
    (`command -v <tool>`) and nothing else. NEVER assume a tool is installed,
    and NEVER hardcode an install path (`/usr/local/bin/x`,
    `~/.local/share/mise/installs/...`, `/opt/homebrew/...`).
  - **A project-local entry point is NOT a tool, and no `PATH` probe validates
    it.** `just check`, `npm run lint`, `make test`, `mise run ci`,
    `pre-commit run`, `nox -s tests` and `./scripts/gate.sh` are contracts of one
    REPOSITORY, not of a machine. `command -v just` succeeds on any machine that
    has `just` while that repo's `check` recipe does not exist — the probe passes
    and the command still fails, which is worse than no probe at all. A portable
    skill MUST NOT name one.
  - Instead, DISCOVER the repo's entry point at run time, and state the detection
    order: a pre-commit config, then a task runner (`justfile`, `Makefile`,
    `mise.toml`, `package.json` scripts, `pyproject` scripts), then a
    `scripts/`/`bin/` entry. Run what is found. When nothing is found, report that
    and skip — NEVER invent a command, and NEVER assume the conventional name is
    present.
  - **Exception: repo-scoped skills.** A skill that ships inside the repository
    it serves MAY, and SHOULD, name that repo's commands directly — they are its
    contract rather than an assumption. It MUST declare `metadata.scope:
    repo-local` and name that repository near the top, so the next reader knows
    the naming is deliberate and does not lift the skill somewhere it cannot
    work.
  - **Exception: a skill ABOUT a tool may bind to that tool, and to nothing
    else.** Naming `pytest` inside a pytest skill is its subject, not an
    assumption, and demanding tool-agnosticism there is incoherent. The
    carve-out covers the subject ONLY: that same skill MUST still discover the
    repo's runner rather than naming `just test`, MUST still probe for any tool
    beyond its subject, and MUST still state what happens when its own subject
    is absent. Assuming a SECOND tool is the ordinary defect wearing the
    subject's clothes, and it is harder to see precisely because the first
    binding was legitimate.
  - When a tool is absent, the skill MUST degrade to a reported skip or a named
    alternative, NEVER fail and NEVER silently continue as though the step ran.
  - Where several tools do the job, list them in preference order and accept any
    one. A single hardcoded tool rots the moment the ecosystem moves.
  - Paths to a skill's own bundled files MUST be relative to the skill
    directory. NEVER write `~/.claude/skills/<name>/...`: it breaks under
    `CLAUDE_CONFIG_DIR` and for project-scoped installs alike.
  - NEVER reference the authoring machine — its absolute paths, its usernames,
    its specific package manager, or a tool version only it has.

## Step 6: Build Resources

### Scripts
- MUST encapsulate deterministic, repeatable operations
- Scripts execute without loading into context; major token savings
- MUST test every script before packaging
- In SKILL.md, MUST document only command and arguments, not source code

### References
- MUST organize by domain, not by type
- MUST use one level of nesting only
- Large files (>100 lines) SHOULD have a table of contents at the top
- Every reference MUST carry a symptom-shaped load trigger in SKILL.md — "load when X happens", never a topic label. "`05-advanced.md` — power tools, proxy, shell hook" says what is inside; it never says when to pay for it, and an agent given only topic labels loads nothing or loads everything.
- The package MUST carry a "do NOT load" block naming what not to read, and when.
- NEVER let one reference outgrow the rest of the package combined. Split it, cut what is recoverable from it, and give each named section its own trigger. A reference that large is loaded whole or not at all, and both are wrong.

Already covered at Step 2 by `references/architecture-patterns.md`; do NOT re-load it here.

### Assets
- Templates, images, fonts used in output
- Not loaded into context, just referenced by path
- If the skill is adapted from upstream, use `assets/ATTRIBUTIONS.template.md`
  as the starting point for `ATTRIBUTIONS.md`

## Step 7: Test ⚠️ REQUIRED

⛔ Load `references/testing-guide.md` here — the four areas below are headings; the file
carries what each test actually consists of and the metric targets to hit.

Four areas to cover:
1. **Triggering**: does the skill activate for the right queries and stay dormant for others?
2. **Functional**: does each workflow produce correct outputs?
3. **Performance**: is the skill better than no skill? (fewer messages, fewer errors, better consistency)
4. **Claim verification**: where the skill asserts how a tool or system behaves, MUST exercise those claims against the real thing rather than reviewing them by reading. Record the version and the date, name which claims were checked and which were not, and state what to re-run first after an upgrade. A reference skill has no workflow to test functionally, so without this it ships unexercised — which is how a documented warning that never fires survives review.

MUST test before proceeding to review.

## Step 8: Review ⚠️ REQUIRED

MUST present the skill summary to the user and confirm before packaging.

For a scored design review, MAY invoke the `skill-judge` skill via the Skill tool
if it appears in this session's available-skills list — it grades the draft
against eight weighted dimensions (knowledge delta, anti-patterns, description
quality, freedom calibration, and more) and returns concrete fixes. Otherwise use
the Pre-Delivery Checklist below.

### Pre-Delivery Checklist

#### Structure
- [ ] SKILL.md under 500 lines
- [ ] Frontmatter has `name` and `description`
- [ ] Description includes trigger keywords and usage scenarios
- [ ] Frontmatter metadata uses current author and correct license
- [ ] Adapted skills have `ATTRIBUTIONS.md` with upstream provenance
- [ ] Adapted skills ship `LICENSE.upstream`, and `NOTICE.upstream` where upstream has one
- [ ] No example or placeholder files left from initialization

#### Quality
- [ ] Has an Iron Law or core constraint at the top
- [ ] Has a trackable workflow checklist with ⚠️/⛔ markers, OR the task has no real
      ordering and the skill says so in one line
- [ ] Confirmation gates before destructive or generative operations
- [ ] Uses question-style instructions, not vague directives
- [ ] Lists anti-patterns (what NOT to do)
- [ ] References loaded progressively, and each carries a symptom-shaped load trigger
- [ ] A "do NOT load" block exists; no single reference exceeds the rest combined
- [ ] No transcribed CLI flags, schemas, config keys, or counts a live source reports
- [ ] Claims about tool behavior carry the version and date they were verified
- [ ] All behavioral directives use RFC 2119 keywords in ALL CAPS
- [ ] Every rule the skill states is obeyed by its own examples, templates,
      commands and conduct — check each rule against the instances it governs,
      not against other rules
- [ ] Every countable claim about the package ("each…", "all four…", "the
      only…") was recounted after the last edit

#### Resources
- [ ] Scripts tested and executable
- [ ] References organized by domain, one level deep
- [ ] Large references have table of contents
- [ ] Assets used in output, not loaded into context

#### Portability
- [ ] Every external tool is reached through a `command -v` probe, with a
      degraded path when absent
- [ ] No absolute install paths, no `~`-rooted paths to bundled files, no
      authoring-machine paths or usernames
- [ ] Where alternatives exist, more than one tool is accepted
- [ ] No project-local entry point (`just <recipe>`, `npm run <script>`,
      `make <target>`, `./scripts/*`) named by a portable skill; the repo's own
      runner is discovered at run time instead
- [ ] Any skill with repo-specific bindings declares `metadata.scope:
      repo-local` AND names its repository near the top; a portable skill may
      omit the key, because absent means portable
- [ ] A skill about a tool binds to that tool only — every OTHER tool it touches
      is still probed, and its own runner is still discovered

#### Anti-Patterns to Avoid

Every checklist item above is also an anti-pattern; they are not repeated here. These two
have no checklist counterpart because they are about what the package CONTAINS rather than
what it says:

- Shipping user-facing documentation inside the skill — `README.md`,
  `INSTALLATION_GUIDE.md`, `QUICK_REFERENCE.md`, `CHANGELOG.md`. A skill SHOULD contain only
  files that directly support its function; docs about the skill belong outside it.
- Putting "When to Use" guidance in the body instead of the `description`. The body loads
  only after the description has already decided whether to trigger, so guidance there can
  never affect the decision it describes.

## Step 9: Validate

```bash
python3 scripts/quick_validate.py <path/to/skill-folder>
```

MUST fix every error and re-run. Needs PyYAML; where it is absent, invoke it through a
runner that supplies it (`uv run --with pyyaml python3 …`) rather than treating the
ImportError as a validation result.

⚠️ **Read the warnings, not just the verdict.** Failures are structural only. An
unrecognised frontmatter key warns rather than fails, because each target harness owns its
own schema and adds fields on its own timetable — so it means "check that agent's docs",
never "this is broken". Unset `metadata.author`/`license` warns for the same reason: a
defect in a skill authored here, expected in a third-party skill under evaluation.

**A pass is not a review.** It reads frontmatter and nothing else — not the 500-line
ceiling, a missing Iron Law, a topic-label trigger, leftover placeholders or an absent
`LICENSE.upstream`. The Pre-Delivery Checklist covers those, and it is not automated.

## Step 10: Iterate

After real usage:
1. Notice where the agent struggles or is inconsistent
2. Identify which workflow step needs improvement
3. Add more specific instructions, examples, or anti-patterns
4. Re-test and re-package

Load `references/testing-guide.md` again only when the skill is misbehaving in the wild —
firing when it should not, staying silent when it should fire, or failing mid-workflow. Its
Iteration Signals table maps each symptom to the adjustment.
