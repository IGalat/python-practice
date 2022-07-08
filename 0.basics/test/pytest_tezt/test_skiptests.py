import sys

import pytest

from pytest_tezt.conftest import external_conditional_skip_marker


# skip = never execute, gray "no" sign in idea for test.
@pytest.mark.skip
def test_add_1():
    assert 100 + 200 == 400


@pytest.mark.skip(reason="here could be your reason!")
def test_add_2():
    assert 100 + 200 == 300


# xfail = if OK, green checkmark; if fail, gray "no" sign. Silly, won't use
@pytest.mark.xfail
def test_add_3():
    assert 15 + 13 == 28


@pytest.mark.xfail
def test_add_4():
    assert 15 + 13 == 100


# conditional skip. noice
@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def test_add_5():
    assert 3 + 2 == 5


# good idea to have one file where you define the markers
# which you then consistently apply throughout your test suite.
# has to be imported manually, unlike test fixtures from conftest
my_conditional_skip_marker = pytest.mark.skipif(
    sys.platform == "linux", reason="does not run on linux"
)


# If multiple skipif decorators are applied to a test function,
# it will be skipped if any of the skip conditions is true.
@my_conditional_skip_marker
def test_add_6():
    assert 3 + 2 == 6


@external_conditional_skip_marker
def test_add_7():
    assert 3 + 2 == 7
