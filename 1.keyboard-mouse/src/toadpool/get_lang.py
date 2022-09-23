import ctypes.wintypes
from typing import Any

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
kernel32 = ctypes.windll.kernel32


def bit_slice(value: Any, start: None | int = None, end: None | int = None) -> int:
    return int(bin(value)[start:end], 2)


def main() -> None:
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)

    locale_id = user32.GetKeyboardLayout(thread_id) & (2**16 - 1)
    # locale id = 1024 * sub_language id  +  primary language id.
    # en-US   sub lang - prim lang
    # https://docs.microsoft.com/en-us/openspecs/office_standards/ms-oe376/6c085406-a698-4e12-9d4d-c3b0ee3dbc4a
    print(f"{locale_id = }, sub lang {locale_id % 1024}, prim lang {locale_id // 1024}")


if __name__ == "__main__":
    main()
