import pytest


@pytest.mark.parametrize(
    "input1, input2, output",
    [(5, 5, 10), (3, 5, 12), ("first", "second", "firstsecond")],
)
def test_add(input1, input2, output):
    assert input1 + input2 == output
