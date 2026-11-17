import httpx
import pytest

from hooksvc.errors import DeliveryError
from hooksvc.sender import deliver
from hooksvc.store import Store


def client_returning(status: int) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(status)))


def test_records_successful_delivery(store: Store) -> None:
    subscription_id = store.add_subscription("t1", "https://hooks.example.com/in", "s3cret")
    deliver(store, client_returning(204), subscription_id, "{}")


def test_raises_on_rejected_delivery(store: Store) -> None:
    subscription_id = store.add_subscription("t1", "https://hooks.example.com/in", "s3cret")
    with pytest.raises(DeliveryError) as raised:
        deliver(store, client_returning(503), subscription_id, "{}")
    assert raised.value.status_code == 503
