# Plugin Recommendations

Plugins are installable bundles of skills, commands, agents, and hooks.

**This file deliberately names no plugins.** A plugin catalogue rots on someone else's release schedule, and
the CLI answers the question authoritatively at the moment it is asked. What is here instead is the install
contract, the way to enumerate candidates, and the judgment about when a plugin is the wrong recommendation.
MUST resolve every plugin against [Verify before recommending](#verify-before-recommending) before it reaches
the report.

---

## The Install Contract

Three things the recommendation MUST carry, or the user cannot act on it:

1. **A marketplace must be added first.** Plugins do not install by bare name from nowhere.
2. **Plugin ids are `plugin@marketplace`.** The bare name works only when it is unambiguous across the
   configured marketplaces.
3. **Installing requires a restart** before the plugin's skills, hooks, and agents load.

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

There is **no** `/plugin info` subcommand — `claude plugin details` is the equivalent. Other useful
subcommands: `enable`, `disable`, `uninstall`, `update`, `validate`.

### Verify Before Recommending

```bash
claude plugin marketplace list                 # what is configured
claude plugin list                             # what is already installed — do not re-recommend
claude plugin details <name> 2>/dev/null       # does it resolve, and what does it cost in tokens
```

`claude plugin details` reports the projected token cost. Quote it when recommending a large plugin — every
enabled plugin's skill descriptions and commands occupy context in every session.

---

## Finding Candidates

**Enumerate the marketplace rather than reciting plugin names.** A catalogue written into this file is a
snapshot of something that changes on someone else's schedule, and a plugin name is exactly the kind of fact
the CLI answers authoritatively and for free. Anthropic's own marketplace held 39 plugins when this section
was written on 2026-09-03; any fixed list here would be a silent sample of it.

```bash
claude plugin marketplace add anthropics/claude-plugins-official  # if not already configured
claude plugin marketplace list                                    # what is configured
```

Then browse interactively with `/plugin`, or resolve a specific candidate with `claude plugin details <name>`.
Match the plugin to the signals Phase 1 found, and drop anything Phase 0 shows as already installed.

Two families recur often enough to name as *categories*, not as fixed ids:

- **Language servers.** The marketplace carries one `*-lsp` plugin per major language. Recommend at most the
  one matching the project's primary language, and only when no symbol-aware tooling is configured already —
  an LSP-backed MCP server covers the same ground and the two together are waste.
- **Output styles.** These change how Claude writes rather than what it can do. Recommend one only when the
  user has asked about explanation or teaching behavior; it is not a codebase-driven recommendation.

Every other recommendation should come from what `claude plugin details` actually reports today.

---

## When to Recommend Plugins

- The user wants several related capabilities at once
- A team wants standardized workflows from a shared marketplace
- First-time Claude Code setup

**When not to:** a single skill is needed. Creating one file under `.claude/skills/` costs less context than
installing a bundle whose other components load in every session.
