# generated-file-verify — archived 2026-09-28

Archived at the user's direction because its subject belongs to one repository. It was promoted from
the author's Nix configuration repository on 2026-09-06, and every concrete step it carries is Nix: `writeText` and `files.file`
wrappers, per-file `nix flake check` registrations, and `--no-eval-cache`. Its generic description matched
almost any repository, yet it recorded no `Skill` call in the 30 days before archiving. It had never been through
the 2026-09-28 description and `writing-for-agents` passes.

## Where its guidance lives now

That repository's verification memory file already held two of its four lessons: classify a generator as
live-derived or static prose before rerunning it, and run a files-generator in a throwaway detached worktree
first. The other two were added there on 2026-09-28: confirm exactly one generator owns the target file, and
retry with `--no-eval-cache` before chasing an impossible-looking result as a content bug.

## Where it was deployed

- Group: `skills/shared/development/`, Kasetto base scope
- Destinations: the Claude Code, Codex, and Copilot CLI skills directories

## Left in place

`src/tools/session-scoring/src/sessionlib/candidates.py` keeps its entry in `DOMAIN_SIGNALS`, because recorded
transcripts from before this date still name the skill.

## Reviving it

`git mv skills/archived/generated-file-verify skills/shared/development/nix/generated-file-verify`, then commit
and let the post-commit hook deploy it. `SKILL.md` is byte-identical to the last deployed version. Scope its
description to Nix and run both passes before redeploying it.
