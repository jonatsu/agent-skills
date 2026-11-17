# Scheduled Report Delivery Specification

Status: accepted. Revision 2, accepted 2026-10-27 by the product owner.

Requirement identifiers (`SRD-n`) are stable.

## Purpose

Users receive a saved report by email on a schedule they choose, without opening the product.

## Actors

- Report owner: a signed-in user who owns a saved report and manages its schedules.
- Recipient: a person who receives the delivered report by email. A recipient need not have an account.

## Requirements

### SRD-1 Create a schedule

A report owner can create a schedule for a saved report by choosing a frequency (daily, weekly, or monthly), a time of
day, and a time zone.

Acceptance: after the owner saves a schedule, it appears in the report's schedule list with its next run time shown in
the chosen time zone.

### SRD-2 Recipients

A schedule has between one and ten recipients, each identified by an email address. The report owner can add and remove
recipients.

Acceptance: saving a schedule with zero or eleven recipients is refused with a message that states the allowed range.

### SRD-3 Delivered content

At each scheduled time, the system emails every recipient a PDF of the report as it stands at that time, with the
report's name and the run time in the subject line.

Acceptance: a recipient of a daily schedule receives one email per day whose attachment matches the report shown in the
product at that time.

### SRD-4 Delivery history

When a delivery succeeds, the schedule's history lists it with the delivery time and the word "Delivered".

Acceptance: after a successful run, the history shows a new row with that time and status.

### SRD-5 Pause and resume

A report owner can pause a schedule. A paused schedule delivers nothing until resumed, and resuming continues from the
next scheduled time, with no catch-up deliveries.

Acceptance: pausing for three days and resuming delivers nothing for the paused days and one delivery at the next
scheduled time.

### SRD-6 Edits and deletion

A change to a schedule applies from its next run. Deleting a schedule stops all further deliveries and removes it from
the list.

Acceptance: after the owner changes the time of day, the next delivery arrives at the new time.

## Non-goals

- Delivery by channels other than email.
- Report formats other than PDF.
- Conditional delivery, such as sending only when the data changed.

## Revision history

| Revision | Date       | Change                                                          |
| -------- | ---------- | --------------------------------------------------------------- |
| 2        | 2026-10-27 | Added pause and resume (SRD-5); the recipient limit is now ten. |
| 1        | 2026-10-06 | First accepted revision.                                        |
