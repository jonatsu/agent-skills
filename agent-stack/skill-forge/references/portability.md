# Portability

Check format, runtime, and client portability independently. A skill can satisfy one dimension while failing
another.

## Format Portability

Use fields defined by the Agent Skills specification for new portable skills. Store extension data as
string-valued entries under `metadata` when that representation is appropriate and client-neutral. Keep
product-specific extensions in optional named adapters.

Validate the result with `skills-ref`. Do not maintain a second copy of the external schema in the skill.

## Runtime Portability

Portable is the default when `metadata.scope` is absent. Portable skills:

- may require a tool intrinsic to their purpose;
- declare material runtime requirements in `compatibility`;
- refer to bundled files with relative paths from the skill root;
- make no assumptions about surrounding paths, configuration, installed tools, clients, or repository
  conventions;
- check optional surrounding tools before using them; and
- check required intrinsic dependencies before use and report their absence clearly.

A named dependency is legitimate when the skill is about that tool or cannot perform its stated capability
without it. Do not force a misleading fallback merely to appear tool-agnostic.

## Bundled Scripts Run Standalone

A bundled script ships to machines that have never seen the repository it was written in, so **a portable
skill's script MUST run from its deployed location with nothing around it but its own package**. The
deployment copies the skill directory; everything outside it is gone.

- **Resolve paths from the script's own location or from its arguments.** Reaching a sibling inside the same
  package is correct; walking upward out of the package is not. Take the target directory or file as a
  command-line argument rather than discovering it by climbing parents or by shelling out to a version-control
  tool.
- **Declare dependencies in the script itself.** Either restrict it to the standard library and say so in its
  module docstring, or carry PEP 723 inline script metadata so a runner resolves them on the spot. Never
  assume the authoring project's virtual environment, lockfile, task runner, or interpreter pinning exists.
- **Never read the authoring project's configuration.** A script that needs settings takes them as options
  with documented defaults.
- **Report a missing dependency by name** and exit with a distinct status, rather than failing on an import
  traceback a caller cannot interpret.

Environment coupling fails silently and late: the script keeps working for its author for months, and breaks
for the first person who installs the skill anywhere else.

A `repo-local` skill may bind to its repository's commands and paths, because that binding is its purpose.
**Prefer the standalone form there too.** A repository's layout, runner, and environment all move, and a
script wired into them breaks at the moment of the move, usually in someone else's change and with a failure
that names the script rather than the rename that caused it. Bind deliberately, to the smallest surface, and
keep the binding in one place.

## Client Portability

Name the clients the skill claims to support. For each client, verify the relevant contract:

- how it discovers or explicitly invokes a skill;
- which metadata it reads and when it loads the body;
- how bundled paths resolve;
- which tools, permissions, and network access exist; and
- whether scripts, continuation, and output delivery work as the skill assumes.

When the user names no client, target the specification-defined core. Do not claim client discovery or
behavior until a declared client is tested.

Deployment to a client proves file placement only. It does not prove discovery or correct behavior. Record an
untested client as a coverage limit.

Keep the specification-defined package as the portable core. Put product metadata, UI settings, invocation
syntax, and runner commands in named adapters. Add an adapter only when the user targets that product and its
current contract is verified. An optional adapter must not make the core unusable elsewhere.

The `agents/` directory is one possible product-extension location, not a universal requirement. Use a
product's current documentation before adding a file there. Do not infer one vendor's schema from another.

## Repository-Specific Skills

A repository-specific skill sets:

```yaml
metadata:
  scope: repo-local
```

It names the repository near the start of its body. It may then rely on that repository's commands, paths,
conventions, and checked-in tools because those bindings are part of its purpose. It still declares external
environment requirements and avoids assumptions about the author's machine.

`metadata.scope: repo-local` is this workflow's convention. Do not imply that a client enforces it unless that
client documents the behavior.

Before changing scope, check whether consumers expect the current portability boundary. Narrowing a portable
skill to one repository is a behavioral change, not a documentation cleanup.
