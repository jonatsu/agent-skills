"""Billing-side consumer kept in this repository as the reference consumer."""

from ledger.events import decode


def invoice_key(message: str) -> str:
    """Return the invoice partition key for an account event."""
    event = decode(message)
    return f"acct-{event.account_id:010d}"
