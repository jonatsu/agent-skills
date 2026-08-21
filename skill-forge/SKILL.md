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

## Complexity Tiers

MUST detect the appropriate tier based on the user's description:

| Tier | Structure | Use When |
|------|-----------|----------|
| 1 | Single SKILL.md (<200 lines) | Simple workflow, no scripts needed |
| 2 | SKILL.md + scripts/ | Needs deterministic execution (validation, data processing) |
| 3 | Multi-skill orchestrator | Complex domain with multiple distinct workflows |
| 4 | Full ecosystem (orchestrator + agents + scripts) | Enterprise-grade with parallel delegation |

MUST start at the lowest tier that works. MUST upgrade only when complexity demands it.

## Workflow

Copy this checklist and check off items as you complete them:

```text
Skill Forge Progress:

- [ ] Step 1: Understand the Skill ⚠️ REQUIRED
  - [ ] 1.1 Clarify purpose and concrete use cases
  - [ ] 1.2 Collect 3+ concrete usage examples
  - [ ] 1.3 Identify trigger scenarios and keywords
  - [ ] 1.4 Determine complexity tier (1-4)
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
- [ ] Step 8: Review ⚠️ REQUIRED
  - [ ] Run pre-delivery checklist
  - [ ] Present summary to user for confirmation
- [ ] Step 9: Package
  - [ ] Run quick_validate.py
  - [ ] Run package_skill.py
- [ ] Step 10: Iterate based on real usage
```

## Step 1: Understand the Skill ⚠️ REQUIRED

Ask yourself:
- What specific problem does this skill solve that the agent cannot do well on its own?
- What would a user literally type to trigger this skill?
- What are 3-5 concrete usage examples with realistic inputs and expected outputs?
- What complexity tier fits? (See Complexity Tiers above)

If unclear, MUST ask the user. MUST start with the most critical question first.

NEVER proceed until you have at least 3 concrete examples.

## Step 2: Plan Architecture

For each concrete example, ask:
1. What operations are deterministic and repeatable? -> `scripts/`
2. What domain knowledge is needed at specific steps? -> `references/`
3. What files are used in output but not in reasoning? -> `assets/`

Key constraints:
- SKILL.md MUST stay under 500 lines; everything else goes to `references/`
- References SHOULD be organized by domain, one level of nesting only
- Load `references/architecture-guide.md` for progressive loading patterns
- Load `references/pro-agent.md` for the 3-layer architecture (directive/orchestration/execution)

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

Load `references/description-guide.md` for keyword bombing and good/bad examples.

Key rule: NEVER put "When to Use" info in the SKILL.md body. The body loads after triggering; too late.

## Step 5: Write SKILL.md Body

Load reference files as needed for each sub-step.

### 5.1 Set Iron Law

Ask: "What is the ONE mistake the agent will most likely make with this skill?"
MUST write a rule that prevents it. MUST place it at the top of SKILL.md, right after frontmatter.

Load `references/writing-techniques.md` for Iron Law patterns and red flag signals.

### 5.2 Design Workflow Checklist

Create a trackable checklist with:
- ⚠️ REQUIRED for steps that MUST NOT be skipped
- ⛔ BLOCKING for prerequisites
- Sub-step nesting for complex steps
- (conditional) for steps that depend on earlier choices

Load `references/workflow-patterns.md` for checklist patterns and examples.

### 5.3 Add Confirmation Gates

MUST force the agent to stop and ask the user before:
- Destructive operations (delete, overwrite, modify)
- Generative operations with significant cost
- Applying changes based on analysis

Load `references/workflow-patterns.md` for confirmation gate patterns.

### 5.4 Add Parameter System (if applicable)

If the skill benefits from flags like `--quick`, `--style`, `--regenerate N`, load `references/parameter-system.md`.

### 5.5 Apply Writing Techniques

Three techniques that dramatically improve output quality:
1. Question-style instructions: give questions, not vague directives
2. Anti-pattern documentation: list what NOT to do
3. Iron Law + red flags: prevent shortcuts

Load `references/writing-techniques.md` for examples.

### 5.6 Add Anti-Patterns List

