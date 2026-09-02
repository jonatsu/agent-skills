# Skill Descriptions

The description is an always-loaded routing pointer. It must satisfy the Agent Skills specification by stating what the
skill does and when to use it, while remaining discriminating enough to avoid unrelated tasks.

## Method

1. State the capability in concrete terms.
2. Identify the distinct request branches the skill handles.
3. Represent each branch once using language a user is likely to use.
4. Add an exclusion only for a nearby skill or task that could plausibly be misrouted.
5. Remove implementation details and instructions that matter only after activation.

Distinct branches earn separate trigger language. Synonyms for the same branch usually do not. Lists of every related
verb and noun consume permanent context, blur boundaries, and attract false positives.

```yaml
# Too vague
description: Helps with PDFs.

# Too broad
description: Creates, reads, writes, edits, changes, fixes, processes, analyzes, and manages documents and files.

# Discriminating
description: Extracts text and tables from PDFs, fills PDF forms, and merges PDF files. Use when the task concerns PDF extraction, forms, or document assembly.
```

## Checks

- The description names both capability and activation conditions.
- Every trigger phrase represents a distinct supported branch.
- A representative unrelated request does not appear to match.
- The body contains no routing guidance that arrived too late to affect activation.
- The value meets the current Agent Skills specification.
