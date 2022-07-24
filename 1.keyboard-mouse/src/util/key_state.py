from typing import Final

from key import Key, get_vk, Keys
from tap import Tap
from tap_group import TapGroup
from util.misc import flatten_to_list


class KeypressManager:
    """
    Manages real vs tapper-emitted key presses
    """

    _emulated_press_count: Final[dict[int, int]] = {}
    """ key_vk: amount of times to be emulate-pressed """

    _emulated_release_count: Final[dict[int, int]] = {}
    """ key_vk: amount of times to be emulate-released """

    _keys_pressed: Final[set[int]] = set()

    @classmethod
    def keys_pressed(cls) -> set[int]:
        return cls._keys_pressed

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
            if vk not in [Keys.scroll_wheel_up.vk_code, Keys.scroll_wheel_down.vk_code]:
                cls.keys_pressed().add(vk)
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
            cls.remove_from_pressed(vk)
            return True

    @classmethod
    def remove_from_pressed(cls, vk: int) -> None:
        try:
            cls.keys_pressed().remove(vk)
        except KeyError:
            pass  # todo GetKeyState of all keys in set

    @classmethod
    def is_pressed(cls, key: int | Key) -> bool:
        if isinstance(key, Key):
            return any(vk in cls.keys_pressed() for vk in key.all_vk_codes)
        else:
            return key in cls.keys_pressed()


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
        taps = group.get_all()
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
