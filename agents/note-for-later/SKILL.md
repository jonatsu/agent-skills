---
name: note-for-later
description: "Record work for later in the repository's own ledger, such as its TODO, backlog, or roadmap, as a committed entry a stranger can act on, then resume the current work. Use when asked to note, park, or remember something for later, add it to the TODO, backlog, or roadmap, file a bug or idea to handle another time, or on /note-for-later. Not for session memory or lessons learned, or for tracking steps within the current task."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Note for Later

Record each item in a versioned file now, then return to the work in progress. An item held in a task list,
the conversation, or agent memory is lost when the session ends, and an item left for the next natural break
is lost when the break never comes. Recording takes a minute, so it preempts the current work.

The request is the text after the invocation, or the user's words asking to note something for later. It may
hold several items; split them and route each on its own.

## 1. Read the Destination Override

An item may start with a prefix naming its destination:

- a type: `todo:`, `bug:`, `backlog:`, `roadmap:`, or `idea:`; or
- a ledger path, such as `skills/TODO.md:`.

A prefix settles the destination, so skip step 2 for that item. When the named ledger does not exist, say so
and ask where it goes, since the user chose a place that is not there.

## 2. Classify the Item

Without a prefix, infer the type from the user's wording and the item itself:

- **TODO:** open work needed soon, such as a bug, a dated recheck, or work the user asked for.
- **Backlog:** wanted work that nothing depends on yet, with reasoning worth keeping.
- **Roadmap:** planned direction or a milestone for a product or stack.
- **Plan follow-up:** a step, open question, or deviation that belongs to an active plan or design document.
  The plan owns it, so it goes there rather than into a general ledger.
- **Idea or source to evaluate:** a tool, repository, or article to assess later.

Decide without asking. A question interrupts the work this skill exists to protect, and the confirmation in
step 6 lets the user move a misplaced item with one reply.

## 3. Find the Ledger

Read the repository's floor file and the header of each candidate ledger. A ledger's header usually states
what belongs in it, and that rule outranks the type list above.

Choose the most specific ledger in scope: a subtree's own `TODO.md` or roadmap beats the root one for work
inside that subtree. An idea to evaluate goes to a ledger's candidate list when one exists, and otherwise to the
backlog.

When the repository has no ledger for the type, create `TODO.md` or `BACKLOG.md` at the root with a short header
stating what belongs there, following `context-architecture`'s default layout when that skill is available.
Those two are the only ledgers to create unasked: a roadmap item in a repository without a roadmap goes to the
backlog, and the confirmation says so.

## 4. Check for a Duplicate

Search the chosen ledger, and its neighbours, for an entry on the same subject. When one exists, add the new
information to it rather than writing a second entry, and say that you updated it.

## 5. Write the Entry

Match the format of the entries already in the ledger: its heading level, bullet or checkbox style, bold lead,
and section. Put the entry in the section it belongs to, near related entries.

Write for a reader who was not in this session. The entry holds:

- what the work is, in one clear lead sentence;
- why it matters, or what goes wrong without it;
- what is already known: findings, decisions made, paths ruled out;
- every link, path, URL, command, and error text the user gave or the session established, verbatim; and
- the date, from a time source rather than memory, and the condition for picking it up again when one exists.

Take every detail from the user or the session. Where something the reader will need is unknown, write that it
is unknown; a plausible guess in a ledger reads later as a fact.

Keep the entry proportionate: one or two sentences for a simple item, a short paragraph or two for one that
carries context.

## 6. Commit and Confirm

Commit each entry on its own, naming only the ledger file in the commit's pathspec, so it never mixes with work
in progress, and in the repository's commit convention. When the ledger file already has changes that are not
yours, leave the entry uncommitted and say so instead. Push only when the user authorizes it. When the
repository uses an issue tracker and the user asks for an issue, create one there instead of a file entry;
it publishes the item, so confirm the title and body first.

Then confirm in one line per item: what was recorded, the ledger and section, and the commit. Resume the
interrupted work in the same turn.
