#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template with best-practice structure.
"""

import sys
from pathlib import Path

SKILL_TEMPLATE = """---
name: {skill_name}
description: "[TODO: Write a keyword-rich description. Include: (1) core capability in first sentence, (2) 5+ action verbs users might say, (3) 5+ object nouns, (4) natural language trigger phrases. See references/description-guide.md for examples. ALL trigger info goes HERE, not in the body.]"
metadata:
  author: Joonas Onatsu
  license: MIT
---

# {skill_title}

[TODO: Write your Iron Law here. Ask: \"What is the ONE mistake the agent will most likely make?\" Then write an unbreakable rule to prevent it.]

IRON LAW: [TODO: e.g., \"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.\"]

## Workflow

Copy this checklist and check off items as you complete them:

```text
{skill_title} Progress:

- [ ] Step 1: [TODO: First step] ⚠️ REQUIRED
  - [ ] 1.1 [TODO: Sub-step]
  - [ ] 1.2 [TODO: Sub-step]
- [ ] Step 2: Confirm with user ⚠️ REQUIRED
- [ ] Step 3: [TODO: Core operation]
- [ ] Step 4: [TODO: Output / delivery]
```

## Step 1: [TODO: First Step]

[TODO: Use question-style instructions, not vague directives.]

## Step 2: Confirm ⚠️ REQUIRED

- Proceed with all?
- Only high-priority items?
- Select specific items?
- View only, no changes?

⚠️ Do NOT proceed without user confirmation.

## Step 3: [TODO: Core Operation]

- Load references/[TODO].md for [specific purpose]

## Step 4: [TODO: Output]

[TODO: Define output format and structure]

## Anti-Patterns

[TODO: Ask: \"What would the agent's lazy default look like?\"]
- [TODO]
- [TODO]

## Pre-Delivery Checklist

- [ ] [TODO: e.g., No placeholder text remaining (TODO, FIXME)]
- [ ] [TODO: e.g., All generated code runs without errors]
- [ ] [TODO: e.g., Output matches requested format]
"""


def title_case_skill_name(skill_name):
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def init_skill(skill_name, path):
    skill_dir = Path(path).resolve() / skill_name
    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None
    skill_dir.mkdir(parents=True, exist_ok=False)
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name, skill_title=skill_title
    ).lstrip("\n")
    (skill_dir / "SKILL.md").write_text(skill_content)
    # Intentionally do NOT pre-create scripts/references/assets: empty dirs are
    # untracked by git and vanish on clone. Create them on demand when the skill
    # gains its first script/reference/asset (start at the lowest tier).
    print(f"Skill '{skill_name}' initialized at {skill_dir}")
    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != "--path":
        print("Usage: init_skill.py <skill-name> --path <path>")
        sys.exit(1)
    result = init_skill(sys.argv[1], sys.argv[3])
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
