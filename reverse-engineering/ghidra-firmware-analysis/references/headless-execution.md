# Headless execution

## Contents

- Fresh import
- Query an existing program
- Intentional edits and recovery
- Open saved projects safely
- Retire a project only after comparing it
- Write scripts against the documented API
- The `pyghidra` command
- Scripting limits in headless mode
- Upstream references

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

The Ghidra front end, not CodeBrowser, holds the project lock, so closing CodeBrowser leaves headless writes blocked.\
Collect headless writes into one window and ask the user to close the whole GUI once for it. Edits to a tool's saved\
configuration files also need the GUI closed. While the GUI stays open, make small edits through MCP instead.

## Open saved projects safely

Ghidra opens a project only from an absolute directory path in which no element starts with a dot, so a project under\
any dot-prefixed directory fails with "Path element starting with '.' is not permitted". A project records its creator\
as `OWNER` in `NAME.rep/project.prp`, and any other user who opens it gets `NotOwnerException`. A project created\
inside a container usually belongs to the container's user. Keep the original as it is; copy the project, and change\
`OWNER` only in the copy.

To read programs without any risk to the saved ones, open a copy with `GhidraProject.openProject(dir, name)` and take\
each program through `DomainFile.getImmutableDomainObject(consumer, DomainFile.DEFAULT_VERSION, monitor)`. The returned\
program cannot be changed or saved to its file. Release it with the same consumer object when done.

## Retire a project only after comparing it

Before deleting a project copy, inventory each of its programs and the retained project's matching program: functions\
with names and signatures, comments by `CommentType`, data types and their archives, and defined data by address and\
type. Key each inventory by the project's directory, because copies often share a project name. Compare the entries\
themselves; equal counts do not show equal content. Delete the copy only when every entry is in the retained project.\
Merge a unique annotation only after checking it against the retained program's bytes, and record the finding it\
carries where the project keeps its findings. Compare two type archives type by type, by path and length, not by file\
hash.

## Write scripts against the documented API

Read a class page from the release's `docs/GhidraAPI_javadoc.zip` with `unzip -p`; the archive holds\
`api/allclasses-index.html` and one page per class under its package path, such as\
`api/ghidra/program/model/data/DataTypeManager.html`. When the documentation leaves a question open, inspect the live\
class once from a PyGhidra session, with `dir()` or Java reflection, instead of rerunning a guessed call. For the\
common edits, start from the patterns in [scripting recipes](scripting-recipes.md), which were checked against the\
12.1.4 API documentation, and confirm each call in the installed release's documentation.

A PyGhidra overload error, `TypeError: No matching overloads found`, prints the accepted signatures. Match them\
exactly: `None` can match several overloads and become ambiguous, Python `str` and `int` arguments may need the Java\
types the signature names, and a task monitor must be the declared `TaskMonitor` type.

Write bulk-edit scripts to handle the common case and to list every site they skip, with its address and reason, in the\
same format on every run. Fix the listed sites by hand. Extending a script to cover each rare shape costs more than the\
manual fixes.

## The `pyghidra` command

The PyGhidra package also installs a `pyghidra` command, separate from `pyghidraRun`. In pyghidra 3.1.0 it takes\
`pyghidra [--project-path DIR --project-name NAME] [--skip-analysis] [BINARY] [SCRIPT.py [ARGS...]]`; the script runs\
with the flat API globals, such as `currentProgram` and `monitor`, and reads its arguments from `sys.argv[1:]`. Know\
three behaviours before relying on it:

- It exits 0 whatever the script does. It catches every exception, `SystemExit` included, and may print no traceback; a\
  path that does not exist prints only the usage text. Have each script write its result to a file, and treat a missing\
  or incomplete file as a failure.
- It nests the project: `--project-path DIR --project-name NAME` opens `DIR/NAME/NAME.gpr`. Pointed at a standard\
  Ghidra project, `DIR/NAME.gpr`, it creates a separate project at `DIR/NAME/` and leaves the standard one untouched.
- It opens the project's program named like the binary, or imports the binary, then analyses it unless\
  `--skip-analysis` is set, and saves the program after the script. It is never a read-only route.

For a standard project, run Python with PyGhidra started instead. Open the project with\
`pyghidra.open_project(dir, name)`, take a program with `pyghidra.program_context(project, "/name")`, and edit inside\
`pyghidra.transaction(program, description)`. Call `program.save(description, pyghidra.task_monitor())` before the\
context ends; without the save, the edits are lost.

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
