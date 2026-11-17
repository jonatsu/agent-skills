from tokenapi.tokens import find_token, hash_token, issue_token

NOW = "2026-01-15T12:00:00+00:00"


def test_raw_token_is_not_stored(conn):
    raw = issue_token(conn, 1, "ci", NOW)
    stored = [row["token_hash"] for row in conn.execute("SELECT token_hash FROM api_tokens")]
    assert stored == [hash_token(raw)]
    assert raw not in stored


def test_find_token_returns_record(conn):
    raw = issue_token(conn, 1, "ci", NOW)
    record = find_token(conn, raw)
    assert record is not None
    assert (record.account_id, record.label, record.revoked_at) == (1, "ci", None)
