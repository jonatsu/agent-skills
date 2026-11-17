"""Account events published to other services."""

import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AccountCreated:
    """Published once when an account is created."""

    account_id: int
    name: str


def encode(event: AccountCreated) -> str:
    """Serialize an event for the message bus."""
    return json.dumps({"type": "account.created", "data": asdict(event)})


def decode(message: str) -> AccountCreated:
    """Parse a message from the bus; consumers use this helper."""
    body = json.loads(message)
    data = body["data"]
    return AccountCreated(account_id=int(data["account_id"]), name=str(data["name"]))
