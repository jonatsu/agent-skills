# lean-ctx — archived 2026-08-27

**Archived because lean-ctx itself was removed from this setup**, so the skill
documents a tool that no longer runs here. Confirmed by the user on 2026-08-27:
*"lean-ctx is removed and skill is not needed."* The removal was visible from
inside the session that archived it — the `lean-ctx` MCP server disconnected
mid-turn, taking every `ctx_*` tool with it, and the user restarted the session
for that reason.

Removing the server is what makes the skill stale, not any defect in it. Every
trigger in its description names a `ctx_*` tool or a lean-ctx config surface;
with no server, none of them can fire.

## What it was

A skill covering lean-ctx and its `ctx_*` MCP tools: read modes and edit ops,
the shell hook, MCP config, profiles, compression, the proxy, `doctor`, the
writer commands, and rules injection. 207 lines of `SKILL.md` plus eleven
reference files, 2111 lines in total.

**The three original reference files are the part most worth keeping**, and the
reason this is an archive rather than a deletion:

| File | Why it is not recoverable from upstream |
|---|---|
| `references/12-troubleshooting.md` | Root-capture mechanics, rules injection and the skill-overwrite playbook, all measured locally |
| `references/13-silent-failure-modes.md` | Every entry measured against a running lean-ctx; no upstream counterpart |
| `references/14-ctx-patch-contract.md` | Per-op field contract recovered from runtime errors rather than from the published schema |

`ATTRIBUTIONS.md` records which of the remaining files are derivative of
upstream and which are local prose.

## The upstream licence files stay

The skill is Apache-2.0, inherited from
[yvgude/lean-ctx](https://github.com/yvgude/lean-ctx) and never relicensed.
`LICENSE.upstream` and `NOTICE.upstream` sit beside `SKILL.md` because sections
4(a) and 4(d) require them to travel with it. **That obligation does not lapse
on archival** — it is a condition on the copy, not on the deployment. Do not
tidy either file away, and keep them with the directory if it is ever moved
again.

## Where it was deployed

- Group: `skills/shared/context/` → Kasetto scopes `claude`, `opencode` and
  `copilot`
- Destinations: `~/.config/claude/skills/lean-ctx`,
  `~/.config/opencode/skills/lean-ctx`, `~/.copilot/skills/lean-ctx`

Archiving did **not** empty `skills/shared/context/`, which keeps `handoff`,
`semantic-compression` and `token-optimiser`. That matters for the prune:
`kasetto-deploy.sh` still has locked siblings to name, so the deployed copies
are removed by the ordinary post-commit sync rather than by the manual
`kst sync --project --update` that an emptied group would have required. See
`../README.md` for the emptied-group case.

Checked 2026-08-27, immediately before the `git mv`: the Claude and Copilot
copies had already been removed by hand as part of taking lean-ctx off this
machine, while `~/.config/opencode/skills/lean-ctx` was still present. Nothing
in this repository would have reported that leftover — `just skills-owned`
excludes the OpenCode directory under `check-skill-ownership.sh`'s
`skip_targets`, and `git status` cannot see a directory outside the repo.

## What this archival does NOT retire

lean-ctx's writer commands are why `scripts/check-skill-deploy-drift.sh` exists:
`setup`, `onboard`, `init`, `install`, `update`, `wrap`, `doctor --fix` and
`skill` each installed their own vendored `SKILL.md` into every agent directory
in one pass, leaving a `.bak` and a clean `git status` here. **That gate stays,
and so does the reasoning in `AGENTS.md` and in the script's header.** The
hazard is a property of deploying real copies rather than symlinks; lean-ctx was
the tool that demonstrated it, not the only tool that can cause it.

Still live elsewhere in this repo at the time of archiving, and out of scope for
this change: the `.claude/settings.json` hook matchers on
`mcp__lean-ctx__ctx_shell` and `mcp__lean-ctx__ctx_read`, the `lean-ctx/*` tool
entries in `copilot/agents/*.agent.md`, and the references in
`services/AGENTS.md` and the `docs/plans/` design records.

## Reviving it

`git mv skills/archived/lean-ctx skills/shared/context/lean-ctx`, then
`just deploy`. Nothing else is needed — the `skills: "*"` glob under the
`context` domain re-resolves membership, so the skill returns to all three
scopes on the next sync. `SKILL.md` is byte-identical to the last deployed
version, so there is no banner or marker to strip.

Revival would also mean re-checking the content against whatever lean-ctx
version is installed then. The pinned upstream commit is recorded in
`ATTRIBUTIONS.md`, and the rules-injection behaviour was characterised against a
newer one — both were already out of step with the docs when the skill was live.
