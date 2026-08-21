# Workflow Patterns

## The Checklist Pattern

A trackable checklist gives the agent a clear execution path. Without one, it freestyles - inconsistent, skipping steps, mixing priorities.

### Basic Structure

```markdown
Copy this checklist and check off items as you complete them:

- [ ] Step 1: Setup & Analyze
  - [ ] 1.1 Load preferences
  - [ ] 1.2 Analyze content
  - [ ] 1.3 Check existing ⚠️ REQUIRED
- [ ] Step 2: Confirmation ⚠️ REQUIRED
- [ ] Step 3: Execute core task
- [ ] Step 4: Review & output
```

### Markers

| Marker | Meaning | When to Use |
|--------|---------|-------------|
| ⚠️ REQUIRED | Must not skip | User confirmation, critical validation |
| ⛔ BLOCKING | Must complete before proceeding | Prerequisite setup, dependency loading |
| (conditional) | Execute based on earlier decisions | Optional review, user-selected features |

### Design Principles

1. **Progressive depth**: start macro, go micro
2. **Sub-step nesting**: complex steps broken into 1.1, 1.2, 1.3
3. **Conditional branches**: mark steps that only run in certain scenarios

## Confirmation Gates

MUST force the agent to stop and ask the user before critical operations.

### When to Add Confirmation Gates

- Before any destructive operation (delete, overwrite, modify)
- Before any generative operation with significant compute cost
- Before applying changes based on analysis
- When user preferences affect the output

### Pattern 1: Simple Gate

```markdown
## Step 5: Confirm ⚠️ REQUIRED

Present findings to the user. Ask:
- Proceed with all recommendations?
- Only apply high-priority (P0/P1) items?
- Select specific items to apply?
- View only, no changes?

⚠️ NEVER proceed without explicit user confirmation.
```

### Pattern 2: Blocking Gate

```markdown
## Step 0: Load Preferences ⛔ BLOCKING

- Found -> load and continue
- Not found -> run first-time setup -> MUST complete before Step 1
```

## Pre-Delivery Checklist Pattern

MUST add concrete, verifiable checks before delivering output. Each item MUST be specific enough to check by looking at the output.

### Bad vs Good

```markdown
# Bad
- [ ] Ensure good quality
- [ ] Make sure it's accessible

# Good
- [ ] No placeholder text remaining (TODO, FIXME, xxx)
- [ ] All images have alt text
- [ ] All clickable elements have cursor-pointer
- [ ] Transitions are 150-300ms
```

### Priority-Based Output

| Level | Meaning | Action |
|-------|---------|--------|
| P0 | Critical | MUST block delivery |
| P1 | High | SHOULD fix before delivery |
| P2 | Medium | Create follow-up task |
| P3 | Low | Optional improvement |
