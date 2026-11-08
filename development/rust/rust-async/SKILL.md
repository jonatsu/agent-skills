---
name: rust-async
description: Write and review asynchronous Rust on tokio. Use for spawning tasks, Send and 'static errors on spawned futures, blocking calls inside async code, select! and cancellation safety, timeouts, channels, shared state and locks across await, graceful shutdown, and async functions in traits. Child processes and signals belong to rust-unix-processes, async tests to rust-testing.
license: MIT
compatibility: Rust 1.85 or later (edition 2024) with tokio 1 and tokio-util 0.7.
metadata:
  author: Joonas Onatsu
---

# Rust Async

Asynchronous Rust on the tokio runtime: how tasks run, how they stop, and how they shut down. Code that
compiles can still hang, lose data on cancellation, or stall the runtime, so most of this skill is about those
failures. Other subjects have their own skills:

| Subject                                                     | Skill                 |
| ----------------------------------------------------------- | --------------------- |
| Everyday style, lints, and the crate's minimum Rust version | `rust-style`          |
| Error types inside tasks and at the binary's edge           | `rust-error-handling` |
| Child processes, pseudo-terminals, and Unix signals         | `rust-unix-processes` |
| `#[tokio::test]`, paused time, and testing async code       | `rust-testing`        |

Current known: tokio 1.54.1 and tokio-util 0.7.20, checked on 2026-11-08 against their API documentation for
those versions. tokio-util changes its API between minor versions, so confirm a signature on docs.rs for the
version in `Cargo.lock`.

## The Runtime

`#[tokio::main]` starts the multi-threaded runtime by default, with one worker thread per CPU; it needs tokio's
`macros` and `rt-multi-thread` features. Use one runtime per process. From synchronous code, build a `Runtime`
and call `block_on` at the top; calling `block_on` from inside an async context panics.

Dropping the runtime, which happens when `main` returns, drops each async task the next time it yields and
waits for it. It also waits forever for every `spawn_blocking` closure that has started, and for a task that
never yields. A blocking read that never returns therefore keeps the process alive after `main` returns. To
bound that wait, build the `Runtime` yourself and end with `runtime.shutdown_timeout(duration)`, which returns
after the timeout and leaves stuck work running until the process exits.

## Blocking Work

An async task runs on a shared worker thread until it reaches an `.await`. Code that blocks that thread stalls
every other task on it: `std::thread::sleep`, `std::fs` calls on slow storage, a blocking `read` on a file
descriptor, a long CPU loop, or a `std::sync::Mutex` held for long.

- Use the async equivalent when one exists: `tokio::time::sleep`, `tokio::fs`, `tokio::net`,
  `tokio::process`. `tokio::io::stdin()` is not one for interactive input: it reads on a blocking thread that
  cannot be cancelled, so shutdown hangs until the user presses Enter. Read a terminal on a dedicated
  `std::thread` and send the input over a channel.
- Move bounded blocking work into `tokio::task::spawn_blocking`, and await its handle.
- Run an endless blocking loop, such as reading a terminal or a pipe forever, on a thread from
  `std::thread::spawn`. A `spawn_blocking` closure cannot be aborted once it starts, and it holds runtime
  shutdown open until it returns.
- Limit parallel CPU-bound work with a `Semaphore`, because the blocking pool allows hundreds of threads.

`tokio::fs` itself runs each call through `spawn_blocking`, so many small file operations are cheaper as one
`spawn_blocking` closure that uses `std::fs`.

```rust,run
use std::path::PathBuf;

async fn count_lines(path: PathBuf) -> std::io::Result<usize> {
    tokio::task::spawn_blocking(move || {
        let text = std::fs::read_to_string(path)?;
        Ok(text.lines().count())
    })
    .await
    .expect("the blocking task does not panic")
}

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let file = tempfile::NamedTempFile::new()?;
    std::fs::write(file.path(), "one\ntwo\n")?;
    assert_eq!(count_lines(file.path().to_owned()).await?, 2);
    Ok(())
}
```

## Spawned Tasks

`tokio::spawn` requires a future that is `Send + 'static`: it may move to another thread and may outlive the
caller. Two errors follow from that.

- **`'static`:** the task cannot borrow from the caller. Move owned values in with `async move`, and clone an
  `Arc` before spawning so the task gets its own handle.
- **`Send`:** every value alive across an `.await` must be `Send`. A `std::sync::MutexGuard`, an `Rc`, or a
  `RefCell` borrow held over an `.await` makes the whole future non-`Send`. End the guard's scope before the
  `.await`, as in a block, rather than reaching for an async lock.

```rust,compile_fail
// error: future cannot be sent between threads safely
use std::sync::{Arc, Mutex};

async fn record(counter: Arc<Mutex<u64>>) {
    let mut count = counter.lock().unwrap();
    *count += 1;
    tokio::task::yield_now().await;
}

fn main() {
    let counter = Arc::new(Mutex::new(0));
    drop(tokio::spawn(record(counter)));
}
```

