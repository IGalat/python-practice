import ctypes
from typing import Final
from typing import Optional

import winput
from adapter import BaseAdapter
from key import Keys
from winput import winput

WINPUT_PROPAGATE: Final[int] = 0
WINPUT_SUPPRESS: Final[int] = 4

EVENT_PRESS: Final[set[int]] = {256, 260}
EVENT_RELEASE: Final[set[int]] = {257, 261}

MOUSE_MOVE = 512
WHEEL_MOVE = 522  # additional: +X for X times up, -X for down

LMB_DOWN = 513
LMB_UP = 514
RMB_DOWN = 516
RMB_UP = 517
MMB_DOWN = 519
MMB_UP = 520
XMB_DOWN = 523  # additional: 1 for x1, 2 for x2
XMB_UP = 524

MOUSE_INPUT = {  # vks to winput's button codes
    Keys.lmb.vk_code: 1,
    Keys.mmb.vk_code: 2,
    Keys.rmb.vk_code: 4,
    Keys.x1mb.vk_code: 8,
    Keys.x2mb.vk_code: 16,
    Keys.scroll_wheel_up.vk_code: None,
    Keys.scroll_wheel_down.vk_code: None,
}

user32 = ctypes.windll.user32


class WinputAdapter(BaseAdapter):
    @classmethod
    def start(cls) -> None:
        winput.set_DPI_aware(True)
        # winput.hook_mouse(cls.mouse_callback)
        winput.hook_keyboard(cls.keyboard_callback)
        winput.wait_messages()

    @classmethod
    def stop(cls) -> None:
        winput.stop()
        winput.unhook_mouse()
        winput.unhook_keyboard()

    @classmethod
    def press_key(cls, vk_code: int) -> None:
        if vk_code in MOUSE_INPUT:
            cls.press_mouse_button(vk_code)
        winput.press_key(vk_code)

    @classmethod
    def release_key(cls, vk_code: int) -> None:
        if vk_code in MOUSE_INPUT:
            cls.release_mouse_button(vk_code)
        winput.release_key(vk_code)

    @classmethod
    def keyboard_callback(cls, event: winput.KeyboardEvent) -> Optional[int]:
        if event.action in EVENT_PRESS:
            return cls.to_callback_result(cls.on_press(event.key))
        elif event.action in EVENT_RELEASE:
            return cls.to_callback_result(cls.on_release(event.key))
        else:
            return WINPUT_PROPAGATE

    @staticmethod
    def to_callback_result(inner_func_result: bool) -> int:
        if inner_func_result:
            return WINPUT_PROPAGATE
        else:
            return WINPUT_SUPPRESS

    @classmethod
    def _pressed(cls, vk_code: int) -> bool:
        # pressed key has 16th bit at 1
        return user32.GetKeyState(vk_code) >> 15 == 1

    @classmethod
    def _toggled(cls, vk_code: int) -> bool:
        # toggled key has 1st bit at 1
        return user32.GetKeyState(vk_code) & 1 == 1

    # ugly as hell, don't care for poc
    @classmethod
    def mouse_callback(cls, event: winput.MouseEvent) -> Optional[int]:
        if (action := event.action) == MOUSE_MOVE:
            return WINPUT_PROPAGATE
        elif action == LMB_DOWN:
            return cls.to_callback_result(cls.on_press(Keys.lmb.get_vk_code()))
        elif action == LMB_UP:
            return cls.to_callback_result(cls.on_release(Keys.lmb.get_vk_code()))

        elif action == RMB_DOWN:
            return cls.to_callback_result(cls.on_press(Keys.rmb.get_vk_code()))
        elif action == RMB_UP:
            return cls.to_callback_result(cls.on_release(Keys.rmb.get_vk_code()))

        elif action == MMB_DOWN:
            return cls.to_callback_result(cls.on_press(Keys.mmb.get_vk_code()))
        elif action == MMB_UP:
            return cls.to_callback_result(cls.on_release(Keys.mmb.get_vk_code()))

        elif action == WHEEL_MOVE:
            if event.additional_data > 0:
                return cls.to_callback_result(cls.on_press(Keys.wheel_up.get_vk_code()))
            else:
                return cls.to_callback_result(
                    cls.on_press(Keys.wheel_down.get_vk_code())
                )

        elif action == XMB_DOWN:
            xmb = Keys.x1mb if event.additional_data == 1 else Keys.x2mb
            return cls.to_callback_result(cls.on_press(xmb.get_vk_code()))
        elif action == XMB_UP:
            xmb = Keys.x1mb if event.additional_data == 1 else Keys.x2mb
            return cls.to_callback_result(cls.on_release(xmb.get_vk_code()))
        else:
            raise ValueError(f"UNKNOWN EVENT IN WINPUT ADAPTER: {action}")

    @classmethod
    def _press_mouse_button(cls, vk_code: int) -> None:
        winput.press_mouse_button(MOUSE_INPUT[vk_code])

    @classmethod
    def release_mouse_button(cls, vk_code: int) -> None:
        winput.release_mouse_button(MOUSE_INPUT[vk_code])

    @classmethod
    def move_mousewheel(cls, times: int) -> None:
        winput.move_mousewheel(times)

    @classmethod
    def move_mouse(cls, dx: int, dy: int) -> None:
        winput.move_mouse(dx, dy)

    @classmethod
    def set_mouse_pos(cls, x: int, y: int) -> None:
        winput.set_mouse_pos(x, y)

    @classmethod
    def get_mouse_pos(cls) -> tuple[int, int]:
        return winput.get_mouse_pos()
