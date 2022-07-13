from typing import Optional, Callable, List

import attrs

from key import Key, Keys
from util.misc import is_list_of


def suppress_keystroke() -> None:
    """
    Marker function for disabling (suppressing) a keystroke.
    Use as "action" in Tap.
    """
    pass


def keys_from_string(key_str: str | List[str]) -> List[Key]:
    if isinstance(key_str, str):
        key_str = key_str.split("+")  # todo split a++ to a, +
    return [Keys[key] for key in key_str]  # todo look in Key.input_variants as fallback


def to_keys(hotkey: Key | List[Key] | str | List[str]) -> List[Key]:
    if isinstance(hotkey, Key):
        keys = [hotkey]
    elif is_list_of(hotkey, Key):
        keys = hotkey  # type:ignore # todo mypy
    elif isinstance(hotkey, str) or is_list_of(hotkey, str):
        keys = keys_from_string(hotkey)
    else:
        raise TypeError("Incorrect type of hotkey")
    return keys


@attrs.define
class Tap:
    additional_keys: List[Key]
    """ For hotkey, these have to be pressed """

    trigger_key: Key
    """ Main key that's watched. Last in key combination supplied """

    action: Optional[Callable]
    """
    None - key will be pressed as usual
    suppress_keystroke - marker function, will suppress trigger_key but not others
    """

    interrupt_on_suspend: bool
    """ Should action be interrupted when hotkey, its group, or tapper is suspended? """

    def __init__(
        self, hotkey: Key | List[Key] | str | List[str], action: Optional[Callable], interrupt_on_suspend: bool = True
    ) -> None:
        """
        :param hotkey: Trigger keys for hotkey or hotstring.
        Examples: Keys.a; [Keys.shift, Keys.ctrl, Keys.plus]; "alt+shift+f11"
        """

        keys = to_keys(hotkey)
        self.trigger_key = keys[-1]
        self.additional_keys = keys[:-1]
        self.action = action
        self.interrupt_on_suspend = interrupt_on_suspend

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)  # todo comparison with aliases, str, etc. __ne__
