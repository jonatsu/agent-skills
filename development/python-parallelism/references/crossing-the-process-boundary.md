# Crossing the Process Boundary

Read this before writing a process pool. Workers are separate interpreters: the function, its arguments and its
results travel by pickle, and nothing else is shared. Four consequences break code that works in one process.

## Not Everything Can Be Sent

The function itself is pickled by qualified name, so it must be importable from the module top level. Measured
on CPython 3.12.14, submitting a lambda or a nested function to a `ProcessPoolExecutor` fails with:

```text
AttributeError: Can't get local object 'main.<locals>.<lambda>'
AttributeError: Can't get local object 'make_local.<locals>.local_fn'
```

Note the class: it is an `AttributeError` naming the object's scope path, not a `PicklingError`, so searching
for "pickle" in the traceback finds nothing. Define the worker function at module level. Where you need to bind
extra arguments, use `functools.partial` on a module-level function rather than a closure.

Arguments and return values have the same constraint. Open files, sockets, database connections, locks,
generators and loggers do not pickle. Pass a path, a DSN or a plain value and let the worker open its own.

`joblib` uses `loky`, which pickles with `cloudpickle` and therefore accepts lambdas and closures. That is a
real convenience, and it is also why code written against joblib does not necessarily port to
`ProcessPoolExecutor` unchanged.

## Workers Do Not Share Memory

A global mutated in a worker changes that worker's copy and nothing else. The parent sees no change, and
neither does any sibling. Return the result instead — that is what the return value is for.

Where genuinely shared state is unavoidable, `multiprocessing.Manager` provides proxied objects and
`multiprocessing.shared_memory` provides a raw shared buffer, both at a synchronization cost that frequently
erases the speedup. Prefer a design where workers are independent and the parent combines their results.

Large read-only inputs are the common case that looks like it needs sharing. A big NumPy array passed as an
argument is copied into every worker. Write it to disk and let workers memory-map it, or use joblib, which
memory-maps large arrays for you.

## Random Streams Must Be Split Deliberately

Workers that inherit one seed produce identical "random" results, which silently biases everything downstream.
The fix that looks obvious — adding the worker ID to a root seed — is documented by NumPy as unsafe: repeat
runs whose root seeds differ by a small increment produce overlapping worker streams, so subsets of workers
return identical results across runs.

Spawn instead:

```python
parent = np.random.default_rng(root_seed)
streams = parent.spawn(n_workers)          # one independent Generator per worker
```

Or derive each worker's generator from the ID and the root seed as a **list**, with the varying ID first:

```python
rng = np.random.default_rng([worker_id, root_seed])
```

Both go through `SeedSequence`, which hashes its inputs so that nearby seeds produce distant states. The
authority is NumPy's
[parallel random number generation](https://numpy.org/doc/stable/reference/random/parallel.html) page; check it
rather than a summary. For the standard library's `random`, give each worker its own `random.Random(seed)`
instance rather than sharing the module-level one.

## Start Methods, and Why fork Bites

Measured on CPython 3.12.14 on Linux, the default start method is `fork`: the child is a copy of the parent's
memory, made without running its imports again.

That is fast, and it is also why a forked child can inherit a lock held by a thread that does not exist in the
child — which deadlocks, intermittently, usually under load and rarely in testing. Any program that combines
threads with `fork` has this exposure. `spawn` starts a fresh interpreter and has no such inheritance; it is
the default on macOS and Windows, which is one reason a pool that works on Linux can behave differently there.

```python
mp.set_start_method("spawn")        # once, at start-up, before creating any pool
```

Choose `spawn` or `forkserver` for any program that also uses threads. CPython is moving the same way — 3.14
changes the Linux default to `forkserver` — so code that only works under `fork` is on borrowed time. Confirm
the default for the versions you target with `mp.get_start_method()` rather than assuming either.

Under `spawn`, the child re-imports the main module. **Module-level code that creates a pool then runs again in
every worker**, which spawns processes without end. Guard the entry point:

```python
if __name__ == "__main__":
    main()
```

This is not optional style. It is what makes a process pool safe to import.
