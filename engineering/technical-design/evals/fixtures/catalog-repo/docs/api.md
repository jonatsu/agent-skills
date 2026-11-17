# API reference

## Command line

```text
catalogcheck PATH
```

`PATH` is the catalog file to check. The command takes no options yet.

## Python

### `catalogcheck.__version__`

The installed version string.

### `catalogcheck.main(argv=None) -> int`

The command's entry point. It reads the arguments from `argv`, or from `sys.argv` when `argv` is `None`, and returns the
process exit status. The current implementation accepts the path argument only; checking is not yet implemented.
