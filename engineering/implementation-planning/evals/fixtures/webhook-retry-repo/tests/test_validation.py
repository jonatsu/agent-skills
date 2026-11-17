import pytest

from hooksvc.errors import InvalidEndpointError
from hooksvc.validation import validate_endpoint


def test_accepts_public_https() -> None:
    assert validate_endpoint("https://hooks.example.com/in") == "https://hooks.example.com/in"


@pytest.mark.parametrize(
    "url", ["http://hooks.example.com/in", "https://10.0.0.5/in", "https://127.0.0.1/in"]
)
def test_rejects_disallowed_targets(url: str) -> None:
    with pytest.raises(InvalidEndpointError):
        validate_endpoint(url)