```rust
use std::sync::{Arc, Mutex};

pub async fn record(counter: Arc<Mutex<u64>>) {
    {
        let mut count = counter.lock().expect("lock poisoned");
        *count += 1;
    }
    tokio::task::yield_now().await;
}

pub fn start(counter: Arc<Mutex<u64>>) -> tokio::task::JoinHandle<()> {
    tokio::spawn(record(counter))
}
```

Dropping a `JoinHandle` does not stop the task; it detaches it, and its result and any panic are lost. Keep
every handle you need to wait for, or put the tasks in a `JoinSet` or a `TaskTracker`. Awaiting a handle gives
`Err(JoinError)` when the task panicked or was aborted; check `is_panic` and `is_cancelled` rather than
unwrapping, so one failed task does not hide the reason. `abort` only requests cancellation; await the
handle to know that the task has stopped.

`JoinSet` aborts all of its tasks when dropped and collects their results through `join_next`.
`tokio_util::task::TaskTracker` only waits for tasks, frees each one as it finishes, and does not abort on drop.
Use `JoinSet` when you need the results, and `TaskTracker` for long-running services that spawn many tasks.

## Shared State

Use `std::sync::Mutex` for shared data, and lock it only inside short non-async sections. The tokio
documentation recommends this over `tokio::sync::Mutex`, which is slower and exists to be held across an
`.await`. Reach for the async mutex only when the guarded value is used across an `.await`, as with a
connection. Often the better design is a task that owns the resource and receives requests over a channel.

## Cancellation

Dropping a future cancels it. It stops at the `.await` it was waiting on, the code after that point never runs,
and its local values are dropped. `select!`, `timeout`, `JoinHandle::abort`, a dropped `JoinSet`, and runtime
shutdown all cancel this way. Ask of every `.await` in a cancellable future: is the state consistent if the
function stops here and is never resumed?

An operation is **cancellation safe** when dropping it before it completes loses nothing, so recreating it
continues the work. The tokio documentation lists, among others:

| Cancellation safe                                               | Not cancellation safe                                                                                                            |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `mpsc::Receiver::recv`, `broadcast::Receiver::recv`             | `AsyncReadExt::read_exact`, `read_to_end`, `read_to_string`                                                                      |
| `watch::Receiver::changed`                                      | `AsyncWriteExt::write_all`                                                                                                       |
| `TcpListener::accept`, `UnixListener::accept`                   | tokio's `Mutex::lock`, `RwLock::read` and `write`, `Semaphore::acquire`, `Notify::notified`, which lose their place in the queue |
| `AsyncReadExt::read`, `AsyncWriteExt::write`, `StreamExt::next` |                                                                                                                                  |
| `signal::unix::Signal::recv`                                    |                                                                                                                                  |

Cancelling an unsafe operation is not always a bug: during shutdown, a half-read message usually does not
matter. It is a bug inside a loop that retries, where each cancellation silently loses data.

## `select!`

`tokio::select!` polls its branches in random order unless the first line is `biased;`, and it drops every
branch that did not finish. Use `biased;` when one branch, such as shutdown, must win a tie.

A branch is disabled for that call when its `, if condition` precondition is false or when its result does
not match its pattern. `else` runs only when every branch is disabled; without an `else`, that case panics. A
branch with an irrefutable pattern, such as `() = token.cancelled()`, is never disabled. So once
`Some(job) = jobs.recv()` stops matching at the end of the channel, `select!` keeps waiting on the token, and
the loop hangs instead of reaching `else`. Match the end of a channel explicitly:

```rust,run
use tokio::sync::mpsc;
use tokio_util::sync::CancellationToken;

async fn drain(mut jobs: mpsc::Receiver<u32>, token: CancellationToken) -> u32 {
    let mut total = 0;
    loop {
        tokio::select! {
            biased;
            () = token.cancelled() => break,
            job = jobs.recv() => match job {
                Some(value) => total += value,
                None => break,
            },
        }
    }
    total
}

#[tokio::main]
async fn main() {
    let (sender, jobs) = mpsc::channel(8);
    let worker = tokio::spawn(drain(jobs, CancellationToken::new()));
    for value in [1, 2, 3] {
        sender.send(value).await.expect("the worker is running");
    }
    drop(sender);
    assert_eq!(worker.await.expect("the worker does not panic"), 6);
}
```

To keep a non-cancellation-safe operation running across loop iterations, create its future once before the
loop, pin it with `std::pin::pin!`, and select on `&mut` that future, so each iteration polls the same future
instead of recreating it. Leave the loop from that branch, or guard it with `, if !done`, because polling a
future again after it completed panics. When the operation must finish no matter what, move it into its own
task and select on that task's handle.

## Channels and Time

- **`mpsc::channel(capacity)`** is the default for work queues, because a full channel makes senders wait and
  so limits memory. Use `unbounded_channel` only when the producer's rate is bounded by something else.
