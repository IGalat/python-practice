from enum import Enum
from typing import List, Optional

import attrs
from typing_extensions import Self


@attrs.define
class Key:
    vk_code: Optional[int] = None
    vk_constant: Optional[str] = None
    input_variants: Optional[str] = None
    alias_for: Optional[List[Self]] = None  # type:ignore # todo mypy

    def __attrs_post_init__(self) -> None:
        if self.vk_code is None and self.alias_for is None:
            raise ValueError("Must either be a key or an alias")


class Keys(Key, Enum):
    a = Key(65)
    b = Key(66)

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
