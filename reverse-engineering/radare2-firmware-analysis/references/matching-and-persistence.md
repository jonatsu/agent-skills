# Matching and persistence

Radare2 zignatures match functions using masked bytes, basic-block hashes, and other code features. They use radare2's\
own JSON and SDB formats; Ghidra FunctionID databases and type archives are separate formats.

## Carry names from a donor

Choose analysed, named donor functions whose relationship to the target is supported by build or library evidence.\
Record the donor input hash, analysis mapping, radare2 version, plugin identity, signature SDB hash, and matching\
settings.

```text
zaf sym.name donor_name  signature for one analysed function
zg                      generate signatures from analysed functions
zj                      export signature JSON
zos exports/donor.sdb   save signature SDB
zo metadata/donor.sdb   load signature SDB
z.                      match the current function
e search.in=bin.sections.x
z/                      search executable sections and analysed metrics
zi                      inspect match evidence
```

Confirm command support and matching configuration with installed `z?` and `e??zign` help. Use actual donor symbol\
names and fresh export paths; inspect loaded signature counts before matching. An executable-section search requires\
recognised sections, so use appropriate mapped ranges for a raw image. For each proposed identification, preserve donor\
name, donor hash, target address, and match features. Verify instruction structure, constants, callees, and references\
before recording a confirmed name.

Short common routines can collide; graph, type, reference, and original-offset criteria can add weak matches across\
builds. Inspect which features produced each hit, including adjacent `next` propagation where reported. Keep unresolved\
matches labelled as candidates instead of importing them into another tool as established names. Inspect diagnostics\
and verify exported signatures before reusing an SDB. Successful decompilation can coexist with lossy optional\
signature metadata.

## Preserve types and annotations

```text
"td struct research_record { unsigned int status; unsigned int count; };"
tc struct.research_record
PS exports/session.r2
```

Quote a C declaration so its semicolons remain inside one radare2 command. The example tests parser and persistence\
behavior; it does not describe a recovered firmware structure. Derive real declarations from observed offsets, access\
widths, and operations, recording uncertain field meanings. Check target type widths and ABI before importing\
header-derived declarations.

`session.r2` contains executable commands, file-derived names, inferred functions, signature guesses, and manual\
definitions. Review it before replaying, including commands that reopen a recorded binary path. Use the matching input\
hash, loading model, and path layout. Confirm `-i` support with installed help, then replay into fresh analysis state:

```sh
r2 -N -i "$reviewed_session_path" "$binary_path"
```

Resolve both shell variables to reviewed absolute paths. Check expected symbols, structures, and queried function\
entries after replay. Preserve the original export while testing restoration so a failed replay cannot discard the only\
annotation copy. Verify native project persistence separately if using it; session-script tests do not prove every\
project format preserves analysis.
