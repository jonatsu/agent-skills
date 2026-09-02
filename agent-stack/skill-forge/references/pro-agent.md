# Script Decisions

Use a bundled script when deterministic execution materially improves reliability or avoids repeatedly
recreating the same operation.

Good candidates include:

- exact parsing, transformation, or validation;
- repeated operations with a stable interface;
- fragile command sequences whose errors are hard to diagnose; and
- calculations or output formats that must be reproducible.

Keep work in agent instructions when it depends on judgment, varies substantially by context, or is clearer as
a direct tool call. Determinism alone does not justify a script when the operation is trivial and unlikely to
recur.

For every bundled script:

- document its purpose, invocation, dependencies, and result at the point of use;
- say whether the agent should execute it or inspect it as reference;
- emit actionable errors for anticipated failures;
- avoid authoring-machine assumptions;
- test representative success, invalid-input, and dependency-failure paths; and
- keep implementation details out of `SKILL.md` unless they affect correct use.

Vendored tools are a separate case. Keep their upstream source and license intact, pin the revision, record
omissions or modifications in `ATTRIBUTIONS.md`, and invoke them through their declared runtime rather than
absorbing their logic into the skill's own scripts.
