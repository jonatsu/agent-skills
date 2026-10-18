# angr targeted analysis

## Initialize the relevant state

Inspect the installed angr/Claripy versions and loader results before constructing the harness. Confirm architecture,\
object bases, rebasing, imports, and the actual addresses of find/avoid targets. A hard-coded address from another\
mapping can solve the wrong path. With `auto_load_libs=False`, external functions still need appropriate summaries or\
explicit handling; turning off shared-library loading does not implement their semantics.

Select the constructor deliberately:

| Constructor       | Intended boundary          | Required justification                                                   |
| ----------------- | -------------------------- | ------------------------------------------------------------------------ |
| `entry_state`     | Main binary entry          | Arguments, environment, stdin/files, and loader expectations             |
| `full_init_state` | Initializers before entry  | Supported initialization and environment model                           |
| `call_state`      | One function call          | Prototype, calling convention, arguments, pointed-to memory, globals     |
| `blank_state`     | Arbitrary machine location | Every consumed register, memory range, stack effect, and path assumption |

Inspect warnings about unconstrained state. Determine whether those bytes/registers are legitimate inputs or missing\
setup. Do not use blanket unconstrained-state suppression as evidence that initialization is correct. For a function,\
verify argument/return storage against instructions even when a prototype was supplied.

## Inputs and hooks

Construct symbolic stdin, argv, files, or memory with an evidence-supported length and terminator policy. Constrain\
only documented or observed input domains; include newline/EOF behavior in the input model. Preserve the symbolic\
object used as input so extraction does not accidentally return unrelated stdin bytes. Use the installed API\
documentation for SimFile/SimFileStream and explicit end-of-file behavior.

Prefer reviewed built-in SimProcedures where their semantics match the target library version. For custom summaries,\
document the preconditions, side effects, return width, and unsupported cases. Compare a concrete call's effects with\
the summary before exploration. Hooking a check to return success deliberately changes the question; label resulting\
paths accordingly. Treat uninitialized bytes, random numbers, syscall results, and string comparisons as part of the\
model.

## Explore and bound

Set explicit find/avoid predicates tied to verified addresses or outputs. Use the simulation manager's supported\
exploration-technique API; inspect installed help/examples before copying keyword syntax. Veritesting and merging can\
help some branch structures but are not universally beneficial. DFS changes search order, not semantic coverage.\
`LAZY_SOLVES` delays satisfiability checks; it does not bound loops. Use explicit stepping/instruction/loop/state\
limits plus wall and solver time budgets as appropriate.

Inspect active, found, deadended, errored, unconstrained, and budget-pruned states rather than only checking\
`found[0]`. Preserve exceptions and the address of the first unsupported or mis-modeled operation. Constrain symbolic\
addresses only when evidence supports the chosen region or index range. A forced concrete address can hide the path\
that answers the question.

Unicorn acceleration may execute supported concrete regions faster when available in the installed angr build. Check\
architecture/backend support and compare a known input before trusting the accelerated route. It is an execution\
optimization, not an independent corroborating model.

## Extract and check

For a found state, solve the preserved symbolic input and serialize bytes in target order. Recheck all constraints for\
the candidate and record whether unconstrained data influenced success. Replay the full input against the original\
routine and compare the intended branch/output. Retain unknown or incomplete runs separately from an unsat result.

## Authoritative references

- [State constructors and memory](https://docs.angr.io/en/latest/core-concepts/states.html)
- [Hooks and environment limitations](https://docs.angr.io/en/latest/advanced-topics/gotchas.html)
- [State option meanings](https://docs.angr.io/en/latest/appendix/options.html)
