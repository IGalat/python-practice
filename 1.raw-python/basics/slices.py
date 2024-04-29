def sliceable_datatypes() -> None:
    # Iterables are valid for slice, so string/bytes/list/tuple/range
    assert "A slice is..."[2:7] == "slice"

    assert b"Bytez"[2:] == b"tez"

    assert list(range(0, 10))[:4] == [0, 1, 2, 3]

    # Reusable slice object
    slice__3 = slice(3)  # Here 3 is stop param, not start
    assert range(0, 10)[:3] == range(0, 10)[slice__3] == range(0, 3)

    tup_0_10 = tuple(range(0, 10))
    slice_7_ = slice(7, None)  # Here 7 is start param
    assert tup_0_10[7:] == tup_0_10[slice_7_] == (7, 8, 9)


def slice_range() -> None:
    text = "Extrapolation"
    assert text[5] == "p"  # Not a slice, just index

    assert text[:5] == "Extra"
    assert text[:-5] == "Extrapol"

    assert text[5:] == "polation"
    assert text[-5:] == "ation"

    assert text[5:-5] == "pol"

    # Any non-overlap results in empty
    assert text[10:1] == ""
    assert text[-5:5] == ""
    assert text[5:5] == ""


def slice_with_step() -> None:
    text = "Hello slice"

    reusable_reverse_slice = slice(None, None, -1)
    assert text[::-1] == text[reusable_reverse_slice] == "ecils olleH"

    assert text[::2] == "Hlosie"
    assert text[::5] == "H e"
    assert text[::-5] == "e H"

    # Step direction is considered before range. So "slice" is first and not "Hello".
    assert text[:5:-1] == "ecils"

    # But step itself is after range. So "Hello" is cut, and then stepped.
    assert text[:5:2] == "Hlo"


def main() -> None:
    sliceable_datatypes()
    slice_range()
    slice_with_step()


if __name__ == "__main__":
    main()
