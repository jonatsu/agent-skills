from identity.reset import GENERIC_RESPONSE, request_reset


def test_unknown_address_gets_generic_response_and_no_email() -> None:
    sent: list[str] = []
    result = request_reset("nobody@example.com", lambda _: None, lambda to, _: sent.append(to))
    assert result == GENERIC_RESPONSE
    assert sent == []


def test_known_address_gets_email() -> None:
    sent: list[str] = []
    request_reset("user@example.com", lambda _: "a1", lambda to, _: sent.append(to))
    assert sent == ["user@example.com"]
