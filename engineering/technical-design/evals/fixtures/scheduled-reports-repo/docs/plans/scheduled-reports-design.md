# Scheduled Report Delivery Design

Status: draft, in progress. Realizes the
[scheduled report delivery specification](../specs/scheduled-report-delivery-spec.md), revision 2 (accepted). A design
leads implementation, then follows it: once code exists, the code wins and this document is updated to match. Open
items are in the questions register and the task ledger at the end.

## 1. Introduction and goals

The service delivers saved reports by email at times the report owner chose. It adds three obligations to the existing
reporting product: keeping each schedule's next run time correct across time zones and daylight saving changes (SRD-1,
SRD-6), producing the PDF as the report stands at the run time (SRD-3), and recording each successful delivery
(SRD-4). Pause and resume (SRD-5) must not create catch-up deliveries.

## 3. Context and scope

The service sits between three existing systems. The reporting product owns saved reports and renders them to PDF on
request. The mail provider accepts a message with an attachment and returns an acceptance or a rejection. The product
database holds users and saved reports. The service is new and owns schedules, runs, and deliveries.

## 5. Building block view

| Component   | Responsibility                                                                                     |
| ----------- | -------------------------------------------------------------------------------------------------- |
| Scheduler   | Finds schedules whose next run time has passed, creates one run for each, and advances the time.   |
| Renderer    | Asks the reporting product for the PDF of a saved report at the run time.                          |
| Dispatcher  | Sends the PDF to each recipient through the mail provider and returns the provider's answer.       |
| Schedule DB | Stores schedules, recipients, runs, and delivery records. Only the Scheduler writes next run time. |

The Scheduler and the Dispatcher never call each other. A run record connects them: the Scheduler creates it, and a
worker moves it through rendering and dispatch.

## 6. Runtime view

### 6.1 A scheduled run

1. The Scheduler selects every active schedule whose next run time is at or before now, in one transaction.
2. For each, it inserts a run record keyed by schedule identifier and planned run time, then advances the schedule's
   next run time to the next occurrence in the schedule's time zone. The key makes the insert idempotent, so two
   Scheduler instances cannot create the same run twice (SRD-3).
3. A worker claims the run, calls the Renderer, and passes the PDF to the Dispatcher.
4. After the provider accepts the message for every recipient, the worker records a delivery with the delivery time
   (SRD-4).

### 6.2 Pause and resume

Pausing sets the schedule's state to paused, and the Scheduler skips paused schedules. Resuming sets the next run time
to the next occurrence after now, so no skipped occurrence is created (SRD-5).

## 9. Architecture decisions

| Decision                                                         | Status      | Reason                                                              |
| ---------------------------------------------------------------- | ----------- | ------------------------------------------------------------------- |
| Store next run time as a UTC instant plus the schedule's zone    | Decided     | Recomputing from the zone keeps wall-clock time across DST changes. |
| One run record per planned occurrence, unique by schedule + time | Decided     | Makes scheduler restarts and parallel instances safe.               |
| Render at run time, not at schedule creation                     | Decided     | SRD-3 requires the report as it stands at that time.                |
| Use the existing job queue for workers                           | Provisional | Avoids a new dependency; its limits are unchecked.                  |

## Questions register

1. Does the existing job queue support delayed and unique jobs, or does the Scheduler need its own claim mechanism?
2. How large can a rendered PDF be, and does the mail provider's attachment limit bind?
3. Which run time applies to the subject line when a worker starts late?

## Task ledger

1. Design how a run's rendering and dispatch are recorded, and the states a run moves through.
2. Design observability for the Scheduler and workers.
3. Write the planning handoff once the questions register is empty.
