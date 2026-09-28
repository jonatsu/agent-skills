---
name: python-typing
description: Resolve Python typing problems and run a type checker. Use when the checker rejects code that looks correct, writing generics or Protocols, narrowing a union it will not follow, deciding where Any is acceptable, configuring mypy, pyright or basedpyright, fixing a language server that misses imports or references, or making strict mode pass on a codebase that does not yet.
license: MIT
compatibility: Examples target Python 3.12+ for PEP 695 generic syntax, with the older TypeVar form shown where it differs. Verified against mypy 2.3.1; import roots verified against basedpyright 1.40.1.
metadata:
  author: Joonas Onatsu
---

# Python Typing

This skill covers the cases where a capable writer stalls: variance, Protocols, narrowing the checker refuses to
follow, import roots the checker cannot see, and getting an existing codebase to pass strict mode. Ordinary
signature defaults and value types live in `python-style`, runtime validation of external data in
`python-error-handling`, and wiring the checker into hooks and CI in `python-project-management`.

## Respect Project Conventions

Use these defaults for new projects. In established projects, follow declared conventions and consistent local practice,
including for new files and modules. Check both before filling an undecided choice.

Do not recommend changes merely because these defaults differ. Recommend corrections supported by incorrect behavior,
security vulnerabilities, or concrete reliability or maintenance harm. Explain the evidence, consequence, and smallest
remedy. A different tool, layout, style, or supported syntax is not itself a defect.

Apply fixes within the authorized task; otherwise report the recommendation without changing the project.
An explicit modernization or conventions review permits broader recommendations.

## Read the Project First

- **Which checker.** mypy, pyright, basedpyright, ty, or none. Look for `[tool.mypy]`, `mypy.ini`,
  `[tool.pyright]`, `[tool.basedpyright]`, `pyrightconfig.json`, `[tool.ty]`, and the CI workflow. With none, start
  a new project on strict mypy.
- **How strict, and where.** A project often has a strict core and lenient legacy modules. Per-module
  overrides matter more than the global setting.
- **How it runs.** A direct command, a task recipe, a CI step, a hook, or several. Match what is there.
- **Where imports resolve from.** Script-style siblings, a `src/` layout, several tools in one repository, or
  tests without `__init__.py` each add an import root the checker must be told about.
- **Which Python version it targets.** That decides whether PEP 695 syntax, `Self`, and `override` are
  available.

Leave the checker configuration as you found it unless the task is to change it; tightening it as a side effect
of another task turns that task into a migration.

## Generics

Import abstract collection interfaces from `collections.abc` when the project's Python floor supports them.
Accept the capabilities a function needs: use `Sequence` for indexing and `Iterable` for iteration alone.

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

Before 3.12, the same thing with an explicit `TypeVar`:

```python
T = TypeVar("T")

class Box(Generic[T]):
    ...
```

Both forms are correct; use whichever the project's floor allows, and keep one form per file.

Bound a type parameter when the code calls methods on it, or the checker has to assume `object`. Prefer a
bound (`T: float`) to a constraint (`T: (int, str)`): a constraint solves to one of the listed types exactly,
losing any subtype, so reach for it only when the implementation genuinely branches on which it received.

Read [generics.md](references/generics.md) when a generic signature rejects a call that looks correct, or when
writing bounds, variance, `Self`, overloads, `ParamSpec`, `TypedDict`, or type aliases.

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
checker cannot connect to the value: a helper returning `bool`, or a `dict.get()` check followed by a
subscript. A condition stored in a local flag first narrows under pyright but not under mypy.

To make a helper narrow, give it a `TypeIs` or `TypeGuard` return. `TypeIs` (3.13+) narrows both branches, but
only when the narrowed type is compatible with the input type. `TypeGuard` narrows the positive branch alone,
and it is the one that handles an invariant container, such as `list[object]` to `list[str]`:

```python
def is_str_list(value: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(item, str) for item in value)
```

The [typing documentation](https://docs.python.org/3/library/typing.html#typing.TypeIs) states the
compatibility condition. A 3.11 or 3.12 project gets both from `typing_extensions`.

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

Adding `Color.GREEN` to the enum without adding a branch makes mypy report
`Argument 1 to "assert_never" has incompatible type "Literal[Color.GREEN]"; expected "Never"`. It names the
case you forgot, which is why this beats a `raise ValueError` default wherever an enum or a discriminated
union is matched and every case must be handled.

## Any

`Any` disables checking for everything it touches, and it spreads: a function returning `Any` silently
un-types its callers.

Legitimate uses:

- Genuinely dynamic data before validation, such as a freshly parsed JSON payload.
- An untyped third-party library at the boundary where you call it.
- A deliberate escape hatch with a comment saying why.

Prefer the narrower option where one exists. `object` when you accept anything but will check before using it.
`dict[str, Any]` rather than bare `Any` for a payload whose shape is partly known. A `TypedDict` once the
shape is known at all.

Confine `Any` to the boundary. Convert to a real type immediately, and everything inward stays checked.

## Running the Checker

Read [checker-setup.md](references/checker-setup.md) when setting up a checker, before turning on `strict`
anywhere that has existing code, when a checker or language server misses a project's own imports or
cross-file references, when writing a suppression, and when the checker and the code disagree. It holds the
starting configuration, the per-module ladder, import roots, and the debugging order.

Write every suppression as `# type: ignore[error-code]`, so it stops working when the error changes. Each
checker honours that form differently; the reference says how.

## Common Complaints

| Message                                                               | Usually means                                                       |
| --------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `Item "None" of "X \| None" has no attribute`                         | Narrow the optional first, or the check is invisible to the checker |
| `Incompatible types in assignment` on an empty container              | Annotate it: `items: list[str] = []`                                |
| `Returning Any from function declared to return X`                    | An untyped dependency is leaking; convert at the boundary           |
| `Argument has incompatible type "list[Dog]"; expected "list[Animal]"` | `list` is invariant; take `Sequence[Animal]`                        |
| `Cannot determine type of "x"`                                        | Circular inference; annotate the attribute explicitly               |
| `Library stubs not installed for "x"`                                 | Missing stubs; install the `types-*` package                        |
| `Module has no attribute` on a real attribute                         | The type information omits it: stale stubs, or a runtime attribute  |
| `Need type annotation for "x"`                                        | Inference had nothing to work from                                  |

## Before Calling Typing Work Done

1. Does the checker pass at the project's configured strictness, not a lower one you chose?
2. Is every new `# type: ignore` code-specific and justified?
3. Did any signature change from an interface a caller depends on?
4. Is `Any` confined to a boundary, rather than propagating inward?
5. Is a mutable container in a parameter position deliberate, rather than an invariance mistake?
