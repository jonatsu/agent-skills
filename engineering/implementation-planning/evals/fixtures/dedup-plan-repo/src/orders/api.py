"""HTTP handlers for order creation."""

import json
import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    """A minimal HTTP response."""

    status: int
    body: str


def create_order(db: sqlite3.Connection, account_id: str, body: str) -> Response:
    """Handle `POST /orders`: store the order and return it."""
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return Response(400, json.dumps({"error": "invalid json"}))
    cursor = db.execute(
        "INSERT INTO orders (account_id, item, quantity) VALUES (?, ?, ?)",
        (account_id, payload["item"], int(payload["quantity"])),
    )
    order = {"id": cursor.lastrowid, "item": payload["item"], "quantity": payload["quantity"]}
    return Response(201, json.dumps(order))
