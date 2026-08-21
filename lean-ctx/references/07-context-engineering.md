# Context engineering

## Principles

- Spend context only where it changes the decision.
- Prefer structure before bytes: tree/search/map/signatures, then focused reads.
- Keep compression recoverable; raw/full reads remain available.
- Preserve provider prompt-cache friendliness where possible.

## Compression surfaces

- File reads: modes, line slices, signatures, maps, diffs.
- Search: grouped matches, context windows, semantic summaries.
- Shell: known log/test/build patterns, folded noise, retained failures.
- Docs: short skill injection plus load-on-demand references.

## Recovery

If compressed output omits needed details, recover by handle, exact path, raw
read, line slice, or fresh read. Do not repeatedly re-read whole files when a
targeted slice or search answers the question.

## Skill-forge layout

Put durable, universal rules in `SKILL.md`. Put setup maps, command references,
debug playbooks, and long explanations under `docs/` or `references/`.
