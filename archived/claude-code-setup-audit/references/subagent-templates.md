# Subagent File Format

Read this when recommending a subagent. `SKILL.md` carries the signal-to-agent mapping; this file carries the
file format and the two facts that make a recommendation runnable rather than plausible.

Subagents are Markdown files in `.claude/agents/<name>.md` (project) or the user-level `agents/` directory.
Each runs with its own context window and tool access, which is why they suit focused review and analysis.

## Frontmatter

| Field         | Required    | Format                                                                              |
| ------------- | ----------- | ----------------------------------------------------------------------------------- |
| `name`        | Yes         | lowercase-hyphens, matches the filename                                             |
| `description` | Yes         | Prose naming 2-4 concrete trigger scenarios — this is what routes work to the agent |
| `model`       | Recommended | `inherit`, `sonnet`, `opus`, or `haiku`                                             |
| `tools`       | No          | Comma-separated; omit to inherit all. Least privilege — a reviewer gets no Edit     |
| `color`       | No          | Cosmetic only                                                                       |

Verified 2026-09-03 against six working agents in the authoring environment's user-level `agents/` directory:
all six omit `color` and load correctly, and one omits `tools` and correctly inherits the full set. Do not
recommend a field as mandatory without checking a loaded agent that omits it — an unnecessary required field
is the kind of claim that survives review because it looks like documentation.

`model` is marked Recommended rather than optional because every agent checked declared one, so its absence
was not observed. State that limit if a recommendation depends on omitting it.

The `description` is the routing signal — a vague one means the agent is never invoked. The body is the
system prompt the agent actually reads.

## The Key That Is Silently Ignored

**An agent's tool restriction uses `tools`. A skill uses `allowed-tools`.** They are not interchangeable and
the wrong key is dropped without an error, so a file documented as read-only runs with full tool access. Check
which artifact is being written before writing the key.

## Worked Template

```markdown
---
name: security-reviewer
description: Use when reviewing code that touches authentication, authorization, secrets, user input, or payment flows. Typical triggers include a diff adding a login route, a change to token handling, or a new file-upload endpoint. Does not modify code — reports findings only.
model: inherit
tools: Read, Grep, Glob
---

You review code for security defects and report them. You NEVER edit files.

## Method

1. Identify the trust boundaries the change crosses.
2. Check each against OWASP Top 10 categories relevant to the language.
3. For each finding, give: file:line, the concrete failure scenario, severity,
   and the minimal fix.

## Output

Findings ordered by severity. State explicitly when a category was checked and
found clean. NEVER pad the report with generic advice.
```

## Choosing a Model and Tool Set

| Model    | Fits                             | Trade-off                        |
| -------- | -------------------------------- | -------------------------------- |
| `haiku`  | Simple, repetitive checks        | Fast, cheap, less thorough       |
| `sonnet` | Most review and analysis         | Balanced; the usual default      |
| `opus`   | Complex migrations, architecture | Thorough, slower, more expensive |

Prefer `inherit` when the agent should track whatever the session is running rather than pin a tier.

Grant tools by what the agent must do, not by what it might want: `Read, Grep, Glob` for anything that only
reports, plus `Write` when it generates files, plus `Bash` only when it runs commands. A reviewer that can
edit will eventually edit.
