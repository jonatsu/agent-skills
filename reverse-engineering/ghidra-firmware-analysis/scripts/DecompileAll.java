// Ghidra headless postScript: export C without overwriting prior evidence.
// Usage: -postScript DecompileAll.java <fresh-output.c>
// Native Java fallback when a Python script provider is unavailable.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.listing.Function;
import java.io.BufferedWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class DecompileAll extends GhidraScript {
    private static final int DECOMPILE_TIMEOUT_SECONDS = 60;

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length != 1) {
            throw new IllegalArgumentException("Usage: DecompileAll.java <fresh-output.c>");
        }
        if (currentProgram == null) {
            throw new IllegalStateException("A loaded Ghidra program is required");
        }
        DecompInterface decomp = new DecompInterface();
        int count = 0;
        int failed = 0;
        try {
            if (!decomp.openProgram(currentProgram)) {
                throw new IllegalStateException("Cannot open decompiler: " + decomp.getLastMessage());
            }
            try (BufferedWriter output = Files.newBufferedWriter(
                    Path.of(args[0]), StandardCharsets.UTF_8,
                    StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE)) {
                output.write("// decompiled from " + currentProgram.getName());
                output.newLine();
                for (Function function : currentProgram.getFunctionManager().getFunctions(true)) {
                    monitor.checkCancelled();
                    count++;
                    DecompileResults result = decomp.decompileFunction(
                            function, DECOMPILE_TIMEOUT_SECONDS, monitor);
                    monitor.checkCancelled();
                    if (result != null && result.decompileCompleted()) {
                        output.write(result.getDecompiledFunction().getC());
                        output.newLine();
                    } else {
                        failed++;
                        String error = result == null ? "No result" : result.getErrorMessage();
                        error = String.valueOf(error).replace('\n', ' ').replace('\r', ' ');
                        output.write("// FAILED: " + function.getName() + " @ "
                                + function.getEntryPoint() + ": " + error);
                        output.newLine();
                    }
                }
            }
        } finally {
            decomp.dispose();
        }
        println("wrote " + args[0] + " (" + count + " functions attempted, " + failed + " failed)");
    }
}
