# Reverse-engineering skill set evaluation

## Scope and review basis

This record covers the twelve packages under `reverse-engineering/` and the retained Ghidra exporters. The\
[accepted implementation plan](../plans/reverse-engineering-set-implementation-plan.md) defines their contracts, source\
revisions, boundaries, review gates, and integration obligations. Evidence below distinguishes executable checks,\
heuristic walkthroughs, and unmeasured behavior.

## Preservation and cases

| Package         | Preserved analytical workflow                                                                          | Representative case and expected boundary                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| methodology     | Target-first triage, competing explanations, tool choice, build comparison, evidence continuity        | Unknown raw image retains alternate bases; missing peripheral remains a named execution blocker             |
| binary patterns | ABI-aware instructions, data/control flow, caller/field inference, iterative model checks              | Signed/unsigned branches and relocation-sensitive references require byte/coordinate corroboration          |
| anti-reversing  | Classify obstacles, establish baseline, intervene narrowly, validate resulting behavior                | Hypervisor queries, guest artifacts, timing, and debugger checks are distinguished from dependency failures |
| protocol        | Infer framing/state, test parser hypotheses, correlate sessions, validate unseen inputs                | Split headers and multiple messages in one TCP segment require stream reconstruction                        |
| memory          | Verify capture/layers/symbols, correlate object views, extract with provenance                         | Hidden-process/injection indicators require corroboration; offline missing symbols remain a setup failure   |
| Ghidra          | Known-call retyping/naming, listing checks, merged-variable regressions, donor/type enrichment, reopen | Wrong donor or packed layout is rejected even if pseudocode looks cleaner                                   |
| radare2         | Mapping hypotheses, references, decompiler disagreement, donor uncertainty, saved-state replay         | Conditional-return disagreement is resolved against predicate bytes and the last flag writer                |
| ARM             | Mode/ABI/flag tracing, widths, caller constraints, privileged-state interpretation                     | Hidden result pointer and alignment prevent inferring arity by counting consumed registers                  |
| crypto          | Construction recovery, exact authenticated bytes, conditional weakness tests, transcript validation    | Decryption success does not establish signature acceptance; multiple transcript pairs discriminate models   |
| QEMU            | Route/prerequisite diagnosis, initialization, bounded experiment, loader/peripheral discrimination     | Static execution can emit syscall trace; a generic board does not supply proprietary devices                |
| symbolic        | Targeted inputs, state construction, models/hooks, finite exploration, candidate replay                | A solved byte gate is conditional on initialization; forced checks do not prove original satisfiability     |
| VM/bytecode     | Dispatcher/state recovery, ISA hypotheses, extraction, decoder/model, divergence refinement            | Truncated operands and unknown opcodes remain undecoded; one trace does not prove all paths                 |

ARM references were independently rewritten after inherited manual-derived expression lacked suitable redistribution\
evidence. Useful interpretation coverage remains; source relationships are retained in attribution records. Project\
adapters, private symbols, fixed hardware defaults, and local filesystem conventions are absent from the packages.

## Independent review findings

Skill Forge review lite examined every package after author validation, including source preservation and heuristic\
discovery cases. The Ghidra review corrected unsupported inherited consultation dates and license precision. The\
methodology review restored a consultation date that its original attribution explicitly recorded. The memory review\
corrected an unsupported version flag and moved offline symbol policy before the first analysis command. Scoped\
rechecks closed every package finding. All twelve package verdicts are ready with risks under review lite.

Code correctness and clean-code reviews inspected both exporter scripts and their tests and found no material defects.\
No reviewer edited production files.

## Executable evidence

Both specification and local policy validators pass for every package at the author and package-review gates. The\
specification result establishes package shape; the policy result covers additional repository obligations. Whole-tree\
attribution, name, description-form, and reference checks include 95 indexed skills after staging the twelve additions.\
Six pre-existing code-health description-budget warnings remain outside this change.

Twelve Python exporter tests pass through normal repository discovery, with real output files and a fake Ghidra API\
boundary. They cover arguments, loaded-program checks, every-function attempts, timeout/monitor forwarding, failed/null\
diagnostics, exclusive creation and symlinks, exceptions, cancellation including the final call, partial output, and\
decompiler disposal. Ruff lint and formatting checks pass for these tests and the retained Python script. These tests\
establish orchestration behavior, not native decompilation semantics.

QEMU 10.2.1 executed a synthetic static AArch32 ELF on an x86_64 Ubuntu host. The fixture requested exit status 37;\
`qemu-arm -strace` emitted `exit(37)` and the process returned 37. No downloaded or private target sample was executed.

Candidate-wide `just check` passes in an isolated local snapshot based on `363f8dd8b79e4b0f5996f52bbf6969208ae437f2`
plus the owned package, documentation, and test changes. History secret scanning, every hook, 75 pytest tests, and
103 unittest tests pass. The snapshot excludes concurrent work and prevents full-tree formatters from rewriting it.
License-notice wording is preserved; packaging normalizes trailing spaces and the final newline to satisfy hygiene hooks.

Fresh conformance review found no material implementation mismatch against the accepted plan.
Its open evidence item was a temporary-clone author configuration that affected an existing missing-author test.
Removing that temporary local name resolved the focused test and the full suite without changing tests or gates.
The stale scratch execution record was corrected. These integration findings are closed after the final passing run.

## Coverage limits and follow-up

Java, Ghidra, radare2, TShark, Volatility, angr, Z3, and Triton were unavailable in the checked execution environment.\
Ghidra GUI/MCP mutation/persistence, Java compilation, native PyGhidra binding, r2 plugins/signatures/replay, system\
boot, debugger attachment, peripherals, crypto proofs, and solver integrations were not executed. The preferred MCP\
integration was inspected at the revision recorded in its package attribution.

Client discovery and controlled model behavior were not measured. Review-lite conclusions are capped at ready with\
risks. A future behavioral evaluation needs explicit cases, clients, repetitions, side effects, and an authorized run\
ceiling. Native-tool smoke tests should use disposable programs and synthetic inputs before retained analysis or live\
targets.

The new `reverse-engineering` group requires a matching entry in the separate installer configuration before its pin\
update. No external configuration, installed skills, running MCP services, remote branches, or deployment state was\
changed.
