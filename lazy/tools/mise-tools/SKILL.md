---
name: mise-tools
description: Manage tool versions, environments, and tasks with mise. Use for mise.toml, .miserc.toml, mise.lock, mise installation or activation, wrong tool versions, missing shims, and configuration or task failures in mise-managed environments.
license: MIT
compatibility: Mise is required for runtime inspection and verification.
metadata:
  author: Joonas Onatsu
---

# Mise Tools

Use the narrowest mise scope and activation model that satisfies the request. For a new project setup, default
to project-local configuration and command-scoped execution. Do not edit shell startup files or global mise
configuration unless the user requested that scope or separately approved it.

## Route the Task

For a routine command in an existing project, inspect the active config and use the project's established
mise path. Do not impose a setup workflow.

| Task                                                              | Load                                                                              |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Install or activate mise; configure CI, bootstrap, or containers  | [install-and-activation.md](references/install-and-activation.md)                 |
| Bound a large or slow cold install without throttling daily tasks | [install-and-activation.md](references/install-and-activation.md)                 |
| Change config scope, environment layers, or discovery boundaries  | [config-and-env.md](references/config-and-env.md)                                 |
| Add tools, tasks, hooks, lockfiles, or backend options            | [tools-tasks-and-isolation.md](references/tools-tasks-and-isolation.md)           |
| Change TOML keys, types, or structure                             | [schemas.md](references/schemas.md), plus the relevant behavior reference         |
| Use Tera, `.miserc.toml`, `MISE_ENV`, or platform environments    | [templating-and-early-init.md](references/templating-and-early-init.md)           |
| Use the `go:` backend or diagnose unexpected Go paths             | [go-backend.md](references/go-backend.md)                                         |
| Diagnose surprising behavior, missing tools, or broken shims      | [operations-and-troubleshooting.md](references/operations-and-troubleshooting.md) |

Use installed CLI help and current upstream documentation for version-sensitive behavior.

## Preflight Safety

Inspect unfamiliar config and task files as text before running a mise command that loads them. Config can
execute Tera `exec()` or `read_file()`, environment sources, hooks, and tasks. Use `MISE_SAFE=1` for compatible
inspection outside the user's trust boundary. Safe mode refuses executable behavior and project environment
injection; treat that as reduced capability rather than bypassing it.

Keep `MISE_STATE_DIR` and `MISE_CACHE_DIR` outside the project, including in tests. Mise stores trusted-config
symlinks in its state directory, so project-local state can create a recursive walk through the repository.

`mise exec` enables `exec_auto_install` by default. Inspect installed tools with `mise ls` first. When
installation is not authorized, set `MISE_EXEC_AUTO_INSTALL=false` and stop if the required tool is absent.
Combine this with safe mode when the config is untrusted.

## Choose Scope and Execution

Inspect existing `mise.toml`, local and environment overlays, `.miserc.toml`, `mise.lock`, task files, shell
activation, and ancestor configs before changing setup. Preserve the repository's established model unless the
request requires a different one.

Prefer:

- `mise.toml` for shared project configuration;
- `mise.local.toml` for developer-specific values and secrets after confirming it is ignored;
- `mise.<env>.toml` for named environment overlays;
- `.miserc.toml` only for early environment selection or config-search boundaries;
- `mise exec -- <command>` for scripts, CI, and agent-run commands;
- `mise activate <shell>` for an explicitly requested interactive-shell integration; and
- shims when editors or non-interactive shells need tool lookup without prompt hooks.

Scope by the consumer, not the author. A tool used only inside a repository's own commands belongs in that
repository's `mise.toml`. But a tool invoked by a process the harness spawns from an arbitrary working
directory — an editor hook, an MCP server launcher, a connect-time credential helper — must go in the global
config: its shim sits on `PATH` everywhere, yet resolves a version only from the config active in the caller's
directory, so a repo-local declaration fails with `No version is set for shim: <tool>` anywhere else. "Narrowest
scope" is bounded below by where the tool actually runs, which is not always where it is declared.

Use exact pins or a committed lockfile when the requested workflow must reproduce across machines. A request
to create or update a reproducible mise setup authorizes the expected project lockfile write. Ask before
replacing unresolved user changes or adding a lockfile when the request does not establish that intent.

Keep secrets out of committed configuration. Prefer explicit tasks to automatic hooks. Label experimental
features and verify that the installed mise version supports them.

Before storing secrets locally, confirm that version control ignores `mise.local.toml`,
`mise.*.local.toml`, `mise.local.lock`, and `mise.*.local.lock`. Add the applicable patterns when the request
authorizes repository ignore changes. If mise is unavailable, installation guidance still applies, but report
runtime validation as omitted.

TOML table headers retain scope until another header begins. When a flat `[tools]` list also contains
`[tools."backend:configured-tool"]` subtables, place every flat sibling before the first tool subtable. A file
can parse and match the schema while later tools are silently owned by the wrong table. After structural
edits, inspect the parsed `tools` tree before executing mise; see `config-and-env.md`.

## Trust and State Changes

Start with `mise trust --show` when trust may explain a failure. In normal mode, `mise exec`, `mise run`, naked
task invocations, `mise install`, and `mise watch` automatically trust active config. Run them only when the
user's authority covers the config behavior and persistent trust transition. Run `mise trust <config>` only
when the selected mode requires explicit trust and the user authorized that persistent state change.

Installation, lock updates, shell edits, global config changes, and task execution can change state. Diagnosis
alone does not authorize them. Inspect first, then perform the smallest state change supported by evidence when
the user requested a repair or setup. Treat destructive task bodies, force reinstallations, deploys, and
publishes according to their actual impact and the host agent's authorization rules.

## Diagnose Before Repairing

Begin with read-only evidence appropriate to the symptom:

1. Record `mise --version` and relevant environment or execution context.
2. Inspect applicable config and task files as text, including active ancestor files, then check
   `mise trust --show`.
3. Inspect `mise doctor`, `mise cfg`, and `mise env` as applicable, using safe mode outside the trust boundary.
4. Inspect installed and configured tools with `mise ls`; inspect tasks with `mise tasks` when relevant.
5. Reproduce through the intended path, such as `mise exec -- <tool> --version`, only after applying the trust
   and auto-install controls above.

Do not run `mise install` merely to diagnose activation or config resolution. When missing tools are the
supported cause and installation is authorized, preview with `mise install --dry-run` when useful, install the
required scope, and repeat the original reproduction.

## Verify the Result

For a config edit, require all of these before completion:

- the file parses and its structured view shows every edited key under the intended owner;
- `mise ls` still contains an unaffected sibling tool when the edit changed `[tools]` structure;
- the affected tool or task behaves through the same path the user will use; and
- verification caused no unauthorized install, trust transition, lock update, or shell edit.

Match runtime verification to the consumer:

- command-scoped automation: `mise exec -- <command>` with the applicable trust and installation authority;
- interactive activation: a fresh or re-sourced target shell;
- shims: tool lookup from the intended non-interactive context;
- tasks: the affected task and any relevant dependency view;
- locked setup: the project's locked install path; and
- containers or system installs: the intended user after the expected mounts are present.

Report changed files, checks actually run, and any manual activation or installation step that remains. Do not
claim an install, trust transition, or clean-environment reproduction that was not performed.
