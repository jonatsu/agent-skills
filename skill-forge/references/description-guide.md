# Writing Skill Descriptions

## Why Description Matters

The `description` field in frontmatter is the ONLY thing the runtime sees before deciding to trigger your skill. The SKILL.md body loads AFTER triggering. So "When to Use This Skill" sections in the body are useless for triggering.

Two things the description controls:
1. Whether the skill triggers automatically
2. Whether users find it by search

## The Keyword Bombing Technique

MUST list every possible trigger scenario: actions, objects, synonyms, and natural language phrases a user would literally say.

### Four Dimensions of a Great Description

1. **Core capability** - what it does (first sentence)
2. **Action verbs** - what users ask to do
3. **Object nouns** - what users mention
4. **Natural phrases** - what users would literally type

### Good Example

```yaml
description: "Create beautiful, elegant Excalidraw diagrams based on
user intent. Use when user asks to draw, visualize, diagram, sketch,
illustrate concepts, create flowcharts, architecture diagrams, mind maps,
process flows, or any visual representation. Triggers on keywords like
'draw', 'diagram', 'visualize', 'sketch', 'flowchart', 'architecture',
'mind map', 'illustrate'."
```

### Bad vs Good

```yaml
# Bad - too vague, will not trigger reliably
description: "Code review tool"

# Good - covers natural language triggers
description: "Code review and quality analysis. Use when user says
'review this', 'check my code', 'audit this PR', 'does this code have
problems'. Supports Python, JavaScript, TypeScript, Go, Rust. Actions:
review, check, audit, inspect, analyze code quality, find bugs,
security review."
```

## Checklist

- [ ] First sentence states core capability
- [ ] 5+ action verbs listed
- [ ] 5+ object nouns or project types listed
- [ ] Natural language trigger phrases included
- [ ] Under 1024 characters
- [ ] MUST NOT contain angle brackets (`<` or `>`)
- [ ] All "when to use" info MUST be HERE, not in SKILL.md body

## Key Rule

NEVER put "When to Use This Skill" in the SKILL.md body. All trigger information belongs in the `description` field.
