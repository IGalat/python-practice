from typing import Any, Type

import hypothesis.strategies as st
from hypothesis import given, example
from hypothesis.strategies import lists

from util.misc import is_list_of


@given(lists(st.characters()) | lists(st.dates()) | lists(st.integers()))
@example(["q", 2])
def test_hypo_OneTypeLists_is_list_of(input: Any) -> None:
    tru = len(input) == 0 or type(input[0]) == int
    helper_is_list_of(input, int, tru)


@given(st.characters() | st.dates() | st.integers())
def test_hypo_primitives_is_list_of(input: Any) -> None:
    helper_is_list_of(input, int, False)


def helper_is_list_of(input: Any, type_: Type, tru: bool) -> None:
    if tru:
        assert is_list_of(input, type_)
    else:
        assert not is_list_of(input, type_)
