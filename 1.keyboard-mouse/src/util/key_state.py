from typing import Final

from key import Key, Keys
from tap import Tap
from tap_group import TapGroup
from util.misc import flatten_to_list


def get_vk(key: int | Key | str) -> int:
    int_key: int = -1  # mypy made me do it!
    if isinstance(key, int):
        int_key = key
    if isinstance(key, Key):
        int_key = key.get_vk_code()
    elif isinstance(key, str):
        found = Keys.by_str(key)
        if not found:
            raise ValueError(f"Tried to emulate press of {key}, but didn't find it in Keys.")
        int_key = found.get_vk_code()
    return int_key


class KeypressManager:
    """
    Manages real vs tapper-emitted key presses
    """

    _emulated_press_count: Final[dict[int, int]] = {}
    """ key_vk: amount of times to be emulate-pressed """

    _emulated_release_count: Final[dict[int, int]] = {}
    """ key_vk: amount of times to be emulate-released """

    keys_pressed: Final[set[int]] = set()

    @classmethod
    def will_emulate_press(cls, key: int | Key | str) -> None:
        int_key = get_vk(key)
        key_count = cls._emulated_press_count
        if int_key not in key_count:
            key_count[int_key] = 0
        key_count[int_key] += 1

    @classmethod
    def will_emulate_release(cls, key: int | Key | str) -> None:
        int_key = get_vk(key)
        key_count = cls._emulated_release_count
        if int_key not in key_count:
            key_count[int_key] = 0
        key_count[int_key] += 1

    @classmethod
    def was_pressed_real(cls, vk: int) -> bool:
        """
        :return: True if press was real and should be propagated
        """
        key_count = cls._emulated_press_count
        if vk in key_count and key_count[vk] > 0:
            key_count[vk] -= 1
            return False
        else:
            cls.keys_pressed.add(vk)
            return True

    @classmethod
    def was_released_real(cls, vk: int) -> bool:
        """
        :return: True if release was real and should be propagated
        """
        key_count = cls._emulated_release_count
        if vk in key_count and key_count[vk] > 0:
            key_count[vk] -= 1
            return False
        else:
            cls.keys_pressed.remove(vk)
            return True


class HotkeyMatcher:
    @classmethod
    def active_hotkeys_with_trigger(cls, vk: int) -> list[Tap]:
        """
        :return: In order of relevance - first hotkey that also matches other
        conditions should get triggered
        """
        from tapper import Tapper
        
        if Tapper().suspended():  # counting on singleton. rework after poc
            return cls.candidates_from_group(Tapper().controlGroup, vk)
        return flatten_to_list([cls.candidates_from_group(g, vk) for g in Tapper().groups])

    @classmethod
    def candidates_from_group(cls, group: TapGroup, vk: int) -> list[Tap]:
        taps = group._taps
        if group._always_active:
            return [tap for tap in taps if cls.trigger_key_match(tap, vk)]
        else:
            if group.suspended():
                return []
            match = []
            for tap in taps:
                if not tap.suspended() and cls.trigger_key_match(tap, vk):
                    match.append(tap)
            return match

    @classmethod
    def trigger_key_match(cls, tap: Tap, vk: int) -> bool:
        return vk in tap.trigger_key.all_vk_codes
