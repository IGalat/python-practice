from typing import List, Any, TypeGuard, TypeVar

# everything that's too small for a separate util module

T = TypeVar("T")


def is_list_of(target: Any, _type: T) -> TypeGuard[List[T]]:
    return target is not None and isinstance(target, list) and all(type(x) == _type for x in target)
