# headroom-management — archived 2026-08-26

**Archived because the Headroom proxy it manages was rejected**, so the skill
governs a tool this setup no longer runs. The decision is recorded in
`~/.config/claude/TODO.md`: *"CLOSED 2026-08-25: 6e rejected the proxy, so no
unit is needed and this never becomes live."* The disabled
`~/.config/systemd/user/headroom-default.service` stays on disk under that same
entry.

Confirmed by the user on 2026-08-26: the proxy was rejected, which is what made
this skill — and the open item that planned to generalize it — stale.

## What it was

An OpenCode-only skill covering Headroom proxy setup, deployment, service
management, backend selection and troubleshooting. 297 lines of `SKILL.md` plus
`references/opencode-integration.md` (95 lines). Its Iron Law — never debug
against a live install, start from the documented healthy-case baseline and probe
in temp directories with explicit env overrides — is the part most likely to be
worth lifting into something else.

## Where it was deployed

- Group: `skills/opencode/` → Kasetto scope `opencode-extra`
- Destination: `~/.config/opencode/skills/headroom-management`
- Never deployed to Claude Code or Copilot CLI: `opencode/` deploys to OpenCode
  alone, and Copilot receives `shared/` only.

It was the **only** skill in `skills/opencode/`, so archiving it emptied that
group. The group directory is gone from git (git does not track empty
directories), while `skills/kasetto/opencode-extra/` and its lock deliberately
remain — see `../README.md` for what that costs and why the scope was kept.

## Superseded plans

`skills/TODO.md` carried an open item to generalize this skill to work with
Claude Code and move it to `shared/`. **That item was pruned rather than struck
through**, on the user's instruction: the proxy's rejection made the plan stale
rather than rejected-on-its-merits, so there is no argument worth preserving to
stop it being re-proposed. If Headroom ever returns, the plan is one line to
rewrite; this file is the record that it existed.

## Related material kept elsewhere

A rescue archive of the in-progress Headroom work sits outside this repository at
`~/src/context-tools/headroom/rescue-2026-08-25/`, including a hardened
`systemd-headroom.service` that invokes a launcher directly instead of running an
installer through `ExecStart`. Noted 2026-08-26 from `~/.config/claude/TODO.md`;
not verified to still exist at that path.

## Reviving it

`git mv skills/archived/headroom-management skills/opencode/headroom-management`,
then `just deploy`. Nothing else is needed — the `skills: "*"` glob re-resolves
membership, so the skill returns to the `opencode-extra` scope on the next sync.
`SKILL.md` is byte-identical to the last deployed version, so there is no banner
or marker to strip.
