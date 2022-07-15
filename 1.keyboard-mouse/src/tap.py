from typing import Optional, Callable, List

import attrs

from key import Key, Keys
from util.misc import is_list_of


def keys_from_string(key_str: str | List[str]) -> List[Key]:
    if isinstance(key_str, str):
        key_str = key_str.split("+")  # todo split a++ to a, +
    return [Keys[key] for key in key_str]  # todo look in Key.input_variants as fallback;


def to_keys(hotkey: Key | List[Key] | str | List[str]) -> List[Key]:
    if isinstance(hotkey, Key):
        keys = [hotkey]
    elif is_list_of(hotkey, Key):
        keys = hotkey  # type:ignore # todo mypy
    elif isinstance(hotkey, str) or is_list_of(hotkey, str):
        keys = keys_from_string(hotkey)
    else:
        raise TypeError(f"{hotkey} is incorrect type of hotkey")
    if len(keys) == 0 or len(keys) >= 20:
        raise ValueError(f"{hotkey} must have >0 and <20 keys. Resulting keys: {keys}")
    return keys


@attrs.define
class Tap:
    additional_keys: List[Key]
    """ For hotkey, these have to be pressed """

    trigger_key: Key
    """ Main key that's watched. Last in key combination supplied """

    action: Optional[Callable]
    """
    None - key will be typed as usual
    otherwise - will suppress trigger_key but not others
    """

    interrupt_on_suspend: bool
    """ Should action be interrupted when hotkey, its group, or tapper is suspended? """

    trigger_if: Optional[Callable] = None
    """ 
    If function is supplied here, it runs each time before hotkey is triggered.
    When it returns True, action runs as usual.
    When it returns False, key is typed as when action = None.
    """

    def __init__(
        self,
        hotkey: Key | List[Key] | str | List[str],
        action: Optional[Callable],
        *,
        interrupt_on_suspend: bool = True,
        trigger_if: Callable = None,
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
        self.trigger_if = trigger_if

    # def __eq__ # todo comparison with aliases, str, etc. , __ne__
