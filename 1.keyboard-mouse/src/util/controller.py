import time
from typing import Any
from typing import Final
from typing import Optional

from adapter import BaseAdapter
from config import Config
from key import get_vk
from key import Key
from key import Keys
from util.key_state import KeypressManager
from util.parser import InputStringParser
from util.parser import KeyAction
from util.parser import KeyActionOptions
from winadapter.base import Window
from winadapter.base import WindowAdapterBase


class Controller:
    @classmethod
    def adapter(cls) -> BaseAdapter:
        return Config.adapter

    @classmethod
    def winadapter(cls) -> WindowAdapterBase:
        return Config.winadapter

    @classmethod
    def sleep_between_actions(cls) -> None:
        time.sleep(Config.controller_interval_sec)

    @classmethod
    def press(cls, key: int | Key | str, real: bool = False) -> None:
        vk_code = get_vk(key)
        if not real:
            KeypressManager.will_emulate_press(vk_code)
        cls.adapter().press_key(vk_code)
        cls.sleep_between_actions()

    @classmethod
    def release(cls, key: int | Key | str, real: bool = False) -> None:
        vk_code = get_vk(key)
        if not real:
            KeypressManager.will_emulate_release(vk_code)
        cls.adapter().release_key(vk_code)
        cls.sleep_between_actions()

    @classmethod
    def release_all_keys(cls) -> None:
        for vk in KeypressManager.keys_pressed().copy():
            cls.release(vk, real=True)

    @classmethod
    def send_key(cls, key: int | Key | str, real: bool = False) -> None:
        cls.press(key, real)
        cls.release(key, real)

    @classmethod
    def send(cls, *keys: int | Key | str, real: bool = False) -> None:
        for arg in keys:
            if isinstance(arg, int):
                cls.send_key(arg, real)
            elif isinstance(arg, Key):
                cls.send_key(arg.get_vk_code(), real)
            elif isinstance(arg, str):
                parsed: list[KeyAction] = InputStringParser.parse(
                    arg, KeypressManager.keys_pressed()
                )
                for doit in parsed:
                    actions[doit.action_option](doit.vk_code, real)

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
    def click(
        cls,
        key: int | Key | str | list | tuple,
        x: Optional[int] = None,
        y: Optional[int] = None,
    ) -> None:
        cls.mouseover(x, y)
        if not isinstance(key, (list, tuple)):
            key = [key]
        cls.send(*key)

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
        return cls.winadapter().get_open(
            exec_or_title, handle=handle, pid=pid, exec=exec, title=title
        )

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
        return cls.winadapter().get_fore(
            exec_or_title, handle=handle, pid=pid, exec=exec, title=title
        )

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
        # no idea why this works :D without it, only works if script console is in foreground
        cls.click(Keys.alt)
        return cls.winadapter().set_fore(
            exec_or_title, handle=handle, pid=pid, exec=exec, title=title
        )


actions: Final[dict] = {
    KeyActionOptions.CLICK: Controller.send_key,
    KeyActionOptions.PRESS: Controller.press,
    KeyActionOptions.RELEASE: Controller.release,
}
