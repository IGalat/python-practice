def pop_use() -> None:
    user = {"name": "martha", "age": 30, "hair": "black"}
    print(user.pop("hair"))
    print(user)
    print(f"locals = {locals()}")


def locals_with_pop(name: str, age: int) -> None:
    x = 1
    y = 2
    result = locals()
    result.pop("x")
    print(result)


if __name__ == "__main__":
    pop_use()
    print()
    locals_with_pop(name="vasya", age=111)
