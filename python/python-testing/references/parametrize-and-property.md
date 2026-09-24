# Parametrize and Property-Based Testing

Read this when one behavior needs many inputs, or when the interesting inputs are the ones nobody thought of.

`SKILL.md` shows the basic `parametrize` form.

## Readable Case Names

Without help, pytest generates ids from the values, which is unreadable once the values are objects or long
strings. Name the cases:

```python
@pytest.mark.parametrize(
    ("payload", "error"),
    [
        pytest.param({}, "missing name", id="empty"),
        pytest.param({"name": ""}, "empty name", id="blank-name"),
        pytest.param({"name": "x" * 300}, "too long", id="over-length"),
    ],
)
def test_rejects_bad_payloads(payload, error):
    with pytest.raises(ValidationError, match=error):
        validate(payload)
```

`pytest -k over-length` then selects exactly that case, which is what makes ids worth writing.

## Expected Failures Inside a Set

`pytest.param` also carries marks, so one known-bad case does not need its own test:

```python
        pytest.param("١٢٣", 123, id="arabic-digits", marks=pytest.mark.xfail(reason="issue #412")),
```

Prefer `xfail` with a reason over deleting or commenting out the case. An `xfail` that starts passing is
reported as `XPASS`, which tells you the bug is fixed.

## Stacking

Stacked `parametrize` decorators multiply, producing the cartesian product:

```python
@pytest.mark.parametrize("scheme", ["http", "https"])
@pytest.mark.parametrize("port", [80, 8080])
def test_builds_a_url(scheme, port):        # runs 4 times
    ...
```

Useful for genuinely independent dimensions. Two stacked lists of five are twenty-five tests, so check that
the combinations mean something before stacking.

## When Not to Parametrize

If the cases need different assertions, different setup, or different mocks, they are different tests. Forcing
them into one parametrized function produces a body full of `if expected is None:` branches, which is harder
to read than the tests it replaced.

## Property-Based Testing with Hypothesis

Parametrize checks the inputs you thought of. [Hypothesis](https://hypothesis.readthedocs.io/) generates
inputs you did not, and shrinks any failure to a minimal reproducing case.

```python
from hypothesis import given, strategies as st

@given(st.integers())
def test_roundtrips_through_json(value):
    assert decode(encode(value)) == value
```

It fits where a property holds for all valid inputs:

| Property     | Example                                                           |
| ------------ | ----------------------------------------------------------------- |
| Round trip   | `decode(encode(x)) == x`                                          |
| Invariant    | Sorting preserves length and multiset                             |
| Idempotence  | `normalize(normalize(x)) == normalize(x)`                         |
| Agreement    | A fast implementation matches an obvious slow one                 |
| Never raises | A parser returns an error value rather than crashing on any bytes |

It fits badly where the expected output is a lookup rather than a rule. Do not reimplement the function under
test inside the test to compute the expectation; that only tests that you wrote the same bug twice.

### Composing Inputs

```python
@st.composite
def orders(draw):
    quantity = draw(st.integers(min_value=1, max_value=1000))
    price = draw(st.decimals(min_value=0, max_value=10_000, places=2))
    return Order(quantity=quantity, price=price)

@given(orders())
def test_total_is_never_negative(order):
    assert order.total() >= 0
```

### Reproducing a Failure

Hypothesis prints a `@reproduce_failure` decorator and stores failing examples in `.hypothesis/`. Pin the case
permanently once it is understood:

```python
@given(st.integers())
@example(0)              # the regression this test was written for
def test_handles_zero(value):
    ...
```

`@example` cases always run, so the specific bug stays covered even if the generator stops producing it.

### Practical Notes

- Hypothesis runs each test many times. Keep the body fast and avoid I/O inside it.
- A `@given` test cannot take a function-scoped fixture that must be fresh per example; pytest creates it
  once for the whole test. Build per-example state inside the test.
- `settings(deadline=None)` silences flaky timing failures on a slow machine, but consider whether the
  variance is telling you something first.
