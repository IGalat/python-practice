from dataclasses import dataclass
from typing import Final, Optional

from config import Config
from interfaces import Suspendable, SingletonMeta
from tap_group import TapGroup
from util.misc import is_list_of


def to_tap_groups(taps: TapGroup | list[TapGroup] | dict) -> Optional[list[TapGroup]]:
    if taps is None:
        return None
    if isinstance(taps, dict):
        return [TapGroup.from_dict(taps)]
    elif isinstance(taps, TapGroup):
        return [taps]
    elif isinstance(taps, list) and is_list_of(taps, TapGroup):
        return taps
    else:
        raise TypeError(f"taps is {type(taps)}")


@dataclass
class Tapper(Suspendable, metaclass=SingletonMeta):
    groups: Final[list[TapGroup]]
    """
    in order of precedence. Add more global groups last
    """

    controlGroup: Final[TapGroup] = TapGroup([])  # doesn't get suspended, always active

    def __init__(self, taps: TapGroup | list[TapGroup] | dict | None = None):
        """
        :param taps: TapGroup, list[TapGroup], dict {"hotkey": action}, or None
        """
        self.groups = [self.controlGroup]
        self.controlGroup._always_active = True

        self.unsuspend()

        if not taps:
            return
        if isinstance(taps, dict):
            self.groups.append(TapGroup.from_dict(taps))
        elif one := isinstance(taps, TapGroup) or is_list_of(taps, TapGroup):
            if one:
                taps = [taps]
            self.groups.extend(taps)
        else:
            raise TypeError

    def start(self, default_controls: bool = True) -> None:  # todo
        """
        :param default_controls: If you didn't add anything to controlGroup,
        this will fill default controls for you, to suspend/reload/exit script.

        """
        Config.fill_absent()

        if default_controls and not self.controlGroup:
            self.controlGroup.add(Config.default_controls.get_all())

        for group in self.groups:
            group._parent = self
            for tap in group.get_all():
                tap._parent = group

    def get_groups(self) -> list[TapGroup]:
        return self.groups

    def remove_groups(self, groups: list[TapGroup] | TapGroup) -> None:
        groups = to_tap_groups(groups)
        self.groups[:] = [gr for gr in self.groups if gr not in groups]

    def add_groups(self, groups: list[TapGroup] | TapGroup) -> None:
        correct_groups = to_tap_groups(groups)
        self.groups.extend(correct_groups)
