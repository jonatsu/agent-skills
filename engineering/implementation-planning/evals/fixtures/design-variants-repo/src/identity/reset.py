"""Password reset requests."""

from collections.abc import Callable

GENERIC_RESPONSE = "If the address is registered, a reset email is on its way."


def request_reset(
    email: str,
    find_account: Callable[[str], str | None],
    send_email: Callable[[str, str], None],
) -> str:
    """Send a reset email when the address belongs to an account; always return the same text."""
    account_id = find_account(email)
    if account_id is not None:
        send_email(email, f"reset link for {account_id}")
    return GENERIC_RESPONSE
