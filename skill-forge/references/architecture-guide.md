# Skill Architecture Guide

## Progressive Loading

### The 500-Line Rule

SKILL.md MUST stay under 500 lines. Everything beyond that goes into `references/`.

Why: the context window is shared with system prompts, conversation history, user input, and other skill metadata. A bloated SKILL.md crowds out everything else.

**Bad:** a 2000-line SKILL.md with API docs, examples, and FAQ all in one file.

**Good:** a 150-line SKILL.md with clear workflow steps. Each step says "Load references/xxx.md" only when needed.

### Three-Level Loading

1. **Metadata** (`name` + `description`) - always in context
2. **SKILL.md body** - loaded when skill triggers
3. **Bundled resources** - loaded on demand

### Load-on-Demand Pattern

```markdown
## Step 3: Security Review
Load references/security-checklist.md and check each item against the code.
```

## Reference Organization

### Organize by Domain, Not by Type

```text
# Bad
references/checklists/
references/templates/
references/examples/

# Good
references/palettes/
references/renderings/
references/config/
references/workflow/
```

Rules:
1. MUST use one level of nesting only
2. MUST include clear "when to load" instructions
3. Large files (>100 lines) SHOULD get a TOC
4. MUST NOT duplicate between SKILL.md and references

## Script Encapsulation

### When to Use Scripts

Ask: "Is this operation deterministic and repeatable?" If yes -> script it.

Examples:
- PDF rotation -> `scripts/rotate_pdf.py`
- Search -> `scripts/search.py`
- Format conversion -> `scripts/convert.py`

### Key Benefit: No Context Cost

Scripts execute without being loaded into context. The agent only needs to know:
1. The script exists
2. What arguments it takes
3. What it returns

### Document Scripts Minimally in SKILL.md

```markdown
## Available Scripts

### scripts/search.py
Search the database for matching styles.
Usage: `python3 scripts/search.py "<query>" --domain <color|font|layout>`
Returns: JSON array of matching entries.
```

## What NOT to Include in a Skill

MUST NOT create:
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- Other user-facing documentation

A skill SHOULD contain only files that directly support its functionality.
