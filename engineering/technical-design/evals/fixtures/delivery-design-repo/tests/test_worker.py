from delivery import store
from delivery.worker import Worker

NOW = "2026-02-01T10:00:00+00:00"


def make_conn():
    conn = store.connect(":memory:")
    store.add_message(conn, "m1", "https://hooks.example.com/a", "{}", NOW)
    return conn


def status_of(conn, message_id):
    return conn.execute(
        "SELECT status, attempts FROM messages WHERE id = ?", (message_id,)
    ).fetchone()


def test_success_marks_delivered_and_sends_the_message_id():
    conn = make_conn()
    seen = []

    def send(endpoint, body, key):
        seen.append(key)
        return 204

    assert Worker(conn, send, "w1").run_once(NOW)
    assert seen == ["m1"]
    assert tuple(status_of(conn, "m1")) == ("delivered", 1)


def test_failure_returns_the_message_to_pending_until_five_attempts():
    conn = make_conn()
    worker = Worker(conn, lambda *_: 503, "w1")
    for _ in range(4):
        worker.run_once(NOW)
    assert tuple(status_of(conn, "m1")) == ("pending", 4)
    worker.run_once(NOW)
    assert tuple(status_of(conn, "m1")) == ("failed", 5)


def test_no_pending_message_returns_false():
    conn = store.connect(":memory:")
    assert Worker(conn, lambda *_: 200, "w1").run_once(NOW) is False
