# Skill Descriptions

The description is an always-loaded routing pointer. It must satisfy the Agent Skills specification by stating
what the skill does and when to use it, while remaining discriminating enough to avoid unrelated tasks.

## Method

1. State the capability in concrete terms.
2. When the description names a specialized tool, product, or artifact, provide enough plain context for
   accurate activation. State the capability and user intent that the name represents. Do not define concepts
   the target agent can reasonably be expected to know or add background that does not improve routing.
3. Identify the distinct request branches the skill handles.
4. Represent each branch once using language a user is likely to use.
5. Add an exclusion only for a nearby skill or task that could plausibly be misrouted.
6. Remove implementation details and instructions that matter only after activation.

Distinct branches earn separate trigger language. Synonyms for the same branch usually do not. Lists of every
related verb and noun consume permanent context, blur boundaries, and attract false positives.

## Form and Length

Write the description as an inline scalar on one logical line. Some deployment tooling mishandles folded
(`>-`) and literal (`|`) block scalars, and a repository that has hit such a defect states the constraint and
its owner in its own instructions. Check for a repository rule before choosing a block scalar.

Budget the description by length, never by line width. A column ceiling such as markdownlint's MD013 governs
wrapped prose; a description cannot wrap while it stays an inline scalar, and Markdown tooling commonly treats
frontmatter as non-content and never inspects it. The Agent Skills specification caps a description at 1024
characters, which the reference validator enforces.

Staying under the cap is not the same as being affordable. Every description in a collection is loaded for
every request, so its length is charged against the discovery context that all other skills share. Spend it on
distinct branches and necessary exclusions; a repository MAY set a tighter budget than the specification and
enforce it separately.

```yaml
# Too vague
description: Helps with PDFs.

# Too broad
description: Creates, reads, writes, edits, changes, fixes, processes, analyzes, and manages documents and files.

# Discriminating
description: Extract PDF text and tables, fill forms, and merge files. Use for extraction, forms, or assembly.
```

```yaml
# Assumes the router already understands the tool and artifact
description: Build and maintain justfiles.

# Communicates the capability and user intent
description: Build and maintain Just command-runner files for repeatable project tasks.
```

## Checks

- The description names both capability and activation conditions.
- Every trigger phrase represents a distinct supported branch.
- A representative unrelated request does not appear to match.
- A request phrased by user outcome can activate the skill without requiring the tool or artifact name.
- Specialized names carry enough context for routing without unnecessary definitions.
- The body contains no routing guidance that arrived too late to affect activation.
- The value meets the current Agent Skills specification.

Static wording checks do not establish activation. Read [testing-guide.md](testing-guide.md) when creating or
repairing discovery behavior, and test through the target client's actual skill-selection mechanism.
