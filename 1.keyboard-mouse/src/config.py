from dataclasses import dataclass
from typing import ClassVar

import adapter
from adapter import BaseAdapter


@dataclass
class Config:
    adapter: ClassVar[BaseAdapter]
    action_threads: ClassVar[int] = 1
    controller_interval_sec = 0

    @classmethod
    def fill_absent(cls) -> None:
        if not hasattr(cls, "adapter"):
            cls.adapter = adapter.get_platform_default_adapter()
