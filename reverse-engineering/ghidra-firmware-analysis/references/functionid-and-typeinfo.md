# FunctionID, type archives, and symbol metadata

## Contents

- Symbol sources
- FunctionID
- Type archives, built from headers or from compiler debug information
- Keep archive references resolvable
- Locking and validation

Names, function matches, and C types solve different gaps in a stripped program. Determine what already survives in the\
input before building or applying external metadata.

## Symbol sources

A stripped ELF can retain exported dynamic symbols in `.dynsym` after losing `.symtab`. A dynamic caller may retain\
named imports through relocation and linkage metadata. Static functions and non-exported application code often need\
recovery from donors, strings, or call patterns. Relocatable kernel modules may retain full symbols, but inspect each\
input rather than assuming that all modules are unstripped. Record each name's source: file symbol, matching candidate,\
debug string, or confirmed research inference.

Before recovering a name by hand, check whether an authoritative symbol or debug source exists for a recognisable\
component and can be fetched by build identity. An ELF carries a `.note.gnu.build-id` that debuginfod resolves to\
separated debug info, and a Windows binary resolves its PDB from a symbol server by GUID and age. A stripped\
proprietary firmware's own code has no such source, but an upstream library, kernel, or module build often does, and\
matching the exact upstream version is the discipline donor selection already demands.

## FunctionID

A FunctionID database (`.fidb`) recognises known compiled function bodies and can supply names for statically linked or\
duplicated code. Build donors from named binaries whose provenance and compiler relationship to the target are\
understood. Record donor hashes, source/build versions, language ID, selection criteria, and database identity. Inspect\
the installed FunctionID plugin documentation for database creation and attachment. For a bulk or headless run, load\
the FunctionID databases from a folder at the start and unload them after, so the set can change between files without\
a permanent install.

Check exact language compatibility before applying a database. A donor analysed under a different processor variant may\
be rejected even when both binaries use the same broad architecture. Compiler options, relocation, and\
position-independent code can change matching effectiveness. A hash hit alone does not establish the application-level\
role of a common wrapper or tiny helper. Corroborate matches using callers, constants, argument effects, and\
instructions before accepting disputed names.

Prepare donors so that ingest records them. FunctionID names an entry from the function's primary symbol, so it skips\
functions that still carry default `FUN_` names. Analyse donors with the Function ID and Library Identification\
analyzers disabled, so earlier matches do not contaminate the database. Disable the Demangler too when the database\
must match raw mangled names. The bundled `FunctionIDHeadlessPrescript` shows these settings for a headless import.

Most false positives come from tiny functions and from recurring idioms, such as destructors that compile identically\
under different names. Raising the instruction-count threshold in the analysis options suppresses the tiny matches,\
at the cost of some true ones. Per-entry flags tune one database more precisely:

- Force Specific accepts the entry only on an exact full-hash match, which suits idioms that embed known constants.
- Force Relation requires a matching parent or child, which separates large idioms.
- Auto Fail never matches the entry.
- Auto Pass lets a short function with a distinctive instruction sequence pass the threshold.

Set them in the FunctionID debug windows, or in a script on a modifiable `FidDB` with `setForceSpecificByFullHash` and\
its `ForceRelation`, `AutoFail`, and `AutoPass` siblings. Then save the database. `FIDHashCurrentFunction` prints a\
function's hashes. `RemoveFunctions` prunes a finished database and `RepackFid` compacts it; the FunctionID feature's\
`data/building_fid.txt` records how Ghidra tuned its shipped databases.

Version Tracking can correlate programs and propagate accepted annotations. BSim searches decompiler-derived similarity\
signatures and can identify near matches beyond byte-identical code. Both require their own supported setup and match\
review; availability does not establish that a database has already been built.

Partition BSim signatures across several databases by trust level rather than one large store: a single H2 database has\
a signature ceiling and slows as it grows, and one database forces a single similarity threshold across every corpus.\
Query each database at its own threshold, highest-trust first.

## Type archives

A `.gdt` archive stores structures, typedefs, and function signatures. FunctionID supplies a candidate identity; a\
compatible archive can supply its declaration and layout. Build header-derived archives from the correct library\
version with parser profiles and target data organisation. Record header sources, patches or stubs, processor/compiler\
settings, pointer widths, scalar widths, alignment, and calling convention.

Type archives are not governed by the same universal exact-LanguageID rule as FunctionID. Verify the stored data\
organisation and destination ABI rather than rejecting or accepting solely from the archive filename. Inspect installed\
C-parser and Data Type Manager documentation for the actual archive constraints and application options. Ghidra's\
bundled generic archives are the default for common library imports. Measure what they already supply before building\
a libc archive. Analysis applies `generic_clib` automatically, and in 12.1.4 it already gives complete 32-bit layouts\
for `FILE`, `struct stat`, `struct tm`, and `pthread_mutex_t`. A target-specific libc archive then adds mainly the\
functions `generic_clib` lacks and exact-version provenance. When an archive built from the target's exact\
library version is available, compare the two on the types the program uses, and prefer the target-specific archive\
where it is more accurate. Measure the remaining gaps before constructing another archive. Library headers do not\
recover proprietary application structures that were never published.

