# claude-code-setup-audit — archived 2026-09-28

Archived at the user's direction because it saw no use. It had never been through the 2026-09-28 description
and `writing-for-agents` passes, so it was retired rather than refreshed.

## What it was

A Claude Code-only, report-only audit of a codebase and its Claude Code configuration. It recommended the
hooks, subagents, skills, plugins, and MCP servers a project lacked. It was renamed from
`claude-automation-recommender` on 2026-09-03, and it is Apache-2.0, adapted from upstream: `ATTRIBUTIONS.md`
and `LICENSE.upstream` stay with the directory. It was the one deployed skill that set `allowed-tools`.

## Where it was deployed

- Group: `skills/claude/`, Kasetto scope `claude-extra`
- Destination: `~/.config/claude/skills/claude-code-setup-audit`
- Never deployed to Codex or Copilot CLI, which receive `shared/` only.

## Left in place

`src/tools/session-scoring/src/sessionlib/candidates.py` keeps its entry in `DOMAIN_SIGNALS`, because recorded
transcripts from before this date still name the skill.

## Reviving it

`git mv skills/archived/claude-code-setup-audit skills/claude/claude-code-setup-audit`, then
`./scripts/kasetto-deploy.sh`. `SKILL.md` is byte-identical to the last deployed version. Run both passes before
redeploying it.
