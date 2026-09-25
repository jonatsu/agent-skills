---
name: just-task-runner
description: Create, organize, debug, and run justfiles for repeatable project commands. Use when changing recipes, parameters, dependencies, or shell settings; splitting a long justfile into imports or modules; diagnosing Just parsing, quoting, working-directory, or execution failures; validating recipe behavior; or running Just recipes in GitHub Actions. Use mise-tools for mise tasks and toolchain configuration.
license: MIT
compatibility: Just is required for local parsing, formatting, and runtime verification.
metadata:
  author: Joonas Onatsu
---

# Just Task Runner

Treat a justfile as a thin project interface over commands the project already owns. Preserve the repository's
task names, structure, shell choices, and validation conventions. Do not impose a universal recipe catalogue,
layout, default recipe, shell, or dotenv policy.

Check feature syntax and minimum versions in the manual instead of relying on memory:

- `just --man` renders the manual for the installed version, which is the one that matters. Prefer it.
- <https://just.systems/man/en/print.html> is the entire current manual as one page. Fetch this when reading
  the manual over the network; it needs no navigation and no second request.
- <https://just.systems/man/en/> is the same manual paginated, for a single named section.

## Establish the Context

Read the applicable repository instructions and the target justfile. Follow its imports and modules when they
affect the requested work. Inspect package manifests, scripts, and continuous-integration configuration when
they affect the requested recipes.

Record `just --version` before relying on version-sensitive syntax; much of what follows arrived in a specific
release. If Just is unavailable, state that local validation cannot be performed.

Just runs project commands; it does not track build inputs and outputs. Keep an established build system in
charge of its own work unless the user asks to replace it.

## Inspect and Run Recipes Safely

Use the narrowest command that answers the question:

- `just --list` or `just --summary` for discovery, and `just --groups` for the group names in use;
- `just --show <recipe>` to inspect one recipe and its dependencies;
- `just --dump` to parse and inspect the complete resolved justfile;
- `just --evaluate` to inspect variables after reviewing their definitions; and
- `just --dry-run <recipe> [arguments]` to preview the selected command lines.

`--list` and `--summary` omit recipes and aliases whose name starts with `_` and those carrying `[private]`.
They are an inventory of the public interface, not of the file. Use `just --dump` before reporting that a
recipe does not exist, or before adding one that may already exist as a helper.

Variable evaluation can execute backticks and `shell(...)`. Inspect definitions with `just --dump` before
running `just --evaluate`, then confirm that any command effects are within the user's authority.

A recipe can also run arbitrary commands. Inspect its body and dependencies before execution, and judge
authority from the resulting effects rather than from the recipe name. A dry run does not grant permission
or prove that the real command will succeed.

`just --yes` automatically confirms every `[confirm]` recipe in the invocation, including ones reached through
dependencies. Do not pass it to work around a prompt.

## Match the Structure to the Size

A flat justfile with doc comments is the right structure, and stays right until a specific problem appears.
Climb a rung only when its trigger has fired, and name the trigger when proposing the change.

| Trigger                                                                                | Mechanism                                                      |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| A reader scans past the recipe they wanted in `just --list`                            | `[group('name')]` on recipes and modules                       |
| A recipe exists only to be depended on                                                 | `_` name prefix, or `[private]` to hide it without renaming    |
| Two recipes share a long invocation prefix                                             | A `:=` variable holding the prefix                             |
| Two recipes differ only in an argument or flag                                         | One parameterized recipe, invoked through dependency arguments |
| The file is too long to read, but its definitions belong to one namespace              | `import`                                                       |
| A subdirectory owns a lifecycle of its own, or names need a prefix to stay unambiguous | `mod`                                                          |

Comment banners help source readers but do not appear in `just --list` or `just --groups`. Use groups when
callers need that organization; `--list --unsorted` retains their file order.

Groups and modules compose but solve different problems: a group organizes one file's listing, a module splits
namespace and file. A justfile that has just gained modules usually needs fewer groups, not the same groups
repeated per module.

When splitting is the answer, read [references/structuring-justfiles.md](references/structuring-justfiles.md)
for import and module mechanics, path resolution, working-directory semantics, and a worked conversion.

## Author Recipes Deliberately

Preserve existing naming and composition patterns. Add only recipes required by the request or established
project workflows.

### Make the Interface Legible Through Just, Not Comments

The comment line immediately above a recipe becomes its doc comment in `just --list`. `[doc('text')]` overrides
it and a bare `[doc]` suppresses it. Keep a recipe's summary in that position rather than in a block of
commentary that only a source reader sees. Do not record a recipe's history, or what it replaced, in the
justfile; that belongs in the commit message or a decision record.

### Keep One Definition of a Repeated Thing

Assign a repeated invocation prefix to a `:=` variable, and collapse recipes that differ by one argument into a
parameterized recipe reached through dependency arguments:

```just
run := 'uv run --locked'

_deploy-config mode:
    {{run}} python tools/deploy.py --target prod {{mode}}

# Report what deployment would change.
check-config: (_deploy-config '--check')

# Preview the exact keys deployment would change.
diff-config: (_deploy-config '--dry-run')
```

Use recipe dependencies for fixed task relationships, and `&&` post-dependencies for work that must follow the
body. Use recursive `just` calls only when runtime selection, iteration, or another dynamic relationship
requires them. When a dependency list grows long enough to be unreadable, that is a signal the recipes below it
belong in groups or a module, not that the list needs a comment.

