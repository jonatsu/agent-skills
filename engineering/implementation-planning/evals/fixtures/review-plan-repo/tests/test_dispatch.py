from notify.dispatch import dispatch


def test_dispatch_uses_every_channel() -> None:
    sent: list[tuple[str, str, str]] = []
    channels = {
        "email": lambda user, msg: sent.append(("email", user, msg)),
        "in_app": lambda user, msg: sent.append(("in_app", user, msg)),
    }
    assert dispatch("u1", "hello", channels) == ["email", "in_app"]
    assert len(sent) == 2
