from typing import List, Any, TypeGuard, TypeVar, Dict, Iterable, Callable, Optional

# everything that's too small for a separate util module

T = TypeVar("T")


def is_list_of(target: Any, values_type: T) -> TypeGuard[list[T]]:
    return target is not None and isinstance(target, list) and all(type(x) == values_type for x in target)


def is_tuple_of(target: Any, values_type: T) -> TypeGuard[list[T]]:
    return target is not None and isinstance(target, tuple) and all(type(x) == values_type for x in target)


def enum_to_list(data_structure: Iterable) -> List:
    return list(map(lambda c: c.value, data_structure))


def enum_to_dict(data_structure: Iterable) -> Dict[str, Any]:
    return dict(map(lambda c: (c.name, c.value), data_structure))


def flatten_to_list(data_structure: Iterable) -> list:
    return [item for sublist in data_structure for item in sublist]


def func_repr(func: Optional[Callable]) -> str:
    if not func:
        return ""
    if not callable(func):
        return str(func)
    return f'{str(func).partition(" at")[0]}>'
