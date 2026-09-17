# Structuring Justfiles Across Files

Read this when a justfile is being split, when a split one behaves unexpectedly, or when choosing between an
import and a module. Confirm version-sensitive behavior against `just --man` for the installed version, or
against the Organization chapter of <https://just.systems/man/en/print.html>.

## Import or Module

Both pull a second file in. They differ in namespace, and that difference is the whole decision.

**`import` merges.** The imported definitions land in the importing file's namespace, as if written there. A
recipe in the parent can depend on an imported recipe, and an imported recipe can use the parent's variables
and settings. Use it when the definitions are one interface that has outgrown one file, or when several
justfiles share a common set of recipes.

**`mod` namespaces.** The module gets its own recipes, aliases, variables, and settings, and none of them are
visible to the parent or to a sibling module. Recipes are invoked as `just bar b` or `just bar::b`. Use it when
a subdirectory owns a lifecycle of its own, or when names need a prefix to stay unambiguous.

Modules cannot yet refer to another module's variables. A justfile that needs shared values across modules
either passes them as arguments or keeps that part flat.

## Imports

```just
import 'foo/bar.just'
import? 'optional/local.just'
```

- The path is absolute or relative to the file containing the `import`; a leading `~/` expands to the home
  directory.
- Justfiles are order-insensitive, so an imported file may reference definitions that appear after its
  `import` statement, and imports nest recursively.
- `import?` makes a missing file not an error. This is the mechanism for an optional per-developer or
  per-machine overlay.
- Importing the same file along two paths is not an error, so two imported files may both import a third.

**Duplicate definitions.** A duplicate is an error unless `set allow-duplicate-recipes` or
`set allow-duplicate-variables` is in force. With them, shallower wins: a definition in the importing file
overrides one from an import, which overrides one from a deeper import. Between two duplicates at the same
depth, the **earlier** import wins — the opposite of the "last one wins" most configuration formats use.
Upstream considers this a bug held in place by backwards compatibility, so do not build an override scheme on
it. Prefer arranging for the override to live at a shallower depth.

## Modules

```just
mod bar
mod tools 'path/to/tools.just'
mod? optional-stack
```

- `mod` statements stabilized in Just 1.31.0. Check `just --version` before introducing one.
- For `mod foo`, Just searches `foo.just`, `foo/mod.just`, `foo/justfile`, and `foo/.justfile`. The last two
  may carry any capitalization.
- `mod foo 'PATH'` loads from `PATH` instead, which may name the source file itself or a directory containing
  `mod.just`, `justfile`, or `.justfile`. A leading `~/` expands to the home directory.
- `mod?` makes a missing source file not an error. A recipe depending on a missing optional module, directly or
  transitively, is disabled: invoking it is an error, while the rest of the file still runs. Several `mod?`
  statements may share a name with different paths, as long as at most one file exists.
- A comment above a `mod` statement becomes the module's doc comment in `just --list`.

**Working directory is the trap.** A recipe in a submodule runs with the working directory set to the directory
containing the submodule's source file, unless it carries `[no-cd]`. A recipe moved from a root justfile into a
module therefore runs somewhere else, and any relative path in it silently changes meaning. Check relative
paths as part of the move rather than after the first failure.

`justfile()` and `justfile_directory()` are not affected: they always name the root justfile and its directory,
even inside a submodule recipe. They are the reliable way to reach a repository-root-relative path from a
module.

Environment files load per module under that module's settings, and a parent's environment variables are
visible in its children.

## Converting a Flat Justfile

A root justfile whose recipes cluster into `deploy-*`, `test-*`, and `check-*` groups, with a subdirectory that
already has its own justfile reached by a hand-written forwarding recipe:

1. **Name the clusters against the trigger.** A cluster earns a module when it owns a lifecycle or needs its
   prefix to disambiguate. A cluster that is merely long earns a group or an import instead. Do not convert
   every banner comment into a module.
2. **Adopt the justfile that already exists.** A recipe of the form `cd sub && just sub-task` is a module
   already, forwarded by hand and exposing one recipe instead of all of them. Replace it with `mod sub 'sub'`
   and the whole subdirectory interface becomes `just sub::…`.
3. **Move one cluster at a time**, and after each, check relative paths against the module's new working
   directory, and re-add any setting the cluster depended on — settings do not cross the module boundary.
4. **Drop the prefix from moved recipe names.** `test-vault` inside `mod vault` becomes `vault::test`; leaving
   it produces `vault::test-vault`.
5. **Re-check the interface** with `just --list`, `just --list <module>`, and `just --groups`. A recipe that
   vanished is usually private, shadowed by a duplicate, or disabled behind a missing optional module.
6. **Keep the aggregate recipes at the root.** A recipe like `check` that fans out across modules stays in the
   root justfile and depends on `module::recipe` targets.
