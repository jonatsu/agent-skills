---
name: python-typing
description: Add and fix Python type annotations, and run a type checker. Use when annotating existing code, writing generics or Protocols, narrowing a union the checker rejects, deciding where Any is acceptable, configuring mypy or pyright, or making strict mode pass on a codebase that does not yet.
license: MIT
compatibility: Examples target Python 3.12+ for PEP 695 generic syntax, with the older TypeVar form shown where it differs. Verified against mypy 2.3.1.
metadata:
  author: Joonas Onatsu
---

# Python Typing

Annotations that a type checker can act on, and the checker itself. This skill is for the cases where a
capable writer stalls: variance, Protocols, narrowing the checker refuses to follow, and getting an existing
codebase to pass strict mode.

Annotating an ordinary function signature needs no skill. Read this when the checker disagrees with you.

## Read the Project First

- **Which checker.** mypy, pyright, ty, or none. Look for `[tool.mypy]`, `mypy.ini`, `[tool.pyright]`,
  `pyrightconfig.json`, `[tool.ty]`, and the CI workflow.
- **How strict, and where.** A project often has a strict core and lenient legacy modules. Per-module
  overrides matter more than the global setting.
- **How it runs.** A direct command, a task recipe, a CI step, a hook, or several. Match what is there.
- **Which Python version it targets.** That decides whether PEP 695 syntax, `Self`, and `override` are
  available.

Never tighten a project's checker configuration as a side effect of another task.

## Generics

Python 3.12 (PEP 695) declares type parameters inline. No `TypeVar` import, and the scope is explicit:

```python
class Box[T]:
    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value

def first[T](items: Sequence[T]) -> T | None:
    return items[0] if items else None
```

Verified with mypy 2.3.1 under `--strict`: `Box(1).get()` reveals `int`, and `first(["a"])` reveals
`str | None`.

Before 3.12, the same thing with an explicit `TypeVar`:

```python
T = TypeVar("T")

class Box(Generic[T]):
    ...
```

Both forms are correct; use whichever the project's floor allows. Do not mix them in one file.

**Bound a type parameter when the code calls methods on it**, or the checker has to assume `object`:

```python
def largest[T: (int, float)](items: Sequence[T]) -> T: ...   # constrained to these
def sorted_by_key[T: Comparable](items: Sequence[T]) -> list[T]: ...   # upper bound
```

Variance, `ParamSpec`, `TypeVarTuple` and overloads are in [generics.md](references/generics.md).

## Protocols Over Inheritance

A `Protocol` types what an object can do without requiring it to inherit anything:

```python
class Reader(Protocol):
    def read(self) -> bytes: ...

def load(source: Reader) -> Config:
    return parse(source.read())
```

Any object with a matching `read` satisfies this, including `io.BytesIO`, an open file, and a test double.
That is the point: the caller is not forced to import your base class.

| Use        | When                                                                               |
| ---------- | ---------------------------------------------------------------------------------- |
| `Protocol` | You consume something and only care about its shape                                |
| ABC        | You provide a base class with shared implementation, and want an explicit registry |

Protocols are the right default for a function parameter. Reach for an ABC when there is behavior to inherit.

Add `@runtime_checkable` only if you need `isinstance`, and know that it checks method names only, not
signatures.

## Narrowing

The checker follows narrowing that it can see:

```python
def process(user_id: str) -> UserData:
    user = find_user(user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return UserData(name=user.name)      # user is User here, not User | None
```

`isinstance`, `is None`, `assert`, and a truthiness check all narrow. What does not narrow is a check the
checker cannot connect to the value: a helper returning `bool`, a lookup in a dict, or a flag set earlier.

For a helper, say what it proves with `TypeIs` (3.13+) or `TypeGuard`:

```python
def is_str_list(value: list[object]) -> TypeIs[list[str]]:
    return all(isinstance(item, str) for item in value)
```

`TypeIs` narrows in both branches and is the better default; `TypeGuard` narrows only the positive branch.

## Exhaustiveness

`assert_never` turns a missing case into a checker error rather than a runtime surprise:

```python
def describe(color: Color) -> str:
    match color:
        case Color.RED:
            return "red"
        case Color.BLUE:
            return "blue"
        case _:
            assert_never(color)
```

Verified with mypy 2.3.1: adding `Color.GREEN` to the enum without adding a branch produces
`Argument 1 to "assert_never" has incompatible type "Literal[Color.GREEN]"; expected "Never"`. It names the
case you forgot, which is why this beats a `raise ValueError` default.

Use it wherever an enum or a discriminated union is matched and every case must be handled.

## Any

`Any` disables checking for everything it touches, and it spreads: a function returning `Any` silently
un-types its callers.

Legitimate uses:

- Genuinely dynamic data before validation, such as a freshly parsed JSON payload.
- An untyped third-party library at the boundary where you call it.
- A deliberate escape hatch with a comment saying why.

Prefer the narrower option where one exists. `object` when you accept anything but will check before using it.
`dict[str, Any]` rather than bare `Any` for a payload whose shape is partly known. A `TypedDict` or a
validation library once the shape is known at all.

Confine `Any` to the boundary. Convert to a real type immediately, and everything inward stays checked.

## Running the Checker

```bash
mypy src/
pyright src/
```

A useful starting configuration, and the per-module ladder for a codebase that does not pass yet, are in
[checker-setup.md](references/checker-setup.md). Read it before turning on `strict` anywhere that has
existing code.

Two habits worth having:

- **`reveal_type(x)`** makes the checker print what it thinks a value is. It is the fastest way to find where
  an inference went wrong, and it needs no import.
- **Never add a bare `# type: ignore`.** Use `# type: ignore[error-code]` so the suppression stops working
  when the error changes, and enable `warn_unused_ignores` so stale ones get reported.

## Common Complaints

| Message                                                               | Usually means                                                       |
| --------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `Item "None" of "X \| None" has no attribute`                         | Narrow the optional first, or the check is invisible to the checker |
| `Incompatible types in assignment` on an empty container              | Annotate it: `items: list[str] = []`                                |
| `Returning Any from function declared to return X`                    | An untyped dependency is leaking; convert at the boundary           |
| `Argument has incompatible type "list[Dog]"; expected "list[Animal]"` | `list` is invariant; take `Sequence[Animal]`                        |
| `Cannot determine type of "x"`                                        | Circular inference; annotate the attribute explicitly               |
| `Module has no attribute` on a real attribute                         | Missing stubs; install the `types-*` package                        |
| `Need type annotation for "x"`                                        | Inference had nothing to work from                                  |

Variance, the `list` versus `Sequence` rule, and the rest of the container guidance are in
[generics.md](references/generics.md).

## Before Calling Typing Work Done

1. Does the checker pass at the project's configured strictness, not a lower one you chose?
2. Is every new `# type: ignore` code-specific and justified?
3. Did any signature change from an interface a caller depends on?
4. Is `Any` confined to a boundary, rather than propagating inward?
5. Is a mutable container in a parameter position deliberate, rather than an invariance mistake?
