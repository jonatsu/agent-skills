import json
import sqlite3

from orders.api import create_order


def make_db() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute(
        "CREATE TABLE orders (id INTEGER PRIMARY KEY, account_id TEXT, item TEXT, quantity INTEGER)"
    )
    return db


def test_creates_order() -> None:
    response = create_order(make_db(), "acct-1", json.dumps({"item": "widget", "quantity": 2}))
    assert response.status == 201
    assert json.loads(response.body)["item"] == "widget"


def test_rejects_invalid_json() -> None:
    assert create_order(make_db(), "acct-1", "{").status == 400
