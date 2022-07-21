from dataclasses import dataclass
from typing import Callable, Optional, Dict, Final

from typing_extensions import Self

from interfaces import Suspendable
from tap import Tap, to_keys
from util.misc import is_tuple_of, is_list_of


@dataclass(repr=False)
class TapGroup(Suspendable):
    _taps: Final[list[Tap]]
    name: Optional[str] = None
    _parent: Optional[Suspendable] = None
    _always_active: bool = False

    def __init__(self, taps: list[Tap], name: str = None) -> None:
        self._taps = taps
        self.name = name
        self.unsuspend()

    def __repr__(self) -> str:
        desc = [f"name={self.name}", f"_taps={self._taps}"]
        if self._always_active:
            desc.append(f"_always_active={self._always_active}")
        return "TapGroup(" + ",".join(desc) + ")"

    @classmethod
    def from_dict(
            cls, binds: dict[str | tuple[str], Optional[Callable | str]], name: str = None
    ) -> Self:  # type:ignore
        taps = [Tap(key, value) for (key, value) in binds.items()]
        return TapGroup(taps, name)

    def get_all(self) -> list[Tap]:
        return self._taps

    def get_by_hotkey(self, hotkey: str) -> Optional[Tap]:
        keys = to_keys(hotkey)
        try:
            return next(tap for tap in self._taps if tap.same_hotkey(keys))
        except StopIteration:
            return None

    def add(self, taps: Dict[str | tuple[str], Optional[Callable]] | Tap | tuple[Tap, ...] | list[Tap]) -> None:
        if (one := isinstance(taps, Tap)) or is_tuple_of(taps, Tap) or is_list_of(taps, Tap):
            if one:
                taps = (taps,)
        elif isinstance(taps, dict):
            taps = tuple([Tap(key, taps[key]) for key in taps])
        self._taps.extend(taps)

    def remove(self, taps: Tap | tuple[Tap] | str | tuple[str]) -> None:
        if (one := isinstance(taps, Tap)) or is_tuple_of(taps, Tap):
            if one:
                taps = (taps,)
            for tap in taps:
                self._taps.remove(tap)
            return
        elif (one := isinstance(taps, str)) or is_tuple_of(taps, str):
            if one:
                taps = (taps,)
            for tap_str in taps:
                keys = to_keys(tap_str)
                self._taps[:] = [self_tap for self_tap in self._taps if self_tap.same_hotkey(keys)]
            return
        else:
            raise TypeError

    def suspended(self) -> bool:
        return self._suspended or self._parent.suspended()
