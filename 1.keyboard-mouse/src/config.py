from typing import Optional, ClassVar

import attrs

from adapter import BaseAdapter
from tap_group import TapGroup


@attrs.define
class Config:
    adapter: ClassVar[Optional[BaseAdapter]] = None
    default_controls: ClassVar[TapGroup] = TapGroup()  # todo fill

    @staticmethod
    def fill_defaults() -> None:
        """
        Fills absent configurations. Called before Tapper start usually
        """

