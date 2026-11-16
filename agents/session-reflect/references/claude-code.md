# Claude Code

The config root is `${CLAUDE_CONFIG_DIR:-~/.claude}`; it is written `<config>` below.

## Where things live

- **Memory**: one folder per project, `<config>/projects/<project>/memory/`, holding one fact per Markdown file
  and a `MEMORY.md` index with a one-line pointer to each. `<project>` is the working directory with every
  non-alphanumeric character turned into `-`.
- **User instructions**: `<config>/CLAUDE.md` and the files it imports.
- **Project instructions**: `CLAUDE.md` or `AGENTS.md` in the repository; `.claude/skills/` and
  `.claude/agents/` for repo-specific skills and agents.
- **Session logs**: JSONL at `<config>/projects/<project>/<session-id>.jsonl`.

## Memory format

Each file carries frontmatter with `name`, `description`, and `metadata.type` (`user`, `feedback`, `project`,
or `reference`). A `feedback` or `project` body ends with **Why:** and **How to apply:** lines, and links related
memories with `[[name]]`. Add the file's pointer to `MEMORY.md` in the same step, and remove or update it when a
memory is deleted or merged.

There is no global memory store. A fact true everywhere still lands in whichever project's folder is open, and
only that project's recalls see it. Recall matches the `description` text, and nothing filters on frontmatter, so
such a fact says it holds everywhere in its `description`. Set `metadata.scope: machine` or `global` as well,
for the maintenance sweep and the human reader.

## Compaction backlog

A `PreCompact` hook, where installed, appends one breadcrumb per compaction to
`<config>/hooks/capture-pending.jsonl`, with the fields `ts`, `session_id`, `cwd`, `transcript_path`, and
`trigger`. Each line marks a session whose detail was summarized away, and is the only pointer back to it.

Report its line count in every report, and drain it on request or once it passes about twenty:

```bash
wc -l < "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/hooks/capture-pending.jsonl" 2>/dev/null || echo 0
```

Read [compaction-backlog.md](compaction-backlog.md) before draining it.
