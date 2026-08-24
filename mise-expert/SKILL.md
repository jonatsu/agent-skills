---
name: mise-expert
description: Mise toolchain setup, isolated development environments, mise.toml, mise.local.toml, mise.lock, .miserc.toml, tool installs, task runner, env activation, shell hooks, trust, CI, Docker, bootstrap, backend selection, troubleshooting. Use when setting up or operating a project with mise, replacing asdf or direnv, pinning runtimes, adding tasks, fixing activation, or making an agent work inside a reproducible dev environment.
---

# Mise Expert

IRON LAW: NEVER mutate shell rc files, global mise config, or project tool versions until you can explain which activation model, config scope, and isolation target the user actually needs. When asked to set up an environment, default to a local, isolated mise environment unless the user explicitly instructs otherwise. NEVER edit global mise configuration unless the user explicitly approves that scope.

Copy this checklist and check off items as you complete them:

```text
Mise Expert Progress:

- [ ] Step 1: Classify the environment goal ⚠️ REQUIRED
  - [ ] 1.1 Identify platform, shell, repo layout, and whether this is interactive shell, CI, container, or one-shot script
  - [ ] 1.2 Identify the isolation target: project-local, user-global, CI/bootstrap, or container/system
  - [ ] 1.3 Identify whether the user needs shell activation, shims, or only `mise exec`
- [ ] Step 2: Inspect existing mise surface ⚠️ REQUIRED
  - [ ] 2.1 Check for `mise.toml`, `mise.local.toml`, `.miserc.toml`, `mise.lock`, and task files
  - [ ] 2.2 Check for existing tool versions, env files, trust requirements, and shell-hook state
  - [ ] 2.3 Load the relevant references before changing anything
- [ ] Step 3: Choose the operating model ⚠️ REQUIRED
  - [ ] 3.1 Pick config scope and write target
  - [ ] 3.2 Pick activation model
  - [ ] 3.3 Pick reproducibility level: fuzzy pins, exact pins, or lockfile-enforced
- [ ] Step 4: Confirm risky writes ⚠️ REQUIRED
  - [ ] 4.1 Present planned edits if they touch shell rc files, global config, lockfiles, or destructive task commands
  - [ ] 4.2 Do not proceed without explicit confirmation for those changes
- [ ] Step 5: Implement the mise setup
  - [ ] 5.1 Install or verify mise
  - [ ] 5.2 Author or update config files
  - [ ] 5.3 Install tools and verify trust state
  - [ ] 5.4 Add tasks, env wiring, hooks, or bootstrap logic only if required
- [ ] Step 6: Verify the environment ⚠️ REQUIRED
  - [ ] 6.1 Validate with `mise install`, `mise tasks`, `mise env`, or `mise exec -- <tool>` as appropriate
  - [ ] 6.2 Verify the chosen activation model actually works in the intended context
  - [ ] 6.3 Verify reproducibility expectations: pins, lockfile, or CI bootstrap
- [ ] Step 7: Deliver with operational notes
  - [ ] 7.1 Summarize files changed and why
  - [ ] 7.2 List remaining manual actions, especially shell restart or trust confirmation
  - [ ] 7.3 Flag any experimental mise features used
```

Red Flags (return to Step 1 if any appear):
- You are about to add shell activation before deciding whether `mise exec` is enough.
- You are about to use `mise use` in a script and then invoke the tool directly instead of using `mise exec -- ...` or `eval "$(mise hook-env)"` first.
- You are about to write to `~/.bashrc`, `~/.zshrc`, or `~/.config/mise/config.toml` even though project-local config would work.
- You are about to pin fuzzy versions in a workflow that claims reproducibility.
- You are about to cite repo examples as if they were official mise behavior.

## Step 1: Classify the environment goal ⚠️ REQUIRED

Ask:
- Is this an interactive shell, CI job, container image, devcontainer, remote sandbox, or one-shot script?
- Does the user need a project-local environment, a reusable global tool install, or a system image baked with tools?
- Does the environment need prompt-based activation, shims, or only command-scoped execution?
- Does the environment need exact reproducibility across machines?

