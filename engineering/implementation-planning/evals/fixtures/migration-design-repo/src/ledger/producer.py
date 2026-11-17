"""Create accounts and publish their events."""

from collections.abc import Callable

from ledger.events import AccountCreated, encode
from ledger.storage import AccountStore


def open_account(store: AccountStore, publish: Callable[[str], None], name: str) -> int:
    """Create an account, publish `account.created`, and return the id."""
    account = store.create(name)
    publish(encode(AccountCreated(account_id=account.id, name=account.name)))
    return account.id
