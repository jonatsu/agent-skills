# Implementation Plan: Request Deduplication

Status: Draft

Design: [request-dedup.md](../design/request-dedup.md)

## Overview

Add the `idempotency_keys` table, then teach `create_order` to read the `Idempotency-Key` header, store results, and
return stored results on retry. Cleanup comes last because nothing depends on it.

## Unit 1: Key storage

Add migration `0002_idempotency_keys.sql` creating the table with primary key `(account_id, key)`, and a small
`orders/idempotency.py` module with `lookup`, `begin`, and `complete` functions.

Verification:

- `rg idempotency_key src/` shows the new module and migration.
- `git status` shows a clean tree after committing.

## Unit 2: Handler integration

Change `create_order` to accept an optional `idempotency_key` argument, hash the canonical body, and use the module from
Unit 1 for the same-key, conflict, and in-progress paths.

Verification:

- `rg idempotency_key src/orders/api.py` finds the new argument.
- `just lint` passes.
- `git status` shows a clean tree after committing.

## Unit 3: Expiry cleanup

Add an hourly job that deletes rows older than 24 hours.

Verification:

- `rg 86400 src/` finds the expiry constant.
- `git status` shows a clean tree after committing.

## Done When

`rg idempotency_key` finds the feature in every expected file and the tree is clean.