Default assumption for setup work: create a project-local, isolated mise environment. Switch to global, shared-machine, or system scope only when the user explicitly asks for it.

MUST use `https://raw.githubusercontent.com/jdx/mise/refs/heads/main/llms.txt` as the latest upstream documentation pointer when freshness matters. Treat the contributing and codebase-architecture parts of that file as upstream internal workflow, not user-facing operational guidance.

The mise repository ships JSON Schema definitions for every TOML config file it accepts (`mise.toml`, `.miserc.toml`, global settings, task definitions, plugin configs, and registry tool entries). They live at `https://github.com/jdx/mise/tree/main/schema`. When authoring or editing any mise TOML config, consult the relevant schema to confirm valid keys, field types, and structure. Load `references/schemas.md` for the schema-to-file mapping, fetch instructions, and per-schema scope.

Load `references/overview.md` first. If containers, CI, or bootstrap are involved, also load `references/install-and-activation.md`. If `.miserc.toml` or environment selection is involved, also load `references/config-and-env.md`. If the `go:` backend, any `go.*` setting, or Go writing files somewhere unexpected is involved, also load `references/go-backend.md`.

## Step 2: Inspect existing mise surface ⚠️ REQUIRED

Check for:
- `mise.toml`, `mise.local.toml`, `mise.<env>.toml`, `.miserc.toml`, `mise.lock`
- task files under `mise-tasks/`, `.mise-tasks/`, `mise/tasks/`, `.mise/tasks/`, or `.config/mise/tasks/`
- shell activation lines, shim setup, `MISE_*` overrides, and existing env files
- existing trust assumptions or lockfile mode
- parent or ancestor mise configs that could leak into this repo

Ask:
- Which file currently owns the project environment?
- Is there already a lockfile, min_version, or `.miserc.toml` policy?
- Are there parent configs that could leak in unless `ceiling_paths` or monorepo settings are used?

If strict local isolation matters, explicitly evaluate whether `.miserc.toml` should constrain config discovery with `ceiling_paths`.

Load `references/config-and-env.md` for config resolution. Load `references/schemas.md` before authoring or editing any mise TOML config to confirm valid keys and field types against the official JSON Schema. Load `references/templating-and-early-init.md` only when templated env logic, `.miserc.toml`, or environment selection rules matter. Load `references/tools-tasks-and-isolation.md` if tools or tasks are involved.

## Step 3: Choose the operating model ⚠️ REQUIRED

### 3.1 Config scope

Prefer the narrowest scope that solves the problem:
- Project-local isolated setup by default → `mise.toml`
- Project-local secret or developer override → `mise.local.toml`
- Environment-specific overlay → `mise.<env>.toml` with `MISE_ENV`
- User-global defaults only when the request is truly machine-wide → `~/.config/mise/config.toml`

If the user says only "set up an environment" or equivalent, interpret that as project-local and isolated unless they explicitly ask for global, shared-machine, or system-level setup.

### 3.2 Activation model

Choose deliberately:
- One-shot scripts, agent tool calls, CI steps → `mise exec -- <command>`
- Interactive developer shell → `mise activate <shell>`
- Non-interactive shells or editor integration where prompt hooks do not fire reliably → `mise activate --shims`

Load `references/install-and-activation.md` before making this choice.

### 3.3 Reproducibility model

Ask:
- Is fuzzy `node = "20"` acceptable, or must exact versions be reproducible?
- Should the repo commit `mise.lock` and enforce locked installs?
- Does CI need vendored bootstrap instead of curl-based install?

Use `min_version` whenever the skill teaches recent or experimental mise features. Load `references/tools-tasks-and-isolation.md` for lockfile guidance.

## Step 4: Confirm risky writes ⚠️ REQUIRED

You MUST stop and ask before:
- editing shell rc files or login shell config
- writing or replacing `mise.lock`
- changing global mise config, and you MUST treat explicit user approval as required
- enabling destructive hooks or tasks, such as commands using `rm`, `--force`, publish, deploy, or reset flows
- baking env values into images or global config

Safe default: if project-local config plus `mise exec` solves the problem, prefer that and avoid shell mutation entirely.

