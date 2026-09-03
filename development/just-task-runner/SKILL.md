---
name: just-task-runner
description: Build and maintain Just command-runner files for repeatable project tasks.
license: MIT
compatibility: Just is required for local parsing, formatting, and runtime verification.
metadata:
  author: Joonas Onatsu
---

# Just Task Runner

Treat a justfile as a thin project interface over commands the project already owns. Preserve the repository's
task names, structure, shell choices, and validation conventions. Do not impose a universal recipe catalogue,
layout, default recipe, shell, or dotenv policy.

## Establish the Context

Read the applicable repository instructions and the target justfile. Follow its imports and modules when they
affect the requested work. Inspect package manifests, scripts, and continuous-integration configuration only
as needed to understand the commands that recipes should expose.

Record `just --version` before relying on version-sensitive syntax. Use `just --help`, `just --man`, and the
[official manual](https://just.systems/man/en/) as the runtime sources for supported settings, attributes,
functions, and command-line options. If Just is unavailable, state that local validation cannot be performed.

Just is a command runner rather than an incremental build system. Do not recommend replacing an established
task runner or build system unless the user asked for that decision.

## Inspect and Run Recipes Safely

Use the narrowest command that answers the question:

- `just --list` or `just --summary` for discovery;
- `just --show <recipe>` to inspect one recipe and its dependencies;
- `just --dump` to parse and inspect the complete resolved justfile;
- `just --evaluate` to inspect variables after reviewing their definitions; and
- `just --dry-run <recipe> [arguments]` to preview the selected command lines.

Variable evaluation can execute backticks and `shell(...)`. Inspect definitions with `just --dump` before
running `just --evaluate`, then confirm that any command effects are within the user's authority.

A recipe can also run arbitrary commands. Inspect its body and dependencies before execution, and judge
authority from the resulting effects rather than from the recipe name. A dry run does not grant permission
or prove that the real command will succeed.

## Author Recipes Deliberately

- Preserve existing naming and composition patterns. Add only recipes required by the request or established
  project workflows.
- Keep recipes thin when another project command already owns the logic. Put substantial shell logic in an
  appropriate script or use a script recipe when keeping it in the justfile remains cohesive.
- Remember that ordinary recipe lines run in separate shell invocations. Use one shell line or a script recipe
  when working-directory changes, variables, traps, or shell state must persist across commands.
- Use recipe dependencies for fixed task relationships. Use recursive `just` calls only when runtime selection,
  iteration, or another dynamic relationship requires them.
- Treat `{{ ... }}` as text inserted before the recipe shell parses the command. For Bourne-compatible shells,
  use `quote()` when a scalar parameter must remain one shell argument. For other shells, use that shell's
  argument-safe mechanism. Preserve arbitrary argument boundaries with a target-shell mechanism such as
  positional arguments with `"$@"` in a Bourne-compatible shell.
- Use an import when definitions should share a namespace. Use a module when recipes need a separate namespace.
  Split files only when ownership or size makes the boundary useful.
- Add file-wide settings such as dotenv loading, environment export, shell replacement, or working-directory
  changes only when the project contract requires their global effect.
- Make mutating, destructive, deployment, and publishing recipes explicit about their effects. Validate exact
  targets before destructive commands. A Just confirmation attribute supplements the caller's authorization;
  it does not replace it.

When the recipe contains non-trivial Bash or POSIX shell behavior, apply the relevant shell skill to that body.
When the task concerns mise tasks or toolchain configuration rather than Just, use the mise skill.

## Diagnose Failures

Separate failures into four stages: parsing, expression evaluation, recipe execution, and the invoked tool.
Reproduce the exact recipe and arguments, then inspect the smallest relevant definition with `just --show`.

Check these common boundaries before changing code:

- whether the installed Just version supports the syntax;
- whether separate recipe lines lost shell state;
- whether interpolation changed quoting or argument boundaries;
- whether a dependency failed before the selected recipe ran;
- whether imports merged definitions while modules namespaced them; and
- whether the recipe ran from the directory selected by Just or an explicit working-directory setting.

Fix the owning layer. Do not hide a failing underlying command with ignored statuses, unconditional success,
or a wrapper recipe that discards its error.

## Verify the Result

Validate through the same justfile and working directory the user will use:

1. Parse the resolved file with `just --dump`.
2. Run `just --fmt --check` when the installed version supports it and formatting is in scope. Report a
   pre-existing formatting difference instead of rewriting unrelated content.
3. Preview each changed execution path with `just --dry-run`, including representative parameters and relevant
   module paths.
4. Execute safe representative recipes when authorized, and verify their outputs, exit statuses, dependencies,
   and working directories.
5. Exercise expected failure paths when the change affects validation, parameters, platform branches, or
   destructive-target guards.

Parsing and dry-run output do not establish runtime behavior. Report the checks performed, checks omitted, and
the Just version used.
