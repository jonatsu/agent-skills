# Attributions

## Current Skill

- Skill: `python-parallelism`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: independently written

## Influencing Sources

Read on 2026-09-15. Neither supplied wording or code.

- ["Parallel Processing in Python"](https://kitchingroup.cheme.cmu.edu/pycse/book/24-parallel-processing.html),
  John Kitchin, *pycse*. Supplied the subject inventory this skill covers: the GIL's split between threads and
  processes, `concurrent.futures` as the unified API, `submit` with `as_completed`, pickling constraints,
  chunking, shared state, joblib, and when to escalate to Dask or Ray.

  **Its measurements were not carried across, because they contradict its own narrative.** Every parallel
  benchmark it prints is slower than the sequential baseline it is compared against — 0.87x for a
  multiprocessing pool, 0.069s against 0.704s for joblib, and 0.006s against 1.382s for a Monte Carlo run — and
  the text presents them as demonstrations of parallelism without remarking on it. That inversion is a genuine
  and useful result, so this skill states it as the lead rule and measures its own version of it.

  **Its parallel-seeding guidance was rejected as unsafe.** The chapter ends on `base_seed + i` with the legacy
  `np.random.RandomState`; NumPy's own documentation marks that exact construction "UNSAFE! Do not do this!"
  This skill teaches `Generator.spawn` and `default_rng([worker_id, root_seed])` instead.

- [NumPy, "Parallel random number generation"](https://numpy.org/doc/stable/reference/random/parallel.html),
  read to settle the seeding question above. It is the authority cited in the reference, not summarized in
  place of it.

Sibling skill `python-async-patterns` supplied the shared structure — decision table first, measured claims,
a closing checklist — and owns the I/O-bound half of the same question.

## Verified Behavior

Measured on CPython 3.12.14, 10 cores, on 2026-09-15, rather than taken from documentation:

- **Threads do not parallelize CPU-bound Python.** Four pure-Python arithmetic tasks: 0.220s sequential, 0.218s
  through a `ThreadPoolExecutor` (1.01x), 0.060s through a `ProcessPoolExecutor` (3.70x).
- **Threads do parallelize blocking I/O.** Four blocking sleeps: 1.200s sequential against 0.301s threaded,
  3.99x.
- **Process overhead dominates small tasks.** 2000 trivial increments took 0.122s through a
  `ProcessPoolExecutor` against effectively 0s sequentially — 1348x slower.
- **Unpicklable callables fail as `AttributeError`, not `PicklingError`.** A lambda reports
  `Can't get local object 'main.<locals>.<lambda>'` and a nested function
  `Can't get local object 'make_local.<locals>.local_fn'`.
- **The default start method on Linux is `fork`** on this version.
- **Neither interpreter here is a free-threaded build.** `sysconfig.get_config_var("Py_GIL_DISABLED")` is false
  on both 3.12.14 and 3.13.15, so the GIL results above describe the default build, which is what
  `python3` gives you.
