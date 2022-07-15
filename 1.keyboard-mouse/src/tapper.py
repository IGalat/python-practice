from typing import Final, Optional

import attrs

from config import Config
from interfaces import Suspendable
from tap_group import TapGroup
from util.misc import is_list_of


def to_tap_groups(taps: TapGroup | list[TapGroup] | dict) -> Optional[list[TapGroup]]:
    if taps is None:
        return None
    if isinstance(taps, dict):
        return [TapGroup.from_dict(taps)]
    elif isinstance(taps, TapGroup):
        return [taps]
    elif isinstance(taps, list):
        return taps


@attrs.define
class Tapper(Suspendable):
    config: Final[Config] = Config()
    groups: Final[list[TapGroup]] = []
    controlGroup: Final[TapGroup] = TapGroup()  # doesn't get suspended, always active

    def __init__(self, taps: TapGroup | list[TapGroup] | dict) -> None:
        """
        :param taps: TapGroup, list[TapGroup], dict {"hotkey": action}, or None
        """
        if isinstance(taps, dict):
            self.groups.append(TapGroup.from_dict(taps))
        elif one := isinstance(taps, TapGroup) or is_list_of(taps, TapGroup):
            if one:
                taps = [taps]
            self.groups.extend(taps)
        else:
            raise TypeError

        self.groups.append(self.controlGroup)

    def start(self, default_controls: bool = True) -> None:  # todo
        """
        :param default_controls: If you didn't add anything to controlGroup,
        this will fill default controls for you, to suspend/reload/exit script.

        """
        if default_controls and not self.controlGroup:
            self.controlGroup.add(*self.config.default_controls.get_all())

    def get_groups(self) -> list[TapGroup]:
        return self.groups


# todo add, remove, get group(s)
