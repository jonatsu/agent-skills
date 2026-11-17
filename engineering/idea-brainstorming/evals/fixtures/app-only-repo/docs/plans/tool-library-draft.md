# Tool Library Reservations: Brainstorm Draft

Status: incomplete draft, handed to technical design. The user confirmed that it captures what they want to refine.

Governing overview: [Tool Library Overview](tool-library-overview.md). This direction advances it by replacing manual
pickup coordination with self-service reservations.

## Original Idea

Volunteers spend hours each week matching borrowers to tools by phone calls and a paper sign-up sheet. The idea was to
let residents reserve tools themselves.

## Purpose and Desired Outcome

Residents reserve an available tool and collect it at an agreed time without a volunteer arranging it. Volunteers see
the day's pickups in one place.

## Branches Considered

- **Mobile app with reservations and push reminders** (selected by the user). Residents browse the collection, join a
  queue for a tool, and get a push notification when it is ready.
- **Shared spreadsheet maintained by volunteers.** Cheap, but keeps volunteers in the loop for every booking.
- **Marketplace for lending private tools between residents.** Parked: it widens the scope beyond the shared
  collection.

## Current Direction

An app-only service: residents reserve tools in a mobile app, receive push reminders, and confirm pickup in the app.
Volunteers use the same app to see pickups.

## Scope and Exclusions

In scope: reservations for the shared collection, a queue per tool, pickup reminders. Excluded: payments and deposits.
Parked: the private-tool marketplace.

## Assumptions

- Provisional: residents who borrow tools carry smartphones and will install the app.
- Provisional: volunteers will check the app before each pickup slot.

## Observable Success Signal

Within two months of launch, most pickups are booked without a volunteer phone call.

## Questions for Technical Design

- How should the queue handle a resident who misses a pickup slot?
- Which push notification service fits the volunteers' budget?

## Route

Straight to technical design: the direction is small and its behavior is clear. The user decided not to write a
separate spec.
