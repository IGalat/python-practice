import re
from dataclasses import dataclass
from enum import Enum
from typing import Pattern, ClassVar, Final

from key import Key, Keys, Symbol


class KeyActionOptions(str, Enum):
    CLICK = ""
    PRESS = "down"
    RELEASE = "up"


@dataclass
class KeyAction:
    vk_code: int
    action_option: KeyActionOptions


class ParseError(Exception):
    pass


class InputStringParser:
    pattern: ClassVar[Pattern] = re.compile("\$\([a-zA-Z0-9 ]+\)")
    dummy_char: Final[str] = chr(0x101111)
    watched_shift_mods: list[Key] = [Keys.left_shift, Keys.right_shift]  # have vk codes

    @classmethod
    def parse(cls, text: str, pressed: set[int]) -> list[KeyAction]:
        key_actions: list[KeyAction] = []
        text, replaced = cls.replace_patterns(text)

        real_mods_pressed = [mod for mod in cls.watched_shift_mods if mod.vk_code in pressed]

        for i, char in enumerate(text):
            if char == cls.dummy_char:
                key_actions.append(replaced[i])
            else:
                key_found = Keys.by_str(char)
                if not key_found:
                    raise ParseError(text, char)
                if isinstance(key_found, Symbol) and real_mods_pressed and len(text) > 1:
                    for mod in real_mods_pressed:
                        key_actions.append(KeyAction(mod.vk_code, KeyActionOptions.RELEASE))
                        real_mods_pressed.remove(mod)

                key_actions.extend(cls.get_actions(char, key_found))

        if were_pressed := cls.previously_pressed_modifiers(key_actions, pressed):
            restore = [KeyAction(vk, KeyActionOptions.PRESS) for vk in were_pressed]
            key_actions.extend(restore)

        return key_actions

    @classmethod
    def get_actions(cls, char: str, key: Key) -> list[KeyAction]:
        if isinstance(key, Symbol) and key.uppercase == char:
            return [
                KeyAction(Keys.shift.get_vk_code(), KeyActionOptions.PRESS),
                KeyAction(key.get_vk_code(), KeyActionOptions.CLICK),
                KeyAction(Keys.shift.get_vk_code(), KeyActionOptions.RELEASE),
            ]
        else:
            return [KeyAction(key.get_vk_code(), KeyActionOptions.CLICK)]

    @classmethod
    def previously_pressed_modifiers(cls, key_actions: list[KeyAction], pressed: set[int]) -> set[int]:
        watched_mods_were_pressed = [mod for mod in cls.watched_shift_mods if mod.vk_code in pressed]
        if not watched_mods_were_pressed:
            return set()

        pressed = set(
            [
                mod.vk_code
                for mod in cls.watched_shift_mods
                if mod.vk_code in pressed and cls.released(mod.vk_code, key_actions)
            ]
        )
        return pressed

    @classmethod
    def released(cls, vk: int, key_actions: list[KeyAction]) -> bool:
        """
        If last thing that happened to a key was CLICK or RELEASE.
        """
        for action in reversed(key_actions):
            if action.vk_code == vk:
                if action.action_option in [KeyActionOptions.PRESS, KeyActionOptions.RELEASE]:
                    return True
                else:
                    return False
        return False

    @classmethod
    def replace_patterns(cls, text: str) -> tuple[str, dict[int, KeyAction]]:
        replaced: dict[int, KeyAction] = {}
        while match := cls.pattern.search(text):
            values = match.group()[2:-1].split(" ")
            if (length := len(values)) > 2:
                raise ParseError(text, match.group())
            elif length == 2:
                option = KeyActionOptions(values[1])
            elif length == 1:
                option = KeyActionOptions.CLICK
            else:
                raise ParseError(text, match.group())

            key_str: str = values[0]
            key = Keys.by_str(key_str)
            if not key:
                raise ParseError(text, key_str)

            index = match.start()
            text = text.replace(match.group(), cls.dummy_char, 1)
            replaced[index] = KeyAction(key.get_vk_code(), option)
        return text, replaced
