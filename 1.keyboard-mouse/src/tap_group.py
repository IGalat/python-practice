from dataclasses import dataclass
from typing import Callable
from typing import Dict
from typing import Final
from typing import Optional

from interfaces import Suspendable
from tap import Tap
from tap import to_keys
from typing_extensions import Self
from util.misc import is_list_of
from util.misc import is_tuple_of


@dataclass(repr=False)
class TapGroup(Suspendable):
    _taps: Final[list[Tap]]
    trigger_if: Optional[Callable]
    name: Optional[str] = None
    _parent: Optional[Suspendable] = None
    _always_active: bool = False

    def __init__(
        self,
        taps: list[Tap],
        name: Optional[str] = None,
        trigger_if: Optional[Callable] = None,
    ) -> None:
        self._taps = taps
        self.name = name
        self.unsuspend()
        self.trigger_if = trigger_if

    def __repr__(self) -> str:
        desc = [f"name={self.name}", f"_taps={self._taps}"]
        if self._always_active:
            desc.append(f"_always_active={self._always_active}")
        return "TapGroup(" + ",".join(desc) + ")"

    @classmethod
    def from_dict(
        cls,
        binds: dict[str | tuple[str], Optional[Callable | str]],
        name: Optional[str] = None,
        trigger_if: Optional[Callable] = None,
    ) -> Self:  # type:ignore
        taps = [Tap(key, value) for (key, value) in binds.items()]
        return TapGroup(taps, name, trigger_if)

    def get_all(self) -> list[Tap]:
        return self._taps

    def get_by_hotkey(self, hotkey: str) -> Optional[Tap]:
        keys = to_keys(hotkey)
        try:
            return next(tap for tap in self._taps if tap.same_hotkey(keys))
        except StopIteration:
            return None

    def add(
        self,
        taps: list[Tap]
        | Dict[str | tuple[str], Optional[Callable]]
        | Tap
        | tuple[Tap, ...],
    ) -> None:
        if (
            (one := isinstance(taps, Tap))
            or is_tuple_of(taps, Tap)
            or is_list_of(taps, Tap)
        ):
            if one:
                taps = (taps,)
        elif isinstance(taps, dict):
            taps = tuple(Tap(key, taps[key]) for key in taps)
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
                self._taps[:] = [
                    self_tap for self_tap in self._taps if self_tap.same_hotkey(keys)
                ]
            return
        else:
            raise TypeError

    def suspended(self) -> bool:
        return bool(Suspendable.suspended(self) or self._parent.suspended())


def get_group(group: TapGroup | str, groups: list[TapGroup]) -> TapGroup:
    if isinstance(group, TapGroup):
        return group
    elif isinstance(group, str):
        found = next(gr for gr in groups if gr.name == group)
        if not found:
            raise ValueError()
        return found
    else:
        raise TypeError(f"Tried to find group with {group}, type {type(group)}")
