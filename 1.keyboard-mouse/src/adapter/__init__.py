import sys
from typing import Callable

from adapter.base import BaseAdapter


def _winput_adapter() -> BaseAdapter:
    from adapter.winput import WinputAdapter

    return WinputAdapter()


def _pynput_adapter() -> BaseAdapter:
    from adapter.pynput import PynpytAdapter

    return PynpytAdapter()


def _default_adapter() -> BaseAdapter:
    from adapter.winput import WinputAdapter

    return WinputAdapter()


adapter_names: dict[str, Callable[[], BaseAdapter]] = {
    "winput": _winput_adapter,
}


def _get_adapter(adapter: str | BaseAdapter | None) -> BaseAdapter:
    if adapter is None:
        if sys.platform == "Win32":
            return _winput_adapter()
        else:
            raise NotImplementedError(
                "For this platform no low-level adapter exists. "
                "You can make your own, take a look at "
                "winput.adapter package"
            )

    if isinstance(adapter, str):
        return adapter_names[adapter]()

    assert not True, f"Internal func. Should never be called with type {type(adapter)}, {adapter}"
