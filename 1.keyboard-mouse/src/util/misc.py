from typing import List, Any, TypeGuard, TypeVar

# everything that's too small for a separate util module

T = TypeVar("T")


def is_list_of(target: Any, values_type: T) -> TypeGuard[List[T]]:
    return target is not None and isinstance(target, list) and all(type(x) == values_type for x in target)
