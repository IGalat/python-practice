from dataclasses import dataclass, field
from typing import Optional, ClassVar

from util.misc import flatten_to_list


@dataclass(repr=False)
class Key:
    vk_code: Optional[int] = None
    vk_name: Optional[str] = None
    input_variants: Optional[list[str]] = None
    alias_for: list["Key"] = field(default_factory=list)
    all_vk_codes: list[int] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if not self.vk_code and not self.alias_for:
            raise ValueError("Must either be a key or an alias")
        self.all_vk_codes = self.collect_vk_codes()

    def __repr__(self) -> str:
        desc = []
        if self.vk_code:
            desc.append(f"{self.vk_code}")
        if self.vk_name:
            desc.append(f"{self.vk_name}")
        if self.input_variants:
            desc.append("input_variants={self.input_variants}")
        if self.alias_for:
            desc.append(f"alias_for={self.alias_for}")
        return "Key(" + ",".join(desc) + ")"

    def get_vk_code(self) -> int:
        if self.vk_code is not None:
            return self.vk_code
        return self.alias_for[0].get_vk_code()

    def collect_vk_codes(self) -> list[int]:
        vk_lists = []
        if self.vk_code:
            vk_lists = [self.vk_code]
        if self.alias_for:
            vk_lists.extend(flatten_to_list([alias.collect_vk_codes() for alias in self.alias_for]))
        return vk_lists


@dataclass
class Keys:
    _all: ClassVar[dict]

    @classmethod
    def all(cls) -> dict:
        try:
            return cls._all
        except AttributeError:
            cls._fill_all()
        return cls._all

    @classmethod
    def _fill_all(cls) -> None:
        def is_key(name: str) -> bool:
            return not name.startswith("_") and not callable(getattr(cls, name))

        cls._all = {name: value for (name, value) in vars(cls).items() if is_key(name)}

    @classmethod
    def by_vk_code(cls, vk: Optional[int]) -> Optional[Key]:
        if vk is None:
            return None
        for key in cls.all():
            if vk == key.vk_code:
                return key
        return None

    @classmethod
    def by_str(cls, input: Optional[str]) -> Optional[Key]:
        if input is None:
            return None
        try:
            key = cls.all()[input]
            return key
        except AttributeError:
            for key in cls.all():
                input_variants = key.input_variants
                if input_variants and input in input_variants:
                    return key
            return None

    escape = Key(27, "VK_ESCAPE")

    a = Key(65)
    b = Key(66)
    c = Key(67)
    d = Key(68)
    e = Key(69)

    left_control = Key(162, "VK_LCONTROL")
    right_control = Key(163, "VK_RCONTROL")

    control = Key(17, alias_for=[left_control, right_control])

    # aliases
    esc = escape

    A = a
    B = b
    C = c

    lctrl = left_control
    lcontrol = left_control
    rctrl = right_control
    rcontrol = right_control
    ctrl = control
