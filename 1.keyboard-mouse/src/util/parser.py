import re
from dataclasses import dataclass
from enum import Enum
from typing import Pattern, ClassVar, Final

from key import Key, Keys


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
    pattern: ClassVar[Pattern] = re.compile("\$\{[a-zA-Z1-9 ]+}")
    dummy_char: Final[str] = chr(0x101111)

    @classmethod
    def parse(cls, text: str) -> list[KeyAction]:
        key_actions: list[KeyAction] = []
        replaced: dict[int, KeyAction] = {}

        # replace all ${key action}
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
            key: Key = Keys.by_str(key_str)
            if not key:
                raise ParseError(text, key_str)

            index = match.start()
            text = text.replace(match.group(), cls.dummy_char, 1)
            replaced[index] = KeyAction(key.get_vk_code(), option)

        for i, char in enumerate(text):
            if char == cls.dummy_char:
                key_actions.append(replaced[i])
            else:
                key_found = Keys.by_str(char)
                if not key_found:
                    raise ParseError(text, char)
                key_actions.append(KeyAction(key_found.get_vk_code(), KeyActionOptions.CLICK))

        return key_actions
