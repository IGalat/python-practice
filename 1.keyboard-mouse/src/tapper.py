from typing import List, Final, Optional

import attrs

import adapter
from tap_group import TapGroup


def to_tap_groups(taps: TapGroup | List[TapGroup] | dict) -> Optional[List[TapGroup]]:
    if taps is None:
        return None
    if isinstance(taps, dict):
        return [TapGroup.from_dict(taps)]
    elif isinstance(taps, TapGroup):
        return [taps]
    elif isinstance(taps, list):
        return taps


@attrs.define
class Tapper:
    adapter: Optional[adapter.base.BaseAdapter | str] = None
    groups: List[TapGroup] = []
    controlGroup: Final[TapGroup] = TapGroup()  # doesn't get suspended, always active
    _suspended: bool = False

    def __init__(self, taps: TapGroup | List[TapGroup] | dict) -> None:
        """
        :param taps: TapGroup, List[TapGroup], dict {"hotkey": action}, or None
        """
        if isinstance(taps, dict):
            self.groups = [TapGroup.from_dict(taps)]
        elif isinstance(taps, TapGroup):
            self.groups = [taps]
        else:
            self.groups = taps

        self.groups.append(self.controlGroup)

    def start(self) -> None:
        self.adapter = adapter.get_adapter(self.adapter)
