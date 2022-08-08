from collections.abc import Sequence
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import TypeGuard
from typing import TypeVar

# everything that's too small for a separate util module

T = TypeVar("T")


# noinspection PyTypeHints
def is_list_of(target: Any, values_type: T) -> TypeGuard[list[T]]:
    return (
        target is not None
        and isinstance(target, list)
        and all(isinstance(x, values_type) for x in target)  # type: ignore
    )


# noinspection PyTypeHints
def is_tuple_of(target: Any, values_type: T) -> TypeGuard[list[T]]:
    return (
        target is not None
        and isinstance(target, tuple)
        and all(isinstance(x, values_type) for x in target)  # type: ignore
    )


def enum_to_list(data_structure: Iterable) -> List:
    return list(map(lambda c: c.value, data_structure))


def enum_to_dict(data_structure: Iterable) -> Dict[str, Any]:
    return dict(map(lambda c: (c.name, c.value), data_structure))


def flatten_to_list(data_structure: Sequence) -> list:
    return list(flatten(data_structure))


def flatten(xs: Sequence) -> Iterable:
    if isinstance(xs, Sequence) and not isinstance(xs, (str, bytes)):
        for x in xs:
            if isinstance(x, Sequence) and not isinstance(x, (str, bytes)):
                yield from flatten(x)
            else:
                yield x
    else:
        yield xs


def func_repr(func: Optional[Callable]) -> str:
    if not func:
        return ""
    if not callable(func):
        return str(func)
    return f'{str(func).partition(" at")[0]}>'
