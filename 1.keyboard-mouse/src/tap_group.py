from typing import List, Callable, Optional, Dict, Final

import attrs
from typing_extensions import Self

from interfaces import Suspendable
from tap import Tap, to_keys
from util.misc import is_list_of


@attrs.define
class TapGroup(Suspendable):
    _taps: Final[List[Tap]] = []

    def __init__(self, taps: List[Tap]) -> None:
        self._taps.extend(taps)

    @classmethod
    def from_dict(cls, binds: Dict[str | List[[str], Optional[Callable]]]) -> Self:  # type:ignore # todo mypy
        taps = [Tap(key, binds[key]) for key in binds]  # type:ignore # todo mypy
        return TapGroup(taps)

    def get_all(self) -> List[Tap]:
        return self._taps

    def get_by_hotkey(self, hotkey: str) -> Optional[Tap]:
        keys = to_keys(hotkey)
        try:
            return next(tap for tap in self._taps if tap.same_hotkey(keys))
        except StopIteration:
            return None

    def add(self, taps: Dict[str | List[str], Optional[Callable]] | Tap | List[Tap]) -> None:
        if one := isinstance(taps, Tap) or is_list_of(taps, Tap):
            if one:
                taps = [taps]
        elif isinstance(taps, dict):
            taps = [Tap(key, taps[key]) for key in taps]  # type:ignore # mypy wtf
        self._taps.extend(taps)

    def remove(self, taps: Tap | List[Tap] | str | List[str]) -> None:
        if one := isinstance(taps, Tap) or is_list_of(taps, Tap):
            if one:
                taps = [taps]
            for tap in taps:
                self._taps.remove(tap)
        elif one := isinstance(taps, str) or is_list_of(taps, str):
            if one:
                taps = [taps]
            for tap_str in taps:
                keys = to_keys(tap_str)
                self._taps[:] = [self_tap for self_tap in self._taps if self_tap.same_hotkey(keys)]
        else:
            raise TypeError

    # todo __init__ from Tap(s)
