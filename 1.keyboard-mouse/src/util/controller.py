import time
from typing import Final, Optional

from adapter import BaseAdapter
from config import Config
from key import Key, get_vk
from util.key_state import KeypressManager
from util.parser import InputStringParser, KeyAction, KeyActionOptions


class Controller:
    @classmethod
    def adapter(cls) -> BaseAdapter:
        return Config.adapter

    @classmethod
    def sleep_between_actions(cls) -> None:
        time.sleep(Config.controller_interval_sec)

    @classmethod
    def press(cls, key: int | Key | str) -> None:
        vk_code = get_vk(key)
        KeypressManager.will_emulate_press(vk_code)
        cls.adapter().press_key(vk_code)
        cls.sleep_between_actions()

    @classmethod
    def release(cls, key: int | Key | str) -> None:
        vk_code = get_vk(key)
        KeypressManager.will_emulate_release(vk_code)
        cls.adapter().release_key(vk_code)
        cls.sleep_between_actions()

    @classmethod
    def send_key(cls, key: int | Key | str) -> None:
        cls.press(key)
        cls.release(key)

    @classmethod
    def send(cls, *keys: int | Key | str) -> None:
        for arg in keys:
            if isinstance(arg, int):
                cls.send_key(arg)
            elif isinstance(arg, Key):
                cls.send_key(arg.get_vk_code())
            elif isinstance(arg, str):
                parsed: list[KeyAction] = InputStringParser.parse(arg, KeypressManager.keys_pressed())
                for doit in parsed:
                    actions[doit.action_option](doit.vk_code)

    @classmethod
    def pressed(cls, key: int | Key | str) -> bool:
        vk_code = get_vk(key)
        return cls.adapter().pressed(vk_code)

    @classmethod
    def toggled(cls, key: int | Key | str) -> bool:
        vk_code = get_vk(key)
        return cls.adapter().toggled(vk_code)

    @classmethod
    def get_mouse_pos(cls) -> tuple[int, int]:
        return cls.adapter().get_mouse_pos()

    @classmethod
    def mouseover(cls, x: Optional[int], y: Optional[int]) -> None:
        if x is None and y is None:
            return
        if x is None or y is None:
            was_x, was_y = cls.adapter().get_mouse_pos()
            if x is None:
                x = was_x
            else:
                y = was_y
        cls.adapter().set_mouse_pos(x, y)

    @classmethod
    def move_mouse_delta(cls, dx: int, dy: int) -> None:
        cls.adapter().move_mouse(dx, dy)

    @classmethod
    def click(cls, key: int | Key | str | list | tuple, x: Optional[int] = None, y: Optional[int] = None) -> None:
        cls.mouseover(x, y)
        if not isinstance(key, (list, tuple)):
            key = [key]
        [cls.send_key(k) for k in key]


actions: Final[dict] = {
    KeyActionOptions.CLICK: Controller.send_key,
    KeyActionOptions.PRESS: Controller.press,
    KeyActionOptions.RELEASE: Controller.release,
}
