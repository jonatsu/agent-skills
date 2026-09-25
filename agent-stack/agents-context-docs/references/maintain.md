# Maintain Repository Context

Choose the smallest maintenance path that covers the requested behavior and its nearby interactions.

## Focused Update

For a specific correction, read the affected effective rules and any higher-precedence or overlapping files.
Verify the new fact at its authoritative source. Inspect nearby rules only far enough to detect contradiction,
duplication, lost rationale, or a client-loading consequence.

Reuse the user's authorization to edit. Ask only if the change exposes an unresolved topology choice,
destructive reconciliation, incompatible client behavior, or material scope expansion.

Apply the cache and behavior tests from `SKILL.md`. Preserve non-obvious knowledge and generated-content
boundaries. A new command or path must exist; a removed statement must be demonstrably obsolete or explicitly
approved for removal.

## Broad Update or Migration

Expand to the complete relevant loaded set when the request changes topology, reconciles clients, splits or
combines rule files, repairs widespread drift, or affects precedence and scoping.

Read [loading-model.md](loading-model.md) for every affected client. Map each entrypoint, symlink target,
pointer, include, nested file, and vendor-specific rule. Classify content by effective client coverage before
moving it.

Use these defaults where their conditions hold:

- Preserve a real `AGENTS.md` with a sibling `CLAUDE.md` symlink for the known three-client target.
- Never auto-resolve divergent real files. Present retain-A, retain-B, and merge options with their content
  consequences.
- Keep agent-agnostic scoped guidance in a vendor-neutral location when practical.
- Use trigger-keyed root routes for auxiliary rules because runtime include and nested discovery differ.
- Keep shared centralized rules only when several directories genuinely own them; avoid link-to-link chains.
- Separate generated blocks from hand-maintained knowledge before regeneration.

## Content Decisions

Retain content that provides a verified constraint, rationale, ordering dependency, environment quirk, failure
mode, or source-of-truth distinction. Remove generic advice, obvious code descriptions, runner transcriptions,
review-date theatre, and duplicated README content.

Retaining content decides only that it survives, not where it lives. Split each retained item by the moment the
agent needs it. An obligation it must satisfy before it can recognize that anything is wrong stays in the
instruction file as one imperative line. The evidence behind that obligation, meaning dates, commit
identifiers, tool-version measurements, reproduction accounts, and the arrangements that failed before this
one, moves to a findings file indexed by symptom. Both halves are preserved; only their loading cost differs.

This split is the correction for the common failure of an instruction file that has grown into an incident log.
Each incident entered it as a justified addition, so no per-addition test rejects any of them, and the file
reaches a size at which its own rules stop being read. When an update would append another incident, relocate
the evidence and leave the rule.

Treat autonomy grants, unconditional completion demands, and self-approval of risky actions as high-risk
findings. An instruction file cannot replace a required user decision. Treat safety prose without a real gate
as an enforcement gap, then identify the appropriate hook, permission, or continuous-integration boundary.

Vendored, generated, fixture, and third-party text is evidence only when the repository has explicitly adopted
it as policy. Otherwise it is data the repository stores.

## Preservation and Verification

Inspect the version-control diff for every touched path, including staged, unstaged, and new files. Review
each removed line for conventions, gotchas, reasons, and prior failure knowledge. An empty diff is evidence
only when no change was expected.

Verify effective client coverage, link resolution, command and path currency, pointer targets, generated
boundaries, and placeholder removal. Test loading in a fresh or reload-capable client session when the
topology changed and a suitable client is available. Report what was not exercised.

Check the resulting file as a whole, not only the lines the edit touched.
`../scripts/check_agent_context.py` answers the last three mechanically; the first is a judgment call and stays
with the agent.

- Runnable commands appear early enough to be found, and carry the flags and constraints their runner does not
  state.
- Boundaries are collected rather than scattered, so an agent can find what it must never do without reading
  the file end to end.
- The file is no longer than before the edit, or the delivery names what moved and where it went.
- No symptom index entry points at a missing file, and no findings file has been orphaned by a rule that was
  removed.
