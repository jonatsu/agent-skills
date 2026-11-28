---
name: architecture-styles
description: "Choose and apply an application architecture style: layered, hexagonal (ports and adapters), Clean or Onion, or functional core and imperative shell. Use when structuring an application around its domain, deciding whether a style is worth its cost, placing interfaces to databases or services, keeping ORM and framework types out of the core, or testing through fakes. Not for the design document (technical-design), Python package layout (python-architecture), or architecture review (architecture-review)."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Architecture Styles

Layered, hexagonal, Clean, and Onion Architecture all apply one dependency rule at different granularity: the core,
which holds the domain and its decisions, names no outer code, and the outer code depends on the core. Functional core
and imperative shell reaches the same goal without interfaces. Choose how much of this an application needs, then
apply it so the rule holds.

## 1. Decide Whether a Style Earns Its Cost

Every boundary adds indirection, mapping code, and one more place to look. It pays for itself when the code has at
least one of these:

- domain rules complex enough to need tests that run without a database or network;
- several ways in or out, such as an HTTP API, a CLI, a queue, and two external services;
- input and output that is slow, costly, or awkward to exercise in tests;
- a long expected life, with the infrastructure likely to change under the domain.

When none holds, as in create-read-update-delete work with simple rules or a short script, use plain modules, or let
the framework be the platform, for example with Active Record. Apply a style to the parts that need it, not to the
whole application by default. No controlled study shows that one style beats another, so argue from the code's
needs.

This step is done when the design names, for each part of the application, the reason it gets a boundary or none.

## 2. Choose the Shape

- **Functional core, imperative shell:** the default wherever the decisions can be pure functions. The core takes
  values and returns values, including decisions about what to do next, and a thin shell does all input and output.
- **Ports and adapters (hexagonal):** when the core must hold an ongoing conversation with the outside, such as
  loading state partway through a decision, or calling a payment service and acting on the result.
- **Clean or Onion rings:** ports and adapters with named inner layers, such as entities inside use cases. Add rings
  only when there are many use cases that share entities.
- **Plain layering:** presentation, domain, and data access, acceptable when the domain depends on data access only
  through interfaces the domain defines. With that inversion, layering becomes ports and adapters.

## 3. Apply the Dependency Rule

1. Put the domain types and decisions in the core, and import nothing into it from the framework, the database
   driver, or the network library.
2. Define each port in the core, named for what the core needs, such as `OrderRepository` or `PaymentGateway`, never
   for what provides it. A driving port is what callers ask of the core; a driven port is what the core asks of the
   outside.
3. Draw a port only for a real dependency: storage, an external service, a clock, randomness, or a delivery
   mechanism. Keep it to the operations the core uses.
4. Pass plain values across every boundary, never ORM rows, request objects, or framework types. The adapter maps
   between them.
5. Implement each port in an adapter outside the core, one adapter per technology.

The rule holds when the core builds and its tests run with no adapter present.

## 4. Wire It in One Place

Create the adapters and hand them to the core in one composition root, as close to the entry point as possible, such
as `main` or the application factory. Wire by hand first: constructor arguments and plain functions suffice. A
dependency-injection container is optional, and only the composition root may refer to it. A library has no
composition root; it accepts its dependencies from the application that uses it.

## 5. Test Through the Ports

- Test the core's decisions directly, as pure functions where possible, with no test doubles.
- Test code that uses a driven port with a hand-written fake: a small working implementation, such as an in-memory
  repository. A fake checks results rather than call sequences, so it survives refactoring.
- Use a mock only where the call itself is the result, such as "an email was sent".
- Give each adapter a few integration tests against the real technology.

When a port is hard to fake, it is too large or too close to its technology, so narrow it.

## 6. Enforce the Rule Mechanically

A diagram cannot detect a violation, so add a check that fails the build when the core imports outer code: an import
contract in Python, or separate crates in Rust, where the compiler enforces the direction. Run it in CI.

## Recognize the Failures

- **Leaking types:** an ORM entity, request object, or framework annotation in the domain.
- **An interface for every class:** ports for things with one implementation and no reason to vary.
- **Pass-through layers:** a service that only forwards to a repository, added because the diagram has a ring.
- **An anemic domain:** entities that only hold data while the use cases make every decision. Move each rule into the
  type that owns the data it protects.
- **Cross-cutting leaks:**
  - transactions belong behind a unit-of-work port;
  - caching belongs in an adapter that wraps another adapter;
  - authentication belongs in the driving adapter, and authorization in the core.

## Move Existing Code Gradually

Restructure one slice at a time, starting where the code changes for a business reason. First write characterization
tests that pin down the current behaviour. Then put a port in front of the legacy code, with an adapter that calls
it, and move rules into the core one at a time. Avoid a rewrite, which discards the edge cases the old code learned.

## Language Notes

- Python: read [references/python.md](references/python.md) before defining ports or mapping between the domain and
  an ORM.
- Rust: read [references/rust.md](references/rust.md) before choosing between generics and trait objects, or
  splitting crates.
