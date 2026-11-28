# Attributions

- Author: Joonas Onatsu
- License: `MIT`

Every rule was written independently from the sources below; no text was copied.

## Third-party Sources

### Alistair Cockburn: "Hexagonal architecture"

- Source: <https://alistair.cockburn.us/hexagonal-architecture/>
- License: `LicenseRef-Proprietary`
- Version: HaT Technical Report 2005.02, 2005-09-04

The article supplied ports named for their purpose, several adapters for one port with an in-memory one among them,
and the point that a drawn layer boundary has no way to detect a violation.

### Robert C. Martin: "The Clean Architecture"

- Source: <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
- License: `LicenseRef-No-License`
- Version: published 2012-08-13

The post states no license. It supplied the dependency rule that source dependencies point only inward, and passing
plain data structures across boundaries rather than entities or database rows.

### Jeffrey Palermo: "The Onion Architecture"

- Source: <https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/>,
  <https://jeffreypalermo.com/2013/08/onion-architecture-part-4-after-four-years/>
- License: `LicenseRef-No-License`
- Version: part 1 July 2008, part 4 August 2013

The posts state no license. They supplied interfaces defined by the inner layers, a core that builds without its
infrastructure, and that the style does not suit small applications.

### Martin Fowler: bliki and articles on layering and test doubles

- Source: <https://martinfowler.com/bliki/PresentationDomainDataLayering.html>,
  <https://martinfowler.com/articles/badri-hexagonal/>, <https://martinfowler.com/bliki/TestDouble.html>,
  <https://martinfowler.com/articles/mocksArentStubs.html>
- License: `LicenseRef-No-License`
- Version: 2015-08-26, 2014-06, 2006-01-17, and read 2026-11-28

The pages state no license. They supplied that swapping a database is rare, that a framework can serve as the
platform for a simple domain, and the difference between fakes and mocks.

### Mark Seemann: posts on composition and architecture

- Source: <https://blog.ploeh.dk/2011/07/28/CompositionRoot/>,
  <https://blog.ploeh.dk/2013/12/03/layers-onions-ports-adapters-its-all-the-same/>,
  <https://blog.ploeh.dk/2014/06/10/pure-di/>,
  <https://blog.ploeh.dk/2016/03/18/functional-architecture-is-ports-and-adapters/>
- License: `LicenseRef-No-License`
- Version: 2011-07-28, 2013-12-03, 2014-06-10, 2016-03-18

The posts state no license. They supplied the composition root near the entry point, wiring by hand before any
container, layering with inverted dependencies as ports and adapters, and functional design arriving at the same
shape.

### Gary Bernhardt: "Boundaries" and "Functional Core, Imperative Shell"

- Source: <https://www.destroyallsoftware.com/talks/boundaries>,
  <https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell>
- License: `LicenseRef-No-License`
- Version: 2012

The pages state no license. The talk supplied a pure core that decides on values and a thin shell that does the
input and output, with core tests that need no test doubles.

### Harry Percival and Bob Gregory: Architecture Patterns with Python

- Source: <https://www.cosmicpython.com/book/>
- License: `LicenseRef-CC-BY-NC-ND`
- Version: online edition, last updated 2023-11-24

The book states a CC BY-NC-ND license without a version, so no text or code was adapted. It supplied the cost of
every extra layer, Active Record as the better choice for simple cases, a hard-to-fake port as a sign of a poor
abstraction, duck-typed ports, and the bootstrap script as the composition root.

### Gerard Meszaros: xUnit Test Patterns, "Fake Object"

- Source: <http://xunitpatterns.com/Fake%20Object.html>
- License: `LicenseRef-Proprietary`
- Version: book 2007

The pattern supplied the fake as a lightweight working implementation that replaces a dependency in tests.

### David Heinemeier Hansson and Jimmy Bogard: critiques of layered and hexagonal designs

- Source: <https://dhh.dk/2014/test-induced-design-damage.html>,
  <https://www.jimmybogard.com/vertical-slice-architecture/>
- License: `LicenseRef-No-License`
- Version: 2014, and read 2026-11-28

The posts state no license. They supplied the failures of applying a style by rote: indirection added for tests
alone, and layers that only pass calls through.

### The Rust Project: The Rust Reference, traits

- Source: <https://github.com/rust-lang/reference>, `src/items/traits.md`
- License: `MIT OR Apache-2.0`
- Version: read 2026-11-28

The reference supplied the dyn-compatibility rules, including that an `async fn` makes a trait unusable as a trait
object.

### FerroxLabs: wayland `clean-architecture-patterns` and `hexagonal-architecture` skills

- Source: <https://github.com/FerroxLabs/wayland>,
  `src/process/resources/skills-library/bodies/skills/software-engineering/`
- License: `AGPL-3.0-or-later`
- Version: `4c030c7b01c241df7b6e3535635a970f10d781af`

The repository's `package.json` declares the license, and the files' frontmatter claims Apache-2.0. The skills
supplied the split between driving and driven ports, where cross-cutting concerns belong, the anemic-domain failure,
and gradual migration behind a port.
