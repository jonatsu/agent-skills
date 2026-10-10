# Script Decisions

Use a bundled script when deterministic execution materially improves reliability or avoids repeatedly
recreating the same operation.

Run traces are the strongest signal. When the traces of several test or real-use runs show each one writing
the same helper, bundle that helper as a script: every run is already paying to rebuild it, and each rebuild
is a fresh chance to get it wrong.

Use an existing tool directly for a simple one-off command. Do not bundle a script merely to wrap an available
command. Pin a version only when repeatability requires it, with the reason beside the pin (see *Version facts*
in `authoring.md`), and declare runtime prerequisites in `SKILL.md` or `compatibility`.

Good candidates include:

- exact parsing, transformation, or validation;
- repeated operations with a stable interface;
- fragile command sequences whose errors are hard to diagnose; and
- calculations or output formats that must be reproducible.

Keep work in agent instructions when it depends on judgment, varies substantially by context, or is clearer as
a direct tool call. Determinism alone does not justify a script when the operation is trivial and unlikely to
recur.

Write each bundled script to its language's established conventions. Use the coding guidance your environment
supplies for that language, such as installed skills, rules, or a style guide the repository declares, and load
it before the script's first line. Where no such guidance exists, follow the language's community standard and
its standard formatter, linter, and type checker. A portable script stays self-contained, so a convention that
needs a dependency or an import from outside the package yields to that constraint. Say so in a comment where a
reader would otherwise read it as an oversight.

For every bundled script:

- document its purpose, invocation, dependencies, and result at the point of use;
- say whether the agent should execute it or inspect it as reference;
- accept input through arguments, environment variables, or standard input without interactive prompts;
- provide concise `--help` output with purpose, arguments, options, and representative usage;
- state what failed, what was expected, and the next corrective action in anticipated errors;
- emit structured results on standard output and diagnostics on standard error when composition matters;
- use meaningful, documented exit statuses;
- reject ambiguous input instead of guessing;
- provide a dry-run or equivalent preview for destructive or stateful work;
- use safe defaults and require explicit selection for consequential behavior;
- limit large terminal output or require an explicit output destination;
- avoid authoring-machine assumptions;
- test representative success, invalid-input, and dependency-failure paths; and
- keep implementation details out of `SKILL.md` unless they affect correct use.

## Stateful Script Contracts

For scripts that change state, document the behavior of repeated invocation: how an already-completed
operation is recognized, when retry is safe, and what the caller must do after partial or uncertain
completion. Identify any existing tool guarantee the script relies on and verify that it applies to the
actual invocation. Use the [operational-workflow contract](operational-workflows.md) when these decisions span
several operations or invocations.

Where recovery depends on the distinction, make completed, partial, and unknown outcomes distinguishable.
Return the operation identity or other evidence the caller needs to inspect or continue the work. Do not
report success merely because a request was accepted.

Pure transformations need no operation identity or recovery state when repeating them has no consequential
effect. Match the interface to the caller's actual decisions.

## Vendored Tools

Vendored tools are a separate case. Keep their upstream source and license intact, pin the revision, record
omissions or modifications in `ATTRIBUTIONS.md`, and invoke them through their declared runtime rather than
absorbing their logic into the skill's own scripts.