Ask: "What would the agent's lazy default look like for this task?" Then MUST explicitly forbid it.

### 5.7 Add Pre-Delivery Checklist

MUST add concrete, verifiable checks. NOT "ensure good quality"; instead "no placeholder text remaining (TODO, FIXME, xxx)".

Load `references/output-patterns.md` for checklist patterns and priority-based output.

### Writing Principles

- **Concise**: MUST only add what the agent does not already know
- **Imperative form**: SHOULD use "Analyze the input" not "You should analyze the input"
- **RFC 2119 keywords**: all behavioral directives MUST use ALL CAPS keywords (MUST, SHOULD, NEVER, MAY)
- **Authorship and license metadata**:
  - For a newly created skill, MUST set `metadata.author` to `Joonas Onatsu` and `metadata.license` to `MIT`.
  - For a skill adapted from upstream, MUST still set `metadata.author` to `Joonas Onatsu` and MUST set `metadata.license` to the upstream license.
  - For a skill adapted from upstream, MUST move upstream provenance out of `SKILL.md` frontmatter and into `ATTRIBUTIONS.md`.
  - `ATTRIBUTIONS.md` MUST record original author or authors, upstream project or URL, pinned commit or tag when available, and a short adaptation note.
  - When creating `ATTRIBUTIONS.md`, SHOULD start from `assets/ATTRIBUTIONS.template.md`.
- **Match freedom to fragility**:
  - High freedom (text): multiple valid approaches
  - Medium (pseudocode/params): preferred pattern, some variation OK
  - Low (specific scripts): fragile operations, consistency critical
- **Environment independence**: a skill is universal by nature — it runs on
  machines nobody configured for it, months after it was written. It MUST NOT
  depend on any environmental fact it did not verify at run time.
  - Tool availability MUST be established by a `PATH` probe
    (`command -v <tool>`) and nothing else. NEVER assume a tool is installed,
    and NEVER hardcode an install path (`/usr/local/bin/x`,
    `~/.local/share/mise/installs/...`, `/opt/homebrew/...`).
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

Load `references/patterns.md` for proven workflow patterns and anti-patterns.

### Assets
- Templates, images, fonts used in output
- Not loaded into context, just referenced by path
- If the skill is adapted from upstream, use `assets/ATTRIBUTIONS.template.md`
  as the starting point for `ATTRIBUTIONS.md`

## Step 7: Test ⚠️ REQUIRED

Load `references/testing-guide.md` for the full testing methodology.

Three areas to cover:
1. **Triggering**: does the skill activate for the right queries and stay dormant for others?
2. **Functional**: does each workflow produce correct outputs?
3. **Performance**: is the skill better than no skill? (fewer messages, fewer errors, better consistency)

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
- [ ] No example or placeholder files left from initialization

#### Quality
- [ ] Has an Iron Law or core constraint at the top
- [ ] Has a trackable workflow checklist with ⚠️/⛔ markers
- [ ] Confirmation gates before destructive or generative operations
- [ ] Uses question-style instructions, not vague directives
- [ ] Lists anti-patterns (what NOT to do)
- [ ] References loaded progressively, not all upfront
- [ ] All behavioral directives use RFC 2119 keywords in ALL CAPS

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

#### Anti-Patterns to Avoid
- Stuffing everything into one massive SKILL.md (>500 lines)
- Vague description like "A tool for X"
- No workflow; letting the agent freestyle
- No confirmation gates; unchecked execution
- Vague instructions like "ensure good quality"
- Including README.md, INSTALLATION_GUIDE.md, or other user-facing docs
- "When to Use" info in the body instead of the description field
- Hardcoding one tool, one install path, or the authoring machine's layout

## Step 9: Package

```bash
python3 scripts/quick_validate.py <path/to/skill-folder>
python3 scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

MUST validate before packaging. MUST fix errors and re-run.

## Step 10: Iterate

After real usage:
1. Notice where the agent struggles or is inconsistent
2. Identify which workflow step needs improvement
3. Add more specific instructions, examples, or anti-patterns
4. Re-test and re-package

Load `references/testing-guide.md` for iteration signals (under-triggering, over-triggering, execution issues).
