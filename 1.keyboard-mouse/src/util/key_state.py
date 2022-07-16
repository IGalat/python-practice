from typing import Final

from key import Key, Keys


class EmulatedKeypressManager:
    """
    Manages tapper-emitted key presses and differentiates them from real
    """

    _emulated_press_count: Final[dict[int, int]] = {}
    """ key_vk: amount of times to be emulate-pressed """

    @classmethod
    def will_emulate_press(cls, key: int | Key | str) -> None:
        if isinstance(key, int):
            int_key = key
        elif isinstance(key, Key):
            int_key = key.get_vk_code()
        elif isinstance(key, str):
            found = Keys.by_str(key)
            if not found:
                raise ValueError(f"Tried to emulate press of {key}, but didn't find it in Keys.")
            int_key = found.get_vk_code()
        key_count = cls._emulated_press_count
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
            return True
