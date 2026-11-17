import pytest

from tokenapi import AuthError, authenticate
from tokenapi.tokens import issue_token, revoke_token

NOW = "2026-01-15T12:00:00+00:00"


def test_valid_token_authenticates(conn):
    raw = issue_token(conn, 1, "ci", NOW)
    principal = authenticate(conn, {"Authorization": f"Bearer {raw}"})
    assert principal.account_id == 1


def test_missing_header_is_rejected(conn):
    with pytest.raises(AuthError):
        authenticate(conn, {})


def test_wrong_scheme_is_rejected(conn):
    raw = issue_token(conn, 1, "ci", NOW)
    with pytest.raises(AuthError):
        authenticate(conn, {"Authorization": f"Basic {raw}"})


def test_unknown_token_is_rejected(conn):
    with pytest.raises(AuthError):
        authenticate(conn, {"Authorization": "Bearer tk_unknown"})


def test_revoked_token_is_rejected(conn):
    raw = issue_token(conn, 1, "ci", NOW)
    token_id = authenticate(conn, {"Authorization": f"Bearer {raw}"}).token_id
    revoke_token(conn, token_id, NOW)
    with pytest.raises(AuthError):
        authenticate(conn, {"Authorization": f"Bearer {raw}"})


def test_all_failures_share_one_response():
    assert AuthError.status == 401
    assert AuthError.body == {"error": "unauthorized"}
