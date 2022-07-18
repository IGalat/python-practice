from dataclasses import dataclass
from typing import Optional, Callable

from interfaces import Suspendable
from key import Key, Keys
from util.misc import is_tuple_of


def keys_from_string(key_str: str | list[str]) -> list[Key]:
    if isinstance(key_str, str):
        key_str = key_str.split("+")  # todo split a++ to a, +
    keys: list[Key] = [Keys[key] for key in key_str]  # todo look in Key.input_variants as fallback;
    return keys


def to_keys(hotkey: Key | tuple[Key, ...] | str | tuple[str, ...]) -> tuple[Key, tuple[Key, ...]]:
    """Returns (trigger_key, [additional_keys])"""
    keys: tuple[Key, ...]
    if one := isinstance(hotkey, Key) or is_tuple_of(hotkey, Key):
        if one:
            hotkey = (hotkey,)
        keys = hotkey
    elif isinstance(hotkey, str) or is_tuple_of(hotkey, str):
        keys = (*keys_from_string(hotkey),)
    else:
        raise TypeError(f"{hotkey} is incorrect type of hotkey")
    if not keys or len(keys) >= 20:
        raise ValueError(f"{hotkey} must have >0 and <20 keys. Resulting keys: {keys}")
    return keys[-1], keys[:-1]


@dataclass(init=False)
class Tap(Suspendable):
    additional_keys: tuple[Key, ...]
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

    suppress_trigger_key_on_action: bool

    trigger_if: Optional[Callable]
    """ 
    If function is supplied here, it runs each time before hotkey is triggered.
    When it returns True, action runs as usual.
    When it returns False, key is typed as when action = None.
    """

    _parent: Optional[Suspendable] = None

    def __init__(
            self,
            hotkey: Key | tuple[Key] | str | tuple[str],
            action: Optional[Callable],
            *,
            interrupt_on_suspend: bool = True,
            suppress_trigger_key_on_action: bool = True,
            trigger_if: Callable = None,
    ):
        """
        :param hotkey: Trigger keys for hotkey or hotstring.
        Examples: Keys.a; [Keys.shift, Keys.ctrl, Keys.plus]; "alt+shift+f11"
        """

        self.trigger_key, self.additional_keys = to_keys(hotkey)
        self.action = action
        self.interrupt_on_suspend = interrupt_on_suspend
        self.suppress_trigger_key_on_action = suppress_trigger_key_on_action
        self.trigger_if = trigger_if
        self.unsuspend()

    def suspended(self) -> bool:
        return not self._suspended and not self._parent.suspended()  # type:ignore # todo mypy

    def same_hotkey(self, hotkey: tuple[Key, tuple[Key, ...]]) -> bool:
        return (self.trigger_key, self.additional_keys) == hotkey

# def __eq__ # todo comparison with aliases, str, etc. , __ne__
