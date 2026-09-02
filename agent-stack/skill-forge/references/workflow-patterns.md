# Workflow Patterns

Choose control flow from the task's real dependencies. Most skills need ordinary prose or one simple sequence.

## Available Patterns

- **Sequence:** use when one result is required by the next step.
- **Branch:** use when input, user choice, or environment selects materially different instructions.
- **Iteration:** use when an observable quality criterion supports repeated improvement.
- **Delegation:** use when independent work can run concurrently and the target environment supports agents.
- **Degradation:** use when an optional capability may be unavailable and a truthful reduced result remains useful.
- **Template:** use when downstream consumers require a stable output structure.

Do not turn these patterns into skill categories or combine them without a concrete need.

## Checklists

Use a checklist when a long session could lose a required order, prerequisite, or completion state. Each item should end in
an observable result. Independent rules and judgment do not need numbered steps.

## Confirmation Gates

Reuse authorization already present in the user's request and the host agent's policies. Add a gate when a later choice,
cost, disclosure, destructive target, or outward-facing action cannot be understood or authorized earlier. State exactly
what decision or authority is required.

## Output Contracts

Use a strict template when software or a formal process consumes the output. Use a flexible outline when only information
order matters. Avoid templates that standardize phrasing without improving correctness or use.
