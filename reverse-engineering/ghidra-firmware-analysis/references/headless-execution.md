# Headless execution

Use the supplied installation's launcher and help to confirm supported options and script providers. `analyzeHeadless`\
supports Java scripts; a PyGhidra-enabled installation can expose `pyghidraRun -H` for Python 3. Set shell variables\
below to reviewed absolute paths and names before executing examples. The examples use `headless_launcher` for an\
executable launcher path, not a command string containing flags.

## Fresh import

Choose a new project name and an existing writable project directory. Confirm that the target project does not already\
contain research work before import.

```sh
"$headless_launcher" "$project_dir" "$new_project_name" \
    -import "$binary_path" \
    -analysisTimeoutPerFile 600 -log "$fresh_log_path"
```

For PyGhidra, use the equivalent invocation with the discovered `pyghidraRun` launcher and add `-H` before project\
arguments. For an evidence-supported raw mapping, add `-loader BinaryLoader`, `-loader-baseAddr ADDRESS`, and\
`-processor LANGUAGE_ID`. Confirm loader argument names in the installed help; use the selected language's `.ldefs` to\
resolve its exact identifier. Set `-cspec COMPILER_SPEC_ID` when the default does not match the ABI; it requires an\
explicit processor choice. Record mapping, file offsets, imported ranges, and any relocation setting alongside the\
input hash.

Keep `-overwrite` and `-deleteProject` out of preservation workflows because they can destroy imported research state.\
Review diagnostics for skipped duplicate imports and analysis timeouts even if the launcher returns success.\
`-analysisTimeoutPerFile` limits auto-analysis; it does not set a script's per-function decompiler timeout. Discover\
the launcher's supported JVM heap configuration before adjusting memory limits.

A relocatable ELF module can leave a saved project after reporting unresolved external-data relocations. Trace each\
symbol and addend to its section and consuming function before using the project. Keep the import failure visible: an\
independently checked, unaffected function may support a bounded research edit in an isolated copy, but the whole\
module is not clean. A complete result needs reviewed linkage of the external symbol and a new guarded import;\
suppressing the diagnostic does not resolve the reference.

## Query an existing program

Use an exact program name, the preserved project, and a fresh export destination. Resolve `skill_scripts` to this\
package's `scripts` directory from its actual installed location. For the Java exporter:

```sh
"$headless_launcher" "$project_dir" "$project_name" \
    -process "$program_name" -noanalysis -readOnly \
    -scriptPath "$skill_scripts" \
    -postScript DecompileAll.java "$fresh_output_path" \
    -log "$fresh_log_path"
```

For Python 3, use the discovered PyGhidra launcher with `-H` and replace the script name with `decompile_all.py`.\
Neither exporter assumes a repository, project location, or container filesystem layout. Their only dependency beyond\
the script host is the Ghidra API; they are not ordinary standalone Python or Java programs. `-readOnly` prevents\
saving program changes, but project opening can still require writable locks. Script output writes are separate from\
program persistence and must use an explicitly writable destination.

## Intentional edits and recovery

Before saving edits, preserve the project or a lossless program archive and identify the program by binary hash. Use\
`-process -noanalysis` without `-readOnly` only when the operation intentionally saves changes. Validate complete\
rename/type input before mutation and use a transaction with rollback on failure. Close archive managers and decompiler\
interfaces reliably. Check that labels, signatures, structures, and comments survive reopening, then retain the updated\
preservation copy.

Lossless program archives preserve more than an exported C file or rename list. A semantic inventory can check selected\
annotations but does not prove that every database detail survived. For a version or ownership migration, test recovery\
into a separate project before promoting it. Avoid editing an active script during execution; preserve the exact script\
bytes for each run.

## Scripting limits in headless mode

A script that reaches a Ghidra service through the tool (`getState().getTool().getService(...)`) fails headless:\
`getTool()` returns null there, because the tool and its services are coupled. A script needing such a service must\
inline the logic it would provide, or run in the GUI.

When one script chains another script or an analyzer, wait for auto-analysis to finish before the dependent step: poll\
the analysis state with a short sleep and honour cancellation, so a dependent pass never reads a half-analysed program.

## Upstream references

The [headless guide][headless] specifies import, process, loader, timeout, and read-only semantics. The\
[PyGhidra guide][pyghidra] documents supported Python launchers and script APIs. Consult the equivalent documentation\
bundled with the supplied installation when its version differs.

[headless]: https://www.ghidradocs.com/12.1.4_PUBLIC/support/analyzeHeadlessREADME.html
[pyghidra]: https://www.ghidradocs.com/12.1.4_PUBLIC/Ghidra/Features/PyGhidra/pypkg/README.html