- **`oneshot`** carries one reply, such as the answer to a request sent over `mpsc`.
- **`watch`** holds the latest value, such as configuration or state, and receivers see only the newest.
- **`broadcast`** delivers every message to every receiver. A receiver that falls behind by more than the
  capacity gets `RecvError::Lagged` with the number of messages it missed, and must handle it.

A channel closes, and `recv` returns `None`, only after every `Sender` is dropped. A sender stored in a struct
that the receiving task also owns keeps the channel open forever, so the loop never ends.

Wrap an operation in `tokio::time::timeout(duration, future)` to bound it; the future is cancelled when the
time runs out. The first tick of `tokio::time::interval` completes immediately, and missed ticks fire in a burst
by default to catch up. Call
`set_missed_tick_behavior(MissedTickBehavior::Delay)` when catching up would overload the work.

## Graceful Shutdown

Shut a service down in this order, so in-flight work finishes and nothing waits forever:

1. Wait for the trigger: `tokio::signal::ctrl_c()`, or SIGTERM through `tokio::signal::unix`. The
   `rust-unix-processes` skill covers signals and forwarding them to child processes.
2. Cancel a shared `tokio_util::sync::CancellationToken`. Give each task a clone, or a `child_token` for a
   subtree, and have every task loop select on `token.cancelled()`.
3. Close the `TaskTracker`, then wait for it inside `tokio::time::timeout`, so one stuck task cannot hang the
   exit.
4. When the timeout expires, report which work did not stop, and exit. Returning from `main` drops the
   runtime, which drops the remaining tasks when they next yield but waits for any that never do; use
   `shutdown_timeout` from The Runtime section when that wait must be bounded.

Give tasks time to clean up before forcing them: calling `abort` right after `cancel` removes the window in
which they flush, reply, or release resources.

```rust,run
use std::time::Duration;
use tokio_util::sync::CancellationToken;
use tokio_util::task::TaskTracker;

async fn worker(id: u32, token: CancellationToken) {
    let mut tick = tokio::time::interval(Duration::from_millis(5));
    loop {
        tokio::select! {
            () = token.cancelled() => {
                println!("worker {id} flushed and stopped");
                return;
            }
            _ = tick.tick() => {}
        }
    }
}

#[tokio::main]
async fn main() {
    let token = CancellationToken::new();
    let tracker = TaskTracker::new();
    for id in 0..3 {
        tracker.spawn(worker(id, token.child_token()));
    }

    // A real service waits for ctrl_c or SIGTERM here.
    tokio::time::sleep(Duration::from_millis(20)).await;

    token.cancel();
    tracker.close();
    if tokio::time::timeout(Duration::from_secs(5), tracker.wait()).await.is_err() {
        eprintln!("some workers did not stop within 5 seconds");
    }
}
```

## Copying Between Streams

Copy a proxied connection in both directions with `tokio::io::copy_bidirectional`. When one side reaches end of
file, it shuts down the other side's writer and keeps copying the remaining direction. Two `tokio::io::copy`
calls inside `select!` instead drop the second direction at the first end of file and cut off half-closed
connections.

A `BufWriter` discards its buffer when dropped. Call `flush`, or `shutdown` on a connection, before dropping
it, so the last bytes are sent.

## Async Functions in Traits

A trait may declare `async fn` directly (Rust 1.75). Two limits apply:

- The trait is not dyn-compatible, so `Box<dyn Trait>` does not compile.
- A caller generic over the trait cannot require the returned future to be `Send`, so it cannot
  `tokio::spawn` the call.

When implementations are spawned, declare the method as returning `impl Future<Output = T> + Send` in the trait.
Implementations may still write `async fn`, and the compiler checks that each one is `Send`. When you need
`dyn Trait`, return `Pin<Box<dyn Future<Output = T> + Send + '_>>` from the trait method, or use the
`async-trait` crate, which generates that form.

```rust
use std::future::Future;

pub trait Backend {
    fn status(&self) -> impl Future<Output = String> + Send;
}

pub struct Local;

impl Backend for Local {
    async fn status(&self) -> String {
        "ready".to_owned()
    }
}

pub fn spawn_status<B>(backend: B) -> tokio::task::JoinHandle<String>
where
    B: Backend + Send + 'static,
{
    tokio::spawn(async move { backend.status().await })
}
```

An `AsyncFn` bound, from async closures (Rust 1.85), cannot require the closure's future to be `Send` either.
When the future is spawned, take `F: Fn() -> Fut` with `Fut: Future<Output = T> + Send + 'static`.

## Tracing Across Tasks

A `tracing` span does not follow a future into `tokio::spawn`. Attach it with
`tokio::spawn(future.instrument(tracing::Span::current()))`, using `tracing::Instrument`, or mark the async
function `#[tracing::instrument]`, so the task's events keep their context.
