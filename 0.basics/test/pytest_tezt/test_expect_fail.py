import pytest


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        x = 1 / 0


# fails the test, error was not raised
def test_no_error():
    with pytest.raises(ZeroDivisionError):
        x = 1 / 2


# wraps error with pytest's ExceptionInfo
def test_recursion_depth():
    def infinite_recursion():
        infinite_recursion()

    #  RecursionError is subclass of RuntimeError, so ok
    with pytest.raises(RuntimeError) as pytest_error_wrapper:
        infinite_recursion()
    assert "maximum recursion" in str(pytest_error_wrapper.value)
    assert RecursionError == pytest_error_wrapper.type

    # traceback is stack trace, guess it's just for info
    # assert RuntimeWarning == pytest_error_wrapper.traceback


def myfunc():
    raise ValueError("Exception 123 raised")


def test_message_match_regex():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        myfunc()
    with pytest.raises(ValueError, match="123"):
        myfunc()
