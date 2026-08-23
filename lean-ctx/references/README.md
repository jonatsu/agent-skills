# lean-ctx reference index

Load on demand, one file at a time, by symptom. `SKILL.md` carries the trigger
for each — use it rather than picking from this list.

## Measured here (authoritative over upstream prose)

- `12-troubleshooting.md` — path-jail and project-root capture, rules injection
  reappearing, deployed skill files being rewritten
- `13-silent-failure-modes.md` — calls that return a plausible-looking wrong
  answer: truncation, redaction, stale caches, read-dedup stubs
- `14-ctx-patch-contract.md` — per-op fields, batching, `dry_run`, write gates.
  The field-name authority for `ctx_patch`

## Local prose over upstream behavior

- `01-setup-and-onboarding.md` — wrap, onboard, setup, bootstrap, init
- `04-code-intelligence.md` — symbols, graph, impact; what is LSP-backed and what
  only approximates it
- `05-advanced.md` — power tools, MCP, proxy, shell hook, write doctrine
- `06-lifecycle.md` — update, repair, sessions, cache, migration

## Upstream snapshots (pinned; live state outranks them)

- `appendix-cli-map.md` — compact CLI command map
- `appendix-mcp-tools.md` — MCP tool inventory and profile membership
- `appendix-paths-and-config.md` — config, path jail, editor env guidance
- `appendix-reference-docs.md` — upstream reference journeys 01–13, distilled.
  Largest file here; read one named section, never the whole thing

## About the numbering

The numbers mirror upstream's journey numbering, so the gaps are intentional:
journeys 03, 08, 09, 10, and 11 (memory/knowledge, multi-agent, team/cloud/CI,
customization/governance, analytics) exist only as sections inside
`appendix-reference-docs.md`, because nothing local needed to be said about them.
Journeys 02 and 07 were retired once `13`, `14`, and `05` covered their content
with measured detail.

Do not renumber these files. `12`, `13`, `14`, and `04` are referenced by name
from outside this skill.

## Drift rule

Trust generated appendices, `ctx_load_tools`, live tool lists, and `doctor` over
static prose when versions differ. Within this skill, the measured files above
outrank the upstream snapshots.
