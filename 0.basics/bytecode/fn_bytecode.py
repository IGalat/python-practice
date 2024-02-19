from typing import Callable


def compare_bytecode(fn1: Callable, fn2: Callable) -> None:
    print(
        f"co_code '{fn1.__code__.co_code}' vs '{fn2.__code__.co_code}', {fn1.__code__.co_code == fn2.__code__.co_code}"
    )
    print(
        f"co_code '{fn1.__code__.co_consts}' vs '{fn2.__code__.co_consts}', {fn1.__code__.co_consts == fn2.__code__.co_consts}"
    )
    print(
        f"co_code '{fn1.__code__.co_stacksize}' vs '{fn2.__code__.co_stacksize}', {fn1.__code__.co_stacksize == fn2.__code__.co_stacksize}"
    )
    print(
        f"co_code '{fn1.__code__.co_varnames}' vs '{fn2.__code__.co_varnames}', {fn1.__code__.co_varnames == fn2.__code__.co_varnames}"
    )
    print(
        f"co_code '{fn1.__code__.co_flags}' vs '{fn2.__code__.co_flags}', {fn1.__code__.co_flags == fn2.__code__.co_flags}"
    )
    print(
        f"co_code '{fn1.__code__.co_name}' vs '{fn2.__code__.co_name}', {fn1.__code__.co_name == fn2.__code__.co_name}"
    )
    print(
        f"co_code '{fn1.__code__.co_names}' vs '{fn2.__code__.co_names}', {fn1.__code__.co_names == fn2.__code__.co_names}"
    )


def main() -> None:
    compare_bytecode(lambda x: x + 1, lambda x: x + 2)


if __name__ == "__main__":
    main()
