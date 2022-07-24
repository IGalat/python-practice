import ctypes
import ctypes.wintypes
import time

import win32con
import win32gui

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
kernel32 = ctypes.windll.kernel32

processFlag = getattr(win32con, "PROCESS_QUERY_LIMITED_INFORMATION", win32con.PROCESS_QUERY_INFORMATION)
threadFlag = getattr(win32con, "THREAD_QUERY_LIMITED_INFORMATION", win32con.THREAD_QUERY_INFORMATION)


def getProcessID(hwnd):
    if hwnd:
        process_id = ctypes.wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
        if process_id:
            process_id = process_id.value
        else:
            process_id = None
    else:
        process_id = None

    return process_id


def getProcessFilename(processID):
    h_process = kernel32.OpenProcess(processFlag, 0, processID)
    if not h_process:
        return None

    try:
        filename_buffer_size = ctypes.wintypes.DWORD(4096)
        filename = ctypes.create_unicode_buffer(filename_buffer_size.value)
        kernel32.QueryFullProcessImageNameW(h_process, 0, ctypes.byref(filename), ctypes.byref(filename_buffer_size))
        return filename.value
    finally:
        kernel32.CloseHandle(h_process)


def get_win_info(hwnd) -> tuple:
    if win32gui.IsWindowVisible(hwnd):
        text = win32gui.GetWindowText(hwnd)
        if text:
            pid = getProcessID(hwnd)
            filename = getProcessFilename(pid)
            exec = "\\".join(filename.rsplit("\\", 2)[-1:])
            return hwnd, pid, exec, text


def print_win_info(hwnd, pid, exec, text) -> None:
    print(f"{hwnd:<10} {pid:<8}, {exec= :<20}, {text= }")


windows = []


def winEnumPrint(hwnd, ctx):
    global windows
    info = get_win_info(hwnd)
    if not info:
        return
    hwnd, pid, exec, text = info
    print_win_info(hwnd, pid, exec, text)
    windows.append((hwnd, pid, exec, text))


def set_fore_win(name_or_exec: str) -> None:
    global windows
    for win in windows:
        if name_or_exec in win[2] or name_or_exec in win[3]:
            print(f"trying to set fore {win[0]= }")
            win32gui.SetForegroundWindow(win[0])
            return


time.sleep(1)

win32gui.EnumWindows(winEnumPrint, None)

curr_window = win32gui.GetForegroundWindow()
print("\n Fore window:")
get_win_info(curr_window)

set_fore_win("foobar")
