# Architecture Styles in Python

## Define a Port as a Protocol

A `typing.Protocol` states what the core needs without making adapters inherit from it: any class with matching
methods satisfies it, and the type checker verifies the match. Use an abstract base class instead only when adapters
should share default methods. Add `@runtime_checkable` only when code must test `isinstance` against the port.

```python
# shop/core/orders.py: the core imports nothing from adapters or frameworks.
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Order:
    order_id: str
    total_cents: int


class DuplicateOrder(Exception):
    pass


class OrderRepository(Protocol):
    def get(self, order_id: str) -> Order | None: ...

    def add(self, order: Order) -> None: ...


def place_order(orders: OrderRepository, order: Order) -> None:
    if orders.get(order.order_id) is not None:
        raise DuplicateOrder(order.order_id)
    orders.add(order)
```

## Fake the Port in Tests

The fake is a small working repository. Tests check the result through it rather than the calls made on it:

```python
# tests/fakes.py
from shop.core.orders import Order


class InMemoryOrders:
    def __init__(self) -> None:
        self.orders: dict[str, Order] = {}

    def get(self, order_id: str) -> Order | None:
        return self.orders.get(order_id)

    def add(self, order: Order) -> None:
        self.orders[order.order_id] = order
```

## Keep the ORM Out of the Core

The core's types stay plain dataclasses, and the adapter maps between them and the database:

- With SQLAlchemy, either map the domain class imperatively in the adapter package, with
  `registry().map_imperatively(Order, orders_table)`, or keep a separate ORM model and convert in the repository.
- With an ORM whose models must inherit from its base class, such as Django's, keep the models in the adapter and
  convert to and from the core's types in the repository.

Return the core's types from every adapter method, never ORM rows or query sets.

## Wire in the Composition Root

```python
# shop/entrypoints/cli.py: the only module that knows every adapter.
from shop.adapters.sql_orders import SqlOrders
from shop.core.orders import Order, place_order


def main() -> None:
    orders = SqlOrders.connect("sqlite:///shop.db")
    place_order(orders, Order(order_id="A-1", total_cents=500))
```

## Enforce the Direction

`import-linter` fails when a module imports across a forbidden boundary. A `layers` contract lists the packages from
outermost to innermost, and a lower layer may never import a higher one:

```text
[tool.importlinter]
root_package = "shop"

[[tool.importlinter.contracts]]
name = "The core depends on nothing outside it"
type = "layers"
layers = ["shop.entrypoints", "shop.adapters", "shop.core"]
```

Run `lint-imports` in CI, beside the tests.
