# Attributions

## Current skill

- Skill: `lean-ctx`
- Current author: Joonas Onatsu
- Current license: Apache License 2.0 (inherited from upstream; not relicensed)
- Status: adapted from upstream documentation, then substantially extended with
  locally measured tool behavior

## Original authors and source

- Original author: Yves Gugger and the `yvgude/lean-ctx` maintainers
- Upstream project: [yvgude/lean-ctx](https://github.com/yvgude/lean-ctx)
- Docs: <https://leanctx.com/docs>
- llms.txt: <https://raw.githubusercontent.com/yvgude/lean-ctx/refs/heads/main/llms.txt>
- Reference docs root: <https://github.com/yvgude/lean-ctx/tree/main/docs/reference>
- Pinned upstream commit: `5ad09b5030254e5368e91cbd419b07564f98ea95`
- Rules-injection gating characterized against commit `934477bc…`, newer than the
  pinned one. Verify live `doctor` / `--help` output if the installed version
  differs from either.

## Provenance per file

| File here | Relationship to upstream |
|---|---|
| `SKILL.md` | Rewritten. The routing shape is local; the "Must-remember gotchas" and "Anti-patterns" blocks are locally measured and have no upstream counterpart |
| `references/appendix-reference-docs.md` | Derivative. Distilled from upstream `docs/reference/` journeys 01–13; retains upstream's structure, command sets, and many phrasings |
| `references/appendix-mcp-tools.md` | Derivative. Built from upstream's generated MCP registry and profile map; retains tool names, parameter names, and table structure |
| `references/appendix-paths-and-config.md` | Derivative in substance. Local prose over upstream config keys |
| `references/01-setup-and-onboarding.md` | Local prose summarizing upstream setup flows |
| `references/04-code-intelligence.md` | Local prose; the LSP-versus-approximation section is original, from local testing |
| `references/05-advanced.md` | Local prose; the `ctx_shell` write-doctrine section is original |
| `references/06-lifecycle.md` | Local prose; the "an update does not reach the running session" section is original |
| `references/12-troubleshooting.md` | Original. Root-capture mechanics, rules-injection and skill-overwrite playbooks measured locally |
| `references/13-silent-failure-modes.md` | Original. Every entry measured against a running lean-ctx; no upstream counterpart |
| `references/14-ctx-patch-contract.md` | Original. Per-op field contract recovered from runtime errors, not from the published schema |

The three original reference files (`12`, `13`, `14`) document defects and
undocumented behavior observed while running lean-ctx. They are not upstream
content and were not derived from upstream text.

## Upstream license

The upstream source is used under the Apache License, Version 2.0. A verbatim
copy is kept alongside this file as `LICENSE.upstream`, and upstream's own
attribution notice as `NOTICE.upstream`.

As required by section 4 of that license, this is a modified version; the
per-file changes are listed above. Sections 4(a) and 4(d) require that both
files travel with this skill — keep them when redistributing or re-deploying it.

Copyright 2026 Yves Gugger.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at <http://www.apache.org/licenses/LICENSE-2.0>.

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
