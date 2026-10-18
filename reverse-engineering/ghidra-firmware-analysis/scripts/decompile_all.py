# Ghidra postScript for PyGhidra/Python 3. Requires a loaded current program.
# Usage: -postScript decompile_all.py <fresh-output.c>
from ghidra.app.decompiler import DecompInterface

args = getScriptArgs()  # noqa: F821 - Ghidra flat API global
if len(args) != 1:
    raise ValueError("Usage: decompile_all.py <fresh-output.c>")
out_path = args[0]
program = getCurrentProgram()  # noqa: F821 - Ghidra flat API global
if program is None:
    raise ValueError("A loaded Ghidra program is required")

DECOMPILE_TIMEOUT_SECONDS = 60
decomp = DecompInterface()
count = 0
failed = 0
try:
    if not decomp.openProgram(program):
        raise RuntimeError(f"Cannot open decompiler: {decomp.getLastMessage()}")
    with open(out_path, "x", encoding="utf-8") as output:
        output.write(f"// decompiled from {program.getName()}\n\n")
        for function in program.getFunctionManager().getFunctions(True):
            monitor.checkCancelled()  # noqa: F821 - Ghidra script monitor
            count += 1
            result = decomp.decompileFunction(
                function,
                DECOMPILE_TIMEOUT_SECONDS,
                monitor,  # noqa: F821 - Ghidra script monitor
            )
            monitor.checkCancelled()  # noqa: F821 - cancellation can occur during the final call
            if result and result.decompileCompleted():
                output.write(result.getDecompiledFunction().getC())
                output.write("\n")
            else:
                failed += 1
                error = result.getErrorMessage() if result else "No result"
                error = str(error).replace("\n", " ").replace("\r", " ")
                output.write(
                    f"// FAILED: {function.getName()} @ {function.getEntryPoint()}: {error}\n\n"
                )
finally:
    decomp.dispose()

print(f"wrote {out_path} ({count} functions attempted, {failed} failed)")
