# Attributions

- Author: Joonas Onatsu
- License: `MIT`

Every rule was written independently from the sources below; no text was copied.

## Third-party Sources

### Google: Site Reliability Engineering Workbook, chapter 12, "Introducing Non-Abstract Large System Design"

- Source: <https://sre.google/workbook/non-abstract-design/>
- License: `CC-BY-NC-ND-4.0`
- Version: first edition, 2018, read 2026-11-27

The chapter supplied the four questions asked of each design iteration, estimating with rounded inputs until a
binding constraint appears, the search for single points of failure on each pass, and the cap a consensus round
trip puts on writes that run in sequence.

### Google: Site Reliability Engineering, chapter 4, "Service Level Objectives"

- Source: <https://sre.google/sre-book/service-level-objectives/>
- License: `CC-BY-NC-ND-4.0`
- Version: first edition, 2016, read 2026-11-27

The chapter supplied the SLI, SLO, and SLA distinction, percentiles over averages, the error budget, targets set
from user need rather than current performance, few targets, and an internal SLO tighter than any SLA.

### Gernot Starke: quality.arc42.org, "Specify Quality Requirements"

- Source: <https://quality.arc42.org/articles/specify-quality-requirements>
- License: `CC-BY-SA-4.0`
- Version: revised March 2026, read 2026-11-27

The article supplied the scenario form and its lighter one-sentence variant, and the rules that a measure states
the load it holds at and what the system does on breach.

### Len Bass, Paul Clements, and Rick Kazman; SEI: Software Architecture in Practice, ADD, and ATAM

- Source: *Software Architecture in Practice*, 4th edition, Addison-Wesley, 2021; Attribute-Driven Design 2.0,
  CMU/SEI-2006-TR-023; ATAM, CMU/SEI-2000-TR-004
- License: `LicenseRef-Proprietary`
- Version: as listed in Source

The SEI work supplied the quality attribute scenario, the decomposition loop driven by the highest-ranked quality
drivers, and ranking each target by importance and difficulty.

### Simon Brown: The C4 model

- Source: <https://c4model.com/>
- License: `CC-BY-4.0`
- Version: read 2026-11-27

The model supplied the names of the levels: system, container, component, and deployment node.

### Martin Kleppmann and Chris Riccomini: Designing Data-Intensive Applications

- Source: O'Reilly Media
- License: `LicenseRef-Proprietary`
- Version: 2nd edition, 2026

The book informed choosing a data model from its access patterns, replication lag as something readers see,
sharding keys and hot spots, and consistency named per operation.

### Michael T. Nygard: Release It! Design and Deploy Production-Ready Software

- Source: Pragmatic Bookshelf
- License: `LicenseRef-Proprietary`
- Version: 2nd edition, 2018

The book's stability patterns informed the failure pass: timeouts, circuit breakers, bulkheads, backpressure, and
load shedding, and the load that retries add during an outage.

### Jeffrey Dean and Luiz André Barroso: "The Tail at Scale"

- Source: Communications of the ACM 56(2), 74–80
- License: `LicenseRef-Proprietary`
- Version: February 2013

The paper supplied the fan-out arithmetic behind the latency budget: with 100 calls each fast 99% of the time,
most requests meet a slow call.

### FerroxLabs: wayland `system-designer` skill

- Source: <https://github.com/FerroxLabs/wayland>,
  `src/process/resources/skills-library/bodies/skills/software-engineering/system-designer/SKILL.md`
- License: `AGPL-3.0-or-later`
- Version: `4c030c7b01c241df7b6e3535635a970f10d781af`

The repository's `package.json` declares the licence, and the file's frontmatter claims Apache-2.0. The skill
prompted this one, and supplied the rate conversions, the cache questions, the pagination kinds, and the
rate-limiting windows.

### Hoang Nguyen: agent-skills-standard `system-design` skills

- Source: <https://github.com/HoangNguyen0403/agent-skills-standard>, `skills/system-design/`
- License: `MIT`
- Version: read 2026-11-27

The skills supplied two corrections: percentiles do not add across hops, and availability multiplies only under
independent failure.
