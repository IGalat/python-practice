from dataclasses import dataclass
from typing import Optional, Callable

from interfaces import Suspendable
from key import Key, Keys
from util.misc import is_tuple_of, func_repr


def keys_from_string(key_str: str | list[str]) -> list[Key]:
    if isinstance(key_str, str):
        key_str = key_str.split("+")
    keys: list[Key] = []
    for key in key_str:
        found = Keys.by_str(key)
        if not found:
            raise ValueError(f"Could not find key corresponding to '{key}'")
        keys.append(found)
    return keys


def to_keys(hotkey: Key | tuple[Key, ...] | str | tuple[str, ...]) -> tuple[Key, tuple[Key, ...]]:
    """Returns (trigger_key, (additional_keys))"""
    keys: tuple[Key, ...]
    if (one := isinstance(hotkey, Key)) or is_tuple_of(hotkey, Key):
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


def to_action(action: Callable | str) -> Callable:
    if callable(action):
        return action
    elif isinstance(action, str):
        from util.controller import Controller

        return lambda: Controller.send(action)
    else:
        raise TypeError(type(action))


@dataclass(init=False, repr=False)
class Tap(Suspendable):
    additional_keys: tuple[Key, ...]
    """ For hotkey, these have to be pressed """

    trigger_key: Key
    """ Main key that's watched. Last in key combination supplied """

    action: Optional[Callable]  # todo accept *args **kwargs, and in trigger_if
    """
    None - key will be typed as usual
    otherwise - will suppress trigger_key but not others
    """

    interrupt_on_suspend: bool
    """ Should action be interrupted when hotkey, its group, or tapper is suspended? """

    suppress_trigger_key_on_action: bool

    no_additional_keys: bool
    """
    When True: if any keys other than specified are pressed, hotkey isn't triggered
    """

    trigger_if: Optional[Callable]
    """ 
    If function is supplied here, it runs each time before hotkey is triggered.
    When it returns True, action runs as usual.
    When it returns False, key is typed as when action = None.
    """

    _parent: Optional[Suspendable] = None

    def __init__(
        self,
        hotkey: Key | tuple[Key, ...] | str | tuple[str, ...],
        action: Optional[Callable] | str,
        *,
        interrupt_on_suspend: bool = True,
        suppress_trigger_key_on_action: bool = True,
        no_additional_keys: bool = False,
        trigger_if: Optional[Callable] = None,
    ):
        """
        :param hotkey: Trigger keys for hotkey or hotstring.
        Examples: Keys.a; [Keys.shift, Keys.ctrl, Keys.plus]; "alt+shift+f11"
        """

        self.trigger_key, self.additional_keys = to_keys(hotkey)
        self.action = to_action(action)
        self.interrupt_on_suspend = interrupt_on_suspend
        self.suppress_trigger_key_on_action = suppress_trigger_key_on_action
        self.no_additional_keys = no_additional_keys
        self.trigger_if = trigger_if
        self.unsuspend()

    def __repr__(self) -> str:
        desc = [f"trigger_key={self.trigger_key}"]
        if self.additional_keys:
            desc.append(f"additional_keys={self.additional_keys}")
        desc.append(f"action={func_repr(self.action)}")
        if not self.interrupt_on_suspend:
            desc.append(f"interrupt_on_suspend={self.interrupt_on_suspend}")
        if not self.suppress_trigger_key_on_action:
            desc.append(f"suppress_trigger_key_on_action={self.suppress_trigger_key_on_action}")
        if self.trigger_if:
            desc.append(f"trigger_if={func_repr(self.trigger_if)}")
        if self._parent and hasattr(self._parent, "name"):
            desc.append(f"parent_name='{self._parent.name}'")  # type:ignore
        desc.append(super().__repr__())
        return "Tap(" + ",".join(desc) + ")"

    def suspended(self) -> bool:
        return (self._suspended or self._parent.suspended()) is not None

    def same_hotkey(self, hotkey: tuple[Key, tuple[Key, ...]]) -> bool:
        return (self.trigger_key, self.additional_keys) == hotkey


# def __eq__ # todo comparison with aliases, str, etc. , __ne__
