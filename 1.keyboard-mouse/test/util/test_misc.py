from typing import Any, Type

import hypothesis.strategies as st
from hypothesis import given, example
from hypothesis.strategies import lists

from util.misc import is_list_of, flatten_to_list


@given(lists(st.characters()) | lists(st.dates()) | lists(st.integers()))
@example(["mixed list", 2])
@example((123, "what about tuple?"))
@example({"some dict too": 456})
def test_hypoDataStructures_is_list_of(input: Any) -> None:
    tru = type(input) == list and (not input or type(input[0]) == int)
    helper_is_list_of(input, int, tru)


@given(st.characters() | st.dates() | st.integers())
def test_hypoPrimitives_is_list_of(input: Any) -> None:
    helper_is_list_of(input, int, False)


def helper_is_list_of(input: Any, type_: Type, tru: bool) -> None:
    if tru:
        assert is_list_of(input, type_)
    else:
        assert not is_list_of(input, type_)


@given(st.dates() | lists(st.dates() | lists(st.dates() | lists(st.dates()))))
def test_flatten_to_list(input: list) -> None:
    flat = flatten_to_list(input)
    assert isinstance(flat, list)
    assert not any(isinstance(item, list) for item in flat)
