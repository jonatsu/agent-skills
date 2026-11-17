-- Initial schema; matches hooksvc.store.SCHEMA at version 0.4.0.
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    secret TEXT NOT NULL
);
CREATE TABLE deliveries (
    id INTEGER PRIMARY KEY,
    subscription_id INTEGER NOT NULL REFERENCES subscriptions(id),
    payload TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
