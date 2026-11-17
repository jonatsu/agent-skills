import sqlite3
from pathlib import Path

from ledger.events import decode
from ledger.invoice_consumer import invoice_key
from ledger.producer import open_account
from ledger.storage import AccountStore

SCHEMA = Path(__file__).parent.parent / "migrations" / "0001_accounts.sql"


def make_store() -> AccountStore:
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA.read_text())
    return AccountStore(connection)


def test_open_account_publishes_event() -> None:
    store = make_store()
    published: list[str] = []
    account_id = open_account(store, published.append, "Example Org")
    assert decode(published[0]).account_id == account_id
    assert store.get(account_id) is not None


def test_invoice_key_pads_integer_id() -> None:
    message = '{"type": "account.created", "data": {"account_id": 42, "name": "x"}}'
    assert invoice_key(message) == "acct-0000000042"
