def test_file2_method1():
    x = 5
    y = 6
    assert x + 1 == y
    assert x == y, "test failed because x=" + str(x) + " y=" + str(y)


def test_file2_method2():
    x = 5
    y = 6
    assert x + 1 == y, "test failed"
