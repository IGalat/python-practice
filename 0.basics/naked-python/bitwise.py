def last_bit_is_1(x: int) -> None:
    print(f"Last bit of {x} is 1? {x & 1}")


[last_bit_is_1(x) for x in range(10)]
