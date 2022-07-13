from util.misc import is_list_of


def test_is_list_of() -> None:
    assert is_list_of(["q", "w"], str)
