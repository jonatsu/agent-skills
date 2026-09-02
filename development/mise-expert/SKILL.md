---
name: mise-expert
description: Configure and operate mise toolchains, environments, tasks, activation, and lockfiles. Use when a request explicitly involves mise, mise.toml, .miserc.toml, mise tasks or backends, or migration from asdf or direnv to mise.
license: MIT
compatibility: Mise is required for runtime inspection and verification; installation guidance can be used before it is available.
metadata:
  author: Joonas Onatsu
---

# Mise Expert

Use the narrowest mise scope and activation model that satisfies the request. For a new project setup, default
to project-local configuration and command-scoped execution. Do not edit shell startup files or global mise
configuration unless the user requested that scope or separately approved it.

## Route the Task

- For a routine command in an existing project, inspect the active config and run the command through the
  project's established mise path. Do not impose a setup workflow.
- For installation, shell activation, CI, bootstrap, or containers, read
  [references/install-and-activation.md](references/install-and-activation.md).
- For config layering, environment selection, or parent-config leakage, read
  [references/config-and-env.md](references/config-and-env.md).
- For tools, tasks, hooks, lockfiles, or backend choice, read
  [references/tools-tasks-and-isolation.md](references/tools-tasks-and-isolation.md).
- For `.miserc.toml`, Tera templates, or platform environments, also read
  [references/templating-and-early-init.md](references/templating-and-early-init.md).
- For the `go:` backend, `go.*` settings, or unexpected Go cache paths, read
  [references/go-backend.md](references/go-backend.md).
- For surprising behavior or failures, read
  [references/operations-and-troubleshooting.md](references/operations-and-troubleshooting.md).

Consult the relevant upstream JSON Schema when adding or changing config keys, field types, or structure, or
when their validity is uncertain. [references/schemas.md](references/schemas.md) maps config files to schemas.
Use the installed CLI help and current upstream documentation for version-sensitive behavior instead of
relying on remembered syntax.

## Choose Scope and Execution

Inspect existing `mise.toml`, local and environment overlays, `.miserc.toml`, `mise.lock`, task files, shell
activation, and ancestor configs before changing setup. Preserve the repository's established model unless the
request requires a different one.

Prefer:

- `mise.toml` for shared project configuration;
- `mise.local.toml` for developer-specific values and secrets;
- `mise.<env>.toml` for named environment overlays;
- `.miserc.toml` only for early environment selection or config-search boundaries;
- `mise exec -- <command>` for scripts, CI, and agent-run commands;
- `mise activate <shell>` for an explicitly requested interactive-shell integration; and
- shims when editors or non-interactive shells need tool lookup without prompt hooks.

Use exact pins or a committed lockfile when the requested workflow must reproduce across machines. A request
to create or update a reproducible mise setup authorizes the expected project lockfile write. Ask before
replacing unresolved user changes or adding a lockfile when the request does not establish that intent.

Keep secrets out of committed configuration. Prefer explicit tasks to automatic hooks. Label experimental
features and verify that the installed mise version supports them.

## Trust and State Changes

Start with `mise trust --show` when trust may explain a failure. Normal execution commands automatically trust
active config in normal mode, and safe configs need no trust. Run `mise trust <config>` only when the selected
mode requires explicit trust and the user authorized that persistent state change.

Installation, lock updates, shell edits, global config changes, and task execution can change state. Diagnosis
alone does not authorize them. Inspect first, then perform the smallest state change supported by evidence when
the user requested a repair or setup. Treat destructive task bodies, force reinstallations, deploys, and
publishes according to their actual impact and the host agent's authorization rules.

## Diagnose Before Repairing

Begin with read-only evidence appropriate to the symptom:

1. Record `mise --version` and relevant environment or execution context.
2. Inspect `mise doctor`, `mise cfg`, `mise env`, and `mise trust --show` as applicable.
3. Inspect installed and configured tools with `mise ls`; inspect tasks with `mise tasks` when relevant.
4. Reproduce through the intended path, such as `mise exec -- <tool> --version`, only when running that command
   is safe.

Do not run `mise install` merely to diagnose activation or config resolution. When missing tools are the
supported cause and installation is authorized, preview with `mise install --dry-run` when useful, install the
required scope, and repeat the original reproduction.

## Verify the Result

Verify the same path the user will use:

- command-scoped automation: `mise exec -- <command>`;
- interactive activation: a fresh or re-sourced target shell;
- shims: tool lookup from the intended non-interactive context;
- tasks: the affected task and any relevant dependency view;
- locked setup: the project's locked install path; and
- containers or system installs: the intended user after the expected mounts are present.

Report changed files, checks actually run, and any manual activation or installation step that remains. Do not
claim an install, trust transition, or clean-environment reproduction that was not performed.
