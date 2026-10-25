# Scripting recipes

Each pattern is checked against the Ghidra 12.1.4 API documentation. Confirm each call in the installed release's\
documentation before use, as [headless execution][headless] describes. A Java script uses the same classes and calls.

## Contents

- Frame every writing script the same way
- Retype or rename a decompiler local
- Change a parameter, a return type, or a whole signature
- Build types from C headers
- Apply archive types and signatures
- Define data and stack variables
- Comments, labels, and equates
- Navigate references and calls
- PyGhidra and JPype bindings

## Frame every writing script the same way

Check the program before writing: compare `program.getExecutableSHA256()` with the input hash you expect and\
`str(program.getLanguageID())` with the expected language, and stop on a mismatch. Read and classify every site first,\
then make all the edits in one transaction that rolls back on failure:

```python
tx = program.startTransaction("retype from callee signatures")
ok = False
try:
    apply_plan(plan)
    ok = True
finally:
    program.endTransaction(tx, ok)
```

Count each skipped site by its reason, and write the applied and skipped sites with their addresses to a report file;\
the report, not the launcher's exit status, shows whether the run worked. Re-decompile each changed function afterwards\
and compare it with the plan. A headless `-process` run saves the program when the script ends; a standalone PyGhidra\
session must call `program.save(description, monitor)` itself. Call `monitor.checkCancelled()` inside long loops.

## Retype or rename a decompiler local

Decompiler names such as `puVar3` and `local_30` change between runs, so identify a variable by its storage and the\
address of its first use as well. Change a local through its `HighSymbol`:

```python
from ghidra.app.decompiler import DecompInterface
from ghidra.program.model.pcode import HighFunctionDBUtil
from ghidra.program.model.symbol import SourceType

def find_local(high_function, storage, pc_address):
    symbols = high_function.getLocalSymbolMap().getSymbols()
    while symbols.hasNext():
        symbol = symbols.next()
        if str(symbol.getStorage()) == storage and str(symbol.getPCAddress()) == pc_address:
            return symbol
    return None

decompiler = DecompInterface()
decompiler.openProgram(program)
try:
    result = decompiler.decompileFunction(func, 120, monitor)
    if not result.decompileCompleted():
        raise RuntimeError(result.getErrorMessage())
    symbol = find_local(result.getHighFunction(), "r4:4", "00401a20")
    if symbol is not None and not symbol.isParameter():
        HighFunctionDBUtil.updateDBVariable(symbol, None, new_type, SourceType.USER_DEFINED)
finally:
    decompiler.dispose()
```

A symbol whose storage holds its value over the whole function has a null first-use address, which `str()` turns into\
`"None"`. Pass `None` as the name to retype only, or `None` as the type to rename only. Leave parameters to the\
signature recipe below, because `updateDBVariable` on a parameter can rewrite the whole function signature as a side\
effect.

## Change a parameter, a return type, or a whole signature

```python
func.getParameters()[0].setDataType(file_pointer, SourceType.USER_DEFINED)
func.setReturnType(char_pointer, SourceType.USER_DEFINED)
```

To apply a whole declaration from C text:

```python
from ghidra.app.cmd.function import ApplyFunctionSignatureCmd
from ghidra.app.util.parser import FunctionSignatureParser

parser = FunctionSignatureParser(program.getDataTypeManager(), None)
signature = parser.parse(func.getSignature(), "char *read_line(char *buf, int size, FILE *stream)")
command = ApplyFunctionSignatureCmd(func.getEntryPoint(), signature, SourceType.USER_DEFINED)
if not command.applyTo(program, monitor):
    raise RuntimeError(command.getStatusMsg())
```

Check `func.getSignatureSource()` first, and leave a `USER_DEFINED` signature alone unless replacing it is the point. A\
function whose signature is still the default has no database parameters until a write creates them; read its\
parameters from the decompiler's `HighParam` variables, whose `getSlot()` gives the position.

## Build types from C headers

```python
from jpype import JArray, JString
from ghidra.app.util.cparser.C import CParserUtils

def java_strings(values):
    return JArray(JString)([JString(value) for value in values])

archive = CParserUtils.parseHeaderFiles(
    None, java_strings(headers), java_strings(include_dirs), java_strings(["-DCONFIG_SMP=1"]),
    archive_path, str(program.getLanguageID()),
    str(program.getCompilerSpec().getCompilerSpecID()), monitor)
try:
    archive.save()
finally:
    archive.close()
```

