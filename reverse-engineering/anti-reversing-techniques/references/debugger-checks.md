# Debugger Checks

## Locate the First Divergence

Compare ordinary execution with the selected debugger or instrumentation route using identical inputs. Trace\
termination backward to the decision, then forward through both outcomes. Early ELF initialization and PE TLS callbacks\
can execute before the nominal entry routine. Inspect loader events and initialization arrays when entry breakpoints\
arrive too late.

Classify observed evidence before choosing a technique:

| Evidence                                    | Investigation                                                               | Candidate local intervention                                     |
| ------------------------------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Debug-state API query                       | Follow return value and output buffer into the decision                     | Scope a hook to the relevant call and preserve API semantics     |
| Direct process/thread structure read        | Verify target OS/build, architecture, and actual field access               | Modify a working-copy decision or narrowly modeled read          |
| Tracing request fails                       | Inspect error, existing tracer, policy, and namespaces                      | Correct the analysis route or model only the confirmed check     |
| Signal or exception path differs            | Trace handler installation, delivery, debugger first/second-chance settings | Forward the specific exception as the program expects            |
| Code bytes or debug registers are inspected | Identify scanned region and comparison                                      | Use a compatible observation method or controlled decision patch |
| Parent/child repeatedly checks liveness     | Recover protocol, ownership and expected side effects                       | Follow both processes or model the checked exchange              |

A tracing failure is not definitive evidence of another debugger. Permissions, process state, security policy, and\
tracing restrictions can produce the same result. Similarly, a debugger-name string can be a diagnostic message or\
unused data. Require dataflow and a relevant branch before assigning a detection role.

## Linux and Unix-Like Targets

Inspect `ptrace` calls, `/proc` reads, signal handlers, environment checks, parent/process inspection, and memory-map\
scans when present. `LD_PRELOAD` hooks apply only where the dynamic loader and symbol resolution actually use them;\
static binaries, direct syscalls, secure execution, and integrity checks can bypass or expose that method.

For a `TracerPid` reader, trace the parser and all related reads rather than changing one visible string. For a signal\
test, identify the installed handler and the expected state change. Debugger-wide signal suppression can break\
application logic. Read the debugger's local help and configure only the relevant handling rule.

Follow fork/clone and attach ownership where supported. Killing a watchdog is not equivalent to satisfying its\
protocol; the surviving process may wait forever or lose state. Preserve IPC, deadlines, and initialization if you\
model the exchange.

## Windows Targets

API checks may read process debug state directly or indirectly. Inspect `IsDebuggerPresent`,\
`CheckRemoteDebuggerPresent`, relevant process/thread queries, and direct PEB/TEB access only when evidence points\
there. Windows structures exist on multiple architectures; fixed x86/x64 offsets are not portable layouts. Use symbols\
or verified target-build definitions rather than copying offsets into a general patch.

For APIs with separate status and output values, model both correctly. Different information classes can invert boolean\
meanings or use handles and error status. Inspect actual caller expectations before overriding results.

Heap/debug flags can reflect diagnostic configurations as well as debugger launch history. Exception tricks, thread\
hiding, invalid handles, and debug-register inspection depend on OS and debugger behavior. Discover a compatible\
user-mode plugin if useful, then enable only relevant features and verify their effects. Kernel drivers and host-wide\
security changes are not routine prerequisites for this workflow.

## Integrity and Timing Interactions

Software breakpoints modify code bytes; hardware breakpoints have finite resources and may themselves be queried. An\
instrumentation agent can change modules, timing, memory maps, and exception handling. Select the least intrusive\
observation that answers the question and record the footprint it introduces.

After bypassing an early check, continue to the requested region with bounded tracing. Look for repeated checks,\
state-dependent failure, code checksum validation, or a delayed alternate path. Preserve the original result and label\
findings obtained only after modification. There is no supported universal coverage percentage.
