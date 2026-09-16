---
name: python-error-handling
description: Design how Python code validates input and fails. Use when validating arguments or external data at a boundary, loading configuration or handling secrets at startup, designing an exception hierarchy, chaining or re-raising exceptions, handling partial failure in a batch, or writing an error message someone has to act on.
license: MIT
compatibility: ExceptionGroup and except* examples require Python 3.11+. Everything else works on 3.9+.
metadata:
  author: Joonas Onatsu
---

# Python Error Handling

How code rejects bad input, reports failure, and survives partial failure. The shape of the boundary, not the
mechanics of `try`.

Type annotations that make absence explicit are `python-typing`. Asserting on failures in tests is
`python-testing`.

## Respect Project Conventions

Use these defaults for new projects. In established projects, follow declared conventions and consistent local practice,
including for new files and modules. Check both before filling an undecided choice.

Do not recommend changes merely because these defaults differ. Recommend corrections supported by incorrect behavior,
security vulnerabilities, or concrete reliability or maintenance harm. Explain the evidence, consequence, and smallest
remedy. A different tool, layout, style, or supported syntax is not itself a defect.

Apply fixes within the authorized task; otherwise report the recommendation without changing the project.
An explicit modernization or conventions review permits broader recommendations.

## Validate at the Boundary, Then Trust

Check external input once, where it enters, and convert it to something the rest of the program can rely on.
Code inside the boundary should not re-check.

```python
def export(rows: list[dict], format_name: str) -> bytes:
    output_format = OutputFormat.parse(format_name)   # fails here or not at all
    return _render(rows, output_format)
```

A boundary is anywhere data arrives from outside your control: a request handler, a CLI argument, a config
file, a queue message, a third-party response, a database row with a nullable column.

**Convert to a domain type at the boundary rather than passing strings inward.** A function taking
`OutputFormat` cannot receive `"jsno"`; a function taking `str` can, and will, from somewhere far away.

```python
class OutputFormat(Enum):
    JSON = "json"
    CSV = "csv"

    @classmethod
    def parse(cls, raw: str) -> "OutputFormat":
        try:
            return cls(raw.lower())
        except ValueError as exc:
            valid = ", ".join(f.value for f in cls)
            raise ValueError(f"unknown format {raw!r}; expected one of: {valid}") from exc
```

Note the `from exc`, and see the chaining section below for why.

## Configuration Is a Boundary Too

Configuration arrives from outside the program, so it gets the same treatment as any other external input:
validated once, at the edge, and converted to something the rest of the program can trust.

```python
class Settings(BaseSettings):
    database_url: str
    api_token: SecretStr
    request_timeout: float = 5.0
```

Load it once at startup and pass it down. Reading `os.environ` deep in the call tree hides a dependency the
caller cannot see, cannot substitute in a test, and cannot discover before the code path runs.

Fail at startup rather than at first use. A settings model validated on construction gives that for free: a
missing variable becomes a startup error naming the field, instead of a `KeyError` an hour into a batch job.

Type a secret as `SecretStr` so it is redacted from logs, reprs, and tracebacks, and call `.get_secret_value()`
only at the point of use. An unredacted token reaches a log the first time an exception renders the settings
object, which is exactly when the traceback gets pasted somewhere.

Keep secrets and environment-specific values out of the repository and out of defaults. Ship a `.env.example`
listing the names with no values, so the required set is discoverable without the values leaking.

## Report Every Problem, Not the First

Validation that stops at the first failure makes the caller fix one thing, resubmit, and discover the next.
Collect and report together:

```python
def validate_order(payload: Mapping[str, Any]) -> list[str]:
    problems = []
    if not payload.get("id"):
        problems.append("'id' is required")
    quantity = payload.get("quantity")
    if not isinstance(quantity, int) or quantity <= 0:
        problems.append(f"'quantity' must be a positive integer, got {quantity!r}")
    return problems
```

This applies to a form, a config file, and a CLI invocation. It does not apply where continuing is unsafe:
stop immediately when a later check depends on the value that just failed, or when proceeding would touch
something it should not.

For complex external schemas, prefer Pydantic v2 when the project has no established validation library.
Use `pydantic-settings` for environment settings when needed. Verify coercion, unknown-field behavior, and error paths
against the boundary's contract. Simple scalar checks and ordinary mappings do not require a model or new dependency.
Keep internal value-type choices in `python-style` and typing-only interfaces in `python-typing`.

## Choose the Exception

Use a built-in when one fits. A caller already knows what `ValueError` means.

| Situation                                    | Raise                           |
| -------------------------------------------- | ------------------------------- |
| A value is the right type but unusable       | `ValueError`                    |
| A value is the wrong type                    | `TypeError`                     |
| A required key or item is absent             | `KeyError`, `IndexError`        |
| An operation is invalid in the current state | `RuntimeError`                  |
| Something is not implemented for this input  | `NotImplementedError`           |
| A file, permission, or network problem       | The relevant `OSError` subclass |

