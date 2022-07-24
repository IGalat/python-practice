from dataclasses import dataclass
from typing import ClassVar

import adapter
import winadapter
from adapter import BaseAdapter
from winadapter import WindowAdapterBase


@dataclass
class Config:
    adapter: ClassVar[BaseAdapter]
    winadapter: ClassVar[WindowAdapterBase]
    action_threads: ClassVar[int] = 1
    controller_interval_sec = 0

    @classmethod
    def fill_absent(cls) -> None:
        if not hasattr(cls, "adapter"):
            cls.adapter = adapter.get_platform_default_adapter()
        if not hasattr(cls, "winadapter"):
            cls.winadapter = winadapter.get_platform_default_adapter()
