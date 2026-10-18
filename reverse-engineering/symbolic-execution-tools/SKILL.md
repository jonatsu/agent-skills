---
name: symbolic-execution-tools
description: Recover inputs and path conditions for bounded binary routines using symbolic execution and constraint solving. Use for targeted angr exploration, Triton instruction-level symbolic or taint analysis, solver-assisted branch analysis, or validating a recovered check against concrete execution.
license: MIT
compatibility: Requires a Python environment with the selected analysis engine and solver. angr and Triton are alternative branches; target instruction support and guest dependencies must be checked. Concrete replay needs a safe compatible execution or emulation environment.
metadata:
  author: Joonas Onatsu
---

# Symbolic execution for reverse engineering

Answer one bounded question: which inputs reach a branch, satisfy a recovered check, or influence an output? Begin with\
the binary identity, function/address range, architecture/ABI, input boundary, and concrete success oracle. A\
satisfying assignment is a result for the model; confirm it against the original routine before claiming target\
behavior.

## Select the model and discover prerequisites

Use direct SMT constraints when the recovered arithmetic is small and independently understood. Use angr when loading,\
function calls, and path exploration benefit from a program-state framework. Use Triton when a short instruction\
stream, concrete trace, taint question, or selective symbolic input is available. Unicorn is concrete CPU emulation;\
Qiling models selected execution environments. Neither supplies symbolic solving merely by being installed, and neither\
guarantees a complete firmware hardware model.

Check the selected interpreter, engine distribution/version, solver backend, and architecture/instruction coverage.\
Distinguish the Triton binary-analysis library (`triton-library`, importing `triton`) from unrelated GPU software.\
Check required native libraries and guest artifacts from that engine's current installation guidance. Recommend missing\
packages and supported versions for the actual host; do not assume sudo or install silently. Only require the chosen\
branch. A missing engine still permits static slicing and an explicit prerequisite report.

## Bound the question before exploration

Identify the input bytes and their lengths, encoding, provenance, and allowable ranges from evidence. Name the success\
condition by address plus instruction/context, or an observed output whose origin is verified. Define failure and\
stopping addresses, code boundaries, time, state, instruction/loop, and solver budgets. Keep unknown input length or\
load address as explicit alternatives rather than padding until a solver succeeds. Record virtual addresses versus file\
offsets, relocation base, instruction mode, and input hash.

Build the smallest dependency slice containing the check. Inventory memory, registers, globals, imports, callbacks,\
external effects, and return convention that it consumes. Preserve the observed environment or model it explicitly.\
Starting after initialization does not reconstruct its side effects. Use\
[modeling and replay](references/modeling-and-replay.md) for widths, assumptions, hooks, and result interpretation.

## Execute the selected branch

Read [angr targeted analysis](references/angr-targeted-analysis.md) before selecting a state constructor, installing\
hooks, configuring exploration, or extracting results. Read\
[Triton bounded analysis](references/triton-bounded-analysis.md) before translating a trace or snapshot, symbolizing\
inputs, checking instruction support, or solving a branch.

Begin with a concrete known input and compare modeled effects with an independent execution or instruction calculation.\
Then symbolize only the input region needed for the question and keep observed constants concrete with their\
provenance. If the concrete check disagrees, fix initialization or semantics before expanding the search. Introduce\
hooks one at a time and record what each preserves, approximates, or deliberately removes. A forced-success hook is\
useful for downstream exploration, not evidence that the original condition is satisfiable.

When exploration grows, inspect the source of branching or symbolic addresses before constraining further. Use\
evidence-supported domains, focused start states, justified summaries, and finite exploration limits. Do not turn\
arbitrary concretization, dropped paths, or loop cutoffs into a proof of impossibility. Stop on unsupported\
instructions, unknown solver results, or unmet budgets and preserve resumable evidence.

## Validate and deliver

Extract input bytes in the target's actual order, including terminators and lengths. Replay a candidate against the\
unmodified routine with the intended environment and success oracle. Separate replay using the same assumptions from an\
independent corroborating observation. If replay is unavailable, deliver the candidate as conditional and explain\
exactly what must be supplied to verify it.

Report binary/mapping identity, model boundaries, symbolic inputs, concrete state sources, hooks, constraints,\
engine/solver identities, budgets, explored coverage, candidate bytes, and replay observations. Distinguish sat, proven\
unsat for the stated model, unknown, timeout, unsupported semantics, and incomplete exploration. Unsat of an\
overconstrained model does not prove the real program cannot pass. Preserve harnesses, logs, snapshots, and unresolved\
assumptions outside the installed skill package. Completion means the bounded question is answered with its evidence\
and limitations, or the precise stopping cause is recorded.
