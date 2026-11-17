"""Send one signed webhook request."""

import hashlib
import hmac

import httpx

from hooksvc.errors import DeliveryError
from hooksvc.store import Store

TIMEOUT_SECONDS = 10.0


def sign(secret: str, body: bytes) -> str:
    """Return the hex HMAC-SHA256 signature for a body."""
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def deliver(store: Store, client: httpx.Client, subscription_id: int, payload: str) -> None:
    """Send the payload once and record whether it was delivered."""
    subscription = store.get_subscription(subscription_id)
    if subscription is None:
        raise DeliveryError(f"unknown subscription {subscription_id}")
    body = payload.encode()
    headers = {"X-Signature": sign(subscription.secret, body), "Content-Type": "application/json"}
    try:
        response = client.post(
            subscription.endpoint, content=body, headers=headers, timeout=TIMEOUT_SECONDS
        )
    except httpx.HTTPError as error:
        store.record_delivery(subscription_id, payload, "failed")
        raise DeliveryError("request failed") from error
    if response.status_code >= 300:
        store.record_delivery(subscription_id, payload, "failed")
        raise DeliveryError("endpoint rejected delivery", response.status_code)
    store.record_delivery(subscription_id, payload, "delivered")
