import time
from typing import Final

from adapter import BaseAdapter
from config import Config
from key import Key, get_vk
from util.key_state import KeypressManager
from util.parser import InputStringParser, KeyAction, KeyActionOptions


class KeyboardController:

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
    def click(cls, key: int | Key | str) -> None:
        cls.press(key)
        cls.release(key)

    @classmethod
    def send(cls, *keys: int | Key | str) -> None:
        for arg in keys:
            if isinstance(arg, int):
                cls.click(arg)
            elif isinstance(arg, Key):
                cls.click(arg.get_vk_code())
            elif isinstance(arg, str):
                parsed: list[KeyAction] = InputStringParser.parse(arg, KeypressManager.keys_pressed())
                for doit in parsed:
                    actions[doit.action_option](doit.vk_code)


actions: Final[dict] = {
    KeyActionOptions.CLICK: KeyboardController.click,
    KeyActionOptions.PRESS: KeyboardController.press,
    KeyActionOptions.RELEASE: KeyboardController.release,
}
