# Retention and Recovery Specification

Status: accepted. Revision 4, accepted 2026-10-09 by the product owner.

Requirement identifiers (`RR-n`) are stable. A change to a requirement's meaning gets a new identifier.

## Purpose

Members can undo a deletion for a limited time, and administrators control what is removed permanently and when.

## Actors

- Member: a person in a workspace who adds and deletes items.
- Item owner: the member who added an item.
- Administrator: a member with the administrator role in a workspace.

## Requirements

### RR-1 Deleted items wait in Recently deleted

When a member deletes an item they may delete, the item disappears from folder listings and search, and appears in the
workspace's "Recently deleted" list with its deletion date.

Acceptance: after deletion, a search for the item's name returns nothing and the Recently deleted list shows it.

### RR-2 Restore within 30 days

The item owner or an administrator can restore a deleted item within 30 days of its deletion. A restored item returns to
its original folder, or to the workspace's top level when that folder no longer exists.

Acceptance: restoring on day 29 returns the item to its folder; restoring after its folder was deleted places it at the
top level.

### RR-3 Permanent removal after 30 days

An item that has stayed deleted for 30 days is removed permanently. Nobody can restore it afterwards, and it no longer
counts toward the workspace's storage use.

Acceptance: on day 31, the item is absent from Recently deleted and cannot be restored.

### RR-4 Early permanent deletion

An administrator can permanently delete an item from Recently deleted before 30 days have passed.

Acceptance: after the administrator confirms, the item is absent from Recently deleted and cannot be restored.

### RR-5 Holds

An administrator can place a hold on an item. A held item is not removed permanently until the hold is released, and its
30 days start again when the hold is released.

Acceptance: a deleted item under hold is still restorable on day 45; after release, it stays restorable for 30 more
days.

### RR-6 Earlier versions

The last 10 versions of an item are kept, and the item owner or an administrator can restore an earlier version as the
current one.

Acceptance: after 12 edits, the version list shows 10 versions, and restoring the third newest makes it current.

### RR-7 Activity record

Deleting, restoring, and permanently removing an item each add an entry to the workspace activity log with the item, the
member, and the time.

Acceptance: after a delete and a restore, the log shows two entries naming the same item and member.

## Non-goals

- Recovery of a deleted workspace.
- Deletion requests under privacy law, which another specification will cover.
- Changing the retention period per workspace.

## Revision history

| Revision | Date       | Change                                             |
| -------- | ---------- | -------------------------------------------------- |
| 4        | 2026-10-09 | Added holds (RR-5) and the activity record (RR-7). |
| 3        | 2026-09-22 | Added earlier versions (RR-6).                     |
| 2        | 2026-09-08 | Added early permanent deletion (RR-4).             |
| 1        | 2026-08-25 | First accepted revision.                           |
