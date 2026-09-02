# Archived: find-skills

- **Archived**: 2026-09-02
- **Last deployed to**: Claude Code, OpenCode and GitHub Copilot CLI, via the
  `shared` group (`skills/shared/agent-stack/find-skills`)
- **Successor**: no single cross-agent successor. Use each agent's supported
  skill discovery and installation mechanism.

## Why

The user retired this local cross-agent discovery and installation workflow on
2026-09-02. Its source catalogue, trust tiers, scanner advice and installation
commands require continuing maintenance against external services and agent
interfaces. Its self-update section was already stale: it named the former
`agent-skills` repository, the pre-domain source path and the retired skillsmgr
store model.

Codex now provides the system `skill-installer` skill for curated OpenAI skills
and GitHub repository paths. That narrower capability covers installation on
Codex, but it does not replace this skill's cross-agent search or security review
workflow. The archived copy remains useful as reference material for provenance
classification and pre-install inspection.

`SKILL.md`, both references and `scripts/verify_skill.sh` are byte-identical to
the last deployed version.

## Where It Was Deployed

- Group: `skills/shared/agent-stack/` to Kasetto scopes `claude`, `opencode` and
  `copilot`
- Destinations: `~/.config/claude/skills/find-skills`,
  `~/.config/opencode/skills/find-skills` and
  `~/.copilot/skills/find-skills`

Archiving does not empty `skills/shared/agent-stack/`, so the regular deploy
wrapper can re-resolve the shared source and prune the three copies. The
post-commit hook still misses this move because Git reports only the archived
destination for a detected rename. See `../README.md` for the required manual
redeploy and destination checks.

## Reviving It

Do not restore it without first updating the source catalogue, scanner claims,
installation methods and agent-specific invocation behavior. If those are
current and a cross-agent workflow is still useful, move the directory to
`skills/shared/agent-stack/find-skills`, then deploy it through Kasetto.
