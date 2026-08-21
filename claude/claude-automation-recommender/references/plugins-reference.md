# Plugin Recommendations

Plugins are installable bundles of skills, commands, agents, and hooks.

**Any plugin list in this file is a snapshot and rots.** MUST verify a plugin
still exists before recommending it — see [Verify before
recommending](#verify-before-recommending).

---

## The Install Contract

Three things the recommendation MUST carry, or the user cannot act on it:

1. **A marketplace must be added first.** Plugins do not install by bare name
   from nowhere.
2. **Plugin ids are `plugin@marketplace`.** The bare name works only when it is
   unambiguous across the configured marketplaces.
3. **Installing requires a restart** before the plugin's skills, hooks, and
   agents load.

```bash
# 1. Add the marketplace (URL, local path, or GitHub owner/repo)
claude plugin marketplace add anthropics/claude-plugins-official

# 2. Install
claude plugin install plugin-dev@claude-plugins-official

# 3. Inspect
claude plugin list                  # installed plugins
claude plugin details <plugin>      # component inventory + projected token cost
claude plugin marketplace list      # configured marketplaces
```

Interactively, `/plugin` opens the same thing as a browser UI.

There is **no** `/plugin info` subcommand — `claude plugin details` is the
equivalent. Other useful subcommands: `enable`, `disable`, `uninstall`,
`update`, `validate`.

### Verify Before Recommending

```bash
claude plugin marketplace list                 # what is configured
claude plugin list                             # what is already installed — do not re-recommend
claude plugin details <name> 2>/dev/null       # does it resolve, and what does it cost in tokens
```

`claude plugin details` reports the projected token cost. Quote it when
recommending a large plugin — every enabled plugin's skill descriptions and
commands occupy context in every session.

---

## Official Plugins (`claude-plugins-official`)

Snapshot — confirm with `claude plugin details` before recommending.

### Development and Code Quality

| Plugin | Best For |
|--------|----------|
| **plugin-dev** | Building plugins: skills for skill, hook, command, agent, and MCP development |
| **skill-creator** | Authoring individual skills |
| **pr-review-toolkit** | PR review workflows with specialized review agents |
| **code-review** | Multi-agent automated code review |
| **code-simplifier** | Refactoring while preserving behavior |
| **code-modernization** | Migrating legacy patterns |
| **feature-dev** | End-to-end feature workflow |

### Git and Workflow

| Plugin | Best For |
|--------|----------|
| **commit-commands** | `/commit`, `/commit-push-pr` |
| **hookify** | Generating hooks from conversation patterns |

### Frontend

| Plugin | Best For |
|--------|----------|
| **frontend-design** | Production-grade UI, avoids generic AI aesthetics |

### Guidance and Output Styles

| Plugin | Best For |
|--------|----------|
| **security-guidance** | Warns about security issues while editing |
| **explanatory-output-style** | Educational commentary on code choices |
| **learning-output-style** | Requests user input at decision points |

### Language Servers

One per language: `typescript-lsp`, `pyright-lsp`, `gopls-lsp`,
`rust-analyzer-lsp`, `clangd-lsp`, `jdtls-lsp`, `kotlin-lsp`, `swift-lsp`,
`csharp-lsp`, `php-lsp`, `lua-lsp`, `ruby-lsp`.

Recommend at most the one matching the project's primary language, and only when
no symbol-aware tooling is already configured — an LSP-backed MCP server such as
Serena covers the same ground.

---

## Detection → Plugin

| Codebase Signal | Recommended Plugin |
|-----------------|-------------------|
| Building plugins or skills | plugin-dev, skill-creator |
| PR-based workflow | pr-review-toolkit |
| Git commits without a convention | commit-commands |
| React/Vue/Angular | frontend-design |
| Repeated manual review rules | hookify |
| Auth, payments, or secrets handling | security-guidance |
| Primary language with no symbol tooling | the matching `*-lsp` |

---

## When to Recommend Plugins

- The user wants several related capabilities at once
- A team wants standardized workflows from a shared marketplace
- First-time Claude Code setup

**When not to:** a single skill is needed. Creating one file under
`.claude/skills/` costs less context than installing a bundle whose other
components load in every session.
