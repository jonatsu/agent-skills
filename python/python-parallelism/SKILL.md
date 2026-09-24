---
name: python-parallelism
description: Use every CPU core from Python with threads, processes and joblib. Use when slow work might parallelize and you must decide whether it will pay, choosing between threads and processes, running a parameter sweep or batch job, or fixing a pool that hangs or cannot pickle its argument.
license: MIT
compatibility: Measurements and examples target Python 3.12+. The free-threading notes concern 3.13+ free-threaded builds, which are a separate interpreter build from the default one.
metadata:
  author: Joonas Onatsu
---

# Python Parallelism

Using more than one core: choosing threads or processes, paying the overhead knowingly, and the failure modes
that only appear once work crosses a process boundary. Work built on asyncio, including handing a blocking call
off a running event loop, is `python-async-patterns`.

## Respect Project Conventions

Use these defaults for new projects. In established projects, follow declared conventions and consistent local practice,
including for new files and modules. Check both before filling an undecided choice.

Do not recommend changes merely because these defaults differ. Recommend corrections supported by incorrect behavior,
security vulnerabilities, or concrete reliability or maintenance harm. Explain the evidence, consequence, and smallest
remedy. A different tool, layout, style, or supported syntax is not itself a defect.

Apply fixes within the authorized task; otherwise report the recommendation without changing the project.
An explicit modernization or conventions review permits broader recommendations.

## First, Measure. Parallelism Is Usually the Wrong Fix

**Profile before parallelizing.** A better algorithm, a vectorized NumPy call, or removing an accidental
quadratic beats four cores, and none of them add a failure mode. Parallelism is what you reach for when the
work is already efficient and genuinely independent.

Then check that the work is big enough to be worth moving. Measured on CPython 3.12.14, 10 cores: **2000
trivial tasks through a `ProcessPoolExecutor` ran 1348x slower than the same work in a list comprehension** —
0.122s against effectively 0s. Every argument and result was pickled and shipped between processes to save
arithmetic that cost nothing.

That is the normal outcome for small tasks, not a pathological case. A task must be long enough that the
per-task round trip disappears next to it: milliseconds of work per task, not microseconds. When the tasks are
inherently small, chunk them (below).

## Threads or Processes: the GIL Decides

On a default CPython build, the Global Interpreter Lock lets one thread execute Python bytecode at a time.
Threads therefore overlap **waiting**, never Python-level **computing**. Measured on 3.12.14 over four tasks,
pure-Python arithmetic ran 1.01x faster on threads and 3.70x on processes, while blocking `time.sleep` calls ran
3.99x faster on threads. The rule that falls out:

| The work is                                             | Use                                          |
| ------------------------------------------------------- | -------------------------------------------- |
| CPU-bound Python: loops, parsing, `scipy` solves        | `ProcessPoolExecutor`                        |
| Blocking I/O with a synchronous library                 | `ThreadPoolExecutor`                         |
| Blocking I/O, many concurrent operations, async library | asyncio — `python-async-patterns`            |
| CPU-bound inside native code that releases the GIL      | `ThreadPoolExecutor`; measure, do not assume |
| Too big for one machine, or a real task graph           | Dask or Ray                                  |

That fourth row is the one people get wrong in both directions. NumPy, SciPy and pandas release the GIL around
large native operations, so threads can parallelize them — but only for the part that is actually inside the C
code. Time it both ways; the answer depends on the array sizes, not on the library's reputation.

**Free-threaded builds change this rule, and they are a different interpreter.** From 3.13 CPython ships an
optional build with no GIL, where threads do parallelize CPU-bound Python. It is not what `python3` gives you
unless you installed it deliberately — verified on the 3.12.14 and 3.13.15 builds here, both report
`sysconfig.get_config_var("Py_GIL_DISABLED")` as false. That variable says only that the build supports free
threading: a free-threaded interpreter re-enables the GIL at runtime when it imports an extension module not
marked as supporting free threading, or when `PYTHON_GIL` or `-X gil` asks for it. Check
`sys._is_gil_enabled()` (3.13+) in the running process before claiming either behavior, and keep writing code
that is correct on both.

## Use concurrent.futures

`concurrent.futures` is the default API. `ThreadPoolExecutor` and `ProcessPoolExecutor` share one interface, so
testing the other hypothesis is a one-word edit, as long as the payload pickles.

```python
with ProcessPoolExecutor() as pool:
    results = list(pool.map(solve, parameters))     # results in input order
```

`map` is right when you want every result and the input order. When you want to handle results as they land, or
to know which input produced which failure, submit and keep the mapping:

