from tokenapi.db import connect, migrate


def test_migrations_apply_once_in_order():
    conn = connect(":memory:")
    first = migrate(conn)
    assert first == ["0001_create_accounts.sql", "0002_create_api_tokens.sql"]
    assert migrate(conn) == []


def test_api_tokens_table_exists_after_migration():
    conn = connect(":memory:")
    migrate(conn)
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(api_tokens)")}
    assert {"token_hash", "revoked_at"} <= columns
