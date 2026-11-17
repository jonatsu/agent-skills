# Event Consumers

| Consumer                | Events read       | Fields used          | Owner        |
| ----------------------- | ----------------- | -------------------- | ------------ |
| billing (invoice keys)  | `account.created` | `account_id`         | Billing team |
| notifications (welcome) | `account.created` | `account_id`, `name` | Growth team  |

`src/ledger/invoice_consumer.py` mirrors the billing consumer's parsing so changes can be tested here.
