from typing import Optional, ClassVar

import attrs

import adapter
from adapter import BaseAdapter
from tap_group import TapGroup


@attrs.define
class Config:
    adapter: ClassVar[Optional[BaseAdapter | str]] = None
    default_controls: ClassVar[TapGroup] = TapGroup([])  # todo fill
    action_threads: ClassVar[int] = 10

    @classmethod
    def fill_absent(cls) -> None:
        if not cls.adapter:
            adapter.get_adapter(cls.adapter)