```python
with ProcessPoolExecutor() as pool:
    futures = {pool.submit(solve, p): p for p in parameters}
    for future in as_completed(futures):
        parameter = futures[future]                 # the future alone does not tell you
        try:
            record(parameter, future.result())
        except Exception:
            log.exception("failed for %s", parameter)
```

**An exception in a worker is re-raised at `future.result()`, not where it was raised.** Nothing surfaces until
you call `result()`, so a loop that never does silently discards every failure. `pool.map` raises the first
failure, in input order, when iteration reaches it, and cancels the calls not yet started; the loop above keeps
every other result and names the failing input.

Prefer the default worker count. `ProcessPoolExecutor()` uses the CPUs available to the process; naming a
number hard-codes one machine's shape into the program.

## Chunk Small Tasks

When tasks are inherently short, send fewer, larger units of work rather than giving up the cores:

```python
def solve_chunk(chunk: list[float]) -> list[Result]:
    return [solve(p) for p in chunk]

chunks = [parameters[i:i + CHUNK_SIZE] for i in range(0, len(parameters), CHUNK_SIZE)]
with ProcessPoolExecutor() as pool:
    results = [r for chunk in pool.map(solve_chunk, chunks) for r in chunk]
```

A process pool's `map` also takes `chunksize`, which batches dispatch without changing your function; try it
first, since it costs one argument. `ThreadPoolExecutor.map` ignores it. Explicit chunking wins when the chunk
can do something smarter than a loop, such as one vectorized NumPy call over the whole batch.

## joblib for Scientific Batches

[joblib](https://joblib.readthedocs.io/) wraps the same idea with less ceremony, and scikit-learn already
depends on it, so a project doing modelling usually has it:

```python
results = Parallel(n_jobs=-1)(delayed(solve)(p) for p in parameters)
```

`n_jobs=-1` means every core. It adds progress reporting (`verbose`), a `threading` backend for GIL-releasing
code, memory-mapping of large NumPy arrays between workers, and `Memory` for on-disk caching of expensive calls.
Reach for it when a project already has it or wants those features; `concurrent.futures` is the standard-library
answer and needs no dependency.

Before relying on any of that, read joblib's own documentation, which splits by question:

| You need                                             | Read                                                                                                  |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Backends, `n_jobs`, and when to use each             | [Embarrassingly parallel for loops](https://joblib.readthedocs.io/en/stable/user_guide/parallel.html) |
| An exact `Parallel`, `delayed` or `Memory` signature | [API reference](https://joblib.readthedocs.io/en/stable/references.html)                              |
| A worked version of an awkward case                  | [Examples gallery](https://joblib.readthedocs.io/en/stable/auto_examples/index.html)                  |

## Failure Modes

Arguments, return values and the function itself cross a process boundary by pickle, and workers do not share
memory. That breaks things that work fine in one process — unpicklable arguments, lost global state, correlated
random streams, and deadlocks inherited across `fork`. **Read
[crossing-the-process-boundary.md](references/crossing-the-process-boundary.md) before writing a process
pool**, or when one fails in a way the table below does not explain. The first three fail at the moment of
parallelizing and the fourth fails intermittently in production; the reference has their measured error
messages and fixes.

## Diagnosing

| Symptom                                        | Look at                                                            |
| ---------------------------------------------- | ------------------------------------------------------------------ |
| Parallel is slower than sequential             | Tasks too small; chunk them, or stay sequential                    |
| Threads gave no speedup at all                 | CPU-bound work under the GIL; use processes                        |
| `Can't get local object ...`                   | A lambda or nested function sent to a process pool                 |
| `Can't pickle ...` on an argument or result    | An open file, connection, lock or closure in the payload           |
| Failures vanish, results look short            | `future.result()` never called; exceptions stay in the future      |
| Workers all produce identical "random" results | One seed inherited by every worker                                 |
| `BrokenProcessPool`, or a hang, under `spawn`  | Pool created at import time with no `if __name__ == "__main__"`    |
| Memory blows up with worker count              | A large argument copied per worker; memory-map it or share by path |

## Before Calling Parallel Code Done

1. Is there a measurement showing the parallel version is actually faster than sequential?
2. Is the work CPU-bound in Python (processes) or waiting (threads or asyncio)?
3. Is `future.result()` reached for every submitted task, so failures surface?
4. Does every worker get an independent random stream, if randomness is involved?
5. Is the entry point guarded by `if __name__ == "__main__"`?
6. Are arguments and results small, or deliberately shared rather than copied?