This form writes a new archive, so give it an `archive_path` where no file exists yet. Pass archives the headers depend\
on as `JArray(DataTypeManager)([dependency])` in the first argument, and list headers in dependency order. To add types\
to a manager that already exists, use the form that takes that `DataTypeManager`, inside its own transaction. Check the\
result before using it: compare each structure's `getLength()`, each component's `getOffset()`, and the archive's\
`getDataOrganization().getPointerSize()` with the target. The parser's packing limits are in\
[FunctionID and type metadata][metadata].

## Apply archive types and signatures

```python
from java.util import ArrayList
from ghidra.app.cmd.function import ApplyFunctionDataTypesCmd

managers = ArrayList()
managers.add(archive)
command = ApplyFunctionDataTypesCmd(managers, None, SourceType.ANALYSIS, False, True)
command.applyTo(program, monitor)
```

`None` covers the whole program, and `True` bookmarks each change. With `False`, the command replaces only signatures\
whose source ranks below its own `SourceType.ANALYSIS`, so imported and user-defined signatures stay. Copy a single\
type into the program with `program.getDataTypeManager().resolve(data_type, DataTypeConflictHandler.DEFAULT_HANDLER)`.

## Define data and stack variables

```python
from ghidra.app.cmd.data import CreateDataCmd
from ghidra.program.model.data import ArrayDataType, DataUtilities, PointerDataType

command = CreateDataCmd(address, data_type, False, DataUtilities.ClearDataMode.CLEAR_ALL_CONFLICT_DATA)
if not command.applyTo(program):
    raise RuntimeError(command.getStatusMsg())
```

Build an array with `ArrayDataType(element, count, element.getLength())` and a pointer with\
`PointerDataType(target, program.getDataTypeManager())`. Confirm afterwards that\
`listing.getDataAt(address).getLength()` equals the type's length. For a stack aggregate, take\
`frame = func.getStackFrame()`, clear each variable the span overlaps with `frame.clearVariable(offset)`, and create\
the aggregate with `frame.createVariable(name, offset, data_type, SourceType.USER_DEFINED)`. Stop instead when an\
overlapped variable is `USER_DEFINED`, since that is someone's earlier work.

## Comments, labels, and equates

Write comments with `listing.setComment(address, CommentType.EOL, text)` and read them with\
`listing.getComment(CommentType.EOL, address)`; the enum, in `ghidra.program.model.listing`, also has `PRE`, `POST`,\
`PLATE`, and `REPEATABLE`. The `CodeUnit` integer constants are deprecated for removal. Rename with\
`symbol_table.getPrimarySymbol(address).setName(name, SourceType.USER_DEFINED)`, or create a label with\
`symbol_table.createLabel(address, name, SourceType.USER_DEFINED)` where none exists. Name a constant operand with\
`SetEquateCmd(name, address, operand_index, value).applyTo(program)`, imported from `ghidra.app.cmd.equate`.

## Navigate references and calls

`program.getReferenceManager().getReferencesTo(address)` yields references with `getFromAddress()` and\
`getReferenceType()`. `func.getCallingFunctions(monitor)` and `func.getCalledFunctions(monitor)` walk the call graph.\
In a decompiled function, `high_function.getPcodeOps()` yields operations: for `op.getOpcode() == PcodeOp.CALL`,\
`op.getInput(0).getAddress()` is the callee and `op.getInput(i + 1)` is argument `i`.

## PyGhidra and JPype bindings

- Pass Java arrays where a signature names one: `JArray(JString)([...])` for `String[]`, and\
  `buf = JArray(JByte)(count)` for `memory.getBytes(address, buf)`, which fills the buffer.
- Pass a `java.util.ArrayList` where a signature names a `List`.
- Pass a Java object where a signature names `Object`, such as `JString("reader")`; a Python `object()` matches no\
  overload.
- Pass a real `TaskMonitor`, such as the script's `monitor` or `pyghidra.task_monitor()`.
- Walk a Java `Iterator` with `hasNext()` and `next()`.
- Compare Java objects with `.equals()`, because Python `is` is unreliable on the wrappers.
- Mask a signed Java `int` with `& 0xFFFFFFFF`, and convert an address with `str(address)` before joining it to text.

[headless]: headless-execution.md
[metadata]: functionid-and-typeinfo.md
