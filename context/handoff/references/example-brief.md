# Stateful Handoff Example

Read this example only when a substantial handoff needs more than a task pointer. The repository, paths,
branch, and commit are invented.

```markdown
NEXT. Finish the retry-path conversion on `feat/backpressure`. Done means `retry_saturates` and the full pipeline unit
suite pass without restoring the unbounded channel. Run `git status -sb` before editing because the working tree may have
changed since this brief was written.

CONTEXT. The user prefers `thiserror` over hand-written error enums in this crate. A semaphore implementation was rejected
because its cancellation behavior was harder to reason about. Keep the module's `*_saturates` naming convention for load
tests.

STATE. The bounded queue was committed as `4f1c9ab`. `cargo test -p pipeline` passed at that commit, which covered the unit
suite only. The retry path currently compiles, but `queue_test.rs::retry_saturates` still fails. The integration suite has
not been run.

READ.

- `docs/adr/0007-backpressure.md`, section "Bounded queue": the settled design this work implements.
- `src/pipeline/queue.rs`, symbol `RetryQueue`: the conversion target.
- `tests/pipeline/queue_test.rs`, test `retry_saturates`: the behavioral completion condition.

LOCKED. Keep the queue bounded. The downstream service's per-minute rate limit settled this decision, so memory usage
alone is not grounds to reopen it.

SCOPE. Leave the metrics rewrite parked until the collector upgrade. `_bench/` is intentional scaffolding and must neither
be deleted nor connected during this task.

OPEN. Choose fixed or exponential retry backoff. The current lean is exponential with a 30-second ceiling because the
downstream service rate-limits by minute.

PROCESS. The integration suite silently skips without `DATABASE_URL`. `cargo clippy` runs in CI but not in the pre-commit
hook.
```