## Step 5: Implement the mise setup

### 5.1 Install or verify mise

Use the upstream-supported install path for the target context. For CI or reproducible automation, prefer vendored bootstrap when practical. For containers with mounted home directories, prefer `mise install --system` patterns from `references/install-and-activation.md`.

### 5.2 Author or update config files

Keep config boring and explicit:
- add `min_version` for feature-sensitive setups
- pin tools intentionally
- use `[env]` and `env._` directives instead of ad hoc shell exports
- keep secrets out of committed `mise.toml`
- use `.miserc.toml` only for early-init behavior such as environment selection or search-boundary control

Load `references/config-and-env.md` before editing layered config files. Load `references/schemas.md` before authoring or editing any mise TOML config to confirm valid keys and field types against the official JSON Schema definitions in the mise repository. Load `references/templating-and-early-init.md` before editing `.miserc.toml` or adding Tera templating.

### 5.3 Install tools and verify trust state

Run `mise trust` for new or modified local configs, or plan around trusted paths when the environment is non-interactive. Verify installs with `mise install`, `mise ls`, or `mise exec -- <tool> --version`.

### 5.4 Add tasks, hooks, or bootstrap logic only if required

Prefer tasks when the repo needs repeatable commands. Prefer file tasks for larger scripts. Prefer hooks only when automatic behavior is genuinely needed. Prefer bootstrap for machine or service provisioning workflows.

Load `references/tools-tasks-and-isolation.md` before adding tasks or hooks. Load `references/schemas.md` to confirm task, tool, and plugin field shapes against the official JSON Schema before committing new config. Load `references/examples.md` only if you want non-authoritative patterns from real repos.

## Step 6: Verify the environment ⚠️ REQUIRED

Use the verification path that matches the chosen model:
- prompt activation → new shell or explicit hook reload, then `mise env` and a tool command
- shims → confirm PATH/shims behavior without assuming `[env]` is loaded for ordinary shell commands
- `mise exec` → verify the exact target command works through `mise exec --`
- lockfile or strict mode → verify `mise install` works from a clean state
- container/system install → verify tools are visible after mounts and under the intended user

Load `references/operations-and-troubleshooting.md` if anything is off.

## Step 7: Deliver with operational notes

Your final answer MUST include:
- the chosen isolation and activation model
- files created or changed
- verification commands run and what they proved
- any manual follow-up, especially shell restart, trust prompts, or experimental feature caveats

## Anti-Patterns to Avoid

- Editing shell rc files when `mise exec --` would solve the problem.
- Editing global mise config without explicit user approval.
- Defaulting to global or shared-machine setup when the user only asked for an environment.
- Using repo examples as normative documentation.
- Treating fuzzy versions as reproducible without a lockfile.
- Putting secrets into committed `mise.toml`.
- Assuming shims load project `[env]` for plain shell commands.
- Using `mise use` in scripts and then calling tools directly without `mise exec --` or `mise hook-env`.
- Adding hooks for work that should be explicit tasks.
- Using experimental features like `mise oci`, `mise mcp`, `bootstrap`, `deps`, or task templates without flagging them as experimental.
- Ignoring parent-config leakage in monorepos or nested repos.
- Declaring an accelerator that mise itself invokes (e.g. `cargo-binstall`) as a mise-managed tool — `mise install --force` then replaces it mid-run while depending on it.
- Guessing config keys or field types without consulting the official JSON Schema when authoring or editing mise TOML config files.

## Pre-Delivery Checklist

- [ ] Chosen activation model is stated explicitly
- [ ] Chosen config scope is stated explicitly
- [ ] Any shell rc mutation was confirmed first
- [ ] Any global config mutation was confirmed first
- [ ] `min_version`, pinning, and lockfile decisions match the reproducibility goal
- [ ] Verification used the same execution path the user will use
- [ ] No secrets were written to committed config files
- [ ] Experimental mise features are labeled clearly
- [ ] Real-repo examples, if mentioned, are labeled example-only
- [ ] Config keys and field types validated against the official mise JSON Schema when authoring or editing mise TOML config files
