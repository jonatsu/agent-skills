from pathlib import Path

from syncdir.sync import sync


def test_copies_a_new_file(tmp_path: Path) -> None:
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    source.mkdir()
    (source / "a.txt").write_text("hello", encoding="utf-8")
    assert sync(source, destination) == [destination / "a.txt"]
    assert (destination / "a.txt").read_text(encoding="utf-8") == "hello"
