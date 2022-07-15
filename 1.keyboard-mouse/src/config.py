from typing import Optional

import attrs

from adapter import BaseAdapter
from tap_group import TapGroup


@attrs.define
class Config:
    adapter: Optional[BaseAdapter] = None
    default_controls: TapGroup = TapGroup()  # todo fill
