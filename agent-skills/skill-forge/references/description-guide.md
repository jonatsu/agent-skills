# Skill Descriptions

The description is the specification-defined routing pointer. It states what the skill does and when to use it.
Clients may preload, rank, display, or ignore it differently, so verify each declared client's behavior.

## Invocation and Scope

Use the invocation goal established during authoring. For an agent-selected skill, start from realistic user
requests for the job, including requests that do not name the skill or its tool. Put the most useful request
cue early. A file name or symptom earns space when it distinguishes work the skill actually handles, not
because that artifact happens to be present during unrelated work.

For explicit-only use, state the opt-in job without cues from ordinary surrounding work. Verify the intended
client's explicit invocation mechanism; restrictive wording alone does not enforce it. If the skill's job
supports both goals and the user has not chosen one, settle that choice before drafting.

For a portable skill, describe user tasks without relying on surrounding paths, configuration, installed
tools, clients, or repository conventions. Name a tool intrinsic to the job when it explains the capability,
without implying it is installed. For a repository-specific skill, name the repository and use local artifacts
only when they distinguish a request in its supported scope.

## Method

1. State the capability in concrete terms.
2. When the description names a specialized tool, product, or artifact, provide enough plain context for
   accurate activation. State the capability and user intent that the name represents. Do not define concepts
   the target agent can reasonably be expected to know or add background that does not improve routing.
3. Identify the distinct request branches the skill handles.
4. Represent each branch once using language a user is likely to use.
5. Add an exclusion only for a nearby skill or task that could plausibly be misrouted.
6. Remove implementation details and instructions that matter only after activation.

Distinct branches earn separate trigger language. Synonyms for the same branch usually do not. Long lists blur
boundaries and attract false positives. They also consume shared routing context in clients that preload descriptions.

Imperative phrasing can help an agent recognize a condition, but the absence of a literal `Use when` is not a
defect by itself. Check the request branches and near misses, not a fixed sentence pattern.

## Form and Length

Follow the target repository's scalar convention. An inline value on one logical line is a simple default;
some deployment tooling mishandles folded (`>-`) and literal (`|`) block scalars. Check the repository's
rules before using either form.

Budget the description by length, never by line width. A column ceiling such as markdownlint's MD013 governs
wrapped prose; a description cannot wrap while it stays an inline scalar, and Markdown tooling commonly treats
frontmatter as non-content and never inspects it. The Agent Skills specification caps a description at 1024
characters, which the reference validator enforces.

Staying under the cap is not the same as being affordable. Where a client preloads every description, the
collection pays that cost on every request. Spend it on distinct branches and necessary exclusions. A repository
MAY set a tighter budget than the specification and enforce it separately.

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
- For agent-selected skills, a request phrased by user outcome can select the skill without its exact name.
- For explicit-only skills, the description avoids ambient triggers and the client provides a verified
  invocation path.
- Every declared client has a verified automatic or explicit path for intended use.
- Specialized names carry enough context for routing without unnecessary definitions.
- The body contains no routing guidance that arrived too late to affect activation.
- The value meets the current Agent Skills specification.

Static wording checks do not establish activation. Read [testing-guide.md](testing-guide.md) to prepare
author-side discovery cases. Use the target client's actual mechanism only during an authorized full evaluation.
