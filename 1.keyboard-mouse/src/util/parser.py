import re
from dataclasses import dataclass
from enum import Enum
from typing import Pattern, ClassVar, Final

from key import Key, Keys, Symbol
from util.misc import flatten_to_list


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
    pattern: ClassVar[Pattern] = re.compile("\$\([a-zA-Z0-9+_ ]+\)")
    dummy_char: Final[str] = chr(0x101111)
    watched_shift_mods: list[Key] = [Keys.left_shift, Keys.right_shift]  # have vk codes

    @classmethod
    def parse(cls, text: str, pressed: set[int]) -> list[KeyAction]:
        key_actions: list[KeyAction] = []
        text, replaced = cls.replace_patterns(text)

        real_mods_pressed = [mod for mod in cls.watched_shift_mods if mod.vk_code in pressed]

        for i, char in enumerate(text):
            if char == cls.dummy_char:
                key_actions.extend(replaced[i])
            else:
                key_found = Keys.by_str(char)
                if not key_found:
                    raise ParseError(text, char)
                if isinstance(key_found, Symbol) and real_mods_pressed and len(text) > 1:
                    for mod in real_mods_pressed:
                        key_actions.append(KeyAction(mod.vk_code, KeyActionOptions.RELEASE))
                        real_mods_pressed.remove(mod)

                key_actions.extend(cls.get_actions(char, key_found))

        if were_pressed := cls.previously_pressed_modifiers(key_actions, pressed, replaced):
            restore = [KeyAction(vk, KeyActionOptions.PRESS) for vk in were_pressed]
            key_actions.extend(restore)

        return key_actions

    @classmethod
    def get_actions(cls, char: str, key: Key) -> list[KeyAction]:
        if isinstance(key, Symbol) and key.uppercase == char:
            return cls._surround([KeyAction(key.get_vk_code(), KeyActionOptions.CLICK)], Keys.shift.get_vk_code())
        else:
            return [KeyAction(key.get_vk_code(), KeyActionOptions.CLICK)]

    @classmethod
    def _surround(cls, inner: list[KeyAction], vk_code: int) -> list[KeyAction]:
        return [KeyAction(vk_code, KeyActionOptions.PRESS), *inner, KeyAction(vk_code, KeyActionOptions.RELEASE)]

    @classmethod
    def previously_pressed_modifiers(
        cls, key_actions: list[KeyAction], pressed: set[int], replaced: dict[int, list[KeyAction]]
    ) -> set[int]:
        watched_mods_were_pressed = [mod for mod in cls.watched_shift_mods if mod.vk_code in pressed]
        if not watched_mods_were_pressed:
            return set()

        were_replaced = [vk for vk in flatten_to_list(*replaced.values())]
        pressed = set(
            [
                mod.vk_code
                for mod in cls.watched_shift_mods
                if mod.vk_code in pressed
                and cls.released(mod.vk_code, key_actions)
                and mod.vk_code not in were_replaced
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
    def replace_patterns(cls, text: str) -> tuple[str, dict[int, list[KeyAction]]]:
        replaced: dict[int, list[KeyAction]] = {}
        while match := cls.pattern.search(text):
            pattern = match.group()[2:-1]
            if "+" in pattern:
                actions = cls.parse_key_combo(pattern)
            else:
                actions = [cls.parse_single_keystroke(pattern, 2)]

            index = match.start()
            text = text.replace(match.group(), cls.dummy_char, 1)
            replaced[index] = actions
        return text, replaced

    # no ups or downs, for now
    @classmethod
    def parse_key_combo(cls, text: str) -> list[KeyAction]:
        strokes = text.split("+")
        if len(strokes) < 2:
            raise ParseError(f"Key combo '{text}' should have more than one key")
        vks = [cls.parse_single_keystroke(s, 1).vk_code for s in strokes]
        vks.reverse()
        combo = [KeyAction(vks[0], KeyActionOptions.CLICK)]
        for vk in vks[1:]:
            combo = cls._surround(combo, vk)
        return combo

    @classmethod
    def parse_single_keystroke(cls, text: str, max_len: int) -> KeyAction:
        if max_len == 1:
            option = KeyActionOptions.CLICK
            key_str = text
        else:
            # "alt up" and similar
            values = text.split(" ")
            if (length := len(values)) > max_len:
                raise ParseError(text)
            elif length == 2:
                option = KeyActionOptions(values[1])
            elif length == 1:
                option = KeyActionOptions.CLICK
            else:
                raise ParseError(text)
            key_str: str = values[0]

        key = Keys.by_str(key_str)
        if not key:
            raise ParseError(text, key_str)

        return KeyAction(key.get_vk_code(), option)
