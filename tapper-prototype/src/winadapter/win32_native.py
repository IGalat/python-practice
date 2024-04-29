import ctypes.wintypes
from typing import Any
from typing import ClassVar
from typing import Optional

import win32con
import win32gui
from winadapter import WindowAdapterBase
from winadapter.base import Window

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
kernel32 = ctypes.windll.kernel32

processFlag = getattr(
    win32con, "PROCESS_QUERY_LIMITED_INFORMATION", win32con.PROCESS_QUERY_INFORMATION
)


def get_pid(hwnd: Any) -> Optional[int]:
    process_id = None
    if hwnd:
        ulong = ctypes.wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(ulong))
        if ulong:
            process_id = int(ulong.value)
    return process_id


def get_process_exec(pid: Optional[int]) -> Optional[str]:
    h_process = kernel32.OpenProcess(processFlag, 0, pid)
    if not h_process:
        return None
    try:
        filename_buffer_size = ctypes.wintypes.DWORD(4096)
        filename = ctypes.create_unicode_buffer(filename_buffer_size.value)
        kernel32.QueryFullProcessImageNameW(
            h_process, 0, ctypes.byref(filename), ctypes.byref(filename_buffer_size)
        )
        return filename.value
    finally:
        kernel32.CloseHandle(h_process)


def to_window(hwnd: Any) -> Optional[Window]:
    if win32gui.IsWindowVisible(hwnd):
        text = win32gui.GetWindowText(hwnd)
        if text:
            pid = get_pid(hwnd)
            filename = get_process_exec(pid)
            if not filename:
                return None
            exec = "\\".join(filename.rsplit("\\", 2)[-1:])
            return Window(hwnd, pid, exec, text)
    return None


def win_filter(
    win: Optional[Window],
    exec_or_title: Optional[str] = None,
    handle: Any = None,
    pid: Optional[int] = None,
    exec: Optional[str] = None,
    title: Optional[str] = None,
) -> Optional[Window]:
    if not win:
        return None
    if handle and win.handle != handle:
        return None
    if pid and win.pid != pid:
        return None
    if (
        exec_or_title
        and exec_or_title not in win.exec
        and exec_or_title not in win.title
    ):
        return None
    if exec and exec not in win.exec:
        return None
    if title and title not in win.title:
        return None
    return win


class WindowsNativeWindowAdapter(WindowAdapterBase):
    win_handles: ClassVar[Any] = []  # have to make this shared because of EnumWindows

    @classmethod
    def start(cls) -> None:
        pass

    @classmethod
    def stop(cls) -> None:
        pass

    @staticmethod
    def _collect_handle_callback(hwnd: Any, ctx: Any) -> None:
        WindowsNativeWindowAdapter.win_handles.append(hwnd)

    @classmethod
    def get_open(
        cls,
        exec_or_title: Optional[str] = None,
        *,
        handle: Any = None,
        pid: Optional[int] = None,
        exec: Optional[str] = None,
        title: Optional[str] = None
    ) -> list[Window]:
        cls.win_handles = []
        win32gui.EnumWindows(cls._collect_handle_callback, None)
        window_list = [to_window(hwnd) for hwnd in cls.win_handles]
        result = []
        for win in window_list:
            if win_filter(win, exec_or_title, handle, pid, exec, title):
                result.append(win)
        return result

    @classmethod
    def get_fore(
        cls,
        exec_or_title: Optional[str] = None,
        *,
        handle: Any = None,
        pid: Optional[int] = None,
        exec: Optional[str] = None,
        title: Optional[str] = None
    ) -> Optional[Window]:
        fore = win32gui.GetForegroundWindow()
        fore = to_window(fore)
        return win_filter(fore, exec_or_title, handle, pid, exec, title)

    @classmethod
    def set_fore(
        cls,
        exec_or_title: Optional[str] = None,
        *,
        handle: Any = None,
        pid: Optional[int] = None,
        exec: Optional[str] = None,
        title: Optional[str] = None
    ) -> bool:
        if not handle and not exec_or_title and not exec and not title:
            raise ValueError("Tried to set window to fore without args")
        if handle:
            return win32gui.SetForegroundWindow(handle)
        open = cls.get_open(
            exec_or_title, handle=handle, pid=pid, exec=exec, title=title
        )
        if not open:
            return False
        return win32gui.SetForegroundWindow(open[0].handle)
