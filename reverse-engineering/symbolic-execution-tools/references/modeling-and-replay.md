# Modeling and replay

## Preserve machine semantics

Use bitvectors for fixed-width machine arithmetic and integers only for genuinely unbounded mathematical values. Choose\
widths from instructions, including extensions and truncated intermediate results, rather than decompiled names. Make\
signed versus unsigned comparisons, shifts, division, remainder, and overflow explicit. An arithmetic right shift and a\
logical right shift have different high bits; signed division differs from unsigned division. C integer promotions can\
widen a byte before a shift or addition even when storage later truncates it.

Keep input byte order, memory endianness, pointer width, ABI argument locations, stack alignment, and return storage\
explicit. Model loads/stores at their actual width and effective byte offset. A decompiler's pointer arithmetic may be\
scaled. Keep invalid memory, exceptions, and external calls visible; zero-filling unspecified memory invents an\
environment. For a raw routine, provide the stack, return sentinel, data, and any initialized globals it actually\
consumes.

## State assumptions and approximation

Record each assumption with its evidence and its effect on the answer. Printable characters or a familiar prefix are\
constraints only when the target input contract supports them. A single observed random/time value is one environment,\
not all environments. For a library summary, preserve consumed bytes, terminators, return convention, side effects, and\
error behavior. A fixed-size memory comparison is not a general model of a NUL-terminated string comparison. A no-op\
output hook is valid only when output effects and return values cannot affect the analyzed property.

Underapproximation removes possible behaviors and can miss solutions; overapproximation admits extra behaviors and can\
produce candidates that cannot run. Some abstractions mix both effects. Record concretized indices, skipped branches,\
forced returns, bounded loops, and unavailable peripherals. Do not hide model changes as performance flags.

## Replay as the result oracle

First compare one concrete trace or output against the model before symbolizing inputs. Then solve a bounded problem\
and replay its candidate under the original check. For a finite toy check, exhaustive enumeration supplies a useful\
independent oracle. For example, define an unsigned byte gate `((x ^ 0x5a) + 7) mod 256 == 0xa1`. Its candidate is\
`0xc0`: `0xc0 ^ 0x5a == 0x9a`, then `0x9a + 7 == 0xa1`. A solver fixture should also constrain `x == 0` and obtain\
unsat, then replay both inputs in the original arithmetic. This example demonstrates width and validation; it is not\
evidence that an unknown binary uses this check.

Preserve the exact target bytes and hash. Run unknown code only in the authorized isolated execution environment, with\
bounded resources and the intended filesystem/network exposure. Analysis-engine imports do not make samples safe. For\
device-bound behavior, distinguish testing a mathematical predicate from reproducing the physical interaction.

## Interpret stopping conditions

| Result                  | What it establishes                               | What remains open                                              |
| ----------------------- | ------------------------------------------------- | -------------------------------------------------------------- |
| Sat                     | An assignment satisfies the recorded constraints  | Reachability and fidelity of the target model; concrete replay |
| Unsat                   | No assignment satisfies that exact model          | Whether input bounds, hooks, and state match the target        |
| Unknown                 | The solver did not decide                         | The property itself                                            |
| Timeout or state limit  | The resource budget was consumed                  | Unexplored paths and possible candidates                       |
| Unsupported instruction | Semantics are missing at a named address          | Effects needed to continue soundly                             |
| Replay failure          | The model/candidate does not reproduce the oracle | Which initialization, hook, or semantics caused disagreement   |

For multiple candidates, ask whether one witness answers the question or uniqueness/coverage is required. One\
satisfying assignment does not establish that it is the only solution.
