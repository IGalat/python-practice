from enum import Enum
from typing import List, Optional

import attrs
from typing_extensions import Self


@attrs.define
class Key:
    vk_code: Optional[int] = None
    vk_name: Optional[str] = None
    input_variants: Optional[List[str]] = None
    alias_for: Optional[List[Self]] = None  # type:ignore # todo mypy

    def __attrs_post_init__(self) -> None:
        if self.vk_code is None and self.alias_for is None:
            raise ValueError("Must either be a key or an alias")


class Keys(Key, Enum):
    @classmethod
    def by_vk_code(cls, vk: Optional[int]) -> Optional[Key]:
        if vk is None:
            return None
        for key in cls:
            if vk == key.vk_code:
                return key
        return None

    @classmethod
    def by_str(cls, input: Optional[str]) -> Optional[Key]:
        if input is None:
            return None
        try:
            key = cls[input]
            return key
        except AttributeError:
            for key in cls:
                v = key.input_variants
                if v is not None and len(v) > 0 and input in v:
                    return key
            return None

    a = Key(65)
    b = Key(66)
    c = Key(67)
    d = Key(68)
    e = Key(69)

    left_control = Key(162, "VK_LCONTROL")
    right_control = Key(163, "VK_RCONTROL")

    # aliases
    A = a
    B = b

    lctrl = left_control
    lcontrol = left_control
    rctrl = right_control
    rcontrol = right_control

    control = Key(alias_for=[rctrl, lctrl])
    ctrl = control
