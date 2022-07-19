from dataclasses import dataclass
from typing import ClassVar

import adapter
from adapter import BaseAdapter
from tap_group import TapGroup


@dataclass
class Config:
    adapter: ClassVar[BaseAdapter]
    default_controls: ClassVar[TapGroup] = TapGroup([])  # todo fill
    action_threads: ClassVar[int] = 10

    @classmethod
    def fill_absent(cls) -> None:
        if not hasattr(cls, "adapter"):
            cls.adapter = adapter.get_platform_default_adapter()
