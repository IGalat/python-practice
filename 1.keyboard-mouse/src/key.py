from enum import Enum
from typing import Optional

import attrs

from util.misc import flatten_to_list


@attrs.define
class Key:
    vk_code: Optional[int] = None
    vk_name: Optional[str] = None
    input_variants: Optional[list[str]] = None
    alias_for: list["Key"] = []
    all_vk_codes: list[int] = []

    def __attrs_post_init__(self) -> None:
        if (not self.vk_code and not self.alias_for) or (self.vk_code and self.alias_for):
            raise ValueError("Must either be a key or an alias")
        self.all_vk_codes = self.collect_vk_codes()

    def get_vk_code(self) -> int:
        if self.vk_code is not None:
            return self.vk_code
        return self.alias_for[0].get_vk_code()

    def collect_vk_codes(self) -> list[int]:
        if self.vk_code:
            return [self.vk_code]
        vk_lists = [alias.collect_vk_codes() for alias in self.alias_for]
        return flatten_to_list(vk_lists)


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
                input_var = key.input_variants
                if input_var and input in input_var:
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
