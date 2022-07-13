from typing import List, Callable, Optional, Dict

import attrs
from typing_extensions import Self

from tap import Tap


@attrs.define
class TapGroup:
    taps: List[Tap] = []
    _suspended: bool = False

    @classmethod
    def from_dict(cls, binds: Dict[str | List[str], Optional[Callable]]) -> Self:  # type:ignore # todo mypy
        taps = [Tap(key, binds[key]) for key in binds]  # type:ignore # todo mypy
        return TapGroup(taps)