Define your own when callers need to catch **your** failure specifically, without catching an unrelated
`ValueError` from a library three frames down. Give the package one base so a caller can opt into all of it:

```python
class BillingError(Exception):
    """Base for every error this package raises deliberately."""

class PaymentDeclined(BillingError):
    def __init__(self, transaction_id: str, reason: str) -> None:
        super().__init__(f"payment {transaction_id} declined: {reason}")
        self.transaction_id = transaction_id
        self.reason = reason
```

**Carry the data as attributes, not only in the message.** A caller that has to parse your message string to
find the transaction id is coupled to your wording.

Do not build a deep hierarchy in advance. Two levels — a package base and the specific errors — covers almost
everything; add depth when a caller genuinely needs to catch a middle layer.

## Chaining Is Automatic, and `from` Still Matters

Measured on CPython 3.13.15:

| Form                          | `__cause__`  | `__context__` | Traceback says                                             |
| ----------------------------- | ------------ | ------------- | ---------------------------------------------------------- |
| `raise New()` inside `except` | `None`       | The original  | "During handling of the above exception, another occurred" |
| `raise New() from exc`        | The original | The original  | "The above exception was the direct cause"                 |
| `raise New() from None`       | `None`       | The original  | Nothing about the original                                 |

So the original is **never lost** by omitting `from`; Python records it as `__context__` either way. What
`from exc` changes is the claim: it says this failure was caused by that one, rather than merely happening
while handling it. Use it when translating an exception, which is the case in almost every boundary wrapper.

`from None` hides the original from the traceback. It is right when the internal error is noise the caller
cannot act on — a `KeyError` from your own lookup table becoming a clean `ConfigError` — and wrong whenever a
debugger would want the detail.

**Never swallow silently.**

```python
try:
    value = parse(raw)
except ValueError:
    pass          # the program now continues with `value` unbound or stale
```

If a failure really is expected and ignorable, say so with `contextlib.suppress`, which is greppable and
scoped:

```python
with suppress(FileNotFoundError):
    cache_path.unlink()
```

## Catch Narrowly

`except Exception` around a block catches failures you did not think about, including bugs. Catch the specific
type, and keep the `try` body to the statement that can actually fail.

A broad catch is legitimate at exactly two places: a top-level handler that logs and exits non-zero, and a
worker loop that must survive one bad item. Both should log the exception with its traceback, not just its
message.

**`except Exception` does not catch `KeyboardInterrupt`, `SystemExit`, or `asyncio.CancelledError`**, because
those derive from `BaseException`. That is deliberate — never widen to `except BaseException` to "be safe", or
you will catch shutdown signals and hang.

## Partial Failure

When processing many items, one bad item should not lose the other results. Separate the outcomes:

```python
class BatchResult(NamedTuple):
    succeeded: list[Item]
    failed: list[tuple[Item, Exception]]

def process_all(items: Sequence[Item]) -> BatchResult:
    succeeded, failed = [], []
    for item in items:
        try:
            succeeded.append(process(item))
        except ProcessingError as exc:
            failed.append((item, exc))
    return BatchResult(succeeded=succeeded, failed=failed)
```

Return the failures; do not log and drop them. The caller decides whether a 3% failure rate is acceptable, and
it cannot decide from a log line.

Then make the caller confront it: a result type whose failures are easy to ignore will be ignored. Raising
when `failed` is non-empty, unless the caller passed something like `partial_ok=True`, is often the safer
default.

From Python 3.11, `ExceptionGroup` reports several failures as one exception, and `except*` handles them by
type:

```python
def process_all_strict(items: Sequence[Item]) -> list[Item]:
    result = process_all(items)
    if result.failed:
        raise ExceptionGroup("batch failed", [exc for _, exc in result.failed])
    return result.succeeded
```

Verified on 3.13.15: `except* ValueError` receives only the `ValueError` members of the group, and a separate
`except* KeyError` receives only the `KeyError` members. Note that a plain `except ValueError` does **not**
match a group containing one.

## Write the Message for the Person Who Reads It

A good message names what failed, what was received, and what was expected.

```python
raise ValueError(f"'page_size' must be between 1 and 100, got {page_size}")
raise ConfigError(f"config error in {path}: missing required key 'database.url'")
```

Include the offending value with `!r`, so `""` and `" "` are distinguishable. Include the identifier a reader
can search for: a path, a key, an id. Start the message with a stable literal prefix so a message copied out
of a log can be grepped back to its raise site — do not build the identifying part by interpolation.

Do not put remediation in the exception when the caller is code. Do put it in the message when the caller is a
person at a terminal.

## Before Calling Error Handling Done

1. Is every external input validated once, at the boundary, and converted to a domain type?
2. Does each `except` catch the narrowest type that can actually occur there?
3. Does every translation chain with `from`, or suppress with `from None` deliberately?
4. Does any handler swallow an exception without logging, re-raising, or `suppress`?
5. In batch work, are failures returned or raised rather than logged and dropped?
6. Does each message name the value, the expectation, and something searchable?
