import sys

from winadapter.base import WindowAdapterBase


def get_platform_default_adapter() -> WindowAdapterBase:
    if sys.platform.lower() == "win32":
        from winadapter.win32_native import WindowsNativeWindowAdapter

        return WindowsNativeWindowAdapter()
    else:
        raise NotImplementedError(
            f"For this platform ({sys.platform}) no window adapter exists. "
            "You can make your own, take a look at "
            "winput.winadapter package"
        )
