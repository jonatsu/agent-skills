# Script Decisions

Use a bundled script when deterministic execution materially improves reliability or avoids repeatedly
recreating the same operation.

Use an existing tool directly for a simple one-off command. Do not bundle a script merely to wrap an available
command. Pin versions when repeatability matters, and declare runtime prerequisites in `SKILL.md` or
`compatibility`.

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
- accept input through arguments, environment variables, or standard input without interactive prompts;
- provide concise `--help` output with purpose, arguments, options, and representative usage;
- state what failed, what was expected, and the next corrective action in anticipated errors;
- emit structured results on standard output and diagnostics on standard error when composition matters;
- use meaningful, documented exit statuses;
- behave safely under retries and remain idempotent where practical;
- reject ambiguous input instead of guessing;
- provide a dry-run or equivalent preview for destructive or stateful work;
- use safe defaults and require explicit selection for consequential behavior;
- limit large terminal output or require an explicit output destination;
- avoid authoring-machine assumptions;
- test representative success, invalid-input, and dependency-failure paths; and
- keep implementation details out of `SKILL.md` unless they affect correct use.

Vendored tools are a separate case. Keep their upstream source and license intact, pin the revision, record
omissions or modifications in `ATTRIBUTIONS.md`, and invoke them through their declared runtime rather than
absorbing their logic into the skill's own scripts.
