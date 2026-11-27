# Writing an Interface Reference

An interface reference states the contract a caller relies on: what goes in, what comes out, and what fails.
Read the interface's governing source before writing, such as its schema, OpenAPI document, or argument parser.
Where the project generates the reference from a specification or from doc comments, write in that source rather
than in a copy beside it. The prose then adds what the source cannot carry: intent, edge behavior, and recovery.

## Each Item

Give each operation, setting, or option its own heading, named as the reader looks it up. Cover these in the same
order for every item, and say "none" where one does not apply:

- what it does, in one or two sentences, and when to use it;
- what it needs first, such as authentication, a permission, or a prior state;
- each input: its name and location, type, whether it is required, valid values and limits, and what happens
  when it is omitted;
- the output: its shape, each field the caller reads, and which fields may be absent or null;
- each error: what triggers it, what the caller sees, and how the caller recovers;
- each limit a caller can hit, such as a rate limit, with the signal it gives and the wait it expects; and
- an example.

Leave out how the item works inside unless a caller depends on it, such as its cost or its ordering.

## Examples

Show each request with its response, and each command with its output. Show at least one failure beside the
success, with the error the reader will actually meet. Make each example complete enough to run as written,
including its imports, headers, and setup, and build it from reserved values as `SKILL.md` describes.

## Change and Deprecation

Mark each item with the version that introduced it when readers run more than one version. Mark a deprecated
item with the version that deprecated it, the version that removes it when one is set, and its replacement or
migration step, because "deprecated" alone gives the reader nothing to do. Mark an unstable item as experimental
where the reader first meets it.

The reference is done when every item the interface exposes has an entry covering each point above, and each
example has run against the version the reference names.
