# Release Process

Releases ride a staged train. Each stage holds until its watch period ends without an alarm.

1. Canary: one instance, 2 hours.
2. 25 percent of instances, 24 hours.
3. All instances.

Any stage can be halted and rolled back to the previous release from the release train console. A release that
includes a non-reversible migration needs the migration's rollback note approved before the canary starts.

Dashboards: `ledger-overview` shows request errors, event publish failures, and consumer decode errors reported by
subscribed services.
