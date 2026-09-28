# Generics, Variance, and Overloads

Read this when a generic signature does not do what you expected, or when the checker rejects a call that
looks correct.

## Variance, and the Rule That Explains Most Rejections

```text
error: Argument 1 has incompatible type "list[Dog]"; expected "list[Animal]"
```

This is correct, not a checker bug. `list` is **invariant**: `list[Dog]` is not a `list[Animal]`, because a
function taking `list[Animal]` is allowed to append a `Cat` to it, which would corrupt the caller's
`list[Dog]`.

The fix is to ask for less. If the function only reads, take a covariant container:

```python
def total_weight(animals: Sequence[Animal]) -> float:      # accepts list[Dog]
    return sum(a.weight for a in animals)
```

| Want                          | Use                                       | Variance         |
| ----------------------------- | ----------------------------------------- | ---------------- |
| Read a sequence               | `Sequence[T]`                             | Covariant        |
| Read any iterable, once       | `Iterable[T]`                             | Covariant        |
| Read a mapping                | `Mapping[K, V]`                           | Covariant in `V` |
| Mutate the caller's container | `list[T]`, `dict[K, V]`, `MutableMapping` | Invariant        |

A parameter typed `Sequence` rather than `list` accepts tuples and any other sequence, documents that the
function does not mutate, and stops the variance error before it happens. Return concrete types
(`list[str]`), accept abstract ones (`Sequence[str]`).

Callables are contravariant in their parameters and covariant in their return: a `Callable[[Animal], Dog]` is
usable where `Callable[[Dog], Animal]` is expected. This is why a handler taking a broader input type is
always safe to pass.

## Declaring Variance Yourself

With PEP 695 (3.12+), the checker infers variance from how the parameter is used. With the older syntax you
declare it:

```python
T_co = TypeVar("T_co", covariant=True)      # only produced
T_contra = TypeVar("T_contra", contravariant=True)   # only consumed

class Producer(Protocol[T_co]):
    def get(self) -> T_co: ...

class Consumer(Protocol[T_contra]):
    def put(self, item: T_contra) -> None: ...
```

A parameter that is both produced and consumed must stay invariant. Declaring a covariant parameter and then
accepting it as an argument is an error the checker will point out.

## Bounds and Constraints

```python
def largest[T: float](values: Sequence[T]) -> T: ...          # bound: T is float or a subtype
def parse[T: (int, str)](raw: str, kind: type[T]) -> T: ...   # constraint: T is exactly int or exactly str
```

A **bound** admits any subtype and keeps the specific type in the result. A **constraint** admits only the
listed types, and the checker solves for one of them exactly: a subclass of `int` resolves to `int`, losing
the subtype.

Bound to a Protocol when the code calls methods:

```python
class Comparable(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...

def minimum[T: Comparable](items: Sequence[T]) -> T: ...
```

## Self

`Self` (3.11+) types a method that returns its own instance, correctly for subclasses:

```python
class Builder:
    def with_timeout(self, seconds: float) -> Self:
        self._timeout = seconds
        return self
```

Annotating that `-> Builder` breaks chaining for any subclass, because the checker forgets the subclass after
the first call.

## Overloads

`@overload` describes a function whose return type depends on its arguments:

```python
@overload
def get(key: str) -> str | None: ...
@overload
def get(key: str, default: str) -> str: ...

def get(key: str, default: str | None = None) -> str | None:
    return _store.get(key, default)
```

Callers now see `str` when they pass a default and `str | None` when they do not. Only the final
implementation runs; the overloads are signatures only.

Order matters: the checker takes the first matching overload, so put the more specific signatures first.

Use a union return when callers can handle every member of it; three overloads to avoid one `| None` is a
cost with no benefit.

## ParamSpec: Decorators That Preserve Signatures

A decorator typed with `Callable[..., Any]` erases the signature of everything it wraps. `ParamSpec` keeps it:

```python
def logged[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        log.info("calling %s", func.__name__)
        return func(*args, **kwargs)
    return wrapper
```

Callers of a decorated function keep full argument checking. Without `ParamSpec`, every decorated function
silently accepts anything, which is one of the larger sources of un-typed code in a typed project.

`Concatenate` handles a decorator that adds or removes a leading argument:

```python
def with_connection[**P, R](
    func: Callable[Concatenate[Connection, P], R],
) -> Callable[P, R]: ...
```

## TypedDict and NamedTuple

For a dict with a known shape, especially a JSON payload:

```python
class UserPayload(TypedDict):
    id: str
    name: str
    email: NotRequired[str]
```

`NotRequired` marks optional keys; `total=False` makes every key optional. A `TypedDict` is checked
structurally at type-check time only; it is a plain `dict` at runtime and validates nothing, so external data
still needs validating at the boundary.

`TypedDict` is for data that genuinely is a dict. Give a thing with behavior or invariants a class.

## Type Aliases

```python
type UserId = str                       # 3.12+
type Handler[T] = Callable[[T], None]
```

Aliases earn their place when the underlying type is long, repeated, or meaningless on its own.
`type UserId = str` documents intent but does not enforce it: a plain `str` is still accepted. Use `NewType`
when you want the checker to keep them apart:

```python
UserId = NewType("UserId", str)
```

## Generic Classes That Hold State

```python
class Repository[T]:
    def __init__(self, model: type[T]) -> None:
        self._model = model
        self._items: dict[str, T] = {}

    def add(self, key: str, item: T) -> None:
        self._items[key] = item

    def get(self, key: str) -> T | None:
        return self._items.get(key)
```

`type[T]` is the annotation for a class object rather than an instance, which is what makes the constructor
argument carry the type parameter.
