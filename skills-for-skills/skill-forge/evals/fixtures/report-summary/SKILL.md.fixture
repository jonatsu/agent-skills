---
name: report-summary
description: Summarize supplied service counts as a Markdown table. Use when the user provides service records and requests a count report.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Report Summary

Produce a Markdown table with columns `Service` and `Count` from the records supplied in the request.
Sort rows alphabetically by service name. Omit records whose count is zero. Display an absent count as
`unknown`. Use only supplied records and make no external data requests.

The [regression fixture](evals/regression.json) supplies synthetic examples of this procedure's current
output and the requested zero-count correction. These examples are test data, not evidence of model runs.
