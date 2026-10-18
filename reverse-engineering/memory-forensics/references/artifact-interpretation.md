# Artifact Interpretation

## Process and Module Survey

Select installed plugins for active process enumeration, process scanning, ancestry, command lines, modules, handles,\
mappings, and network objects. Compare records by PID plus creation/exit context and object addresses. Parent IDs can\
be reused; an unexpected tree alone does not prove process impersonation.

On Windows, common plugin families include process lists/scans, trees, DLL lists, VAD inspection, network scans, and\
registry inspection. On Linux, look for process/task, mappings, loaded modules, sockets, mount, and environment views.\
On macOS, select only plugins compatible with the verified target. Discover exact installed names rather than copying a\
static cross-version command catalog.

For a process found by scanning but absent from an active list, inspect termination state, timestamps, object validity,\
reference context, acquisition timing, and independent views. A terminated or stale object is not necessarily a hidden\
process. A plain text diff of two differently formatted plugin outputs cannot establish hiding.

## Investigate Executable Memory

Private executable mappings, write-and-execute permissions, unexplained threads, PE headers outside normal images, and\
module-list disagreement justify investigation. JIT compilation, browsers, managed runtimes, security products,\
loaders, and legitimate instrumentation can produce similar patterns. A memory analyzer's injection detector is a\
triage heuristic, not a malware verdict.

For each candidate region, record:

- Process identity, virtual range, permissions, backing object, and extraction availability.
- Entry bytes, decoded instructions where appropriate, references, and thread execution context if available.
- Loaded-image relationships, mapped/disk differences where evidence exists, and expected relocation changes.
- Supporting API, handle, network, timeline, or configuration evidence and plausible benign explanations.

A missing MZ header does not rule out injected code. An MZ prefix alone does not prove a valid PE or injection. Check\
complete header bounds, section/mapping relationships, and actual use. A common function prologue is too broad to serve\
as a meaningful standalone malware signature.

## Network and Persistence Context

Correlate socket records with process identities, times, state, and supplied packet/log evidence. Pool scanning can\
recover stale connections; an address in raw memory need not be an active endpoint. Explain the observation rather than\
claiming a live session or attribution without corroboration.

Registry/service/task/module artifacts can suggest persistence. Record the actual key/object, command or target, time\
context, and supporting evidence. Capture omissions or unpaged data can prevent reconstruction. An empty view is a\
coverage statement, not proof of absence.

For kernel anomalies, compare independent module/object views and validate expected symbol/layout assumptions. Hooks or\
callbacks can be legitimate platform/security components. Confirm ownership, target code, and mismatch semantics before\
calling an object a rootkit.

## Strings and Signature Scans

Constrain scans to the relevant range and encoding where possible. Record image/process identity, virtual versus file\
offset, bytes, rule version, and context. Raw physical-image matches lack reliable process attribution until mapped.\
UTF-16 and terminated strings need proper boundaries; split or missing pages can truncate them.

Use specific contextual rules and validate false positives on comparable benign data when available. A YARA match\
establishes the rule condition, not family identity or behavior. Run FLOSS or executable-specific tooling only on\
supported reconstructed executable inputs; an arbitrary flat process dump may not satisfy their loader requirements.

## Timeline Reasoning

Normalize timestamps only with known timezone/source semantics. Account for clock differences, stale objects, partial\
capture, and smear. Preserve contradictory evidence and distinguish observed ordering from inferred causality. State\
what additional disk, network, or execution evidence would distinguish competing interpretations.
