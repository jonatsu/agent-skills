# Glossary format

Detail behind the glossary shape in `SKILL.md`. Read it when writing a glossary entry, or when a repository holds
more than one bounded context.

## Entry shape

Each entry is a term, a one- or two-sentence definition of what it *is*, and the words to avoid for it:

```markdown
# {Context name}

{One or two sentences on what this context is and why it exists.}

## Language

**Order**:
A **Customer**'s request to buy goods, from placement through fulfillment.
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a **Customer** after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places **Orders**.
_Avoid_: Client, buyer, account
```

Rules:

- **Be opinionated.** When several words name one concept, pick the best and list the rest under `_Avoid_`. A
  glossary that permits every synonym has recorded nothing.
- **Keep definitions tight.** One or two sentences. Define what the term *is*, not what it does.
- **Define with words the reader already has.** The reader is a newcomer to the domain. Use plain words or other
  glossary terms, and bold a glossary term where a definition uses it. Apply `writing-for-humans` to each
  definition.
- **Only project-specific terms.** Before adding one, ask whether it is a concept unique to this domain or a
  general programming concept. Only the former belongs, however often the latter is used.
- **Group under subheadings** when natural clusters emerge; a flat list is fine when the terms cohere.

## Multiple bounded contexts

Most repositories have a single context and a single glossary. When a codebase holds distinct areas where the
same word legitimately means different things, keep a glossary per context and one map at the root that lists the
contexts, where each lives, and how they relate:

```markdown
# Context map

## Contexts

- [Ordering](./src/ordering/GLOSSARY.md): receives and tracks customer orders
- [Billing](./src/billing/GLOSSARY.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/GLOSSARY.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced`; Fulfillment consumes it to start picking.
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched`; Billing consumes it to invoice.
- **Ordering ↔ Billing**: shared `CustomerId` and `Money` types.
```

The filenames above are illustrative — follow the repository's own convention where it has one, as `SKILL.md`
requires. Infer which context a topic belongs to from the map; when it is unclear, ask rather than guess.
