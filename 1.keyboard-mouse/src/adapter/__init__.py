import sys

from adapter.base import BaseAdapter


def get_platform_default_adapter() -> BaseAdapter:
    if sys.platform.lower() == "win32":
        from adapter.winput import WinputAdapter

        return WinputAdapter()
    else:
        raise NotImplementedError(
            f"For this platform ({sys.platform}) no low-level adapter exists. "
            "You can make your own, take a look at "
            "winput.adapter package"
        )
