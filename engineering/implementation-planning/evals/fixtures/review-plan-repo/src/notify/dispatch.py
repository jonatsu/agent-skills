"""Send a notification on every channel."""

from collections.abc import Callable

Channel = Callable[[str, str], None]


def dispatch(user_id: str, message: str, channels: dict[str, Channel]) -> list[str]:
    """Send the message on every channel and return the channel names used."""
    for send in channels.values():
        send(user_id, message)
    return sorted(channels)
