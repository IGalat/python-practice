from typing import Final

from key import Key


class EmulatedKeypressManager:
    """
    Manages tapper-emitted key presses and differentiates them from real
    """
    _emulated_press_count: Final[dict[int, int]] = {}
    """ key_vk: amount of times to be emulate-pressed """

    @classmethod
    def will_emulate_press(cls, vk: int | Key) -> None:
        if isinstance(vk, Key):
            vk = vk.get_vk_code()
        key_count = cls._emulated_press_count
        if vk not in key_count:
            key_count[vk] = 0
        key_count[vk] += 1

    @classmethod
    def was_pressed(cls, vk: int) -> bool:
        """
        :return: True if press was real and should be propagated
        """
        key_count = cls._emulated_press_count
        if key_count[vk] > 0:
            key_count[vk] -=1
            return False
        else:
            return True



