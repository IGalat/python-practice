from typing import Final, Optional

from winput import winput

from adapter import BaseAdapter


class WinputAdapter(BaseAdapter):
    WINPUT_PROPAGATE: Final[int] = 0
    WINPUT_SUPPRESS: Final[int] = 4

    EVENT_PRESS: Final[set[int]] = {256, 260}
    EVENT_RELEASE: Final[set[int]] = {257, 261}

    @classmethod
    def start(cls) -> None:
        # winput.hook_mouse(mouse_callback)
        winput.hook_keyboard(WinputAdapter.keyboard_callback)
        winput.wait_messages()

    @classmethod
    def stop(cls) -> None:
        winput.stop()
        # winput.unhook_mouse()
        winput.unhook_keyboard()

    @classmethod
    def press_key(cls) -> None:
        pass

    @classmethod
    def release_key(cls) -> None:
        pass

    @classmethod
    def keyboard_callback(cls, event: winput.KeyboardEvent) -> Optional[int]:
        if event.action in cls.EVENT_PRESS:
            return cls.to_callback_result(cls.on_press(event.key))
        elif event.action in cls.EVENT_RELEASE:
            return cls.to_callback_result(cls.on_release(event.key))
        else:
            return WinputAdapter.WINPUT_PROPAGATE

    @staticmethod
    def to_callback_result(inner_func_result: bool) -> int:
        if inner_func_result:
            return WinputAdapter.WINPUT_PROPAGATE
        else:
            return WinputAdapter.WINPUT_SUPPRESS
