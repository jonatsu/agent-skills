# Tool Library Reservation Service Draft

Status: draft, explicitly incomplete. The user confirmed on 2026-11-03 that it captures their intent. Governing
overview: [the tool library overview](tool-library-overview.md). Next phase: technical design.

## Original idea

"People keep turning up for the same drill. Let them reserve tools, and let volunteers see the queue."

## Purpose and outcome

The selected direction advances the overview's first goal, fair and predictable borrowing, without weakening its
principle that access does not depend on a device. The outcome is that a resident can join the queue for a tool, learn
when it is theirs, and collect it from a volunteer, and that volunteers can see the same queue.

## Branches considered

| Branch                                    | Status   | Reason                                                              |
| ----------------------------------------- | -------- | ------------------------------------------------------------------- |
| Reservation queue with volunteer pickup   | Selected | Matches how the shed already works and keeps volunteers in control. |
| Self-service lockers with access codes    | Rejected | Costs money the library does not have and removes volunteers.       |
| Marketplace for lending between residents | Parked   | A different product with trust and liability questions of its own.  |

## Direction

A resident reserves a tool and joins that tool's queue. When the tool returns, the next resident in the queue is told it
is available and has a fixed holding window to collect it. Collection and return always happen in person with the
volunteer on duty, who records both.

## Scope

- Reserve, wait in a queue, collect, and return one tool at a time.
- A volunteer view of every tool's state and queue.
- Reminders to the resident that a tool is ready or due back.

## Exclusions

- The marketplace for lending between residents is parked and not part of this work.
- Fees, deposits, insurance, and damage claims.
- Inventory purchasing and tool maintenance schedules.

## Constraints

1. A resident without a smartphone must keep full access: the same queue, the same standing in it, and the same
   reminders. This is a user decision.
2. No resident is required to install an application or create an account with a third-party service. This is a user
   decision.
3. The service stores only what volunteers need to contact a borrower. This follows the overview and is a user
   decision.
4. The library has no operating budget beyond volunteer time. This is a user decision.

## Early technical direction

A small web service with a page for residents and a page for volunteers. This is provisional, a recommendation to test
in design rather than a decision.

## Success signal

For one month, no tool has two residents who believe it is theirs, and every resident who asked for a tool without a
smartphone received it through the same queue. This is a human-judged observation.

## Open questions for technical design

1. Which reminder channels reach a resident without a smartphone, and who sends them?
2. How does the service identify a resident who has no personal device and no account?
3. How does the queue stay fair when a resident does not collect a tool within the holding window?
4. How do volunteers record a reservation made by phone or in person?
5. What happens to queue state if the volunteer view is unavailable during open hours?

## Decision status

| Item                                | Kind                |
| ----------------------------------- | ------------------- |
| Reservation queue, volunteer pickup | User decision       |
| Marketplace parked                  | User decision       |
| Accessibility constraint            | User decision       |
| Web service for both views          | Provisional         |
| Fixed holding window length         | Question for design |
