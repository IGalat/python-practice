import ctypes

import winput

user32 = ctypes.windll.user32

MOUSE_MOVE = 512
WHEEL_MOVE = 522


def mouse_callback(event: winput.MouseEvent) -> None:
    if event.action == MOUSE_MOVE:
        return
    lmb = user32.GetKeyState(1)
    print(f"KB: lmb={lmb} toggle={lmb >> 15}")


def keyboard_callback(event: winput.KeyboardEvent) -> None:
    caps = user32.GetKeyState(winput.VK_CAPITAL)
    a = user32.GetKeyState(winput.VK_A)
    print(f"KB: CAPS={caps >> 15 == 1} toggle={caps & 1 == 1}, a={a} toggle={a & 1}")

    if event.vkCode == winput.VK_F2:
        winput.stop()


# hook input
winput.hook_mouse(mouse_callback)
winput.hook_keyboard(keyboard_callback)

# enter message loop
winput.wait_messages()

# remove input hook
winput.unhook_mouse()
winput.unhook_keyboard()
