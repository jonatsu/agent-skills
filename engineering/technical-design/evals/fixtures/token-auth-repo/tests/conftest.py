import pytest

from tokenapi.db import connect, migrate

NOW = "2026-01-15T12:00:00+00:00"


@pytest.fixture
def conn():
    connection = connect(":memory:")
    migrate(connection)
    connection.execute("INSERT INTO accounts (name, created_at) VALUES ('acme', ?)", (NOW,))
    connection.commit()
    yield connection
    connection.close()
