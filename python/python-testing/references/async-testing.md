# Testing Async Code

Read this before writing the first async test in a project, and when an async test behaves in a way a sync
test would not.

## First: Does the Project Have a Plugin

pytest cannot run a coroutine test on its own. `pytest --version` lists installed plugins; look for
`pytest-asyncio`, `anyio`, `pytest-trio`, or `pytest-tornasync`.

**Without one, the failure is silent on pytest 8 and earlier.** Measured 2026-09-04 on a file whose only test
was `async def test_x(): assert False`:

| pytest | Result                                   | Exit |
| ------ | ---------------------------------------- | ---- |
| 7.4.4  | `1 skipped, 1 warning`                   | 0    |
| 8.3.5  | `1 skipped, 1 warning`                   | 0    |
| 9.1.1  | `1 failed`, naming the candidate plugins | 1    |

A whole async suite can therefore report success while never executing. `pytest -q -rs` lists skips and their
reasons; run it once when adopting async tests, and in CI if the project is on pytest 8 or earlier.

## Choosing the Plugin

| Plugin         | Choose when                                                             |
| -------------- | ----------------------------------------------------------------------- |
| pytest-asyncio | The code targets asyncio directly                                       |
| anyio          | The code is written against anyio, or must run on both asyncio and Trio |
| pytest-trio    | The code targets Trio                                                   |

Do not add a second one. Two async plugins collecting the same test is a source of confusing failures. Use
what the project has.

### pytest-asyncio

Two modes, and the mode decides whether a marker is required.

```toml
[tool.pytest.ini_options]
asyncio_mode = "strict"   # default: every async test needs @pytest.mark.asyncio
# asyncio_mode = "auto"   # every async test is collected automatically
```

```python
@pytest.mark.asyncio
async def test_fetches_a_user(client):
    assert (await client.get_user("1")).name == "Ada"
```

`strict` is the safer default: an async test that was never marked shows up as skipped rather than passing
vacuously. `auto` suits a project whose tests are overwhelmingly async.

An async fixture needs the plugin's fixture decorator, and its loop scope must not be narrower than the tests
using it:

```python
@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient() as c:
        yield c
```

### anyio

anyio's plugin needs a backend parameter, usually supplied by a fixture:

```python
@pytest.fixture
def anyio_backend():
    return "asyncio"          # or a tuple to run every test on both backends

@pytest.mark.anyio
async def test_sleeps():
    await anyio.sleep(0)
```

Returning a tuple of backends runs each test once per backend, which is the point of choosing anyio.

## Faking an Async Dependency

`unittest.mock.AsyncMock` is in the standard library from Python 3.8. Reach for it before any third-party
double.

```python
from unittest.mock import AsyncMock

async def test_uses_the_client():
    client = AsyncMock()
    client.get.return_value = {"ok": True}

    result = await fetch(client, "/users")

    assert result == {"ok": True}
    client.get.assert_awaited_once_with("/users")
```

`assert_awaited_once_with` is the async counterpart of `assert_called_once_with`, and it is the stronger
assertion: a coroutine that was created but never awaited counts as called and not as awaited.

Two behaviors worth knowing:

- **`MagicMock` autospecs async methods.** Patching an object with `unittest.mock.patch` and `autospec=True`
  gives `AsyncMock` for its coroutine functions and `MagicMock` for the rest, so a plain patch usually does
  the right thing.
- **A bare `MagicMock` returns a `MagicMock`, not an awaitable.** Awaiting it raises `TypeError`. That error
  means the double is the wrong kind, not that the code is wrong.

Raising from an async double is the same as the sync form:

```python
client.get.side_effect = TimeoutError("upstream timed out")
```

## Faking HTTP

Prefer the transport hook the client library provides; it exercises more real code than patching the method.

| Library | Tool                                                               | What it is                                                              |
| ------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| aiohttp | [aioresponses](https://github.com/pnuckowski/aioresponses)         | Registers URL patterns and canned responses for `aiohttp.ClientSession` |
| httpx   | [RESPX](https://github.com/lundberg/respx)                         | Mock router for httpx, sync and async                                   |
| httpx   | `httpx.MockTransport`                                              | Built in; a function that maps a request to a response                  |
| any     | [pytest-httpserver](https://github.com/csernazs/pytest-httpserver) | A real local HTTP server, for tests that should cross a socket          |

`httpx.MockTransport` needs no dependency at all:

```python
def handler(request):
    return httpx.Response(200, json={"ok": True})

async def test_calls_the_api():
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        assert (await client.get("https://example.test/")).json() == {"ok": True}
```

## Testing Timeouts and Cancellation

These are the paths async code gets wrong, and they are testable without waiting in real time.

```python
async def test_gives_up_after_the_timeout():
    with pytest.raises(TimeoutError):
        async with asyncio.timeout(0.01):
            await never_returns()
```

`asyncio.timeout` is available from Python 3.11. On older versions use `asyncio.wait_for`, and note that
`asyncio.TimeoutError` is an alias of the built-in `TimeoutError` from 3.11, so catching the built-in works on
both.

Cancellation deserves its own test, because the common bug is swallowing it:

```python
async def test_cleans_up_when_cancelled():
    task = asyncio.create_task(worker())
    await asyncio.sleep(0)          # let it start
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert worker_released_its_resources()
```

If that test hangs or reports no exception, the code under test is catching `CancelledError` without
re-raising. `python-async-patterns` covers why that is wrong; this is how to catch it.

**Do not sleep in real time to make an ordering test pass.** A `sleep(0.5)` is a slow test and a flaky one.
Synchronize on the thing itself: an `asyncio.Event`, awaiting the task, or `asyncio.sleep(0)` to yield one
scheduling turn.

## Time, and Why It Is Worse in Async Tests

Freezing the clock with a library like `freezegun` does not advance an event loop's own timers. A test that
freezes time and then awaits something with a timeout can hang. Prefer injecting the timeout as a parameter
and passing a small real value, or use a plugin built for the loop's clock rather than the wall clock.

## Common Failures

| Symptom                                                           | Cause                                                      |
| ----------------------------------------------------------------- | ---------------------------------------------------------- |
| `1 skipped` on an async test                                      | No plugin, or strict mode with no marker                   |
| `TypeError: object MagicMock can't be used in 'await' expression` | Double should be `AsyncMock`                               |
| Passes but asserts nothing                                        | Coroutine created and never awaited; use `assert_awaited*` |
| `RuntimeError: attached to a different loop`                      | Fixture loop scope narrower than the test's                |
| Hangs on cancellation                                             | Code catches `CancelledError` without re-raising           |
| Flaky ordering                                                    | Real `sleep` used as synchronization                       |
