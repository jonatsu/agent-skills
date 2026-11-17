import pytest

from catalogcheck import __version__, main


def test_version_is_a_string():
    assert isinstance(__version__, str)


def test_main_accepts_a_path():
    assert main(["catalog.json"]) == 0


def test_main_requires_a_path():
    with pytest.raises(SystemExit):
        main([])
