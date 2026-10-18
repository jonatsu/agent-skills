# Evidence and experiments

## Keep a claim attached to its observation

Record the input hash, address space, address/range or capture location, tool identity, relevant command/settings,\
observation, interpretation, and confidence. Distinguish observed behavior, static deduction, and an inherited claim. A\
greppable uncertainty marker such as `TODO(re):` can keep unresolved questions discoverable when the workspace uses\
one. Pair each gap with the observation that would close it; an unbounded reminder to investigate is not an experiment.

A hypothesis may explain a function's role from strings or constants without establishing its complete behavior.\
Separate identity, prototype, layout, reachability, and application-level purpose. Use the same distinction when\
copying metadata from a donor or prior build. Names should communicate current understanding while comments retain\
uncertainty and the basis for revision.

## Choose a discriminating next step

When two explanations fit the current output, identify where their predicted effects differ. Select the smallest safe\
observation at that boundary: one memory access, argument preparation, branch outcome, caller, or field initialization.\
Check prerequisite state before interpreting a failed execution as a property of the binary. Keep each experiment's\
starting state, intervention, prediction, observation, and effect on the hypotheses.

Change one load mapping, signature, hook, or environment variable at a time when isolating a disagreement. If several\
changes are required to run, record their combined assumptions and avoid claiming causal isolation. Return to\
instructions when decompiler output omits stores, merges unrelated values, or contradicts callers. Return to the\
runtime/ABI model when concrete replay disagrees with solved constraints. Stop expanding a route whose prerequisites\
cannot be supplied; preserve its blocker and continue an independent route.

## Compare builds and tools on equal coordinates

Establish each binary's identity, architecture/ABI, compiler/build relationship, layout, and relocations before\
diffing. Compare normalized functions and callers rather than assuming equal addresses imply equal routines. A raw byte\
diff identifies changed regions; a disassembly/function diff helps separate relocation noise from logic changes. Tools\
such as `radiff2` can help after their installed syntax and matching assumptions are checked. A source rebuild or donor\
is evidence only for its documented version/options, not every firmware variant.

For cross-tool disagreements, align binary hash, section/load mapping, function entry, instruction mode, and analysis\
coverage. Inspect original bytes, branch conditions, and data effects before choosing the more readable rendering. Two\
front ends sharing a decompiler engine are not independent confirmation of that engine's interpretation. Retain\
contradictory outputs and the reason one model was rejected.

## Bound conclusions and preserve continuity

A trace covers one execution and environment; a static proof covers its stated semantics and assumptions. An empty\
search/reference result can reflect incomplete indexing or analysis. A solver timeout says nothing about impossibility,\
and an accepted signature match does not prove a function's business role. Name missing instructions, peripherals,\
symbols, mappings, or permissions precisely.

Save annotations and evidence after each useful result, with a next action that another analyst can execute. Use the\
workspace's own source index and documentation scheme for research capture; this skill does not impose one.
