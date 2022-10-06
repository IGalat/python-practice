def fn1(x: int, *args, name: str, **kwargs) -> None:
    print(f"{x = } | {args = } | {name = } | {kwargs = }")


def fn2(*args, **kwargs) -> None:
    if args:
        x = args[0]
        args = args[1:]
    else:
        x = None
    name = kwargs.pop("name", None)
    fn1(x, *args, name=name, **kwargs)


fn1(1, 98, 76, name="Vasya", j="k")

fn1(1, j="k", name="Vasya")

fn2(1, 2, 3, name="Joe", q="w")

fn2(z="x")

fn2(5, z="x")
