"""The delivery worker: claims one message at a time and posts it."""

import sqlite3
from collections.abc import Callable

from delivery import store

MAX_ATTEMPTS = 5

# Posts a body to an endpoint with an idempotency key and returns the HTTP status code.
Sender = Callable[[str, str, str], int]


class Worker:
    def __init__(self, conn: sqlite3.Connection, send: Sender, worker_id: str) -> None:
        self._conn = conn
        self._send = send
        self._worker_id = worker_id

    def run_once(self, now: str) -> bool:
        """Deliver one message. Return False when no message was pending."""
        message = store.claim_next(self._conn, self._worker_id, now)
        if message is None:
            return False
        try:
            status = self._send(message["endpoint"], message["body"], message["id"])
        except OSError as error:
            store.mark_attempt_failed(self._conn, message["id"], str(error), MAX_ATTEMPTS)
            return True
        if 200 <= status < 300:
            store.mark_delivered(self._conn, message["id"])
        else:
            store.mark_attempt_failed(self._conn, message["id"], f"HTTP {status}", MAX_ATTEMPTS)
        return True
