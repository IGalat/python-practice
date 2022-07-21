from dataclasses import dataclass
from typing import Final

from config import Config
from interfaces import Suspendable, SingletonMeta
from tap import Tap
from tap_group import TapGroup
from util.misc import is_list_of, flatten_to_list
from util.tap_control import TapControl


def to_tap_groups(taps: TapGroup | list[TapGroup] | dict) -> list[TapGroup]:
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

    controlGroup: Final[TapGroup] = TapGroup([], "CONTROL_GROUP")  # doesn't get suspended, always active

    default_controls: TapGroup = TapGroup(
        [Tap("ctrl+f2", TapControl.restart_script), Tap("f2", TapControl.terminate_script)]
    )

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
            g = to_tap_groups(taps)
            g[0].name = "generic"
            self.groups.extend(g)
        elif isinstance(taps, TapGroup) or is_list_of(taps, TapGroup):
            taps = flatten_to_list([taps])
            self.groups.extend(taps)
        else:
            raise TypeError

    def start(self, default_controls: bool = True) -> None:
        """
        :param default_controls: If you didn't add anything to controlGroup,
        this will fill default controls for you, to suspend/reload/exit script.

        """
        self._pre_start(default_controls)
        Config.adapter.start()

    def _pre_start(self, default_controls: bool) -> None:
        Config.fill_absent()

        if default_controls and not self.controlGroup.get_all():
            self.controlGroup.add(self.default_controls.get_all())

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
