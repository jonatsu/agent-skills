# Architecture Styles in Rust

## Define a Port as a Trait

The core declares the trait and its own error type, and each adapter maps its errors into that type. Take the port as
a generic parameter by default: the compiler checks it, and the call costs nothing at run time.

```rust,run
use std::collections::HashMap;

// The core: domain types, the port, and the decision.
#[derive(Clone, Debug, PartialEq)]
pub struct Order {
    pub id: u64,
    pub total_cents: u64,
}

#[derive(Debug, thiserror::Error)]
pub enum OrderError {
    #[error("order {0} already exists")]
    Duplicate(u64),
    #[error("storage failed: {0}")]
    Storage(String),
}

pub trait OrderRepository {
    fn get(&self, id: u64) -> Result<Option<Order>, OrderError>;
    fn add(&mut self, order: Order) -> Result<(), OrderError>;
}

pub fn place_order<R: OrderRepository>(orders: &mut R, order: Order) -> Result<(), OrderError> {
    if orders.get(order.id)?.is_some() {
        return Err(OrderError::Duplicate(order.id));
    }
    orders.add(order)
}

// A fake adapter: a small working repository for tests.
#[derive(Default)]
pub struct InMemoryOrders {
    orders: HashMap<u64, Order>,
}

impl OrderRepository for InMemoryOrders {
    fn get(&self, id: u64) -> Result<Option<Order>, OrderError> {
        Ok(self.orders.get(&id).cloned())
    }

    fn add(&mut self, order: Order) -> Result<(), OrderError> {
        self.orders.insert(order.id, order);
        Ok(())
    }
}

fn main() {
    let mut orders = InMemoryOrders::default();
    place_order(&mut orders, Order { id: 1, total_cents: 500 }).unwrap();
    let again = place_order(&mut orders, Order { id: 1, total_cents: 500 });
    assert!(matches!(again, Err(OrderError::Duplicate(1))));
}
```

## Choose Generics or a Trait Object

Use a trait object, `&mut dyn OrderRepository` or `Box<dyn OrderRepository>`, when the adapter is chosen at run time
or several adapters share one collection. The trait must then be dyn compatible: no generic methods, no
`-> impl Trait` return, and no `async fn`, because each of these has a type the caller cannot name.

```rust,compile_fail,E0038
trait Notifier {
    async fn notify(&self, message: &str);
}

fn send_all(notifiers: &[Box<dyn Notifier>]) {
    let _ = notifiers;
}
```

For an asynchronous port behind `dyn`, return a boxed future instead:

```rust
use std::future::Future;
use std::pin::Pin;

pub trait Notifier {
    fn notify<'a>(&'a self, message: &'a str) -> Pin<Box<dyn Future<Output = ()> + Send + 'a>>;
}

pub struct ConsoleNotifier;

impl Notifier for ConsoleNotifier {
    fn notify<'a>(&'a self, message: &'a str) -> Pin<Box<dyn Future<Output = ()> + Send + 'a>> {
        Box::pin(async move { println!("{message}") })
    }
}
```

Keep the port generic when nothing needs `dyn`; an `async fn` in a trait then works directly.

## Enforce the Direction With Crates

Split the workspace so Cargo enforces the rule: the core crate's manifest lists no adapter crate, so the core cannot
import one, and a dependency cycle between crates is rejected.

```text
shop/
├── Cargo.toml          # [workspace] members = ["core", "adapters", "app"]
├── core/               # domain types and ports; no adapter or framework dependency
├── adapters/           # depends on core; implements the ports
└── app/                # the binary; depends on both, and wires them in main
```

Start with modules in one crate while the boundaries are still moving, and split into crates once they settle.