### Build an archive from headers

For a reached private structure, check retained type archives and original source headers before writing a declaration.\
Parse the unchanged header with the target's language, data organisation, include paths, and defines when possible.\
Import only types with observed consumers; a large parsed archive does not establish coverage in the firmware.

A successful parse is not a layout check. Inspect size, alignment, field names, and offsets in the generated archive,\
then compare every applied field with target loads and stores. Ghidra's C-parser can accept a GCC\
`__attribute__((packed))` yet give the composite natural alignment. Keep a minimal parser adapter such as\
`#pragma pack` when needed, or use compiler-derived layout evidence; never silently replace a packed source type with\
the parser's natural-aligned version.

When an original header needs a type already present in a compatible `.gdt`, pass that archive as a parser dependency\
rather than transcribing the generic type. If the API needs sibling locks, copy it into a temporary directory under its\
original file name, as "Keep archive references resolvable" explains. A self-contained archive is useful for\
distribution, not an unconditional requirement for a guarded, per-target application.

If direct parsing fails, inspect `<output>_CParser.out` for the failing declaration. As a fallback, let the target\
compiler preprocess the real headers with their include paths and feature defines. Remove unsupported inline bodies or\
attributes only after checking whether they affect layout or signatures; preserve required packing and calling\
conventions. Record the source, any adapter, ABI, and parser diagnostics with the archive.

### Build an archive from compiler debug information

The C-parser rejects glibc's internal headers, such as `libio.h` and `bits/*`, whichever sysroot supplies them; a\
fuller sysroot reproduces the failure. Let the target compiler compute the layouts instead, and import them as DWARF:

1. Write a probe source that references every type you need.
2. Compile it with the target's own cross-compiler at `-g -O0 -fno-eliminate-unused-debug-types`.
3. Import the object into Ghidra with the target language forced.
4. Export its DWARF types into a file archive created for the same language and compiler spec.
5. Compare a few known sizes, such as `struct stat` and `FILE`, against the target ABI.

Take function signatures separately. `gcc -aux-info` over the public headers emits normalised prototypes that the\
C-parser accepts; parse them into a copy of the DWARF archive. Parsing a prototype that names `struct X *` can create a\
new, empty `struct X` that shadows the complete DWARF one, so the parameters bind to the empty type. After the parse,\
replace each empty composite with its complete namesake through `DataTypeManager.replaceDataType`. Then confirm that the\
parameters point at the complete type.

A kernel or kernel-module archive also depends on the kernel configuration, because options change struct layouts.\
Compile the probe with the kernel's own build system, against a tree configured like the target. When the target's\
configuration is unknown, infer each layout-affecting option from the symbols it adds. A symbol's presence in\
`kallsyms` or the kernel image settles the option. For example, `spin_bug` shows spinlock debugging is enabled, which\
enlarges every structure that holds a lock. Check the finished archive against a structure the firmware initialises\
statically, such as a `file_operations` table whose relocated members land at known offsets.

Apply signatures only after verifying both the function identity and its argument/return storage. A C wrapper's calling\
convention can differ from a raw syscall or firmware service ABI. Record uncertain pointer meanings instead of\
interpreting every machine word as a pointer. Preserve existing user-defined types and annotations before applying\
replacements.

## Keep archive references resolvable

A program records each source archive by name, taken from the `.gdt` file name. On open, the GUI looks that name up in\
the Data Type Manager's archive search paths; it does not find the archive by its internal ID. A temporary copy with a\
generated name therefore leaves the program pointing at a file that no longer exists.

Keep one archive per module or library, with a stable name, in a directory listed under Edit Archive Paths. Build a new\
or rebuilt archive at that location under the same name, rather than writing versioned copies into run output. Each new\
name leaves the program with one more reference the GUI must resolve.

Moving types between archives can break their association: `replaceDataType` can leave the replacement as a\
program-local type. Re-associate types with `DataTypeManager.associateDataTypeWithArchive`, remove retired archive\
records with `removeSourceArchive`, and repair a stale archive name with `updateSourceArchiveName` after matching the\
archive's UniversalID. Then reopen the program in the GUI and confirm that no "Archive file not found" dialog appears.

## Locking and validation

Some archive and database APIs create sibling lock files even when the metadata itself is only being read. If a\
read-only source mount prevents opening, copy the verified metadata into a writable temporary directory, keeping its\
file name, and use that copy. Keep the original bytes and hashes intact; check diagnostics rather than treating an\
empty application count as success. Close archive managers after use.

Validate effectiveness against a pre-application inventory: names, signatures, structures, and failed decompilations.\
Keep automatic matches separate from confirmed human annotations, and preserve rollback evidence when an application\
fails.
