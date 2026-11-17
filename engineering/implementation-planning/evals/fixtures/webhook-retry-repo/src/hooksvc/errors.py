"""Exceptions raised by the webhook service."""


class InvalidEndpointError(ValueError):
    """The endpoint URL is not allowed as a webhook target."""


class DeliveryError(RuntimeError):
    """A delivery attempt failed."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
