import random
import time


def main() -> None:
    SAMPLE_SIZE = 10_000_000
    ints = [random.randint(-(10**20), 10**20) for _ in range(SAMPLE_SIZE)]
    strs = [str(int_) for int_ in ints]

    start = time.perf_counter()
    for i in range(SAMPLE_SIZE - 1):
        result = strs[i] == strs[i + 1]
    between = time.perf_counter()
    for i in range(SAMPLE_SIZE - 1):
        result = ints[i] == ints[i + 1]
    after = time.perf_counter()

    print(f"1st time:{between - start:.5f} ; 2nd time: {after - between:.5f}")


if __name__ == "__main__":
    main()
