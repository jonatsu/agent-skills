# Fixtures and Test Doubles

Read this when a test needs setup, cleanup, a temporary resource, or a stand-in for something real.

## Fixture Cleanup

`yield` splits a fixture into setup and teardown. The teardown runs even when the test fails.

```python
@pytest.fixture
def server():
    process = start_server()
    yield process
    process.terminate()
```

`return` is fine when there is nothing to undo. Reach for `yield` the moment a resource has to be released,
and prefer a context manager inside the fixture when the resource already provides one:

```python
@pytest.fixture
def connection(database_url):
    with connect(database_url) as conn:
        yield conn
```

## Factory Fixtures

When each test needs its own variant, return a callable rather than a value:

```python
@pytest.fixture
def make_order():
    def _make(quantity=1, **overrides):
        return Order(quantity=quantity, **overrides)
    return _make

def test_rejects_zero(make_order):
    with pytest.raises(ValueError):
        make_order(quantity=0)
```

This beats a pile of near-identical fixtures, and it keeps each test's relevant difference visible in the
test rather than hidden in a fixture name.

## Parametrized Fixtures

A fixture can multiply the tests that use it:

```python
@pytest.fixture(params=["sqlite", "postgres"])
def backend(request):
    return request.param
```

Every test taking `backend` now runs twice. Powerful and easy to overdo: this multiplies the whole subtree, so
a parametrized session fixture can silently double an entire suite's runtime.

## conftest.py

Fixtures in `conftest.py` are available to every test at or below that directory, with no import. Put a
fixture at the narrowest level that serves its users: a fixture only two files need does not belong at the
root.

`conftest.py` is also where plugin hooks and collection customization live. Keep it small; it is loaded for
every run, and a heavy import at its top slows down even a single-test invocation.

## Built-in Fixtures

| Fixture            | Gives you                                                       |
| ------------------ | --------------------------------------------------------------- |
| `tmp_path`         | A `pathlib.Path` to a fresh directory, per test                 |
| `tmp_path_factory` | The same, session-scoped, for shared expensive artifacts        |
| `monkeypatch`      | Attribute, dict, and environment patching, undone automatically |
| `capsys`, `capfd`  | Captured stdout and stderr                                      |
| `caplog`           | Captured log records, with level control                        |
| `recwarn`          | Captured warnings                                               |
| `request`          | The test's own context: params, node, markers                   |

Use these before writing your own. `tmp_path` in particular removes the need for a filesystem double in most
tests.

```python
def test_writes_a_report(tmp_path):
    destination = tmp_path / "report.json"
    write_report(destination, data)
    assert json.loads(destination.read_text())["rows"] == 3
```

## monkeypatch

`monkeypatch` reverses everything it did when the test ends, which is what makes it safer than assigning
directly.

```python
def test_reads_the_token_from_the_environment(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "t-123")
    assert load_config().token == "t-123"

def test_missing_token_is_an_error(monkeypatch):
    monkeypatch.delenv("API_TOKEN", raising=False)
    with pytest.raises(ConfigError, match="API_TOKEN"):
        load_config()
```

`monkeypatch.chdir`, `monkeypatch.setattr` and `monkeypatch.setitem` cover the other common cases. Patch where
the name is **used**, not where it is defined: a module that did `from x import get` holds its own reference,
so patching `x.get` does not affect it.

## unittest.mock

Reach for a mock when the assertion is about the interaction itself: that a call happened, with which
arguments, how many times.

```python
def test_retries_twice_then_succeeds():
    client = Mock()
    client.request.side_effect = [ConnectionError, ConnectionError, {"status": "ok"}]

    assert Service(client, max_retries=3).fetch() == {"status": "ok"}
    assert client.request.call_count == 3

def test_does_not_retry_a_permanent_error():
    client = Mock()
    client.request.side_effect = ValueError("bad input")

    with pytest.raises(ValueError):
        Service(client, max_retries=3).fetch()
    assert client.request.call_count == 1
```

`side_effect` taking a list is the retry-testing tool: each call consumes the next item, and an exception
class or instance is raised rather than returned.

**Use `autospec=True` when patching.** Without it, a mock accepts any call signature, so a test keeps passing
after the real function's parameters change. That is the failure mode that makes people distrust mocks.

```python
with patch("myapp.services.send_email", autospec=True) as send:
    ...
    send.assert_called_once_with(to="a@example.test", subject="Hi")
```

For async doubles see [async-testing.md](async-testing.md).

## Controlling Time

Injecting the clock is better than patching it: a function taking `now: datetime` is trivially testable and
has no global state.

When the clock is not injectable, [freezegun](https://github.com/spulec/freezegun) freezes it:

```python
from freezegun import freeze_time

@freeze_time("2026-01-15 10:00:00")
def test_token_expiry():
    assert create_token(expires_in_seconds=3600).expires_at == datetime(2026, 1, 15, 11, 0, 0)

def test_expires_after_the_window():
    with freeze_time("2026-01-15 10:00:00") as clock:
        token = create_token(expires_in_seconds=3600)
        clock.move_to("2026-01-15 11:00:01")
        assert token.is_expired()
```

[time-machine](https://github.com/adamchainz/time-machine) is a faster alternative with a similar interface.
Neither advances an event loop's timers, so see the note in [async-testing.md](async-testing.md) before using
one in an async test.

## Database and Other Real Dependencies

When a test uses a real dependency, give each test an isolated slice of it and roll back rather than
recreating:

```python
@pytest.fixture(scope="session")
def engine(database_url):
    engine = create_engine(database_url)
    create_schema(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    yield Session(bind=connection)
    transaction.rollback()
    connection.close()
```

Schema creation is session-scoped because it is expensive; the per-test transaction is function-scoped and
rolled back, so tests cannot see each other's writes and order does not matter.

[pytest-docker](https://github.com/avast/pytest-docker) and
[testcontainers-python](https://github.com/testcontainers/testcontainers-python) start a real service for the
session when one is needed. Both cost startup time, so gate them behind a marker the default run excludes.

**Substituting SQLite for the real database is not a smaller test, it is a different one.** It will not catch
dialect-specific SQL, constraint behavior, or concurrency semantics. If the test needs the real engine, use
it and classify the test honestly.
