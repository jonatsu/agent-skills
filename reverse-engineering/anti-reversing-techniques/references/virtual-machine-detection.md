# Virtual-Machine and Environment Detection

This branch concerns the environment running native code. A custom bytecode interpreter inside a program is a different\
analysis problem.

## Establish That a Check Is Detection

Locate the environment query, its result transformation, and the decision that changes execution. Compare against\
ordinary failure explanations: absent guest loader, missing service used for real work, inaccessible device,\
unsupported CPU instruction, privilege restrictions, or an incorrect emulated machine model.

Record target architecture and OS, hypervisor or emulator configuration, observation method, and input equality. A\
single artifact can identify an environment without showing that the program rejects it. Multiple weak signals can be\
combined; trace the scoring or aggregation logic instead of treating each as independently decisive.

## CPU and Hypervisor Queries

On x86, inspect the actual `CPUID` leaf, returned registers, consumed bits or vendor bytes, and branch condition. The\
conventional hypervisor-present bit and hypervisor vendor leaves are useful hypotheses; target code may use other\
leaves or consistency checks. A hypervisor vendor string does not establish hostile behavior.

A targeted intervention can alter the consumed result in a working-copy analysis or scoped instrumentation route. Where\
an approved disposable guest supports CPU presentation settings, inspect that hypervisor's documented options and the\
current configuration before recommending changes. Do not invent universal command flags or assume that hiding one bit\
conceals all hypervisor behavior.

Preserve register effects and flags relevant to the surrounding code. Later checks may compare independent leaf\
results. Verify the intended analysis region, and compare its inputs with independent observations. Other architectures\
expose different feature and system interfaces; x86 instructions are not a cross-platform recipe.

## Guest Artifacts and Resource Heuristics

Potential queries include firmware tables, device identifiers, guest drivers/services, processes, files, registry\
entries, network adapters, and desktop or user-activity state. Low memory, few CPUs, or a short uptime can also occur\
on legitimate physical systems. Artifact names vary by product and version.

For each queried artifact, record the exact object, API or read path, expected result, error behavior, and downstream\
use. Prefer a scoped query-result intervention when it preserves the surrounding workflow. Changing a disposable\
guest's artifacts is an alternative only where authorized and recoverable. Removing a guest driver can break input,\
networking, storage, or the analysis channel; retain those dependencies in the decision.

A narrowly modeled absence must preserve related size, enumeration, and error semantics. Inspect repeated queries and\
cross-checks. Keep original results with the record so an analyst can distinguish natural from induced behavior.

## Timing and Environment Consistency

Locate the timing sources, units, measured interval, threshold calculation, and all dependent state. Direct timestamp\
instructions, OS clocks, sleep duration, and remote time can be compared. Scheduling, CPU frequency behavior,\
instrumentation overhead, and load complicate interpretation. Fixed cycle thresholds are not portable VM proofs.

Choose an intervention that preserves relationships used downstream: model a consistent local clock progression, reduce\
the specific observation overhead, or patch the confirmed decision in a working copy. Freezing time can break\
deadlines, random seeds, or synchronization; adjusting one clock can contradict another. Record the affected clock\
domain and validate subsequent timed operations.

Special I/O instructions and exception behavior can probe virtualization, but can also fault because of ordinary\
privilege rules. Analyze existing instructions and handlers before attempting execution. Do not issue privileged probes\
on the analyst host as a diagnostic shortcut.

## Minimal Verification Cases

Use locally authorized synthetic fixtures before extending an intervention to a complex target:

- A queried hypervisor bit gates one labeled branch: capture the original result, alter the consumed value, and verify\
  only the expected branch changes.
- A guest-artifact read gates execution: model the query and its error result, then inspect the intended successor.
- Two timing readings gate execution: preserve monotonic relationships and test a later timeout as a countercheck.
- A missing loader prevents startup: diagnose the missing interpreter and recommend its compatible runtime package; no\
  anti-VM intervention applies.

For each case, preserve the original, intervention recipe, recovery, outputs, and unresolved checks. Report static\
walkthroughs separately from executed cases. Reaching one region establishes a local analysis path, not invisibility.
