# GitHub Copilot CLI

The home is `${COPILOT_HOME:-~/.copilot}`; it is written `<home>` below.

## Where things live

- **Memory**: GitHub's cloud Copilot Memory, not a local file. In an interactive session the main agent saves
  one with `store_memory` and reinforces one with `vote_memory`; subagents can only read. Prompt mode
  (`copilot -p`) has memory off unless started with `--enable-memory`, and the user can turn it off with
  `/memory off` or by policy. A memory unused for 90 days expires.
- **User instructions**: `<home>/copilot-instructions.md` and `<home>/instructions/**/*.instructions.md`.
- **Project instructions**: `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`,
  `AGENTS.md`, and `CLAUDE.md`.
- **Session logs**: `<home>/session-state/<session-id>/events.jsonl`, one folder per session.

## Writing a memory

Memory has two scopes, and they differ in who can read them. A user preference is private to the user; save
it directly. A repository fact is shared with everyone who works in that repository on GitHub, which makes it
heavy: propose it first, and keep anything private or client-identifying out of it.

When memory is off or unavailable, route memory candidates to instructions.

The agent cannot delete a memory. For memory maintenance, list the stale entries in the report and send the user
to Copilot settings on GitHub.com, under Memory, to remove them.
