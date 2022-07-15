from typing import List, Any, TypeGuard, TypeVar, Dict, Iterable

# everything that's too small for a separate util module

T = TypeVar("T")


def is_list_of(target: Any, values_type: T) -> TypeGuard[List[T]]:
    return target is not None and isinstance(target, list) and all(type(x) == values_type for x in target)


def enum_to_list(clazz: Iterable) -> List:
    return list(map(lambda c: c.value, clazz))


def enum_to_dict(clazz: Iterable) -> Dict[str, Any]:
    return dict(map(lambda c: (c.name, c.value), clazz))