Keep recipes thin when another project command already owns the logic. Put substantial shell logic in an
appropriate script, or in a script recipe when keeping it in the justfile remains cohesive. A line that chains
commands with `;` and `||` to carry an exit status is a script recipe written in the wrong place.

### Treat File-Wide Settings as a Contract

Add a setting only when the project wants its global effect, and prefer one setting to the same prefix repeated
on every line. `set quiet` replaces a per-line `@`, with `[no-quiet]` on the recipes that should still echo.
Shell replacement, dotenv loading, environment export, and working-directory changes each alter every recipe in
the file or module, so introduce them as a deliberate decision rather than to fix one recipe.

### Control Shell State, Argument Boundaries, and Risk

Ordinary recipe lines run in separate shell invocations. Use one shell line or a script recipe when
working-directory changes, variables, traps, or shell state must persist across commands. State does not cross
recipes at all, so a recipe cannot activate an environment for a later one — invoke the environment's binaries
directly, as with a virtualenv's `./venv/bin/python`, instead of sourcing an activation script. A script
recipe's body also does not abort on a failing line the way separate recipe lines do; give it the target
shell's error handling.

Treat `{{ ... }}` as text inserted before the recipe shell parses the command, so an argument containing
whitespace or quotes splits into several shell words. Three mechanisms fix it, and the trade-off picks between
them:

- manually quoting the interpolation keeps Just's undefined-variable check but breaks when a value contains
  the enclosing quote character; `quote()` also keeps the check and escapes single quotes for Bourne-compatible
  shells;
- `set positional-arguments` with `"$@"` preserves arbitrary boundaries, and is the choice when a recipe takes
  values it does not control; and
- exporting the parameter with `set export` or a `$` prefix handles any value but defeats the
  undefined-variable check, since a misspelled `$name` is no longer caught before running.

For a shell that is not Bourne-compatible, use that shell's own argument-safe mechanism.

Every value except the empty list is truthy, including the empty string. A parameter defaulting to `''` is
true in `if` and `assert()`; use `[]` as the false default when a parameter is a flag.

Make mutating, destructive, deployment, and publishing recipes explicit about their effects, and validate exact
targets before destructive commands. A Just confirmation attribute supplements the caller's authorization; it
does not replace it.

`[cache]` is unstable, applies only to script recipes, and skips work based on a key you are responsible for
completing. Nothing verifies that the key captures the inputs that actually determine the output, so an
incomplete key is a correctness defect rather than a performance one. Do not introduce caching unless the user
asked for it.

When the recipe contains non-trivial Bash or POSIX shell behavior, apply the relevant shell skill to that body.
When the task concerns mise tasks or toolchain configuration, use the mise skill.

## Run Recipes in GitHub Actions

When a workflow needs Just, inspect its existing tool installation and version policy. If it does not already
install Just, use [extractions/setup-just](https://github.com/extractions/setup-just) before the first `just`
step. Check the action's current README for the release tag and inputs rather than copying a remembered version.
Set `just-version` when the project pins its toolchain or needs a minimum feature; the action otherwise selects
the latest matching Just release. For a basic workflow with checkout already configured:

```yaml
steps:
  - uses: extractions/setup-just@v4
  - run: just check
```

Keep the workflow's working directory and environment consistent with local invocation. Preview the recipe
and its dependencies before placing it in CI, especially when it writes, deploys, or needs secrets. Verify the
workflow's selected Just version supports the justfile syntax.

## Diagnose Failures

Separate failures into four stages: parsing, expression evaluation, recipe execution, and the invoked tool.
Reproduce the exact recipe and arguments, then inspect the smallest relevant definition with `just --show`.

Check these common boundaries before changing code:

- whether the installed Just version supports the syntax;
- whether separate recipe lines lost shell state;
- whether interpolation changed quoting or argument boundaries;
- whether a dependency failed before the selected recipe ran;
- whether imports merged definitions while modules namespaced them, and which of two duplicate definitions
  won;
- whether the recipe ran from the root directory, the directory of its own module's source file, or a
  directory an explicit setting selected; and
- whether the missing recipe is private rather than absent.

Fix the owning layer. Do not hide a failing underlying command with ignored statuses, unconditional success,
or a wrapper recipe that discards its error.

## Verify the Result

Validate through the same justfile and working directory the user will use:

1. Parse the resolved file with `just --dump`.
2. Run `just --fmt --check` when the installed version supports it and formatting is in scope. Report a
   pre-existing formatting difference instead of rewriting unrelated content.
3. Compare `just --list` and `just --groups` against the interface the change intended, including each
   module's own listing.
4. Preview each changed execution path with `just --dry-run`, including representative parameters and relevant
   module paths. When the change was meant to preserve behavior, capture `just --summary` and the `--dry-run`
   output of every affected recipe before and after, and diff them. Identical output is the evidence that a
   restructuring changed only structure; each remaining difference is then something to justify individually
   rather than a whole file to re-read.
5. Execute safe representative recipes when authorized, and verify their outputs, exit statuses, dependencies,
   and working directories.
6. Exercise expected failure paths when the change affects validation, parameters, platform branches, or
   destructive-target guards.

Parsing and dry-run output do not establish runtime behavior. Report the checks performed, checks omitted, and
the Just version used.
