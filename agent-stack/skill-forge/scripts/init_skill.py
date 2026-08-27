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

IRON LAW: [TODO: Ask \"What is the ONE mistake the agent will most likely make with this skill?\", then write the unbreakable rule that prevents it. e.g. \"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.\" Nothing goes above this line but the H1.]

[TODO: PICK A SHAPE BEFORE WRITING THE BODY. This template deliberately gives you no
skeleton, because the skeleton depends on the answer.

  process     a phased procedure with real ordering and prerequisites
              -> a trackable checklist with the ⚠️ REQUIRED / ⛔ BLOCKING markers
  mindset     taste and judgement                  -> NO checklist; a strong NEVER list
  navigation  routes the reader to other material  -> NO checklist; a routing table
  tool        decision trees, low freedom          -> NO checklist; the trees themselves
  philosophy  craft-first prose                    -> NO checklist

A checklist in anything but a Process skill instructs the agent to do what it already
does. It is a no-op, and a scored review will dock it. Delete this block once the body
exists.]

## Anti-Patterns

[TODO: Ask \"What would the agent's lazy default look like for this task?\", then forbid
it explicitly. Each entry MUST carry the non-obvious reason, or it reads as fussiness.]
- [TODO]
- [TODO]

## Pre-Delivery Checklist

[TODO: Each item MUST be settleable by looking at the output. \"Ensure good quality\" is
not; \"no placeholder text remaining (TODO, FIXME, xxx)\" is.]
- [ ] [TODO]
- [ ] [TODO]

[TODO: references/ is OPTIONAL — start with none and add one only when SKILL.md is
genuinely too long. If you do add any, each MUST carry a symptom-shaped load trigger in
this file — \"load when X happens\", NEVER a topic label like \"for patterns and
examples\", which says what is inside but never when to pay for it. The package MUST also
carry a \"do NOT load\" block naming what not to read, and when. Delete this block if the
skill ships no references.]
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
